import cv2
import numpy as np
from PIL import Image

ref = np.array(Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA"))

# Look at 2D slice around beak: Y in [165, 215], X in [245, 267]
crop_b = ref[165:215, 245:267, :3]
# Print out an ASCII map of luminance or hue
for y in range(crop_b.shape[0]):
    row = ""
    for x in range(crop_b.shape[1]):
        r, g, b = crop_b[y, x]
        # Beak in 3D is brownish-orange, distinct from surrounding white/cream porcelain
        # Chest porcelain is bright cream (e.g. > 200, 190, 180)
        # Beak is darker (e.g. 170, 140, 120)
        if r < 185 and g < 165:
            row += "##"
        elif r < 205 and g < 185:
            row += ".."
        else:
            row += "  "
    print(f"{165+y:3d} | {row}")
