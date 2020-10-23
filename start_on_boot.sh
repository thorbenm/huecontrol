#/bin/bash

# put this into rc.local:
# sudo -H -u pi /home/pi/Programming/huecontrol/start_on_boot.sh &

THIS_FILE=$(readlink -f "$0")
THIS_DIR=$(dirname "${THIS_FILE}")
cd ${THIS_DIR}
sleep 10
python3 motionsensor.py

