# Network Packet Analysis Assignment

## Overview
This assignment involves capturing and analyzing network packets. The task consists of two parts:
1. **Packet Sniffing** - Capturing real-time network packets using a Python-based sniffer.
2. **Packet Analysis** - Processing the captured packets from a CSV file and extracting useful insights.

## Part 1: Packet Sniffing
The first part involves running a packet sniffer that captures network packets in real time and logs relevant details into a CSV file (`captured_packets_info.csv`). The script captures Ethernet, IPv4, IPv6, TCP, UDP, and ICMP packets, extracting useful information such as:
- Source and Destination MAC Addresses
- Source and Destination IP Addresses
- Transport Layer Protocol (TCP/UDP)
- Source and Destination Ports
- Packet Size
- Traffic type detection (HTTP, DNS, SSL/TLS, etc.)

### Running the Packet Sniffer
#### Prerequisites:
- Run the script with **root/sudo privileges** to access raw sockets.
- Install Python and required libraries (if not already installed):
  ```sh
  sudo apt install python3
  ```

#### Execution:
```sh
sudo python3 packet_sniffer.py
```
The captured packet details will be stored in `captured_packets_info.csv`.

## Part 2: Packet Analysis
This part involves analyzing the captured packet data using Python. The analysis includes:
1. **Computing network metrics:**
   - Total data transferred (bytes)
   - Total packets captured
   - Minimum, maximum, and average packet size
   - Histogram of packet sizes
2. **Finding unique source-destination pairs** (source IP:port → destination IP:port).
3. **Analyzing traffic flows:**
   - Dictionary of IP addresses with total outgoing and incoming flows.
   - Finding the source-destination pair that transferred the most data.

### Running the Analysis Scripts
#### Prerequisites:
Ensure you have the required libraries installed:
```sh
pip install pandas matplotlib
```

#### Execution:
Run the analysis script to process the CSV file and generate insights:
```sh
python3 packet_analysis.py
```
This will display statistics, generate plots, and provide traffic flow details.

## Expected Output
- A summary of packet metrics (total bytes, packet count, min/max/avg size)
- A histogram visualizing packet size distribution
- A list of unique source-destination pairs
- Traffic flow statistics per IP address
- Identification of the most data-intensive communication pair

## Timing Analysis

## Notes
- The sniffer captures **live network traffic**. Ensure you are aware of security policies before running it.
- The analysis script expects `captured_packets_info.csv` to be present in the same directory.
- If using a `.pcap` file instead of live sniffing, you can convert it to CSV using Wireshark or a Python parser.

## Author
Developed by Gaurav Joshi, Husain Malwat.
