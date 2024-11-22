#!/bin/bash
echo $(date) [done.sh] ...Starting done.sh script
FLAG_FILE="/tmp/done_flag"

echo $(date) [done.sh] ...Playing finish beep
paplay --property=media.role=notification /home/username/wyoming-satellite/sounds/done.wav 
sleep 1

echo $(date) [done.sh] ...Killing 'silence' pulseaudio client
sudo kill $(pactl list clients | awk '/application.name = "silence"/,/^$/' | awk -F' = ' '/application.process.id/ {print $2}' | sed 's/"//g')

rm -f "$FLAG_FILE"