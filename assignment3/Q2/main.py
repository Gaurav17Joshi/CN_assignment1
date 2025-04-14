# main.py
#!/usr/bin/env python

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.node import Controller, OVSController
from mininet.link import TCLink
import argparse
import sys
import time

# Import our topology classes
from topology import NetworkLoopTopo, NATTopo
# Import test functions
from tests import run_all_tests

def configure_nat(net):
    """Configure NAT functionality on h9"""
    h9 = net.get('h9')
    h1 = net.get('h1')
    h2 = net.get('h2')
    
    # Configure the interfaces on h9
    # h9-eth0 is connected to s1 (external interface)
    # h9-eth1 is connected to h1 (internal interface)
    # h9-eth2 is connected to h2 (internal interface)
    
    # Set up the external interface with public IP
    h9.cmd('ifconfig h9-eth0 172.16.10.10/24')
    
    # Set up the internal interfaces with the gateway IP
    h9.cmd('ifconfig h9-eth1 10.1.1.1/24')
    h9.cmd('ifconfig h9-eth2 10.1.1.1/24')
    
    # Enable IP forwarding
    h9.cmd('sysctl -w net.ipv4.ip_forward=1')
    
    # Set up NAT (masquerading)
    h9.cmd('iptables -t nat -A POSTROUTING -s 10.1.1.0/24 -o h9-eth0 -j SNAT --to-source 172.16.10.10')
    
    # Allow established connections
    h9.cmd('iptables -A FORWARD -i h9-eth0 -o h9-eth1 -m state --state RELATED,ESTABLISHED -j ACCEPT')
    h9.cmd('iptables -A FORWARD -i h9-eth0 -o h9-eth2 -m state --state RELATED,ESTABLISHED -j ACCEPT')
    
    # Allow outgoing connections from internal network
    h9.cmd('iptables -A FORWARD -i h9-eth1 -o h9-eth0 -j ACCEPT')
    h9.cmd('iptables -A FORWARD -i h9-eth2 -o h9-eth0 -j ACCEPT')
    
    # Make sure h1 and h2 have the correct default route
    h1.cmd('ip route del default')
    h1.cmd('ip route add default via 10.1.1.1')
    h2.cmd('ip route del default')
    h2.cmd('ip route add default via 10.1.1.1')
    
    # Add port forwarding rules for specific services
    # For h1 (ping and iperf)
    h9.cmd('iptables -t nat -A PREROUTING -d 172.16.10.10 -p icmp --icmp-type echo-request -j DNAT --to-destination 10.1.1.2')
    h9.cmd('iptables -t nat -A PREROUTING -d 172.16.10.10 -p tcp --dport 5201 -j DNAT --to-destination 10.1.1.2:5201')
    
    # For h2 (using a different port for iperf)
    h9.cmd('iptables -t nat -A PREROUTING -d 172.16.10.10 -p tcp --dport 5202 -j DNAT --to-destination 10.1.1.3:5201')
    
    # Add secondary IP in the 10.0.0.0/24 network for connectivity with other hosts
    h9.cmd('ip addr add 10.0.0.10/24 dev h9-eth0')
    
    # Add routes on all hosts to reach 172.16.10.0/24 via h9's 10.0.0.10 address
    for host_name in ['h3', 'h4', 'h5', 'h6', 'h7', 'h8']:
        host = net.get(host_name)
        host.cmd('ip route add 172.16.10.0/24 via 10.0.0.10')
    
    info('*** NAT configured on h9\n')
    info('*** NAT rules:\n')
    info(h9.cmd('iptables -t nat -L -v -n'))
    info(h9.cmd('iptables -L FORWARD -v -n'))

def run_network(topo_type, run_tests=False):
    """Create and run the network with the specified topology"""
    
    # Create the appropriate topology
    if topo_type == 'loop':
        topo = NetworkLoopTopo()
        info('*** Using NetworkLoopTopo\n')
    elif topo_type == 'nat':
        topo = NATTopo()
        info('*** Using NATTopo\n')
    else:
        sys.exit(f"Unknown topology type: {topo_type}")
    
    # Create the network
    net = Mininet(topo=topo, controller=OVSController, link=TCLink)
    
    # Start the network
    info('*** Starting network\n')
    net.start()
    
    # Configure NAT if needed
    if topo_type == 'nat':
        configure_nat(net)
    
    # Run tests if specified
    if run_tests and topo_type == 'nat':
        run_all_tests(net)
    
    # Run the CLI
    info('*** Running CLI\n')
    CLI(net)
    
    # Stop the network
    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run network with specified topology')
    parser.add_argument('--topo', choices=['loop', 'nat'], default='loop',
                        help='Topology type: loop (default) or nat')
    parser.add_argument('--test', action='store_true',
                        help='Run tests automatically')
    args = parser.parse_args()
    
    # Configure logging
    setLogLevel('info')
    
    # Run the network
    run_network(args.topo, args.test)
