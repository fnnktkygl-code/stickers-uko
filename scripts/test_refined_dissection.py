import cv2
import numpy as np

# Load front turnaround
front_path = "mascots/owluko/owluko_turnaround_view_1_front.png"
img = cv2.imread(front_path, cv2.IMREAD_UNCHANGED)
h, w, c = img.shape

# 1. Clean despill: eliminate any chroma green fringes from the source
b, g, r, a = img[:, :, 0], img[:, :, 1], img[:, :, 2], img[:, :, 3]
g_despill = np.minimum(g, np.maximum(r, b))
img_clean = img.copy()
img_clean[:, :, 1] = g_despill

# 2. Extract Eyeballs and Eyelids
# Left eye center: (193, 160), radius: 36
# Right eye center: (315, 163), radius: 36
leye_ball = np.zeros((h, w, 4), dtype=np.uint8)
reye_ball = np.zeros((h, w, 4), dtype=np.uint8)
leyelid = np.zeros((h, w, 4), dtype=np.uint8)
reyelid = np.zeros((h, w, 4), dtype=np.uint8)

# Mask for eye sockets
leye_circ = np.zeros((h, w), dtype=np.uint8)
reye_circ = np.zeros((h, w), dtype=np.uint8)
cv2.circle(leye_circ, (193, 160), 36, 255, -1)
cv2.circle(reye_circ, (315, 163), 36, 255, -1)

# In img_clean, within eye circles:
# Amber eye vs porcelain eyelid:
# Eyelid has porcelain color: R > 190, G > 180, B > 165
# Amber eye has: R in [120, 220], G in [60, 150], B in [10, 60] or pupil (very dark)
for y in range(h):
    for x in range(w):
        if leye_circ[y, x] and img_clean[y, x, 3] > 20:
            b_val, g_val, r_val = img_clean[y, x, :3]
            is_porcelain = (r_val > 180 and g_val > 165 and b_val > 145)
            if is_porcelain or y < 145:
                leyelid[y, x] = img_clean[y, x]
            else:
                leye_ball[y, x] = img_clean[y, x]
                
        if reye_circ[y, x] and img_clean[y, x, 3] > 20:
            b_val, g_val, r_val = img_clean[y, x, :3]
            is_porcelain = (r_val > 180 and g_val > 165 and b_val > 145)
            if is_porcelain or y < 147:
                reyelid[y, x] = img_clean[y, x]
            else:
                reye_ball[y, x] = img_clean[y, x]

# Now for the eyeball, inpaint the top half so it is a complete 360 glassy orb!
for eball, cx, cy, r_rad in [(leye_ball, 193, 160, 36), (reye_ball, 315, 163, 36)]:
    miss = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(miss, (cx, cy), r_rad, 255, -1)
    miss[eball[:, :, 3] > 20] = 0
    infilled = cv2.inpaint(eball[:, :, :3], miss, 9, cv2.INPAINT_TELEA)
    eball[:, :, :3] = infilled
    # Set circular alpha with soft 1px anti-aliasing
    for y in range(cy - r_rad - 2, cy + r_rad + 3):
        for x in range(cx - r_rad - 2, cx + r_rad + 3):
            dist = np.sqrt((x - cx)**2 + (y - cy)**2)
            if dist <= r_rad - 1:
                eball[y, x, 3] = 255
            elif dist <= r_rad + 1:
                eball[y, x, 3] = int(255 * (r_rad + 1 - dist) / 2.0)
            else:
                eball[y, x, 3] = 0

# And for the eyelid: extend the porcelain hood slightly downwards with a soft porcelain crease
for lid, cx, cy, r_rad in [(leyelid, 193, 160, 36), (reyelid, 315, 163, 36)]:
    # Eyelid top attaches to forehead porcelain
    # Give it a clean rounded bottom curve
    pass

# Check eyeball and eyelid pixels
print("Left eyeball alpha count:", np.sum(leye_ball[:, :, 3] > 0))
print("Right eyeball alpha count:", np.sum(reye_ball[:, :, 3] > 0))
print("Left eyelid alpha count:", np.sum(leyelid[:, :, 3] > 0))
print("Right eyelid alpha count:", np.sum(reyelid[:, :, 3] > 0))
