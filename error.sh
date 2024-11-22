#!/bin/bash
echo $(date) [error.sh] ...Starting error.sh script
FLAG_FILE="/tmp/done_flag"

echo $(date) [error.sh] ...Killing 'silence' pulseaudio client
sudo kill $(pactl list clients | awk '/application.name = "silence"/,/^$/' | awk -F' = ' '/application.process.id/ {print $2}' | sed 's/"//g')

echo $(date) [error.sh] ...Playing error message
espeak "Home Assistant has trouble responding. Please try again."

# Use attribute since replies can be more than 255 characters
HA_URL="http://homeassistant.local:8123" # Replace with your Home Assistant URL
SENSOR_ENTITY_ID="sensor.assist_speech"
ATTRIBUTE_NAME="tts"
NEW_ATTRIBUTE_VALUE="Home Assistant has trouble responding. Please try again." # Replace with the new value for the attribute
ACCESS_TOKEN="longlivedaccesstokenhere" # Replace with your actual home assistant token

# Update the sensor attribute
curl -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d "{\"state\": \"state\", \"attributes\": {\"$ATTRIBUTE_NAME\": \"$NEW_ATTRIBUTE_VALUE\"}}" \
     "$HA_URL/api/states/$SENSOR_ENTITY_ID"

# echo "Sensor TTS  attribute updated."

rm -f "$FLAG_FILE"