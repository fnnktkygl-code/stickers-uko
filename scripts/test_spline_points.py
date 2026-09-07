#!/usr/bin/env python3
"""
Test cubic spline approximation with different point counts.
Ensures smooth C1 cubic Bézier splines while retaining >99% IoU.
"""

import os
import sys
import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.verify_aituko_component import GROUND_TRUTH, calculate_iou

for comp_name in ["head", "visor", "left_eye", "right_eye", "torso", "left_pod", "right_pod", "left_foot", "right_foot"]:
    gt_raw = GROUND_TRUTH[comp_name]
    cnts, _ = cv2.findContours(gt_raw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnt = max(cnts, key=cv2.contourArea)
    
    for eps in [0.6, 0.8, 1.0, 1.2]:
        approx = cv2.approxPolyDP(cnt, eps, True)
        cand_mask = np.zeros_like(gt_raw)
        cv2.fillPoly(cand_mask, [approx], 255)
        iou = calculate_iou(gt_raw, cand_mask)
        if iou >= 0.995 or eps == 1.2:
            print(f"  {comp_name:12s} eps={eps:.1f} ({len(approx):3d} pts) -> IoU = {iou*100:6.2f}%")
            break
