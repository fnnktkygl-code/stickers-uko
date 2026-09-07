import numpy as np
from PIL import Image

ref = np.array(Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA"))
vec = np.array(Image.open("scratch/temp_svg_rendered.png").convert("RGBA"))

ref_a = ref[445:495, 150:360, 3] > 20
vec_a = vec[445:495, 150:360, 3] > 20

inter = ref_a & vec_a
print(f"Ref feet pixels: {ref_a.sum()}, Vec feet pixels: {vec_a.sum()}, Inter: {inter.sum()}")
print(f"IoU of feet region: {inter.sum() / (ref_a | vec_a).sum() * 100:.2f}%")

ref_rgb = ref[445:495, 150:360, :3][inter]
vec_rgb = vec[445:495, 150:360, :3][inter]
print(f"Feet on INTERSECTION: Ref mean={ref_rgb.mean():.1f}, Vec mean={vec_rgb.mean():.1f}")
mse = np.mean((ref_rgb.astype(float) - vec_rgb.astype(float))**2)
print(f"Feet MSE on intersection: {mse:.1f}")
