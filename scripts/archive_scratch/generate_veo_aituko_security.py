import os
import sys
import time
import glob
import subprocess
import numpy as np
from PIL import Image
from scipy import ndimage
from google import genai
from google.genai import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/richard/Developer/Stickers Uko/stickers-3d-7659bde46f1f.json"
client = genai.Client(vertexai=True, project="stickers-3d", location="us-central1")

master_path = "mascots/aituko/master/aituko_greenscreen_master.jpg"
if not os.path.exists(master_path):
    master_path = "assets/master/bytebot_greenscreen_master.jpg"

prompt = (
    "A cute white minimalist porcelain robot mascot AItuko on solid uniform chroma green background (#00FF00). "
    "The robot raises both of its cute white porcelain hands forward in front of its body in a firm, friendly protective stop and shielding guardian gesture, with bright luminous electric cyan (#00E5FF) eyes and smile. "
    "Absolutely NO shield prop, NO holographic shield, NO neon lock, NO smoke, NO fire, NO blue plasma, NO magical effects. "
    "Smooth 3D character animation, Pixar style."
)

print(f"🎬 [1/5] Lancement de la génération vidéo Google Veo 3.1 pour AItuko 11_security...")
t0 = time.time()

with open(master_path, "rb") as f:
    m_bytes = f.read()

img_input = types.Image(image_bytes=m_bytes, mime_type="image/jpeg")

op = client.models.generate_videos(
    model="veo-3.1-fast-generate-001",
    prompt=prompt,
    image=img_input,
    config=types.GenerateVideosConfig(
        aspect_ratio="16:9",
        duration_seconds=4,
        person_generation="allow_all"
    )
)

while not op.done:
    elapsed = int(time.time() - t0)
    print(f"   ... ({elapsed}s) Rendu Google Veo 3.1 en cours...")
    time.sleep(6)
    op = client.operations.get(op)

if not op.response or not op.response.generated_videos:
    print(f"❌ Erreur Veo: {op.error}")
    sys.exit(1)

print(f"✅ Rendu Veo 3.1 terminé en {int(time.time() - t0)}s !")

vid = op.response.generated_videos[0].video
raw_mp4 = "assets/11_security/source_video.mp4"
os.makedirs("assets/11_security", exist_ok=True)
os.makedirs("mascots/aituko/assets/11_security", exist_ok=True)

if hasattr(vid, "video_bytes") and vid.video_bytes:
    with open(raw_mp4, "wb") as f:
        f.write(vid.video_bytes)
elif hasattr(vid, "uri"):
    client.files.download(file=vid.uri, destination=raw_mp4)

print(f"✅ Vidéo brute enregistrée : {raw_mp4} ({os.path.getsize(raw_mp4)} octets)")

# 2. Ping-pong seamless loop video
looped_mp4 = "assets/11_security/looped_video.mp4"
print("🎬 [2/5] Création de la vidéo bouclée looped_video.mp4...")
subprocess.run([
    "ffmpeg", "-y", "-t", "2.0", "-i", raw_mp4,
    "-filter_complex", "[0:v]split[v1][v2];[v2]reverse[v2rev];[v1][v2rev]concat=n=2:v=1[v]",
    "-map", "[v]", "-r", "24", "-c:v", "libx264", "-pix_fmt", "yuv420p", looped_mp4
], check=True)
subprocess.run(["cp", looped_mp4, "mascots/aituko/assets/11_security/looped_video.mp4"], check=True)

# 3. Extract 512x512 square frames
temp_dir = "assets/11_security/temp_frames"
os.makedirs(temp_dir, exist_ok=True)
# Clean previous temp frames
for old_f in glob.glob(f"{temp_dir}/*"):
    os.remove(old_f)

print("🎞️ [3/5] Extraction des frames 512x512...")
subprocess.run([
    "ffmpeg", "-y", "-i", looped_mp4,
    "-vf", "crop=720:720:280:0,fps=24,scale=512:512",
    f"{temp_dir}/f_%03d.png"
], check=True)

# 4. Matte and despill all frames
print("🟢 [4/5] Détourage Chroma-Key mathématique 100% sans trou...")
from process_all_luneko_states import key_luneko_ultimate

raw_frames = sorted(glob.glob(f"{temp_dir}/f_*.png"))
clean_frames = [key_luneko_ultimate(Image.open(rf)) for rf in raw_frames]

# 5. Export static and animated formats
print("📦 [5/5] Encodage static.png, static.webp, animated.webp, animated.png, animated.gif...")
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

print("🎉 AItuko 11_security ENTIÈREMENT RÉGÉNÉRÉ VIA GOOGLE VEO 3.1 & DÉTOUÉ SELON LA DOCUMENTATION DU PROJET !")
