import re
import cv2
import numpy as np

with open("scratch/test_rwing_fix.svg") as f:
    text = f.read()

m = re.search(r'<clipPath id="bodyClip">\s*<path d="([^"]+)"', text)
d = m.group(1)

# Parse points from SVG path
tokens = d.replace("M", " ").replace("L", " ").replace("Z", " ").split()
pts = []
for i in range(0, len(tokens), 2):
    pts.append([float(tokens[i]), float(tokens[i+1])])

pts = np.array(pts, dtype=np.int32)
dist = cv2.pointPolygonTest(pts, (255, 465), False)
print(f"Point (255, 465) inside bodyClip polygon: {dist >= 0}")
print(f"Point (255, 450) inside bodyClip polygon: {dist >= 0}")
