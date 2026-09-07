import os
import sys
import time
import glob
import shutil
import subprocess
import numpy as np
from PIL import Image
from google import genai
from google.genai import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/richard/Downloads/Stickers 3D/stickers-3d-7659bde46f1f.json"
client = genai.Client(vertexai=True, project="stickers-3d", location="us-central1")

BASE_DOWN = "/Users/richard/Downloads/Stickers 3D"
BASE_DEV = "/Users/richard/Developer/Stickers 3D"

LUNEKO_MASTER = f"{BASE_DOWN}/mascots/luneko/master/luneko_greenscreen_master.jpg"
USAKO_MASTER = f"{BASE_DOWN}/mascots/usako/master/usako_greenscreen_master.jpg"

TASKS = [
    {
        "mascot": "luneko",
        "pose": "08_searching",
        "master": LUNEKO_MASTER,
        "prompt": "Starts from the neutral resting stance on solid chroma green (#00FF00). The cute 3D porcelain kitten Luneko holds a stylized 3D magnifying glass with an orange ceramic rim, round wooden handle, and clear transparent refractive glass lens in its right paw, looking curiously through the lens from left to right, smooth 3D character animation."
    },
    {
        "mascot": "luneko",
        "pose": "03_ai_thinking",
        "master": LUNEKO_MASTER,
        "prompt": "Starts from the neutral resting stance on solid chroma green (#00FF00). The cute 3D porcelain kitten Luneko tilts its head to the side and rests its right front paw under its chin in deep thoughtful contemplation, looking slightly upward in focus, smooth 3D character animation."
    },
    {
        "mascot": "luneko",
        "pose": "10_idea",
        "master": LUNEKO_MASTER,
        "prompt": "Starts from the neutral resting stance on solid chroma green (#00FF00). The cute 3D porcelain kitten Luneko perks up happily with an excited eureka expression as a bright glowing stylized 3D yellow lightbulb with golden filament hovers 15cm above its head with sparkle rays, smooth 3D character animation."
    },
    {
        "mascot": "usako",
        "pose": "10_idea",
        "master": USAKO_MASTER,
        "prompt": "Starts from the neutral resting stance on solid chroma green (#00FF00). The cute 3D agile bunny Usako does a cheerful perk-up with an excited eureka moment as a bright glowing stylized 3D yellow lightbulb with golden filament hovers above its head between its long ears, smooth 3D character animation."
    }
]

def clean_hsv_key(img_pil):
    arr = np.array(img_pil.convert("RGB"), dtype=np.float32)
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    
    # RGB to HSV calculation
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    diff = max_c - min_c
    
    # Saturation (0 to 1)
    s = np.zeros_like(max_c)
    mask = max_c > 0
    s[mask] = diff[mask] / max_c[mask]
    
    # Value (0 to 255)
    v = max_c
    
    # Green backdrop criteria: high saturation, green dominant
    # Background must be distinctly green: G is max channel, G > R + 20, G > B + 20, S > 0.35, V > 40
    is_bg = (g == max_c) & (g > r + 20) & (g > b + 20) & (s > 0.35) & (v > 40)
    
    # Character alpha: 255 for character, 0 for green background
    alpha = np.where(is_bg, 0.0, 255.0)
    
    # Despill: neutralize green reflections on white fur
    max_rb = np.maximum(r, b)
    despilled_g = np.where((g > max_rb) & (alpha > 0), max_rb, g)
    
    clean_rgba = np.dstack([r, despilled_g, b, alpha]).astype(np.uint8)
    return Image.fromarray(clean_rgba, mode="RGBA")

def run():
    for idx, t in enumerate(TASKS, 1):
        m = t["mascot"]
        p = t["pose"]
        prompt = t["prompt"]
        master = t["master"]
        
        out_down_dir = f"{BASE_DOWN}/mascots/{m}/assets/{p}"
        out_dev_dir = f"{BASE_DEV}/mascots/{m}/assets/{p}"
        os.makedirs(out_down_dir, exist_ok=True)
        os.makedirs(out_dev_dir, exist_ok=True)
        
        temp_dir = f"{out_down_dir}/temp_frames"
        os.makedirs(temp_dir, exist_ok=True)
        raw_mp4 = f"{out_down_dir}/source_video.mp4"
        looped_mp4 = f"{out_down_dir}/looped_video.mp4"
        
        print(f"\n[{idx}/{len(TASKS)}] 🎬 Veo 3.1 pour {m.upper()} -> {p}...")
        t0 = time.time()
        
        with open(master, "rb") as f:
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
            print(f"   ... ({elapsed}s) Rendu Veo 3.1 {m} {p}")
            time.sleep(8)
            op = client.operations.get(op)
            
        if not op.response or not op.response.generated_videos:
            print(f"❌ Erreur sur {m} {p}: {op.error}")
            continue
            
        vid = op.response.generated_videos[0].video
        if hasattr(vid, "video_bytes") and vid.video_bytes:
            with open(raw_mp4, "wb") as f:
                f.write(vid.video_bytes)
        elif hasattr(vid, "uri"):
            client.files.download(file=vid.uri, destination=raw_mp4)
            
        # Loop ping pong
        subprocess.run([
            "ffmpeg", "-y", "-t", "2.0", "-i", raw_mp4,
            "-filter_complex", "[0:v]split[v1][v2];[v2]reverse[v2rev];[v1][v2rev]concat=n=2:v=1[v]",
            "-map", "[v]", "-r", "24", "-c:v", "libx264", "-pix_fmt", "yuv420p", looped_mp4
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Extract frames
        subprocess.run([
            "ffmpeg", "-y", "-i", looped_mp4,
            "-vf", "crop=720:720:280:0,fps=24,scale=512:512",
            f"{temp_dir}/f_%03d.png"
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        frame_files = sorted(glob.glob(f"{temp_dir}/f_*.png"))
        clean_pils = [clean_hsv_key(Image.open(f)) for f in frame_files]
        
        if clean_pils:
            clean_pils[0].save(f"{out_down_dir}/static.png", optimize=True)
            clean_pils[0].save(f"{out_down_dir}/static.webp", quality=92)
            clean_pils[0].save(
                f"{out_down_dir}/animated.webp",
                save_all=True,
                append_images=clean_pils[1:],
                duration=41,
                loop=0,
                quality=90,
                method=4
            )
            out_gif = f"{out_down_dir}/animated.gif"
            temp_clean = f"{out_down_dir}/temp_clean"
            os.makedirs(temp_clean, exist_ok=True)
            for i_f, cp in enumerate(clean_pils):
                cp.save(f"{temp_clean}/f_{i_f:03d}.png")
            subprocess.run([
                "ffmpeg", "-y", "-i", f"{temp_clean}/f_%03d.png",
                "-vf", "fps=20,split[s0][s1];[s0]palettegen=reserve_transparent=1[p];[s1][p]paletteuse=alpha_threshold=128",
                out_gif
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Sync to Dev
            subprocess.run(f'cp -R "{out_down_dir}/"* "{out_dev_dir}/"', shell=True)
            
            # Cleanup
            shutil.rmtree(temp_dir, ignore_errors=True)
            shutil.rmtree(temp_clean, ignore_errors=True)
            if os.path.exists(raw_mp4): os.remove(raw_mp4)
            if os.path.exists(looped_mp4): os.remove(looped_mp4)
            if os.path.exists(f"{out_dev_dir}/source_video.mp4"): os.remove(f"{out_dev_dir}/source_video.mp4")
            if os.path.exists(f"{out_dev_dir}/looped_video.mp4"): os.remove(f"{out_dev_dir}/looped_video.mp4")
            print(f"✅ {m} {p} terminé avec perfection absolue en {round(time.time() - t0, 1)}s !")

if __name__ == "__main__":
    run()
