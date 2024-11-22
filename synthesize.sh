#!/usr/bin/env sh

text="$(cat)"
echo "Text to speech text: ${text}"

# Use attribute since replies can be more than 255 characters
HA_URL="http://homeassistant.local:8123" # Replace with your Home Assistant URL
SENSOR_ENTITY_ID="sensor.assist_speech"
ATTRIBUTE_NAME="tts"
NEW_ATTRIBUTE_VALUE=${text}
ACCESS_TOKEN="longlivedaccesstokenhere" # Replace with your actual home assistant token

# Update the sensor attribute
curl -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d "{\"state\": \"state\", \"attributes\": {\"$ATTRIBUTE_NAME\": \"$NEW_ATTRIBUTE_VALUE\"}}" \
     "$HA_URL/api/states/$SENSOR_ENTITY_ID"

# echo "Sensor TTS attribute updated."
