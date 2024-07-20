import requests
from hue_data import ip_address, user_id

def check_sensors(base_url, start_id=1, end_id=100):
    valid_sensors = []
    for sensor_id in range(start_id, end_id + 1):
        url = f"{base_url}/sensors/{sensor_id}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'state' in data:  # Checking if 'state' key is present in the response
                valid_sensors.append((sensor_id, data))
                print(f"Sensor ID {sensor_id} is valid: {data['name']}")
            else:
                print(f"Sensor ID {sensor_id} does not correspond to a valid device.")
        else:
            print(f"Sensor ID {sensor_id} failed with status code {response.status_code}")
    return valid_sensors

def main():
    base_url = f"http://{ip_address}/api/{user_id}"
    valid_sensors = check_sensors(base_url)
    if not valid_sensors:
        print("No valid sensors found in the specified range.")
    else:
        print(f"Found {len(valid_sensors)} valid sensors.")

if __name__ == '__main__':
    main()

