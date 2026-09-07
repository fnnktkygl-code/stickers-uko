import cv2
import numpy as np

# Scale factor: 220.0 / 58.0 = 3.7931
scale = 220.0 / 58.0
# In panel 1: eye midpoint is ((142+200)/2, (93+92)/2) = (171.0, 92.5)
# In master 1024x1024: eye midpoint is ((402+622)/2, (355+355)/2) = (512.0, 355.0)
tx = 512.0 - 171.0 * scale
ty = 355.0 - 92.5 * scale

M = np.float32([[scale, 0, tx], [0, scale, ty]])

for i in [2, 3, 4, 5]:
    p = cv2.imread(f'scratch/waving_panels/panel_{i}.png')
    warped = cv2.warpAffine(p, M, (1024, 1024), borderValue=(255, 255, 255))
    cv2.imwrite(f'scratch/panel_{i}_warped.png', warped)
    print(f"Warped panel {i} saved.")

# In panel 4 warped, let's extract the waving wing contour
p4_w = cv2.imread('scratch/panel_4_warped.png')
# Wing is in x > 650
# Let's visualize where the wing is
wing_mask = np.zeros((1024, 1024), dtype=np.uint8)
gray = cv2.cvtColor(p4_w, cv2.COLOR_BGR2GRAY)
wing_mask[(gray < 250) & (np.arange(1024)[None, :] > 680)] = 255
cv2.imwrite('scratch/wing_mask_warped.png', wing_mask)
print("Saved wing mask.")
