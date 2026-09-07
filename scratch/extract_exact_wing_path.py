import cv2
import numpy as np

# Load wing_p3_aligned_crop (size: 304 x 600)
# This crop is from x in [720, 1024], y in [150, 750]
c3 = cv2.imread('scratch/wing_p3_aligned_crop.png')
gray = cv2.cvtColor(c3, cv2.COLOR_BGR2GRAY)

# The body is on the left (x < 60)
# The wing is the non-white region in x in [60, 280]
# Background is white > 248
mask = np.zeros(gray.shape, dtype=np.uint8)
mask[(gray < 245) & (np.arange(c3.shape[1])[None, :] > 60)] = 255

# Clean mask
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

# Save mask
cv2.imwrite('scratch/wing_p3_mask.png', mask)

contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
c = max(contours, key=cv2.contourArea)

# Approximate with polygon
epsilon = 0.0035 * cv2.arcLength(c, True)
approx = cv2.approxPolyDP(c, epsilon, True)

print(f"Approximated wing with {len(approx)} points.")

# Convert to 1024 coordinates:
# gx = x + 720, gy = y + 150
pts_1024 = []
for p in approx:
    gx = int(p[0][0] + 720)
    gy = int(p[0][1] + 150)
    pts_1024.append((gx, gy))

for i, pt in enumerate(pts_1024):
    print(f"  ({pt[0]}, {pt[1]}),")

