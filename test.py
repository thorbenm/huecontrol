#!/usr/bin/python3
import requests
from phue import Bridge

json_data = requests.get("https://discovery.meethue.com").json()
ip_address = json_data[0]['internalipaddress']

b = Bridge(ip_address)
b.connect
b.set_light('Hue Go', 'bri', 255)
