#!/usr/bin/python3
import requests
from phue import Bridge

json_data = requests.get("https://discovery.meethue.com").json()
ip_address = json_data[0]['internalipaddress']

b = Bridge(ip_address)
b.connect()

def set_lights(lights, bri=None, ct=None, on=None, time=4):
    for l in lights:
        if on is not None:
           b.set_light(l, 'on', on, transitiontime=time)
        if bri is not None:
           b.set_light(l, 'bri', bri, transitiontime=time)
        if ct is not None:
           b.set_light(l, 'ct', ct, transitiontime=time)
