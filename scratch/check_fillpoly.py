import re
import cv2
import numpy as np

with open("scratch/test_rwing_fix.svg") as f:
    text = f.read()

m = re.search(r'<clipPath id="bodyClip">\s*<path d="([^"]+)"', text)
d = m.group(1)

tokens = d.replace("M", " ").replace("L", " ").replace("Z", " ").split()
pts = []
for i in range(0, len(tokens), 2):
    pts.append([int(tokens[i]), int(tokens[i+1])])

pts = np.array(pts, dtype=np.int32)

# Create an image and fill poly
img = np.zeros((512, 512), dtype=np.uint8)
cv2.fillPoly(img, [pts], 255)
print("OpenCV fillPoly at (255, 465):", img[465, 255])
print("OpenCV fillPoly at (255, 450):", img[450, 250])
print("OpenCV fillPoly at (255, 300):", img[300, 255])
