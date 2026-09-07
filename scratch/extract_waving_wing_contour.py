import cv2
import numpy as np
from PIL import Image

# Load panel 4
p4 = cv2.imread('scratch/waving_panels/panel_4.png')
h_p4, w_p4, _ = p4.shape

p4_gray = cv2.cvtColor(p4, cv2.COLOR_BGR2GRAY)

mask_lp = (p4_gray < 70) & (np.arange(w_p4)[None, :] < 160)
ylp, xlp = np.where(mask_lp)
lp_c = (xlp.mean(), ylp.mean())

mask_rp = (p4_gray < 70) & (np.arange(w_p4)[None, :] > 170) & (np.arange(w_p4)[None, :] < 240)
yrp, xrp = np.where(mask_rp)
rp_c = (xrp.mean(), yrp.mean())

print("P4 Left pupil:", lp_c)
print("P4 Right pupil:", rp_c)
eye_dist_p4 = rp_c[0] - lp_c[0]
print("P4 Eye distance:", eye_dist_p4)

# In master: Left (402, 355), Right (622, 355) -> distance = 220 px
scale_factor = 220.0 / eye_dist_p4
print(f"Exact scale factor from P4 to 1024 master: {scale_factor:.4f}")

tx = 402.0 - lp_c[0] * scale_factor
ty = 355.0 - lp_c[1] * scale_factor
print(f"Translation: tx = {tx:.2f}, ty = {ty:.2f}")

# Warp panel 4 to 1024x1024 canvas
M = np.float32([[scale_factor, 0, tx], [0, scale_factor, ty]])
p4_warped = cv2.warpAffine(p4, M, (1024, 1024), borderValue=(255, 255, 255))
cv2.imwrite('scratch/p4_warped_1024.png', p4_warped)
print("Saved p4_warped_1024.png")

# Also warp panel 3 and panel 5
p3 = cv2.imread('scratch/waving_panels/panel_3.png')
p3_warped = cv2.warpAffine(p3, M, (1024, 1024), borderValue=(255, 255, 255))
cv2.imwrite('scratch/p3_warped_1024.png', p3_warped)

p5 = cv2.imread('scratch/waving_panels/panel_5.png')
p5_warped = cv2.warpAffine(p5, M, (1024, 1024), borderValue=(255, 255, 255))
cv2.imwrite('scratch/p5_warped_1024.png', p5_warped)
print("Saved warped panels 3, 4, 5.")
