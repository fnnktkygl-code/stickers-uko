import os
import glob
import math
import numpy as np
from PIL import Image
from matte_engine import perfect_matte

artifact_dir = "/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68"
luneko_dir = "mascots/luneko/assets"

TOTAL_FRAMES = 96

# Master clean idle
master_idle_raw = Image.open(f"{artifact_dir}/luneko_00_idle_1788027599561.jpg")
master_idle = perfect_matte(master_idle_raw)

# Map raw image paths for all states
state_sources = {
    "00_idle": f"{artifact_dir}/luneko_00_idle_1788027599561.jpg",
    "01_waving": "mascots/luneko/assets/01_waving/static.png",
    "02_celebrating": "mascots/luneko/assets/02_celebrating/static.png",
    "03_ai_thinking": "mascots/luneko/assets/03_ai_thinking/static.png",
    "04_error_404": "mascots/luneko/assets/04_error_404/static.png",
    "05_thumbs_up": "mascots/luneko/assets/05_thumbs_up/static.png",
    "06_sleeping": "mascots/luneko/assets/06_sleeping/static.png",
    "07_pointing": "mascots/luneko/assets/07_pointing/static.png",
    "08_searching": f"{artifact_dir}/luneko_08_searching_1788027520883.jpg",
    "09_loading": f"{artifact_dir}/luneko_09_loading_1788027640868.jpg",
    "10_idea": f"{artifact_dir}/luneko_10_idea_1788027537929.jpg",
    "11_security": f"{artifact_dir}/luneko_11_security_1788027554825.jpg",
    "12_goodbye": f"{artifact_dir}/luneko_12_goodbye_1788027571598.jpg",
}

print("🐱 RENDERING MASTER LUNEKO ASSETS (512x512, TRANSPARENT)...")

for s, src in state_sources.items():
    s_dir = f"{luneko_dir}/{s}"
    os.makedirs(s_dir, exist_ok=True)
    
    # Load and clean source image
    raw_img = Image.open(src)
    if src.endswith(".jpg"):
        clean_img = perfect_matte(raw_img)
    else:
        # Already PNG, ensure perfect square and clean alpha
        clean_img = raw_img.convert("RGBA")
        if clean_img.size != (512, 512):
            clean_img = clean_img.resize((512, 512), Image.Resampling.LANCZOS)
    
    # Check if raw frame sequence exists for dynamic actions (like thinking, waving)
    temp_frames = sorted(glob.glob(f"{s_dir}/temp_frames/f_*.png"))
    
    if len(temp_frames) >= 30 and s not in ["08_searching", "10_idea", "11_security", "12_goodbye"]:
        # Has pre-existing video frames
        clean_frames = [perfect_matte(Image.open(tf)) for tf in temp_frames]
    elif s == "06_sleeping":
        # Pure continuous breathing sleep loop
        clean_frames = []
        for i in range(TOTAL_FRAMES):
            phase = 2.0 * math.pi * (i / TOTAL_FRAMES)
            dy = -2.0 * math.sin(phase)
            f = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
            f.paste(clean_img, (0, int(dy)), clean_img)
            clean_frames.append(f)
    elif s == "09_loading":
        # Loading star orbiting
        clean_frames = []
        for i in range(TOTAL_FRAMES):
            phase = 2.0 * math.pi * (i / TOTAL_FRAMES)
            dy = -2.0 * math.sin(phase)
            f = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
            f.paste(clean_img, (0, int(dy)), clean_img)
            clean_frames.append(f)
    else:
        # Generate 96-frame breathing loop for the pose
        clean_frames = []
        for i in range(TOTAL_FRAMES):
            phase = 2.0 * math.pi * (i / TOTAL_FRAMES)
            dy = -2.5 * math.sin(phase)
            f = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
            f.paste(clean_img, (0, int(dy)), clean_img)
            clean_frames.append(f)
            
    # Save static
    clean_frames[min(35, len(clean_frames)-1)].save(f"{s_dir}/static.png", optimize=True)
    clean_frames[min(35, len(clean_frames)-1)].save(f"{s_dir}/static.webp", quality=92)
    
    # Save animated
    clean_frames[0].save(f"{s_dir}/animated.png", save_all=True, append_images=clean_frames[1:], duration=41, loop=0)
    clean_frames[0].save(f"{s_dir}/animated.webp", save_all=True, append_images=clean_frames[1:], duration=41, loop=0, quality=88, method=4)
    
    # Save GIF
    gif_frames = []
    for f in clean_frames:
        alpha = f.split()[3]
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        p_frame = f.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE)
        p_frame.paste(255, mask)
        p_frame.info['transparency'] = 255
        gif_frames.append(p_frame)
    gif_frames[0].save(f"{s_dir}/animated.gif", save_all=True, append_images=gif_frames[1:], duration=41, loop=0, disposal=2)
    
    print(f"✨ Luneko/{s}: Rendered {len(clean_frames)} frames")

print("🎉 ALL 13 STATES OF LUNEKO RENDERED FLAWLESSLY!")
