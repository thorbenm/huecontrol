import requests
from time import sleep
from hue_data import ip_address, user_id
from datetime import datetime
import scene


class Switch():
    def __init__(self, _id):
        self.id = _id
        self.last_state = self.get_state()

        self.on_function = lambda: None
        self.up_function = lambda: None
        self.down_function = lambda:None
        self.off_function = lambda: None

    def interpret_buttonevent(self, buttonevent):
        actions = {
            1000: "Initial press on button 1 (On)",
            1002: "Release after press on button 1 (On)",
            2000: "Initial press on button 2 (Dim Up)",
            2002: "Release after press on button 2 (Dim Up)",
            3000: "Initial press on button 3 (Dim Down)",
            3002: "Release after press on button 3 (Dim Down)",
            4000: "Initial press on button 4 (Off)",
            4002: "Release after press on button 4 (Off)",
            1001: "Hold on button 1 (On)",
            1003: "Release after hold on button 1 (On)",
            2001: "Hold on button 2 (Dim Up)",
            2003: "Release after hold on button 2 (Dim Up)",
            3001: "Hold on button 3 (Dim Down)",
            3003: "Release after hold on button 3 (Dim Down)",
            4001: "Hold on button 4 (Off)",
            4003: "Release after hold on button 4 (Off)"
        }
        return actions.get(buttonevent, f"Unknown event {buttonevent}")
    
    def get_state(self):
        url = f'http://{ip_address}/api/{user_id}/sensors/{self.id}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["state"]
        else:
            print('Failed to fetch data:', response.status_code)
            return None

    def get_digits(self, state):
        number = state["buttonevent"]
        s = str(number)
        return int(s[0]), int(s[3])
    
    def update(self):
        current_state = self.get_state()
        if current_state != self.last_state:
            description = current_state["buttonevent"]
            updated = current_state["lastupdated"]
            print(f"State changed: {description}, Last updated: {updated}")

            button_type, event_type = self.get_digits(current_state)
            last_button_type, _ = self.get_digits(current_state)

            time_delta = (datetime.fromisoformat(current_state["lastupdated"]) -
                          datetime.fromisoformat(self.last_state["lastupdated"])).total_seconds()

            # using a button gives 2 events: press and release
            # ignore release if press happend within last 2 seconds:
            # bet we still need to listen to the release, because there
            # is a chance we miss the press altogether
            if event_type != 2 or last_button_type != button_type or 2.0 < time_delta:
                # ignore hold (for now):
                if event_type != 1 and event_type != 3:
                    if button_type == 1:
                        self.on_function()
                    elif button_type == 2:
                        self.up_function()
                    elif button_type == 3:
                        self.down_function()
                    elif button_type == 4:
                        self.off_function()

            self.last_state = current_state


wohnzimmer_switch = Switch(84)
wohnzimmer_switch.on_function = lambda: scene.transition("hell_wohnzimmer")
wohnzimmer_switch.up_function = lambda: scene.transition("warm_wohnzimmer")
wohnzimmer_switch.down_function = lambda: scene.transition("gemutlich_wohnzimmer")
wohnzimmer_switch.off_function = lambda: scene.transition("off_wohnzimmer")


anne_switch = Switch(87)
anne_switch.on_function = lambda: scene.transition("hell_schlafzimmer")
anne_switch.up_function = lambda: scene.transition("lesen_schlafzimmer")
anne_switch.down_function = lambda: scene.transition("nachtlicht_schlafzimmer")
anne_switch.off_function = lambda: scene.transition("off_schlafzimmer")


thorben_switch = Switch(43)
thorben_switch.on_function = lambda: scene.transition("hell_schlafzimmer")
thorben_switch.up_function = lambda: scene.transition("lesen_schlafzimmer")
thorben_switch.down_function = lambda: scene.transition("nachtlicht_schlafzimmer")
thorben_switch.off_function = lambda: scene.transition("off_schlafzimmer")


def update():
    wohnzimmer_switch.update()
    anne_switch.update()
    thorben_switch.update()


def main():
    test_switch = Switch(84)
    test_switch.on_function = lambda: print("on")
    test_switch.up_function = lambda: print("up")
    test_switch.down_function = lambda: print("down")
    test_switch.off_function = lambda: print("off")
    while True:
        test_switch.update()
        sleep(.5)


if __name__ == '__main__':
    main()

