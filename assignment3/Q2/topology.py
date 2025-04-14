from mininet.topo import Topo
from mininet.link import TCLink

class NetworkLoopTopo(Topo):
    """
    Topology with 4 switches and 8 hosts forming network loops.
    """
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)
        
        # Add switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        
        # Add hosts
        h1 = self.addHost('h1', ip='10.0.0.2/24')
        h2 = self.addHost('h2', ip='10.0.0.3/24')
        h3 = self.addHost('h3', ip='10.0.0.4/24')
        h4 = self.addHost('h4', ip='10.0.0.5/24')
        h5 = self.addHost('h5', ip='10.0.0.6/24')
        h6 = self.addHost('h6', ip='10.0.0.7/24')
        h7 = self.addHost('h7', ip='10.0.0.8/24')
        h8 = self.addHost('h8', ip='10.0.0.9/24')
        
        # Add links between switches (7ms latency)
        self.addLink(s1, s2, cls=TCLink, delay='7ms')
        self.addLink(s2, s3, cls=TCLink, delay='7ms')
        self.addLink(s3, s4, cls=TCLink, delay='7ms')
        self.addLink(s4, s1, cls=TCLink, delay='7ms')
        self.addLink(s1, s3, cls=TCLink, delay='7ms')
        
        # Add links between hosts and switches (5ms latency)
        self.addLink(h1, s1, cls=TCLink, delay='5ms')
        self.addLink(h2, s1, cls=TCLink, delay='5ms')
        self.addLink(h3, s2, cls=TCLink, delay='5ms')
        self.addLink(h4, s2, cls=TCLink, delay='5ms')
        self.addLink(h5, s3, cls=TCLink, delay='5ms')
        self.addLink(h6, s3, cls=TCLink, delay='5ms')
        self.addLink(h7, s4, cls=TCLink, delay='5ms')
        self.addLink(h8, s4, cls=TCLink, delay='5ms')

class NATTopo(Topo):
    """
    Topology with NAT functionality.
    Adds host h9, which acts as a NAT gateway for hosts h1 and h2.
    """
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)
        
        # Add switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        
        # Add hosts with "external" IP addresses in 10.0.0.0/24
        h3 = self.addHost('h3', ip='10.0.0.4/24')
        h4 = self.addHost('h4', ip='10.0.0.5/24')
        h5 = self.addHost('h5', ip='10.0.0.6/24')
        h6 = self.addHost('h6', ip='10.0.0.7/24')
        h7 = self.addHost('h7', ip='10.0.0.8/24')
        h8 = self.addHost('h8', ip='10.0.0.9/24')
        
        # Add h1 and h2 with private IP addresses in 10.1.1.0/24
        # Set default route via h9's internal interface
        h1 = self.addHost('h1', ip='10.1.1.2/24', defaultRoute='via 10.1.1.1')
        h2 = self.addHost('h2', ip='10.1.1.3/24', defaultRoute='via 10.1.1.1')
        
        # Add NAT host h9 (IP addresses will be set later)
        h9 = self.addHost('h9')
        
        # Add links between switches (7ms latency)
        self.addLink(s1, s2, cls=TCLink, delay='7ms')
        self.addLink(s2, s3, cls=TCLink, delay='7ms')
        self.addLink(s3, s4, cls=TCLink, delay='7ms')
        self.addLink(s4, s1, cls=TCLink, delay='7ms')
        self.addLink(s1, s3, cls=TCLink, delay='7ms')
        
        # Add links for h1, h2, and h9
        self.addLink(h9, s1, cls=TCLink, delay='5ms')  # External interface
        self.addLink(h1, h9, cls=TCLink, delay='5ms')  # h1 connected to h9
        self.addLink(h2, h9, cls=TCLink, delay='5ms')  # h2 connected to h9
        
        # Add links for remaining hosts
        self.addLink(h3, s2, cls=TCLink, delay='5ms')
        self.addLink(h4, s2, cls=TCLink, delay='5ms')
        self.addLink(h5, s3, cls=TCLink, delay='5ms')
        self.addLink(h6, s3, cls=TCLink, delay='5ms')
        self.addLink(h7, s4, cls=TCLink, delay='5ms')
        self.addLink(h8, s4, cls=TCLink, delay='5ms')
