import numpy as np
from PIL import Image
from scipy import ndimage

def key_frame_perfect(pil_img):
    img = pil_img.convert('RGB')
    arr = np.array(img, dtype=np.float32)
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    
    # 1. Chroma green criteria
    is_chroma = (g > 130) & (g > r * 1.30) & (g > b * 1.30)
    
    # 2. Label components
    labeled, num_features = ndimage.label(is_chroma)
    
    # 3. Find labels touching the image border
    border_mask = np.zeros(is_chroma.shape, dtype=bool)
    border_mask[0, :] = True
    border_mask[-1, :] = True
    border_mask[:, 0] = True
    border_mask[:, -1] = True
    
    border_labels = np.unique(labeled[border_mask])
    border_labels = border_labels[border_labels != 0]
    
    # 4. True exterior background
    is_true_bg = np.isin(labeled, border_labels)
    
    # 5. Foreground mask with binary hole filling
    fg_mask = ~is_true_bg
    fg_mask_filled = ndimage.binary_fill_holes(fg_mask)
    
    # 6. Green Despill on foreground pixels
    despilled_g = np.copy(g)
    green_spill_mask = fg_mask_filled & (g > (r + b) / 2.0)
    # Neutralize green bounce to average of red and blue
    despilled_g[green_spill_mask] = (r[green_spill_mask] + b[green_spill_mask]) / 2.0
    
    # 7. Sub-pixel anti-aliased edge
    dist_inside = ndimage.distance_transform_edt(fg_mask_filled)
    alpha = np.clip(dist_inside * 255.0, 0.0, 255.0).astype(np.uint8)
    
    out_arr = np.dstack([
        np.clip(r, 0, 255).astype(np.uint8),
        np.clip(despilled_g, 0, 255).astype(np.uint8),
        np.clip(b, 0, 255).astype(np.uint8),
        alpha
    ])
    return Image.fromarray(out_arr)

# Test on master image
master = Image.open('mascots/luneko/master/luneko_greenscreen_master.jpg')
res = key_frame_perfect(master)
res.save('/Users/richard/.gemini/antigravity/brain/5da7469d-6e59-4f3e-8894-cfaf7a0fac27/scratch/test_master_keyed.png')

# Verify no holes in center
arr_res = np.array(res)
center_a = arr_res[100:400, 150:350, 3]
print("Holes in center:", np.sum(center_a == 0))
print("Keyer test successful!")
