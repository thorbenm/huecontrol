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
            current_state = b.get_light(l, 'on')
            # if the light is currently off it will not react to
            # new brightness settings, so we have to turn it
            # on first
            if current_state is False and 1 < bri:
                b.set_light(l, 'on', True, transitiontime=time)
            if 1 < bri:
                b.set_light(l, 'bri', bri, transitiontime=time)
            else:
                b.set_light(l, 'on', False, transitiontime=time)
        if ct is not None:
            b.set_light(l, 'ct', ct, transitiontime=time)
