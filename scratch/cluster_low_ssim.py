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

low_mask = (ssim_full < 0.60) & inter

# Find connected components of low SSIM pixels
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(low_mask.astype(np.uint8))

print(f"Number of low-SSIM clusters: {num_labels - 1}")
# Sort by area descending
clusters = []
for i in range(1, num_labels):
    area = stats[i, cv2.CC_STAT_AREA]
    if area > 100:
        clusters.append((area, i, stats[i], centroids[i]))

clusters.sort(reverse=True)
print(f"Top low-SSIM clusters (area > 100):")
for area, i, stat, (cx, cy) in clusters:
    x = stat[cv2.CC_STAT_LEFT]
    y = stat[cv2.CC_STAT_TOP]
    w = stat[cv2.CC_STAT_WIDTH]
    h = stat[cv2.CC_STAT_HEIGHT]
    mean_s = ssim_full[labels == i].mean()
    print(f"Cluster at ({cx:.1f}, {cy:.1f}), bbox=[X: {x}-{x+w}, Y: {y}-{y+h}], area={area:5d} px, mean SSIM={mean_s*100:4.1f}%")
