#!/bin/bash

cd /home/pi/Programming/huecontrol

sudo systemctl stop phue_server.service

python <<EOF
import _phue
import data
from time import sleep

l = [*data.kuche_lights, *data.bad_lights]
_phue.set_lights(l, bri=_phue.min_bri(), ct=1.0)
sleep(1.0)
_phue.set_lights(l, bri=.4, ct=1.0, time=60.0)
sleep(60.0)
_phue.set_lights(l, bri=1.0, ct=.7, time=120.0)
sleep(120.0)
_phue.set_lights(l, bri=1.0, ct=.48, time=90.0*60.0)
EOF
