import cv2
import numpy as np
import os

os.makedirs('mascots/owluko/components', exist_ok=True)
img = cv2.imread('/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68/.user_uploaded/media_1788764972449.png')

def clean_extract(crop, threshold=6, min_area=500, unmultiply=True):
    """
    Extracts the central foreground object from a pure white background crop,
    ignoring tiny labels/text, with subpixel anti-aliasing and un-multiplication of white background.
    """
    h, w = crop.shape[:2]
    # Background is (255, 255, 255)
    # Difference from white:
    diff = 255.0 - np.min(crop.astype(np.float32), axis=2)
    
    # Binary mask for connected components
    bin_mask = (diff > threshold).astype(np.uint8)
    
    # Find connected components to remove text labels
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(bin_mask)
    
    obj_mask = np.zeros((h, w), dtype=np.uint8)
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        # Keep components with substantial area (objects) and near center
        if area > min_area:
            obj_mask[labels == i] = 255
            
    # Morphological close to bridge tiny gaps inside the object if any
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    obj_mask = cv2.morphologyEx(obj_mask, cv2.MORPH_CLOSE, kernel)
    
    # Compute smooth alpha matting along boundary
    # Inside core: alpha = 1.0
    # Transition zone: distance transform / soft edge
    dist_in = cv2.distanceTransform(obj_mask, cv2.DIST_L2, 3)
    
    # Soft alpha map:
    alpha = np.clip(dist_in / 1.5, 0.0, 1.0)
    
    # Unmultiply white background at soft edges
    # C_obs = alpha * C_fg + (1 - alpha) * 255
    # C_fg = (C_obs - 255 * (1 - alpha)) / alpha
    fg = crop.astype(np.float32)
    if unmultiply:
        safe_alpha = np.maximum(alpha, 0.01)[:, :, np.newaxis]
        fg_unmult = (fg - 255.0 * (1.0 - safe_alpha)) / safe_alpha
        fg_clean = np.clip(fg_unmult, 0.0, 255.0).astype(np.uint8)
    else:
        fg_clean = crop
        
    rgba = np.zeros((h, w, 4), dtype=np.uint8)
    rgba[:, :, :3] = fg_clean
    rgba[:, :, 3] = (alpha * 255.0).astype(np.uint8)
    
    # Crop to non-transparent bounding box with 4px margin
    coords = cv2.findNonZero(rgba[:, :, 3])
    x, y, bw, bh = cv2.boundingRect(coords)
    
    m = 4
    x0 = max(0, x - m)
    y0 = max(0, y - m)
    x1 = min(w, x + bw + m)
    y1 = min(h, y + bh + m)
    
    cropped_rgba = rgba[y0:y1, x0:x1]
    return cropped_rgba

# 1. Base Body (Panel 2)
p2 = img[20:310, 360:660]
base_rgba = clean_extract(p2, threshold=5, min_area=2000)
cv2.imwrite('mascots/owluko/components/body_base.png', base_rgba)
print('Saved body_base.png:', base_rgba.shape)

# 2. Wing (Panel 3)
p3 = img[20:310, 700:1000]
wing_rgba = clean_extract(p3, threshold=5, min_area=2000)
cv2.imwrite('mascots/owluko/components/wing_raw.png', wing_rgba)
print('Saved wing_raw.png:', wing_rgba.shape)

# 3. Eyes (Panel 4)
p4 = img[360:640, 25:315]
eyes_rgba = clean_extract(p4, threshold=8, min_area=500)
cv2.imwrite('mascots/owluko/components/eyes_pair.png', eyes_rgba)
print('Saved eyes_pair.png:', eyes_rgba.shape)

# Also extract left and right eye individually from the pair
h_e, w_e = eyes_rgba.shape[:2]
eye_l = eyes_rgba[:, :w_e//2]
coords_l = cv2.findNonZero(eye_l[:, :, 3])
xl, yl, wl, hl = cv2.boundingRect(coords_l)
eye_l_crop = eye_l[yl:yl+hl, xl:xl+wl]
cv2.imwrite('mascots/owluko/components/eye_left.png', eye_l_crop)

eye_r = eyes_rgba[:, w_e//2:]
coords_r = cv2.findNonZero(eye_r[:, :, 3])
xr, yr, wr, hr = cv2.boundingRect(coords_r)
eye_r_crop = eye_r[yr:yr+hr, xr:xr+wr]
cv2.imwrite('mascots/owluko/components/eye_right.png', eye_r_crop)
print(f'Saved eye_left.png ({eye_l_crop.shape}) and eye_right.png ({eye_r_crop.shape})')

# 4. Beak (Panel 5)
p5 = img[360:640, 370:650]
beak_rgba = clean_extract(p5, threshold=6, min_area=300)
cv2.imwrite('mascots/owluko/components/beak.png', beak_rgba)
print('Saved beak.png:', beak_rgba.shape)

# 5. Feet (Panel 6)
p6 = img[360:640, 700:1000]
feet_rgba = clean_extract(p6, threshold=6, min_area=400)
cv2.imwrite('mascots/owluko/components/feet_pair.png', feet_rgba)
print('Saved feet_pair.png:', feet_rgba.shape)

# Also extract left and right foot individually
h_f, w_f = feet_rgba.shape[:2]
foot_l = feet_rgba[:, :w_f//2]
coords_fl = cv2.findNonZero(foot_l[:, :, 3])
xfl, yfl, wfl, hfl = cv2.boundingRect(coords_fl)
foot_l_crop = foot_l[yfl:yfl+hfl, xfl:xfl+wfl]
cv2.imwrite('mascots/owluko/components/foot_left.png', foot_l_crop)

foot_r = feet_rgba[:, w_f//2:]
coords_fr = cv2.findNonZero(foot_r[:, :, 3])
xfr, yfr, wfr, hfr = cv2.boundingRect(coords_fr)
foot_r_crop = foot_r[yfr:yfr+hfr, xfr:xfr+wfr]
cv2.imwrite('mascots/owluko/components/foot_right.png', foot_r_crop)
print(f'Saved foot_left.png ({foot_l_crop.shape}) and foot_right.png ({foot_r_crop.shape})')

# 6. Belly Patch / Facial Mask from Base & Assembled:
# Let's inspect Panel 1 (Assembled mascot)
p1 = img[20:310, 20:310]
cv2.imwrite('mascots/owluko/components/mascot_assembled_ref.png', p1)
print('Component extraction complete.')
