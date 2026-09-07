from PIL import Image
import numpy as np
import cv2

# Load clean outspread wings animation from 02_celebrating
anim_wings = Image.open("mascots/owluko/assets/02_celebrating/animated.png")
frames_pure_guardian = []

for idx in range(getattr(anim_wings, 'n_frames', 1)):
    anim_wings.seek(idx)
    f = anim_wings.convert("RGBA")
    frames_pure_guardian.append(f)

d11_owl = "mascots/owluko/assets/11_security"
frames_pure_guardian[min(35, len(frames_pure_guardian)-1)].save(f"{d11_owl}/static.png", optimize=True)
frames_pure_guardian[min(35, len(frames_pure_guardian)-1)].save(f"{d11_owl}/static.webp", quality=92)
frames_pure_guardian[0].save(f"{d11_owl}/animated.png", save_all=True, append_images=frames_pure_guardian[1:], duration=41, loop=0)
frames_pure_guardian[0].save(f"{d11_owl}/animated.webp", save_all=True, append_images=frames_pure_guardian[1:], duration=41, loop=0, quality=88, method=4)

gif_frames = []
for f in frames_pure_guardian:
    alpha = f.split()[3]
    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
    p_frame = f.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE)
    p_frame.paste(255, mask)
    p_frame.info['transparency'] = 255
    gif_frames.append(p_frame)
gif_frames[0].save(f"{d11_owl}/animated.gif", save_all=True, append_images=gif_frames[1:], duration=41, loop=0, disposal=2)

print("✅ Pure protective guardian stance applied to Owluko 11_security!")
