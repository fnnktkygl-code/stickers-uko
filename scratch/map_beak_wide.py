import cv2
import numpy as np
from PIL import Image

ref = np.array(Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA"))
# Let's search X in [235, 280], Y in [165, 220]
crop_b = ref[165:220, 235:285, :3]
for y in range(crop_b.shape[0]):
    row = ""
    for x in range(crop_b.shape[1]):
        r, g, b = crop_b[y, x]
        # In LAB or RGB: beak is amber/brown. R > G > B, with R in [140, 210], G in [120, 180], B in [90, 150].
        # Meanwhile surrounding face is cream porcelain: R ~ 220+, G ~ 210+, B ~ 200+.
        # So diff (R - B) or luminance (0.3R + 0.59G + 0.11B)
        lum = 0.299 * r + 0.587 * g + 0.114 * b
        if lum < 165:
            row += "##"
        elif lum < 190:
            row += ".."
        else:
            row += "  "
    print(f"{165+y:3d} | {row}")
