#!/usr/bin/env python3
"""
Test extraction and segmentation of the 4 turnaround views
from mascots/aituko/aituko_master_turnaround.jpeg.
"""

import os
import cv2
import numpy as np

IMG_PATH = "mascots/aituko/aituko_master_turnaround.jpeg"
img = cv2.imread(IMG_PATH)
if img is None:
    raise FileNotFoundError(f"Cannot load {IMG_PATH}")

h, w, _ = img.shape
b, g, r = cv2.split(img)

# Calibrated chroma key background segmentation
bg_mask = (g > 120) & (r < 55) & (b < 55)
char_mask = (~bg_mask).astype(np.uint8) * 255

# Fill enclosed porcelain holes
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
char_mask_closed = cv2.morphologyEx(char_mask, cv2.MORPH_CLOSE, kernel)

# Crop the 4 figures with clean boundaries
# BBoxes in 1376x768:
# View 1: X in [70, 350]
# View 2: X in [380, 700]
# View 3: X in [700, 980]
# View 4: X in [1000, 1320]
boxes = [
    ("front_0deg", 60, 360),
    ("three_quarter_45deg", 380, 710),
    ("profile_90deg", 710, 990),
    ("back_180deg", 1000, 1320)
]

os.makedirs("scratch/turnaround_extraction", exist_ok=True)

for name, x1, x2 in boxes:
    crop_mask = char_mask_closed[:, x1:x2]
    crop_bgr = img[:, x1:x2]
    
    cnts, _ = cv2.findContours(crop_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    valid_cnts = [c for c in cnts if cv2.contourArea(c) > 2000]
    print(f"[{name}] found {len(valid_cnts)} components:")
    
    for i, c in enumerate(valid_cnts):
        cx, cy, cw, ch = cv2.boundingRect(c)
        area = cv2.contourArea(c)
        print(f"   Comp {i}: bbox=({cx}, {cy}, {cw}, {ch}), area={area}")
        
    cv2.imwrite(f"scratch/turnaround_extraction/{name}_mask.png", crop_mask)

print("Turnaround segmentation test complete.")
