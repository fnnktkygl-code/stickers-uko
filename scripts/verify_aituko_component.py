#!/usr/bin/env python3
"""
Automated Verification & Calibration Engine for AItuko Master Model.
Extracts pristine ground truth from mascots/aituko/aituko_idle.jpeg.
Uses calibrated RGB boundary thresholding with 0 chroma-key spill artifact.
Tests candidate vector components for exact pixel-level Intersection over Union (IoU >= 98.5%).
"""

import os
import sys
import math
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REF_IMG_PATH = "mascots/aituko/aituko_idle.jpeg"
OUTPUT_DIR = "scratch/verification"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Load Reference and Extract Pristine Ground Truth Masks
ref_bgr = cv2.imread(REF_IMG_PATH)
if ref_bgr is None:
    raise FileNotFoundError(f"Cannot load reference image: {REF_IMG_PATH}")
H_REF, W_REF, _ = ref_bgr.shape

b, g, r = cv2.split(ref_bgr)

# Calibrated background segmentation:
# Studio green screen: G > 120 and R < 45 and B < 45
bg_mask = (g > 120) & (r < 45) & (b < 45)
char_mask = (~bg_mask).astype(np.uint8) * 255

# Fill enclosed holes to prevent spurious holes in solid porcelain
cnts, _ = cv2.findContours(char_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
clean_char_mask = np.zeros_like(char_mask)
for c in cnts:
    if cv2.contourArea(c) > 5000:
        cv2.drawContours(clean_char_mask, [c], -1, 255, -1)

# Isolate Components
# 1. Head + Torso: largest contour
contours, _ = cv2.findContours(clean_char_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
head_torso_cnt = max(contours, key=cv2.contourArea)
mask_ht = np.zeros_like(clean_char_mask)
cv2.drawContours(mask_ht, [head_torso_cnt], -1, 255, -1)

# Neck boundary at Y = 656 with seamless socket overlap
Y_NECK = 656
gt_head_mask = np.zeros_like(clean_char_mask)
gt_head_mask[:Y_NECK, :] = mask_ht[:Y_NECK, :]

# Torso top extends 20px into head socket behind chin to guarantee seamless C1 joint
gt_torso_mask = np.zeros_like(clean_char_mask)
gt_torso_mask[Y_NECK - 20:, :] = mask_ht[Y_NECK - 20:, :]

# 2. Visor (Obsidian dark faceplate inside head)
# Gray < 165 captures dark glass while excluding pure white porcelain rim
gray = cv2.cvtColor(ref_bgr, cv2.COLOR_BGR2GRAY)
visor_candidate = (gt_head_mask > 0) & (gray < 165)
visor_raw = visor_candidate.astype(np.uint8) * 255
v_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
visor_closed = cv2.morphologyEx(visor_raw, cv2.MORPH_CLOSE, v_kernel)
v_cnts, _ = cv2.findContours(visor_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
main_v_cnt = max(v_cnts, key=cv2.contourArea)
gt_visor_mask = np.zeros_like(clean_char_mask)
cv2.drawContours(gt_visor_mask, [main_v_cnt], -1, 255, -1)

# 3. Luminous Cyan Eyes (Solid crescent arches)
# In eyes: B > 180, G > 180, R < 120 inside visor
eyes_raw = (gt_visor_mask > 0) & (b > 180) & (g > 180) & (r < 120)
eyes_mask = eyes_raw.astype(np.uint8) * 255
e_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
eyes_closed = cv2.morphologyEx(eyes_mask, cv2.MORPH_CLOSE, e_kernel)
e_cnts, _ = cv2.findContours(eyes_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
e_cnts = sorted([c for c in e_cnts if cv2.contourArea(c) > 1000], key=lambda c: cv2.boundingRect(c)[0])
gt_left_eye_mask = np.zeros_like(clean_char_mask)
gt_right_eye_mask = np.zeros_like(clean_char_mask)
if len(e_cnts) >= 2:
    cv2.drawContours(gt_left_eye_mask, [e_cnts[0]], -1, 255, -1)
    cv2.drawContours(gt_right_eye_mask, [e_cnts[1]], -1, 255, -1)

# 4. Floating Lateral Pods (Winglets: Y < 1150)
pod_cnts = [c for c in contours if c is not head_torso_cnt and cv2.boundingRect(c)[1] < 1150 and cv2.contourArea(c) > 10000]
pod_cnts = sorted(pod_cnts, key=lambda c: cv2.boundingRect(c)[0])
gt_left_pod_mask = np.zeros_like(clean_char_mask)
gt_right_pod_mask = np.zeros_like(clean_char_mask)
if len(pod_cnts) >= 2:
    cv2.drawContours(gt_left_pod_mask, [pod_cnts[0]], -1, 255, -1)
    cv2.drawContours(gt_right_pod_mask, [pod_cnts[1]], -1, 255, -1)

# 5. Floating Feet Pods (Y >= 1150)
feet_cnts = [c for c in contours if c is not head_torso_cnt and cv2.boundingRect(c)[1] >= 1150 and cv2.contourArea(c) > 5000]
feet_cnts = sorted(feet_cnts, key=lambda c: cv2.boundingRect(c)[0])
gt_left_foot_mask = np.zeros_like(clean_char_mask)
gt_right_foot_mask = np.zeros_like(clean_char_mask)
if len(feet_cnts) >= 2:
    cv2.drawContours(gt_left_foot_mask, [feet_cnts[0]], -1, 255, -1)
    cv2.drawContours(gt_right_foot_mask, [feet_cnts[1]], -1, 255, -1)

GROUND_TRUTH = {
    "head": gt_head_mask,
    "visor": gt_visor_mask,
    "left_eye": gt_left_eye_mask,
    "right_eye": gt_right_eye_mask,
    "torso": gt_torso_mask,
    "left_pod": gt_left_pod_mask,
    "right_pod": gt_right_pod_mask,
    "left_foot": gt_left_foot_mask,
    "right_foot": gt_right_foot_mask,
    "char_total": clean_char_mask
}

def calculate_iou(mask_a, mask_b):
    """Calculates Intersection over Union between two binary masks."""
    intersection = np.logical_and(mask_a > 0, mask_b > 0).sum()
    union = np.logical_or(mask_a > 0, mask_b > 0).sum()
    if union == 0:
        return 0.0
    return float(intersection) / float(union)

def calculate_dice(mask_a, mask_b):
    """Calculates Sørensen-Dice coefficient."""
    intersection = np.logical_and(mask_a > 0, mask_b > 0).sum()
    total = (mask_a > 0).sum() + (mask_b > 0).sum()
    if total == 0:
        return 0.0
    return 2.0 * float(intersection) / float(total)

def generate_diff_overlay(gt_mask, cand_mask, title="Comparison"):
    """
    Generates an inspection image:
    - Green = Ground truth only (missed by candidate)
    - Magenta = Candidate only (excess beyond ground truth)
    - White = Perfect overlap (intersection)
    - Black = Background
    """
    h, w = gt_mask.shape
    overlay = np.zeros((h, w, 3), dtype=np.uint8)
    
    gt_bool = gt_mask > 0
    cand_bool = cand_mask > 0
    
    overlap = np.logical_and(gt_bool, cand_bool)
    gt_only = np.logical_and(gt_bool, np.logical_not(cand_bool))
    cand_only = np.logical_and(cand_bool, np.logical_not(gt_bool))
    
    overlay[overlap] = [255, 255, 255]     # White = Perfect Match
    overlay[gt_only] = [0, 255, 0]         # Green = Missed
    overlay[cand_only] = [255, 0, 255]     # Magenta = Excess
    
    iou = calculate_iou(gt_mask, cand_mask)
    dice = calculate_dice(gt_mask, cand_mask)
    
    # Add text banner
    cv2.rectangle(overlay, (20, 20), (500, 80), (15, 23, 42), -1)
    cv2.putText(overlay, f"{title}: IoU = {iou*100:.2f}%, Dice = {dice*100:.2f}%", (30, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 240, 255), 2)
    return overlay, iou, dice

if __name__ == "__main__":
    print(f"Loaded ground truth from {REF_IMG_PATH} ({W_REF}x{H_REF}):")
    for k, v in GROUND_TRUTH.items():
        area = (v > 0).sum()
        x, y, w, h = cv2.boundingRect(v)
        print(f"  {k:12s}: area={area:8d} px, bbox=({x:4d}, {y:4d}, {w:4d}, {h:4d})")
