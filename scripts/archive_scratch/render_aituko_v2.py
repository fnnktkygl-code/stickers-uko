import os
import glob
import cv2
import numpy as np
from PIL import Image
import subprocess

print("🚀 RENDERING FLAWLESS AITUKO V2...")

def perfect_matte_and_harmonize_v2(raw_rgb_pil):
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
    
    head_mask = np.zeros((h_img, w_img), dtype=bool)
    head_mask[:int(h_img * 0.55), :] = True
    
    eye_mask = head_mask & (b > 130) & (despilled_g > 130) & (despilled_g - r > 35) & (b - r > 35) & (alpha > 120)
    
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

for s in states:
    d = f"assets/{s}"
    d_mascot = f"mascots/aituko/assets/{s}"
    
    clean_frames = []
    video_path = f"{d}/looped_video.mp4"
    temp_frames_dir = f"{d}/temp_frames"
    
    if os.path.exists(video_path):
        temp_dir = f"preview/temp_extract_{s}"
        os.makedirs(temp_dir, exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-i", video_path, f"{temp_dir}/f_%03d.png"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        extracted = sorted(glob.glob(f"{temp_dir}/f_*.png"))
        for ef in extracted:
            raw_img = Image.open(ef)
            cf = perfect_matte_and_harmonize_v2(raw_img)
            clean_frames.append(cf)
            os.remove(ef)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)
            
    elif os.path.exists(temp_frames_dir) and glob.glob(f"{temp_frames_dir}/f_*.png"):
        raw_files = sorted(glob.glob(f"{temp_frames_dir}/f_*.png"))
        for rf in raw_files:
            raw_img = Image.open(rf)
            cf = perfect_matte_and_harmonize_v2(raw_img)
            clean_frames.append(cf)
            
    elif os.path.exists(f"{d}/animated.png"):
        anim = Image.open(f"{d}/animated.png")
        for idx in range(getattr(anim, 'n_frames', 1)):
            anim.seek(idx)
            f = anim.convert("RGBA")
            cf = perfect_matte_and_harmonize_v2(f)
            clean_frames.append(cf)
            
    if not clean_frames:
        continue
        
    print(f"✨ AItuko/{s}: {len(clean_frames)} frames rendered")
    st_frame = clean_frames[len(clean_frames)//4] if s in ['01_waving', '07_pointing', '08_searching'] else clean_frames[0]
    
    for out_d in [d, d_mascot]:
        st_frame.save(f"{out_d}/static.png", optimize=True)
        st_frame.save(f"{out_d}/static.webp", quality=92)
        
        clean_frames[0].save(
            f"{out_d}/animated.png",
            save_all=True,
            append_images=clean_frames[1:],
            duration=41,
            loop=0
        )
        
        clean_frames[0].save(
            f"{out_d}/animated.webp",
            save_all=True,
            append_images=clean_frames[1:],
            duration=41,
            loop=0,
            quality=88,
            method=4
        )
        
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

print("\n🎉 AITUKO V2 COMPLETED PERFECTLY!")
