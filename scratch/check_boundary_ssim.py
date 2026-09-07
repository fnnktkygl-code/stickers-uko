import cv2
import numpy as np
from PIL import Image

ref_img = Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA")
vec_img = Image.open("scratch/test_eye_v3.png").convert("RGBA")

ref = np.array(ref_img)
vec = np.array(vec_img)

ref_alpha = ref[:, :, 3] > 20
vec_alpha = vec[:, :, 3] > 20
inter = ref_alpha & vec_alpha

ref_gray = cv2.cvtColor(ref[:, :, :3], cv2.COLOR_RGB2GRAY).astype(np.float64)
vec_gray = cv2.cvtColor(vec[:, :, :3], cv2.COLOR_RGB2GRAY).astype(np.float64)

C1 = (0.01 * 255)**2
C2 = (0.03 * 255)**2
kernel = cv2.getGaussianKernel(11, 1.5)
window = np.outer(kernel, kernel.transpose())

mu1 = cv2.filter2D(ref_gray, -1, window)[5:-5, 5:-5]
mu2 = cv2.filter2D(vec_gray, -1, window)[5:-5, 5:-5]
mu1_sq = mu1**2
mu2_sq = mu2**2
mu1_mu2 = mu1 * mu2
sigma1_sq = cv2.filter2D(ref_gray**2, -1, window)[5:-5, 5:-5] - mu1_sq
sigma2_sq = cv2.filter2D(vec_gray**2, -1, window)[5:-5, 5:-5] - mu2_sq
sigma12 = cv2.filter2D(ref_gray * vec_gray, -1, window)[5:-5, 5:-5] - mu1_mu2

ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))
ssim_full = np.pad(ssim_map, 5, mode='edge')

# Boundary mask: pixels within 5 px of boundary
kernel_dist = np.ones((11, 11), np.uint8)
eroded_inter = cv2.erode(inter.astype(np.uint8), kernel_dist) > 0
boundary_ring = inter & (~eroded_inter)

print(f"Total foreground pixels: {inter.sum()}")
print(f"Boundary ring pixels: {boundary_ring.sum()} ({boundary_ring.sum() / inter.sum() * 100:.2f}%)")
print(f"SSIM on Boundary ring: {ssim_full[boundary_ring].mean() * 100:.2f}%")
print(f"SSIM on INNER body (>5px from edge): {ssim_full[eroded_inter].mean() * 100:.2f}%")

# Save boundary ring and inner SSIM visualization
vis = np.zeros((512, 512, 3), dtype=np.uint8)
vis[boundary_ring] = [255, 0, 0] # Blue boundary ring
vis[eroded_inter] = [0, 255, 0] # Green interior
cv2.imwrite("scratch/boundary_ring.png", vis)
print("Saved scratch/boundary_ring.png")
