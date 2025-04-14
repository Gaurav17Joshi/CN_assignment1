from mininet.net import Mininet
from mininet.node import OVSController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from topology import *
from tests import *
from captures import CaptureManager
import time

# def run_test_with_capture(net, capture_manager, src, dst, test_name):
#     """Run ping test with packet capture and analysis"""
#     src_host = net.get(f'h{src}')
#     dst_host = net.get(f'h{dst}')
#     dst_ip = dst_host.IP()
#     interface = src_host.defaultIntf().name
#     capture_file = f"{test_name}.pcap"

#     # Start packet capture
#     info(f"\n\033[1;33mStarting capture for {test_name}...\033[0m\n")
#     pid = capture_manager.start_capture(src_host, interface, capture_file)

#     # Run ping test
#     info(f"\n\033[1;36mRunning ping test: h{src} -> h{dst}...\033[0m\n")
#     result = src_host.cmd(f'ping -c 4 {dst_ip}')
#     info(result)

#     # Stop packet capture
#     capture_manager.stop_capture(src_host, pid)

#     # Analyze capture
#     stats = capture_manager.analyze_capture(capture_file)
#     capture_manager.print_analysis(stats, test_name)

#     return result, stats

def run_test_with_capture(net, capture_manager, src, dst, test_name):
    """Run ping test with packet capture and analysis with a timeout mechanism."""
    src_host = net.get(f'h{src}')
    dst_host = net.get(f'h{dst}')
    dst_ip = dst_host.IP()
    interface = src_host.defaultIntf().name
    capture_file = f"{test_name}.pcap"

    # Start packet capture
    info(f"\n\033[1;33mStarting capture for {test_name}...\033[0m\n")
    pid = capture_manager.start_capture(src_host, interface, capture_file)

    # Run ping test with timeout
    info(f"\n\033[1;36mRunning ping test: h{src} -> h{dst}...\033[0m\n")
    # Using 'timeout' ensures that if ping hangs, it will be killed after 10 seconds.
    result = src_host.cmd(f'timeout 10 ping -c 4 {dst_ip}')
    info(result)

    # Stop packet capture; catch exceptions in case it already terminated
    try:
        capture_manager.stop_capture(src_host, pid)
    except Exception as e:
        info(f"Error stopping capture: {e}\n")

    # Analyze capture
    stats = capture_manager.analyze_capture(capture_file)
    capture_manager.print_analysis(stats, test_name)

    return result, stats

def run_test_without_capture(net, src, dst, test_name):
    """Run ping test without packet capture"""
    src_host = net.get(f'h{src}')
    dst_host = net.get(f'h{dst}')
    dst_ip = dst_host.IP()

    # Run ping test
    info(f"\n\033[1;36mRunning ping test: h{src} -> h{dst} ({test_name})...\033[0m\n")
    result = src_host.cmd(f'ping -c 4 {dst_ip}')
    info(result)

    # Extract total delay from ping output
    delay_line = [line for line in result.split('\n') if "rtt min/avg/max/mdev" in line]
    if delay_line:
        delay_stats = delay_line[0].split('=')[1].strip().split('/')[1]  # Extract avg delay
        info(f"\033[1;32mAverage Delay: {delay_stats} ms\033[0m\n")
    else:
        info("\033[1;31mPing failed. No delay information available.\033[0m\n")

    return result

def main():
    net = Mininet(
        topo=LoopTopo(),
        controller=OVSController,
        link=TCLink,
        autoSetMacs=True
    )
    net.start()
    capture_manager = CaptureManager()

    try:
        # # Part A: Without STP (Without Capture)
        # print_header("TESTING WITHOUT STP (WITHOUT CAPTURE)")
        # for i in range(3):  # Run each test 3 times
        #     run_test_without_capture(net, 1, 3, f"test_h1_h3_run{i+1}")
        #     print("wait 30 seconds... ")
        #     time.sleep(30)
        #     run_test_without_capture(net, 7, 5, f"test_h7_h5_run{i+1}")
        #     print("wait 30 seconds... ")
        #     time.sleep(30)
        #     run_test_without_capture(net, 2, 8, f"test_h2_h8_run{i+1}")
        #     print("wait 30 seconds... ")
        #     time.sleep(30)

        # Part B: Without STP (With Capture)
        print_header("TESTING WITHOUT STP (WITH CAPTURE)")
        for i in range(3):  # Run each test 3 times
            run_test_with_capture(net, capture_manager, 1, 3, f"test_h1_h3_run{i+1}")
            print("wait 30 seconds... ")
            time.sleep(30)
            run_test_with_capture(net, capture_manager, 7, 5, f"test_h7_h5_run{i+1}")
            print("wait 30 seconds... ")
            time.sleep(30)
            run_test_with_capture(net, capture_manager, 2, 8, f"test_h2_h8_run{i+1}")
            print("wait 30 seconds... ")
            time.sleep(30)

        # # Part C: With STP (Without Capture)
        # print_header("ENABLING STP")
        # enable_stp(net)

        # print_header("TESTING WITH STP (WITHOUT CAPTURE)")
        # for i in range(3):  # Run each test 3 times
        #     run_test_without_capture(net, 1, 3, f"stp_test_h1_h3_run{i+1}")
        #     print("wait 30 seconds... ")
        #     time.sleep(30)
        #     run_test_without_capture(net, 7, 5, f"stp_test_h7_h5_run{i+1}")
        #     print("wait 30 seconds... ")
        #     time.sleep(30)
        #     run_test_without_capture(net, 2, 8, f"stp_test_h2_h8_run{i+1}")
        #     print("wait 30 seconds... ")
        #     time.sleep(30)

        # Part D: With STP (With Capture)
        print_header("TESTING WITH STP (WITH CAPTURE)")
        for i in range(3):  # Run each test 3 times
            run_test_with_capture(net, capture_manager, 1, 3, f"stp_test_h1_h3_run{i+1}")
            print("wait 30 seconds... ")
            time.sleep(30)
            run_test_with_capture(net, capture_manager, 7, 5, f"stp_test_h7_h5_run{i+1}")
            print("wait 30 seconds... ")
            time.sleep(30)
            run_test_with_capture(net, capture_manager, 2, 8, f"stp_test_h2_h8_run{i+1}")
            print("wait 30 seconds... ")
            time.sleep(30)

        CLI(net)

    finally:
        net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    main()
# def main():
#     net = Mininet(
#         topo=LoopTopo(),
#         controller=OVSController,
#         link=TCLink,
#         autoSetMacs=True
#     )
#     net.start()
#     capture_manager = CaptureManager()

#     try:
#         # Part A: Without STP
#         print_header("TESTING WITHOUT STP")
#         for i in range(3):  # Run each test 3 times
#             run_test_with_capture(net, capture_manager, 1, 3, f"test_h1_h3_run{i+1}")
#             time.sleep(30)
#             run_test_with_capture(net, capture_manager, 7, 5, f"test_h7_h5_run{i+1}")
#             time.sleep(30)
#             run_test_with_capture(net, capture_manager, 2, 8, f"test_h2_h8_run{i+1}")
#             time.sleep(30)

#         # Part B: With STP
#         print_header("ENABLING STP")
#         enable_stp(net)

#         print_header("TESTING WITH STP")
#         for i in range(3):  # Run each test 3 times
#             run_test_with_capture(net, capture_manager, 1, 3, f"stp_test_h1_h3_run{i+1}")
#             time.sleep(30)
#             run_test_with_capture(net, capture_manager, 7, 5, f"stp_test_h7_h5_run{i+1}")
#             time.sleep(30)
#             run_test_with_capture(net, capture_manager, 2, 8, f"stp_test_h2_h8_run{i+1}")
#             time.sleep(30)

#         CLI(net)

#     finally:
#         net.stop()

# if __name__ == '__main__':
#     setLogLevel('info')
#     main()
