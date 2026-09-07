import json

points_l = [
    { "x": 15.0, "y": -150.0, "cubic": { "rotation": 135.0, "outDistance": 40.0, "inRotation": -55.0, "inDistance": 40.0 } },
    { "x": -36.0, "y": -90.0,  "cubic": { "rotation": 105.0, "outDistance": 45.0, "inRotation": -75.0, "inDistance": 45.0 } },
    { "x": -59.0, "y": 10.0,   "cubic": { "rotation": 85.0,  "outDistance": 42.0, "inRotation": -95.0, "inDistance": 42.0 } },
    { "x": -44.0, "y": 90.0,   "cubic": { "rotation": 50.0,  "outDistance": 38.0, "inRotation": -130.0, "inDistance": 38.0 } },
    { "x": 58.0,  "y": 148.0,  "cubic": { "rotation": -30.0, "outDistance": 28.0, "inRotation": 150.0, "inDistance": 28.0 } },
    { "x": 50.0,  "y": 10.0,   "cubic": { "rotation": -95.0, "outDistance": 75.0, "inRotation": 85.0,  "inDistance": 75.0 } }
]

points_r = []
for p in points_l:
    c = p['cubic']
    points_r.append({
        'x': -p['x'],
        'y': p['y'],
        'cubic': {
            'rotation': (180.0 - c['rotation']) % 360.0,
            'outDistance': c['outDistance'],
            'inRotation': (180.0 - c['inRotation']) % 360.0,
            'inDistance': c['inDistance']
        }
    })

wing_l_main = {
    "id": "owluko_wave_wing_left_main",
    "type": "polygon",
    "x": 224,
    "y": 590,
    "subpaths": [
        {
            "closed": True,
            "points": points_l
        }
    ],
    "fill": {
        "gradient": {
            "type": "linear",
            "start": { "x": -59.0, "y": 0.0 },
            "end": { "x": 50.0, "y": 0.0 },
            "stops": [
                { "color": "#FAF7F2", "position": 0.0 },
                { "color": "#F5EADB", "position": 0.35 },
                { "color": "#EAD9C2", "position": 0.65 },
                { "color": "#D0BB9F", "position": 0.85 },
                { "color": "#EFE0C7", "position": 1.0 }
            ]
        }
    }
}

wing_r_main = {
    "id": "owluko_wave_wing_right_main",
    "type": "polygon",
    "x": 800,
    "y": 590,
    "subpaths": [
        {
            "closed": True,
            "points": points_r
        }
    ],
    "fill": {
        "gradient": {
            "type": "linear",
            "start": { "x": 59.0, "y": 0.0 },
            "end": { "x": -50.0, "y": 0.0 },
            "stops": [
                { "color": "#FAF7F2", "position": 0.0 },
                { "color": "#F5EADB", "position": 0.35 },
                { "color": "#EAD9C2", "position": 0.65 },
                { "color": "#D0BB9F", "position": 0.85 },
                { "color": "#EFE0C7", "position": 1.0 }
            ]
        }
    }
}

# Update scene json
scene_path = 'scratch/owluko_waving.scene.json'
with open(scene_path, 'r') as f:
    scene = json.load(f)

new_shapes = []
for s in scene['shapes']:
    if s['id'] == 'owluko_wave_wing_left_main':
        new_shapes.append(wing_l_main)
    elif s['id'] == 'owluko_wave_wing_right_main':
        new_shapes.append(wing_r_main)
    elif s['id'] == 'owluko_wave_wing_left_shadow' or s['id'] == 'owluko_wave_wing_right_shadow':
        s['opacity'] = 0 # Built-in crease gradient replaces the artifact-prone separate shadow
        new_shapes.append(s)
    else:
        new_shapes.append(s)

scene['shapes'] = new_shapes
with open(scene_path, 'w') as f:
    json.dump(scene, f, indent=2)

print("Flawless wing shapes applied to scratch/owluko_waving.scene.json successfully!")
