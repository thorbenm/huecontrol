import requests
from time import sleep, time
from hue_data import ip_address, user_id
from datetime import datetime
import scene
import subprocess


class Switch():
    def __init__(self, _id):
        self.id = _id
        self.last_state = self.get_state()

        self.on_press_function = lambda: None
        self.up_press_function = lambda: None
        self.down_press_function = lambda:None
        self.off_press_function = lambda: None

        self.on_long_press_function = lambda: None
        self.up_long_press_function = lambda: None
        self.down_long_press_function = lambda:None
        self.off_long_press_function = lambda: None

        self.long_press_duration = 1.0  # which is 3 seconds in reality

        self.on_mode = "long press"
        self.up_mode = "long press"
        self.down_mode = "long press"
        self.off_mode = "long press"

    def get_state(self):
        url = f'http://{ip_address}/api/{user_id}/sensors/{self.id}'
        response = requests.get(url)
        if response.status_code == 200:
            d = response.json()["state"]
            if d["buttonevent"] is None:
                return None
            button_type, event_type = self.get_digits(d["buttonevent"])

            button_type_dict = dict()
            button_type_dict[1] = "on"
            button_type_dict[2] = "up"
            button_type_dict[3] = "down"
            button_type_dict[4] = "off"

            event_type_dict = dict()
            event_type_dict[0] = "press"
            event_type_dict[1] = "hold"
            event_type_dict[2] = "press release"
            event_type_dict[3] = "hold release"

            button_type = button_type_dict[button_type]
            event_type = event_type_dict[event_type]

            ret = dict()
            ret["lastupdated"] = d["lastupdated"]
            ret["button_type"] = button_type
            ret["event_type"] = event_type

            return ret
        else:
            print('Failed to fetch data:', response.status_code)
            return None

    def get_digits(self, buttonevent):
        if buttonevent:
            s = str(buttonevent)
            return int(s[0]), int(s[3])
        return -1, -1

    def check_modes(self):
        for v in [self.on_mode, self.up_mode, self.down_mode, self.off_mode]:
            if v != "long press" and v != "hold":
                raise RuntimeError('invalid mode: '+ v)
    
    def update(self):
        self.check_modes()
        state = self.get_state()
        if state != self.last_state:
            print(state)

            if state["event_type"] == "press release":
                press_function_name = state["button_type"] + "_press_function"
                press_function = getattr(self, press_function_name)
                press_function()
            if state["event_type"] == "hold":
                if self.last_state["event_type"] != "hold":
                    # if current and last state are hold, its probably still the same hold
                    mode = getattr(self, state["button_type"] + "_mode")
                    if mode == "long press":
                        start = time()
                        while self.get_state()["event_type"] == "hold":
                            sleep(.25)
                            if self.long_press_duration <= time() - start:
                                long_press_function_name = state["button_type"] + "_long_press_function"
                                long_press_function = getattr(self, long_press_function_name)
                                long_press_function()
                                break

            self.last_state = state


def run_detached_shell(command):
    full_command = f"( (nohup {command} > /dev/null 2> /dev/null < /dev/null) & )"
    subprocess.Popen(full_command, shell=True, executable="/bin/bash")


wohnzimmer_switch = Switch(84)
wohnzimmer_switch.on_press_function = lambda: scene.transition("hell_wohnzimmer")
wohnzimmer_switch.up_press_function = lambda: scene.transition("warm_wohnzimmer")
wohnzimmer_switch.down_press_function = lambda: scene.transition("gemutlich_wohnzimmer")
wohnzimmer_switch.off_press_function = lambda: scene.transition("off_wohnzimmer")

wohnzimmer_switch.on_long_press_function = lambda: run_detached_shell("/home/pi/Programming/huecontrol/wakeup.py -w -t2 2m")
wohnzimmer_switch.off_long_press_function = lambda: scene.transition("off_wohnzimmer", time=15*60)


schlafzimmer_bed_switch = Switch(87)
schlafzimmer_bed_switch.on_press_function = lambda: scene.transition("hell_schlafzimmer")
schlafzimmer_bed_switch.up_press_function = lambda: scene.transition("lesen_schlafzimmer")
schlafzimmer_bed_switch.down_press_function = lambda: scene.transition("nachtlicht_schlafzimmer")
schlafzimmer_bed_switch.off_press_function = lambda: scene.transition("off_schlafzimmer")

schlafzimmer_bed_switch.on_long_press_function = lambda: run_detached_shell("/home/pi/Programming/huecontrol/wakeup.py -s -t2 1m")
schlafzimmer_bed_switch.off_long_press_function = lambda: scene.transition("off_schlafzimmer", time=3*60)


schlafzimmer_door_switch = Switch(43)
schlafzimmer_door_switch.on_press_function = lambda: scene.transition("hell_schlafzimmer")
schlafzimmer_door_switch.up_press_function = lambda: scene.transition("lesen_schlafzimmer")
schlafzimmer_door_switch.down_press_function = lambda: scene.transition("nachtlicht_schlafzimmer")
schlafzimmer_door_switch.off_press_function = lambda: scene.transition("off_schlafzimmer")

schlafzimmer_door_switch.on_long_press_function = lambda: run_detached_shell("/home/pi/Programming/huecontrol/wakeup.py -s -t2 1m")
schlafzimmer_door_switch.off_long_press_function = lambda: scene.transition("off_schlafzimmer", time=3*60)


def update():
    wohnzimmer_switch.update()
    schlafzimmer_bed_switch.update()
    schlafzimmer_door_switch.update()


def main():
    test_switch = Switch(84)
    test_switch.on_press_function = lambda: print("on press")
    test_switch.up_press_function = lambda: print("up press")
    test_switch.down_press_function = lambda: print("down press")
    test_switch.off_press_function = lambda: print("off press")

    test_switch.on_long_press_function = lambda: print("on hold")
    test_switch.up_long_press_function = lambda: print("up hold")
    test_switch.down_long_press_function = lambda: print("down hold")
    test_switch.off_long_press_function = lambda: print("off hold")
    while True:
        test_switch.update()
        sleep(.5)


if __name__ == '__main__':
    main()

