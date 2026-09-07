import cv2
import numpy as np
import subprocess
import os
import re

# Load ref
ref = np.array(cv2.imread("mascots/owluko/owluko_master_exact_512.png", cv2.IMREAD_UNCHANGED))
ref_gray = cv2.cvtColor(ref[:, :, :3], cv2.COLOR_BGR2GRAY).astype(np.float64)

# Eye region crops
ys_l, xs_l = slice(125, 195), slice(155, 240)
ys_r, xs_r = slice(125, 195), slice(270, 355)

ref_l_gray = ref_gray[ys_l, xs_l]
ref_r_gray = ref_gray[ys_r, xs_r]

def compute_ssim(img1, img2):
    C1 = (0.01 * 255)**2
    C2 = (0.03 * 255)**2
    kernel = cv2.getGaussianKernel(11, 1.5)
    window = np.outer(kernel, kernel.transpose())
    mu1 = cv2.filter2D(img1, -1, window)[5:-5, 5:-5]
    mu2 = cv2.filter2D(img2, -1, window)[5:-5, 5:-5]
    mu1_sq = mu1**2
    mu2_sq = mu2**2
    mu1_mu2 = mu1 * mu2
    sigma1_sq = cv2.filter2D(img1**2, -1, window)[5:-5, 5:-5] - mu1_sq
    sigma2_sq = cv2.filter2D(img2**2, -1, window)[5:-5, 5:-5] - mu2_sq
    sigma12 = cv2.filter2D(img1 * img2, -1, window)[5:-5, 5:-5] - mu1_mu2
    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))
    return ssim_map.mean()

with open("scratch/test_rwing_fix.svg") as f:
    template_svg = f.read()

# Let's test the baseline first
cmd = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "--headless", "--disable-gpu", "--screenshot=scratch/temp_eye_test.png",
    "--window-size=512,512", "--default-background-color=00000000",
    f"file://{os.path.abspath('scratch/test_rwing_fix.svg')}"
]
subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
vec = cv2.imread("scratch/temp_eye_test.png", cv2.IMREAD_UNCHANGED)
vec_gray = cv2.cvtColor(vec[:, :, :3], cv2.COLOR_BGR2GRAY).astype(np.float64)

base_l_ssim = compute_ssim(ref_l_gray, vec_gray[ys_l, xs_l])
base_r_ssim = compute_ssim(ref_r_gray, vec_gray[ys_r, xs_r])
print(f"BASELINE: Left Eye SSIM = {base_l_ssim*100:.2f}%, Right Eye SSIM = {base_r_ssim*100:.2f}%")
