import os
import math
import cv2
import numpy as np
from PIL import Image
from process_all_luneko_states import key_luneko_ultimate

mascots = [
    ("aituko", "assets/00_idle/static.png", "AItuko (Robot)", False),
    ("owluko", "mascots/owluko/assets/00_idle/static.png", "Owluko (Chouette)", False),
    ("luneko", "mascots/luneko/assets/00_idle/static.png", "Luneko (Chat)", False),
    ("usako", "mascots/usako/master/usako_greenscreen_master.jpg", "Usako (Lapin)", True),
    ("inuko", "mascots/inuko/assets/01_waving/static.png", "Inuko (Doberman)", False),
    ("hatoko", "mascots/hatoko/master/hatoko_greenscreen_master.jpg", "Hatoko (Pigeon)", True),
]

TOTAL_FRAMES = 96
moodboard_dir = "preview/moodboards/00_idle"
os.makedirs(moodboard_dir, exist_ok=True)

processed = []
for m_key, m_path, m_title, needs_keying in mascots:
    raw = Image.open(m_path)
    clean = key_luneko_ultimate(raw) if needs_keying else raw.convert("RGBA").resize((512, 512), Image.Resampling.LANCZOS)
    
    # Save standard mascot 00_idle assets
    m_asset_dir = "assets/00_idle" if m_key == "aituko" else f"mascots/{m_key}/assets/00_idle"
    os.makedirs(m_asset_dir, exist_ok=True)
    
    frames = []
    for i in range(TOTAL_FRAMES):
        phase = 2.0 * math.pi * (i / TOTAL_FRAMES)
        dy = -2.5 * math.sin(phase)
        f = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        f.paste(clean, (0, int(dy)), clean)
        frames.append(f)
        
    static_png = f"{moodboard_dir}/{m_key}_static.png"
    anim_gif = f"{moodboard_dir}/{m_key}_animated.gif"
    
    frames[0].save(static_png)
    frames[0].save(f"{m_asset_dir}/static.png")
    frames[0].save(f"{m_asset_dir}/static.webp", quality=92)
    frames[0].save(f"{m_asset_dir}/animated.webp", save_all=True, append_images=frames[1:], duration=41, loop=0, quality=88, method=4)
    frames[0].save(f"{m_asset_dir}/animated.png", save_all=True, append_images=frames[1:], duration=41, loop=0)
    
    gif_frames = []
    for f in frames:
        alpha = f.split()[3]
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        p_frame = f.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE)
        p_frame.paste(255, mask)
        p_frame.info['transparency'] = 255
        gif_frames.append(p_frame)
    gif_frames[0].save(anim_gif, save_all=True, append_images=gif_frames[1:], duration=41, loop=0, disposal=2)
    gif_frames[0].save(f"{m_asset_dir}/animated.gif", save_all=True, append_images=gif_frames[1:], duration=41, loop=0, disposal=2)
    
    processed.append((m_key, m_title, static_png, anim_gif))
    print(f"✨ 00_idle pour {m_title}: OK")

# Build 6-Mascot Dark Grid
grid_dark = Image.new("RGBA", (6 * 160, 200), (23, 23, 25, 255))
for idx, (m_key, m_title, s_path, g_path) in enumerate(processed):
    im = Image.open(s_path).resize((140, 140), Image.Resampling.LANCZOS)
    grid_dark.paste(im, (idx * 160 + 10, 30), im)

grid_dark.save(f"{moodboard_dir}/moodboard_00_idle_dark_grid.png")

# Build 6-Mascot Light Grid
grid_light = Image.new("RGBA", (6 * 160, 200), (251, 251, 249, 255))
for idx, (m_key, m_title, s_path, g_path) in enumerate(processed):
    im = Image.open(s_path).resize((140, 140), Image.Resampling.LANCZOS)
    grid_light.paste(im, (idx * 160 + 10, 30), im)

grid_light.save(f"{moodboard_dir}/moodboard_00_idle_light_grid.png")
print("🎉 Moodboard 00_idle régénéré à 100% !")
