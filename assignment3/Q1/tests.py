from mininet.net import Mininet
from mininet.log import info
import time

def run_ping_test(net, src, dst, count=4):
    """Run ping test between hosts"""
    src_host = net.get(f'h{src}')
    dst_ip = net.get(f'h{dst}').IP()
    
    info(f"\n\033[1;36m=== Testing h{src} -> h{dst} ===\033[0m\n")
    result = src_host.cmd(f'ping -c {count} {dst_ip}')
    info(result)
    return result

def enable_stp(net):
    """Enable Spanning Tree Protocol on all switches"""
    info("\n\033[1;33m=== Enabling STP ===\033[0m\n")
    for switch in net.switches:
        switch.cmd(f'ovs-vsctl set bridge {switch.name} stp_enable=true')
        info(f"Enabled STP on {switch.name}\n")
    
    info("\n\033[1;33mWaiting 50 seconds for STP convergence...\033[0m\n")
    time.sleep(50)

def print_header(text):
    """Print formatted section header"""
    info(f"\n\033[1;35m{'='*40}\n")
    info(f"{text.center(40)}\n")
    info(f"{'='*40}\033[0m\n\n")
