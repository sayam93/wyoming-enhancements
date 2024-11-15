#!/bin/bash
echo $(date) [awake.sh] ...Starting awake.sh script

### Start the audio ducking process or any additional awake actions
echo $(date) [awake.sh] ...Starting silence
pacat --client-name=silence --volume=0 --property=media.role=notification < /dev/zero > /dev/null 2>&1 &

echo $(date) [awake.sh] ...awake.sh complete