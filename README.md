# Network Packet Analysis Assignment

## Overview
This assignment involves capturing and analyzing network packets. The task consists of two parts:
1. **Packet Sniffing:** - Capturing real-time network packets using a Python-based sniffer.
2. **Packet Analysis:** - Processing the captured packets from a CSV file and extracting useful insights.
3. **Capture the Flag:** - Finding the different hints and messages in the data.

## Part 1: Packet Sniffing

### Running the Packet Sniffer
#### Prerequisites:
- Run the script with **root/sudo privileges** to access raw sockets.
- Install Python and required libraries (if not already installed):
  ```sh
  sudo apt install python3, pip
  pip install socket csv struct 
  ```

#### Execution:
```sh
sudo python3 fast_sniffer.py
```
The captured packet details will be stored in `fast_captured_packets_info.csv`.

### Tcp replay:-

To run the pcap files, we open a different terminals and run:-

> Note: In all the tcpreplay commands, you will have to use your own network interface (use ifconfig-a to get your network interface) 

```sh
sudo tcpreplay -i enp0s1 -M 10 2.pca
```

> Note: Open 2 terminals, run the sniffer code in one first and then the tcpreplay in other. Use contorol+c to terminate the sniffer after the tcpreplay is done.

### Packet Analysis

After this step, the data will be captured in 'fast_captured_packets_info.csv'., and the analysis scripts will be executed.

```sh
pip install matplotlib
```

For Q1
- python3 data_stats.py

For Q2.
- python3 pair_stats.py
You can set the 'print_all' flag to true to print the pairs

For Q3.
- python3 flow_stats.py
You can set the 'print_all' flag to true to print the stats (dictionaries)

### Timing Analysis

For the timing analysis, we will again, run fast_sniffer.py and tcpreplay in 2 separate terminals and check any packets are missed.

For checking fast Mbps:-

```sh
sudo tcpreplay -i enp0s1 -M 10 2.pca
```

For checking fast pps:-

```sh
sudo tcpreplay -i enp0s1 -M 10 2.pca
```

The max times are given in the assignmnet sheet.


## Part 2: Capture the Flag

For capture the flag, we will run our tcpreplay and 'adv_data_sniff.py' in two different terminals.
Here, the 'adv_data_sniff.py' will sniff the data, and print out the captured flags.

> Note: Here, we will require to run the sniffer two times. First, it will print the ip address required for Q2, then the second time, it will be able to count the number of times it appears. 


## Part 3:-
 
This part did not require any direct coding.


## Authors
Developed by Gaurav Joshi (21110065), Husain Malwat (21110117).