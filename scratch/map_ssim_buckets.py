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

# Let's save a colored SSIM map
# Green: > 0.85, Yellow: 0.70 - 0.85, Orange: 0.50 - 0.70, Red: < 0.50
vis = np.zeros((512, 512, 3), dtype=np.uint8)
vis[ssim_full >= 0.85] = [40, 200, 40]   # Bright green
vis[(ssim_full >= 0.70) & (ssim_full < 0.85)] = [220, 220, 40] # Yellow
vis[(ssim_full >= 0.50) & (ssim_full < 0.70)] = [240, 140, 30] # Orange
vis[ssim_full < 0.50] = [230, 40, 40]   # Red
vis[~inter] = [20, 20, 20] # Background

cv2.imwrite("scratch/ssim_zones_colored.png", cv2.cvtColor(vis, cv2.COLOR_RGB2BGR))
print("Saved scratch/ssim_zones_colored.png")

# Print percentage of pixels in each bucket
total_inter = inter.sum()
print(f"Total foreground pixels: {total_inter}")
print(f"SSIM >= 0.90: {((ssim_full >= 0.90) & inter).sum() / total_inter * 100:.2f}%")
print(f"SSIM 0.85 - 0.90: {(((ssim_full >= 0.85) & (ssim_full < 0.90)) & inter).sum() / total_inter * 100:.2f}%")
print(f"SSIM 0.75 - 0.85: {(((ssim_full >= 0.75) & (ssim_full < 0.85)) & inter).sum() / total_inter * 100:.2f}%")
print(f"SSIM 0.60 - 0.75: {(((ssim_full >= 0.60) & (ssim_full < 0.75)) & inter).sum() / total_inter * 100:.2f}%")
print(f"SSIM < 0.60: {((ssim_full < 0.60) & inter).sum() / total_inter * 100:.2f}%")
