from _phue import min_bri


wohnzimmer_lights = [["Hängelampe", ["bri"]],
                     ["Hue Go", ["bri", "ct"]],
                     ["Stehlampe", ["bri", "ct"]],
                     ["Fensterlampe", ["bri", "ct"]],
                     ["LED Streifen", ["bri", "ct"]],
                     ["Ananas", ["bri", "ct"]],
                     ["Lichterkette", ["on"]]]

schlafzimmer_lights = [["Schlafzimmer Hängelampe", ["bri"]],
                       ["Nachttischlampe", ["bri", "ct"]],
                       ["Wickeltischlampe", ["bri", "ct"]]]

all_lights = [*wohnzimmer_lights,
              *schlafzimmer_lights]


off_wohnzimmer = dict()
off_wohnzimmer["Stehlampe"] = {"bri": 0.0, "ct": 1.0}
off_wohnzimmer["Hue Go"] = {"bri": 0.0, "ct": 1.0}
off_wohnzimmer["Fensterlampe"] = {"bri": 0.0, "ct": 1.0}
off_wohnzimmer["LED Streifen"] = {"bri": 0.0, "ct": 1.0}
off_wohnzimmer["Ananas"] = {"bri": 0.0, "ct": 1.0}
off_wohnzimmer["Lichterkette"] = {"on": False}
off_wohnzimmer["Hängelampe"] = {"bri": 0.0}

off_schlafzimmer = dict()
off_schlafzimmer["Nachttischlampe"] = {"bri": 0.0, "ct": 1.0}
off_schlafzimmer["Wickeltischlampe"] = {"bri": 0.0, "ct": 1.0}
off_schlafzimmer["Schlafzimmer Hängelampe"] = {"bri": 0.0}

off = {**off_wohnzimmer, **off_schlafzimmer}


min_wohnzimmer = dict()
min_wohnzimmer["Stehlampe"] = {"bri": min_bri(), "ct": 1.0}
min_wohnzimmer["Hue Go"] = {"bri": min_bri(), "ct": 1.0}
min_wohnzimmer["Fensterlampe"] = {"bri": min_bri(), "ct": 1.0}
min_wohnzimmer["LED Streifen"] = {"bri": min_bri(), "ct": 1.0}
min_wohnzimmer["Ananas"] = {"bri": min_bri(), "ct": 1.0}
min_wohnzimmer["Lichterkette"] = {"on": False}
min_wohnzimmer["Hängelampe"] = {"bri": 0.0}

min_schlafzimmer = dict()
min_schlafzimmer["Nachttischlampe"] = {"bri": min_bri(), "ct": 1.0}
min_schlafzimmer["Wickeltischlampe"] = {"bri": min_bri(), "ct": 1.0}
min_schlafzimmer["Schlafzimmer Hängelampe"] = {"bri": 0.0}

min = {**min_wohnzimmer, **min_schlafzimmer}


nachtlicht_schlafzimmer = dict()
nachtlicht_schlafzimmer["Nachttischlampe"] = {"bri": 0.0, "ct": 1.0}
nachtlicht_schlafzimmer["Wickeltischlampe"] = {"bri": min_bri(), "ct": 1.0}
nachtlicht_schlafzimmer["Schlafzimmer Hängelampe"] = {"bri": 0.0}


dunkel_wohnzimmer = dict()
dunkel_wohnzimmer["Stehlampe"] = {"bri": .1, "ct": 1.0}
dunkel_wohnzimmer["Hue Go"] = {"bri": .1, "ct": 1.0}
dunkel_wohnzimmer["Fensterlampe"] = {"bri": .1, "ct": 1.0}
dunkel_wohnzimmer["LED Streifen"] = {"bri": .1, "ct": 1.0}
dunkel_wohnzimmer["Ananas"] = {"bri": .1, "ct": 1.0}
dunkel_wohnzimmer["Lichterkette"] = {"on": False}
dunkel_wohnzimmer["Hängelampe"] = {"bri": 0.0}

dunkel_schlafzimmer = dict()
dunkel_schlafzimmer["Nachttischlampe"] = {"bri": .1, "ct": 1.0}
dunkel_schlafzimmer["Wickeltischlampe"] = {"bri": .1, "ct": 1.0}
dunkel_schlafzimmer["Schlafzimmer Hängelampe"] = {"bri": 0.0}

dunkel = {**dunkel_wohnzimmer, **dunkel_schlafzimmer}


lesen_wohnzimmer = dict()
lesen_wohnzimmer["Stehlampe"] = {"bri": .1, "ct": 1.0}
lesen_wohnzimmer["Hue Go"] = {"bri": .1, "ct": 1.0}
lesen_wohnzimmer["Fensterlampe"] = {"bri": .5, "ct": 1.0}
lesen_wohnzimmer["LED Streifen"] = {"bri": .1, "ct": 1.0}
lesen_wohnzimmer["Ananas"] = {"bri": .1, "ct": 1.0}
lesen_wohnzimmer["Lichterkette"] = {"on": False}
lesen_wohnzimmer["Hängelampe"] = {"bri": 0.0}

lesen_schlafzimmer = dict()
lesen_schlafzimmer["Nachttischlampe"] = {"bri": .25, "ct": 1.0}
lesen_schlafzimmer["Wickeltischlampe"] = {"bri": min_bri(), "ct": 1.0}
lesen_schlafzimmer["Schlafzimmer Hängelampe"] = {"bri": 0.0}

lesen = {**lesen_wohnzimmer, **lesen_schlafzimmer}


gemutlich_wohnzimmer = dict()
gemutlich_wohnzimmer["Stehlampe"] = {"bri": .4, "ct": 1.0}
gemutlich_wohnzimmer["Hue Go"] = {"bri": .4, "ct": 1.0}
gemutlich_wohnzimmer["Fensterlampe"] = {"bri": .5, "ct": 1.0}
gemutlich_wohnzimmer["LED Streifen"] = {"bri": .4, "ct": 1.0}
gemutlich_wohnzimmer["Ananas"] = {"bri": .4, "ct": 1.0}
gemutlich_wohnzimmer["Lichterkette"] = {"on": True}
gemutlich_wohnzimmer["Hängelampe"] = {"bri": 0.0}

gemutlich_schlafzimmer = dict()
gemutlich_schlafzimmer["Nachttischlampe"] = {"bri": .4, "ct": 1.0}
gemutlich_schlafzimmer["Wickeltischlampe"] = {"bri": .4, "ct": 1.0}
gemutlich_schlafzimmer["Schlafzimmer Hängelampe"] = {"bri": 0.0}

gemutlich = {**gemutlich_wohnzimmer, **gemutlich_schlafzimmer}


warm_wohnzimmer = dict()
warm_wohnzimmer["Stehlampe"] = {"bri": .75, "ct": 1.0}
warm_wohnzimmer["Hue Go"] = {"bri": .75, "ct": 1.0}
warm_wohnzimmer["Fensterlampe"] = {"bri": .75, "ct": 1.0}
warm_wohnzimmer["LED Streifen"] = {"bri": .75, "ct": 1.0}
warm_wohnzimmer["Ananas"] = {"bri": .75, "ct": 1.0}
warm_wohnzimmer["Lichterkette"] = {"on": True}
warm_wohnzimmer["Hängelampe"] = {"bri": 0.0}

warm_schlafzimmer = dict()
warm_schlafzimmer["Nachttischlampe"] = {"bri": .75, "ct": 1.0}
warm_schlafzimmer["Wickeltischlampe"] = {"bri": .75, "ct": 1.0}
warm_schlafzimmer["Schlafzimmer Hängelampe"] = {"bri": 0.0}

warm = {**warm_wohnzimmer, **warm_schlafzimmer}


max_wohnzimmer = dict()
max_wohnzimmer["Stehlampe"] = {"bri": 1.0, "ct": 1.0}
max_wohnzimmer["Hue Go"] = {"bri": 1.0, "ct": 1.0}
max_wohnzimmer["Fensterlampe"] = {"bri": 1.0, "ct": 1.0}
max_wohnzimmer["LED Streifen"] = {"bri": 1.0, "ct": 1.0}
max_wohnzimmer["Ananas"] = {"bri": 1.0, "ct": 1.0}
max_wohnzimmer["Lichterkette"] = {"on": True}
max_wohnzimmer["Hängelampe"] = {"bri": 0.0}

max_schlafzimmer = dict()
max_schlafzimmer["Nachttischlampe"] = {"bri": 1.0, "ct": 1.0}
max_schlafzimmer["Wickeltischlampe"] = {"bri": 1.0, "ct": 1.0}
max_schlafzimmer["Schlafzimmer Hängelampe"] = {"bri": .3}

max = {**max_wohnzimmer, **max_schlafzimmer}


halbwarm_wohnzimmer = dict()
halbwarm_wohnzimmer["Stehlampe"] = {"bri": 1.0, "ct": .6}
halbwarm_wohnzimmer["Hue Go"] = {"bri": 1.0, "ct": .6}
halbwarm_wohnzimmer["Fensterlampe"] = {"bri": 1.0, "ct": .6}
halbwarm_wohnzimmer["LED Streifen"] = {"bri": 1.0, "ct": .6}
halbwarm_wohnzimmer["Ananas"] = {"bri": 1.0, "ct": .6}
halbwarm_wohnzimmer["Lichterkette"] = {"on": True}
halbwarm_wohnzimmer["Hängelampe"] = {"bri": 0.0}

halbwarm_schlafzimmer = dict()
halbwarm_schlafzimmer["Nachttischlampe"] = {"bri": 1.0, "ct": 0.6}
halbwarm_schlafzimmer["Wickeltischlampe"] = {"bri": 1.0, "ct": 0.6}
halbwarm_schlafzimmer["Schlafzimmer Hängelampe"] = {"bri": 1.0}

halbwarm = {**halbwarm_wohnzimmer, **halbwarm_schlafzimmer}


hell_wohnzimmer = dict()
hell_wohnzimmer["Stehlampe"] = {"bri": 1.0, "ct": .35}
hell_wohnzimmer["Hue Go"] = {"bri": 1.0, "ct": .35}
hell_wohnzimmer["Fensterlampe"] = {"bri": 1.0, "ct": .35}
hell_wohnzimmer["LED Streifen"] = {"bri": 1.0, "ct": .35}
hell_wohnzimmer["Ananas"] = {"bri": 1.0, "ct": .35}
hell_wohnzimmer["Lichterkette"] = {"on": True}
hell_wohnzimmer["Hängelampe"] = {"bri": 0.0}

hell_schlafzimmer = dict()
hell_schlafzimmer["Nachttischlampe"] = {"bri": 1.0, "ct": .35}
hell_schlafzimmer["Wickeltischlampe"] = {"bri": 1.0, "ct": .35}
hell_schlafzimmer["Schlafzimmer Hängelampe"] = {"bri": 1.0}

hell = {**hell_wohnzimmer, **hell_schlafzimmer}


focus_wohnzimmer = dict()
focus_wohnzimmer["Stehlampe"] = {"bri": 1.0, "ct": 0.0}
focus_wohnzimmer["Hue Go"] = {"bri": 1.0, "ct": 0.0}
focus_wohnzimmer["Fensterlampe"] = {"bri": 1.0, "ct": 0.0}
focus_wohnzimmer["LED Streifen"] = {"bri": 1.0, "ct": 0.0}
focus_wohnzimmer["Ananas"] = {"bri": 1.0, "ct": 0.0}
focus_wohnzimmer["Lichterkette"] = {"on": True}
focus_wohnzimmer["Hängelampe"] = {"bri": 0.0}

focus_schlafzimmer = dict()
focus_schlafzimmer["Nachttischlampe"] = {"bri": 1.0, "ct": 0.0}
focus_schlafzimmer["Wickeltischlampe"] = {"bri": 1.0, "ct": 0.0}
focus_schlafzimmer["Schlafzimmer Hängelampe"] = {"bri": 1.0}

focus = {**focus_wohnzimmer, **focus_schlafzimmer}