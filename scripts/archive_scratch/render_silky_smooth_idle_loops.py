import os
import math
import cv2
import numpy as np
from PIL import Image

mb_dir = "preview/moodboards/00_idle"
mascots = [
    ("aituko", "assets/00_idle/static.png", "AItuko (Robot)"),
    ("owluko", "mascots/owluko/assets/00_idle/static.png", "Owluko (Chouette)"),
    ("luneko", "mascots/luneko/assets/00_idle/static.png", "Luneko (Chat)"),
    ("usako", "mascots/usako/assets/00_idle/static.png", "Usako (Lapin)"),
    ("inuko", "mascots/inuko/assets/00_idle/static.png", "Inuko (Doberman)"),
    ("hatoko", "mascots/hatoko/assets/00_idle/static.png", "Hatoko (Pigeon)"),
]

TOTAL_FRAMES = 48  # 48 frames at 24fps = 2.0 seconds perfect smooth loop
FPS = 24
FRAME_DURATION_MS = int(1000 / FPS)  # ~41ms

for m_key, static_path, title in mascots:
    static_img = Image.open(static_path).convert("RGBA")
    frames = []
    
    for i in range(TOTAL_FRAMES):
        phase = 2.0 * math.pi * (i / TOTAL_FRAMES)
        
        # 1. Subtle smooth vertical breathing float (sinusoidal easing)
        dy = -4.0 * math.sin(phase)
        
        # 2. Subtle organic micro-scale breathing expansion
        scale_x = 1.0 + 0.015 * math.sin(phase)
        scale_y = 1.0 + 0.018 * math.sin(phase)
        
        # Resize with smooth lanczos
        w, h = static_img.size
        new_w = int(w * scale_x)
        new_h = int(h * scale_y)
        scaled = static_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Canvas 512x512
        f = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        paste_x = (512 - new_w) // 2
        paste_y = (512 - new_h) // 2 + int(dy)
        f.paste(scaled, (paste_x, paste_y), scaled)
        frames.append(f)
        
    # Save animated GIF with perfect transparency disposal
    gif_frames = []
    for f in frames:
        alpha = f.split()[3]
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        p_frame = f.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE)
        p_frame.paste(255, mask)
        p_frame.info['transparency'] = 255
        gif_frames.append(p_frame)
        
    gif_out = f"{mb_dir}/{m_key}_animated.gif"
    m_dir = "assets/00_idle" if m_key == "aituko" else f"mascots/{m_key}/assets/00_idle"
    
    gif_frames[0].save(gif_out, save_all=True, append_images=gif_frames[1:], duration=FRAME_DURATION_MS, loop=0, disposal=2)
    gif_frames[0].save(f"{m_dir}/animated.gif", save_all=True, append_images=gif_frames[1:], duration=FRAME_DURATION_MS, loop=0, disposal=2)
    frames[0].save(f"{m_dir}/animated.webp", save_all=True, append_images=frames[1:], duration=FRAME_DURATION_MS, loop=0, quality=90, method=4)
    frames[0].save(f"{m_dir}/animated.png", save_all=True, append_images=frames[1:], duration=FRAME_DURATION_MS, loop=0)
    
    # Check generated GIF
    check_im = Image.open(gif_out)
    print(f"🎬 {title} : Loop généré avec {check_im.n_frames} frames ({gif_out})")

print("🎉 Tous les GIFs animés 00_idle sont régénérés avec 48 frames ultra-fluides !")
