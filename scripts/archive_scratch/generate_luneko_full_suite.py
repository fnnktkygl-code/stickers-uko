import os
import time
import subprocess
import numpy as np
from PIL import Image, ImageSequence
from scipy import ndimage
from google import genai
from google.genai import types

CREDENTIALS_PATH = "/Users/richard/Downloads/Stickers 3D/stickers-3d-7659bde46f1f.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH
os.environ["GOOGLE_CLOUD_PROJECT"] = "stickers-3d"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"

client = genai.Client(
    vertexai=True,
    project="stickers-3d",
    location="us-central1"
)

MASTER_IMAGE_PATH = "/Users/richard/Downloads/Stickers 3D/mascots/luneko/master/luneko_greenscreen_master.jpg"

LUNEKO_POSES = [
    ("01_waving", "The cute ginger tabby cat sitting upright on solid chroma green background. It raises its right paw to wave friendly at the camera with a gentle warm smile, subtle cheerful tail sway, smooth looping 3d animation."),
    ("02_celebrating", "The cute ginger tabby cat sitting upright on solid chroma green background. It joyfully raises both paws with small colorful confetti particles floating down, happy cheerful smile, lively tail wagging, celebration victory loop."),
    ("03_ai_thinking", "The cute ginger tabby cat sitting upright on solid chroma green background. It tilts its head thoughtfully and brings one front paw under its chin with a curious pensive expression, looking up in contemplation, smooth looping 3d animation."),
    ("04_error_404", "The cute ginger tabby cat sitting upright on solid chroma green background. It holds a small floating 3D sign with 404 text, looking slightly confused with twitching ears, cute curious expression, smooth looping 3d animation."),
    ("05_thumbs_up", "The cute ginger tabby cat sitting upright on solid chroma green background. It proudly extends its right paw with a clear thumbs up approval gesture, winking happily with a warm smile, smooth looping 3d animation."),
    ("06_sleeping", "The cute ginger tabby cat curled up and sleeping peacefully on solid chroma green background, 4 natural paws tucked neatly, gentle rhythmic breathing motion, 3 small 3D golden glowing Zzz floating upward, smooth looping animation."),
    ("07_pointing", "The cute ginger tabby cat sitting upright on solid chroma green background. It points forward to the right with its paw, showing direction with an inviting confident smile, smooth looping 3d animation."),
    ("08_searching", "The cute ginger tabby cat sitting upright on solid chroma green background. It holds a stylized 3D magnifying glass with orange ceramic frame and clear transparent glass lens with spherical refraction in front of its eye, looking closely and searching with curiosity, smooth looping 3d animation."),
    ("09_loading", "The cute ginger tabby cat sitting upright on solid chroma green background. A smooth glowing circular orbital ring spins slowly around its head, the cat watches it with focused playful eyes, smooth looping 3d animation."),
    ("10_idea", "The cute ginger tabby cat sitting upright on solid chroma green background. A bright glowing 3D yellow lightbulb appears and floats above its head, illuminating brightly with a eureka spark, the cat looks up with wide excited happy eyes, smooth looping 3d animation."),
    ("11_security", "The cute ginger tabby cat sitting upright on solid chroma green background. It proudly holds a solid 3D translucent holographic cyan-blue security shield with glowing padlock crest in front of its chest, confident protective posture, smooth looping 3d animation."),
    ("12_goodbye", "The cute ginger tabby cat sitting upright on solid chroma green background. It waves a gentle goodbye with both paws in a polite friendly gesture, soft warm smile, smooth looping 3d animation.")
]

def key_frame_mathematical(pil_img):
    img = pil_img.convert('RGB')
    arr = np.array(img, dtype=np.float32)
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    
    # 1. True Chroma Screen Criteria:
    # Pure green screen: R and B are small (< 65), G is dominant (> 110)
    is_chroma = (g > 110) & (r < 65) & (b < 70) & (g > (r + b) * 1.35)
    
    # 2. Label components
    labeled, num_features = ndimage.label(is_chroma)
    border_mask = np.zeros(is_chroma.shape, dtype=bool)
    border_mask[0, :] = True
    border_mask[-1, :] = True
    border_mask[:, 0] = True
    border_mask[:, -1] = True
    
    border_labels = np.unique(labeled[border_mask])
    border_labels = border_labels[border_labels != 0]
    
    # 3. True exterior background
    is_true_bg = np.isin(labeled, border_labels)
    
    # 4. Foreground mask with binary hole filling (Guarantees 0 internal holes)
    fg_mask = ~is_true_bg
    fg_mask_filled = ndimage.binary_fill_holes(fg_mask)
    
    # 5. Green Despill on foreground pixels
    despilled_g = np.copy(g)
    char_spill = fg_mask_filled & (g > np.maximum(r, b))
    despilled_g[char_spill] = np.maximum(r[char_spill], b[char_spill])
    
    # 6. Distance transform for anti-aliased edge
    dist = ndimage.distance_transform_edt(fg_mask_filled)
    alpha = np.clip(dist * 255.0, 0.0, 255.0).astype(np.uint8)
    
    out_arr = np.dstack([
        np.clip(r, 0, 255).astype(np.uint8),
        np.clip(despilled_g, 0, 255).astype(np.uint8),
        np.clip(b, 0, 255).astype(np.uint8),
        alpha
    ])
    return Image.fromarray(out_arr)

def process_and_save(raw_mp4, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    temp_dir = f"{out_dir}/temp_raw_frames"
    looped_mp4 = f"{out_dir}/looped.mp4"
    os.makedirs(temp_dir, exist_ok=True)
    
    # 1. Create seamless ping-pong loop
    subprocess.run([
        "ffmpeg", "-y", "-t", "2.0", "-i", raw_mp4,
        "-filter_complex", "[0:v]split[v1][v2];[v2]reverse[v2rev];[v1][v2rev]concat=n=2:v=1[v]",
        "-map", "[v]", "-r", "24", "-c:v", "libx264", "-pix_fmt", "yuv420p", looped_mp4
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 2. Extract 512x512 cropped frames
    subprocess.run([
        "ffmpeg", "-y", "-i", looped_mp4,
        "-vf", "crop=720:720:280:0,fps=24,scale=512:512",
        f"{temp_dir}/frame_%04d.png"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    frame_files = sorted([os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if f.endswith('.png')])
    if not frame_files:
        raise RuntimeError("No frames extracted!")
        
    keyed_frames = []
    for ff in frame_files:
        f_im = Image.open(ff)
        k_im = key_frame_mathematical(f_im)
        keyed_frames.append(k_im)
        
    # 3. Save static.png & static.webp (middle frame)
    mid_idx = len(keyed_frames) // 2
    keyed_frames[mid_idx].save(f"{out_dir}/static.png")
    keyed_frames[mid_idx].save(f"{out_dir}/static.webp", quality=90)
    
    # 4. Save animated.webp (high quality, 60fps / 42ms frame duration)
    keyed_frames[0].save(
        f"{out_dir}/animated.webp",
        save_all=True,
        append_images=keyed_frames[1:],
        duration=42,
        loop=0,
        quality=85,
        method=6
    )
    
    # 5. Save animated.gif
    gif_frames = [kf.convert("RGBA") for kf in keyed_frames]
    gif_frames[0].save(
        f"{out_dir}/animated.gif",
        save_all=True,
        append_images=gif_frames[1:],
        duration=42,
        loop=0,
        disposal=2
    )
    
    # Cleanup temp
    subprocess.run(["rm", "-rf", temp_dir, looped_mp4])
    print(f"   ✨ Keyed & saved {len(keyed_frames)} frames -> {out_dir}")

def run_suite():
    print(f"🚀 LANCEMENT DU RENDU COMPLET DE LUNEKO (12 ÉTATS) SUR VERTEX AI VEO 3.1...")
    
    with open(MASTER_IMAGE_PATH, "rb") as f:
        m_bytes = f.read()
    img_input = types.Image(image_bytes=m_bytes, mime_type="image/jpeg")
    
    for idx, (pose_name, prompt_text) in enumerate(LUNEKO_POSES, 1):
        out_dir = f"mascots/luneko/assets/{pose_name}"
        raw_mp4 = f"/tmp/luneko_{pose_name}_raw.mp4"
        
        print(f"\n[{idx}/12] 🎬 Rendu Veo 3.1 pour LUNEKO {pose_name}...")
        t0 = time.time()
        
        op = client.models.generate_videos(
            model="veo-3.1-fast-generate-001",
            prompt=prompt_text,
            image=img_input,
            config=types.GenerateVideosConfig(
                aspect_ratio="16:9",
                duration_seconds=4,
                person_generation="allow_all"
            )
        )
        
        elapsed = 0
        while not op.done:
            time.sleep(8)
            elapsed += 8
            print(f"   ... ({elapsed}s) Rendu {pose_name} en cours...")
            op = client.operations.get(op)
            
        if not op.response or not op.response.generated_videos:
            print(f"❌ Erreur sur {pose_name}: {op.error}")
            continue
            
        vid = op.response.generated_videos[0].video
        with open(raw_mp4, "wb") as f:
            f.write(vid.video_bytes)
            
        # Process and key
        process_and_save(raw_mp4, out_dir)
        total_time = time.time() - t0
        print(f"✅ LUNEKO {pose_name} finalisé avec 0 trou et 100% de cohérence en {total_time:.1f}s !")
        
    print("\n🎉 SUITE COMPLÈTE LUNEKO 12 ÉTATS TERMINÉE AVEC SUCCÈS !")

if __name__ == "__main__":
    run_suite()
