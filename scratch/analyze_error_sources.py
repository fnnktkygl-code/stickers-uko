import cv2, numpy as np
from PIL import Image
from scripts.benchmark_owluko_fidelity import compute_ssim_numpy

ref = np.array(Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA"))
vec = np.array(Image.open("scratch/test_opt_step.png").convert("RGBA"))

inter = (ref[:, :, 3] > 20) & (vec[:, :, 3] > 20)

ref_gray = cv2.cvtColor(ref[:, :, :3], cv2.COLOR_RGB2GRAY).astype(np.float64)
vec_gray = cv2.cvtColor(vec[:, :, :3], cv2.COLOR_RGB2GRAY).astype(np.float64)

# Decompose SSIM
C1 = (0.01 * 255)**2
C2 = (0.03 * 255)**2
kernel = cv2.getGaussianKernel(11, 1.5)
window = np.outer(kernel, kernel.transpose())
mu1 = cv2.filter2D(ref_gray, -1, window)
mu2 = cv2.filter2D(vec_gray, -1, window)
mu1_sq = mu1**2
mu2_sq = mu2**2
mu1_mu2 = mu1 * mu2
sigma1_sq = cv2.filter2D(ref_gray**2, -1, window) - mu1_sq
sigma2_sq = cv2.filter2D(vec_gray**2, -1, window) - mu2_sq
sigma12 = cv2.filter2D(ref_gray * vec_gray, -1, window) - mu1_mu2

lum_term = (2 * mu1_mu2 + C1) / (mu1_sq + mu2_sq + C1)
sigma1 = np.sqrt(np.maximum(0, sigma1_sq))
sigma2 = np.sqrt(np.maximum(0, sigma2_sq))
contrast_term = (2 * sigma1 * sigma2 + C2) / (sigma1_sq + sigma2_sq + C2)
struct_term = (sigma12 + C2/2) / (sigma1 * sigma2 + C2/2)
ssim = lum_term * contrast_term * struct_term

print(f"Mean SSIM on foreground: {ssim[inter].mean()*100:.2f}%")
print(f"  Luminance term: {lum_term[inter].mean()*100:.2f}%")
print(f"  Contrast term:  {contrast_term[inter].mean()*100:.2f}%")
print(f"  Structure term: {struct_term[inter].mean()*100:.2f}%")

# SSIM by region
print("\nSSIM components by region:")
boxes = {
    "Head (Y < 200)": inter & (np.arange(512)[:, None] < 200),
    "Chest (200 <= Y < 320)": inter & (np.arange(512)[:, None] >= 200) & (np.arange(512)[:, None] < 320),
    "Belly (320 <= Y < 430)": inter & (np.arange(512)[:, None] >= 320) & (np.arange(512)[:, None] < 430),
    "Feet (Y >= 430)": inter & (np.arange(512)[:, None] >= 430),
    "Left Eye [130:180, 165:225]": inter & (np.arange(512)[:, None] >= 130) & (np.arange(512)[:, None] < 180) & (np.arange(512)[None, :] >= 165) & (np.arange(512)[None, :] < 225),
    "Right Eye [130:180, 280:340]": inter & (np.arange(512)[:, None] >= 130) & (np.arange(512)[:, None] < 180) & (np.arange(512)[None, :] >= 280) & (np.arange(512)[None, :] < 340),
    "Beak [165:225, 240:272]": inter & (np.arange(512)[:, None] >= 165) & (np.arange(512)[:, None] < 225) & (np.arange(512)[None, :] >= 240) & (np.arange(512)[None, :] < 272),
}

for name, m in boxes.items():
    print(f"{name:30s} | SSIM: {ssim[m].mean()*100:5.2f}% | Lum: {lum_term[m].mean()*100:5.2f}% | Cont: {contrast_term[m].mean()*100:5.2f}% | Struct: {struct_term[m].mean()*100:5.2f}%")
