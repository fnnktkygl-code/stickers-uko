import os
import math
import numpy as np
from PIL import Image
from matte_engine import perfect_matte

# 1. Clean Neutral Base (Frame A)
master_idle = Image.open("assets/00_idle/static.png").convert("RGBA")

# 2. Clean Protective Guard (Frame B)
guard_raw = Image.open("/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68/aituko_protection_clean_2arms_1788021077587.jpg")
guard_clean = perfect_matte(guard_raw)

TOTAL_FRAMES = 96
frames = []

for i in range(TOTAL_FRAMES):
    t = i / TOTAL_FRAMES
    
    # Smooth dynamic motion:
    # Raising hands up into guard, holding guard with breathing, and smooth continuous loop
    if t < 0.25:
        p = 0.5 - 0.5 * math.cos(math.pi * (t / 0.25))
    elif t < 0.75:
        p = 1.0
    else:
        p = 0.5 + 0.5 * math.cos(math.pi * ((t - 0.75) / 0.25))
        
    phase = 2.0 * math.pi * t
    dy = -3.0 * math.sin(phase)
    
    frame = Image.blend(master_idle, guard_clean, p)
    
    final_frame = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    final_frame.paste(frame, (0, int(dy)), frame)
    frames.append(final_frame)

for d in ["assets/11_security", "mascots/aituko/assets/11_security"]:
    frames[min(35, len(frames)-1)].save(f"{d}/static.png", optimize=True)
    frames[min(35, len(frames)-1)].save(f"{d}/static.webp", quality=92)
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

print("🎉 AItuko 11_security dynamic animation generated successfully!")
