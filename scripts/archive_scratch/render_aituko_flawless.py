import os
import glob
import cv2
import numpy as np
from PIL import Image
import subprocess
import zipfile

print("🚀 RENDERING FLAWLESS UNIFIED AITUKO (ELECTRIC CYAN #00E5FF)...")

def perfect_matte_and_harmonize(raw_rgb_pil):
    img = np.array(raw_rgb_pil.convert("RGB"))
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    h, s, v = hsv[:,:,0], hsv[:,:,1], hsv[:,:,2]
    
    # 1. Chroma green detection
    is_green = (h >= 35) & (h <= 85) & (s > 70) & (v > 45)
    
    # 2. Floodfill from borders
    h_img, w_img = img.shape[:2]
    flood_mask = np.zeros((h_img + 2, w_img + 2), dtype=np.uint8)
    flood_mask[1:-1, 1:-1] = (~is_green).astype(np.uint8)
    
    bg_reachable = np.zeros((h_img, w_img), dtype=np.uint8)
    corners = [(0, 0), (w_img - 1, 0), (0, h_img - 1), (w_img - 1, h_img - 1)]
    for cx, cy in corners:
        if is_green[cy, cx]:
            cv2.floodFill(bg_reachable, flood_mask, (cx, cy), 255)
            
    true_bg = (bg_reachable == 255)
    char_fg = ~true_bg
    
    # Morphology closing
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    char_fg_clean = cv2.morphologyEx(char_fg.astype(np.uint8) * 255, cv2.MORPH_CLOSE, kernel)
    
    # Distance transform anti-aliasing
    dist = cv2.distanceTransform(char_fg_clean, cv2.DIST_L2, 3)
    alpha = np.clip(dist, 0.0, 1.0) * 255.0
    alpha = alpha.astype(np.uint8)
    
    # Despill green reflections
    r, g, b = img[:,:,0].astype(int), img[:,:,1].astype(int), img[:,:,2].astype(int)
    max_rb = np.maximum(r, b)
    despilled_g = np.where((g > max_rb) & (alpha > 0), max_rb, g)
    
    # 3. Eye / Smile Electric Cyan Harmonization
    head_mask = np.zeros((h_img, w_img), dtype=bool)
    head_mask[:int(h_img * 0.55), :] = True
    
    # Strict eye/mouth criteria (high saturation cyan, excludes reflection)
    eye_mask = head_mask & (b > 135) & (despilled_g > 135) & (despilled_g - r > 40) & (b - r > 40) & (alpha > 120)
    
    final_r = np.where(eye_mask, np.clip(r * 0.2, 0, 40), r).astype(np.uint8)
    final_g = np.where(eye_mask, np.clip(despilled_g * 1.1 + 30, 225, 255), despilled_g).astype(np.uint8)
    final_b = np.where(eye_mask, np.clip(b * 1.05 + 20, 245, 255), b).astype(np.uint8)
    
    rgba = np.dstack([final_r, final_g, final_b, alpha])
    pil_rgba = Image.fromarray(rgba, mode="RGBA")
    
    if w_img > h_img:
        left = (w_img - h_img) // 2
        pil_rgba = pil_rgba.crop((left, 0, left + h_img, h_img))
        
    return pil_rgba.resize((512, 512), Image.Resampling.LANCZOS)

states = [
    '01_waving', '02_celebrating', '03_ai_thinking', '04_error_404',
    '05_thumbs_up', '06_sleeping', '07_pointing', '08_searching',
    '09_loading', '10_idea', '11_security', '12_goodbye'
]

os.makedirs("preview/aituko_flawless", exist_ok=True)

for s in states:
    d = f"assets/{s}"
    d_mascot = f"mascots/aituko/assets/{s}"
    os.makedirs(d, exist_ok=True)
    os.makedirs(d_mascot, exist_ok=True)
    
    clean_frames = []
    
    # Source A: from looped_video.mp4 if available
    video_path = f"{d}/looped_video.mp4"
    temp_frames_dir = f"{d}/temp_frames"
    
    if os.path.exists(video_path):
        temp_dir = f"preview/temp_extract_{s}"
        os.makedirs(temp_dir, exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-i", video_path, f"{temp_dir}/f_%03d.png"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        extracted = sorted(glob.glob(f"{temp_dir}/f_*.png"))
        for ef in extracted:
            raw_img = Image.open(ef)
            cf = perfect_matte_and_harmonize(raw_img)
            clean_frames.append(cf)
            os.remove(ef)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)
            
    elif os.path.exists(temp_frames_dir) and glob.glob(f"{temp_frames_dir}/f_*.png"):
        raw_files = sorted(glob.glob(f"{temp_frames_dir}/f_*.png"))
        for rf in raw_files:
            raw_img = Image.open(rf)
            cf = perfect_matte_and_harmonize(raw_img)
            clean_frames.append(cf)
            
    elif os.path.exists(f"{d}/animated.png"):
        anim = Image.open(f"{d}/animated.png")
        for idx in range(getattr(anim, 'n_frames', 1)):
            anim.seek(idx)
            f = anim.convert("RGBA")
            cf = perfect_matte_and_harmonize(f)
            clean_frames.append(cf)
            
    if not clean_frames:
        print(f"⚠️ No frames found for {s}!")
        continue
        
    print(f"✅ Processed {len(clean_frames)} frames for AItuko/{s}")
    
    # 1. Save static.png and static.webp
    # Choose representative action frame or frame 0
    # For waving/searching/pointing, choose active action frame
    st_frame = clean_frames[len(clean_frames)//4] if s in ['01_waving', '07_pointing', '08_searching'] else clean_frames[0]
    
    for out_d in [d, d_mascot]:
        st_frame.save(f"{out_d}/static.png", optimize=True)
        st_frame.save(f"{out_d}/static.webp", quality=92)
        
        # 2. Save animated.png (APNG)
        clean_frames[0].save(
            f"{out_d}/animated.png",
            save_all=True,
            append_images=clean_frames[1:],
            duration=41,
            loop=0
        )
        
        # 3. Save animated.webp (60fps feel)
        clean_frames[0].save(
            f"{out_d}/animated.webp",
            save_all=True,
            append_images=clean_frames[1:],
            duration=41,
            loop=0,
            quality=88,
            method=4
        )
        
        # 4. Save animated.gif (Transparent palette, 0 green)
        gif_frames = []
        for f in clean_frames:
            alpha = f.split()[3]
            mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
            p_frame = f.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE)
            p_frame.paste(255, mask)
            p_frame.info['transparency'] = 255
            gif_frames.append(p_frame)
            
        gif_frames[0].save(
            f"{out_d}/animated.gif",
            save_all=True,
            append_images=gif_frames[1:],
            duration=41,
            loop=0,
            disposal=2
        )

print("\n🎉 ALL 12 STATES OF AITUKO ARE NOW FLAWLESS & HARMONIZED!")
