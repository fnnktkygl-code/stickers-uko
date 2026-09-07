import cv2
import numpy as np

p1 = cv2.imread('scratch/waving_panels/panel_1.png')
master = cv2.imread('mascots/owluko/owluko_master_ref_clean.png')

# In master, the mask contour or beak:
# Let's find template match of beak between p1 and master
# Beak in master:
beak_m = master[380:480, 460:560]
# Scale beak_m to various scales to find best match in p1
best_val = -1
best_s = 1.0
best_loc = (0, 0)
for s in np.linspace(0.25, 0.45, 41):
    bm_res = cv2.resize(beak_m, (0, 0), fx=s, fy=s)
    res = cv2.matchTemplate(p1, bm_res, cv2.TM_CCOEFF_NORMED)
    min_v, max_v, min_l, max_l = cv2.minMaxLoc(res)
    if max_v > best_val:
        best_val = max_v
        best_s = s
        best_loc = max_l

print(f"Best beak match scale: {best_s:.4f} (inv={1/best_s:.4f}), score={best_val:.4f}, loc={best_loc}")
# Scale factor from panel 1 to master: 1 / best_s
inv_s = 1 / best_s

# Match center in p1:
p1_cx = best_loc[0] + (beak_m.shape[1] * best_s) / 2
p1_cy = best_loc[1] + (beak_m.shape[0] * best_s) / 2
# Beak center in master:
m_cx = 460 + 50
m_cy = 380 + 50

tx = m_cx - p1_cx * inv_s
ty = m_cy - p1_cy * inv_s
print(f"Inv scale: {inv_s:.3f}, tx: {tx:.2f}, ty: {ty:.2f}")

M = np.float32([[inv_s, 0, tx], [0, inv_s, ty]])
p1_aligned = cv2.warpAffine(p1, M, (1024, 1024), borderValue=(255, 255, 255))
blend1 = cv2.addWeighted(master, 0.5, p1_aligned, 0.5, 0)
cv2.imwrite('scratch/panel_1_perfect_blend.png', blend1)

# Now apply M to panel 4 and panel 5
p4 = cv2.imread('scratch/waving_panels/panel_4.png')
p4_aligned = cv2.warpAffine(p4, M, (1024, 1024), borderValue=(255, 255, 255))
cv2.imwrite('scratch/panel_4_aligned.png', p4_aligned)

p3 = cv2.imread('scratch/waving_panels/panel_3.png')
p3_aligned = cv2.warpAffine(p3, M, (1024, 1024), borderValue=(255, 255, 255))
cv2.imwrite('scratch/panel_3_aligned.png', p3_aligned)

p5 = cv2.imread('scratch/waving_panels/panel_5.png')
p5_aligned = cv2.warpAffine(p5, M, (1024, 1024), borderValue=(255, 255, 255))
cv2.imwrite('scratch/panel_5_aligned.png', p5_aligned)
print("Saved aligned panels.")
