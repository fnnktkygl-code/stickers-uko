import cv2
import numpy as np
from PIL import Image

ref_img = Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA")
vec_img = Image.open("scratch/test_eye_v3.png").convert("RGBA")

ref = np.array(ref_img)
vec = np.array(vec_img)

crop_r = ref[430:490, 275:355]
crop_v = vec[430:490, 275:355]

diff = crop_v[:, :, :3].astype(float) - crop_r[:, :, :3].astype(float)
print(f"Right Foot: mean diff (vec - ref): R={diff[:,:,0].mean():.1f}, G={diff[:,:,1].mean():.1f}, B={diff[:,:,2].mean():.1f}")
print(f"Right Foot: mean abs diff: {np.abs(diff).mean():.1f}")

# Compare row by row average luminance in right foot
ref_lum = 0.299 * crop_r[:,:,0] + 0.587 * crop_r[:,:,1] + 0.114 * crop_r[:,:,2]
vec_lum = 0.299 * crop_v[:,:,0] + 0.587 * crop_v[:,:,1] + 0.114 * crop_v[:,:,2]

print("Right foot row lum (Ref vs Vec):")
for y in range(0, 60, 5):
    mask = crop_r[y, :, 3] > 20
    if mask.sum() > 0:
        print(f"y={430+y}: Ref lum={ref_lum[y][mask].mean():.1f}, Vec lum={vec_lum[y][mask].mean():.1f}, diff={vec_lum[y][mask].mean() - ref_lum[y][mask].mean():.1f}")

