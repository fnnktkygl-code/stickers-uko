#!/usr/bin/env python3
"""
Test vector extraction for 3/4, Profile, and Back views.
"""

import os
import cv2
import numpy as np

for view_name in ["three_quarter", "profile", "back"]:
    rgba = cv2.imread(f"scratch/turnaround_views/{view_name}_clean.png", cv2.IMREAD_UNCHANGED)
    alpha = rgba[:, :, 3]
    bgr = rgba[:, :, :3]
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    
    # 1. Total character contour
    char_mask = (alpha > 100).astype(np.uint8) * 255
    cnts, _ = cv2.findContours(char_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    main_cnts = [c for c in cnts if cv2.contourArea(c) > 500]
    print(f"[{view_name}] found {len(main_cnts)} total silhouette contours")
    
    # 2. Visor (if not back view)
    if view_name != "back":
        # Visor is where gray < 130 and inside upper half
        h, w = char_mask.shape
        visor_cand = (char_mask > 0) & (gray < 130)
        visor_cand[int(h * 0.45):, :] = False  # only head region
        v_mask = visor_cand.astype(np.uint8) * 255
        v_mask = cv2.morphologyEx(v_mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
        vcnts, _ = cv2.findContours(v_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        vcnts = [c for c in vcnts if cv2.contourArea(c) > 1000]
        print(f"  Visor contours: {len(vcnts)}")
        if vcnts:
            vx, vy, vw, vh = cv2.boundingRect(max(vcnts, key=cv2.contourArea))
            print(f"  Visor bbox: ({vx}, {vy}, {vw}, {vh})")
            
        # Eyes: inside visor, cyan pixels (b > 160 and g > 160 and r < 120)
        b, g, r = cv2.split(bgr)
        eyes_cand = (v_mask > 0) & (b > 160) & (g > 160) & (r < 120)
        e_mask = eyes_cand.astype(np.uint8) * 255
        e_mask = cv2.morphologyEx(e_mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
        ecnts, _ = cv2.findContours(e_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        ecnts = [c for c in ecnts if cv2.contourArea(c) > 100]
        print(f"  Eyes contours: {len(ecnts)}")
        for i, ec in enumerate(ecnts):
            ex, ey, ew, eh = cv2.boundingRect(ec)
            print(f"    Eye {i}: bbox=({ex}, {ey}, {ew}, {eh})")
