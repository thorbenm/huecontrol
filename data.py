from _phue import min_bri


HANGELAMPE = "Hängelampe"
KUCHENLAMPE = "Küchenlampe"


wohnzimmer_lights = [
                     ["Stehlampe", ["bri", "ct"]],
                     ["Fensterlampe", ["bri", "ct"]],
                     ["Sofalampe Rechts", ["bri", "ct"]],
                     ["Sofalampe Links", ["bri", "ct"]],
                     ["Deckenlampe", ["bri"]],
                     ["Filament", ["bri"]],
                     ["Lichterkette", ["on"]],
                    ]

schlafzimmer_lights = [
                       ["Nachttischlampe", ["bri", "ct"]],
                       ["Wickeltischlampe", ["bri", "ct"]],
                       ["Schlafzimmer " + HANGELAMPE, ["bri"]],
                      ]

all_lights = [
              *wohnzimmer_lights,
              *schlafzimmer_lights,
             ]

kuche_lights = [
                [KUCHENLAMPE + " Links", ["bri", "ct"]],
                [KUCHENLAMPE + " Rechts", ["bri", "ct"]],
               ]

bad_lights = [
              ["Spiegellampe", ["bri", "ct"]],
              ["Badlampe", ["bri", "ct"]],
             ]

flur_lights = [
               ["Flurlampe 1", ["bri", "ct"]],
               ["Flurlampe 2", ["bri", "ct"]],
               ["Flurlampe 3", ["bri", "ct"]],
              ]


all_scenes = list()


all_scenes.append("off")

off_wohnzimmer = dict()
off_wohnzimmer["Stehlampe"] = {"bri": 0.0, "ct": 1.0}
off_wohnzimmer["Fensterlampe"] = {"bri": 0.0, "ct": 1.0}
off_wohnzimmer["LED Streifen"] = {"bri": 0.0, "ct": 1.0}
off_wohnzimmer["Sofalampe Rechts"] = {"bri": 0.0, "ct": 1.0}
off_wohnzimmer["Sofalampe Links"] = {"bri": 0.0, "ct": 1.0}
off_wohnzimmer["Filament"] = {"bri": 0.0}
off_wohnzimmer["Deckenlampe"] = {"bri": 0.0}
off_wohnzimmer["Lichterkette"] = {"on": False}

off_schlafzimmer = dict()
off_schlafzimmer["Nachttischlampe"] = {"bri": 0.0, "ct": 1.0}
off_schlafzimmer["Wickeltischlampe"] = {"bri": 0.0, "ct": 1.0}
off_schlafzimmer["Schlafzimmer " + HANGELAMPE] = {"bri": 0.0}

off = {**off_wohnzimmer, **off_schlafzimmer}


all_scenes.append("nachtlicht")

nachtlicht_wohnzimmer = dict()
nachtlicht_wohnzimmer["Stehlampe"] = {"bri": 0.0, "ct": 1.0}
nachtlicht_wohnzimmer["Fensterlampe"] = {"bri": 0.0, "ct": 1.0}
nachtlicht_wohnzimmer["LED Streifen"] = {"bri": 0.0, "ct": 1.0}
nachtlicht_wohnzimmer["Sofalampe Rechts"] = {"bri": 0.0, "ct": 1.0}
nachtlicht_wohnzimmer["Sofalampe Links"] = {"bri": 0.0, "ct": 1.0}
nachtlicht_wohnzimmer["Filament"] = {"bri": 0.0}
nachtlicht_wohnzimmer["Deckenlampe"] = {"bri": 0.0}
nachtlicht_wohnzimmer["Lichterkette"] = {"on": False}

nachtlicht_schlafzimmer = dict()
nachtlicht_schlafzimmer["Nachttischlampe"] = {"bri": 0.0, "ct": 1.0}
nachtlicht_schlafzimmer["Wickeltischlampe"] = {"bri": min_bri(), "ct": 1.0}
nachtlicht_schlafzimmer["Schlafzimmer " + HANGELAMPE] = {"bri": 0.0}

nachtlicht = {**nachtlicht_wohnzimmer, **nachtlicht_schlafzimmer}


all_scenes.append("min")

min_wohnzimmer = dict()
min_wohnzimmer["Stehlampe"] = {"bri": min_bri(), "ct": 1.0}
min_wohnzimmer["Fensterlampe"] = {"bri": min_bri(), "ct": 1.0}
min_wohnzimmer["LED Streifen"] = {"bri": min_bri(), "ct": 1.0}
min_wohnzimmer["Sofalampe Rechts"] = {"bri": min_bri(), "ct": 1.0}
min_wohnzimmer["Sofalampe Links"] = {"bri": min_bri(), "ct": 1.0}
min_wohnzimmer["Filament"] = {"bri": 0.0}
min_wohnzimmer["Deckenlampe"] = {"bri": 0.0}
min_wohnzimmer["Lichterkette"] = {"on": False}

min_schlafzimmer = dict()
min_schlafzimmer["Nachttischlampe"] = {"bri": min_bri(), "ct": 1.0}
min_schlafzimmer["Wickeltischlampe"] = {"bri": min_bri(), "ct": 1.0}
min_schlafzimmer["Schlafzimmer " + HANGELAMPE] = {"bri": 0.0}

min = {**min_wohnzimmer, **min_schlafzimmer}


all_scenes.append("dunkel")

dunkel_wohnzimmer = dict()
dunkel_wohnzimmer["Stehlampe"] = {"bri": .1, "ct": 1.0}
dunkel_wohnzimmer["Fensterlampe"] = {"bri": .1, "ct": 1.0}
dunkel_wohnzimmer["LED Streifen"] = {"bri": .1, "ct": 1.0}
dunkel_wohnzimmer["Sofalampe Rechts"] = {"bri": .1, "ct": 1.0}
dunkel_wohnzimmer["Sofalampe Links"] = {"bri": .1, "ct": 1.0}
dunkel_wohnzimmer["Filament"] = {"bri": 0.0}
dunkel_wohnzimmer["Deckenlampe"] = {"bri": 0.0}
dunkel_wohnzimmer["Lichterkette"] = {"on": True}

dunkel_schlafzimmer = dict()
dunkel_schlafzimmer["Nachttischlampe"] = {"bri": .1, "ct": 1.0}
dunkel_schlafzimmer["Wickeltischlampe"] = {"bri": .1, "ct": 1.0}
dunkel_schlafzimmer["Schlafzimmer " + HANGELAMPE] = {"bri": 0.0}

dunkel = {**dunkel_wohnzimmer, **dunkel_schlafzimmer}


all_scenes.append("lesen")

lesen_wohnzimmer = dict()
lesen_wohnzimmer["Stehlampe"] = {"bri": .1, "ct": 1.0}
lesen_wohnzimmer["Fensterlampe"] = {"bri": .5, "ct": 1.0}
lesen_wohnzimmer["LED Streifen"] = {"bri": .1, "ct": 1.0}
lesen_wohnzimmer["Sofalampe Rechts"] = {"bri": .1, "ct": 1.0}
lesen_wohnzimmer["Sofalampe Links"] = {"bri": .1, "ct": 1.0}
lesen_wohnzimmer["Filament"] = {"bri": 0.0}
lesen_wohnzimmer["Deckenlampe"] = {"bri": 0.0}
lesen_wohnzimmer["Lichterkette"] = {"on": True}

lesen_schlafzimmer = dict()
lesen_schlafzimmer["Nachttischlampe"] = {"bri": .25, "ct": 1.0}
lesen_schlafzimmer["Wickeltischlampe"] = {"bri": min_bri(), "ct": 1.0}
lesen_schlafzimmer["Schlafzimmer " + HANGELAMPE] = {"bri": 0.0}

lesen = {**lesen_wohnzimmer, **lesen_schlafzimmer}


all_scenes.append("gemutlich")

gemutlich_wohnzimmer = dict()
gemutlich_wohnzimmer["Stehlampe"] = {"bri": .4, "ct": 1.0}
gemutlich_wohnzimmer["Fensterlampe"] = {"bri": .4, "ct": 1.0}
gemutlich_wohnzimmer["LED Streifen"] = {"bri": .4, "ct": 1.0}
gemutlich_wohnzimmer["Sofalampe Rechts"] = {"bri": .4, "ct": 1.0}
gemutlich_wohnzimmer["Sofalampe Links"] = {"bri": .4, "ct": 1.0}
gemutlich_wohnzimmer["Filament"] = {"bri": 0.0}
gemutlich_wohnzimmer["Deckenlampe"] = {"bri": 0.0}
gemutlich_wohnzimmer["Lichterkette"] = {"on": True}

gemutlich_schlafzimmer = dict()
gemutlich_schlafzimmer["Nachttischlampe"] = {"bri": .4, "ct": 1.0}
gemutlich_schlafzimmer["Wickeltischlampe"] = {"bri": .4, "ct": 1.0}
gemutlich_schlafzimmer["Schlafzimmer " + HANGELAMPE] = {"bri": 0.0}

gemutlich = {**gemutlich_wohnzimmer, **gemutlich_schlafzimmer}


all_scenes.append("warm")

warm_wohnzimmer = dict()
warm_wohnzimmer["Stehlampe"] = {"bri": .8, "ct": .7}
warm_wohnzimmer["Fensterlampe"] = {"bri": .8, "ct": .7}
warm_wohnzimmer["LED Streifen"] = {"bri": .8, "ct": .7}
warm_wohnzimmer["Sofalampe Rechts"] = {"bri": .8, "ct": .7}
warm_wohnzimmer["Sofalampe Links"] = {"bri": .8, "ct": .7}
warm_wohnzimmer["Filament"] = {"bri": 0.0}
warm_wohnzimmer["Deckenlampe"] = {"bri": 0.0}
warm_wohnzimmer["Lichterkette"] = {"on": True}

warm_schlafzimmer = dict()
warm_schlafzimmer["Nachttischlampe"] = {"bri": .8, "ct": .7}
warm_schlafzimmer["Wickeltischlampe"] = {"bri": .8, "ct": .7}
warm_schlafzimmer["Schlafzimmer " + HANGELAMPE] = {"bri": 0.0}

warm = {**warm_wohnzimmer, **warm_schlafzimmer}


all_scenes.append("halbwarm")

halbwarm_wohnzimmer = dict()
halbwarm_wohnzimmer["Stehlampe"] = {"bri": 1.0, "ct": .5}
halbwarm_wohnzimmer["Fensterlampe"] = {"bri": 1.0, "ct": .5}
halbwarm_wohnzimmer["LED Streifen"] = {"bri": 1.0, "ct": .5}
halbwarm_wohnzimmer["Sofalampe Rechts"] = {"bri": 1.0, "ct": .5}
halbwarm_wohnzimmer["Sofalampe Links"] = {"bri": 1.0, "ct": .5}
halbwarm_wohnzimmer["Filament"] = {"bri": 0.5}
halbwarm_wohnzimmer["Deckenlampe"] = {"bri": 0.0}
halbwarm_wohnzimmer["Lichterkette"] = {"on": True}

halbwarm_schlafzimmer = dict()
halbwarm_schlafzimmer["Nachttischlampe"] = {"bri": 1.0, "ct": .5}
halbwarm_schlafzimmer["Wickeltischlampe"] = {"bri": 1.0, "ct": .5}
halbwarm_schlafzimmer["Schlafzimmer " + HANGELAMPE] = {"bri": .5}

halbwarm = {**halbwarm_wohnzimmer, **halbwarm_schlafzimmer}


all_scenes.append("hell")

hell_wohnzimmer = dict()
hell_wohnzimmer["Stehlampe"] = {"bri": 1.0, "ct": .25}
hell_wohnzimmer["Fensterlampe"] = {"bri": 1.0, "ct": .25}
hell_wohnzimmer["LED Streifen"] = {"bri": 1.0, "ct": .25}
hell_wohnzimmer["Sofalampe Rechts"] = {"bri": 1.0, "ct": .25}
hell_wohnzimmer["Sofalampe Links"] = {"bri": 1.0, "ct": .25}
hell_wohnzimmer["Filament"] = {"bri": 1.0}
hell_wohnzimmer["Deckenlampe"] = {"bri": 1.0}
hell_wohnzimmer["Lichterkette"] = {"on": True}

hell_schlafzimmer = dict()
hell_schlafzimmer["Nachttischlampe"] = {"bri": 1.0, "ct": .25}
hell_schlafzimmer["Wickeltischlampe"] = {"bri": 1.0, "ct": .25}
hell_schlafzimmer["Schlafzimmer " + HANGELAMPE] = {"bri": 1.0}

hell = {**hell_wohnzimmer, **hell_schlafzimmer}


all_scenes.append("focus")

focus_wohnzimmer = dict()
focus_wohnzimmer["Stehlampe"] = {"bri": 1.0, "ct": 0.0}
focus_wohnzimmer["Fensterlampe"] = {"bri": 1.0, "ct": 0.0}
focus_wohnzimmer["LED Streifen"] = {"bri": 1.0, "ct": 0.0}
focus_wohnzimmer["Sofalampe Rechts"] = {"bri": 1.0, "ct": 0.0}
focus_wohnzimmer["Sofalampe Links"] = {"bri": 1.0, "ct": 0.0}
focus_wohnzimmer["Filament"] = {"bri": 1.0}
focus_wohnzimmer["Deckenlampe"] = {"bri": 1.0}
focus_wohnzimmer["Lichterkette"] = {"on": True}

focus_schlafzimmer = dict()
focus_schlafzimmer["Nachttischlampe"] = {"bri": 1.0, "ct": 0.0}
focus_schlafzimmer["Wickeltischlampe"] = {"bri": 1.0, "ct": 0.0}
focus_schlafzimmer["Schlafzimmer " + HANGELAMPE] = {"bri": 1.0}

focus = {**focus_wohnzimmer, **focus_schlafzimmer}
