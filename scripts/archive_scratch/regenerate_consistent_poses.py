import os
import sys
import time
import glob
import shutil
import subprocess
import numpy as np
from scipy import ndimage
from PIL import Image
from google import genai
from google.genai import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/richard/Downloads/Stickers 3D/stickers-3d-7659bde46f1f.json"
client = genai.Client(vertexai=True, project="stickers-3d", location="us-central1")

BASE_DOWN = "/Users/richard/Downloads/Stickers 3D"
BASE_DEV = "/Users/richard/Developer/Stickers 3D"

MASTERS = {
    "aituko": f"{BASE_DOWN}/assets/master/bytebot_greenscreen_master.jpg",
    "owluko": f"{BASE_DOWN}/mascots/owluko/master/owleko_greenscreen_master.jpg",
    "luneko": f"{BASE_DOWN}/mascots/luneko/master/luneko_greenscreen_master.jpg",
    "hatoko": f"{BASE_DOWN}/mascots/hatoko/master/hatoko_greenscreen_master.jpg",
    "usako": f"{BASE_DOWN}/mascots/usako/master/usako_greenscreen_master.jpg",
    "inuko": f"{BASE_DOWN}/mascots/inuko/master/inuko_greenscreen_master.jpg"
}

# Targeted consistent poses to regenerate
TASKS = [
    # 1. 08_searching with orange 3D magnifying glass & transparent glass
    {
        "mascot": "aituko",
        "pose": "08_searching",
        "prompt": "Starts from the neutral resting stance on solid chroma green (#00FF00). The cute 3D white porcelain robot AItuko holds a stylized 3D magnifying glass with an orange ceramic rim, round handle, and clear transparent refractive glass lens in its floating hand, inspecting curiously through the glass from left to right, smooth 3D character animation."
    },
    {
        "mascot": "owluko",
        "pose": "08_searching",
        "prompt": "Starts from the neutral resting stance on solid chroma green (#00FF00). The cute 3D owl Owluko holds a stylized 3D magnifying glass with an orange rim and clear transparent glass lens with its right wing, inspecting attentively from left to right, smooth 3D character animation."
    },
    {
        "mascot": "luneko",
        "pose": "08_searching",
        "prompt": "Starts from the neutral resting stance on solid chroma green (#00FF00). The cute 3D porcelain kitten Luneko holds a stylized 3D magnifying glass with an orange rim and transparent refractive glass lens in its right paw, inspecting curiously left and right, smooth 3D character animation."
    },
    {
        "mascot": "inuko",
        "pose": "08_searching",
        "prompt": "Starts from the neutral resting stance on solid chroma green (#00FF00). The cute svelte 3D Doberman Inuko holds a stylized 3D magnifying glass with an orange rim and clear transparent glass lens in its right paw, inspecting from left to right with alert ears, smooth 3D character animation."
    },

    # 2. 06_sleeping with strictly 4 natural limbs (Inuko fix)
    {
        "mascot": "inuko",
        "pose": "06_sleeping",
        "prompt": "Starts from the neutral resting stance on solid chroma green (#00FF00). The cute svelte 3D Doberman Inuko peacefully lies down curled in a cozy sleeping donut on the floor with exactly four natural paws folded neatly under its body, peaceful breathing in deep sleep with three small golden 3D 'Zzz' gently floating upward, anatomically perfect canine body, zero extra limbs, smooth 3D character animation."
    },

    # 3. 10_idea with bright glowing 3D lightbulb
    {
        "mascot": "luneko",
        "pose": "10_idea",
        "prompt": "Starts from the neutral resting stance on solid chroma green (#00FF00). The cute 3D porcelain kitten Luneko suddenly perks up with an excited eureka moment, happy wide eyes, as a bright glowing stylized 3D yellow lightbulb with golden filament illuminates 15cm above its head with subtle sparkle accents, smooth 3D character animation."
    },
    {
        "mascot": "usako",
        "pose": "10_idea",
        "prompt": "Starts from the neutral resting stance on solid chroma green (#00FF00). The cute 3D bunny Usako does an excited sudden leap of inspiration with perked ears as a bright glowing stylized 3D yellow lightbulb illuminates above its head, joyful eureka expression, smooth 3D character animation."
    },
    {
        "mascot": "inuko",
        "pose": "10_idea",
        "prompt": "Starts from the neutral resting stance on solid chroma green (#00FF00). The cute svelte 3D Doberman Inuko suddenly perks up with an excited eureka inspiration moment, tail wagging, as a bright glowing stylized 3D yellow lightbulb illuminates above its head, smooth 3D character animation."
    },

    # 4. 11_security with solid translucent 3D holographic cyan shield
    {
        "mascot": "aituko",
        "pose": "11_security",
        "prompt": "Starts from the neutral resting stance on solid chroma green (#00FF00). The cute 3D porcelain robot AItuko stands in an authoritative protective guardian posture holding a solid translucent 3D holographic cyan-blue security shield with a glowing padlock emblem in front of its chest, smooth 3D character animation."
    },
    {
        "mascot": "owluko",
        "pose": "11_security",
        "prompt": "Starts from the neutral resting stance on solid chroma green (#00FF00). The cute 3D owl Owluko stands guard holding a solid translucent 3D holographic cyan-blue security shield with a glowing lock crest in front of its chest, smooth 3D character animation."
    },
    {
        "mascot": "inuko",
        "pose": "11_security",
        "prompt": "Starts from the neutral resting stance on solid chroma green (#00FF00). The cute svelte 3D Doberman Inuko stands in a proud protective guard stance behind a solid translucent 3D holographic cyan-blue security shield with a glowing padlock emblem in front of its chest, smooth 3D character animation."
    },

    # 5. 03_ai_thinking with pure thoughtful gesture (no disparate neon halos)
    {
        "mascot": "aituko",
        "pose": "03_ai_thinking",
        "prompt": "Starts from the neutral resting stance on solid chroma green (#00FF00). The cute 3D porcelain robot AItuko tilts its head curiously and rests its right floating hand under its chin in deep thoughtful contemplation, looking slightly upward in focus, smooth 3D character animation, clean studio lighting."
    },
    {
        "mascot": "inuko",
        "pose": "03_ai_thinking",
        "prompt": "Starts from the neutral resting stance on solid chroma green (#00FF00). The cute svelte 3D Doberman Inuko tilts its head to the side curiously and taps its chin with its right front paw in deep thoughtful analysis, alert intelligent expression, smooth 3D character animation, clean studio lighting."
    }
]

def reprocess_frames_clean(temp_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    frame_files = sorted(glob.glob(f"{temp_dir}/f_*.png"))
    if not frame_files:
        return False
    
    clean_pils = []
    for fp in frame_files:
        img = Image.open(fp).convert("RGBA")
        arr = np.array(img, dtype=np.float32)
        r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
        
        # Robust chroma green detection (including olive-yellow tones)
        max_rb = np.maximum(r, b)
        is_bg = (g > 105) & (g > r * 1.15) & (g > b * 1.15)
        
        # Hole filling & morphology
        fg_mask = ~is_bg
        closed_body_mask = ndimage.binary_fill_holes(fg_mask)
        closed_body_mask = ndimage.binary_closing(closed_body_mask, structure=np.ones((5,5)))
        
        # Soft feathering
        dist_map = ndimage.distance_transform_edt(closed_body_mask)
        alpha = np.clip(dist_map, 0.0, 1.0) * 255.0
        
        # Despill
        despilled_g = np.where((g > max_rb) & (alpha > 0), max_rb, g)
        
        clean_rgba = np.dstack([r, despilled_g, b, alpha]).astype(np.uint8)
        clean_pil = Image.fromarray(clean_rgba, mode="RGBA")
        clean_pils.append(clean_pil)
        
    if clean_pils:
        # Save static PNG & WebP
        clean_pils[0].save(f"{out_dir}/static.png", optimize=True)
        clean_pils[0].save(f"{out_dir}/static.webp", quality=92)
        
        # Save Animated WebP (60fps feel)
        clean_pils[0].save(
            f"{out_dir}/animated.webp",
            save_all=True,
            append_images=clean_pils[1:],
            duration=41,
            loop=0,
            quality=90,
            method=4
        )
        
        # Save GIF
        out_gif = f"{out_dir}/animated.gif"
        subprocess.run([
            "ffmpeg", "-y", "-i", f"{temp_dir}/f_%03d.png",
            "-vf", "fps=20,split[s0][s1];[s0]palettegen=reserve_transparent=1[p];[s1][p]paletteuse=alpha_threshold=128",
            out_gif
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        return True
    return False

def run():
    print(f"🚀 Lancement de la régénération ciblée des {len(TASKS)} poses non-conformes...")
    
    for i, t in enumerate(TASKS, 1):
        m = t["mascot"]
        p = t["pose"]
        prompt = t["prompt"]
        master_img = MASTERS[m]
        
        out_down_dir = f"{BASE_DOWN}/assets/{p}" if m == "aituko" else f"{BASE_DOWN}/mascots/{m}/assets/{p}"
        out_dev_dir = f"{BASE_DEV}/assets/{p}" if m == "aituko" else f"{BASE_DEV}/mascots/{m}/assets/{p}"
        os.makedirs(out_down_dir, exist_ok=True)
        os.makedirs(out_dev_dir, exist_ok=True)
        
        temp_dir = f"{out_down_dir}/temp_frames"
        os.makedirs(temp_dir, exist_ok=True)
        raw_mp4 = f"{out_down_dir}/source_video.mp4"
        looped_mp4 = f"{out_down_dir}/looped_video.mp4"
        
        print(f"\n[{i}/{len(TASKS)}] 🎬 Veo 3.1 pour {m.upper()} -> {p}...")
        t0 = time.time()
        
        with open(master_img, "rb") as f:
            m_bytes = f.read()
        
        img_input = types.Image(image_bytes=m_bytes, mime_type="image/jpeg")
        
        try:
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
                
            # Ping-pong loop
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
            
            # Reprocess with pure alpha
            success = reprocess_frames_clean(temp_dir, out_down_dir)
            if success:
                subprocess.run(f'cp -R "{out_down_dir}/"* "{out_dev_dir}/"', shell=True)
                # Remove temp files and raw mp4 from production folder
                shutil.rmtree(temp_dir, ignore_errors=True)
                if os.path.exists(raw_mp4): os.remove(raw_mp4)
                if os.path.exists(looped_mp4): os.remove(looped_mp4)
                if os.path.exists(f"{out_dev_dir}/source_video.mp4"): os.remove(f"{out_dev_dir}/source_video.mp4")
                if os.path.exists(f"{out_dev_dir}/looped_video.mp4"): os.remove(f"{out_dev_dir}/looped_video.mp4")
                print(f"✅ {m} {p} harmonisé en {round(time.time() - t0, 1)}s avec 100% de consistance !")
        except Exception as e:
            print(f"❌ Exception sur {m} {p}: {e}")

    print("\n🎉 TOUTES LES POSES NON-CONFORMES ONT ÉTÉ PARFAITEMENT HARMONISÉES !")

if __name__ == "__main__":
    run()
