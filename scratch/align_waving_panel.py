from PIL import Image
import numpy as np

p1 = Image.open('scratch/waving_panels/panel_1.png').convert('RGB')
p4 = Image.open('scratch/waving_panels/panel_4.png').convert('RGB')
p5 = Image.open('scratch/waving_panels/panel_5.png').convert('RGB')
master = Image.open('mascots/owluko/owluko_master_ref_clean.png').convert('RGB')

# Let's find the beak center in panel 1 and master
# Beak is orange: R > 200, G in [100, 170], B < 80
def get_beak_center(img):
    arr = np.array(img)
    beak_mask = (arr[:, :, 0] > 200) & (arr[:, :, 1] > 100) & (arr[:, :, 1] < 180) & (arr[:, :, 2] < 80)
    y, x = np.where(beak_mask)
    if len(x) == 0:
        return None
    return (x.mean(), y.mean(), x.max() - x.min(), y.max() - y.min())

beak_master = get_beak_center(master)
beak_p1 = get_beak_center(p1)
beak_p4 = get_beak_center(p4)
beak_p5 = get_beak_center(p5)

print("Beak in master:", beak_master)
print("Beak in p1:", beak_p1)
print("Beak in p4:", beak_p4)
print("Beak in p5:", beak_p5)

scale_beak = beak_master[2] / beak_p1[2]
print(f"Scale from beak: {scale_beak:.3f}")

# Transform panel 4 to match master:
# Master beak is at (512.6, 427.3)
# In p4, beak is at (170.8, 142.2)
# Scale factor: 512.6 / 170.8 = 3.001! (Notice: 1024 / 341 = 3.0029!)
print(f"Direct grid scale: 1024 / 341 = {1024 / 341:.4f}")

# So the panels are exactly 1/3 resolution of 1024x1024!
# 341.33 x 285 is half height (571 / 2 = 285.5) and one third width (1024 / 3 = 341.33)!
