import os
import math
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

# 1. Base AItuko (Smiling with cyan eyes, head slightly tilted)
# Let's use clean AItuko looking happy
base_aituko = Image.open("assets/00_idle/static.png").convert("RGBA")

# 2. Cyan Discrete Lightbulb
bulb_cyan = Image.open("preview/aituko_discrete_cyan_bulb.png").convert("RGBA")

# 3. Generate 96 frames seamless loop
TOTAL_FRAMES = 96
frames = []

for i in range(TOTAL_FRAMES):
    phase = 2.0 * math.pi * (i / TOTAL_FRAMES)
    
    # Breathing float for character
    dy_char = -2.5 * math.sin(phase)
    
    # Bulb floating and subtle pulsing glow
    dy_bulb = -3.5 * math.sin(phase + 0.3)
    bulb_scale = 1.0 + 0.04 * math.sin(phase * 2.0)
    
    bw = int(bulb_cyan.width * bulb_scale)
    bh = int(bulb_cyan.height * bulb_scale)
    b_resized = bulb_cyan.resize((bw, bh), Image.Resampling.LANCZOS)
    
    # Canvas
    f = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    
    # Paste character
    f.paste(base_aituko, (0, int(dy_char)), base_aituko)
    
    # Paste bulb at exact discrete position (x=325, y=45)
    bx = 325 - (bw - bulb_cyan.width) // 2
    by = int(45 + dy_bulb)
    
    # Add subtle soft cyan glow behind bulb
    glow = Image.new("RGBA", (80, 80), (0, 0, 0, 0))
    glow_arr = np.zeros((80, 80, 4), dtype=np.uint8)
    cv2.circle(glow_arr, (40, 40), 28, (0, 229, 255, int(50 + 25 * math.sin(phase * 2.0))), -1)
    glow_img = Image.fromarray(glow_arr).filter(ImageFilter.GaussianBlur(radius=8))
    
    f.paste(glow_img, (bx - 12, by - 5), glow_img)
    f.paste(b_resized, (bx, by), b_resized)
    
    frames.append(f)

# Save preview files
os.makedirs("preview", exist_ok=True)
frames[min(20, len(frames)-1)].save("preview/aituko_idea_discrete_static.png")

gif_frames = []
for f in frames:
    alpha = f.split()[3]
    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
    p_frame = f.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE)
    p_frame.paste(255, mask)
    p_frame.info['transparency'] = 255
    gif_frames.append(p_frame)

gif_frames[0].save("preview/aituko_idea_discrete_preview.gif", save_all=True, append_images=gif_frames[1:], duration=41, loop=0, disposal=2)

# Also create side-by-side comparison with Owluko idea
owl_static = Image.open("mascots/owluko/assets/10_idea/static.png").resize((256, 256), Image.Resampling.LANCZOS)
ait_static = frames[20].resize((256, 256), Image.Resampling.LANCZOS)

comp = Image.new("RGBA", (540, 280), (23, 23, 25, 255))
comp.paste(owl_static, (10, 12), owl_static)
comp.paste(ait_static, (274, 12), ait_static)
comp.save("preview/idea_comparison_owl_vs_aituko.png")

print("Saved preview/aituko_idea_discrete_static.png and preview/idea_comparison_owl_vs_aituko.png!")
