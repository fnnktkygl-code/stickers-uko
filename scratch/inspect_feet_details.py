import numpy as np
from PIL import Image

ref = np.array(Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA"))
# Let's inspect Left Foot at crevice 1 (x=180), toe 2 crest (x=195), crevice 2 (x=206) across Y in 450:490
print("Left Foot: x=180 (crevice 1), x=195 (toe 2 crest), x=206 (crevice 2):")
for y in range(455, 490, 5):
    print(f"y={y}: crevice1={ref[y, 180, :3].tolist()}, toe2={ref[y, 195, :3].tolist()}, crevice2={ref[y, 206, :3].tolist()}")

print("\nRight Foot: x=304 (crevice 1), x=318 (toe 2 crest), x=330 (crevice 2):")
for y in range(455, 490, 5):
    print(f"y={y}: crevice1={ref[y, 304, :3].tolist()}, toe2={ref[y, 318, :3].tolist()}, crevice2={ref[y, 330, :3].tolist()}")
