#!/usr/bin/env python3
"""
Test extraction of precise anatomical splines for Meoweko from meoweko_master_exact_512.png.
"""
import os
import cv2
import numpy as np

img = cv2.imread("mascots/meoweko/meoweko_master_exact_512.png", cv2.IMREAD_UNCHANGED)
b, g, r, a = cv2.split(img)

def get_contour_pts(mask, eps=1.0, min_area=50):
    cnts, _ = cv2.findContours(mask.astype(np.uint8)*255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    valid = [c for c in cnts if cv2.contourArea(c) > min_area]
    if not valid:
        return []
    c = max(valid, key=cv2.contourArea)
    approx = cv2.approxPolyDP(c, eps, True)
    pts = approx.reshape(-1, 2)
    return [(float(p[0]), float(p[1])) for p in pts]

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

# 1. Total Silhouette
body_mask = (a > 30)
body_pts = get_contour_pts(body_mask, eps=1.0, min_area=5000)
print(f"Body silhouette points: {len(body_pts)}")

# 2. Tail (X in [110, 205], Y in [400, 485])
tail_mask = np.zeros_like(a, dtype=bool)
tail_mask[400:485, 110:205] = (a[400:485, 110:205] > 30) & (r[400:485, 110:205] > 130) & (b[400:485, 110:205] < 100)
tail_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
tail_mask = cv2.morphologyEx(tail_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, tail_kernel) > 0
tail_pts = get_contour_pts(tail_mask, eps=0.8, min_area=500)
print(f"Tail points: {len(tail_pts)}")

# 3. Left flank (X in [145, 230], Y in [330, 455])
flank_l_mask = np.zeros_like(a, dtype=bool)
flank_l_mask[330:455, 145:230] = (a[330:455, 145:230] > 30) & (r[330:455, 145:230] > 140) & (b[330:455, 145:230] < 120)
flank_l_mask = cv2.morphologyEx(flank_l_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, tail_kernel) > 0
flank_l_pts = get_contour_pts(flank_l_mask, eps=0.8, min_area=500)
print(f"Left flank points: {len(flank_l_pts)}")

# 4. Right flank (X in [290, 380], Y in [330, 460])
flank_r_mask = np.zeros_like(a, dtype=bool)
flank_r_mask[330:460, 290:380] = (a[330:460, 290:380] > 30) & (r[330:460, 290:380] > 140) & (b[330:460, 290:380] < 120)
flank_r_mask = cv2.morphologyEx(flank_r_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, tail_kernel) > 0
flank_r_pts = get_contour_pts(flank_r_mask, eps=0.8, min_area=500)
print(f"Right flank points: {len(flank_r_pts)}")

# 5. Central cream body / chest / front legs (Y in [240, 490], X in [185, 330])
chest_mask = np.zeros_like(a, dtype=bool)
chest_mask[240:490, 185:330] = (a[240:490, 185:330] > 30) & (r[240:490, 185:330] > 175) & (g[240:490, 185:330] > 170) & (b[240:490, 185:330] > 160)
chest_mask = cv2.morphologyEx(chest_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))) > 0
chest_pts = get_contour_pts(chest_mask, eps=0.8, min_area=2000)
print(f"Chest / legs points: {len(chest_pts)}")

# 6. Paws (Left: X in [185, 260], Y in [440, 491]; Right: X in [260, 335], Y in [440, 491])
paw_l_mask = np.zeros_like(a, dtype=bool)
paw_l_mask[440:491, 185:260] = chest_mask[440:491, 185:260]
paw_l_pts = get_contour_pts(paw_l_mask, eps=0.6, min_area=300)
print(f"Paw left points: {len(paw_l_pts)}")

paw_r_mask = np.zeros_like(a, dtype=bool)
paw_r_mask[440:491, 260:335] = chest_mask[440:491, 260:335]
paw_r_pts = get_contour_pts(paw_r_mask, eps=0.6, min_area=300)
print(f"Paw right points: {len(paw_r_pts)}")

# 7. Head (Y in [40, 275], X in [150, 395])
head_mask = np.zeros_like(a, dtype=bool)
head_mask[40:275, 150:395] = (a[40:275, 150:395] > 30)
head_pts = get_contour_pts(head_mask, eps=0.8, min_area=5000)
print(f"Head outline points: {len(head_pts)}")

