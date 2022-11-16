import requests
import time

last_updated = requests.get("http://philips-hue/api/0kw0OaACr9vQlk2w-Km8saJAL34wqas1ohczjNQX/sensors").json()[str(87)]["state"]["lastupdated"]
while True:
    r = requests.get("http://philips-hue/api/0kw0OaACr9vQlk2w-Km8saJAL34wqas1ohczjNQX/sensors").json()[str(87)]["state"]
    if last_updated != r["lastupdated"]:
        print(r["buttonevent"])
        last_updated = r["lastupdated"]
    time.sleep(.1)
