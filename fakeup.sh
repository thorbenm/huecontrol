#!/bin/bash

cd /home/pi/Programming/huecontrol

sudo systemctl stop motionsensor.service

python <<EOF
import _phue
import data
from time import sleep

l = [j[0] for j in [*data.kuche_slaves, *data.bad_slaves]]
_phue.set_lights(l, bri=_phue.min_bri(), ct=1.0)
sleep(1.0)
_phue.set_lights(l, bri=.75, ct=1.0, time=120.0)
sleep(120.0)
_phue.set_lights(l, bri=1.0, ct=.58, time=90.0*60.0)
EOF
