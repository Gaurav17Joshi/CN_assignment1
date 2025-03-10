#!/usr/bin/env python3
import socket
import time
import json
import sys
import os

def send_file(nagle, delayed_ack, host='127.0.0.1', port=5001, file_path='data.bin', output_log='client_log.txt'):
    # Ensure file of 4096 bytes exists; create one if needed.
    if not os.path.exists(file_path):
        file_data = b'A' * 4096
        with open(file_path, "wb") as f:
            f.write(file_data)
    else:
        with open(file_path, "rb") as f:
            file_data = f.read()
    
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if not nagle:
        # Disable Nagle's algorithm on the client
        client_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    client_sock.connect((host, port))
    
    # Attempt to disable delayed ACK if specified (platform dependent)
    if not delayed_ack:
        try:
            client_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
        except Exception as e:
            print("Could not disable delayed ACK on client:", e)
    
    print(f"Client connected to {host}:{port} (Nagle: {nagle}, Delayed ACK: {delayed_ack})")
    start_time = time.time()
    first_send_time = None
    last_send_time = None
    total_sent = 0
    chunk_size = 40        # send 40 bytes per chunk

    # Send file data chunk-by-chunk with a 1-second interval to maintain the rate.
    for i in range(0, len(file_data), chunk_size):
        current_time = time.time()
        if first_send_time is None:
            first_send_time = current_time
        last_send_time = current_time
        chunk = file_data[i:i+chunk_size]
        client_sock.sendall(chunk)
        total_sent += len(chunk)
        time.sleep(1)  # wait for 1 second between sends

    end_time = time.time()
    duration = end_time - start_time
    active_duration = (last_send_time - first_send_time) if first_send_time else 0
    result = {
        "total_sent": total_sent,
        "duration": duration,
        "active_duration": active_duration
    }
    with open(output_log, "w") as f:
        json.dump(result, f, indent=4)
    print(f"Client sent {total_sent} bytes in {duration:.2f} sec. Active transfer duration: {active_duration:.2f} sec. Log saved to {output_log}")
    client_sock.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 client.py <nagle: True/False> <delayed_ack: True/False>")
        sys.exit(1)
    nagle = sys.argv[1].lower() == "true"
    delayed_ack = sys.argv[2].lower() == "true"
    send_file(nagle, delayed_ack)
