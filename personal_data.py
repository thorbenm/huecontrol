import json

d = ""
with open("/home/pi/.python_hue") as f:
    d = f.read()

d = json.loads(d)

ip_address = list(d.keys())[0]
user_id = d[ip_address]["username"]
