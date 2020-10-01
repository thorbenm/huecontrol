#/bin/bash
THIS_FILE=$(readlink -f "$0")
THIS_DIR=$(dirname "${THIS_FILE}")
cd ${THIS_DIR}
sleep 10
python3 motionsensor.py
