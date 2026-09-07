#!/usr/bin/env python3
"""
Test script to render clean 4-view turnaround with uniform spotless porcelain.
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

def clean_segment_view(name):
    rgba = cv2.imread(f"scratch/turnaround_views/{name}_clean.png", cv2.IMREAD_UNCHANGED)
    h, w, _ = rgba.shape
    alpha = rgba[:, :, 3]
    bgr = rgba[:, :, :3]
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    
    char_mask = (alpha > 80).astype(np.uint8) * 255
    
    # 1. Cyan Eyes
    cyan_mask = (hsv[:, :, 0] >= 75) & (hsv[:, :, 0] <= 115) & (hsv[:, :, 1] >= 60) & (hsv[:, :, 2] >= 75)
    ec, _ = cv2.findContours(cyan_mask.astype(np.uint8)*255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    eyes = sorted([c for c in ec if cv2.contourArea(c) > 15], key=lambda c: cv2.boundingRect(c)[0])
    
    # 2. Visor (if not back)
    visor = []
    if name != "back":
        head_crop = np.zeros_like(char_mask)
        head_crop[:180, :] = char_mask[:180, :]
        v_cand = (head_crop > 0) & (gray < 85)
        v_mask = cv2.morphologyEx(v_cand.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
        vc, _ = cv2.findContours(v_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        visor = [c for c in vc if cv2.contourArea(c) > 500]
        
    # 3. Head (y < 196)
    head_mask = np.zeros_like(char_mask)
    head_mask[:196, :] = char_mask[:196, :]
    # close bottom to make a clean dome
    head_mask = cv2.morphologyEx(head_mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    hc, _ = cv2.findContours(head_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    head = [c for c in hc if cv2.contourArea(c) > 3000]
    
    # 4. Neck socket (subtle dark joint between head and torso, y: 190..204)
    neck_mask = np.zeros_like(char_mask)
    neck_mask[190:206, :] = (char_mask[190:206, :] > 0) & (gray[190:206, :] < 160)
    neck_c, _ = cv2.findContours(neck_mask.astype(np.uint8)*255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    neck = [c for c in neck_c if cv2.contourArea(c) > 50]
    
    # 5. Feet (y > 415)
    feet_mask = np.zeros_like(char_mask)
    feet_mask[415:, :] = char_mask[415:, :]
    fc, _ = cv2.findContours(feet_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    feet = sorted([c for c in fc if cv2.contourArea(c) > 200], key=lambda c: cv2.boundingRect(c)[0])
    
    # 6. Body & Pods (y 196..415)
    body_mask = np.zeros_like(char_mask)
    body_mask[196:415, :] = char_mask[196:415, :]
    
    # In front and back, pods are distinct connected components
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(body_mask)
    torso_cnts = []
    pods_cnts = []
    
    if num_labels > 2:
        # Sort components by width/area
        comps = []
        for i in range(1, num_labels):
            if stats[i, cv2.CC_STAT_AREA] > 300:
                comps.append((stats[i, cv2.CC_STAT_AREA], i))
        comps.sort(reverse=True)
        # Largest is torso
        if comps:
            torso_label = comps[0][1]
            t_mask = (labels == torso_label).astype(np.uint8)*255
            tc, _ = cv2.findContours(t_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            torso_cnts = [c for c in tc if cv2.contourArea(c) > 1000]
            # Remaining are pods
            for _, lab in comps[1:]:
                p_mask = (labels == lab).astype(np.uint8)*255
                pc, _ = cv2.findContours(p_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                pods_cnts.extend([c for c in pc if cv2.contourArea(c) > 300])
    else:
        # In 3/4 or profile where pod overlaps torso
        tc, _ = cv2.findContours(body_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        torso_cnts = [c for c in tc if cv2.contourArea(c) > 1000]
        
    return {
        "name": name,
        "w": w, "h": h,
        "head": head,
        "visor": visor,
        "eyes": eyes,
        "neck": neck,
        "torso": torso_cnts,
        "pods": pods_cnts,
        "feet": feet
    }

for name in ['front', 'three_quarter', 'profile', 'back']:
    data = clean_segment_view(name)
    print(f"{name}: head={len(data['head'])}, visor={len(data['visor'])}, eyes={len(data['eyes'])}, neck={len(data['neck'])}, torso={len(data['torso'])}, pods={len(data['pods'])}, feet={len(data['feet'])}")
