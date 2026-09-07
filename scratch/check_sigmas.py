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

C2 = (0.03 * 255)**2
kernel = cv2.getGaussianKernel(11, 1.5)
window = np.outer(kernel, kernel.transpose())

mu1 = cv2.filter2D(ref_gray, -1, window)[5:-5, 5:-5]
mu2 = cv2.filter2D(vec_gray, -1, window)[5:-5, 5:-5]
sigma1_sq = cv2.filter2D(ref_gray**2, -1, window)[5:-5, 5:-5] - mu1**2
sigma2_sq = cv2.filter2D(vec_gray**2, -1, window)[5:-5, 5:-5] - mu2**2
sigma12 = cv2.filter2D(ref_gray * vec_gray, -1, window)[5:-5, 5:-5] - mu1 * mu2

sigma1_full = np.pad(np.sqrt(np.maximum(0, sigma1_sq)), 5, mode='edge')
sigma2_full = np.pad(np.sqrt(np.maximum(0, sigma2_sq)), 5, mode='edge')

hu_inter = inter[40:130, 150:360]
print("Head Upper (40-130, 150-360):")
print(f"  Ref mean sigma: {sigma1_full[40:130, 150:360][hu_inter].mean():.2f}")
print(f"  Vec mean sigma: {sigma2_full[40:130, 150:360][hu_inter].mean():.2f}")

lf_inter = inter[180:440, 80:180]
print("\nLeft Flank (180-440, 80-180):")
print(f"  Ref mean sigma: {sigma1_full[180:440, 80:180][lf_inter].mean():.2f}")
print(f"  Vec mean sigma: {sigma2_full[180:440, 80:180][lf_inter].mean():.2f}")

