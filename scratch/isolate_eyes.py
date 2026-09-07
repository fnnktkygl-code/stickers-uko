import sys
sys.path.append(".")
import cv2, numpy as np
from PIL import Image
from scripts.benchmark_owluko_fidelity import compute_ssim_numpy

ref = np.array(Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA"))
vec = np.array(Image.open("scratch/test_rwing_fix.png").convert("RGBA"))

# Left eye box: Y in [135, 185], X in [165, 225]
r_box = ref[135:185, 165:225, :3]
v_box = vec[135:185, 165:225, :3]

r_gray = cv2.cvtColor(r_box, cv2.COLOR_RGB2GRAY).astype(float)
v_gray = cv2.cvtColor(v_box, cv2.COLOR_RGB2GRAY).astype(float)

# Compare luminance, contrast, structure
C1 = (0.01 * 255)**2
C2 = (0.03 * 255)**2
kernel = cv2.getGaussianKernel(11, 1.5)
window = np.outer(kernel, kernel.transpose())

mu1 = cv2.filter2D(r_gray, -1, window)[5:-5, 5:-5]
mu2 = cv2.filter2D(v_gray, -1, window)[5:-5, 5:-5]
mu1_sq = mu1**2
mu2_sq = mu2**2
mu1_mu2 = mu1 * mu2
sigma1_sq = cv2.filter2D(r_gray**2, -1, window)[5:-5, 5:-5] - mu1_sq
sigma2_sq = cv2.filter2D(v_gray**2, -1, window)[5:-5, 5:-5] - mu2_sq
sigma12 = cv2.filter2D(r_gray * v_gray, -1, window)[5:-5, 5:-5] - mu1_mu2

l_term = (2 * mu1_mu2 + C1) / (mu1_sq + mu2_sq + C1)
s1 = np.sqrt(np.maximum(0, sigma1_sq))
s2 = np.sqrt(np.maximum(0, sigma2_sq))
c_term = (2 * s1 * s2 + C2) / (sigma1_sq + sigma2_sq + C2)
st_term = (sigma12 + C2/2) / (s1 * s2 + C2/2)
ssim = l_term * c_term * st_term

print(f"Left eye crop SSIM: {ssim.mean()*100:.2f}%")
print(f"  Lum term:  {l_term.mean()*100:.2f}%")
print(f"  Cont term: {c_term.mean()*100:.2f}%")
print(f"  Struc term:{st_term.mean()*100:.2f}%")

# Same for right eye: [135:185, 280:340]
r_box2 = ref[135:185, 280:340, :3]
v_box2 = vec[135:185, 280:340, :3]
r_gray2 = cv2.cvtColor(r_box2, cv2.COLOR_RGB2GRAY).astype(float)
v_gray2 = cv2.cvtColor(v_box2, cv2.COLOR_RGB2GRAY).astype(float)
mu1_2 = cv2.filter2D(r_gray2, -1, window)[5:-5, 5:-5]
mu2_2 = cv2.filter2D(v_gray2, -1, window)[5:-5, 5:-5]
mu1_sq2 = mu1_2**2
mu2_sq2 = mu2_2**2
mu1_mu2_2 = mu1_2 * mu2_2
sigma1_sq2 = cv2.filter2D(r_gray2**2, -1, window)[5:-5, 5:-5] - mu1_sq2
sigma2_sq2 = cv2.filter2D(v_gray2**2, -1, window)[5:-5, 5:-5] - mu2_sq2
sigma12_2 = cv2.filter2D(r_gray2 * v_gray2, -1, window)[5:-5, 5:-5] - mu1_mu2_2
l_term2 = (2 * mu1_mu2_2 + C1) / (mu1_sq2 + mu2_sq2 + C1)
s1_2 = np.sqrt(np.maximum(0, sigma1_sq2))
s2_2 = np.sqrt(np.maximum(0, sigma2_sq2))
c_term2 = (2 * s1_2 * s2_2 + C2) / (sigma1_sq2 + sigma2_sq2 + C2)
st_term2 = (sigma12_2 + C2/2) / (s1_2 * s2_2 + C2/2)
ssim2 = l_term2 * c_term2 * st_term2

print(f"\nRight eye crop SSIM: {ssim2.mean()*100:.2f}%")
print(f"  Lum term:  {l_term2.mean()*100:.2f}%")
print(f"  Cont term: {c_term2.mean()*100:.2f}%")
print(f"  Struc term:{st_term2.mean()*100:.2f}%")
