import requests
from time import sleep, time
from hue_data import ip_address, user_id
from datetime import datetime
import scene
import subprocess
import data
import _phue
import scheduled_scene


class Switch():
    def __init__(self, _id):
        self.id = _id
        self.last_state = self.get_state()

        self.on_press_function = lambda: None
        self.up_press_function = lambda: None
        self.down_press_function = lambda: None
        self.off_press_function = lambda: None

        self.on_long_press_function = lambda: None
        self.up_long_press_function = lambda: None
        self.down_long_press_function = lambda: None
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


class ButtonHandler():
    def __init__(self, room, update_offset=0.0):
        self.room = room
        self.current_scene = data.all_scenes[len(data.all_scenes) // 2]
        self.current_scene = self.get_current_scene()
        self.update_every = 15.0 * 60.0
        self.last_updated = time() + self.update_every + update_offset

    def get_current_scene(self):
        def difference(scene):
            lights = getattr(data, self.room + "_lights")
            lights = [lights[0]]
            ret = 0.0
            for l in lights:
                light_name = l[0]
                light_attributes = l[1]
                for a in light_attributes:
                    monitor = float(getattr(_phue, "get_" + a)(light_name))
                    setpoint = float(getattr(data, scene + "_" + self.room)[light_name][a])
                    ret += abs(monitor - setpoint)
            return ret

        # efficient search by GPT:

        # Start by checking the current scene first
        min_difference = difference(self.current_scene)
        best_scene = self.current_scene

        # Check upwards in the list until difference increases
        current_index = data.all_scenes.index(self.current_scene)
        for i in range(current_index + 1, len(data.all_scenes)):
            scene = data.all_scenes[i]
            current_difference = difference(scene)
            if current_difference > min_difference:
                break
            min_difference = current_difference
            best_scene = scene

        # Check downwards in the list until difference increases
        for i in range(current_index - 1, -1, -1):
            scene = data.all_scenes[i]
            current_difference = difference(scene)
            if current_difference > min_difference:
                break
            min_difference = current_difference
            best_scene = scene

        #print(self.room, best_scene)
        return best_scene

    def update(self):
        now = time()
        if self.update_every < now - self.last_updated:
            self.force_update()
            self.last_updated = now + self.update_every

    def force_update(self):
        self.current_scene = self.get_current_scene()

    def step(self, step):
        index = data.all_scenes.index(self.current_scene)
        index += step
        index = max(0, index)
        index = min(index, len(data.all_scenes) - 1)
        scene.transition(data.all_scenes[index] + "_" + self.room)
        self.current_scene = data.all_scenes[index]

    def step_down(self):
        self.step(-1)

    def step_up(self):
        self.step(1)


def run_detached_shell(command):
    full_command = f"( (nohup {command} > /dev/null 2> /dev/null < /dev/null) & )"
    subprocess.Popen(full_command, shell=True, executable="/bin/bash")


wbh = ButtonHandler("wohnzimmer")

wohnzimmer_switch = Switch(84)
wohnzimmer_switch.on_press_function = lambda: (scheduled_scene.transition_wohnzimmer(), wbh.force_update())
wohnzimmer_switch.up_press_function = lambda: wbh.step_up()
wohnzimmer_switch.down_press_function = lambda: wbh.step_down()
wohnzimmer_switch.off_press_function = lambda: (scene.transition("off_wohnzimmer"), setattr(wbh, 'current_scene', 'off'))

wohnzimmer_switch.on_long_press_function = lambda: run_detached_shell("/home/pi/Programming/huecontrol/wakeup.py -w -t2 3m")
wohnzimmer_switch.off_long_press_function = lambda: scene.transition("off_wohnzimmer", time=30*60)


sbh = ButtonHandler("schlafzimmer", update_offset=7.5*60.0)

schlafzimmer_bed_switch = Switch(87)
schlafzimmer_bed_switch.on_press_function = lambda: (scheduled_scene.transition_schlafzimmer(), sbh.force_update())
schlafzimmer_bed_switch.up_press_function = lambda: sbh.step_up()
schlafzimmer_bed_switch.down_press_function = lambda: sbh.step_down()
schlafzimmer_bed_switch.off_press_function = lambda: (scene.transition("off_schlafzimmer"), setattr(sbh, 'current_scene', 'off'))

schlafzimmer_bed_switch.on_long_press_function = lambda: run_detached_shell("/home/pi/Programming/huecontrol/wakeup.py -s -t2 1m")
schlafzimmer_bed_switch.off_long_press_function = lambda: (scene.transition("off_schlafzimmer", time=3*60), setattr(sbh, 'current_scene', 'off'))


schlafzimmer_door_switch = Switch(43)
schlafzimmer_door_switch.on_press_function = lambda: (scheduled_scene.transition_schlafzimmer(), sbh.force_update())
schlafzimmer_door_switch.up_press_function = lambda: sbh.step_up()
schlafzimmer_door_switch.down_press_function = lambda: sbh.step_down()
schlafzimmer_door_switch.off_press_function = lambda: (scene.transition("off_schlafzimmer"), setattr(sbh, 'current_scene', 'off'))

schlafzimmer_door_switch.on_long_press_function = lambda: run_detached_shell("/home/pi/Programming/huecontrol/wakeup.py -s -t2 1m")
schlafzimmer_door_switch.off_long_press_function = lambda: (scene.transition("off_schlafzimmer", time=3*60), setattr(sbh, 'current_scene', 'off'))


def update():
    wohnzimmer_switch.update()
    schlafzimmer_bed_switch.update()
    schlafzimmer_door_switch.update()
    wbh.update()
    sbh.update()


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

