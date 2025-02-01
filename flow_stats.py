# Flow calculation
import csv
from collections import defaultdict

# Initialize dictionaries to count flows
source_flows = defaultdict(int)
dest_flows = defaultdict(int)
data_transfer = defaultdict(int)

print_all = False

# Read the CSV file and process the flows
with open('fast_captured_packets_info.csv', mode="r") as file:
    reader = csv.reader(file)
    
    for row in reader:
        print(row)
        srcip_indice = [i for i, x in enumerate(row) if x == "Src IP"][0]
        destip_indice = [i for i, x in enumerate(row) if x == "Dest IP"][0]
        srcport_indice = [i for i, x in enumerate(row) if x == "Src Port"][0]
        destport_indice = [i for i, x in enumerate(row) if x == "Dest Port"][0]
        print(f"{srcip_indice} , {destip_indice} , {srcport_indice} , {destport_indice}")
        break
    
    
    next(reader)  # Skip header row
    
    for row in reader:
        src_ip = row[srcip_indice]  # Source IP 
        dest_ip = row[destip_indice]  # Destination IP 
        src_port = row[srcport_indice]  # Source port 
        dest_port = row[destport_indice]  # Destination port 
        packet_size = int(row[-1])  # Packet size is the last column

        # Count the flows
        source_flows[src_ip] += 1
        dest_flows[dest_ip] += 1

        # Track data transfer for each source-destination pair
        data_transfer[(src_ip, src_port, dest_ip, dest_port)] += packet_size

# Print the flow counts for each IP address
print("Source IP Flows:")
print(f"Total Number of Ip address outgoing flows {len(source_flows)}")

if print_all:
    for ip, count in source_flows.items():
        print(f"{ip}: {count} flows")

print("\nDestination IP Flows:")
print(f"Total Number of Ip address incoming flows {len(dest_flows)}")

if print_all:
    for ip, count in dest_flows.items():
        print(f"{ip}: {count} flows")

# Find the source-destination pair with the most data transferred
max_data_pair = max(data_transfer, key=data_transfer.get)
max_data_size = data_transfer[max_data_pair]

print(f"\nSource-Destination Pair with Most Data Transferred: {max_data_pair}")
print(f"Total Data Transferred: {max_data_size} bytes")


