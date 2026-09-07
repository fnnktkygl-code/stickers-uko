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

# Luminance term l(x,y)
l_map = (2 * mu1_mu2 + C1) / (mu1_sq + mu2_sq + C1)
# Contrast-structure term cs(x,y)
cs_map = (2 * sigma12 + C2) / (sigma1_sq + sigma2_sq + C2)
ssim_map = l_map * cs_map

l_full = np.pad(l_map, 5, mode='edge')
cs_full = np.pad(cs_map, 5, mode='edge')
ssim_full = np.pad(ssim_map, 5, mode='edge')

print("OVERALL FOREGROUND:")
print(f"  Mean l (luminance term): {l_full[inter].mean():.4f}")
print(f"  Mean cs (contrast/structure term): {cs_full[inter].mean():.4f}")
print(f"  Mean SSIM: {ssim_full[inter].mean():.4f}")

zones = {
    "Head Upper (40-130, 150-360)": (slice(40, 130), slice(150, 360)),
    "Chest & Belly (210-440, 160-350)": (slice(210, 440), slice(160, 350)),
    "Left Flank (180-440, 80-180)": (slice(180, 440), slice(80, 180)),
    "Right Flank (180-440, 330-430)": (slice(180, 440), slice(330, 430)),
    "Left Eye (120-200, 150-240)": (slice(120, 200), slice(150, 240)),
    "Right Eye (120-200, 270-355)": (slice(120, 200), slice(270, 355)),
    "Beak (160-230, 240-270)": (slice(160, 230), slice(240, 270)),
    "Feet (440-500, 150-360)": (slice(440, 500), slice(150, 360)),
}

print("\nPER ZONE BREAKDOWN (SSIM = l * cs):")
for name, (ys, xs) in zones.items():
    z_inter = inter[ys, xs]
    if z_inter.sum() > 0:
        zl = l_full[ys, xs][z_inter].mean()
        zcs = cs_full[ys, xs][z_inter].mean()
        zssim = ssim_full[ys, xs][z_inter].mean()
        print(f"{name:35s}: SSIM={zssim*100:5.2f}% | l={zl*100:5.2f}% | cs={zcs*100:5.2f}%")

