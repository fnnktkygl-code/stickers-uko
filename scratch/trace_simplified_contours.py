from PIL import Image
import numpy as np

img = Image.open("mascots/owluko/owluko_simplified_master_ref.png").convert("RGB")
arr = np.array(img)

# 1. Mask contour: where mask meets brow/forehead and cheeks
# Facial mask is lighter than the forehead above:
# Forehead at y=180: (247, 240, 220)
# Mask peak at y=215: (251, 247, 236)
print("Forehead dip between brows:", arr[280:300, 510:515, 0].mean())
print("Left brow peak y:", arr[210:230, 380:390, 0].mean())
print("Right brow peak y:", arr[210:230, 635:645, 0].mean())
print("Mask bottom notch under beak:", arr[430:450, 510:515, 0].mean())

# 2. Belly contour
# Belly is lighter than flanks:
print("Belly top notch:", arr[500:520, 510:515, 0].mean())
print("Belly left lobe:", arr[475:495, 390:410, 0].mean())
print("Belly right lobe:", arr[475:495, 615:635, 0].mean())

