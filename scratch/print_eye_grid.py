import numpy as np
from PIL import Image

ref = np.array(Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA"))

# Left Eye center is around (196, 158)
print("=== LEFT EYE RGB GRID (Y: 145-170, X: 185-210) ===")
# Print at step 2
for y in range(145, 172, 3):
    row_str = f"y={y:3d}: "
    for x in range(185, 210, 3):
        r, g, b = ref[y, x, :3]
        row_str += f"[{r:3d},{g:3d},{b:3d}] "
    print(row_str)

print("\n=== RIGHT EYE RGB GRID (Y: 145-170, X: 295-320) ===")
for y in range(145, 172, 3):
    row_str = f"y={y:3d}: "
    for x in range(295, 320, 3):
        r, g, b = ref[y, x, :3]
        row_str += f"[{r:3d},{g:3d},{b:3d}] "
    print(row_str)
