#!/usr/bin/python3
import argparse
import scene
import ambient
import toolbox
import data
import os
import time
import schedule


PROGRESS_FILE = "/home/pi/wakeup_in_progress"


def read_progress_file(rooms):
    ret = []
    for r in rooms:
        if os.path.exists(PROGRESS_FILE + "_" + r):
            ret.append(r)
    return ret


def _sleep(t, rooms):
    rooms = rooms.copy()
    start = time.time()
    progress_file_last_read = -float("inf")
    read_progress_file_every = 10.0
    while True:
        current_time = time.time()
        if read_progress_file_every < current_time - progress_file_last_read:
            rooms = read_progress_file(rooms)
            progress_file_last_read = current_time
        if t < current_time - start or len(rooms) == 0:
            break
        time.sleep(.1)
    return read_progress_file(rooms)


def wakeup(t1, t2, t3, t4, rooms):
    rooms = rooms.copy()
    try:
        for r in rooms:
            if os.path.exists(PROGRESS_FILE + "_" + r):
                rooms.remove(r)

        if len(rooms) == 0:
            return

        for r in rooms:
            os.mknod(PROGRESS_FILE + "_" + r)  # touch

        ingnore_on_start = ["Nachttischlampe Rechts"]
        override_attributes = {i: {"bri": 0.0} for i in ingnore_on_start}

        scene.transition(name="min", rooms=rooms, increase_only=True, abort_wakeup=False, _override=override_attributes)

        rooms = _sleep(t1, rooms)

        if len(rooms) == 0:
            return

        scene.transition(name="gemutlich", rooms=rooms, time=t2, increase_only=True, abort_wakeup=False, _override=override_attributes)

        rooms = _sleep(t2, rooms)
        if len(rooms) == 0:
            return

        scene.transition(name="halbwarm", rooms=rooms, time=t3, increase_only=True, abort_wakeup=False)

        if t4 is not None:
            rooms = _sleep(t3, rooms)
            if len(rooms) == 0:
                return

            scene.transition(name="hell", rooms=rooms, time=t4, increase_only=True, abort_wakeup=False)

    finally:
        for r in rooms:
            os.remove(PROGRESS_FILE + "_" + r)


def parse_args(input_args=None):
    if isinstance(input_args, str):
        input_args = input_args.split()
        this_file = __file__.split("/")[-1].removesuffix(".py")
        if input_args[0].startswith(this_file):
            input_args = input_args[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('-t1', type=str, default='1s', dest='t1')
    parser.add_argument('-t2', type=str, default='5m', dest='t2')
    parser.add_argument('-t3', type=str, default='5m', dest='t3')
    parser.add_argument('-t4', type=str, default='auto', dest='t4')

    for r in data.get_rooms():
        parser.add_argument(f'--{r}', f'-{r[0]}', action='store_true', dest=r)

    args = parser.parse_args(input_args if input_args else None)

    if not any(getattr(args, r) for r in data.get_rooms()):
        for r in data.get_rooms():
            setattr(args, r, True)

    args.t1 = toolbox.convert_time_string(args.t1)
    args.t2 = toolbox.convert_time_string(args.t2)
    args.t3 = toolbox.convert_time_string(args.t3)

    if args.t4 == "auto":
        simulated_bri = ambient.get_simulated_bri()
        print(f"simulated_bri={simulated_bri}")
        if (.02 < simulated_bri and schedule.get_variable("scheduled_scene") == "hell"):
            args.t4 = toolbox.map(simulated_bri, .02, .5, 109 * 60, 5 * 60, clamp=True)
        else:
            args.t4 = None
        print(f"t4={args.t4}")
    else:
        args.t4 = toolbox.convert_time_string(args.t4)

    return args


def main(input_args=None):
    args = parse_args(input_args)
    rooms = [r for r in data.get_rooms() if getattr(args, r)]
    wakeup(args.t1, args.t2, args.t3, args.t4, rooms)


if __name__ == '__main__':
    main()
