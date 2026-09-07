from PIL import Image
import numpy as np

img = Image.open("scratch/simp_crop_le.png").convert("RGB")
arr = np.array(img)

# Center of eye crop is around (80, 80)
# Let us sample a vertical line through the eye from top to bottom
print("Vertical slice through Left Eye (x=80):")
for y in range(10, 150, 10):
    c = arr[y, 80]
    hex_c = "#{:02X}{:02X}{:02X}".format(c[0], c[1], c[2])
    print(f"y={y:3d}: {hex_c} RGB={c}")

print("\nHorizontal slice through Left Eye (y=80):")
for x in range(10, 150, 10):
    c = arr[80, x]
    hex_c = "#{:02X}{:02X}{:02X}".format(c[0], c[1], c[2])
    print(f"x={x:3d}: {hex_c} RGB={c}")

