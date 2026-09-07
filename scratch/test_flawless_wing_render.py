import cv2
import numpy as np
import json
import math
import sys
sys.path.append('.')
from scratch.fit_rive_wing import render_rive_polygon

# Load body
with open('scratch/owluko_waving.scene.json') as f:
    scene = json.load(f)
shapes = {s['id']: s for s in scene['shapes']}
body_shape = shapes['owluko_wave_body_silhouette']

h, w = 1024, 1024
canvas = np.full((h, w, 3), 255, dtype=np.uint8)

# 1. Render body with its radial gradient
body_mask, _ = render_rive_polygon(body_shape['subpaths'][0]['points'], (body_shape['x'], body_shape['y']))
# Body color around flank is approx RGB(239, 224, 199) -> BGR(199, 224, 239)
canvas[body_mask > 0] = [199, 224, 239]

# 2. Render wing
points_l = [
    { 'x': 8.0, 'y': -150.0, 'cubic': { 'rotation': 130.0, 'outDistance': 38.0, 'inRotation': -60.0, 'inDistance': 38.0 } },
    { 'x': -36.0, 'y': -90.0, 'cubic': { 'rotation': 105.0, 'outDistance': 45.0, 'inRotation': -75.0, 'inDistance': 45.0 } },
    { 'x': -59.0, 'y': 10.0, 'cubic': { 'rotation': 85.0, 'outDistance': 42.0, 'inRotation': -95.0, 'inDistance': 42.0 } },
    { 'x': -44.0, 'y': 90.0, 'cubic': { 'rotation': 50.0, 'outDistance': 38.0, 'inRotation': -130.0, 'inDistance': 38.0 } },
    { 'x': 45.0, 'y': 148.0, 'cubic': { 'rotation': -35.0, 'outDistance': 25.0, 'inRotation': 145.0, 'inDistance': 25.0 } },
    { 'x': 26.0, 'y': 10.0, 'cubic': { 'rotation': -95.0, 'outDistance': 75.0, 'inRotation': 85.0, 'inDistance': 75.0 } }
]
origin_l = (224, 590)
wing_mask, _ = render_rive_polygon(points_l, origin_l)

# Linear gradient from p_start = (165, 590) to p_end = (250, 590)
p_start = np.array([165.0, 590.0])
p_end = np.array([250.0, 590.0])
v = p_end - p_start
v_len2 = np.dot(v, v)

# Stops:
# 0.0: #FAF7F2 -> RGB(250, 247, 242) -> BGR(242, 247, 250)
# 0.35: #F5EADB -> RGB(245, 234, 219) -> BGR(219, 234, 245)
# 0.70: #EAD9C2 -> RGB(234, 217, 194) -> BGR(194, 217, 234)
# 0.88: #D4C0A4 -> RGB(212, 192, 164) -> BGR(164, 192, 212)
# 1.0: #EFE0C7 -> RGB(239, 224, 199) -> BGR(199, 224, 239)
stops = [
    (0.0, np.array([242, 247, 250], dtype=np.float32)),
    (0.35, np.array([219, 234, 245], dtype=np.float32)),
    (0.70, np.array([194, 217, 234], dtype=np.float32)),
    (0.88, np.array([164, 192, 212], dtype=np.float32)),
    (1.0, np.array([199, 224, 239], dtype=np.float32))
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

cv2.imwrite('scratch/test_flawless_wing_composite.png', canvas[400:800, 140:320])
print("Saved scratch/test_flawless_wing_composite.png")
