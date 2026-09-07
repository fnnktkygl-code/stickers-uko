#!/usr/bin/env python3
import cv2
import numpy as np

img = cv2.imread('mascots/luneko/luneko_master_turnaround.jpeg')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_green = np.array([35, 60, 50])
upper_green = np.array([85, 255, 255])
mask = cv2.inRange(hsv, lower_green, upper_green)
mascot_mask = cv2.bitwise_not(mask)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
mascot_mask = cv2.morphologyEx(mascot_mask, cv2.MORPH_OPEN, kernel)

b, g, r = cv2.split(img)
excess = np.maximum(0, g.astype(int) - np.maximum(r.astype(int), b.astype(int)))
g_clean = np.where(excess > 0, ((r.astype(float)*0.5 + b.astype(float)*0.5)).astype(np.uint8), g)
a_clean = np.where(mascot_mask < 35, 0, mascot_mask)

clean_img = cv2.merge([b, g_clean, r, a_clean])

boxes = [
    ("front", 55, 271, 623, 1019),
    ("three_quarter", 686, 269, 680, 1021),
    ("profile_right", 1428, 269, 651, 1019),
    ("back", 2085, 271, 625, 1021)
]

TARGET_H = 450.0
for name, x, y, w, h in boxes:
    crop = clean_img[y:y+h, x:x+w]
    ys, xs = np.where(crop[:, :, 3] > 30)
    tight = crop[ys.min():ys.max()+1, xs.min():xs.max()+1]
    
    scale = TARGET_H / float(tight.shape[0])
    nw = int(round(tight.shape[1] * scale))
    nh = int(round(TARGET_H))
    scaled = cv2.resize(tight, (nw, nh), interpolation=cv2.INTER_LANCZOS4)
    
    canvas = np.zeros((512, 512, 4), dtype=np.uint8)
    px = (512 - nw) // 2
    py = 491 - nh
    canvas[py:py+nh, px:px+nw] = scaled
    # Zero shadow below 491
    canvas[492:, :, 3] = 0
    
    cv2.imwrite(f'scratch/meoweko_{name}_clean_512.png', canvas)
    print(f'Saved scratch/meoweko_{name}_clean_512.png')

# Profile left is horizontally flipped profile right
pr = cv2.imread('scratch/meoweko_profile_right_clean_512.png', cv2.IMREAD_UNCHANGED)
pl = cv2.flip(pr, 1)
cv2.imwrite('scratch/meoweko_profile_left_clean_512.png', pl)
print('Saved scratch/meoweko_profile_left_clean_512.png')

