from PIL import Image
import glob
import os
import cv2
import numpy as np
from matte_engine import perfect_matte

# For AItuko 11_security:
# Remove the messy blue cloud on the body and keep AItuko's clean porcelain body and hands in front!
raw_aituko_sec = sorted(glob.glob("assets/11_security/temp_frames/f_*.png"))
clean_aituko_sec = []

# Get master clean torso
master_ait = Image.open("assets/00_idle/static.png").convert("RGBA")

for rf in raw_aituko_sec:
    raw_img = Image.open(rf)
    cf = perfect_matte(raw_img)
    arr = np.array(cf)
    
    # Remove blue smoke pixels on body (y: 200..450)
    body_mask = np.zeros((512, 512), dtype=bool)
    body_mask[220:460, 150:360] = True
    
    smoke_pixels = body_mask & (arr[:,:,2] > 180) & (arr[:,:,1] > 180) & (arr[:,:,0] < 160)
    
    # Replace with clean porcelain white/light grey
    arr[smoke_pixels, 0] = 235
    arr[smoke_pixels, 1] = 238
    arr[smoke_pixels, 2] = 242
    
    clean_f = Image.fromarray(arr, mode="RGBA")
    clean_aituko_sec.append(clean_f)

for d in ["assets/11_security", "mascots/aituko/assets/11_security"]:
    clean_aituko_sec[min(35, len(clean_aituko_sec)-1)].save(f"{d}/static.png", optimize=True)
    clean_aituko_sec[min(35, len(clean_aituko_sec)-1)].save(f"{d}/static.webp", quality=92)
    clean_aituko_sec[0].save(f"{d}/animated.png", save_all=True, append_images=clean_aituko_sec[1:], duration=41, loop=0)
    clean_aituko_sec[0].save(f"{d}/animated.webp", save_all=True, append_images=clean_aituko_sec[1:], duration=41, loop=0, quality=88, method=4)
    
    gif_frames = []
    for f in clean_aituko_sec:
        alpha = f.split()[3]
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        p_frame = f.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE)
        p_frame.paste(255, mask)
        p_frame.info['transparency'] = 255
        gif_frames.append(p_frame)
    gif_frames[0].save(f"{d}/animated.gif", save_all=True, append_images=gif_frames[1:], duration=41, loop=0, disposal=2)

print("✅ AItuko 11_security cleaned of smoke cloud!")
