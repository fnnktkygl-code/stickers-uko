import sys
sys.path.append(".")
import cv2, numpy as np
from PIL import Image
from scripts.benchmark_owluko_fidelity import compute_ssim_numpy

ref = np.array(Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA"))
vec = np.array(Image.open("scratch/test_pod_feet.png").convert("RGBA"))
inter = (ref[:, :, 3] > 20) & (vec[:, :, 3] > 20)

ref_gray = cv2.cvtColor(ref[:, :, :3], cv2.COLOR_RGB2GRAY).astype(float)
vec_gray = cv2.cvtColor(vec[:, :, :3], cv2.COLOR_RGB2GRAY).astype(float)

# Residual image
res_gray = ref_gray - vec_gray
res_gray[~inter] = 0

# Low pass filter of residual (macro lighting error)
low_pass = cv2.GaussianBlur(res_gray, (51, 51), 15)

# If we add low_pass to vec_gray, what would SSIM and NCC be?
ideal_gray = np.clip(vec_gray + low_pass, 0, 255)
ideal_ssim = np.pad(compute_ssim_numpy(ref_gray, ideal_gray), 5, mode="edge")[inter].mean()
ideal_ncc = np.corrcoef(ref_gray[inter], ideal_gray[inter])[0, 1]

print(f"Current Grayscale SSIM: {np.pad(compute_ssim_numpy(ref_gray, vec_gray), 5, mode='edge')[inter].mean()*100:.2f}%")
print(f"With macro lighting correction: SSIM={ideal_ssim*100:.2f}%, NCC={ideal_ncc*100:.2f}%")

# What are the dominant components in low_pass?
# Save low_pass visualization
vis = np.clip(low_pass + 128, 0, 255).astype(np.uint8)
vis[~inter] = 128
cv2.imwrite("scratch/macro_lighting_error.png", vis)
print("Saved macro_lighting_error.png.")
