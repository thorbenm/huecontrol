#!/usr/bin/python3
import os.path
import os
from time import sleep

files = ['mock_kuche']
counters = [3601.0 for j in files]
# deletes all files on startup

while True:
    for j in range(len(files)):
        if os.path.isfile(files[j]):
            counters[j] += 60.0
        else:
            counters[j] = 0.0
        if 3600.0 < counters[j]:
            os.remove(files[j])
    sleep(60.0)
