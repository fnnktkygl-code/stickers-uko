#!/usr/bin/env python3
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

def get_smooth_contour(mask, eps=1.2):
    # Gaussian blur the binary mask slightly, then threshold to get a perfectly smooth continuous edge
    blur = cv2.GaussianBlur(mask, (5, 5), 1.0)
    _, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
    cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not cnts:
        return []
    cnt = max(cnts, key=cv2.contourArea)
    approx = cv2.approxPolyDP(cnt, eps, True)
    return approx.reshape(-1, 2)

for name in ['three_quarter', 'profile', 'back']:
    rgba = cv2.imread(f'scratch/turnaround_views/{name}_clean.png', cv2.IMREAD_UNCHANGED)
    alpha = rgba[:, :, 3]
    gray = cv2.cvtColor(rgba[:, :, :3], cv2.COLOR_BGR2GRAY)
    
    # Head mask: alpha > 80, y < 196
    h_mask = ((alpha > 80) & (np.arange(alpha.shape[0])[:, None] < 196)).astype(np.uint8)*255
    pts = get_smooth_contour(h_mask)
    print(f"{name} smooth head points: {len(pts)}")

