from PIL import Image
import numpy as np
import math
import os
from matte_engine import perfect_matte

# 1. Process AItuko 11_security from native AI render
ait_raw = Image.open("/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68/aituko_protection_clean_2arms_1788021077587.jpg")
ait_clean = perfect_matte(ait_raw)

# Generate 96-frame breathing loop for AItuko 11_security
ait_frames = []
TOTAL_FRAMES = 96
for i in range(TOTAL_FRAMES):
    phase = 2.0 * math.pi * (i / TOTAL_FRAMES)
    dy = -2.5 * math.sin(phase)
    f = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    f.paste(ait_clean, (0, int(dy)), ait_clean)
    ait_frames.append(f)

for d in ["assets/11_security", "mascots/aituko/assets/11_security"]:
    ait_clean.save(f"{d}/static.png", optimize=True)
    ait_clean.save(f"{d}/static.webp", quality=92)
    ait_frames[0].save(f"{d}/animated.png", save_all=True, append_images=ait_frames[1:], duration=41, loop=0)
    ait_frames[0].save(f"{d}/animated.webp", save_all=True, append_images=ait_frames[1:], duration=41, loop=0, quality=88, method=4)
    
    gif_frames = []
    for f in ait_frames:
        alpha = f.split()[3]
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        p_frame = f.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE)
        p_frame.paste(255, mask)
        p_frame.info['transparency'] = 255
        gif_frames.append(p_frame)
    gif_frames[0].save(f"{d}/animated.gif", save_all=True, append_images=gif_frames[1:], duration=41, loop=0, disposal=2)

print("✅ Processed AItuko 11_security from AI render!")

# 2. Process Owluko 11_security from native AI render
owl_raw = Image.open("/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68/owluko_protection_clean_gesture_1788021092522.jpg")
owl_clean = perfect_matte(owl_raw)

# Generate 96-frame breathing loop for Owluko 11_security
owl_frames = []
for i in range(TOTAL_FRAMES):
    phase = 2.0 * math.pi * (i / TOTAL_FRAMES)
    dy = -2.5 * math.sin(phase)
    f = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    f.paste(owl_clean, (0, int(dy)), owl_clean)
    owl_frames.append(f)

d_owl = "mascots/owluko/assets/11_security"
owl_clean.save(f"{d_owl}/static.png", optimize=True)
owl_clean.save(f"{d_owl}/static.webp", quality=92)
owl_frames[0].save(f"{d_owl}/animated.png", save_all=True, append_images=owl_frames[1:], duration=41, loop=0)
owl_frames[0].save(f"{d_owl}/animated.webp", save_all=True, append_images=owl_frames[1:], duration=41, loop=0, quality=88, method=4)

gif_frames = []
for f in owl_frames:
    alpha = f.split()[3]
    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
    p_frame = f.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE)
    p_frame.paste(255, mask)
    p_frame.info['transparency'] = 255
    gif_frames.append(p_frame)
gif_frames[0].save(f"{d_owl}/animated.gif", save_all=True, append_images=gif_frames[1:], duration=41, loop=0, disposal=2)

print("✅ Processed Owluko 11_security from AI render!")
