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

# 1. Render body with exact radial gradient
body_mask, _ = render_rive_polygon(body_shape['subpaths'][0]['points'], (body_shape['x'], body_shape['y']))
for y, x in zip(*np.where(body_mask > 0)):
    d = math.hypot(x - 512, y - 340) / 424.0
    d = min(1.0, max(0.0, d))
    c = (1-d) * np.array([243, 249, 252]) + d * np.array([178, 208, 229])
    canvas[y, x] = c.astype(np.uint8)

# 2. Render wing with exact 56px width
points_l = [
    { "x": 0.0,  "y": -150.0, "cubic": { "rotation": 130.0, "outDistance": 36.0, "inRotation": -65.0, "inDistance": 36.0 } },
    { "x": -36.0, "y": -90.0,  "cubic": { "rotation": 105.0, "outDistance": 42.0, "inRotation": -75.0, "inDistance": 42.0 } },
    { "x": -59.0, "y": 10.0,   "cubic": { "rotation": 85.0,  "outDistance": 42.0, "inRotation": -95.0, "inDistance": 42.0 } },
    { "x": -44.0, "y": 90.0,   "cubic": { "rotation": 50.0,  "outDistance": 38.0, "inRotation": -130.0, "inDistance": 38.0 } },
    { "x": 16.0,  "y": 146.0,  "cubic": { "rotation": -30.0, "outDistance": 22.0, "inRotation": 150.0, "inDistance": 22.0 } },
    { "x": 12.0,  "y": 90.0,   "cubic": { "rotation": -95.0, "outDistance": 36.0, "inRotation": 85.0,  "inDistance": 36.0 } },
    { "x": 4.0,   "y": 10.0,   "cubic": { "rotation": -95.0, "outDistance": 40.0, "inRotation": 85.0,  "inDistance": 40.0 } },
    { "x": 2.0,   "y": -70.0,  "cubic": { "rotation": -95.0, "outDistance": 38.0, "inRotation": 85.0,  "inDistance": 38.0 } }
]

origin_l = (224, 590)
wing_mask, _ = render_rive_polygon(points_l, origin_l)

p_start = np.array([165.0, 590.0])
p_end = np.array([228.0, 590.0])
v = p_end - p_start
v_len2 = np.dot(v, v)

stops = [
    (0.00, np.array([242, 247, 250], dtype=np.float32)), # #FAF7F2
    (0.35, np.array([219, 234, 245], dtype=np.float32)), # #F5EADB
    (0.70, np.array([194, 217, 234], dtype=np.float32)), # #EAD9C2
    (0.88, np.array([160, 188, 210], dtype=np.float32)), # #D2BCA0 (crease)
    (1.00, np.array([199, 224, 239], dtype=np.float32))  # #EFE0C7 (body)
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
ref = cv2.imread('scratch/master_wing_true.png')

# Measure NCC and MAE
ref_gray = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
res_gray = cv2.cvtColor(crop_res, cv2.COLOR_BGR2GRAY)
mask = ref_gray < 248

ncc = np.corrcoef(ref_gray[mask].astype(float), res_gray[mask].astype(float))[0, 1]
diff = np.abs(ref.astype(float) - crop_res.astype(float))
mean_diff = diff[mask].mean()

print(f'Calibrated Wing NCC: {ncc*100:.2f}%')
print(f'Calibrated Wing Mean Diff: {mean_diff:.2f} / 255')
print(f'Calibrated Wing Fidelity: {100.0 - mean_diff/255.0*100.0:.2f}%')

# Save side-by-side
comp = np.zeros((340, 290, 3), dtype=np.uint8)
comp[:, :140] = ref
comp[:, 140:150] = [200, 200, 200]
comp[:, 150:] = crop_res
cv2.imwrite('/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68/calibrated_wing_comparison.png', comp)
