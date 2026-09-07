import os
import glob
import subprocess
import numpy as np
from PIL import Image
from scipy import ndimage

DEV_LUNEKO = "/Users/richard/Developer/Stickers 3D/mascots/luneko/assets"
DOWN_LUNEKO = "/Users/richard/Downloads/Stickers 3D/mascots/luneko/assets"

states = sorted(os.listdir(DOWN_LUNEKO))

for s in states:
    state_dir = os.path.join(DOWN_LUNEKO, s)
    if not os.path.isdir(state_dir):
        continue
    
    raw_mp4 = f"{state_dir}/source_video.mp4"
    looped_mp4 = f"{state_dir}/looped_video.mp4"
    
    # If we have looped_mp4 or source_video.mp4
    video_to_use = looped_mp4 if os.path.exists(looped_mp4) else (raw_mp4 if os.path.exists(raw_mp4) else None)
    
    temp_dir = f"/tmp/luneko_fix_{s}"
    shutil_rm = False
    if video_to_use:
        os.makedirs(temp_dir, exist_ok=True)
        # Extract pure RGB frames
        subprocess.run([
            "ffmpeg", "-y", "-i", video_to_use,
            "-vf", "crop=720:720:280:0,fps=24,scale=512:512",
            f"{temp_dir}/f_%03d.png"
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        frame_files = sorted(glob.glob(f"{temp_dir}/f_*.png"))
        if not frame_files:
            continue
            
        clean_frames = []
        for fp in frame_files:
            img = Image.open(fp).convert("RGB")
            arr = np.array(img, dtype=np.float32)
            r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
            
            # The background is purely outside the character: floodfill from corners
            # Pure chroma green background has G > 120 and G > R + 30 and G > B + 30
            is_green_bg = (g > 100) & (g > r + 25) & (g > b + 25)
            
            # Character mask is everything NOT background, with all internal holes filled
            labeled, num_features = ndimage.label(is_green_bg)
            # Find label of top-left corner (0,0) which is guaranteed to be background
            bg_label = labeled[0, 0]
            
            # Background is all pixels connected to the border background
            actual_bg = (labeled == bg_label)
            # Character is everything else
            char_mask = ~actual_bg
            # Fill any possible internal hole
            char_mask = ndimage.binary_fill_holes(char_mask)
            
            # Smooth edges
            dist = ndimage.distance_transform_edt(char_mask)
            alpha = np.clip(dist, 0.0, 1.0) * 255.0
            
            # Despill: clamp green channel to max(r, b) where character touches green border
            max_rb = np.maximum(r, b)
            despilled_g = np.where((g > max_rb) & (alpha > 0), max_rb, g)
            
            clean_rgba = np.dstack([r, despilled_g, b, alpha]).astype(np.uint8)
            clean_pil = Image.fromarray(clean_rgba, mode="RGBA")
            clean_frames.append(clean_pil)
            
        if clean_frames:
            # Save static & animated
            clean_frames[0].save(f"{state_dir}/static.png", optimize=True)
            clean_frames[0].save(f"{state_dir}/static.webp", quality=92)
            clean_frames[0].save(
                f"{state_dir}/animated.webp",
                save_all=True,
                append_images=clean_frames[1:],
                duration=41,
                loop=0,
                quality=90,
                method=4
            )
            
            # GIF
            out_gif = f"{state_dir}/animated.gif"
            temp_clean = f"/tmp/luneko_clean_{s}"
            os.makedirs(temp_clean, exist_ok=True)
            for idx, cf in enumerate(clean_frames):
                cf.save(f"{temp_clean}/f_{idx:03d}.png")
            subprocess.run([
                "ffmpeg", "-y", "-i", f"{temp_clean}/f_%03d.png",
                "-vf", "fps=20,split[s0][s1];[s0]palettegen=reserve_transparent=1[p];[s1][p]paletteuse=alpha_threshold=128",
                out_gif
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Sync to dev
            dev_state_dir = os.path.join(DEV_LUNEKO, s)
            os.makedirs(dev_state_dir, exist_ok=True)
            subprocess.run(f'cp -R "{state_dir}/"* "{dev_state_dir}/"', shell=True)
            print(f"✅ Luneko {s} réparé (0 trou, 100% plein) !")

print("🎉 Tous les états de Luneko sont nettoyés sans aucun trou !")
