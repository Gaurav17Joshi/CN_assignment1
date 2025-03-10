#!/usr/bin/env python3
import json

def compute_metrics(server_log='server_log.txt', client_log='client_log.txt', output_file='metrics.json'):
    with open(server_log, "r") as f:
        server_data = json.load(f)
    with open(client_log, "r") as f:
        client_data = json.load(f)

    total_sent = client_data.get("total_sent", 0)
    total_received = server_data.get("total_received", 0)
    active_duration = server_data.get("active_duration", 1)  # use active transfer duration

    # Compute metrics based on active transfer duration
    throughput = total_received / active_duration if active_duration > 0 else 0
    # In this simulation, since only the file payload is transmitted, goodput equals throughput.
    goodput = throughput
    # Compute packet loss rate as the fraction of bytes lost (if any)
    packet_loss_rate = (total_sent - total_received) / total_sent if total_sent > 0 else 0
    max_packet_size = max(server_data.get("packet_sizes", [])) if server_data.get("packet_sizes", []) else 0

    metrics = {
        "throughput_bytes_per_sec": throughput,
        "goodput_bytes_per_sec": goodput,
        "packet_loss_rate": packet_loss_rate,
        "max_packet_size": max_packet_size,
        "active_duration_sec": active_duration
    }

    with open(output_file, "w") as f:
        json.dump(metrics, f, indent=4)
    
    print("Computed Metrics:")
    print(json.dumps(metrics, indent=4))

if __name__ == '__main__':
    compute_metrics()
