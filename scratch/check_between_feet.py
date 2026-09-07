import numpy as np
from PIL import Image

ref = np.array(Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA"))
vec = np.array(Image.open("scratch/temp_svg_rendered.png").convert("RGBA"))

print("Reference alpha between feet (X: 225-285, Y: 435-495):")
ref_crop = ref[435:495, 225:285, 3] > 20
vec_crop = vec[435:495, 225:285, 3] > 20

for y in range(0, 60, 2):
    r_row = "".join(["#" if ref_crop[y, x] else "." for x in range(0, 60, 2)])
    v_row = "".join(["#" if vec_crop[y, x] else "." for x in range(0, 60, 2)])
    print(f"{435+y:3d} | Ref: {r_row}  | Vec: {v_row}")

