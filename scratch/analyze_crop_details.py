import cv2
import numpy as np
from PIL import Image

ref = np.array(Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA"))
vec = np.array(Image.open("scratch/temp_svg_rendered.png").convert("RGBA"))

print("=== LEFT EYE (130:190, 160:235) ===")
crop = ref[130:190, 160:235, :3]
# find min and max values
print(f"Ref Left eye shape: {crop.shape}")
# Find center of dark pupil
gray = cv2.cvtColor(crop, cv2.COLOR_RGB2GRAY)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gray)
print(f"Pupil min gray: {min_val} at relative loc (x,y)={min_loc}, absolute ({160+min_loc[0]}, {130+min_loc[1]})")
# Let's find threshold of eye socket
# Where is iris?
# In 3D CGI, amber is high in Red, moderate in Green, low in Blue: (R > 100, B < 50)
amber_mask = (crop[:, :, 0] > 100) & (crop[:, :, 1] > 50) & (crop[:, :, 2] < 60)
ys, xs = np.where(amber_mask)
if len(ys) > 0:
    print(f"Ref Left Amber Iris bounds: X=[{160+xs.min()}, {160+xs.max()}], Y=[{130+ys.min()}, {130+ys.max()}], center=({160+(xs.min()+xs.max())/2:.1f}, {130+(ys.min()+ys.max())/2:.1f})")

print("\n=== RIGHT EYE (130:190, 280:345) ===")
crop_r = ref[130:190, 280:345, :3]
gray_r = cv2.cvtColor(crop_r, cv2.COLOR_RGB2GRAY)
min_val_r, max_val_r, min_loc_r, max_loc_r = cv2.minMaxLoc(gray_r)
print(f"Pupil min gray: {min_val_r} at relative loc (x,y)={min_loc_r}, absolute ({280+min_loc_r[0]}, {130+min_loc_r[1]})")
amber_mask_r = (crop_r[:, :, 0] > 80) & (crop_r[:, :, 1] > 40) & (crop_r[:, :, 2] < 50)
ys_r, xs_r = np.where(amber_mask_r)
if len(ys_r) > 0:
    print(f"Ref Right Amber Iris bounds: X=[{280+xs_r.min()}, {280+xs_r.max()}], Y=[{130+ys_r.min()}, {130+ys_r.max()}], center=({280+(xs_r.min()+xs_r.max())/2:.1f}, {130+(ys_r.min()+ys_r.max())/2:.1f})")

print("\n=== BEAK (160:230, 240:272) ===")
crop_b = ref[160:230, 240:272, :3]
# Beak is distinct color or luminance
# Let's print colors at center column
mid_x = 256 - 240
for y in range(0, 70, 5):
    print(f"y={160+y}, ref_rgb={crop_b[y, mid_x].tolist()}, vec_rgb={vec[160+y, 256, :3].tolist()}")

print("\n=== FEET (440:495, 150:360) ===")
# Let's inspect foot rows
crop_fl = ref[445:495, 155:240, :3]
vec_fl = vec[445:495, 155:240, :3]
print(f"Left foot ref mean RGB: {crop_fl.mean(axis=(0,1))}, vec mean RGB: {vec_fl.mean(axis=(0,1))}")
crop_fr = ref[445:495, 275:360, :3]
vec_fr = vec[445:495, 275:360, :3]
print(f"Right foot ref mean RGB: {crop_fr.mean(axis=(0,1))}, vec mean RGB: {vec_fr.mean(axis=(0,1))}")

