import cv2
import numpy as np
from PIL import Image

ref = np.array(Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA"))
mask = (ref[:, :, 3] > 20).astype(np.uint8)

# Find contours of ref mask
contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
print(f"Number of contours: {len(contours)}")
c = contours[0] # The main body contour
pts = c[:, 0, :]
print(f"Total contour points: {len(pts)}")

# Filter points with Y >= 430
bottom_pts = [(x, y) for x, y in pts if y >= 430]
print(f"Bottom points (Y >= 430): {len(bottom_pts)}")

# Let's sort or trace points along the contour
# Where does contour enter Y >= 430 from left, and exit to right?
indices = [i for i, (x, y) in enumerate(pts) if y >= 430]
# Print the sequence of contour points around the bottom
# Let's find index with min x in bottom
start_idx = indices[0]
for idx in range(start_idx - 5, start_idx + len(indices) + 5):
    i = idx % len(pts)
    x, y = pts[i]
    if y >= 425:
        print(f"i={i:4d}: ({x:3d}, {y:3d})")
