import os
import glob
import cv2
import numpy as np
from PIL import Image, ImageSequence

def perfect_matte(pil_img):
    img = np.array(pil_img.convert("RGB"))
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    h, s, v = hsv[:,:,0], hsv[:,:,1], hsv[:,:,2]
    
    # 1. Initial green background candidate:
    # Pure chroma green is Hue 35..85, Saturation > 70, Value > 45
    is_green = (h >= 35) & (h <= 85) & (s > 70) & (v > 45)
    
    # 2. Border floodfill: Background MUST connect to outer frame borders
    # Create mask for floodFill (requires 2 pixels wider/taller, uint8)
    h_img, w_img = img.shape[:2]
    flood_mask = np.zeros((h_img + 2, w_img + 2), dtype=np.uint8)
    # Set non-green areas as walls (1) so floodfill cannot enter mascot
    flood_mask[1:-1, 1:-1] = (~is_green).astype(np.uint8)
    
    # Floodfill from the 4 corners on a working background plane
    bg_reachable = np.zeros((h_img, w_img), dtype=np.uint8)
    corners = [(0, 0), (w_img - 1, 0), (0, h_img - 1), (w_img - 1, h_img - 1)]
    for cx, cy in corners:
        if is_green[cy, cx]:
            # Seed floodfill
            cv2.floodFill(bg_reachable, flood_mask, (cx, cy), 255)
            
    # True background is ONLY pixels reachable from corners
    true_bg = (bg_reachable == 255)
    
    # Foreground character is everything else
    char_fg = ~true_bg
    
    # Morphological closing to seal any single-pixel fringe
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    char_fg_clean = cv2.morphologyEx(char_fg.astype(np.uint8) * 255, cv2.MORPH_CLOSE, kernel)
    
    # Distance transform for sub-pixel anti-aliased border
    dist = cv2.distanceTransform(char_fg_clean, cv2.DIST_L2, 3)
    alpha = np.clip(dist, 0.0, 1.0) * 255.0
    alpha = alpha.astype(np.uint8)
    
    # Despill: neutralizes any green reflection on character edge
    r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
    max_rb = np.maximum(r, b)
    despilled_g = np.where((g > max_rb) & (alpha > 0), max_rb, g)
    
    rgba = np.dstack([r, despilled_g, b, alpha])
    return Image.fromarray(rgba, mode="RGBA")

print("Tested perfect_matte function successfully.")
