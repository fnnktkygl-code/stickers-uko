import json
import math

with open('scratch/optimized_8pts_wing.json') as f:
    opt = json.load(f)

pts_l = opt['points']

# Create mirrored points for right wing:
pts_r = []
for p in pts_l:
    c = p['cubic']
    pts_r.append({
        'x': -p['x'],
        'y': p['y'],
        'cubic': {
            'rotation': (180.0 - c['rotation']) % 360.0,
            'outDistance': c['outDistance'],
            'inRotation': (180.0 - c['inRotation']) % 360.0,
            'inDistance': c['inDistance']
        }
    })

# Wing Left Main shape
wing_l_main = {
    "id": "owluko_wave_wing_left_main",
    "type": "polygon",
    "x": 224,
    "y": 590,
    "subpaths": [
        {
            "closed": True,
            "points": pts_l
        }
    ],
    "fill": {
        "gradient": {
            "type": "linear",
            "start": { "x": -59.0, "y": -10.0 },
            "end": { "x": 10.0, "y": 25.0 },
            "stops": [
                { "color": "#F8F6EA", "position": 0.0 },
                { "color": "#F5EADB", "position": 0.35 },
                { "color": "#EAD9C2", "position": 0.70 },
                { "color": "#DCC7AC", "position": 1.0 }
            ]
        }
    }
}

# Wing Right Main shape
wing_r_main = {
    "id": "owluko_wave_wing_right_main",
    "type": "polygon",
    "x": 800,
    "y": 590,
    "subpaths": [
        {
            "closed": True,
            "points": pts_r
        }
    ],
    "fill": {
        "gradient": {
            "type": "linear",
            "start": { "x": 59.0, "y": -10.0 },
            "end": { "x": -10.0, "y": 25.0 },
            "stops": [
                { "color": "#F8F6EA", "position": 0.0 },
                { "color": "#F5EADB", "position": 0.35 },
                { "color": "#EAD9C2", "position": 0.70 },
                { "color": "#DCC7AC", "position": 1.0 }
            ]
        }
    }
}

# Soft under-crease contact shadow (strictly under crease between y=550 and y=740, NEVER at shoulder!)
# 4 points along the crease with a soft +6px inward offset
shadow_pts_l = [
    { "x": -4.0, "y": -40.0, "cubic": { "rotation": 90.0, "outDistance": 30.0, "inRotation": -90.0, "inDistance": 10.0 } },
    { "x": 16.0, "y": 90.0, "cubic": { "rotation": 45.0, "outDistance": 25.0, "inRotation": -135.0, "inDistance": 25.0 } },
    { "x": 55.0, "y": 150.0, "cubic": { "rotation": -45.0, "outDistance": 15.0, "inRotation": 135.0, "inDistance": 15.0 } },
    { "x": 30.0, "y": 140.0, "cubic": { "rotation": -135.0, "outDistance": 25.0, "inRotation": 45.0, "inDistance": 25.0 } }
]
shadow_pts_r = []
for p in shadow_pts_l:
    c = p['cubic']
    shadow_pts_r.append({
        'x': -p['x'],
        'y': p['y'],
        'cubic': {
            'rotation': (180.0 - c['rotation']) % 360.0,
            'outDistance': c['outDistance'],
            'inRotation': (180.0 - c['inRotation']) % 360.0,
            'inDistance': c['inDistance']
        }
    })

wing_l_shadow = {
    "id": "owluko_wave_wing_left_shadow",
    "type": "polygon",
    "x": 224,
    "y": 590,
    "subpaths": [
        {
            "closed": True,
            "points": shadow_pts_l
        }
    ],
    "opacity": 0.12,
    "fill": {
        "color": "#B89C7B"
    }
}

wing_r_shadow = {
    "id": "owluko_wave_wing_right_shadow",
    "type": "polygon",
    "x": 800,
    "y": 590,
    "subpaths": [
        {
            "closed": True,
            "points": shadow_pts_r
        }
    ],
    "opacity": 0.12,
    "fill": {
        "color": "#B89C7B"
    }
}

# Update scratch/owluko_waving.scene.json
scene_path = 'scratch/owluko_waving.scene.json'
with open(scene_path, 'r') as f:
    scene = json.load(f)

new_shapes = []
for s in scene['shapes']:
    if s['id'] == 'owluko_wave_wing_left_main':
        new_shapes.append(wing_l_main)
    elif s['id'] == 'owluko_wave_wing_left_shadow':
        new_shapes.append(wing_l_shadow)
    elif s['id'] == 'owluko_wave_wing_right_main':
        new_shapes.append(wing_r_main)
    elif s['id'] == 'owluko_wave_wing_right_shadow':
        new_shapes.append(wing_r_shadow)
    else:
        new_shapes.append(s)

scene['shapes'] = new_shapes
with open(scene_path, 'w') as f:
    json.dump(scene, f, indent=2)

print("Updated scratch/owluko_waving.scene.json with flawless organic wing shapes!")
