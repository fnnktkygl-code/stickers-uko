import os
import sys
import time
import glob
import json
import zipfile
import subprocess
import base64
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google import genai
from google.genai import types
from core_pipeline.keyer import key_greenscreen_master

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/richard/Developer/Stickers Uko/stickers-3d-7659bde46f1f.json"
client = genai.Client(vertexai=True, project="stickers-3d", location="us-central1")
brain_dir = "/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68"

def generate_state(state_id, state_title, mascot_configs):
    print(f"\n=======================================================")
    print(f"🚀 PRODUCTION DE L'ÉTAT : {state_id.upper()} ({state_title})")
    print(f"=======================================================")
    
    mb_dir = f"preview/moodboards/{state_id}"
    os.makedirs(mb_dir, exist_ok=True)
    
    mascots_widget_data = []
    
    for m_key, master_p, prompt, role, color, desc in mascot_configs:
        print(f"\n==========================================")
        print(f"🎬 [1/5] Google Veo 3.1 pour {m_key.upper()} ({state_id})...")
        print(f"==========================================")
        
        with open(master_p, "rb") as f:
            m_bytes = f.read()
        img_input = types.Image(image_bytes=m_bytes, mime_type="image/jpeg")
        
        t0 = time.time()
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
            print(f"   ... ({elapsed}s) Rendu Veo 3.1 en cours pour {m_key}...")
            time.sleep(6)
            op = client.operations.get(op)
            
        if not op.response or not op.response.generated_videos:
            print(f"❌ Erreur Veo pour {m_key}: {op.error}")
            continue
            
        print(f"✅ Rendu Veo 3.1 terminé en {int(time.time() - t0)}s !")
        vid = op.response.generated_videos[0].video
        
        m_dir = f"assets/{state_id}" if m_key == "aituko" else f"mascots/{m_key}/assets/{state_id}"
        os.makedirs(m_dir, exist_ok=True)
        raw_mp4 = f"{m_dir}/source_video.mp4"
        
        if hasattr(vid, "video_bytes") and vid.video_bytes:
            with open(raw_mp4, "wb") as f:
                f.write(vid.video_bytes)
        elif hasattr(vid, "uri"):
            client.files.download(file=vid.uri, destination=raw_mp4)
            
        print(f"✅ Vidéo brute enregistrée : {raw_mp4}")
        
        # 2. Ping-pong seamless loop video (4.0s @ 24fps)
        looped_mp4 = f"{m_dir}/looped_video.mp4"
        print(f"🎬 [2/5] Bouclage temporel ping-pong (4.0s @ 24fps)...")
        subprocess.run([
            "ffmpeg", "-y", "-t", "2.0", "-i", raw_mp4,
            "-filter_complex", "[0:v]split[v1][v2];[v2]reverse[v2rev];[v1][v2rev]concat=n=2:v=1[v]",
            "-map", "[v]", "-r", "24", "-c:v", "libx264", "-pix_fmt", "yuv420p", looped_mp4
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # 3. Extract frames 512x512
        temp_dir = f"{m_dir}/temp_frames"
        os.makedirs(temp_dir, exist_ok=True)
        for old_f in glob.glob(f"{temp_dir}/*"):
            os.remove(old_f)
            
        print(f"🎞️ [3/5] Extraction des frames 512x512 à 24fps...")
        subprocess.run([
            "ffmpeg", "-y", "-i", looped_mp4,
            "-vf", "crop=720:720:280:0,fps=24,scale=512:512",
            f"{temp_dir}/f_%03d.png"
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # 4. Matte and despill all frames
        print(f"🟢 [4/5] Détourage mathématique solide sans trou...")
        raw_frames = sorted(glob.glob(f"{temp_dir}/f_*.png"))
        clean_frames = [key_greenscreen_master(Image.open(rf)) for rf in raw_frames]
        
        # 5. Export multi-formats
        print(f"📦 [5/5] Encodage PNG, WebP, APNG, GIF transparent...")
        mid_idx = min(24, len(clean_frames) - 1)
        clean_frames[mid_idx].save(f"{m_dir}/static.png")
        clean_frames[mid_idx].save(f"{m_dir}/static.webp", quality=92)
        clean_frames[mid_idx].save(f"{mb_dir}/{m_key}_static.png")
        clean_frames[mid_idx].save(f"{brain_dir}/{m_key}_{state_id}_static.png")
        
        clean_frames[0].save(f"{m_dir}/animated.png", save_all=True, append_images=clean_frames[1:], duration=41, loop=0)
        clean_frames[0].save(f"{m_dir}/animated.webp", save_all=True, append_images=clean_frames[1:], duration=41, loop=0, quality=88, method=4)
        
        gif_frames = []
        for f in clean_frames:
            alpha = f.split()[3]
            mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
            p_frame = f.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE)
            p_frame.paste(255, mask)
            p_frame.info['transparency'] = 255
            gif_frames.append(p_frame)
        gif_frames[0].save(f"{m_dir}/animated.gif", save_all=True, append_images=gif_frames[1:], duration=41, loop=0, disposal=2)
        gif_frames[0].save(f"{mb_dir}/{m_key}_animated.gif", save_all=True, append_images=gif_frames[1:], duration=41, loop=0, disposal=2)
        gif_frames[0].save(f"{brain_dir}/{m_key}_{state_id}_anim.gif", save_all=True, append_images=gif_frames[1:], duration=41, loop=0, disposal=2)
        
        # 6. Snippet JSON
        snippet_data = {
            "mascot": m_key,
            "state": state_id,
            "react": f'<img src="/mascots/{m_key}/assets/{state_id}/animated.webp" alt="{m_key} {state_id}" width="512" height="512" className="w-32 h-32 object-contain" />',
            "vue": f'<img src="/mascots/{m_key}/assets/{state_id}/animated.webp" alt="{m_key} {state_id}" width="512" height="512" class="w-32 h-32 object-contain" />',
            "html": f'<picture><source srcset="/mascots/{m_key}/assets/{state_id}/animated.webp" type="image/webp"><img src="/mascots/{m_key}/assets/{state_id}/animated.gif" alt="{m_key} {state_id}" width="512" height="512"></picture>'
        }
        with open(f"{m_dir}/snippet.json", "w") as f:
            json.dump(snippet_data, f, indent=2)
            
        # 7. ZIP bundle
        zip_path = f"{m_dir}/bundle_{m_key}_{state_id}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for item in ["static.png", "static.webp", "animated.gif", "animated.webp", "animated.png", "looped_video.mp4", "snippet.json"]:
                p_item = f"{m_dir}/{item}"
                if os.path.exists(p_item):
                    zipf.write(p_item, arcname=f"{m_key}_{state_id}/{item}")
                    
        # Add to widget data
        with open(looped_mp4, "rb") as vf, open(f"{m_dir}/static.png", "rb") as sf:
            v_b64 = base64.b64encode(vf.read()).decode("utf-8")
            s_b64 = base64.b64encode(sf.read()).decode("utf-8")
            mascots_widget_data.append({
                "id": m_key,
                "name": m_key.capitalize(),
                "role": role,
                "color": color,
                "video": v_b64,
                "static": s_b64,
                "desc": desc
            })
            
        print(f"✨ Mascotte {m_key.upper()} ({state_id}) 100% finalisée et certifiée !")

    # Generate HTML Moodboard Widget (<6MB)
    widget_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=3.0, user-scalable=yes">
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    body {{ background: #121214; color: #F4F4F5; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 12px; }}
    .bg-zinc-card {{ background-color: #18181B; }}
    .mascot-btn.active {{ border-color: #00E5FF; background: rgba(0, 229, 255, 0.16); color: #FFFFFF; }}
    video {{ border-radius: 12px; outline: none; width: 100%; height: 100%; object-fit: contain; }}
  </style>
</head>
<body class="antialiased">
  <div class="max-w-2xl mx-auto space-y-4">
    <div class="bg-zinc-card border border-zinc-800 rounded-xl p-4 shadow-lg flex items-center justify-between">
      <div>
        <div class="flex items-center gap-2">
          <span class="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse"></span>
          <span class="text-[10px] uppercase font-bold tracking-wider text-cyan-400">Google Veo 3.1 MP4 (4.0s @ 24 FPS)</span>
        </div>
        <h1 class="text-base font-bold text-white mt-0.5">Moodboard : État {state_id} ({state_title})</h1>
        <p class="text-xs text-zinc-400 mt-1">6 Mascottes animées avec le pipeline certifié Veo 3.1.</p>
      </div>
      <span class="text-xs bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 px-3 py-1 rounded-full font-bold">
        {state_id} 🎬
      </span>
    </div>

    <div class="flex gap-2 overflow-x-auto pb-1.5 scrollbar-none">
      {''.join([f'''<button onclick="selectMascot({idx})" id="btn-{idx}" class="mascot-btn {'active' if idx==0 else ''} flex items-center gap-2 px-3 py-2 rounded-lg border border-zinc-700 bg-zinc-800/80 text-xs font-semibold whitespace-nowrap transition-all">
        <span>{['🤖','🦉','🐱','🐰','🐕','🕊️'][idx]}</span> {m['name']}
      </button>''' for idx, m in enumerate(mascots_widget_data)])}
    </div>

    <div class="bg-zinc-card border border-zinc-800 rounded-xl p-4 shadow-xl">
      <div class="flex items-center justify-between pb-3 border-b border-zinc-800">
        <div>
          <h2 id="detail-name" class="text-base font-bold text-white flex items-center gap-2">{mascots_widget_data[0]['name']}</h2>
          <p id="detail-role" class="text-xs text-zinc-400">{mascots_widget_data[0]['role']}</p>
        </div>
        <span class="text-[11px] font-mono text-cyan-400 bg-cyan-950/60 border border-cyan-800 px-2 py-0.5 rounded">4.0s Ping-Pong</span>
      </div>

      <div class="my-4 flex items-center justify-center bg-black/80 rounded-xl p-2 border border-zinc-800 min-h-[320px]">
        <video id="main-video" class="w-full max-h-[360px] rounded-lg shadow-2xl" autoplay loop muted playsinline controls>
          <source id="video-source" src="data:video/mp4;base64,{mascots_widget_data[0]['video']}" type="video/mp4">
        </video>
      </div>

      <p id="detail-desc" class="text-xs text-zinc-300 mt-2 p-3 bg-zinc-900/60 rounded-lg border border-zinc-800/80 leading-relaxed">
        {mascots_widget_data[0]['desc']}
      </p>
    </div>

    <div class="bg-zinc-card border border-zinc-800 rounded-xl p-4 shadow-lg space-y-3">
      <div class="flex items-center justify-between">
        <h3 class="text-xs font-bold uppercase tracking-wider text-zinc-300">Les 6 Mascottes ({state_title})</h3>
        <span class="text-[10px] text-cyan-400 font-mono">100% Veo 3.1</span>
      </div>
      <div class="grid grid-cols-3 md:grid-cols-6 gap-2">
        {''.join([f'''<div onclick="selectMascot({idx})" class="cursor-pointer bg-zinc-900/80 hover:border-cyan-500 p-2 rounded-lg border border-zinc-800 text-center transition-all">
          <p class="text-[10px] font-bold text-cyan-400 mb-1">{m['name']}</p>
          <img src="data:image/png;base64,{m['static']}" class="w-16 h-16 mx-auto object-contain" alt="{m['name']}">
          <span class="text-[9px] text-zinc-500 mt-1 block">Regarder ▶</span>
        </div>''' for idx, m in enumerate(mascots_widget_data)])}
      </div>
    </div>
  </div>

  <script>
    const mascots = {json.dumps(mascots_widget_data)};
    let currentIndex = 0;
    function selectMascot(index) {{
      currentIndex = index;
      const m = mascots[index];
      document.querySelectorAll('.mascot-btn').forEach((btn, idx) => {{
        btn.classList.toggle('active', idx === index);
      }});
      document.getElementById('detail-name').innerText = m.name;
      document.getElementById('detail-role').innerText = m.role;
      document.getElementById('detail-desc').innerText = m.desc;
      const video = document.getElementById('main-video');
      video.src = 'data:video/mp4;base64,' + m.video;
      video.load();
      video.play().catch(e => console.log('Autoplay blocked:', e));
    }}
  </script>
</body>
</html>
"""
    widget_path = f"{brain_dir}/veo_{state_id}_player.html"
    with open(widget_path, "w") as f:
        f.write(widget_html)
    print(f"\n🎉 ÉTAT {state_id.upper()} TERMINÉ AVEC SUCCÈS ! Widget: {widget_path} ({os.path.getsize(widget_path)/(1024*1024):.2f} MB)")

if __name__ == "__main__":
    configs_01_waving = [
        ("aituko", "mascots/aituko/master/aituko_greenscreen_master.jpg", 
         "A high-end 3D character animation of this cute white porcelain robot mascot AItuko on uniform solid chroma green screen background (#00FF00). The robot cheerfully raises its right hand with its 4 delicate porcelain fingers and waves happily in a warm, friendly welcoming greeting, smiling with bright glowing cyan (#00E5FF) curved smiling eyes and mouth. Clean porcelain reflections, high-end Pixar 3D animation, 24fps.",
         "Robot Porcelaine", "#00E5FF", "AItuko lève joyeusement sa main en porcelaine à 4 doigts pour saluer chaleureusement, yeux et sourire cyan lumineux."),
        
        ("owluko", "mascots/owluko/master/owleko_greenscreen_master.jpg",
         "A high-end 3D character animation of this cute cream owl mascot Owluko on uniform solid chroma green screen background (#00FF00). The owl cheerfully raises its right wing and waves in a warm welcoming greeting, blinking its big golden amber eyes happily, subtle fluffy plumage motion. High-end Pixar 3D animation, soft feathers, 24fps.",
         "Chouette Savante", "#F59E0B", "Owluko lève son aile droite pour faire un signe de bienvenue bienveillant, grands yeux dorés ambrés pétillants."),
        
        ("luneko", "mascots/luneko/master/luneko_greenscreen_master.jpg",
         "A high-end 3D character animation of this cute ginger tabby cat mascot Luneko on uniform solid chroma green screen background (#00FF00). The cat sits happily, raises its right paw and gives a friendly, warm wave of greeting, blinking with cheerful brown eyes. Solid white chest fur, high-end Pixar 3D character animation, 24fps.",
         "Chat Tabby Roux", "#FB923C", "Luneko lève sa patte droite pour saluer d'un geste félin amical, torse blanc plein et regard complice."),
        
        ("usako", "mascots/usako/master/usako_greenscreen_master.jpg",
         "A high-end 3D character animation of this cute white bunny mascot Usako with its signature brown patch on the side and sage green headband on uniform solid chroma green screen background (#00FF00). The bunny raises its right paw and waves happily in a cute, cheerful welcoming greeting. High-end Pixar 3D animation, clean fluffy fur, 24fps.",
         "Lapin Zen", "#10B981", "Usako fait un signe de la patte avec entrain, bandeau vert sauge et sa marque brune signature parfaitement préservée."),
        
        ("inuko", "mascots/inuko/master/inuko_greenscreen_master.jpg",
         "A high-end 3D character animation of this noble black and tan Doberman mascot Inuko on uniform solid chroma green screen background (#00FF00). The dog sits proudly and lifts its right front paw in a friendly, gentle welcoming greeting gesture, smiling loyally. High-end Pixar 3D animation, sleek fur, 24fps.",
         "Doberman Gardien", "#F43F5E", "Inuko lève la patte avant droite avec loyauté et calme pour accueillir chaleureusement."),
        
        ("hatoko", "mascots/hatoko/master/hatoko_greenscreen_master.jpg",
         "A high-end 3D character animation of this cute round messenger pigeon mascot Hatoko with its closed leather satchel on uniform solid chroma green screen background (#00FF00). The pigeon lifts its right wing in a cheerful, friendly greeting wave. Closed leather mail satchel, high-end Pixar 3D animation, 24fps.",
         "Pigeon Voyageur", "#A855F7", "Hatoko agite l'aile pour saluer, plumage tourterelle doux et sacoche en cuir fermée propre.")
    ]
    
    generate_state("01_waving", "Salutation / Bienvenue", configs_01_waving)
