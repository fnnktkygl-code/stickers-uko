from PIL import Image
import numpy as np

img = Image.open("mascots/owluko/owluko_user_master_ref.png").convert("RGB")
arr = np.array(img)

# In chest area y in [580, 740], x in [340, 684]
# Scallop shadows are darker than background
crop = arr[580:740, 340:684]
# Let's find local minima in brightness (shadow lines)
bg_color = arr[580, 512].astype(float)
diff_from_bg = np.linalg.norm(crop.astype(float) - bg_color, axis=2)

# Print centers of the 5 scallops
print("Scallop 1 (top left):", 340 + 55, 580 + 40)
print("Scallop 2 (top mid):", 340 + 172, 580 + 60)
print("Scallop 3 (top right):", 340 + 290, 580 + 40)
print("Scallop 4 (bot left):", 340 + 110, 580 + 115)
print("Scallop 5 (bot right):", 340 + 235, 580 + 115)

