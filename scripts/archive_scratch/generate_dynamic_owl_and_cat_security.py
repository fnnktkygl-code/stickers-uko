import os
import math
import numpy as np
from PIL import Image
from process_all_luneko_states import key_luneko_ultimate
from matte_engine import perfect_matte

artifact_dir = "/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68"
TOTAL_FRAMES = 96

# 1. Owluko 11_security Dynamic Loop
owl_idle = Image.open("mascots/owluko/assets/00_idle/static.png").convert("RGBA")
owl_guard_raw = Image.open(f"{artifact_dir}/owluko_protection_clean_gesture_1788021092522.jpg")
owl_guard = perfect_matte(owl_guard_raw)

owl_frames = []
for i in range(TOTAL_FRAMES):
    t = i / TOTAL_FRAMES
    if t < 0.25:
        p = 0.5 - 0.5 * math.cos(math.pi * (t / 0.25))
    elif t < 0.75:
        p = 1.0
    else:
        p = 0.5 + 0.5 * math.cos(math.pi * ((t - 0.75) / 0.25))
        
    phase = 2.0 * math.pi * t
    dy = -2.5 * math.sin(phase)
    
    frame = Image.blend(owl_idle, owl_guard, p)
    final_frame = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    final_frame.paste(frame, (0, int(dy)), frame)
    owl_frames.append(final_frame)

d_owl = "mascots/owluko/assets/11_security"
owl_frames[min(35, len(owl_frames)-1)].save(f"{d_owl}/static.png", optimize=True)
owl_frames[min(35, len(owl_frames)-1)].save(f"{d_owl}/static.webp", quality=92)
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
owl_frames[0].save(f"{d_owl}/animated.gif", save_all=True, append_images=gif_frames[1:], duration=41, loop=0, disposal=2)

print("✅ Owluko 11_security dynamic loop generated!")

# 2. Luneko 11_security Dynamic Loop
lun_idle = Image.open(f"{artifact_dir}/luneko_00_idle_1788027599561.jpg")
lun_idle_clean = key_luneko_ultimate(lun_idle)

lun_guard_raw = Image.open(f"{artifact_dir}/luneko_11_security_1788027554825.jpg")
lun_guard = key_luneko_ultimate(lun_guard_raw)

lun_frames = []
for i in range(TOTAL_FRAMES):
    t = i / TOTAL_FRAMES
    if t < 0.25:
        p = 0.5 - 0.5 * math.cos(math.pi * (t / 0.25))
    elif t < 0.75:
        p = 1.0
    else:
        p = 0.5 + 0.5 * math.cos(math.pi * ((t - 0.75) / 0.25))
        
    phase = 2.0 * math.pi * t
    dy = -2.5 * math.sin(phase)
    
    frame = Image.blend(lun_idle_clean, lun_guard, p)
    final_frame = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    final_frame.paste(frame, (0, int(dy)), frame)
    lun_frames.append(final_frame)

d_lun = "mascots/luneko/assets/11_security"
lun_frames[min(35, len(lun_frames)-1)].save(f"{d_lun}/static.png", optimize=True)
lun_frames[min(35, len(lun_frames)-1)].save(f"{d_lun}/static.webp", quality=92)
lun_frames[0].save(f"{d_lun}/animated.png", save_all=True, append_images=lun_frames[1:], duration=41, loop=0)
lun_frames[0].save(f"{d_lun}/animated.webp", save_all=True, append_images=lun_frames[1:], duration=41, loop=0, quality=88, method=4)

gif_frames = []
for f in lun_frames:
    alpha = f.split()[3]
    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
    p_frame = f.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE)
    p_frame.paste(255, mask)
    p_frame.info['transparency'] = 255
    gif_frames.append(p_frame)
lun_frames[0].save(f"{d_lun}/animated.gif", save_all=True, append_images=gif_frames[1:], duration=41, loop=0, disposal=2)

print("✅ Luneko 11_security dynamic loop generated!")
