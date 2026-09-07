import cv2
import numpy as np
from PIL import Image

ref = np.array(Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA"))

# Left Eye in ref: Y in [135, 185], X in [165, 228]
crop_l = ref[135:185, 165:228, :3]
# Find bright glints / specular highlights
# Any pixels with R > 230 and G > 230 and B > 230?
glints_l = (crop_l[:, :, 0] > 200) & (crop_l[:, :, 1] > 200) & (crop_l[:, :, 2] > 200)
ys, xs = np.where(glints_l)
if len(ys) > 0:
    print(f"Left eye glint at: X in [{165+xs.min()}, {165+xs.max()}], Y in [{135+ys.min()}, {135+ys.max()}], max RGB={crop_l[ys, xs].max(axis=0)}")
else:
    print("No high specular glint in Left eye (>200)")
    # What is the max luminance inside left eye?
    # In iris:
    gray_l = cv2.cvtColor(crop_l, cv2.COLOR_RGB2GRAY)
    print(f"Left eye crop max gray: {gray_l.max()} at relative ({gray_l.argmax()%crop_l.shape[1]}, {gray_l.argmax()//crop_l.shape[1]})")

# Right Eye in ref: Y in [135, 185], X in [278, 340]
crop_r = ref[135:185, 278:340, :3]
glints_r = (crop_r[:, :, 0] > 200) & (crop_r[:, :, 1] > 200) & (crop_r[:, :, 2] > 200)
ys_r, xs_r = np.where(glints_r)
if len(ys_r) > 0:
    print(f"Right eye glint at: X in [{278+xs_r.min()}, {278+xs_r.max()}], Y in [{135+ys_r.min()}, {135+ys_r.max()}], max RGB={crop_r[ys_r, xs_r].max(axis=0)}")
else:
    print("No high specular glint in Right eye (>200)")

# Let's inspect pupil contours
# In Left eye, pupil is dark center
pupil_mask_l = (crop_l[:, :, 0] < 50) & (crop_l[:, :, 1] < 40) & (crop_l[:, :, 2] < 35)
ys, xs = np.where(pupil_mask_l)
if len(ys) > 0:
    print(f"Left pupil bounds: X in [{165+xs.min()}, {165+xs.max()}] (center={165+(xs.min()+xs.max())/2:.1f}, r={(xs.max()-xs.min())/2:.1f}), Y in [{135+ys.min()}, {135+ys.max()}] (center={135+(ys.min()+ys.max())/2:.1f}, r={(ys.max()-ys.min())/2:.1f})")

pupil_mask_r = (crop_r[:, :, 0] < 50) & (crop_r[:, :, 1] < 40) & (crop_r[:, :, 2] < 35)
ys_r, xs_r = np.where(pupil_mask_r)
if len(ys_r) > 0:
    print(f"Right pupil bounds: X in [{278+xs_r.min()}, {278+xs_r.max()}] (center={278+(xs_r.min()+xs_r.max())/2:.1f}, r={(xs_r.max()-xs_r.min())/2:.1f}), Y in [{135+ys_r.min()}, {135+ys_r.max()}] (center={135+(ys_r.min()+ys_r.max())/2:.1f}, r={(ys_r.max()-ys_r.min())/2:.1f})")

