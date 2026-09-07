import sys, os
sys.path.insert(0, os.getcwd())
import os
import sys
import time
import glob
import json
import shutil
import zipfile
import subprocess
from PIL import Image
from google import genai
from google.genai import types
from core_pipeline.keyer import key_greenscreen_master

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/richard/Developer/Stickers Uko/stickers-3d-7659bde46f1f.json"

client = genai.Client(
    vertexai=True,
    project="stickers-3d",
    location="us-central1"
)

AITUKO_STATES = {
    "06_sleeping": {
        "title": "Veille & Sommeil Zzz",
        "category": "cat1_ambient",
        "ref": "mascots/aituko/state_references/06_sleeping_reference.jpg",
        "prompt": "A high-end 3D character animation of this exact cute white porcelain robot mascot AItuko on solid uniform chroma green background (#00FF00). The robot is peacefully sleeping in standby mode throughout the ENTIRE animation, eyes closed in calm cyan slits, floating gently with subtle rhythmic breathing of the torso, tiny stylized cyan Zzz bubbles floating up smoothly, continuous deep peaceful sleep loop, never waking up, never standing up, 24fps Pixar 3D animation."
    },
    "08_searching": {
        "title": "Recherche & Scan à la Loupe",
        "category": "cat3_processing",
        "ref": "mascots/aituko/state_references/08_searching_reference.jpg",
        "prompt": "A high-end 3D digital animation of this white porcelain robot character on uniform chroma green (#00FF00). The robot holds a modern orange glass lens with both hands, scanning left and right smoothly in a rhythmic search motion, glowing cyan lights, 24fps studio render."
    },
    "09_loading": {
        "title": "Chargement & Orbite Étoile",
        "category": "cat3_processing",
        "ref": "mascots/aituko/state_references/09_loading_reference.jpg",
        "prompt": "A high-end 3D character animation of this exact cute white porcelain robot mascot AItuko on solid uniform chroma green background (#00FF00). The robot looks up happily as a small glowing golden 3D star orbits smoothly around its head in a continuous 360 celestial loading loop, gentle floating posture, 24fps Pixar 3D animation."
    },
    "03_ai_thinking": {
        "title": "Réflexion IA & Analyse",
        "category": "cat3_processing",
        "ref": "mascots/aituko/state_references/03_ai_thinking_reference.jpg",
        "prompt": "A high-end 3D character animation of this exact cute white porcelain robot mascot AItuko on solid uniform chroma green background (#00FF00). The robot tilts its head thoughtfully with hand to chin, glowing cyan eyes pulsing in intelligent problem-solving analysis, subtle micro-movements of deep thought, 24fps Pixar 3D animation."
    },
    "04_error_404": {
        "title": "Erreur 404 & Shrug",
        "category": "cat2_oneshot",
        "ref": "mascots/aituko/state_references/04_error_404_reference.jpg",
        "prompt": "A high-end 3D character animation of this exact cute white porcelain robot mascot AItuko on solid uniform chroma green background (#00FF00). The robot holds a small cute wooden '404' sign, giving a sweet apologetic shrug, eyes displaying soft cyan question marks, smooth movement, 24fps Pixar 3D animation."
    },
    "01_waving": {
        "title": "Salutation & Bienvenue",
        "category": "cat2_oneshot",
        "ref": "mascots/aituko/state_references/01_waving_reference.jpg",
        "prompt": "A high-end 3D character animation of this exact cute white porcelain robot mascot AItuko on solid uniform chroma green background (#00FF00). The robot raises its right hand and waves warmly in a friendly welcoming greeting, smiling with glowing cyan crescent eyes, smooth motion, 24fps Pixar 3D animation."
    },
    "02_celebrating": {
        "title": "Victoire & Célébration",
        "category": "cat2_oneshot",
        "ref": "mascots/aituko/state_references/02_celebrating_reference.jpg",
        "prompt": "A high-end 3D character animation of this exact cute white porcelain robot mascot AItuko on solid uniform chroma green background (#00FF00). The robot floats with joy with both hands raised in victory, cheerful smiling cyan eyes, colorful confetti gently floating around, 24fps Pixar 3D animation."
    },
    "05_thumbs_up": {
        "title": "Pouce en l'Air & Validation",
        "category": "cat2_oneshot",
        "ref": "mascots/aituko/state_references/05_thumbs_up_reference.jpg",
        "prompt": "A high-end 3D digital animation of this white porcelain robot character on uniform chroma green (#00FF00). The robot raises its right arm in an affirmative approval gesture with glowing cyan curved smile eyes, nodding gently, 24fps studio render."
    },
    "07_pointing": {
        "title": "Pointage & Guidage",
        "category": "cat2_oneshot",
        "ref": "mascots/aituko/master/aituko_greenscreen_master.jpg",
        "prompt": "A high-end 3D character animation of this exact cute white porcelain robot mascot AItuko on solid uniform chroma green background (#00FF00). The robot raises its right hand and gestures to the right side in a warm guiding posture, smiling with glowing cyan crescent eyes, smooth motion, 24fps."
    },
    "10_idea": {
        "title": "Idée Trouvée & Ampoule",
        "category": "cat3_processing",
        "ref": "mascots/aituko/state_references/10_idea_reference.jpg",
        "prompt": "A high-end 3D character animation of this exact cute white porcelain robot mascot AItuko on solid uniform chroma green background (#00FF00). A small 3D lightbulb illuminates above its head with bright electric cyan light, robot gasps happily in eureka revelation with glowing cyan eyes, 24fps Pixar 3D animation."
    },
    "11_security": {
        "title": "Sécurité & Protection",
        "category": "cat2_oneshot",
        "ref": "mascots/aituko/state_references/11_security_reference.jpg",
        "prompt": "A high-end 3D character animation of this exact cute white porcelain robot mascot AItuko on solid uniform chroma green background (#00FF00). The robot raises both hands in a firm, protective stop and guarding posture, confident resolute cyan eyes, zero shield gadget, 24fps Pixar 3D animation."
    },
    "12_goodbye": {
        "title": "Au Revoir & Départ",
        "category": "cat2_oneshot",
        "ref": "mascots/aituko/state_references/12_goodbye_reference.jpg",
        "prompt": "A high-end 3D character animation of this exact cute white porcelain robot mascot AItuko on solid uniform chroma green background (#00FF00). The robot waves a gentle, friendly goodbye with a warm comforting smile on its glowing cyan eyes, 24fps Pixar 3D animation."
    }
}

def generate_veo_state(state_id, state_info):
    ref_img = state_info["ref"]
    output_mp4 = f"assets/{state_id}/source_video.mp4"
    os.makedirs(f"assets/{state_id}", exist_ok=True)
    
    with open(ref_img, "rb") as f:
        img_bytes = f.read()
        
    title = state_info["title"]
    print(f"\n🎬 [Veo 3.1] Lancement rendu {state_id} ({title})...", flush=True)
    t0 = time.time()
    
    op = client.models.generate_videos(
        model="veo-3.1-fast-generate-001",
        prompt=state_info["prompt"],
        image=types.Image(image_bytes=img_bytes, mime_type="image/jpeg"),
        config=dict(
            aspect_ratio="16:9",
            duration_seconds=4,
            person_generation="dont_allow"
        )
    )
    
    while not op.done:
        elapsed = int(time.time() - t0)
        print(f"   ... ({elapsed}s) Calcul GPU Veo 3.1 ({state_id})...", flush=True)
        time.sleep(5)
        op = client.operations.get(op)
        
    if not op.response or not op.response.generated_videos:
        raise RuntimeError(f"Erreur Veo pour {state_id}: {op.error}")
        
    vid = op.response.generated_videos[0].video
    with open(output_mp4, "wb") as f:
        f.write(vid.video_bytes)
        
    print(f"✅ Vidéo source générée ({int(time.time() - t0)}s) : {output_mp4}", flush=True)
    return output_mp4

def process_and_package_state(state_id, state_info, src_mp4):
    state_dir = f"assets/{state_id}"
    tmp_raw = f"{state_dir}/_tmp_raw"
    tmp_clean = f"{state_dir}/_tmp_clean"
    os.makedirs(tmp_raw, exist_ok=True)
    os.makedirs(tmp_clean, exist_ok=True)
    
    category = state_info["category"]
    title = state_info["title"]
    looped_mp4 = f"{state_dir}/looped_video.mp4"
    
    # 1. Video Looping Strategy
    subprocess.run([
        "ffmpeg", "-y", "-t", "2.0", "-i", src_mp4,
        "-filter_complex", "[0:v]split[v1][v2];[v2]reverse[v2rev];[v1][v2rev]concat=n=2:v=1[v]",
        "-map", "[v]", "-r", "24", "-c:v", "libx264", "-pix_fmt", "yuv420p", looped_mp4
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 2. Extract 24fps frames
    subprocess.run([
        "ffmpeg", "-y", "-i", looped_mp4,
        "-vf", "fps=24", f"{tmp_raw}/f_%03d.png"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    raw_frames = sorted(glob.glob(f"{tmp_raw}/f_*.png"))
    if not raw_frames:
        raise RuntimeError(f"Extraction frames impossible pour {state_id}")
        
    clean_frames = []
    for idx, rf in enumerate(raw_frames):
        im = Image.open(rf)
        w, h = im.size
        if w != h:
            left = (w - h) // 2
            im = im.crop((left, 0, left + h, h))
        clean = key_greenscreen_master(im)
        clean_frames.append(clean)
        clean.save(f"{tmp_clean}/f_{idx+1:03d}.png", "PNG")
        
    # 3. Keyframe Static
    ref_im = Image.open(state_info["ref"])
    rw, rh = ref_im.size
    if rw != rh:
        left = (rw - rh) // 2
        ref_im = ref_im.crop((left, 0, left + rh, rh))
    keyed_static = key_greenscreen_master(ref_im)
    
    keyed_static.save(f"{state_dir}/static.png", "PNG")
    keyed_static.save(f"{state_dir}/static.webp", "WEBP", quality=92)
    
    # 4. Animated WebP
    clean_frames[0].save(
        f"{state_dir}/animated.webp",
        format="WEBP",
        save_all=True,
        append_images=clean_frames[1:],
        duration=int(1000 / 24),
        loop=0,
        quality=88,
        method=4
    )
    
    # 5. Animated GIF
    gif_path = f"{state_dir}/animated.gif"
    subprocess.run([
        "ffmpeg", "-y", "-framerate", "24", "-i", f"{tmp_clean}/f_%03d.png",
        "-filter_complex", "[0:v]split[a][b];[a]palettegen=reserve_transparent=on:transparency_color=ffffff00[p];[b][p]paletteuse=alpha_threshold=128:dither=bayer:bayer_scale=3",
        gif_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 6. Snippets JSON
    snippet_data = {
        "name": f"AItuko - {title}",
        "category": category,
        "html": f'<img src="assets/{state_id}/animated.webp" alt="AItuko {title}" width="512" height="512" />',
        "react": f'<img src="{{`/assets/{state_id}/animated.webp`}}" alt="AItuko {title}" className="w-32 h-32 object-contain" />',
        "vue": f'<img :src="`/assets/{state_id}/animated.webp`" alt="AItuko {title}" class="w-32 h-32 object-contain" />'
    }
    with open(f"{state_dir}/snippet.json", "w", encoding="utf-8") as f:
        json.dump(snippet_data, f, indent=2, ensure_ascii=False)
        
    # 7. ZIP Bundle
    zip_path = f"{state_dir}/bundle_aituko_{state_id}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(f"{state_dir}/static.png", "static.png")
        z.write(f"{state_dir}/static.webp", "static.webp")
        z.write(f"{state_dir}/animated.webp", "animated.webp")
        if os.path.exists(gif_path):
            z.write(gif_path, "animated.gif")
        z.write(looped_mp4, "video_loop.mp4")
        z.write(f"{state_dir}/snippet.json", "snippet.json")
        
    # Replicate to mascots/aituko/assets/
    m_dir = f"mascots/aituko/assets/{state_id}"
    os.makedirs(m_dir, exist_ok=True)
    for fn in ["static.png", "static.webp", "animated.webp", "animated.gif", "looped_video.mp4", "snippet.json", f"bundle_aituko_{state_id}.zip"]:
        src_f = f"{state_dir}/{fn}"
        if os.path.exists(src_f):
            shutil.copy(src_f, f"{m_dir}/{fn}")
            
    # Cleanup tmp
    shutil.rmtree(tmp_raw, ignore_errors=True)
    shutil.rmtree(tmp_clean, ignore_errors=True)
    print(f"✨ [Package OK] {state_id} terminé avec succès (ZIP: {zip_path})", flush=True)

if __name__ == "__main__":
    target_state = sys.argv[1] if len(sys.argv) > 1 else "06_sleeping"
    if target_state == "all":
        for st_id, st_info in AITUKO_STATES.items():
            try:
                src_mp4 = generate_veo_state(st_id, st_info)
                process_and_package_state(st_id, st_info, src_mp4)
            except Exception as e:
                print(f"❌ Erreur sur {st_id}: {e}", flush=True)
    else:
        st_info = AITUKO_STATES.get(target_state)
        if not st_info:
            print(f"État inconnu: {target_state}", flush=True)
            sys.exit(1)
        src_mp4 = generate_veo_state(target_state, st_info)
        process_and_package_state(target_state, st_info, src_mp4)
