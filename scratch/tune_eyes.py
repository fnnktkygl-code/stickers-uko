import sys
sys.path.append(".")
import cv2, numpy as np
from PIL import Image
from scripts.benchmark_owluko_fidelity import compute_ssim_numpy

ref = np.array(Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA"))
ref_gray = cv2.cvtColor(ref[:, :, :3], cv2.COLOR_RGB2GRAY)

# Left eye box: [130:180, 165:225]
# Right eye box: [130:180, 280:340]
l_ref_box = ref_gray[130:180, 165:225]
r_ref_box = ref_gray[130:180, 280:340]

print(f"Left eye crop mean: {l_ref_box.mean():.1f}, min: {l_ref_box.min():.1f}, max: {l_ref_box.max():.1f}")
print(f"Right eye crop mean: {r_ref_box.mean():.1f}, min: {r_ref_box.min():.1f}, max: {r_ref_box.max():.1f}")
