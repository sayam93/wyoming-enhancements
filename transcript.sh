#!/usr/bin/env sh

text="$(cat)"
echo "Speech to text transcript: ${text}"

# Use attribute since replies can be more than 255 characters
HA_URL="http://homeassistant.local:8123" # Replace with your Home Assistant URL
SENSOR_ENTITY_ID="sensor.assist_speech"
ATTRIBUTE_NAME="stt"
NEW_ATTRIBUTE_VALUE=${text}
ACCESS_TOKEN="longlivedaccesstokenhere" # Replace with your actual home assistant token

# Update the sensor attribute
curl -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d "{\"state\": \"state\", \"attributes\": {\"$ATTRIBUTE_NAME\": \"$NEW_ATTRIBUTE_VALUE\"}}" \
     "$HA_URL/api/states/$SENSOR_ENTITY_ID"

# echo "Sensor STT attribute updated."

# Define a flag file that done.sh will delete or touch upon completion
FLAG_FILE="/tmp/done_flag"
touch "$FLAG_FILE"
