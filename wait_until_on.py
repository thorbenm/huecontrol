#!/usr/bin/python3
import sys
import _phue
import time

light = sys.argv[1]

while not _phue.get_on(light):
    time.sleep(10.0)
