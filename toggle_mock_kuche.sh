#/bin/bash

THIS_FILE=$(readlink -f "$0")
THIS_DIR=$(dirname "${THIS_FILE}")
cd ${THIS_DIR}

if test -f "mock_kuche"; then
    rm -rf mock_kuche
    exit 0
fi

touch mock_kuche
sleep 3600
rm -rf mock_kucke
