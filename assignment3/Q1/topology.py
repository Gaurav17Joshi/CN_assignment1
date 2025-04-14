from mininet.topo import Topo
from mininet.link import TCLink

class LoopTopo(Topo):
    """Network topology with switches in loop configuration"""
    
    def build(self):
        # Create switches
        switches = [self.addSwitch(f's{i+1}') for i in range(4)]
        
        # Create hosts with IP addresses
        hosts = [
            self.addHost(f'h{i+1}', ip=f'10.0.0.{i+2}/24')
            for i in range(8)
        ]
        
        # Host-switch connections (5ms latency)
        host_links = [
            (0, 0), (0, 1),  # h1,h2 -> s1
            (1, 2), (1, 3),  # h3,h4 -> s2
            (2, 4), (2, 5),  # h5,h6 -> s3
            (3, 6), (3, 7)   # h7,h8 -> s4
        ]
        
        for sw_idx, host_idx in host_links:
            self.addLink(
                switches[sw_idx], 
                hosts[host_idx], 
                cls=TCLink, 
                delay='5ms'
            )
        
        # Switch-switch connections (7ms latency)
        switch_links = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Main loop
            (0, 2)  # Cross-connection
        ]
        
        for i, j in switch_links:
            self.addLink(
                switches[i], 
                switches[j], 
                cls=TCLink, 
                delay='7ms'
            )
