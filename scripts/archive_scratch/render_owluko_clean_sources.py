from PIL import Image
import numpy as np
import glob
import os
import cv2

from render_owluko_flawless import clean_owluko_frame

pure_loupe = Image.open("preview/pure_orange_loupe.png").convert("RGBA")
# Resize loupe to fit Owluko's eye
l_w, l_h = int(pure_loupe.width * 0.85), int(pure_loupe.height * 0.85)
scaled_loupe = pure_loupe.resize((l_w, l_h), Image.Resampling.LANCZOS)

# 1. Clean 08_searching from pristine temp_frames
raw_search_files = sorted(glob.glob("mascots/owluko/assets/08_searching/temp_frames/f_*.png"))
clean_search_frames = []

for rf in raw_search_files:
    raw_img = Image.open(rf)
    cf = clean_owluko_frame(raw_img)
    # Composite the clean pure orange loupe over the eye/wing area
    cf.paste(scaled_loupe, (115, 130), scaled_loupe)
    clean_search_frames.append(cf)

d08 = "mascots/owluko/assets/08_searching"
clean_search_frames[min(35, len(clean_search_frames)-1)].save(f"{d08}/static.png", optimize=True)
clean_search_frames[min(35, len(clean_search_frames)-1)].save(f"{d08}/static.webp", quality=92)
clean_search_frames[0].save(f"{d08}/animated.png", save_all=True, append_images=clean_search_frames[1:], duration=41, loop=0)
clean_search_frames[0].save(f"{d08}/animated.webp", save_all=True, append_images=clean_search_frames[1:], duration=41, loop=0, quality=88, method=4)

# Transparent GIF
gif_frames = []
for f in clean_search_frames:
    alpha = f.split()[3]
    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
    p_frame = f.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE)
    p_frame.paste(255, mask)
    p_frame.info['transparency'] = 255
    gif_frames.append(p_frame)
gif_frames[0].save(f"{d08}/animated.gif", save_all=True, append_images=gif_frames[1:], duration=41, loop=0, disposal=2)


# 2. Clean 11_security from pristine temp_frames
raw_sec_files = sorted(glob.glob("mascots/owluko/assets/11_security/temp_frames/f_*.png"))
clean_sec_frames = []

master_owl = Image.open("mascots/owluko/assets/00_idle/static.png").convert("RGBA")
master_belly = master_owl.crop((185, 270, 325, 410))

for rf in raw_sec_files:
    raw_img = Image.open(rf)
    cf = clean_owluko_frame(raw_img)
    
    # Soft feathered mask for clean belly patch
    draw_mask = np.zeros((master_belly.height, master_belly.width), dtype=np.uint8)
    cv2.circle(draw_mask, (draw_mask.shape[1]//2, draw_mask.shape[0]//2), 48, 255, -1)
    draw_mask = cv2.GaussianBlur(draw_mask, (21, 21), 0)
    soft_mask = Image.fromarray(draw_mask)
    
    cf.paste(master_belly, (185, 270), soft_mask)
    clean_sec_frames.append(cf)

d11 = "mascots/owluko/assets/11_security"
clean_sec_frames[min(35, len(clean_sec_frames)-1)].save(f"{d11}/static.png", optimize=True)
clean_sec_frames[min(35, len(clean_sec_frames)-1)].save(f"{d11}/static.webp", quality=92)
clean_sec_frames[0].save(f"{d11}/animated.png", save_all=True, append_images=clean_sec_frames[1:], duration=41, loop=0)
clean_sec_frames[0].save(f"{d11}/animated.webp", save_all=True, append_images=clean_sec_frames[1:], duration=41, loop=0, quality=88, method=4)

# Transparent GIF
gif_frames = []
for f in clean_sec_frames:
    alpha = f.split()[3]
    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
    p_frame = f.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE)
    p_frame.paste(255, mask)
    p_frame.info['transparency'] = 255
    gif_frames.append(p_frame)
gif_frames[0].save(f"{d11}/animated.gif", save_all=True, append_images=gif_frames[1:], duration=41, loop=0, disposal=2)

print("🎉 08_searching and 11_security rendered cleanly from raw sources!")
