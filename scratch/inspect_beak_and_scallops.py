from PIL import Image
import numpy as np

img = Image.open("mascots/owluko/owluko_user_master_ref.png").convert("RGBA")
arr = np.array(img)

# Beak alone
crop_bk = arr[370:480, 450:570]
mask_bk = (crop_bk[:, :, 0] > 180) & (crop_bk[:, :, 1] > 80) & (crop_bk[:, :, 1] < 170) & (crop_bk[:, :, 2] < 70)
y_b, x_b = np.where(mask_bk)
if len(x_b) > 0:
    print(f"Beak alone: x=[{450 + x_b.min()}, {450 + x_b.max()}], y=[{370 + y_b.min()}, {370 + y_b.max()}], center=({450 + x_b.mean():.1f}, {370 + y_b.mean():.1f})")

# Let's find mouth opening inside beak
mask_mouth = (crop_bk[:, :, 0] > 120) & (crop_bk[:, :, 0] < 200) & (crop_bk[:, :, 1] < 60) & (crop_bk[:, :, 2] < 60)
y_m, x_m = np.where(mask_mouth)
if len(x_m) > 0:
    print(f"Mouth opening: x=[{450 + x_m.min()}, {450 + x_m.max()}], y=[{370 + y_m.min()}, {370 + y_m.max()}], center=({450 + x_m.mean():.1f}, {370 + y_m.mean():.1f})")

# Left foot vs right foot
crop_ft = arr[830:880, 340:680]
mask_ft = (crop_ft[:, :, 0] > 180) & (crop_ft[:, :, 1] > 80) & (crop_ft[:, :, 2] < 70)
y_f, x_f = np.where(mask_ft)
x_f_glob = 340 + x_f
l_foot = x_f_glob[x_f_glob < 512]
r_foot = x_f_glob[x_f_glob > 512]
print(f"Left foot x: [{l_foot.min()}, {l_foot.max()}], center={l_foot.mean():.1f}")
print(f"Right foot x: [{r_foot.min()}, {r_foot.max()}], center={r_foot.mean():.1f}")

# Left wing edge and right wing edge
# Body width at various Y levels
for y_level in [200, 300, 400, 500, 600, 700, 800]:
    row = arr[y_level, :, 3]
    x_in = np.where(row > 100)[0]
    if len(x_in) > 0:
        print(f"Body at Y={y_level}: x=[{x_in.min()}, {x_in.max()}], width={x_in.max() - x_in.min()}")

