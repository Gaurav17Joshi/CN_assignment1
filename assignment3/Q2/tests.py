import time
import re
from mininet.log import info

def run_ping_test(net, source, dest, count=4):
    """Run a ping test between two hosts"""
    source_host = net.get(source)
    dest_host = net.get(dest)
    
    info(f'*** Testing ping from {source} to {dest}\n')
    
    # Run ping command
    output = source_host.cmd(f'ping -c {count} {dest_host.IP()}')
    
    # Check for ping success
    success = "0% packet loss" in output
    
    # Extract ping statistics
    rtt_match = re.search(r'rtt min/avg/max/mdev = ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+)', output)
    if rtt_match:
        min_rtt, avg_rtt, max_rtt, mdev_rtt = rtt_match.groups()
        info(f'*** Ping results: min={min_rtt}ms, avg={avg_rtt}ms, max={max_rtt}ms\n')
    
    if success:
        info(f'*** Ping from {source} to {dest} succeeded\n')
    else:
        info(f'*** Ping from {source} to {dest} failed\n')
    
    return success, output

def run_ping_test_via_nat(net, source, dest, count=4):
    """Run a ping test from a host to a NAT-ed host"""
    source_host = net.get(source)
    
    info(f'*** Testing ping from {source} to {dest} via NAT\n')
    
    # For pinging internal hosts (h1, h2), use h9's public IP
    dest_ip = '172.16.10.10' if dest in ['h1', 'h2'] else net.get(dest).IP()
    
    # Run ping command
    output = source_host.cmd(f'ping -c {count} {dest_ip}')
    
    # Check for ping success
    success = "0% packet loss" in output
    
    # Extract ping statistics
    rtt_match = re.search(r'rtt min/avg/max/mdev = ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+)', output)
    if rtt_match:
        min_rtt, avg_rtt, max_rtt, mdev_rtt = rtt_match.groups()
        info(f'*** Ping results: min={min_rtt}ms, avg={avg_rtt}ms, max={max_rtt}ms\n')
    
    if success:
        info(f'*** Ping from {source} to {dest} via NAT succeeded\n')
    else:
        info(f'*** Ping from {source} to {dest} via NAT failed\n')
    
    return success, output

def run_iperf3_test(net, server, client, duration=30):
    """Run an iperf3 test between two hosts"""
    server_host = net.get(server)
    client_host = net.get(client)
    
    info(f'*** Running iperf3 test from {client} to {server} for {duration} seconds\n')
    
    # Start iperf3 server
    server_host.cmd(f'iperf3 -s &')
    time.sleep(1)  # Give server time to start
    
    # Run iperf3 client
    output = client_host.cmd(f'iperf3 -c {server_host.IP()} -t {duration}')
    
    # Kill iperf3 server
    server_host.cmd('pkill -f "iperf3 -s"')
    
    # Extract iperf3 results
    bw_match = re.search(r'([\d.]+) ([GMK])bits/sec', output)
    if bw_match:
        bw_value, bw_unit = bw_match.groups()
        info(f'*** Bandwidth: {bw_value} {bw_unit}bits/sec\n')
    
    return output

def run_iperf3_test_via_nat(net, server, client, duration=30, port=5201):
    """Run an iperf3 test between two hosts via NAT"""
    server_host = net.get(server)
    client_host = net.get(client)
    
    info(f'*** Running iperf3 test from {client} to {server} via NAT for {duration} seconds\n')
    
    # Start iperf3 server
    server_host.cmd(f'iperf3 -s -p {port} &')
    time.sleep(1)  # Give server time to start
    
    # Determine the server IP to connect to
    if server in ['h1', 'h2']:
        # Use h9's public IP for internal hosts
        server_ip = '172.16.10.10'
    else:
        server_ip = server_host.IP()
    
    # Run iperf3 client
    output = client_host.cmd(f'iperf3 -c {server_ip} -p {port} -t {duration}')
    
    # Kill iperf3 server
    server_host.cmd(f'pkill -f "iperf3 -s -p {port}"')
    
    # Extract iperf3 results
    bw_match = re.search(r'([\d.]+) ([GMK])bits/sec', output)
    if bw_match:
        bw_value, bw_unit = bw_match.groups()
        info(f'*** Bandwidth: {bw_value} {bw_unit}bits/sec\n')
    
    return output

def list_nat_rules(net):
    """List NAT rules on h9"""
    h9 = net.get('h9')
    
    info('*** NAT forwarding rules (FORWARD chain):\n')
    output = h9.cmd('iptables -L FORWARD -v -n')
    info(output)
    
    info('*** NAT translation rules (NAT table, POSTROUTING chain):\n')
    output = h9.cmd('iptables -t nat -L POSTROUTING -v -n')
    info(output)
    
    info('*** NAT port forwarding rules (NAT table, PREROUTING chain):\n')
    output = h9.cmd('iptables -t nat -L PREROUTING -v -n')
    info(output)
    
    return output

def show_nat_connections(net):
    """Show active NAT connections using conntrack"""
    h9 = net.get('h9')
    
    info('*** Active NAT connections:\n')
    output = h9.cmd('conntrack -L -n')
    info(output)
    
    return output

def run_all_tests(net):
    """Run all the required tests"""
    # Test communication to an external host from an internal host
    info('\n*** Test 1: Communication to an external host from an internal host\n')
    
    # i) Ping to h5 from h1
    run_ping_test(net, 'h1', 'h5')
    list_nat_rules(net)
    show_nat_connections(net)
    
    # ii) Ping to h3 from h2
    run_ping_test(net, 'h2', 'h3')
    list_nat_rules(net)
    show_nat_connections(net)
    
    # Test communication to an internal host from an external host
    info('\n*** Test 2: Communication to an internal host from an external host\n')
    
    # i) Ping to h1 from h8
    run_ping_test_via_nat(net, 'h8', 'h1')
    list_nat_rules(net)
    show_nat_connections(net)
    
    # ii) Ping to h2 from h6
    run_ping_test_via_nat(net, 'h6', 'h2')
    list_nat_rules(net)
    show_nat_connections(net)
    
    # Iperf tests
    info('\n*** Test 3: Iperf tests\n')
    
    # i) Run iperf3 server in h1 and iperf3 client in h6
    run_iperf3_test_via_nat(net, 'h1', 'h6', duration=120, port=5201)
    list_nat_rules(net)
    show_nat_connections(net)
    
    # ii) Run iperf3 server in h8 and iperf3 client in h2
    run_iperf3_test(net, 'h8', 'h2', duration=120)
    list_nat_rules(net)
    show_nat_connections(net)
