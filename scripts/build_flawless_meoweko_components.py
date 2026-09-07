import cv2, numpy as np
from PIL import Image

# Load ground-truth 3D master
master_rgba = Image.open("mascots/meoweko/meoweko_master_exact_512.png").convert("RGBA")
master_np = np.array(master_rgba)
h, w = 512, 512

# 1. Ground baseline check: verify Y=490 baseline
alpha = master_np[:, :, 3]
ys, xs = np.where(alpha > 10)
print(f"Master bounds: X=[{xs.min()}, {xs.max()}], Y=[{ys.min()}, {ys.max()}]")
assert ys.max() == 490, f"Expected baseline Y=490, got {ys.max()}"

# 2. Extract Tail: X in [115, 205], Y in [395, 485]
# Tail is behind the left haunch. We can isolate it with a soft boundary where it passes behind the left haunch.
tail_rgba = np.zeros_like(master_np)
# Tail mask
tail_mask = np.zeros((h, w), dtype=bool)
tail_mask[395:485, 115:200] = (alpha[395:485, 115:200] > 10) & (master_np[395:485, 115:200, 0] > 120) & (master_np[395:485, 115:200, 2] < 100)
# Clean tail mask
tail_mask = cv2.morphologyEx(tail_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))) > 0
# Exclude the left haunch / paw where X > 175 and Y > 440
tail_mask[445:491, 175:230] = False
tail_rgba[tail_mask] = master_np[tail_mask]

# Inpaint behind haunch to make tail tip/body continuous
# The tail connects into the pelvis behind the left haunch
Image.fromarray(tail_rgba).save("scratch/meoweko_comp_tail.png")
print("Extracted scratch/meoweko_comp_tail.png")

# 3. Extract Eyes (Left & Right)
# Left eye: box around (223, 178) -> [148:208, 195:255]
# Right eye: box around (317, 176) -> [148:208, 288:348]
eyes_rgba = np.zeros_like(master_np)
eye_l_mask = np.zeros((h, w), dtype=bool)
eye_r_mask = np.zeros((h, w), dtype=bool)

# Left eye mask
cv2.circle(eye_l_mask.view(np.uint8), (223, 178), 28, 1, -1)
# Right eye mask
cv2.circle(eye_r_mask.view(np.uint8), (317, 176), 28, 1, -1)

# Refine with color threshold (amber or dark pupil/eyeliner)
r, g, b = master_np[:, :, 0], master_np[:, :, 1], master_np[:, :, 2]
eye_color_l = eye_l_mask & (alpha > 10) & (((r < 75) & (g < 75) & (b < 75)) | ((r > 150) & (g > 100) & (b < 80)) | ((r > 150) & (g > 150) & (b > 150)))
eye_color_r = eye_r_mask & (alpha > 10) & (((r < 75) & (g < 75) & (b < 75)) | ((r > 150) & (g > 100) & (b < 80)) | ((r > 150) & (g > 150) & (b > 150)))

eyes_rgba[eye_color_l | eye_color_r] = master_np[eye_color_l | eye_color_r]
Image.fromarray(eyes_rgba).save("scratch/meoweko_comp_eyes.png")
print("Extracted scratch/meoweko_comp_eyes.png")

# 4. Extract Head with Inpainted Eyes (Closed Eyelids for natural feline blink)
head_rgba = np.zeros_like(master_np)
head_mask = np.zeros((h, w), dtype=bool)
# Head spans Y in [41, 265], X in [145, 395]
head_mask[41:265, 145:395] = (alpha[41:265, 145:395] > 10)
head_rgba[head_mask] = master_np[head_mask]

# Inpaint eye areas using Navier-Stokes / Telea for porcelain eyelid skin
inpaint_mask = np.zeros((h, w), dtype=np.uint8)
inpaint_mask[eye_color_l | eye_color_r] = 255
# Dilate inpaint mask slightly
inpaint_mask = cv2.dilate(inpaint_mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))

bgr = cv2.cvtColor(head_rgba[:, :, :3], cv2.COLOR_RGB2BGR)
inpainted_bgr = cv2.inpaint(bgr, inpaint_mask, 5, cv2.INPAINT_TELEA)
head_inpainted = head_rgba.copy()
head_inpainted[:, :, :3] = cv2.cvtColor(inpainted_bgr, cv2.COLOR_BGR2RGB)
# Keep alpha intact
head_inpainted[~head_mask, 3] = 0

Image.fromarray(head_inpainted).save("scratch/meoweko_comp_head_inpainted.png")
print("Extracted scratch/meoweko_comp_head_inpainted.png")

# 5. Extract Grounded Body (Torso, Flanks, Legs, Paws)
body_rgba = np.zeros_like(master_np)
body_mask = np.zeros((h, w), dtype=bool)
body_mask[245:491, 160:385] = (alpha[245:491, 160:385] > 10)
body_rgba[body_mask] = master_np[body_mask]
Image.fromarray(body_rgba).save("scratch/meoweko_comp_body.png")
print("Extracted scratch/meoweko_comp_body.png")
