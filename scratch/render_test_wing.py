import cv2
import numpy as np
import json
import math

with open('scratch/optimized_8pts_wing.json') as f:
    data = json.load(f)

pts = data['points']
origin = data['origin'] # (224, 590)

# Render with gradient
h, w = 1024, 1024
from scratch.fit_rive_wing import render_rive_polygon
mask, curve_pts = render_rive_polygon(pts, origin, (h, w))

# Create linear gradient fill
grad_img = np.zeros((h, w, 3), dtype=np.float32)
# Gradient axis: from P3 (-59, 10) -> global (165, 600) to P7 (-3, 0) -> global (221, 590)
p_start = np.array([165.0, 560.0])
p_end = np.array([225.0, 620.0])
v = p_end - p_start
v_len2 = np.dot(v, v)

# Colors in BGR:
# 0.0: #F8F6EA -> RGB(248, 246, 234) -> BGR(234, 246, 248)
# 0.4: #F5EADB -> RGB(245, 234, 219) -> BGR(219, 234, 245)
# 0.8: #EAD9C2 -> RGB(234, 217, 194) -> BGR(194, 217, 234)
# 1.0: #DCC7AC -> RGB(220, 199, 172) -> BGR(172, 199, 220)

stops = [
    (0.0, np.array([234, 246, 248], dtype=np.float32)),
    (0.35, np.array([219, 234, 245], dtype=np.float32)),
    (0.70, np.array([194, 217, 234], dtype=np.float32)),
    (1.0, np.array([172, 199, 220], dtype=np.float32))
]

ys, xs = np.where(mask > 0)
for y, x in zip(ys, xs):
    pt = np.array([float(x), float(y)])
    proj = np.dot(pt - p_start, v) / v_len2
    proj = max(0.0, min(1.0, proj))
    # Interpolate color
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]
        t1, c1 = stops[i+1]
        if t0 <= proj <= t1:
            alpha = (proj - t0) / (t1 - t0)
            color = (1 - alpha) * c0 + alpha * c1
            grad_img[y, x] = color
            break

cv2.imwrite('scratch/rendered_left_wing_grad.png', grad_img[420:770, 140:300].astype(np.uint8))
print("Rendered scratch/rendered_left_wing_grad.png")
