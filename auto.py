#!/usr/bin/python3

import _phue
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--slaves', type=str, required=True, dest='slaves', help='--slaves="lamp 1,lamp 2"')
args = parser.parse_args()

master = 'Stehlampe'
slaves = args.slaves.split(',')
minimum = 0.1
maximum = 1.0

bri = _phue.get_bri(master)
bri = max(min(bri, maximum), minimum)
ct = _phue.get_ct(master)

_phue.set_lights(slaves, bri=bri, ct=ct)
