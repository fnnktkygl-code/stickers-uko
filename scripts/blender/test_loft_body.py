import cv2
import numpy as np
import math

front = cv2.imread('mascots/owluko/owluko_turnaround_view_1_front.png', cv2.IMREAD_UNCHANGED)
profile = cv2.imread('mascots/owluko/owluko_turnaround_view_2_profile_right.png', cv2.IMREAD_UNCHANGED)

alpha_f = front[:, :, 3]
alpha_p = profile[:, :, 3]

# Body vertical range: Y=40 (top of head) to Y=450 (base of pelvis, above feet)
# Image coords: Y goes from 40 (top) down to 450 (bottom).
# In 3D: Z goes from Z_max (top) down to Z_min (bottom).
# Let canvas center be (256, 256).
# Scale factor: 1 unit = 256 pixels.

y_samples = np.linspace(42, 450, 60)
rings = []

for y in y_samples:
    y_int = int(round(y))
    xf = np.where(alpha_f[y_int, :] > 50)[0]
    xp = np.where(alpha_p[y_int, :] > 50)[0]
    if len(xf) == 0 or len(xp) == 0:
        continue
    
    # In front view: X is Mascot X, Y is Mascot Z (inverted)
    rx = (xf.max() - xf.min()) / 2.0
    cx = (xf.max() + xf.min()) / 2.0 - 256.0
    
    # In profile view (viewing from right, mascot faces left (-X in profile view, so mascot forward is -Y)):
    # Let's inspect which way profile faces:
    ry = (xp.max() - xp.min()) / 2.0
    cy = (xp.max() + xp.min()) / 2.0 - 256.0
    
    # 3D coordinates:
    # X: (pixel_x - 256) / 200.0
    # Y: Mascot depth (forward is -Y)
    # Z: (450 - y) / 200.0
    rings.append({
        'y_img': y_int,
        'z_3d': (450.0 - y) / 200.0,
        'rx': rx / 200.0,
        'cx': cx / 200.0,
        'ry': ry / 200.0,
        'cy': cy / 200.0,
    })

print(f"Generated {len(rings)} smooth cross-sectional rings.")
print("Top ring:", rings[0])
print("Max width ring:", max(rings, key=lambda r: r['rx']))
print("Bottom ring:", rings[-1])
