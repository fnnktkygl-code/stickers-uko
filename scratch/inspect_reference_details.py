from PIL import Image
import numpy as np

img = Image.open("mascots/owluko/owluko_user_master_ref.png").convert("RGBA")
arr = np.array(img)

# Let's inspect key regions
# 1. Beak center and bounds
# Beak is orange: high R, medium G, low B
mask_beak = (arr[:, :, 0] > 180) & (arr[:, :, 1] > 80) & (arr[:, :, 1] < 170) & (arr[:, :, 2] < 70)
y_beak, x_beak = np.where(mask_beak)
if len(x_beak) > 0:
    print(f"Beak bounds: x=[{x_beak.min()}, {x_beak.max()}], y=[{y_beak.min()}, {y_beak.max()}], center=({x_beak.mean():.1f}, {y_beak.mean():.1f})")

# 2. Left eye (iris/pupil)
# Left eye pupil is dark: R<50, G<40, B<30 around x in [300, 480], y in [280, 440]
crop_le = arr[280:440, 300:480]
mask_le_dark = (crop_le[:, :, 0] < 50) & (crop_le[:, :, 1] < 40) & (crop_le[:, :, 2] < 30) & (crop_le[:, :, 3] > 200)
y_le, x_le = np.where(mask_le_dark)
if len(x_le) > 0:
    print(f"Left Eye Pupil: x=[{300 + x_le.min()}, {300 + x_le.max()}], y=[{280 + y_le.min()}, {280 + y_le.max()}], center=({300 + x_le.mean():.1f}, {280 + y_le.mean():.1f})")

# Left Eye Iris amber
mask_iris = (crop_le[:, :, 0] > 160) & (crop_le[:, :, 1] > 100) & (crop_le[:, :, 2] < 80)
y_ir, x_ir = np.where(mask_iris)
if len(x_ir) > 0:
    print(f"Left Eye Iris outer bounds: x=[{300 + x_ir.min()}, {300 + x_ir.max()}], y=[{280 + y_ir.min()}, {280 + y_ir.max()}], center=({300 + x_ir.mean():.1f}, {280 + y_ir.mean():.1f})")

# 3. Right Eye Wink
crop_re = arr[320:420, 560:720]
mask_wink = (crop_re[:, :, 0] < 120) & (crop_re[:, :, 1] < 90) & (crop_re[:, :, 2] < 80) & (crop_re[:, :, 3] > 200)
y_wk, x_wk = np.where(mask_wink)
if len(x_wk) > 0:
    print(f"Right Eye Wink: x=[{560 + x_wk.min()}, {560 + x_wk.max()}], y=[{320 + y_wk.min()}, {320 + y_wk.max()}], center=({560 + x_wk.mean():.1f}, {320 + y_wk.mean():.1f})")

# 4. Feet
crop_feet = arr[800:900, 300:720]
mask_feet = (crop_feet[:, :, 0] > 180) & (crop_feet[:, :, 1] > 90) & (crop_feet[:, :, 1] < 180) & (crop_feet[:, :, 2] < 80)
y_ft, x_ft = np.where(mask_feet)
if len(x_ft) > 0:
    print(f"Feet overall: x=[{300 + x_ft.min()}, {300 + x_ft.max()}], y=[{800 + y_ft.min()}, {800 + y_ft.max()}], center=({300 + x_ft.mean():.1f}, {800 + y_ft.mean():.1f})")

