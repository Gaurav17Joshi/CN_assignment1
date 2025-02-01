# Detailed real time sniffer code:
import socket
import struct
import csv

# Define constants for Ethernet frame
ETH_P_ALL = 0x0003  # Capture all protocols
BUFFER_SIZE = 65535
CSV_FILENAME = "fast_captured_packets_info.csv"  # Output file for logging packets

# Function to format MAC addresses into human-readable format
def mac_format(mac):
    return ":".join(map("{:02x}".format, mac))

# Function to format raw IP addresses into standard format
def ip_format(addr):
    return ".".join(map(str, addr))

# Function to format IPv6 addresses into standard format
def ipv6_format(addr):
    return ":".join(f"{addr[i]:02x}{addr[i+1]:02x}" for i in range(0, 16, 2))

# Function to parse Ethernet header (first 14 bytes of packet)
def parse_ethernet_header(raw_data):
    """
    Ethernet Frame Format:
    - 6 bytes: Destination MAC
    - 6 bytes: Source MAC
    - 2 bytes: Protocol (indicates the type of payload, e.g., IPv4, ARP)
    """
    dest_mac, src_mac, eth_proto = struct.unpack("!6s6sH", raw_data[:14])
    return mac_format(dest_mac), mac_format(src_mac), socket.htons(eth_proto), raw_data[14:]

# Function to parse IPv4 header (first 20 bytes of IP packet)
def parse_ipv4_header(raw_data):
    """
    IPv4 Header Format:
    - 1 byte: Version & IHL (Internet Header Length)
    - 1 byte: Differentiated Services (TOS)
    - 2 bytes: Total Length
    - 2 bytes: Identification
    - 2 bytes: Flags & Fragment Offset
    - 1 byte: Time to Live (TTL)
    - 1 byte: Protocol (6=TCP, 17=UDP, etc.)
    - 2 bytes: Header Checksum
    - 4 bytes: Source IP Address
    - 4 bytes: Destination IP Address
    """
    ip_header = struct.unpack("!BBHHHBBH4s4s", raw_data[:20])
    version_ihl = ip_header[0]
    version = version_ihl >> 4
    header_length = (version_ihl & 15) * 4
    ttl = ip_header[5]
    proto = ip_header[6]
    src_ip = ip_format(ip_header[8])
    dest_ip = ip_format(ip_header[9])
    return version, header_length, ttl, proto, src_ip, dest_ip, raw_data[header_length:]
    
# Function to parse IPv6 header (first 40 bytes of IPv6 packet)
def parse_ipv6_header(raw_data):
    """
    IPv6 Header Format (40 bytes):
    - 4 bits: Version (should be 6)
    - 8 bits: Traffic Class
    - 20 bits: Flow Label
    - 16 bits: Payload Length
    - 8 bits: Next Header (e.g., TCP=6, UDP=17, ICMPv6=58)
    - 8 bits: Hop Limit (like TTL in IPv4)
    - 128 bits (16 bytes): Source IP Address
    - 128 bits (16 bytes): Destination IP Address
    """
    ipv6_header = struct.unpack("!IHBB16s16s", raw_data[:40])
    version = (ipv6_header[0] >> 28) & 0xF  # Extract version (should be 6)
    traffic_class = (ipv6_header[0] >> 20) & 0xFF
    flow_label = ipv6_header[0] & 0xFFFFF
    payload_length = ipv6_header[1]
    next_header = ipv6_header[2]  # Protocol (TCP=6, UDP=17, ICMPv6=58)
    hop_limit = ipv6_header[3]
    src_ip = ipv6_format(ipv6_header[4])
    dest_ip = ipv6_format(ipv6_header[5])
    return version, traffic_class, flow_label, payload_length, next_header, hop_limit, src_ip, dest_ip, raw_data[40:]

# Function to parse TCP header (first 20 bytes of TCP segment)
def parse_tcp_header(raw_data):
    """
    TCP Header Format:
    - 2 bytes: Source Port
    - 2 bytes: Destination Port
    - 4 bytes: Sequence Number
    - 4 bytes: Acknowledgment Number
    - 4 bits: Data Offset
    """
    tcp_header = struct.unpack("!HHLLBBHHH", raw_data[:20])
    src_port, dest_port, seq, ack, offset_reserved_flags = tcp_header[:5]
    header_length = (offset_reserved_flags >> 4) * 4
    return src_port, dest_port, seq, ack, header_length, raw_data[header_length:]

# Function to parse UDP header (first 8 bytes of UDP segment)
def parse_udp_header(raw_data):
    """
    UDP Header Format:
    - 2 bytes: Source Port
    - 2 bytes: Destination Port
    - 2 bytes: Length
    """
    udp_header = struct.unpack("!HHHH", raw_data[:8])
    src_port, dest_port, length = udp_header[:3]
    return src_port, dest_port, length, raw_data[8:]

# Function to parse ICMP header
def parse_icmp_header(raw_data):
    icmp_type, code, checksum = struct.unpack("!BBH", raw_data[:4])
    return icmp_type, code, checksum, raw_data[4:]

# Function to identify HTTP traffic (simple check for GET/POST requests)
def is_http(payload):
    return payload[:4] in [b'GET ', b'POST', b'HTTP']

# Function to identify SSL/TLS traffic (typically on port 443)
def is_ssl(src_port, dest_port):
    return src_port == 443 or dest_port == 443




# Create a raw socket to capture packets
sniffer = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(ETH_P_ALL))

total_captured_packets = 0
total_saved_packets = 0

# Open CSV file to log packets
with open(CSV_FILENAME, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Ethernet Src", "Ethernet Dest", "Protocol", "IP Src", "IP Dest", "Transport Protocol", "Src Port", "Dest Port", "Packet Size"])

    print("\U0001f50e Sniffing packets... Press Ctrl+C to stop.\n")

    try:
        while True:
            # Receive raw packet data
            raw_data, addr = sniffer.recvfrom(BUFFER_SIZE)
            total_captured_packets = total_captured_packets + 1
            packet_size = len(raw_data)  # Capture packet size

            # Parse Ethernet header
            dest_mac, src_mac, eth_proto, data = parse_ethernet_header(raw_data)
            print(f"\n\U0001f4e1 Ethernet: {src_mac} \u2192 {dest_mac} | Protocol: {eth_proto} | Size: {packet_size} bytes")

            # Default values for logging
            src_ip = dest_ip = src_port = dest_port = transport_protocol = "N/A"

            # Parse IP header if applicable
            if eth_proto == 8:  # IPv4
                version, header_length, ttl, proto, src_ip, dest_ip, data = parse_ipv4_header(data)
                print(f"\U0001f310 IPv4: {src_ip} \u2192 {dest_ip} | Protocol: {proto} | TTL: {ttl}")

                # Parse TCP segment if protocol is TCP (6)
                if proto == 6:
                    src_port, dest_port, seq, ack, header_length, data = parse_tcp_header(data)
                    transport_protocol = "TCP"
                    print(f"\U0001f535 TCP: {src_ip}:{src_port} \u2192 {dest_ip}:{dest_port} | Seq: {seq} | Ack: {ack}")

                    if is_http(data):
                         print("\U0001f30d HTTP Traffic Detected")
                    elif is_ssl(src_port, dest_port):
                         print("\U0001f512 SSL/TLS Traffic Detected")

                # Parse UDP segment if protocol is UDP (17)
                elif proto == 17:
                    src_port, dest_port, length, data = parse_udp_header(data)
                    transport_protocol = "UDP"
                    print(f"\U0001f7e2 UDP: {src_ip}:{src_port} \u2192 {dest_ip}:{dest_port} | Length: {length}")

                    if src_port == 53 or dest_port == 53:
                        print("\U0001f4e1 DNS Traffic Detected")

                else:
                    print(f"\U0001f536 Other Protocol: {proto}")
                    
            # Parse IPv6 header
            elif eth_proto == 0x86DD:  # IPv6
                version, traffic_class, flow_label, payload_length, next_header, hop_limit, src_ip, dest_ip, data = parse_ipv6_header(data)
                print(f"\U0001f310 IPv6: {src_ip} \u2192 {dest_ip} | Next Header: {next_header} | Hop Limit: {hop_limit}")

                if next_header == 6:  # TCP
                    src_port, dest_port, seq, ack, header_length, data = parse_tcp_header(data)
                    transport_protocol = "TCP"
                    print(f"\U0001f535 TCP: {src_ip}:{src_port} \u2192 {dest_ip}:{dest_port} | Seq: {seq} | Ack: {ack}")

                elif next_header == 17:  # UDP
                    src_port, dest_port, length, data = parse_udp_header(data)
                    transport_protocol = "UDP"
                    print(f"\U0001f7e2 UDP: {src_ip}:{src_port} \u2192 {dest_ip}:{dest_port} | Length: {length}")



            # Write packet data to CSV file
            writer.writerow([src_mac, dest_mac, eth_proto, src_ip, dest_ip, transport_protocol, src_port, dest_port, packet_size])
            total_saved_packets = total_saved_packets + 1

    except KeyboardInterrupt:
        print("\n\U0001f6d1 Sniffing stopped.")
        print(f"\n Total captured Packets: {total_captured_packets} and Total saved Packets: {total_saved_packets} ")
        sniffer.close()