import requests
from hue_data import user_id
from time import sleep
import sys
import json

json_data = requests.get("https://discovery.meethue.com").json()
ip_address = json_data[0]['internalipaddress']

def get_sensor_state(sensor_id):
    response = requests.get("http://%s/api/%s/sensors/%d" % (
                            ip_address, user_id, sensor_id))
    json_data = json.loads(response.text)
    return json_data['state']['presence']

valid_indices = []
for j in range(100):
    try:
        get_sensor_state(j)
        print(str(j) + " valid")
        valid_indices.append(j)
    except:
        print(str(j) + " invalid")
        pass
while True:
    for j in valid_indices:
        print(str(j) + ": " + str(get_sensor_state(j)))
    print(" ")
    sleep(0.5)
