import cv2
import numpy as np
import json
import math
import sys
sys.path.append('.')
from scratch.fit_rive_wing import render_rive_polygon

# Load scene
with open('scratch/owluko_waving.scene.json') as f:
    scene = json.load(f)
shapes = {s['id']: s for s in scene['shapes']}
body_shape = shapes['owluko_wave_body_silhouette']

# Render body
body_mask, _ = render_rive_polygon(body_shape['subpaths'][0]['points'], (body_shape['x'], body_shape['y']))

# 6 smooth cubic bezier points for the left wing:
# Origin at (224, 590)
# P0: Top Shoulder    (8, -150)    -> global (232, 440)
# P1: Upper Outer     (-36, -90)   -> global (188, 500)
# P2: Mid Outer Apex  (-59, 10)    -> global (165, 600)  [Apex reaches 165!]
# P3: Lower Outer     (-44, 90)    -> global (180, 680)
# P4: Bottom Tip      (31, 155)    -> global (255, 745)
# P5: Mid Inner Crease(22, 10)     -> global (246, 600)  [Inside body, 80px before belly!]

# Let's define the smooth handles:
points_l = [
    {
        "x": 8.0,
        "y": -150.0,
        "cubic": {
            "rotation": 130.0,
            "outDistance": 38.0,
            "inRotation": -60.0,
            "inDistance": 38.0
        }
    },
    {
        "x": -36.0,
        "y": -90.0,
        "cubic": {
            "rotation": 105.0,
            "outDistance": 45.0,
            "inRotation": -75.0,
            "inDistance": 45.0
        }
    },
    {
        "x": -59.0,
        "y": 10.0,
        "cubic": {
            "rotation": 85.0,
            "outDistance": 42.0,
            "inRotation": -95.0,
            "inDistance": 42.0
        }
    },
    {
        "x": -44.0,
        "y": 90.0,
        "cubic": {
            "rotation": 50.0,
            "outDistance": 38.0,
            "inRotation": -130.0,
            "inDistance": 38.0
        }
    },
    {
        "x": 31.0,
        "y": 155.0,
        "cubic": {
            "rotation": -35.0,
            "outDistance": 30.0,
            "inRotation": 145.0,
            "inDistance": 30.0
        }
    },
    {
        "x": 22.0,
        "y": 10.0,
        "cubic": {
            "rotation": -95.0,
            "outDistance": 75.0,
            "inRotation": 85.0,
            "inDistance": 75.0
        }
    }
]

origin_l = (224, 590)
wing_mask, _ = render_rive_polygon(points_l, origin_l)

# Check gap: pixels that are adjacent to wing but neither wing nor body
# Combined mask:
combined = np.logical_or(body_mask > 0, wing_mask > 0)

# Check if there is any white gap between wing and body in the wing region y in [440, 750], x in [165, 300]
sub_combined = combined[440:750, 165:300]
print("Combined mask empty pixels in wing bounding box:", np.sum(~sub_combined))

# Visual composite: Body gray + Wing orange
comp = np.zeros((1024, 1024, 3), dtype=np.uint8)
comp[body_mask > 0] = [200, 200, 200]
comp[wing_mask > 0] = [100, 150, 255]
comp[np.logical_and(body_mask > 0, wing_mask > 0)] = [180, 120, 220] # Overlap purple
cv2.imwrite('scratch/capsule_wing_overlap.png', comp[400:800, 140:320])
print("Saved scratch/capsule_wing_overlap.png")
