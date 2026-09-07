import os
import glob
import subprocess
from PIL import Image
from process_all_luneko_states import key_luneko_ultimate

mascots = ["aituko", "owluko", "luneko", "usako", "inuko", "hatoko"]
mb_dir = "preview/moodboards/00_idle"
os.makedirs(mb_dir, exist_ok=True)

for m in mascots:
    m_dir = "assets/00_idle" if m == "aituko" else f"mascots/{m}/assets/00_idle"
    raw_mp4 = f"{m_dir}/source_video.mp4"
    looped_mp4 = f"{m_dir}/looped_video.mp4"
    temp_dir = f"{m_dir}/temp_frames"
    os.makedirs(temp_dir, exist_ok=True)
    
    print(f"🎬 Processing REAL Veo video for {m.upper()}...")
    
    # 1. Create ping-pong loop 4s @ 24fps
    subprocess.run([
        "ffmpeg", "-y", "-t", "2.0", "-i", raw_mp4,
        "-filter_complex", "[0:v]split[v1][v2];[v2]reverse[v2rev];[v1][v2rev]concat=n=2:v=1[v]",
        "-map", "[v]", "-r", "24", "-c:v", "libx264", "-pix_fmt", "yuv420p", looped_mp4
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 2. Extract 512x512 square frames
    for old_f in glob.glob(f"{temp_dir}/*"):
        os.remove(old_f)
    subprocess.run([
        "ffmpeg", "-y", "-i", looped_mp4,
        "-vf", "crop=720:720:280:0,fps=24,scale=512:512",
        f"{temp_dir}/f_%03d.png"
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 3. Key all frames with solid matte
    raw_frames = sorted(glob.glob(f"{temp_dir}/f_*.png"))
    clean_frames = [key_luneko_ultimate(Image.open(rf)) for rf in raw_frames]
    
    # 4. Save formats
    mid_idx = min(24, len(clean_frames) - 1)
    clean_frames[mid_idx].save(f"{m_dir}/static.png")
    clean_frames[mid_idx].save(f"{m_dir}/static.webp", quality=92)
    clean_frames[mid_idx].save(f"{mb_dir}/{m}_static.png")
    
    clean_frames[0].save(f"{m_dir}/animated.webp", save_all=True, append_images=clean_frames[1:], duration=41, loop=0, quality=88, method=4)
    clean_frames[0].save(f"{m_dir}/animated.png", save_all=True, append_images=clean_frames[1:], duration=41, loop=0)
    
    gif_frames = []
    for f in clean_frames:
        alpha = f.split()[3]
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        p_frame = f.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE)
        p_frame.paste(255, mask)
        p_frame.info['transparency'] = 255
        gif_frames.append(p_frame)
        
    gif_frames[0].save(f"{m_dir}/animated.gif", save_all=True, append_images=gif_frames[1:], duration=41, loop=0, disposal=2)
    gif_frames[0].save(f"{mb_dir}/{m}_animated.gif", save_all=True, append_images=gif_frames[1:], duration=41, loop=0, disposal=2)
    
    print(f"✅ {m.upper()} : {len(clean_frames)} frames détourées et encodées !")

print("🎉 TOUTES LES VRAIES BOUCLES VÉO SONT PRÊTES !")
