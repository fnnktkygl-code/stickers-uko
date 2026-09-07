import cv2
import numpy as np
from PIL import Image

ref_img = Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA")
vec_img = Image.open("scratch/test_eye_v3.png").convert("RGBA")

ref = np.array(ref_img)
vec = np.array(vec_img)

# Crop left flank
ref_lf = ref[180:440, 85:180]
vec_lf = vec[180:440, 85:180]

# Compute gradient or Sobel to see the edge/wing in ref
ref_gray = cv2.cvtColor(ref_lf[:, :, :3], cv2.COLOR_RGB2GRAY)
vec_gray = cv2.cvtColor(vec_lf[:, :, :3], cv2.COLOR_RGB2GRAY)

sobel_x_ref = cv2.Sobel(ref_gray, cv2.CV_64F, 1, 0, ksize=3)
sobel_y_ref = cv2.Sobel(ref_gray, cv2.CV_64F, 0, 1, ksize=3)
grad_ref = np.sqrt(sobel_x_ref**2 + sobel_y_ref**2)

sobel_x_vec = cv2.Sobel(vec_gray, cv2.CV_64F, 1, 0, ksize=3)
sobel_y_vec = cv2.Sobel(vec_gray, cv2.CV_64F, 0, 1, ksize=3)
grad_vec = np.sqrt(sobel_x_vec**2 + sobel_y_vec**2)

print(f"Ref Left Flank mean edge gradient: {grad_ref.mean():.2f}")
print(f"Vec Left Flank mean edge gradient: {grad_vec.mean():.2f}")

# Where are the highest gradients in ref?
# Inside the body mask (not the outer silhouette edge)
ref_mask = ref_lf[:, :, 3] > 200
# Erode mask by 5 pixels to exclude outer boundary
kernel = np.ones((9, 9), np.uint8)
inner_mask = cv2.erode(ref_mask.astype(np.uint8), kernel) > 0

print(f"INNER Ref Left Flank mean edge gradient: {grad_ref[inner_mask].mean():.2f}")
print(f"INNER Vec Left Flank mean edge gradient: {grad_vec[inner_mask].mean():.2f}")

# Find where inner ref gradient is significant (> 10)
ys, xs = np.where((grad_ref > 10) & inner_mask)
print(f"Pixels with gradient > 10 inside ref left flank: {len(ys)}")
if len(ys) > 0:
    print(f"Y range: [{180+ys.min()}, {180+ys.max()}], X range: [{85+xs.min()}, {85+xs.max()}]")
