from PIL import Image
import numpy as np

# Load panel 2, panel 3, panel 4, panel 5
p2 = Image.open('scratch/waving_panels/panel_2.png').convert('RGBA')
p3 = Image.open('scratch/waving_panels/panel_3.png').convert('RGBA')
p4 = Image.open('scratch/waving_panels/panel_4.png').convert('RGBA')
p5 = Image.open('scratch/waving_panels/panel_5.png').convert('RGBA')

# In panel 4, let's locate the waving wing
# Background is white (255, 255, 255)
arr4 = np.array(p4)
# Wing is on the right side: x > 200
mask_wing = (arr4[:, :, 0] < 250) & (arr4[:, :, 1] < 250) & (arr4[:, :, 2] < 250)
y_indices, x_indices = np.where(mask_wing)

# Find wing tip on the right
wing_x = x_indices[x_indices > 230]
wing_y = y_indices[x_indices > 230]
print(f"Panel 4 wing bounds: x=[{wing_x.min()}, {wing_x.max()}], y=[{wing_y.min()}, {wing_y.max()}]")

# In panel 5, analyze happy eyes
arr5 = np.array(p5)
# Happy eyes are dark brown pixels
dark_mask = (arr5[:, :, 0] < 120) & (arr5[:, :, 1] < 90) & (arr5[:, :, 2] < 60)
y_d, x_d = np.where(dark_mask)
print(f"Panel 5 dark eye bounds: x=[{x_d.min()}, {x_d.max()}], y=[{y_d.min()}, {y_d.max()}]")

# Print eye sample colors
eye_pixels = arr5[y_d, x_d]
mean_color = eye_pixels.mean(axis=0)
print(f"Panel 5 happy eye color mean: RGB=({mean_color[0]:.1f}, {mean_color[1]:.1f}, {mean_color[2]:.1f})")

