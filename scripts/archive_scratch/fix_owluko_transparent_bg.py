from PIL import Image
import numpy as np
import glob
import cv2

from render_aituko_v2 import perfect_matte_and_harmonize_v2

pure_loupe = Image.open("preview/pure_orange_loupe.png").convert("RGBA")
l_w, l_h = int(pure_loupe.width * 0.85), int(pure_loupe.height * 0.85)
scaled_loupe = pure_loupe.resize((l_w, l_h), Image.Resampling.LANCZOS)

# 1. Process 08_searching with perfect matte
raw_search = sorted(glob.glob("mascots/owluko/assets/08_searching/temp_frames/f_*.png"))
clean_search = []
for rf in raw_search:
    raw_img = Image.open(rf)
    cf = perfect_matte_and_harmonize_v2(raw_img)
    cf.paste(scaled_loupe, (115, 130), scaled_loupe)
    clean_search.append(cf)

d08 = "mascots/owluko/assets/08_searching"
clean_search[min(35, len(clean_search)-1)].save(f"{d08}/static.png", optimize=True)
clean_search[min(35, len(clean_search)-1)].save(f"{d08}/static.webp", quality=92)
clean_search[0].save(f"{d08}/animated.png", save_all=True, append_images=clean_search[1:], duration=41, loop=0)
clean_search[0].save(f"{d08}/animated.webp", save_all=True, append_images=clean_search[1:], duration=41, loop=0, quality=88, method=4)

gif_frames = []
for f in clean_search:
    alpha = f.split()[3]
    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
    p_frame = f.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE)
    p_frame.paste(255, mask)
    p_frame.info['transparency'] = 255
    gif_frames.append(p_frame)
gif_frames[0].save(f"{d08}/animated.gif", save_all=True, append_images=gif_frames[1:], duration=41, loop=0, disposal=2)


# 2. Process 11_security with perfect matte
raw_sec = sorted(glob.glob("mascots/owluko/assets/11_security/temp_frames/f_*.png"))
clean_sec = []
master_owl = Image.open("mascots/owluko/assets/00_idle/static.png").convert("RGBA")
master_belly = master_owl.crop((185, 270, 325, 410))

for rf in raw_sec:
    raw_img = Image.open(rf)
    cf = perfect_matte_and_harmonize_v2(raw_img)
    
    draw_mask = np.zeros((master_belly.height, master_belly.width), dtype=np.uint8)
    cv2.circle(draw_mask, (draw_mask.shape[1]//2, draw_mask.shape[0]//2), 48, 255, -1)
    draw_mask = cv2.GaussianBlur(draw_mask, (21, 21), 0)
    soft_mask = Image.fromarray(draw_mask)
    
    cf.paste(master_belly, (185, 270), soft_mask)
    clean_sec.append(cf)

d11 = "mascots/owluko/assets/11_security"
clean_sec[min(35, len(clean_sec)-1)].save(f"{d11}/static.png", optimize=True)
clean_sec[min(35, len(clean_sec)-1)].save(f"{d11}/static.webp", quality=92)
clean_sec[0].save(f"{d11}/animated.png", save_all=True, append_images=clean_sec[1:], duration=41, loop=0)
clean_sec[0].save(f"{d11}/animated.webp", save_all=True, append_images=clean_sec[1:], duration=41, loop=0, quality=88, method=4)

gif_frames = []
for f in clean_sec:
    alpha = f.split()[3]
    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
    p_frame = f.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE)
    p_frame.paste(255, mask)
    p_frame.info['transparency'] = 255
    gif_frames.append(p_frame)
gif_frames[0].save(f"{d11}/animated.gif", save_all=True, append_images=gif_frames[1:], duration=41, loop=0, disposal=2)

print("✅ Perfect alpha matte applied to Owluko 08 and 11!")
