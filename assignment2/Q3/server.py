#!/usr/bin/env python3
import socket
import time
import json
import sys

def start_server(nagle, delayed_ack, host='127.0.0.1', port=5001, output_log='server_log.txt'):
    # Create and configure socket
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if not nagle:
        # Disable Nagle's algorithm
        server_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    server_sock.bind((host, port))
    server_sock.listen(1)
    print(f"Server listening on {host}:{port} (Nagle: {nagle}, Delayed ACK: {delayed_ack})")

    conn, addr = server_sock.accept()
    with conn:
        # Attempt to disable delayed ACK if specified (may be platform dependent)
        if not delayed_ack:
            try:
                conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
            except Exception as e:
                print("Could not disable delayed ACK on server:", e)
        print("Connection from", addr)
        overall_start_time = time.time()
        first_data_time = None
        last_data_time = None
        total_received = 0
        packet_sizes = []
        # Receive data until the connection is closed
        while True:
            data = conn.recv(1024)
            if not data:
                break
            current_time = time.time()
            if first_data_time is None:
                first_data_time = current_time
            last_data_time = current_time
            total_received += len(data)
            packet_sizes.append(len(data))
        overall_end_time = time.time()
        total_duration = overall_end_time - overall_start_time
        active_duration = (last_data_time - first_data_time) if first_data_time else 0

        # Save the server log results as JSON
        result = {
            "total_received": total_received,
            "total_duration": total_duration,
            "active_duration": active_duration,
            "packet_sizes": packet_sizes
        }
        with open(output_log, "w") as f:
            json.dump(result, f, indent=4)
        print(f"Server received {total_received} bytes. Total duration: {total_duration:.2f} sec, Active transfer duration: {active_duration:.2f} sec. Log saved to {output_log}")

    server_sock.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 server.py <nagle: True/False> <delayed_ack: True/False>")
        sys.exit(1)
    nagle = sys.argv[1].lower() == "true"
    delayed_ack = sys.argv[2].lower() == "true"
    start_server(nagle, delayed_ack)
