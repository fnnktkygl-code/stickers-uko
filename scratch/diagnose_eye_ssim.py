import cv2
import numpy as np
from PIL import Image

ref_img = Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA")
vec_img = Image.open("scratch/test_direct_render.png").convert("RGBA") # the 82.40% baseline

ref = np.array(ref_img)
vec = np.array(vec_img)

# Let's compute ssim map
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

# Left eye crop
le_ref = ref[130:190, 160:235]
le_vec = vec[130:190, 160:235]
le_ssim = ssim_full[130:190, 160:235]

print("Left eye baseline mean SSIM:", le_ssim.mean())
# Find worst SSIM pixels in left eye
ys, xs = np.where(le_ssim < 0.5)
print(f"Number of pixels with SSIM < 0.5 in left eye: {len(ys)} / {le_ssim.size}")
# Where are these low-ssim pixels?
print(f"Low SSIM Y range: [{130+ys.min()}, {130+ys.max()}], X range: [{160+xs.min()}, {160+xs.max()}]")
# Print a few samples of ref vs vec in that low SSIM region:
for i in range(0, len(ys), max(1, len(ys)//10)):
    y, x = ys[i], xs[i]
    print(f"At ({160+x}, {130+y}): ref={le_ref[y, x, :3].tolist()}, vec={le_vec[y, x, :3].tolist()}, ssim={le_ssim[y, x]:.3f}")

