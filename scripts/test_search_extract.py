import cv2, numpy as np

cap = cv2.VideoCapture('mascots/owluko/owluko_searching.mp4')
ret, frame = cap.read()
cap.release()

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
lower_green = np.array([35, 60, 50])
upper_green = np.array([85, 255, 255])
mask = cv2.inRange(hsv, lower_green, upper_green)
mascot_mask = cv2.bitwise_not(mask)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
mascot_mask = cv2.morphologyEx(mascot_mask, cv2.MORPH_OPEN, kernel)

# Despill
b, g, r = cv2.split(frame)
excess = np.maximum(0, g.astype(int) - np.maximum(r.astype(int), b.astype(int)))
g_clean = np.where(excess > 0, ((r.astype(float)*0.5 + b.astype(float)*0.5)).astype(np.uint8), g)
a_clean = np.where(mascot_mask < 35, 0, mascot_mask)

# Find bounding box
ys, xs = np.where(a_clean > 30)
fig = cv2.merge([b, g_clean, r, a_clean])[ys.min():ys.max()+1, xs.min():xs.max()+1]

TARGET_H = 450.0
scale = TARGET_H / float(fig.shape[0])
nw = int(round(fig.shape[1] * scale))
nh = int(round(TARGET_H))
scaled = cv2.resize(fig, (nw, nh), interpolation=cv2.INTER_LANCZOS4)

canvas = np.zeros((512, 512, 4), dtype=np.uint8)
px = (512 - nw) // 2
py = 491 - nh # feet bottom locked at 491
canvas[py:py+nh, px:px+nw] = scaled

cv2.imwrite('scratch/test_f0_clean_512.png', canvas)
print(f'Test f0 saved, nw={nw}, nh={nh}, px={px}, py={py}')
