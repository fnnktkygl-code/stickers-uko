import os
import glob
import cv2
import numpy as np
from PIL import Image

print("🎨 HARMONIZING AITUKO TO UNIFIED ELECTRIC CYAN (#00E5FF / #38BDF8)...")

TARGET_HUE = 94 # ~188 degrees in 360 scale = Pure Vibrant Electric Cyan

def harmonize_aituko_frame(pil_img):
    """Maps any visor glow (blue/teal/turquoise/indigo) to the exact reference Electric Cyan."""
    rgba = np.array(pil_img.convert("RGBA"))
    r, g, b, a = rgba[:,:,0], rgba[:,:,1], rgba[:,:,2], rgba[:,:,3]
    
    h_img, w_img = rgba.shape[:2]
    # Visor is always in top 55% of the frame
    head_mask = np.zeros((h_img, w_img), dtype=bool)
    head_mask[:int(h_img * 0.55), :] = True
    
    # Convert RGB to HSV
    rgb = rgba[:,:,:3]
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    h, s, v = hsv[:,:,0], hsv[:,:,1], hsv[:,:,2]
    
    # Identify any blue/cyan/teal/indigo glow in head/visor area
    # In OpenCV HSV: H=70 (cyan-green) to H=135 (purple-blue)
    glow_mask = head_mask & (h >= 65) & (h <= 135) & (s > 35) & (v > 65) & (a > 80)
    
    # Remap hue to exact target electric cyan
    h[glow_mask] = TARGET_HUE
    # Boost saturation and brightness consistently for luminous OLED display effect
    s[glow_mask] = np.clip(s[glow_mask].astype(int) + 30, 150, 240).astype(np.uint8)
    v[glow_mask] = np.clip(v[glow_mask].astype(int) + 20, 180, 255).astype(np.uint8)
    
    # Convert back to RGB
    harmonized_hsv = np.dstack([h, s, v])
    harmonized_rgb = cv2.cvtColor(harmonized_hsv, cv2.COLOR_HSV2RGB)
    
    out_rgba = np.dstack([harmonized_rgb, a])
    return Image.fromarray(out_rgba, mode="RGBA")

states = [
    '01_waving', '02_celebrating', '03_ai_thinking', '04_error_404',
    '05_thumbs_up', '06_sleeping', '07_pointing', '08_searching',
    '09_loading', '10_idea', '11_security', '12_goodbye'
]

targets = ["assets", "mascots/aituko/assets"]

for base_dir in targets:
    for s in states:
        d = f"{base_dir}/{s}"
        if not os.path.exists(d):
            continue
            
        apng_path = f"{d}/animated.png"
        gif_path = f"{d}/animated.gif"
        webp_path = f"{d}/animated.webp"
        static_png = f"{d}/static.png"
        static_webp = f"{d}/static.webp"
        
        # 1. Process all animation frames from APNG
        if os.path.exists(apng_path):
            anim = Image.open(apng_path)
            n_frames = getattr(anim, 'n_frames', 1)
            frames = []
            durations = []
            
            for idx in range(n_frames):
                anim.seek(idx)
                f = anim.convert("RGBA")
                f_harm = harmonize_aituko_frame(f)
                frames.append(f_harm)
                durations.append(anim.info.get('duration', 41))
                
            # Save updated APNG
            frames[0].save(
                apng_path,
                save_all=True,
                append_images=frames[1:],
                duration=durations,
                loop=0
            )
            
            # Save updated WebP
            frames[0].save(
                webp_path,
                save_all=True,
                append_images=frames[1:],
                duration=durations,
                loop=0,
                quality=90,
                method=4
            )
            
            # Save updated Transparent GIF
            gif_frames = []
            for f in frames:
                alpha = f.split()[3]
                mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
                p_frame = f.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE)
                p_frame.paste(255, mask)
                p_frame.info['transparency'] = 255
                gif_frames.append(p_frame)
                
            gif_frames[0].save(
                gif_path,
                save_all=True,
                append_images=gif_frames[1:],
                duration=durations,
                loop=0,
                disposal=2
            )
            
        # 2. Process Static PNG and WebP
        if os.path.exists(static_png):
            st = Image.open(static_png).convert("RGBA")
            st_harm = harmonize_aituko_frame(st)
            st_harm.save(static_png, optimize=True)
            st_harm.save(static_webp, quality=92)

print("✅ AITUKO 100% UNIFIED & HARMONIZED!")
