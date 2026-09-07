#!/usr/bin/env python3
import cv2
import numpy as np

img = cv2.imread("mascots/meoweko/meoweko_master_exact_512.png", cv2.IMREAD_UNCHANGED)
b, g, r, a = cv2.split(img)

def get_contour_pts(mask, eps=0.8, min_area=30):
    cnts, _ = cv2.findContours(mask.astype(np.uint8)*255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    valid = [c for c in cnts if cv2.contourArea(c) > min_area]
    if not valid:
        return []
    c = max(valid, key=cv2.contourArea)
    approx = cv2.approxPolyDP(c, eps, True)
    pts = approx.reshape(-1, 2)
    return [(float(p[0]), float(p[1])) for p in pts]

# 1. Left inner ear:
# Look in X in [160, 220], Y in [65, 145]
ear_l_mask = np.zeros_like(a, dtype=bool)
# Inner ear is pinker/lighter than outer ginger
ear_l_roi = img[65:145, 160:220]
# In inner ear: r > 180, g in [110, 160], b in [85, 150]
el_pink = (ear_l_roi[:,:,3] > 30) & (ear_l_roi[:,:,2] > 180) & (ear_l_roi[:,:,1] > 110) & (ear_l_roi[:,:,1] < 170) & (ear_l_roi[:,:,0] > 80)
ear_l_mask[65:145, 160:220] = el_pink
el_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
ear_l_mask = cv2.morphologyEx(ear_l_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, el_kernel) > 0
ear_l_pts = get_contour_pts(ear_l_mask, eps=0.6, min_area=100)
print(f"Ear L inner points: {len(ear_l_pts)}")

# 2. Right inner ear:
# Look in X in [335, 385], Y in [65, 145]
ear_r_mask = np.zeros_like(a, dtype=bool)
ear_r_roi = img[65:145, 335:385]
er_pink = (ear_r_roi[:,:,3] > 30) & (ear_r_roi[:,:,2] > 180) & (ear_r_roi[:,:,1] > 110) & (ear_r_roi[:,:,1] < 170) & (ear_r_roi[:,:,0] > 80)
ear_r_mask[65:145, 335:385] = er_pink
ear_r_mask = cv2.morphologyEx(ear_r_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, el_kernel) > 0
ear_r_pts = get_contour_pts(ear_r_mask, eps=0.6, min_area=100)
print(f"Ear R inner points: {len(ear_r_pts)}")

# 3. Eyes:
# Left Eye Socket: X in [180, 255], Y in [140, 215]
eye_l_dark = (a[140:215, 180:255] > 30) & (r[140:215, 180:255] < 75) & (g[140:215, 180:255] < 75) & (b[140:215, 180:255] < 75)
eye_l_iris = (a[140:215, 180:255] > 30) & (r[140:215, 180:255] > 90) & (g[140:215, 180:255] > 80) & (b[140:215, 180:255] < 85)
eye_l_mask = np.zeros_like(a, dtype=bool)
eye_l_mask[140:215, 180:255] = eye_l_dark | eye_l_iris
eye_l_mask = cv2.morphologyEx(eye_l_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))) > 0
eye_l_pts = get_contour_pts(eye_l_mask, eps=0.5, min_area=500)
print(f"Left eye orb points: {len(eye_l_pts)}")

# Right Eye Socket: X in [290, 360], Y in [140, 215]
eye_r_dark = (a[140:215, 290:360] > 30) & (r[140:215, 290:360] < 75) & (g[140:215, 290:360] < 75) & (b[140:215, 290:360] < 75)
eye_r_iris = (a[140:215, 290:360] > 30) & (r[140:215, 290:360] > 90) & (g[140:215, 290:360] > 80) & (b[140:215, 290:360] < 85)
eye_r_mask = np.zeros_like(a, dtype=bool)
eye_r_mask[140:215, 290:360] = eye_r_dark | eye_r_iris
eye_r_mask = cv2.morphologyEx(eye_r_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))) > 0
eye_r_pts = get_contour_pts(eye_r_mask, eps=0.5, min_area=500)
print(f"Right eye orb points: {len(eye_r_pts)}")

# 4. White blaze & cheeks (Cream white on face, Y in [80, 260], excluding eyes)
face_white_mask = np.zeros_like(a, dtype=bool)
face_white_mask[80:260, 150:390] = (a[80:260, 150:390] > 30) & (r[80:260, 150:390] > 185) & (g[80:260, 150:390] > 180) & (b[80:260, 150:390] > 170)
# Exclude eyes
face_white_mask[eye_l_mask] = False
face_white_mask[eye_r_mask] = False
face_white_mask = cv2.morphologyEx(face_white_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))) > 0
blaze_pts = get_contour_pts(face_white_mask, eps=0.8, min_area=2000)
print(f"White face/blaze points: {len(blaze_pts)}")

# 5. Ginger crown / temples / ears shell (Head area excluding white face)
ginger_head_mask = np.zeros_like(a, dtype=bool)
ginger_head_mask[40:260, 150:395] = (a[40:260, 150:395] > 30) & (~face_white_mask[40:260, 150:395]) & (~eye_l_mask[40:260, 150:395]) & (~eye_r_mask[40:260, 150:395])
ginger_head_mask = cv2.morphologyEx(ginger_head_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))) > 0
ginger_head_pts = get_contour_pts(ginger_head_mask, eps=0.8, min_area=3000)
print(f"Ginger crown points: {len(ginger_head_pts)}")

