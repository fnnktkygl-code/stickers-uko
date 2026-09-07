from PIL import Image
import numpy as np

img = Image.open("mascots/owluko/owluko_user_master_ref.png").convert("RGB")
arr = np.array(img)

# Mascot pixels are < 248 in any channel
mask = (arr[:, :, 0] < 248) | (arr[:, :, 1] < 248) | (arr[:, :, 2] < 248)
y_m, x_m = np.where(mask)
print(f"Clean mascot bounds: x=[{x_m.min()}, {x_m.max()}], y=[{y_m.min()}, {y_m.max()}]")
print(f"Width = {x_m.max() - x_m.min() + 1}, Height = {y_m.max() - y_m.min() + 1}")
print(f"Center = ({(x_m.min()+x_m.max())/2:.1f}, {(y_m.min()+y_m.max())/2:.1f})")

print("\nContour slice every 30px Y:")
for y in range(y_m.min(), y_m.max() + 1, 30):
    row = np.where(mask[y, :])[0]
    if len(row) > 0:
        print(f"Y={y:3d}: x_min={row.min():3d}, x_max={row.max():3d}, width={row.max()-row.min()+1:3d}, cx={(row.min()+row.max())/2:.1f}")

