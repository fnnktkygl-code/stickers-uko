from PIL import Image
import numpy as np

# Load panel 4 and panel 1
p1 = Image.open('scratch/waving_panels/panel_1.png').convert('RGBA')
p4 = Image.open('scratch/waving_panels/panel_4.png').convert('RGBA')

# Panel dimensions: 341 x 285
# On 1024x1024 canvas, let's find the scale factor
# In master ref 1024x1024, the mascot is roughly:
# body width ~ 600 px, height ~ 730 px.
# In panel 1, let's find the mascot bounds:
arr1 = np.array(p1)
mask1 = (arr1[:, :, 0] < 250) | (arr1[:, :, 1] < 250) | (arr1[:, :, 2] < 250)
y1, x1 = np.where(mask1)
p1_w = x1.max() - x1.min()
p1_h = y1.max() - y1.min()
print(f"Panel 1 mascot bounds in 341x285: x=[{x1.min()}, {x1.max()}] (w={p1_w}), y=[{y1.min()}, {y1.max()}] (h={p1_h})")

# In 1024x1024 master ref:
im_clean = Image.open('mascots/owluko/owluko_master_ref_clean.png').convert('RGBA')
arr_c = np.array(im_clean)
mask_c = (arr_c[:, :, 0] < 250) | (arr_c[:, :, 1] < 250) | (arr_c[:, :, 2] < 250)
yc, xc = np.where(mask_c)
clean_w = xc.max() - xc.min()
clean_h = yc.max() - yc.min()
print(f"Clean master bounds in 1024x1024: x=[{xc.min()}, {xc.max()}] (w={clean_w}), y=[{yc.min()}, {yc.max()}] (h={clean_h})")

scale = clean_h / p1_h
print(f"Scale from panel to 1024 canvas: {scale:.3f}")

# Now let's trace the waving wing in panel 4
arr4 = np.array(p4)
# Wing pixels are non-white on the right side of the body: x > 230
wing_mask = ((arr4[:, :, 0] < 250) | (arr4[:, :, 1] < 250) | (arr4[:, :, 2] < 250)) & (np.arange(341)[None, :] >= 235)
yw, xw = np.where(wing_mask)
print(f"Wing in panel 4: x=[{xw.min()}, {xw.max()}], y=[{yw.min()}, {yw.max()}]")

# Map wing center and tips to 1024 coordinates:
# Origin offset between panel 1 and clean master:
offset_x = xc.min() - x1.min() * scale
offset_y = yc.min() - y1.min() * scale
print(f"Offset x: {offset_x:.1f}, offset y: {offset_y:.1f}")

scaled_wing_x0 = xw.min() * scale + offset_x
scaled_wing_x1 = xw.max() * scale + offset_x
scaled_wing_y0 = yw.min() * scale + offset_y
scaled_wing_y1 = yw.max() * scale + offset_y
print(f"Wing mapped to 1024 canvas: x=[{scaled_wing_x0:.1f}, {scaled_wing_x1:.1f}], y=[{scaled_wing_y0:.1f}, {scaled_wing_y1:.1f}]")

