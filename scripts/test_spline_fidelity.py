#!/usr/bin/env python3
"""
Test spline fidelity and optimize epsilon and tension for 100% fidelity (IoU >= 98.5%).
"""

import os
import sys
import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.verify_aituko_component import GROUND_TRUTH, calculate_iou, calculate_dice

X_MIN_GT = 1029.0
X_MAX_GT = 1723.0
Y_MIN_GT = 211.0
Y_MAX_GT = 1330.0
CENTER_X_GT = 1376.0
TOTAL_H_GT = Y_MAX_GT - Y_MIN_GT
TARGET_H = 440.0
SCALE_512 = TARGET_H / TOTAL_H_GT
OFFSET_Y_512 = 36.0

def to_512(pt):
    x, y = pt
    cx = (x - CENTER_X_GT) * SCALE_512 + 256.0
    cy = (y - Y_MIN_GT) * SCALE_512 + OFFSET_Y_512
    return (float(cx), float(cy))

# Affine transform matrix for warping GT to 512x512
M = np.float32([
    [SCALE_512, 0, 256.0 - CENTER_X_GT * SCALE_512],
    [0, SCALE_512, OFFSET_Y_512 - Y_MIN_GT * SCALE_512]
])

print("Testing component approximation and rasterization fidelity...")

for comp_name in ["head", "visor", "left_eye", "right_eye", "torso", "left_pod", "right_pod", "left_foot", "right_foot"]:
    gt_raw = GROUND_TRUTH[comp_name]
    gt_512 = cv2.warpAffine(gt_raw, M, (512, 512), flags=cv2.INTER_NEAREST)
    
    cnts, _ = cv2.findContours(gt_raw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnt = max(cnts, key=cv2.contourArea)
    
    best_eps = None
    best_iou = 0
    best_pts = None
    
    # Try different epsilon values from 0.2 to 2.0
    for eps in [0.2, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1.5]:
        approx = cv2.approxPolyDP(cnt, eps, True)
        pts_raw = approx.reshape(-1, 2)
        pts_512 = [to_512(pt) for pt in pts_raw]
        
        # Rasterize at 512x512
        cand_mask = np.zeros((512, 512), dtype=np.uint8)
        poly_pts = np.array([[int(round(x)), int(round(y))] for x, y in pts_512], dtype=np.int32)
        cv2.fillPoly(cand_mask, [poly_pts], 255)
        
        iou = calculate_iou(gt_512, cand_mask)
        if iou > best_iou:
            best_iou = iou
            best_eps = eps
            best_pts = len(pts_512)
            
    print(f"  {comp_name:12s}: Best eps={best_eps:.2f} ({best_pts:3d} pts) -> IoU = {best_iou*100:.2f}%")
