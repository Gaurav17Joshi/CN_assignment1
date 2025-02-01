import csv
import matplotlib.pyplot as plt

# Initialize variables
total_data = 0
total_packets = 0
packet_sizes = []

# Read the CSV file and extract the necessary data
with open('fast_captured_packets_info.csv', mode="r") as file:
    reader = csv.reader(file)

    for row in reader:
        print(row)
        indice = [i for i, x in enumerate(row) if x == "Packet Size"][0]
        break

    next(reader)

    for row in reader:
        packet_size = int(row[indice])  # The last column is packet size
        total_data += packet_size
        total_packets += 1
        packet_sizes.append(packet_size)

# Calculate packet size metrics
min_size = min(packet_sizes)
max_size = max(packet_sizes)
avg_size = total_data / total_packets

# Print the results
print(f"Total Data Transferred: {total_data} bytes")
print(f"Total Packets Transferred: {total_packets}")
print(f"Minimum Packet Size: {min_size} bytes")
print(f"Maximum Packet Size: {max_size} bytes")
print(f"Average Packet Size: {avg_size:.2f} bytes")

# Plot packet size distribution
plt.hist(packet_sizes, bins=20, edgecolor='black')
plt.title("Packet Size Distribution")
plt.xlabel("Packet Size (bytes)")
plt.ylabel("Frequency")
plt.savefig("Packet_Size_dist")
plt.close()
