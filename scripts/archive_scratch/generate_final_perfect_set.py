import os
import sys
import time
import glob
import shutil
import subprocess
import numpy as np
from PIL import Image
from scipy import ndimage
from google import genai
from google.genai import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/richard/Downloads/Stickers 3D/stickers-3d-7659bde46f1f.json"
client = genai.Client(vertexai=True, project="stickers-3d", location="us-central1")

BASE_DOWN = "/Users/richard/Downloads/Stickers 3D"
BASE_DEV = "/Users/richard/Developer/Stickers 3D"

def perfect_key(pil_img):
    img = np.array(pil_img.convert("RGB"), dtype=np.float32)
    r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
    
    # Precise chroma green backdrop isolation (G must dominate by >= 55)
    is_green = (g > 130) & (g > r + 55) & (g > b + 55)
    
    # Label connected components
    labeled, num_features = ndimage.label(is_green)
    
    # Background MUST connect to image borders
    border_pixels = []
    border_pixels.extend(labeled[0, :].tolist())
    border_pixels.extend(labeled[-1, :].tolist())
    border_pixels.extend(labeled[:, 0].tolist())
    border_pixels.extend(labeled[:, -1].tolist())
    border_labels = set(border_pixels)
    border_labels.discard(0)
    
    true_bg = np.isin(labeled, list(border_labels))
    char_fg = ~true_bg
    char_fg = ndimage.binary_fill_holes(char_fg)
    char_fg = ndimage.binary_closing(char_fg, structure=np.ones((5,5)))
    
    dist = ndimage.distance_transform_edt(char_fg)
    alpha = np.clip(dist, 0.0, 1.0) * 255.0
    
    # Despill: clamp green channel to max(r, b) where alpha > 0
    max_rb = np.maximum(r, b)
    despilled_g = np.where((g > max_rb) & (alpha > 0), max_rb, g)
    
    rgba = np.dstack([r, despilled_g, b, alpha]).astype(np.uint8)
    return Image.fromarray(rgba, mode="RGBA")

def render_state(mascot, pose, prompt, master_path):
    out_down = f"{BASE_DOWN}/assets/{pose}" if mascot == "aituko" else f"{BASE_DOWN}/mascots/{mascot}/assets/{pose}"
    out_dev = f"{BASE_DEV}/assets/{pose}" if mascot == "aituko" else f"{BASE_DEV}/mascots/{mascot}/assets/{pose}"
    os.makedirs(out_down, exist_ok=True)
    os.makedirs(out_dev, exist_ok=True)
    
    temp_dir = f"{out_down}/temp_frames"
    os.makedirs(temp_dir, exist_ok=True)
    raw_mp4 = f"{out_down}/source_video.mp4"
    looped_mp4 = f"{out_down}/looped_video.mp4"
    
    print(f"\n🎬 Rendu Veo 3.1 pour {mascot.upper()} {pose}...")
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
        print(f"   ... ({elapsed}s) Rendu {mascot} {pose}")
        time.sleep(8)
        op = client.operations.get(op)
        
    if not op.response or not op.response.generated_videos:
        print(f"❌ Erreur sur {mascot} {pose}: {op.error}")
        return False
        
    vid = op.response.generated_videos[0].video
    if hasattr(vid, "video_bytes") and vid.video_bytes:
        with open(raw_mp4, "wb") as f:
            f.write(vid.video_bytes)
    elif hasattr(vid, "uri"):
        client.files.download(file=vid.uri, destination=raw_mp4)
        
    # Looping ping-pong
    subprocess.run([
        "ffmpeg", "-y", "-t", "2.0", "-i", raw_mp4,
        "-filter_complex", "[0:v]split[v1][v2];[v2]reverse[v2rev];[v1][v2rev]concat=n=2:v=1[v]",
        "-map", "[v]", "-r", "24", "-c:v", "libx264", "-pix_fmt", "yuv420p", looped_mp4
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Extract
    subprocess.run([
        "ffmpeg", "-y", "-i", looped_mp4,
        "-vf", "crop=720:720:280:0,fps=24,scale=512:512",
        f"{temp_dir}/f_%03d.png"
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    frame_files = sorted(glob.glob(f"{temp_dir}/f_*.png"))
    clean_pils = [perfect_key(Image.open(f)) for f in frame_files]
    
    if clean_pils:
        clean_pils[0].save(f"{out_down}/static.png", optimize=True)
        clean_pils[0].save(f"{out_down}/static.webp", quality=92)
        clean_pils[0].save(
            f"{out_down}/animated.webp",
            save_all=True,
            append_images=clean_pils[1:],
            duration=41,
            loop=0,
            quality=90,
            method=4
        )
        out_gif = f"{out_down}/animated.gif"
        temp_clean = f"{out_down}/temp_clean"
        os.makedirs(temp_clean, exist_ok=True)
        for i_f, cp in enumerate(clean_pils):
            cp.save(f"{temp_clean}/f_{i_f:03d}.png")
        subprocess.run([
            "ffmpeg", "-y", "-i", f"{temp_clean}/f_%03d.png",
            "-vf", "fps=20,split[s0][s1];[s0]palettegen=reserve_transparent=1[p];[s1][p]paletteuse=alpha_threshold=128",
            out_gif
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Mirror to dev
        subprocess.run(f'cp -R "{out_down}/"* "{out_dev}/"', shell=True)
        
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)
        shutil.rmtree(temp_clean, ignore_errors=True)
        if os.path.exists(raw_mp4): os.remove(raw_mp4)
        if os.path.exists(looped_mp4): os.remove(looped_mp4)
        if os.path.exists(f"{out_dev}/source_video.mp4"): os.remove(f"{out_dev}/source_video.mp4")
        if os.path.exists(f"{out_dev}/looped_video.mp4"): os.remove(f"{out_dev}/looped_video.mp4")
        print(f"✅ {mascot} {pose} finalisé avec perfection absolue en {round(time.time() - t0, 1)}s !")
        return True
    return False

if __name__ == "__main__":
    inuko_master = f"{BASE_DOWN}/mascots/inuko/master/inuko_greenscreen_master.jpg"
    luneko_master = f"{BASE_DOWN}/mascots/luneko/master/luneko_greenscreen_master.jpg"
    
    # 1. Inuko 10_idea (Lightbulb clearly visible floating between pointed ears)
    p_inuko_idea = "Starts from the neutral resting stance on solid chroma green (#00FF00). The cute svelte 3D Doberman Inuko tilts its head up with an excited eureka moment as a prominent glowing 3D yellow glass lightbulb with golden filament hovers brightly between its pointed ears, joyful smile, smooth 3D character animation."
    render_state("inuko", "10_idea", p_inuko_idea, inuko_master)
    
    # 2. Luneko 08_searching (Orange loupe, zero chest holes)
    p_luneko_search = "Starts from the neutral resting stance on solid chroma green (#00FF00). The cute 3D porcelain ginger cat Luneko holds a stylized 3D magnifying glass with an orange ceramic rim, round handle, and transparent glass lens in its right paw, looking through the lens from left to right with curiosity, smooth 3D character animation."
    render_state("luneko", "08_searching", p_luneko_search, luneko_master)
    
    # 3. Luneko 03_ai_thinking (Pensive pose, zero chest holes)
    p_luneko_think = "Starts from the neutral resting stance on solid chroma green (#00FF00). The cute 3D porcelain ginger cat Luneko tilts its head to the side and rests its right paw thoughtfully under its chin in deep contemplation, looking slightly upward in focus, smooth 3D character animation."
    render_state("luneko", "03_ai_thinking", p_luneko_think, luneko_master)

    print("\n🎉 MASTER PRODUCTION COMPLÈTE & PARFAITE !")
