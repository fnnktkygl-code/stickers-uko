import cv2
import numpy as np
from PIL import Image

def perfect_matte(raw_rgb_pil):
    img = np.array(raw_rgb_pil.convert("RGB"))
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    h, s, v = hsv[:,:,0], hsv[:,:,1], hsv[:,:,2]
    
    # 1. Background detection: Chroma green OR black letterbox borders
    is_green = (h >= 35) & (h <= 85) & (s > 60) & (v > 40)
    is_black_border = (v < 20)
    is_bg_candidate = is_green | is_black_border
    
    # 2. Floodfill from borders
    h_img, w_img = img.shape[:2]
    flood_mask = np.zeros((h_img + 2, w_img + 2), dtype=np.uint8)
    flood_mask[1:-1, 1:-1] = (~is_bg_candidate).astype(np.uint8)
    
    bg_reachable = np.zeros((h_img, w_img), dtype=np.uint8)
    border_seeds = []
    for x in range(0, w_img, 20):
        border_seeds.extend([(x, 0), (x, h_img - 1)])
    for y in range(0, h_img, 20):
        border_seeds.extend([(0, y), (w_img - 1, y)])
        
    for cx, cy in border_seeds:
        if is_bg_candidate[cy, cx] and bg_reachable[cy, cx] == 0:
            cv2.floodFill(bg_reachable, flood_mask, (cx, cy), 255)
            
    true_bg = (bg_reachable == 255)
    char_fg = ~true_bg
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    char_fg_clean = cv2.morphologyEx(char_fg.astype(np.uint8) * 255, cv2.MORPH_CLOSE, kernel)
    
    dist = cv2.distanceTransform(char_fg_clean, cv2.DIST_L2, 3)
    alpha = np.clip(dist, 0.0, 1.0) * 255.0
    alpha = alpha.astype(np.uint8)
    
    r, g, b = img[:,:,0].astype(int), img[:,:,1].astype(int), img[:,:,2].astype(int)
    max_rb = np.maximum(r, b)
    despilled_g = np.where((g > max_rb) & (alpha > 0), max_rb, g)
    
    rgba = np.dstack([r.astype(np.uint8), despilled_g.astype(np.uint8), b.astype(np.uint8), alpha])
    pil_rgba = Image.fromarray(rgba, mode="RGBA")
    
    if w_img > h_img:
        left = (w_img - h_img) // 2
        pil_rgba = pil_rgba.crop((left, 0, left + h_img, h_img))
        
    return pil_rgba.resize((512, 512), Image.Resampling.LANCZOS)
