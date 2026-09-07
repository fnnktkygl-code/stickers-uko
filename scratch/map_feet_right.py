import cv2
import numpy as np
from PIL import Image

ref = np.array(Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA"))
vec = np.array(Image.open("scratch/temp_svg_rendered.png").convert("RGBA"))

crop_r = ref[445:492, 275:355, :3]
crop_vr = vec[445:492, 275:355, :3]

lums_r = 0.299 * crop_r[:, :, 0] + 0.587 * crop_r[:, :, 1] + 0.114 * crop_r[:, :, 2]
vlums_r = 0.299 * crop_vr[:, :, 0] + 0.587 * crop_vr[:, :, 1] + 0.114 * crop_vr[:, :, 2]

print("Reference Right Foot Luminance Map:")
for y in range(0, 47, 2):
    row = ""
    for x in range(0, 80, 2):
        l = lums_r[y, x]
        if l > 120:
            row += "##"
        elif l > 80:
            row += "++"
        elif l > 45:
            row += ".."
        else:
            row += "  "
    print(f"{445+y:3d} | {row}")

print("\nVector Right Foot Luminance Map:")
for y in range(0, 47, 2):
    row = ""
    for x in range(0, 80, 2):
        l = vlums_r[y, x]
        if l > 120:
            row += "##"
        elif l > 80:
            row += "++"
        elif l > 45:
            row += ".."
        else:
            row += "  "
    print(f"{445+y:3d} | {row}")
