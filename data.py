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
  "Play": ["bri", "ct"],
  "Sofalampe": ["bri", "ct"],
  "Kaminlampe": ["bri", "ct"],
  "Esstischlampe": ["bri"],
  "Lichterkette": ["on"],
}


schlafzimmer_light_attributes = {
  "Nachttischlampe Links": ["bri", "ct"],
  "Nachttischlampe Rechts": ["bri", "ct"],
  "Schlafzimmer " + HANGELAMPE: ["bri"],
}


kinderzimmer_light_attributes = {
  "Kinderlampe": ["bri", "ct"],
  "Kinderzimmer " + HANGELAMPE: ["bri"],
}


arbeitszimmer_light_attributes = {
  "Bildschirm": ["bri", "ct"],
  "Deckenlampe Arbeitszimmer": ["bri", "ct"],
  "Globus": ["bri", "ct"],
}

all_light_attributes = {
  **wohnzimmer_light_attributes,
  **schlafzimmer_light_attributes,
  **kinderzimmer_light_attributes,
  **arbeitszimmer_light_attributes
}
all_lights = list(all_light_attributes.keys())


all_rooms = [
    "wohnzimmer",
    "schlafzimmer",
    "kinderzimmer",
    "arbeitszimmer"
]


all_light_attributes = {}
for r in all_rooms:
    assert r + "_light_attributes" in globals(), f"{r}_lights not found"
    all_light_attributes.update(eval(r + "_light_attributes"))
    exec(f"{r}_lights = list(eval(r + '_light_attributes').keys())")


all_slave_rooms = [
    "kuche",
    "bad",
    "flur",
    "diele",
    "klo",
]


kuche_light_attributes = {
  KUCHENLAMPE + " 1": ["bri", "ct"],
  KUCHENLAMPE + " 2": ["bri", "ct"],
  "Filament": ["bri"],
}
kuche_lights = list(kuche_light_attributes.keys())


bad_light_attributes = {
  "Badlampe": ["bri", "ct"],
}
bad_lights = list(bad_light_attributes.keys())


flur_light_attributes = {
  "Flurlampe": ["bri", "ct"],
  "Schranklampe Anne": ["bri"],
  "Schranklampe Thorben": ["bri"],
}
flur_lights = list(flur_light_attributes.keys())


diele_light_attributes = {
  "Garderobenlampe" : ["bri", "ct"],
  "Dielenlampe" : ["bri", "ct"],
}
diele_lights = list(diele_light_attributes.keys())


klo_light_attributes = {
  "Spiegellampe" : ["bri", "ct"],
}
klo_lights = list(klo_light_attributes.keys())


all_slave_lights = [*kuche_lights, *bad_lights, *flur_lights, *diele_lights, *klo_lights]


buttons = {
    '434e02f5-0679-47d8-afb7-7e74ba8b0f0a': ['wohnzimmer', 'on'],
    '9b85666c-ff81-4c8c-95d8-9034b74e9c57': ['wohnzimmer', 'up'],
    '2cdf8ceb-d272-44fb-ad7e-a9903045633a': ['wohnzimmer', 'down'],
    '86ccd746-e412-4089-81ab-882c4826bdaf': ['wohnzimmer', 'off'],

    '40d45630-a6a3-461c-bbb9-240788c87910': ['wohnzimmer', 'on'],
    '49b46ed1-a774-4656-8456-ec262b07a375': ['wohnzimmer', 'up'],
    'bdaf080a-e651-4e30-bfe6-1e169eb9b6f4': ['wohnzimmer', 'down'],
    '6133ace3-7a9e-4de8-a1a6-ec0f6bf9c3c4': ['wohnzimmer', 'off'],

    '5610d840-191e-4ebb-9087-1db469842897': ['schlafzimmer', 'on'],
    'cacdfa45-d676-4c3f-af87-e144c1036d86': ['schlafzimmer', 'up'],
    '772ca980-dbdf-4c09-854c-52cd0054835e': ['schlafzimmer', 'down'],
    '3105cbbd-9559-45f4-b470-591e75977014': ['schlafzimmer', 'off'],

    '78a2ea22-6d24-44b8-8129-4628f8fc1486': ['schlafzimmer', 'on'],
    '4583c212-827e-44aa-b89f-91312f8b5d1c': ['schlafzimmer', 'up'],
    '42fc8925-9d12-4ee2-bcc9-daaa984689ec': ['schlafzimmer', 'down'],
    'bed51e86-48ef-4e72-a6ac-732a2d149703': ['schlafzimmer', 'off'],

    '7651940a-eadc-44b6-8757-75ac59df36bf': ['kinderzimmer', 'on'],
    'c2fa050b-7c44-45db-9df7-53c9fb5f23c1': ['kinderzimmer', 'up'],
    'da413bc1-b656-4679-a804-3a73e9ee146d': ['kinderzimmer', 'down'],
    'be2ac1af-410c-426d-a673-fcabcd317b61': ['kinderzimmer', 'off'],

    'a759cbf5-505a-47a8-8df8-c2890e346c9a': ['arbeitszimmer', 'on'],
    'a8f4487b-34c9-4d11-8b69-3740d2cfbee4': ['arbeitszimmer', 'up'],
    '4f4ae822-d861-43d0-81ab-df0d381c50c2': ['arbeitszimmer', 'down'],
    '9f2fd579-addd-41f5-a05b-f704d3fff603': ['arbeitszimmer', 'off'],
}


def get_scene(scene, rooms="all"):
    if rooms == "all":
        rooms = all_rooms
    elif isinstance(rooms, str):
        rooms = [rooms]
    else:
        rooms = rooms

    exceptions = {
        "min": {
            "Filament": {"bri": 0.0},
            "Deckenlampe": {"bri": 0.0},
            "Schlafzimmer " + HANGELAMPE: {"bri": 0.0},
            "Kinderzimmer " + HANGELAMPE: {"bri": 0.0},
            "Esstischlampe": {"bri": 0.0},
            "Deckenlampe Arbeitszimmer": {"bri": 0.0},
        },
        "dunkel": {
            "Filament": {"bri": 0.0},
            "Deckenlampe": {"bri": 0.0},
            "Schlafzimmer " + HANGELAMPE: {"bri": 0.0},
            "Kinderzimmer " + HANGELAMPE: {"bri": 0.0},
            "Esstischlampe": {"bri": 0.0},
            "Deckenlampe Arbeitszimmer": {"bri": 0.0},
        },
        "gemutlich": {
            "Filament": {"bri": 0.0},
            "Deckenlampe": {"bri": 0.0},
            "Schlafzimmer " + HANGELAMPE: {"bri": 0.0},
            "Kinderzimmer " + HANGELAMPE: {"bri": 0.0},
            "Esstischlampe": {"bri": 0.0},
            "Deckenlampe Arbeitszimmer": {"bri": min_bri()},
        },
        "lounge": {
            "Filament": {"bri": 0.0},
            "Deckenlampe": {"bri": 0.0},
            "Schlafzimmer " + HANGELAMPE: {"bri": 0.0},
            "Kinderzimmer " + HANGELAMPE: {"bri": 0.0},
            "Esstischlampe": {"bri": 0.25},
            "Deckenlampe Arbeitszimmer": {"bri": 0.25},
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
            "Schlafzimmer " + HANGELAMPE: {"bri": 0.8},
            "Kinderzimmer " + HANGELAMPE: {"bri": 0.8},
        }
    }

    light_attributes = {}
    for r in rooms:
        light_attributes = {**light_attributes, **eval(r + "_light_attributes")}
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


def get_lights(room, include_slaves=False):
    # not 100% clear if slave rooms should be rooms
    if room not in [*all_rooms, *all_slave_rooms, "all"]:
        raise ValueError(f"Room {room} not found")
    if include_slaves and room is "all":
        return eval(room + "_lights") + all_slave_lights
    else:
        return eval(room + "_lights")


def get_light_attributes(room):
    if room not in [*all_rooms, *all_slave_rooms, "all"]:
        raise ValueError(f"Room {room} not found")
    return eval(room + "_light_attributes")


def get_rooms():
    return all_rooms
