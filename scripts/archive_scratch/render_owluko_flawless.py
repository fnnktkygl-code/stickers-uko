import os
import glob
import cv2
import numpy as np
from PIL import Image
import subprocess
import math

print("🦉 RENDERING FLAWLESS OWLUKO...")

def clean_owluko_frame(pil_img):
    """Refines Owluko frame: despill, solid alpha, 512x512 centered."""
    img = np.array(pil_img.convert("RGBA"))
    r, g, b, a = img[:,:,0], img[:,:,1], img[:,:,2], img[:,:,3]
    h_img, w_img = img.shape[:2]
    
    # Remove any chroma green residue
    is_green = (g > np.maximum(r, b) * 1.1) & (g > 80)
    despilled_g = np.where(is_green, np.maximum(r, b), g)
    
    # Solid alpha closing (no holes in feathers)
    mask = (a > 60).astype(np.uint8) * 255
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    clean_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    dist = cv2.distanceTransform(clean_mask, cv2.DIST_L2, 3)
    clean_alpha = (np.clip(dist, 0.0, 1.0) * 255.0).astype(np.uint8)
    
    rgba = np.dstack([r, despilled_g, b, clean_alpha])
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

# 1. Generate 00_idle for Owluko
print("🫁 Generating Owluko 00_idle breathing loop...")
raw_master = Image.open("mascots/owluko/master/owleko_greenscreen_master.jpg").convert("RGB")
from render_aituko_v2 import perfect_matte_and_harmonize_v2
base_owluko = perfect_matte_and_harmonize_v2(raw_master)

TOTAL_FRAMES = 96
idle_frames = []
for frame_idx in range(TOTAL_FRAMES):
    phase = 2.0 * math.pi * (frame_idx / TOTAL_FRAMES)
    dy = -3.5 * math.sin(phase)
    scale = 1.0 + 0.008 * math.sin(phase)
    
    w, h = base_owluko.size
    new_w = int(w * scale)
    new_h = int(h * scale)
    scaled_img = base_owluko.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    frame_canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    pos_x = (512 - new_w) // 2
    pos_y = int((512 - new_h) // 2 + dy)
    frame_canvas.paste(scaled_img, (pos_x, pos_y), scaled_img)
    idle_frames.append(frame_canvas)

out_idle = "mascots/owluko/assets/00_idle"
os.makedirs(out_idle, exist_ok=True)
idle_frames[0].save(f"{out_idle}/static.png", optimize=True)
idle_frames[0].save(f"{out_idle}/static.webp", quality=92)
idle_frames[0].save(f"{out_idle}/animated.png", save_all=True, append_images=idle_frames[1:], duration=41, loop=0)
idle_frames[0].save(f"{out_idle}/animated.webp", save_all=True, append_images=idle_frames[1:], duration=41, loop=0, quality=88, method=4)

gif_frames = []
for f in idle_frames:
    alpha = f.split()[3]
    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
    p_frame = f.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE)
    p_frame.paste(255, mask)
    p_frame.info['transparency'] = 255
    gif_frames.append(p_frame)
gif_frames[0].save(f"{out_idle}/animated.gif", save_all=True, append_images=gif_frames[1:], duration=41, loop=0, disposal=2)

# 2. Extract and refine all 12 states for Owluko
loupe_img = Image.open("preview/aituko_clean_loupe.png").convert("RGBA")

for s in states:
    d = f"mascots/owluko/assets/{s}"
    apng_path = f"{d}/animated.png"
    if not os.path.exists(apng_path):
        continue
        
    anim = Image.open(apng_path)
    n_frames = getattr(anim, 'n_frames', 1)
    frames = []
    
    for idx in range(n_frames):
        anim.seek(idx)
        f = anim.convert("RGBA")
        cf = clean_owluko_frame(f)
        
        # Special harmonization for 08_searching: composite orange 3D loupe
        if s == '08_searching':
            # Position loupe on left wing area
            # Scale loupe appropriately
            l_w, l_h = int(loupe_img.width * 0.95), int(loupe_img.height * 0.95)
            scaled_loupe = loupe_img.resize((l_w, l_h), Image.Resampling.LANCZOS)
            cf.paste(scaled_loupe, (105, 120), scaled_loupe)
            
        # Special clean for 11_security: remove blue chest sparks
        if s == '11_security':
            arr = np.array(cf)
            # Remove bright blue spark pixels in lower chest
            # Chest area: y=280..420, x=200..320
            chest_sparks = (arr[:,:,2] > 180) & (arr[:,:,2] - arr[:,:,0] > 60) & (arr[:,:,1] > 140)
            # Replace chest sparks with soft cream feather color
            arr[chest_sparks, 0] = 238
            arr[chest_sparks, 1] = 230
            arr[chest_sparks, 2] = 218
            cf = Image.fromarray(arr, mode="RGBA")
            
        frames.append(cf)
        
    # Choose representative active action frame for static
    if s == '06_sleeping':
        st_frame = frames[0] # fully sleeping
    elif s in ['01_waving', '02_celebrating', '03_ai_thinking', '05_thumbs_up', '07_pointing', '08_searching', '10_idea', '12_goodbye']:
        st_frame = frames[min(35, len(frames)-1)]
    else:
        st_frame = frames[0]
        
    st_frame.save(f"{d}/static.png", optimize=True)
    st_frame.save(f"{d}/static.webp", quality=92)
    
    frames[0].save(f"{d}/animated.png", save_all=True, append_images=frames[1:], duration=41, loop=0)
    frames[0].save(f"{d}/animated.webp", save_all=True, append_images=frames[1:], duration=41, loop=0, quality=88, method=4)
    
    gif_frames = []
    for f in frames:
        alpha = f.split()[3]
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        p_frame = f.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE)
        p_frame.paste(255, mask)
        p_frame.info['transparency'] = 255
        gif_frames.append(p_frame)
    gif_frames[0].save(f"{d}/animated.gif", save_all=True, append_images=gif_frames[1:], duration=41, loop=0, disposal=2)
    
    print(f"✨ Owluko/{s}: {len(frames)} frames perfected")

print("\n🎉 OWLUKO COMPLETED FLAWLESSLY!")
