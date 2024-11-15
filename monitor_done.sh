#!/bin/bash
FLAG_FILE="/tmp/done_flag"
MONITOR_INTERVAL=1  # Time to wait between checks (in seconds)
TIMEOUT=30          # Max time to wait before running done.sh (in seconds)

echo $(date) [monitor_done.sh] ...Starting monitor script

while true; do
    if [ -f "$FLAG_FILE" ]; then
        echo $(date) [monitor_done.sh] ...Flag detected, starting countdown
        SECONDS_PASSED=0
        
        while [ -f "$FLAG_FILE" ] && [ $SECONDS_PASSED -lt $TIMEOUT ]; do
            sleep $MONITOR_INTERVAL
            SECONDS_PASSED=$((SECONDS_PASSED + MONITOR_INTERVAL))
        done
        
        if [ -f "$FLAG_FILE" ]; then
            echo $(date) [monitor_done.sh] ...done.sh not detected within $TIMEOUT seconds, calling done.sh manually
            /home/username/wyoming-enhancements/done.sh
            rm -f "$FLAG_FILE"
        else
            echo $(date) [monitor_done.sh] ...done.sh completed in time, no action needed
        fi
    fi
    
    sleep $MONITOR_INTERVAL
done