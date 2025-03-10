import pandas as pd
import matplotlib.pyplot as plt
import os

# Load TCP connections (SYN packets)
syn_df = pd.read_csv("~/Desktop/Computer_network/connections.csv", sep="\t", names=["time", "src_ip", "dst_ip", "src_port", "dst_port"])

# Load TCP termination events (FIN or RESET)
end_df = pd.read_csv("~/Desktop/Computer_network/connection_end.csv", sep="\t", names=["time", "src_ip", "dst_ip", "src_port", "dst_port"])

# Merge data to compute connection duration
merged_df = pd.merge(syn_df, end_df, on=["src_ip", "dst_ip", "src_port", "dst_port"], suffixes=("_start", "_end"))

# Compute connection duration
merged_df["duration"] = merged_df["time_end"] - merged_df["time_start"]

# Assign default duration of 100s to connections without proper termination
# merged_df["duration"].fillna(100, inplace=True)
merged_df["duration"] = merged_df["duration"].fillna(100)

# Plot connection duration over time
plt.figure(figsize=(10, 5))
plt.scatter(merged_df["time_start"], merged_df["duration"], color="red", label="Connection Duration")
plt.axvline(x=merged_df["time_start"].min() + 20, color="blue", linestyle="--", label="Attack Start (20s)")
plt.axvline(x=merged_df["time_start"].min() + 120, color="green", linestyle="--", label="Attack Stop (120s)")
plt.xlabel("Connection Start Time")
plt.ylabel("Connection Duration (s)")
plt.title("Effect of SYN Flood Attack on Connection Durations")
plt.legend()

# Save the figure as an image file in Ubuntu's "Computer_network" directory
# output_path = "~/Desktop/Computer_network/syn_flood_plot.png"
output_path = os.path.expanduser("~/Desktop/Computer_network/syn_flood_plot.png")
plt.savefig(output_path, dpi=300)  # Save with high resolution

print(f"Plot saved successfully at: {output_path}")
