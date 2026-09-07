import cv2
import numpy as np
from PIL import Image

ref = np.array(Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA"))
vec = np.array(Image.open("scratch/temp_svg_rendered.png").convert("RGBA"))

# Let's inspect Left Foot (Y: 445-492, X: 155-235)
crop_l = ref[445:492, 155:235, :3]
crop_vl = vec[445:492, 155:235, :3]

print("=== LEFT FOOT PROFILE ===")
# Let's print out the toe highlights and crevice positions in the reference
# In reference, let's find Y of highest luminance in each toe column
lums = 0.299 * crop_l[:, :, 0] + 0.587 * crop_l[:, :, 1] + 0.114 * crop_l[:, :, 2]
vlums = 0.299 * crop_vl[:, :, 0] + 0.587 * crop_vl[:, :, 1] + 0.114 * crop_vl[:, :, 2]

# Let's see an ASCII visualization of left foot reference
print("Reference Left Foot Luminance Map:")
for y in range(0, 47, 2):
    row = ""
    for x in range(0, 80, 2):
        l = lums[y, x]
        if l > 140:
            row += "##"
        elif l > 100:
            row += "++"
        elif l > 60:
            row += ".."
        else:
            row += "  "
    print(f"{445+y:3d} | {row}")

print("\nVector Left Foot Luminance Map:")
for y in range(0, 47, 2):
    row = ""
    for x in range(0, 80, 2):
        l = vlums[y, x]
        if l > 140:
            row += "##"
        elif l > 100:
            row += "++"
        elif l > 60:
            row += ".."
        else:
            row += "  "
    print(f"{445+y:3d} | {row}")

