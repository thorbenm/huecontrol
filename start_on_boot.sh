#/bin/bash

# put this into rc.local:
# sudo -H -u pi /home/pi/Programming/huecontrol/start_on_boot.sh &

THIS_FILE=$(readlink -f "$0")
THIS_DIR=$(dirname "${THIS_FILE}")
cd ${THIS_DIR}
sleep 90
rm -rf mock_kuche
echo "" >> delme_log_motionsensor.txt
echo "" >> delme_log_motionsensor.txt
echo "" >> delme_log_motionsensor.txt
echo "" >> delme_log_motionsensor.txt
echo "" >> delme_log_motionsensor.txt
python3 motionsensor.py 1>> delme_log_motionsensor.txt 2>> delme_log_motionsensor.txt &
python3 mock_file_deleter.py &
