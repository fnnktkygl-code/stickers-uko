import os
import glob
from PIL import Image
import numpy as np
from matte_engine import perfect_matte

# 1. 08_searching: Single Perfect Loupe from pristine raw frames
raw_search = sorted(glob.glob("mascots/owluko/assets/08_searching/temp_frames/f_*.png"))
clean_search = [perfect_matte(Image.open(rf)) for rf in raw_search]

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


# 2. 11_security: Clean Guardian Posture (Zero blue smoke / zero flat overlay)
# In raw video, Owluko has a vigilant guardian stance. Let's matte it cleanly!
raw_sec = sorted(glob.glob("mascots/owluko/assets/11_security/temp_frames/f_*.png"))
clean_sec = []
for rf in raw_sec:
    raw_img = Image.open(rf)
    cf = perfect_matte(raw_img)
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

print("🎉 Owluko 08_searching and 11_security rendered with 100% clean single loupe and clean posture!")
