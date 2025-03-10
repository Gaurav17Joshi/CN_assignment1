#!/bin/bash
# Ensure the script is executable: chmod +x run_tests.sh

CONFIG_FILE="config.json"
RESULTS_DIR="results"
mkdir -p $RESULTS_DIR

# Determine the number of scenarios from the JSON config using Python.
num_scenarios=$(python3 -c "import json; print(len(json.load(open('$CONFIG_FILE'))['scenarios']))")

for (( i=0; i<num_scenarios; i++ ))
do
    echo "============================================"
    echo "Running scenario $i"
    # Extract the nagle and delayed_ack values for the current scenario.
    read nagle delayed_ack <<< $(python3 -c "import json; data=json.load(open('$CONFIG_FILE')); s=data['scenarios'][$i]; print(s['nagle'], s['delayed_ack'])")
    
    echo "Scenario $i: Nagle = $nagle, Delayed ACK = $delayed_ack"

    # Start the server in the background and redirect its log.
    python3 server.py $nagle $delayed_ack > $RESULTS_DIR/server_${i}.log 2>&1 &
    server_pid=$!

    # Give the server a moment to start up.
    sleep 2

    # Run the client; its log is saved separately.
    python3 client.py $nagle $delayed_ack > $RESULTS_DIR/client_${i}.log 2>&1

    # Wait for the server process to finish.
    wait $server_pid

    # Run metrics calculation and save the results.
    python3 metrics.py > $RESULTS_DIR/metrics_${i}.log 2>&1

    echo "Scenario $i completed. Logs saved in the '$RESULTS_DIR' directory."
    echo "============================================"
    sleep 2
done

echo "All scenarios completed."
