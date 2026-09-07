import numpy as np
from PIL import Image, ImageSequence
from scipy import ndimage

# Load Luneko 01_waving
im = Image.open('mascots/luneko/assets/01_waving/animated.webp')
frames = [f.convert('RGBA') for f in ImageSequence.Iterator(im)]
f0 = frames[0]

arr = np.array(f0)
r, g, b, a = arr[:,:,0].astype(float), arr[:,:,1].astype(float), arr[:,:,2].astype(float), arr[:,:,3].astype(float)

# What makes true background?
# Pure chroma green: high G, low R, low B
# On the borders (x=0, x=511, y=0, y=511)
is_chroma = (g > 140) & (g > r * 1.35) & (g > b * 1.35)

# Floodfill from border
labeled, num_features = ndimage.label(is_chroma)

# Find all labels that touch any border
border_mask = np.zeros_like(is_chroma, dtype=bool)
border_mask[0, :] = True
border_mask[-1, :] = True
border_mask[:, 0] = True
border_mask[:, -1] = True

border_labels = np.unique(labeled[border_mask])
# Remove 0 (which is non-chroma)
border_labels = border_labels[border_labels != 0]

true_bg_mask = np.isin(labeled, border_labels)

# Fill holes in the foreground (everything not true background is 100% solid foreground)
fg_mask = ~true_bg_mask
# Binary fill holes to make character 100% solid
fg_mask_filled = ndimage.binary_fill_holes(fg_mask)

# Despill on edges
# If any pixel in fg has g > (r+b)/2, clamp g to max(r, b)
despilled_g = np.where((fg_mask_filled) & (g > (r + b)/2 * 1.1), (r + b) / 2, g)

# Anti-alias alpha along the border
dist_to_bg = ndimage.distance_transform_edt(fg_mask_filled)
alpha = np.clip(dist_to_bg * 255.0, 0, 255).astype(np.uint8)

new_arr = np.dstack([r.astype(np.uint8), despilled_g.astype(np.uint8), b.astype(np.uint8), alpha])
res_img = Image.fromarray(new_arr)
res_img.save('/Users/richard/.gemini/antigravity/brain/5da7469d-6e59-4f3e-8894-cfaf7a0fac27/scratch/luneko_01_waving_repaired.png')

# Count internal holes
center_alpha = alpha[100:400, 150:350]
print("Holes remaining in center:", np.sum(center_alpha == 0))
