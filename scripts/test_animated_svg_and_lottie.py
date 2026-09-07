#!/usr/bin/env python3
import os
import json
import math
import subprocess
import cv2
import numpy as np
from PIL import Image

def get_filled_contour_pts(mask, eps=0.6, min_area=1000):
    cnts, _ = cv2.findContours(mask.astype(np.uint8)*255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    valid = [c for c in cnts if cv2.contourArea(c) > min_area]
    if not valid:
        return []
    c = max(valid, key=cv2.contourArea)
    approx = cv2.approxPolyDP(c, eps, True)
    pts = approx.reshape(-1, 2)
    return [(round(float(p[0]), 2), round(float(p[1]), 2)) for p in pts]

def points_to_svg_cubic_spline(pts, tension=1.0):
    n = len(pts)
    if n < 3:
        return ""
    c_factor = tension / 6.0
    d = [f"M {pts[0][0]:.2f} {pts[0][1]:.2f}"]
    for i in range(n):
        p_prev = pts[(i - 1) % n]
        p_curr = pts[i]
        p_next = pts[(i + 1) % n]
        p_next2 = pts[(i + 2) % n]
        c1_x = p_curr[0] + (p_next[0] - p_prev[0]) * c_factor
        c1_y = p_curr[1] + (p_next[1] - p_prev[1]) * c_factor
        c2_x = p_next[0] - (p_next2[0] - p_curr[0]) * c_factor
        c2_y = p_next[1] - (p_next2[1] - p_curr[1]) * c_factor
        d.append(f"C {c1_x:.2f} {c1_y:.2f}, {c2_x:.2f} {c2_y:.2f}, {p_next[0]:.2f} {p_next[1]:.2f}")
    d.append("Z")
    return " ".join(d)

def points_to_lottie_shape(pts, center_x=0.0, center_y=0.0, tension=1.0):
    n = len(pts)
    c_factor = tension / 6.0
    v, it, ot = [], [], []
    for i in range(n):
        p_prev = pts[(i - 1) % n]
        p_curr = pts[i]
        p_next = pts[(i + 1) % n]
        v.append([round(float(p_curr[0] - center_x), 2), round(float(p_curr[1] - center_y), 2)])
        ot.append([round(float((p_next[0] - p_prev[0]) * c_factor), 2), round(float((p_next[1] - p_prev[1]) * c_factor), 2)])
        it.append([round(float(-(p_next[0] - p_prev[0]) * c_factor), 2), round(float(-(p_next[1] - p_prev[1]) * c_factor), 2)])
    return {
        "ty": "sh", "d": 1,
        "ks": {"a": 0, "k": {"c": True, "i": it, "o": ot, "v": v}},
        "nm": "Path"
    }

def make_lottie_kf(t, s, e=None):
    kf = {
        "t": t,
        "s": s if isinstance(s, list) else [s],
        "i": {"x": [0.45, 0.45, 0.45] if isinstance(s, list) else [0.45], "y": [1.0, 1.0, 1.0] if isinstance(s, list) else [1.0]},
        "o": {"x": [0.55, 0.55, 0.55] if isinstance(s, list) else [0.55], "y": [0.0, 0.0, 0.0] if isinstance(s, list) else [0.0]}
    }
    if e is not None:
        kf["e"] = e if isinstance(e, list) else [e]
    return kf

# Extract points from master
img = cv2.imread("mascots/meoweko/meoweko_master_exact_512.png", cv2.IMREAD_UNCHANGED)
b, g, r, a = cv2.split(img)
bgr = cv2.merge([b, g, r])

body_mask = (a > 30)
body_pts = get_filled_contour_pts(body_mask, eps=0.6, min_area=5000)

tail_roi = img[400:485, 115:195]
tail_mask = np.zeros_like(a, dtype=bool)
tail_mask[400:485, 115:195] = (tail_roi[:,:,3] > 30) & (tail_roi[:,:,2] > 130) & (tail_roi[:,:,0] < 105)
tail_mask = cv2.morphologyEx(tail_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))) > 0
tail_pts = get_filled_contour_pts(tail_mask, eps=0.5, min_area=500)

flank_l_roi = img[330:460, 145:225]
flank_l_mask = np.zeros_like(a, dtype=bool)
flank_l_mask[330:460, 145:225] = (flank_l_roi[:,:,3] > 30) & (flank_l_roi[:,:,2] > 140) & (flank_l_roi[:,:,0] < 125)
flank_l_mask = cv2.morphologyEx(flank_l_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))) > 0
flank_l_pts = get_filled_contour_pts(flank_l_mask, eps=0.6, min_area=500)

flank_r_roi = img[330:460, 295:380]
flank_r_mask = np.zeros_like(a, dtype=bool)
flank_r_mask[330:460, 295:380] = (flank_r_roi[:,:,3] > 30) & (flank_r_roi[:,:,2] > 140) & (flank_r_roi[:,:,0] < 125)
flank_r_mask = cv2.morphologyEx(flank_r_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))) > 0
flank_r_pts = get_filled_contour_pts(flank_r_mask, eps=0.6, min_area=500)

# White solid fur
hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
white_cand = (a > 30) & (hsv[:,:,1] < 65) & (hsv[:,:,2] > 140)
neck_shadow_white = (a > 30) & (hsv[:,:,1] < 50) & (hsv[:,:,2] > 110) & (np.arange(512)[:, None] > 200) & (np.arange(512)[:, None] < 265) & (np.arange(512)[None, :] > 200) & (np.arange(512)[None, :] < 320)
cheeks_white = (a > 30) & (np.arange(512)[:, None] > 175) & (np.arange(512)[:, None] < 250) & (np.arange(512)[None, :] > 155) & (np.arange(512)[None, :] < 365) & (hsv[:,:,1] < 80)
blaze_white = (a > 30) & (np.arange(512)[:, None] > 110) & (np.arange(512)[:, None] < 200) & (np.arange(512)[None, :] > 230) & (np.arange(512)[None, :] < 285) & (hsv[:,:,1] < 70)
eye_bridge = (np.arange(512)[:, None] > 145) & (np.arange(512)[:, None] < 195) & (np.arange(512)[None, :] > 190) & (np.arange(512)[None, :] < 330) & (a > 30)
white_total = white_cand | neck_shadow_white | cheeks_white | blaze_white | eye_bridge
white_u8 = cv2.morphologyEx(white_total.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
cnts, _ = cv2.findContours(white_u8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
white_solid = np.zeros_like(white_u8)
main_white_cnt = max(cnts, key=cv2.contourArea)
cv2.drawContours(white_solid, [main_white_cnt], -1, 255, -1)
white_coat_pts = get_filled_contour_pts(white_solid > 0, eps=0.6, min_area=3000)

print(f"Points: body={len(body_pts)}, tail={len(tail_pts)}, flank_l={len(flank_l_pts)}, flank_r={len(flank_r_pts)}, white={len(white_coat_pts)}")

