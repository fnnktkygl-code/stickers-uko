from PIL import Image
import numpy as np
import math

hand_full = Image.open("preview/exact_open_hand.png").convert("RGBA")
arr_h = np.array(hand_full)
arr_h[:, :45] = 0
pure_hand_r = Image.fromarray(arr_h)

# Slightly smaller (90%) and angled inward
pure_hand_r = pure_hand_r.resize((int(pure_hand_r.width * 0.9), int(pure_hand_r.height * 0.9)), Image.Resampling.LANCZOS)
guard_r = pure_hand_r.rotate(18, resample=Image.Resampling.BICUBIC, expand=True)
guard_l = guard_r.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

master = Image.open("assets/00_idle/static.png").convert("RGBA")

guard_frames = []
TOTAL_FRAMES = 96

for i in range(TOTAL_FRAMES):
    phase = 2.0 * math.pi * (i / TOTAL_FRAMES)
    dy = -2.5 * math.sin(phase)
    
    frame = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    
    body_no_arms = np.array(master)
    body_no_arms[280:430, :190] = 0
    body_no_arms[280:430, 320:] = 0
    body_img = Image.fromarray(body_no_arms)
    
    frame.paste(body_img, (0, int(dy)), body_img)
    
    # Position hands firmly in front of chest
    frame.paste(guard_l, (150, int(225 + dy)), guard_l)
    frame.paste(guard_r, (260, int(225 + dy)), guard_r)
    
    guard_frames.append(frame)

guard_frames[0].save("preview/perfect_pure_aituko_guardian_v2.png")
print("Saved preview/perfect_pure_aituko_guardian_v2.png")

# Save to assets/11_security and mascots/aituko/assets/11_security
for d in ["assets/11_security", "mascots/aituko/assets/11_security"]:
    guard_frames[0].save(f"{d}/static.png", optimize=True)
    guard_frames[0].save(f"{d}/static.webp", quality=92)
    guard_frames[0].save(f"{d}/animated.png", save_all=True, append_images=guard_frames[1:], duration=41, loop=0)
    guard_frames[0].save(f"{d}/animated.webp", save_all=True, append_images=guard_frames[1:], duration=41, loop=0, quality=88, method=4)
    
    gif_frames = []
    for f in guard_frames:
        alpha = f.split()[3]
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        p_frame = f.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE)
        p_frame.paste(255, mask)
        p_frame.info['transparency'] = 255
        gif_frames.append(p_frame)
    gif_frames[0].save(f"{d}/animated.gif", save_all=True, append_images=gif_frames[1:], duration=41, loop=0, disposal=2)

print("✅ Perfect pure guardian applied to AItuko 11_security!")
