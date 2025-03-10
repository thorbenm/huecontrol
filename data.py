from _phue import min_bri


HANGELAMPE = "Hängelampe"
KUCHENLAMPE = "Küchenlampe"


all_scene_attributes = {
    "off": {"bri": 0.0, "ct": 1.0, "on": False},
    "min": {"bri": min_bri(), "ct": 1.0, "on": False},
    "dunkel": {"bri": 0.1, "ct": 1.0, "on": True},
    "gemutlich": {"bri": 0.4, "ct": 1.0, "on": True},
    "lounge": {"bri": 0.6, "ct": 1.0, "on": True},
    "warm": {"bri": 0.8, "ct": 0.75, "on": True},
    "halbwarm": {"bri": 1.0, "ct": 0.5, "on": True},
    "hell": {"bri": 1.0, "ct": 0.25, "on": True},
    "focus": {"bri": 1.0, "ct": 0.0, "on": True}
}
all_scenes = list(all_scene_attributes.keys())


wohnzimmer_light_attributes = {
  "Stehlampe": ["bri", "ct"],
  "Sofalampe Rechts": ["bri", "ct"],
  "Sofalampe Links": ["bri", "ct"],
  "Deckenlampe": ["bri"],
  "Filament": ["bri"],
  "Lichterkette": ["on"]
}
wohnzimmer_lights = list(wohnzimmer_light_attributes.keys())


schlafzimmer_light_attributes = {
  "Nachttischlampe Links": ["bri", "ct"],
  "Nachttischlampe Rechts": ["bri", "ct"],
  "Schlafzimmer " + HANGELAMPE: ["bri"]
}
schlafzimmer_lights = list(schlafzimmer_light_attributes.keys())


kinderzimmer_light_attributes = {
  "Kinderlampe": ["bri", "ct"],
  "Kinderzimmer " + HANGELAMPE: ["bri"]
}
kinderzimmer_lights = list(kinderzimmer_light_attributes.keys())


all_light_attributes = {
  **wohnzimmer_light_attributes,
  **schlafzimmer_light_attributes,
  **kinderzimmer_light_attributes
}
all_lights = list(all_light_attributes.keys())


all_rooms = [
    "wohnzimmer",
    "schlafzimmer",
    "kinderzimmer",
]


all_slave_rooms = [
    "kuche",
    "bad",
    "flur",
]


kuche_light_attributes = {
  KUCHENLAMPE + " Links": ["bri", "ct"],
  KUCHENLAMPE + " Rechts": ["bri", "ct"]
}
kuche_lights = list(kuche_light_attributes.keys())


bad_light_attributes = {
  "Spiegellampe": ["bri", "ct"],
  "Badlampe": ["bri", "ct"]
}
bad_lights = list(bad_light_attributes.keys())


flur_light_attributes = {
  "Flurlampe 1": ["bri", "ct"],
  "Flurlampe 2": ["bri", "ct"],
  "Flurlampe 3": ["bri", "ct"]
}
flur_lights = list(flur_light_attributes.keys())


def get_scene(scene, room="all"):
    if room not in [*all_rooms, "all"]:
        raise ValueError(f"Room {room} not found")

    exceptions = {
        "min": {
            "Filament": {"bri": 0.0},
            "Deckenlampe": {"bri": 0.0},
            "Schlafzimmer " + HANGELAMPE: {"bri": 0.0},
            "Kinderzimmer " + HANGELAMPE: {"bri": 0.0},
        },
        "dunkel": {
            "Filament": {"bri": 0.0},
            "Deckenlampe": {"bri": 0.0},
            "Schlafzimmer " + HANGELAMPE: {"bri": 0.0},
            "Kinderzimmer " + HANGELAMPE: {"bri": 0.0},
        },
        "gemutlich": {
            "Filament": {"bri": 0.0},
            "Deckenlampe": {"bri": 0.0},
            "Schlafzimmer " + HANGELAMPE: {"bri": 0.0},
            "Kinderzimmer " + HANGELAMPE: {"bri": 0.0},
        },
        "lounge": {
            "Filament": {"bri": 0.0},
            "Deckenlampe": {"bri": 0.0},
            "Schlafzimmer " + HANGELAMPE: {"bri": 0.0},
            "Kinderzimmer " + HANGELAMPE: {"bri": 0.0},
        },
        "warm": {
            "Filament": {"bri": 0.0},
            "Deckenlampe": {"bri": 0.0},
            "Schlafzimmer " + HANGELAMPE: {"bri": 0.0},
            "Kinderzimmer " + HANGELAMPE: {"bri": 0.0},
        },
        "halbwarm": {
            "Filament": {"bri": 0.5},
            "Deckenlampe": {"bri": 0.0},
            "Schlafzimmer " + HANGELAMPE: {"bri": 0.5},
            "Kinderzimmer " + HANGELAMPE: {"bri": 0.5},
        }
    }

    light_attributes = eval(room + "_light_attributes")
    scene_attributes = all_scene_attributes[scene]
    ret = {}
    for light, attributes in light_attributes.items():
        ret[light] = {}
        for attr in attributes:
            if attr in scene_attributes:
                ret[light][attr] = scene_attributes[attr]
        if scene in exceptions:
            if light in exceptions[scene]:
                ret[light].update(exceptions[scene][light])
    return ret


def get_lights(room):
    # not 100% clear if slave rooms should be rooms
    if room not in [*all_rooms, *all_slave_rooms, "all"]:
        raise ValueError(f"Room {room} not found")
    return eval(room + "_lights")


def get_light_attributes(room):
    if room not in [*all_rooms, *all_slave_rooms, "all"]:
        raise ValueError(f"Room {room} not found")
    return eval(room + "_light_attributes")
