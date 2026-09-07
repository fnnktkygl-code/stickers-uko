from PIL import Image
import numpy as np

img = Image.open("mascots/owluko/owluko_user_master_ref.png").convert("RGB")
arr = np.array(img)

# Background is white (255, 255, 255)
# Mascot is cream/beige, not pure white
mask_mascot = ~((arr[:, :, 0] > 252) & (arr[:, :, 1] > 252) & (arr[:, :, 2] > 252))

y_m, x_m = np.where(mask_mascot)
print(f"Total mascot bounds: x=[{x_m.min()}, {x_m.max()}], y=[{y_m.min()}, {y_m.max()}]")
print(f"Width = {x_m.max() - x_m.min()}, Height = {y_m.max() - y_m.min()}, Center = ({(x_m.min()+x_m.max())/2:.1f}, {(y_m.min()+y_m.max())/2:.1f})")

for y in range(160, 870, 40):
    row_x = np.where(mask_mascot[y, :])[0]
    if len(row_x) > 0:
        print(f"Y={y}: x=[{row_x.min()}, {row_x.max()}], width={row_x.max() - row_x.min()}, cx={(row_x.min()+row_x.max())/2:.1f}")

