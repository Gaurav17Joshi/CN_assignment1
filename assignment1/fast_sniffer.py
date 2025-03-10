import socket
import struct
import csv

# Define constants
ETH_P_ALL = 0x0003  # Capture all protocols
BUFFER_SIZE = 65535
CSV_FILENAME = "fast_captured_packets_info.csv"

# Helper functions
def ip_format(addr):
    return ".".join(map(str, addr))

def ipv6_format(addr):
    return ":".join(f"{addr[i]:02x}{addr[i+1]:02x}" for i in range(0, 16, 2))

def parse_ethernet_header(raw_data):
    _, _, eth_proto = struct.unpack("!6s6sH", raw_data[:14])
    return socket.htons(eth_proto), raw_data[14:]

def parse_ipv4_header(raw_data):
    ip_header = struct.unpack("!BBHHHBBH4s4s", raw_data[:20])
    proto = ip_header[6]
    src_ip = ip_format(ip_header[8])
    dest_ip = ip_format(ip_header[9])
    return proto, src_ip, dest_ip, raw_data[20:]

def parse_ipv6_header(raw_data):
    ipv6_header = struct.unpack("!IHBB16s16s", raw_data[:40])
    next_header = ipv6_header[2]
    src_ip = ipv6_format(ipv6_header[4])
    dest_ip = ipv6_format(ipv6_header[5])
    return next_header, src_ip, dest_ip, raw_data[40:]

def parse_tcp_udp_header(raw_data, is_tcp=True):
    header_format = "!HHHH" if not is_tcp else "!HHLLBBHHH"
    header_size = 8 if not is_tcp else 20
    parsed = struct.unpack(header_format, raw_data[:header_size])
    return parsed[0], parsed[1], raw_data[header_size:]

def parse_icmp_igmp_header(raw_data):
    icmp_type, code = struct.unpack("!BB", raw_data[:2])
    return icmp_type, code

# Create raw socket
sniffer = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(ETH_P_ALL))

total_captured_packets = 0
total_saved_packets = 0

# Open CSV file for logging
with open(CSV_FILENAME, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Src IP", "Dest IP", "Protocol", "Src Port", "Dest Port", "Packet Size"])

    try:
        while True:
            raw_data, _ = sniffer.recvfrom(BUFFER_SIZE)
            total_captured_packets = total_captured_packets + 1
            packet_size = len(raw_data)

            eth_proto, data = parse_ethernet_header(raw_data)
            src_ip = dest_ip = src_port = dest_port = "N/A"
            transport_protocol = "Other"

            if eth_proto == 8:  # IPv4
                proto, src_ip, dest_ip, data = parse_ipv4_header(data)
            elif eth_proto == 0x86DD:  # IPv6
                proto, src_ip, dest_ip, data = parse_ipv6_header(data)
            else:
                continue  # Skip non-IP packets

            if proto == 6:  # TCP
                src_port, dest_port, _ = parse_tcp_udp_header(data, is_tcp=True)
                transport_protocol = "TCP"
            elif proto == 17:  # UDP
                src_port, dest_port, _ = parse_tcp_udp_header(data, is_tcp=False)
                transport_protocol = "UDP"
            elif proto == 1:  # ICMP
                parse_icmp_igmp_header(data)
                transport_protocol = "ICMP"
            elif proto == 2:  # IGMP
                parse_icmp_igmp_header(data)
                transport_protocol = "IGMP"
                
            print(f"Packet: {src_ip}:{src_port} -> {dest_ip}:{dest_port}, Protocol: {transport_protocol}, Size: {packet_size}")

            writer.writerow([src_ip, dest_ip, transport_protocol, src_port, dest_port, packet_size])
            total_saved_packets = total_saved_packets + 1

    except KeyboardInterrupt:
        print("\nSniffing stopped.")
        print(f"\n Total captured Packets: {total_captured_packets} and Total saved Packets: {total_saved_packets} ")
        sniffer.close()
