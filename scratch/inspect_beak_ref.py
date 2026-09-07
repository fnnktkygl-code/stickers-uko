import numpy as np
from PIL import Image

ref = np.array(Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA"))
# Let's inspect rows 170 to 212 of beak, columns 245 to 267
crop_b = ref[170:212, 244:268, :3]
print("Beak vertical profile at center (x=255):")
for y in range(170, 212, 2):
    print(f"y={y}: RGB={ref[y, 255, :3].tolist()}")

print("\nBeak horizontal profile at y=190 (mid-beak):")
for x in range(244, 268, 2):
    print(f"x={x}: RGB={ref[190, x, :3].tolist()}")

print("\nBeak horizontal profile at y=204 (near tip):")
for x in range(248, 264, 2):
    print(f"x={x}: RGB={ref[204, x, :3].tolist()}")
