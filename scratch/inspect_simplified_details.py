from PIL import Image
import numpy as np

img = Image.open("mascots/owluko/owluko_simplified_master_ref.png").convert("RGB")
arr = np.array(img)

def sample_rgb(x, y, r=2):
    patch = arr[y-r:y+r+1, x-r:x+r+1]
    mean = patch.mean(axis=(0, 1)).astype(int)
    return "#{:02X}{:02X}{:02X}".format(*mean), mean

# Let's inspect Left Eye
# Iris center: where amber is darkest / most saturated
crop_le = arr[260:440, 310:480]
# Find center of dark pupil
dark_mask_le = (crop_le[:, :, 0] < 90) & (crop_le[:, :, 1] < 70) & (crop_le[:, :, 2] < 50)
y_p, x_p = np.where(dark_mask_le)
cx_lp, cy_lp = 310 + x_p.mean(), 260 + y_p.mean()
print(f"Left Eye Pupil Center: ({cx_lp:.1f}, {cy_lp:.1f})")

# Find outer iris radius: where iris meets mask
# Iris has high saturation (R-B > 80)
iris_mask_le = (crop_le[:, :, 0] > 140) & (crop_le[:, :, 1] > 90) & (crop_le[:, :, 2] < 80)
y_i, x_i = np.where(iris_mask_le)
cx_li, cy_li = 310 + x_i.mean(), 260 + y_i.mean()
r_li_x = (x_i.max() - x_i.min()) / 2
r_li_y = (y_i.max() - y_i.min()) / 2
print(f"Left Eye Iris Center: ({cx_li:.1f}, {cy_li:.1f}), rx={r_li_x:.1f}, ry={r_li_y:.1f}")

# Right eye
crop_re = arr[260:440, 540:710]
dark_mask_re = (crop_re[:, :, 0] < 90) & (crop_re[:, :, 1] < 70) & (crop_re[:, :, 2] < 50)
y_rp, x_rp = np.where(dark_mask_re)
cx_rp, cy_rp = 540 + x_rp.mean(), 260 + y_rp.mean()
print(f"Right Eye Pupil Center: ({cx_rp:.1f}, {cy_rp:.1f})")

iris_mask_re = (crop_re[:, :, 0] > 140) & (crop_re[:, :, 1] > 90) & (crop_re[:, :, 2] < 80)
y_ri, x_ri = np.where(iris_mask_re)
cx_ri, cy_ri = 540 + x_ri.mean(), 260 + y_ri.mean()
r_ri_x = (x_ri.max() - x_ri.min()) / 2
r_ri_y = (y_ri.max() - y_ri.min()) / 2
print(f"Right Eye Iris Center: ({cx_ri:.1f}, {cy_ri:.1f}), rx={r_ri_x:.1f}, ry={r_ri_y:.1f}")

# Beak apex, tip, width
crop_bk = arr[370:460, 460:564]
mask_bk = (crop_bk[:, :, 0] > 200) & (crop_bk[:, :, 1] > 110) & (crop_bk[:, :, 1] < 180) & (crop_bk[:, :, 2] < 70)
y_bk, x_bk = np.where(mask_bk)
print(f"Beak bounds: x=[{460+x_bk.min()}, {460+x_bk.max()}], y=[{370+y_bk.min()}, {370+y_bk.max()}]")
print(f"Beak width: {x_bk.max()-x_bk.min()+1}, height: {y_bk.max()-y_bk.min()+1}")

# Colors
print("\nColor samples:")
print("Crown top (512, 170):", sample_rgb(512, 170))
print("Facial mask brow (390, 240):", sample_rgb(390, 240))
print("Facial mask center dip (512, 290):", sample_rgb(512, 290))
print("Facial mask cheek (280, 360):", sample_rgb(280, 360))
print("Eye socket depression (340, 360):", sample_rgb(340, 360))
print("Iris amber top (390, 315):", sample_rgb(390, 315))
print("Iris golden bottom (390, 405):", sample_rgb(390, 405))
print("Pupil deep (400, 355):", sample_rgb(400, 355))
print("Specular main (375, 335):", sample_rgb(375, 335))
print("Specular secondary (418, 385):", sample_rgb(418, 385))
print("Beak bridge highlight (512, 395):", sample_rgb(512, 395))
print("Beak apex (512, 382):", sample_rgb(512, 382))
print("Beak body (512, 415):", sample_rgb(512, 415))
print("Beak tip (512, 448):", sample_rgb(512, 448))
print("Belly center (512, 650):", sample_rgb(512, 650))
print("Belly lower (512, 750):", sample_rgb(512, 750))
print("Flank flank shadow (200, 600):", sample_rgb(200, 600))
print("Wing left outer (180, 560):", sample_rgb(180, 560))
print("Wing left tip (220, 700):", sample_rgb(220, 700))
print("Feet middle toe (408, 855):", sample_rgb(408, 855))

