import cv2
import numpy as np

# Load panel 4 aligned
p4 = cv2.imread('scratch/panel_4_aligned.png')
# Wing area: x in [740, 1020], y in [150, 720]
crop = p4[150:720, 740:1020]
gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

# Find wing mask: non-white pixels
# Background is white > 248
mask = np.zeros(gray.shape, dtype=np.uint8)
mask[gray < 245] = 255

# Clean up mask
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

# Find largest contour
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
c = max(contours, key=cv2.contourArea)

# Approximate contour with polygon
epsilon = 0.006 * cv2.arcLength(c, True)
approx = cv2.approxPolyDP(c, epsilon, True)

print(f"Approximated wing contour with {len(approx)} vertices.")

# Global points on 1024x1024 canvas
pts_global = []
for p in approx:
    gx = int(p[0][0] + 740)
    gy = int(p[0][1] + 150)
    pts_global.append((gx, gy))

for i, pt in enumerate(pts_global):
    print(f"  pt {i}: ({pt[0]}, {pt[1]})")

# Shoulder attachment point in global coords:
# In idle, wing_r_group is at (806, 498).
# The waving wing pivots around shoulder joint: around (780, 560)
