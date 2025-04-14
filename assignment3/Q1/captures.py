import os
import pyshark
from mininet.log import info

class CaptureManager:
    """Handles packet capture operations and analysis"""
    
    def __init__(self):
        self.capture_dir = 'captures'
        os.makedirs(self.capture_dir, exist_ok=True)
    
    def start_capture(self, host, interface, filename):
        """Start packet capture on a host interface"""
        cmd = f'tcpdump -i {interface} -w {self.capture_dir}/{filename} 2>/dev/null &'
        pid = host.cmd(cmd).strip()
        return pid

    def stop_capture(self, host, pid):
        """Stop packet capture using process ID"""
        host.cmd(f'kill -9 {pid}')
    
    def analyze_capture(self, filename):
        """Analyze packet capture file"""
        cap = pyshark.FileCapture(f'{self.capture_dir}/{filename}')
        stats = {
            'arp_requests': 0,
            'arp_replies': 0,
            'icmp_requests': 0,
            'icmp_replies': 0
        }
        
        for pkt in cap:
            if 'ARP' in pkt:
                if int(pkt.arp.opcode) == 1:
                    stats['arp_requests'] += 1
                elif int(pkt.arp.opcode) == 2:
                    stats['arp_replies'] += 1
            elif 'ICMP' in pkt:
                if pkt.icmp.type == '8':
                    stats['icmp_requests'] += 1
                elif pkt.icmp.type == '0':
                    stats['icmp_replies'] += 1
        
        return stats

    def print_analysis(self, stats, test_name):
        """Print formatted analysis results"""
        info(f"\n\033[1;34m=== Analysis for {test_name} ===\033[0m\n")
        info(f"ARP Requests: {stats['arp_requests']}\n")
        info(f"ARP Replies: {stats['arp_replies']}\n")
        info(f"ICMP Requests: {stats['icmp_requests']}\n")
        info(f"ICMP Replies: {stats['icmp_replies']}\n")
        info("="*50 + "\n")
