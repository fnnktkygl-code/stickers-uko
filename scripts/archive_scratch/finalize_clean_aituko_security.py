import os
import glob
import subprocess
from PIL import Image
from process_all_luneko_states import key_luneko_ultimate

raw_mp4 = "preview/test_veo_aituko_small_hands.mp4"
looped_mp4 = "assets/11_security/looped_video.mp4"
temp_dir = "assets/11_security/temp_frames"

os.makedirs("assets/11_security", exist_ok=True)
os.makedirs("mascots/aituko/assets/11_security", exist_ok=True)
os.makedirs(temp_dir, exist_ok=True)

# 1. Copy source video
subprocess.run(["cp", raw_mp4, "assets/11_security/source_video.mp4"], check=True)
subprocess.run(["cp", raw_mp4, "mascots/aituko/assets/11_security/source_video.mp4"], check=True)

# 2. Ping-pong loop
print("🎬 Création du looped_video.mp4...")
subprocess.run([
    "ffmpeg", "-y", "-t", "2.0", "-i", raw_mp4,
    "-filter_complex", "[0:v]split[v1][v2];[v2]reverse[v2rev];[v1][v2rev]concat=n=2:v=1[v]",
    "-map", "[v]", "-r", "24", "-c:v", "libx264", "-pix_fmt", "yuv420p", looped_mp4
], check=True)
subprocess.run(["cp", looped_mp4, "mascots/aituko/assets/11_security/looped_video.mp4"], check=True)

# 3. Extract frames
for old in glob.glob(f"{temp_dir}/*"):
    os.remove(old)
print("🎞️ Extraction des frames 512x512...")
subprocess.run([
    "ffmpeg", "-y", "-i", looped_mp4,
    "-vf", "crop=720:720:280:0,fps=24,scale=512:512",
    f"{temp_dir}/f_%03d.png"
], check=True)

# 4. Matte all frames
print("🟢 Détourage mathématique...")
raw_frames = sorted(glob.glob(f"{temp_dir}/f_*.png"))
clean_frames = [key_luneko_ultimate(Image.open(rf)) for rf in raw_frames]

# 5. Export formats
print("📦 Encodage static et animations...")
for target_dir in ["assets/11_security", "mascots/aituko/assets/11_security"]:
    clean_frames[min(35, len(clean_frames)-1)].save(f"{target_dir}/static.png", optimize=True)
    clean_frames[min(35, len(clean_frames)-1)].save(f"{target_dir}/static.webp", quality=92)
    clean_frames[0].save(f"{target_dir}/animated.png", save_all=True, append_images=clean_frames[1:], duration=41, loop=0)
    clean_frames[0].save(f"{target_dir}/animated.webp", save_all=True, append_images=clean_frames[1:], duration=41, loop=0, quality=88, method=4)
    
    gif_frames = []
    for f in clean_frames:
        alpha = f.split()[3]
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        p_frame = f.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE)
        p_frame.paste(255, mask)
        p_frame.info['transparency'] = 255
        gif_frames.append(p_frame)
    gif_frames[0].save(f"{target_dir}/animated.gif", save_all=True, append_images=gif_frames[1:], duration=41, loop=0, disposal=2)

print("🎉 AItuko 11_security FINALISÉ AVEC DE PETITES MAINS PROPORTIONNELLES PARFAITES !")
