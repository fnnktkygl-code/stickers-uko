import cv2
import numpy as np
import json
import math
import sys
sys.path.append('.')
from scratch.fit_rive_wing import render_rive_polygon

with open('scratch/owluko_waving.scene.json') as f:
    scene = json.load(f)
shapes = {s['id']: s for s in scene['shapes']}
body_shape = shapes['owluko_wave_body_silhouette']

h, w = 1024, 1024
canvas = np.full((h, w, 3), 255, dtype=np.uint8)

# 1. Render body
body_mask, _ = render_rive_polygon(body_shape['subpaths'][0]['points'], (body_shape['x'], body_shape['y']))
# Use the exact body gradient
for y, x in zip(*np.where(body_mask > 0)):
    # Distance to radial gradient center (512, 340)
    d = math.hypot(x - 512, y - 340) / 424.0
    d = min(1.0, max(0.0, d))
    # Interpolate #FCF9F3 -> #F7EEDB -> #EFE0C7 -> #E5D0B2
    c = (1-d) * np.array([243, 249, 252]) + d * np.array([178, 208, 229])
    canvas[y, x] = c.astype(np.uint8)

# 2. Render wing
points_l = [
    { "x": 15.0, "y": -150.0, "cubic": { "rotation": 135.0, "outDistance": 40.0, "inRotation": -55.0, "inDistance": 40.0 } },
    { "x": -36.0, "y": -90.0,  "cubic": { "rotation": 105.0, "outDistance": 45.0, "inRotation": -75.0, "inDistance": 45.0 } },
    { "x": -59.0, "y": 10.0,   "cubic": { "rotation": 85.0,  "outDistance": 42.0, "inRotation": -95.0, "inDistance": 42.0 } },
    { "x": -44.0, "y": 90.0,   "cubic": { "rotation": 50.0,  "outDistance": 38.0, "inRotation": -130.0, "inDistance": 38.0 } },
    { "x": 58.0,  "y": 148.0,  "cubic": { "rotation": -30.0, "outDistance": 28.0, "inRotation": 150.0, "inDistance": 28.0 } },
    { "x": 50.0,  "y": 10.0,   "cubic": { "rotation": -95.0, "outDistance": 75.0, "inRotation": 85.0,  "inDistance": 75.0 } }
]
origin_l = (224, 590)
wing_mask, _ = render_rive_polygon(points_l, origin_l)

p_start = np.array([165.0, 590.0])
p_end = np.array([274.0, 590.0])
v = p_end - p_start
v_len2 = np.dot(v, v)

stops = [
    (0.00, np.array([242, 247, 250], dtype=np.float32)), # #FAF7F2
    (0.35, np.array([219, 234, 245], dtype=np.float32)), # #F5EADB
    (0.65, np.array([194, 217, 234], dtype=np.float32)), # #EAD9C2
    (0.85, np.array([159, 187, 208], dtype=np.float32)), # #D0BB9F (crease)
    (1.00, np.array([199, 224, 239], dtype=np.float32))  # #EFE0C7 (blends to body)
]

ys, xs = np.where(wing_mask > 0)
for y, x in zip(ys, xs):
    pt = np.array([float(x), float(y)])
    proj = np.dot(pt - p_start, v) / v_len2
    proj = max(0.0, min(1.0, proj))
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]
        t1, c1 = stops[i+1]
        if t0 <= proj <= t1:
            alpha = (proj - t0) / (t1 - t0)
            color = (1 - alpha) * c0 + alpha * c1
            canvas[y, x] = color.astype(np.uint8)
            break

crop_res = canvas[420:760, 150:290]
cv2.imwrite('scratch/final_flawless_wing_render.png', crop_res)
print("Saved scratch/final_flawless_wing_render.png")
