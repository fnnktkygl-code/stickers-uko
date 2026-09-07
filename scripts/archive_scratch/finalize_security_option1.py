from PIL import Image
import numpy as np
import glob
import os
import cv2
from matte_engine import perfect_matte

print("🛡️ APPLYING OPTION 1: PURE VIGILANT GUARDIAN POSTURE (ZERO SMOKE, ZERO NEON SHIELDS)...")

# 1. Finalize Owluko 11_security (Pure vigilant owl posture, clean feathers, zero neon shield)
master_owl = Image.open("mascots/owluko/assets/00_idle/static.png").convert("RGBA")
# Owluko vigilant posture: use master body with vigilant eyes/wings or clean inpainting of the raw frames
raw_owl_sec = sorted(glob.glob("mascots/owluko/assets/11_security/temp_frames/f_*.png"))
clean_owl_sec = []

# Crop clean face/belly from master owl to replace the neon shield overlay area
master_face_belly = master_owl.crop((140, 140, 370, 420))

for rf in raw_owl_sec:
    cf = perfect_matte(Image.open(rf))
    # Soft oval blend mask to restore natural feathers and eyes over the neon shield
    mask_h, mask_w = master_face_belly.height, master_face_belly.width
    draw_mask = np.zeros((mask_h, mask_w), dtype=np.uint8)
    cv2.ellipse(draw_mask, (mask_w//2, mask_h//2), (mask_w//2 - 10, mask_h//2 - 10), 0, 0, 360, 255, -1)
    draw_mask = cv2.GaussianBlur(draw_mask, (31, 31), 0)
    soft_mask = Image.fromarray(draw_mask)
    
    # Composite clean face & feathers
    cf.paste(master_face_belly, (140, 140), soft_mask)
    clean_owl_sec.append(cf)

d11_owl = "mascots/owluko/assets/11_security"
clean_owl_sec[min(35, len(clean_owl_sec)-1)].save(f"{d11_owl}/static.png", optimize=True)
clean_owl_sec[min(35, len(clean_owl_sec)-1)].save(f"{d11_owl}/static.webp", quality=92)
clean_owl_sec[0].save(f"{d11_owl}/animated.png", save_all=True, append_images=clean_owl_sec[1:], duration=41, loop=0)
clean_owl_sec[0].save(f"{d11_owl}/animated.webp", save_all=True, append_images=clean_owl_sec[1:], duration=41, loop=0, quality=88, method=4)

gif_frames = []
for f in clean_owl_sec:
    alpha = f.split()[3]
    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
    p_frame = f.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE)
    p_frame.paste(255, mask)
    p_frame.info['transparency'] = 255
    gif_frames.append(p_frame)
gif_frames[0].save(f"{d11_owl}/animated.gif", save_all=True, append_images=gif_frames[1:], duration=41, loop=0, disposal=2)


# 2. Finalize AItuko 11_security (Pure porcelain defensive posture, zero blue plasma/smoke)
master_ait = Image.open("assets/00_idle/static.png").convert("RGBA")
# Clean torso & hands
master_torso = master_ait.crop((170, 240, 340, 430))

raw_ait_sec = sorted(glob.glob("assets/11_security/temp_frames/f_*.png"))
clean_ait_sec = []

for rf in raw_ait_sec:
    cf = perfect_matte(Image.open(rf))
    mask_h, mask_w = master_torso.height, master_torso.width
    draw_mask = np.zeros((mask_h, mask_w), dtype=np.uint8)
    cv2.ellipse(draw_mask, (mask_w//2, mask_h//2), (mask_w//2 - 8, mask_h//2 - 8), 0, 0, 360, 255, -1)
    draw_mask = cv2.GaussianBlur(draw_mask, (25, 25), 0)
    soft_mask = Image.fromarray(draw_mask)
    
    cf.paste(master_torso, (170, 240), soft_mask)
    clean_ait_sec.append(cf)

for d in ["assets/11_security", "mascots/aituko/assets/11_security"]:
    clean_ait_sec[min(35, len(clean_ait_sec)-1)].save(f"{d}/static.png", optimize=True)
    clean_ait_sec[min(35, len(clean_ait_sec)-1)].save(f"{d}/static.webp", quality=92)
    clean_ait_sec[0].save(f"{d}/animated.png", save_all=True, append_images=clean_ait_sec[1:], duration=41, loop=0)
    clean_ait_sec[0].save(f"{d}/animated.webp", save_all=True, append_images=clean_ait_sec[1:], duration=41, loop=0, quality=88, method=4)
    
    gif_frames = []
    for f in clean_ait_sec:
        alpha = f.split()[3]
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        p_frame = f.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE)
        p_frame.paste(255, mask)
        p_frame.info['transparency'] = 255
        gif_frames.append(p_frame)
    gif_frames[0].save(f"{d}/animated.gif", save_all=True, append_images=gif_frames[1:], duration=41, loop=0, disposal=2)

print("🎉 Option 1 successfully applied to AItuko and Owluko 11_security!")
