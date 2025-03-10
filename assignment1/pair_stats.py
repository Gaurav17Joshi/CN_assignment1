# Collecting the pair wise stats

import csv

# Initialize a set to store unique source-destination pairs
unique_pairs = set()
print_all = False

# Read the CSV file and extract source-destination pairs
with open('captured_packets_info.csv', mode="r") as file:
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
        unique_pairs.add((src_ip, src_port, dest_ip, dest_port))

# Print the unique source-destination pairs
print(f"Number of unique pairs: {len(unique_pairs)}")

if print_all:
    for pair in unique_pairs:
        print(f"Source: {pair[0]}:{pair[1]} -> Destination: {pair[2]}:{pair[3]}")

