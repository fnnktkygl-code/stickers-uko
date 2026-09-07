#!/usr/bin/env python3
"""
Calibrate clean segmentation of AItuko mascot.
Extracts ground truth with 0 chroma-key spill artifact.
"""

import os
import cv2
import numpy as np

REF_IMG_PATH = "mascots/aituko/aituko_idle.jpeg"
img = cv2.imread(REF_IMG_PATH)
if img is None:
    raise FileNotFoundError("Reference image not found")

b, g, r = cv2.split(img)

# Background is pure chroma key green
# In the background: G > 120 and R < 45 and B < 45
bg_mask = (g > 120) & (r < 45) & (b < 45)

# Invert to get character mask
char_mask = (~bg_mask).astype(np.uint8) * 255

# Fill any small enclosed holes (if any)
cnts, _ = cv2.findContours(char_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
clean_char_mask = np.zeros_like(char_mask)
# Keep the valid character components (area > 5000)
for c in cnts:
    if cv2.contourArea(c) > 5000:
        cv2.drawContours(clean_char_mask, [c], -1, 255, -1)

# Now check the components:
# 1. Head + Torso: largest contour
contours, _ = cv2.findContours(clean_char_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
head_torso_cnt = max(contours, key=cv2.contourArea)
mask_ht = np.zeros_like(clean_char_mask)
cv2.drawContours(mask_ht, [head_torso_cnt], -1, 255, -1)

Y_NECK = 656
head_mask = np.zeros_like(clean_char_mask)
head_mask[:Y_NECK, :] = mask_ht[:Y_NECK, :]

torso_mask = np.zeros_like(clean_char_mask)
torso_mask[Y_NECK:, :] = mask_ht[Y_NECK:, :]

# Let's inspect torso bottom crop
x, y, w, h = cv2.boundingRect(torso_mask)
print(f"Torso bbox: x={x}, y={y}, w={w}, h={h}")
torso_crop = clean_char_mask[1100:1220, 1200:1550]
cv2.imwrite("scratch/clean_torso_rgb_test.png", torso_crop)

# Let's inspect feet
feet_cnts = [c for c in contours if c is not head_torso_cnt and cv2.boundingRect(c)[1] >= 1150]
print(f"Found {len(feet_cnts)} feet components")
for i, fc in enumerate(feet_cnts):
    fx, fy, fw, fh = cv2.boundingRect(fc)
    print(f"  Foot {i}: bbox=({fx}, {fy}, {fw}, {fh}), area={cv2.contourArea(fc)}")

feet_crop = clean_char_mask[1150:1350, 1150:1600]
cv2.imwrite("scratch/clean_feet_rgb_test.png", feet_crop)

# Let's inspect lateral pods
pod_cnts = [c for c in contours if c is not head_torso_cnt and cv2.boundingRect(c)[1] < 1150]
print(f"Found {len(pod_cnts)} pod components")
for i, pc in enumerate(pod_cnts):
    px, py, pw, ph = cv2.boundingRect(pc)
    print(f"  Pod {i}: bbox=({px}, {py}, {pw}, {ph}), area={cv2.contourArea(pc)}")

# Visor: inside head mask, visor has dark glass (porcelain is bright white: R,G,B > 180)
# Inside head_mask, porcelain has B > 180 and G > 180 and R > 180.
# Visor glass has dark tone: average intensity (R+G+B)/3 < 160.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
visor_candidate = (head_mask > 0) & (gray < 165)
visor_mask = visor_candidate.astype(np.uint8) * 255
# Morphological close to bridge specular streaks
v_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
visor_mask = cv2.morphologyEx(visor_mask, cv2.MORPH_CLOSE, v_kernel)
vcnts, _ = cv2.findContours(visor_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
main_visor_cnt = max(vcnts, key=cv2.contourArea)
final_visor = np.zeros_like(visor_mask)
cv2.drawContours(final_visor, [main_visor_cnt], -1, 255, -1)

vx, vy, vw, vh = cv2.boundingRect(final_visor)
print(f"Visor bbox: x={vx}, y={vy}, w={vw}, h={vh}, area={(final_visor>0).sum()}")
visor_crop = final_visor[250:350, 1150:1600]
cv2.imwrite("scratch/clean_visor_rgb_test.png", visor_crop)

# Luminous Eyes
# Eyes have high cyan/blue saturation and high brightness inside visor
# In eyes: B > 180 and G > 180 and R < 100
eyes_raw = (final_visor > 0) & (b > 180) & (g > 180) & (r < 120)
eyes_mask = eyes_raw.astype(np.uint8) * 255
# Smooth and close scanline gaps
e_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
eyes_closed = cv2.morphologyEx(eyes_mask, cv2.MORPH_CLOSE, e_kernel)
ecnts, _ = cv2.findContours(eyes_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
ecnts = sorted([c for c in ecnts if cv2.contourArea(c) > 500], key=lambda c: cv2.boundingRect(c)[0])
print(f"Found {len(ecnts)} eye components")
for i, ec in enumerate(ecnts):
    ex, ey, ew, eh = cv2.boundingRect(ec)
    print(f"  Eye {i}: bbox=({ex}, {ey}, {ew}, {eh}), area={cv2.contourArea(ec)}")

cv2.imwrite("scratch/clean_eyes_test.png", eyes_closed[360:480, 1200:1550])
print("Calibration test images generated in scratch/")
