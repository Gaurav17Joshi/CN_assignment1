import socket
import struct

# Define constants
ETH_P_ALL = 0x0003  
BUFFER_SIZE = 65535

# Function to format IP address
def ip_format(addr):
    return ".".join(map(str, addr))

# Function to parse Ethernet header
def parse_ethernet_header(raw_data):
    dest_mac, src_mac, eth_proto = struct.unpack("!6s6sH", raw_data[:14])
    return socket.htons(eth_proto), raw_data[14:]

# Function to parse IPv4 header
def parse_ipv4_header(raw_data):
    ip_header = struct.unpack("!BBHHHBBH4s4s", raw_data[:20])
    header_length = (ip_header[0] & 15) * 4
    src_ip = ip_format(ip_header[8])
    dest_ip = ip_format(ip_header[9])
    proto = ip_header[6]
    return src_ip, dest_ip, proto, raw_data[header_length:]

# Function to parse TCP header
def parse_tcp_header(raw_data):
    tcp_header = struct.unpack("!HHLLBBHHH", raw_data[:20])  # Correct TCP header parsing
    src_port = tcp_header[0]
    dest_port = tcp_header[1]
    sequence = tcp_header[2]
    ack = tcp_header[3]
    offset_reserved_flags = tcp_header[4]
    header_length = (offset_reserved_flags >> 4) * 4  # Extract TCP header length
    window = tcp_header[5]
    checksum = tcp_header[6]
    urg_pointer = tcp_header[7]
    
    return src_port, dest_port, checksum, raw_data[header_length:]
    

# Initialize variables
found_ip = "10.1.2.200"
ip_packet_count = 0
laptop_name = None
laptop_packet_checksum = None
order_successful_count = 0

captured_packets = 0
# Create raw socket
sniffer = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(ETH_P_ALL))

try:
    while True:
        raw_data, addr = sniffer.recvfrom(BUFFER_SIZE)
        captured_packets = captured_packets + 1
        eth_proto, data = parse_ethernet_header(raw_data)

        if eth_proto == 8:  # IPv4
            src_ip, dest_ip, proto, data = parse_ipv4_header(data)

            if proto == 6:  # TCP
                src_port, dest_port, checksum, payload = parse_tcp_header(data)

                # Convert payload to a readable string
                try:
                    payload_text = payload.decode(errors="ignore")
                    payload_text = payload_text.lower()
                except:
                    payload_text = ""

                
                # Q1: Find the IP Address
                if "my ip address =" in payload_text:
                    print(payload_text)
                    print(f"✅ Found IP Address in TCP Packet")

                # Q2: Count packets containing found IP
                if found_ip and (found_ip == src_ip or found_ip == dest_ip):
                    ip_packet_count += 1

                # Q3: Find Laptop Name and Checksum
                if laptop_name is None and "laptop =" in payload_text:
                    print(payload_text)
                    laptop_name = payload_text
                    print(f"✅ Found Laptop")
                    laptop_packet_checksum = checksum

                # Q4: Count "Order successful" packets
                if "order successful" in payload_text:
                    order_successful_count += 1

except KeyboardInterrupt:
    print("\n\U0001f6d1 Sniffing stopped.")
    print(f"\nTotal packets checked = {captured_packets}")
    print(f"\nQ1. Extracted IP Address: {found_ip}")
    print(f"Q2. Number of packets with IP {found_ip}: {ip_packet_count}")
    print(f"Q3a. Laptop Name: {laptop_name}")
    print(f"Q3b. TCP Checksum of laptop name packet: {laptop_packet_checksum}")
    print(f"Q4. Number of packets with 'Order successful': {order_successful_count}")

    sniffer.close()
