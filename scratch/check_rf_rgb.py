import numpy as np
from PIL import Image

ref = np.array(Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA"))
vec = np.array(Image.open("scratch/temp_svg_rendered.png").convert("RGBA"))

crop_r = ref[445:492, 275:355, :3]
crop_vr = vec[445:492, 275:355, :3]

print(f"Ref R mean={crop_r.mean():.1f}, min={crop_r.min()}, max={crop_r.max()}")
print(f"Vec R mean={crop_vr.mean():.1f}, min={crop_vr.min()}, max={crop_vr.max()}")
print("Ref center pixel (y=470, x=315):", ref[470, 315, :3].tolist())
print("Vec center pixel (y=470, x=315):", vec[470, 315, :3].tolist())
