#!/usr/bin/env python3
"""
Extracts clean components for all 4 views of AItuko turnaround:
1. Front (0°)
2. Three-Quarter (45°)
3. Profile (90°)
4. Back (180°)
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
char_mask = cv2.morphologyEx(char_mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))

# Regions in 1376x768 for each figure:
views_config = [
    {
        "name": "front",
        "label": "0° - VUE DE FACE",
        "bbox": (80, 140, 260, 490),  # x, y, w, h
    },
    {
        "name": "three_quarter",
        "label": "45° - TROIS-QUARTS",
        "bbox": (420, 140, 270, 490),
    },
    {
        "name": "profile",
        "label": "90° - PROFIL",
        "bbox": (730, 140, 240, 490),
    },
    {
        "name": "back",
        "label": "180° - VUE DE DOS",
        "bbox": (1030, 140, 260, 490),
    }
]

os.makedirs("scratch/turnaround_views", exist_ok=True)

for v in views_config:
    vx, vy, vw, vh = v["bbox"]
    crop_bgr = img[vy:vy+vh, vx:vx+vw]
    crop_mask = char_mask[vy:vy+vh, vx:vx+vw]
    
    # Despill green edge
    cb, cg, cr = cv2.split(crop_bgr)
    spill = (cg > cr) & (cg > cb) & (crop_mask > 0)
    cg_clean = cg.copy()
    cg_clean[spill] = np.maximum(cr[spill], cb[spill])
    
    alpha_clean = cv2.GaussianBlur(crop_mask, (3, 3), 0)
    rgba = cv2.merge([cb, cg_clean, cr, alpha_clean])
    
    out_path = f"scratch/turnaround_views/{v['name']}_clean.png"
    cv2.imwrite(out_path, rgba)
    print(f"Saved {v['name']} view to {out_path} ({vw}x{vh})")

print("Turnaround views extracted successfully.")
