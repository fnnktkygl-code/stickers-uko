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

ys, xs = slice(440, 500), slice(150, 360)
f_ssim = ssim_full[ys, xs]
f_inter = inter[ys, xs]
f_ref = ref[ys, xs]
f_vec = vec[ys, xs]

print("Mean SSIM in feet intersection:", f_ssim[f_inter].mean())

# Print out a map of low SSIM pixels in feet
for y in range(0, 60, 2):
    row = ""
    for x in range(0, 210, 4):
        if not f_inter[y, x]:
            row += "  "
        elif f_ssim[y, x] < 0.4:
            row += "XX"
        elif f_ssim[y, x] < 0.7:
            row += ".."
        else:
            row += "##"
    print(f"{440+y:3d} | {row}")
