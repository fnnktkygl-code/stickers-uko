import cv2, numpy as np
from PIL import Image

ref = np.array(Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA"))
beak_ref = ref[160:220, 235:275, :3]

# In ref, find the color of beak along center line
center_col = beak_ref[:, 254-235]
print("Beak vertical colors from Y=160 to 220:")
for y_rel in range(0, 60, 5):
    print(f"Y={160+y_rel}: RGB={center_col[y_rel]}")
