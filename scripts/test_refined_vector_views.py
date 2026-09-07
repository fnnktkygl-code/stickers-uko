#!/usr/bin/env python3
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

def smooth_mask(mask, blur_k=5, thresh_val=128):
    b = cv2.GaussianBlur(mask, (blur_k, blur_k), 0)
    _, t = cv2.threshold(b, thresh_val, 255, cv2.THRESH_BINARY)
    return t

def get_clean_spline_pts(mask, eps=1.0):
    sm = smooth_mask(mask, blur_k=7)
    cnts, _ = cv2.findContours(sm, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not cnts:
        return []
    c = max(cnts, key=cv2.contourArea)
    approx = cv2.approxPolyDP(c, eps, True)
    return approx.reshape(-1, 2)

# Test on 3/4 view
rgba_3q = cv2.imread("scratch/turnaround_views/three_quarter_clean.png", cv2.IMREAD_UNCHANGED)
h, w, _ = rgba_3q.shape
alpha = rgba_3q[:, :, 3]
gray = cv2.cvtColor(rgba_3q[:, :, :3], cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(rgba_3q[:, :, :3], cv2.COLOR_BGR2HSV)
char_mask = (alpha > 80).astype(np.uint8) * 255

# Head: y < 196
h_mask = np.zeros_like(char_mask)
h_mask[:196, :] = char_mask[:196, :]
# Visor inside head: gray < 70, y < 170
v_mask = np.zeros_like(char_mask)
v_mask[:170, :] = (h_mask[:170, :] > 0) & (gray[:170, :] < 70)
v_pts = get_clean_spline_pts(v_mask, eps=1.0)
print("3/4 visor pts:", len(v_pts))

# Test on profile
rgba_prof = cv2.imread("scratch/turnaround_views/profile_clean.png", cv2.IMREAD_UNCHANGED)
alpha_p = rgba_prof[:, :, 3]
gray_p = cv2.cvtColor(rgba_prof[:, :, :3], cv2.COLOR_BGR2GRAY)
char_p = (alpha_p > 80).astype(np.uint8) * 255
vp_mask = np.zeros_like(char_p)
vp_mask[:170, :] = (char_p[:170, :] > 0) & (gray_p[:170, :] < 70)
vp_pts = get_clean_spline_pts(vp_mask, eps=0.8)
print("Profile visor pts:", len(vp_pts))

