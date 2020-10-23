#/bin/bash

if test -f "mock_kuche"; then
    rm -rf mock_kuche
    exit 0
fi

touch mock_kuche
sleep 3600
rm -rf mock_kucke
