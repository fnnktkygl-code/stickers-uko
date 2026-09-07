from PIL import Image
import numpy as np

img = Image.open("mascots/owluko/owluko_simplified_master_ref.png").convert("RGBA")
arr = np.array(img)
print("Image size:", img.size)

# 1. Total mascot bounding box (pixels with R<250 or G<250 or B<250)
mask = (arr[:, :, 0] < 250) | (arr[:, :, 1] < 250) | (arr[:, :, 2] < 250)
y_m, x_m = np.where(mask)
print(f"Mascot bounds: x=[{x_m.min()}, {x_m.max()}], y=[{y_m.min()}, {y_m.max()}]")
print(f"Width = {x_m.max() - x_m.min() + 1}, Height = {y_m.max() - y_m.min() + 1}")
print(f"Center = ({(x_m.min()+x_m.max())/2:.1f}, {(y_m.min()+y_m.max())/2:.1f})")

# 2. Beak analysis (orange pixels: high R, med G, low B around center)
crop_beak = arr[350:480, 440:584]
mask_beak = (crop_beak[:, :, 0] > 200) & (crop_beak[:, :, 1] > 100) & (crop_beak[:, :, 1] < 180) & (crop_beak[:, :, 2] < 80)
y_b, x_b = np.where(mask_beak)
if len(x_b) > 0:
    bx_min, bx_max = 440 + x_b.min(), 440 + x_b.max()
    by_min, by_max = 350 + y_b.min(), 350 + y_b.max()
    print(f"Beak: x=[{bx_min}, {bx_max}], y=[{by_min}, {by_max}], size={bx_max-bx_min+1}x{by_max-by_min+1}, center=({(bx_min+bx_max)/2:.1f}, {(by_min+by_max)/2:.1f})")

# 3. Eyes analysis
# Left eye pupil & iris
crop_le = arr[260:440, 300:470]
mask_le_dark = (crop_le[:, :, 0] < 80) & (crop_le[:, :, 1] < 60) & (crop_le[:, :, 2] < 40)
y_lep, x_lep = np.where(mask_le_dark)
if len(x_lep) > 0:
    print(f"Left Pupil: center=({300 + x_lep.mean():.1f}, {260 + y_lep.mean():.1f}), bounds x=[{300+x_lep.min()}, {300+x_lep.max()}], y=[{260+y_lep.min()}, {260+y_lep.max()}]")

# Right eye pupil & iris
crop_re = arr[260:440, 550:720]
mask_rep_dark = (crop_re[:, :, 0] < 80) & (crop_re[:, :, 1] < 60) & (crop_re[:, :, 2] < 40)
y_rep, x_rep = np.where(mask_rep_dark)
if len(x_rep) > 0:
    print(f"Right Pupil: center=({550 + x_rep.mean():.1f}, {260 + y_rep.mean():.1f}), bounds x=[{550+x_rep.min()}, {550+x_rep.max()}], y=[{260+y_rep.min()}, {260+y_rep.max()}]")

# 4. Feet
crop_feet = arr[800:880, 320:704]
mask_ft = (crop_feet[:, :, 0] > 200) & (crop_feet[:, :, 1] > 100) & (crop_feet[:, :, 1] < 180) & (crop_feet[:, :, 2] < 80)
y_ft, x_ft = np.where(mask_ft)
if len(x_ft) > 0:
    x_glob = 320 + x_ft
    l_ft = x_glob[x_glob < 512]
    r_ft = x_glob[x_glob > 512]
    print(f"Left foot x: [{l_ft.min()}, {l_ft.max()}], center={l_ft.mean():.1f}")
    print(f"Right foot x: [{r_ft.min()}, {r_ft.max()}], center={r_ft.mean():.1f}")
    print(f"Feet y: [{800+y_ft.min()}, {800+y_ft.max()}], center={800+y_ft.mean():.1f}")

# 5. Wings bounds
# Left wing width at various Y levels
print("\nProfile slices:")
for y in range(200, 860, 40):
    row = np.where(mask[y, :])[0]
    if len(row) > 0:
        print(f"Y={y:3d}: x=[{row.min():3d}, {row.max():3d}], width={row.max()-row.min()+1:3d}, cx={(row.min()+row.max())/2:.1f}")

