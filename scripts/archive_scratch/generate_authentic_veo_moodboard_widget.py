import base64
import json
import os
import shutil

mb_dir = "preview/moodboards/00_idle"
brain_dir = "/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68"
mascots_keys = ["aituko", "owluko", "luneko", "usako", "inuko", "hatoko"]

for m in mascots_keys:
    shutil.copy(f"{mb_dir}/{m}_static.png", f"{brain_dir}/{m}_veo_idle_static.png")
    shutil.copy(f"{mb_dir}/{m}_animated.gif", f"{brain_dir}/{m}_veo_idle_anim.gif")

def to_b64(filepath):
    with open(filepath, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

mascots_data = [
    {
        "id": "aituko",
        "name": "AItuko",
        "role": "Robot Porcelaine",
        "color": "#00E5FF",
        "video": to_b64("assets/00_idle/looped_video.mp4"),
        "anim": to_b64(f"{brain_dir}/aituko_veo_idle_anim.gif"),
        "static": to_b64(f"{brain_dir}/aituko_veo_idle_static.png"),
        "desc": "Vidéo Veo 3.1 : Respiration sobre 3D, clignement naturel des yeux et sourire cyan électrique (#00E5FF)."
    },
    {
        "id": "owluko",
        "name": "Owluko",
        "role": "Chouette Savante",
        "color": "#F59E0B",
        "video": to_b64("mascots/owluko/assets/00_idle/looped_video.mp4"),
        "anim": to_b64(f"{brain_dir}/owluko_veo_idle_anim.gif"),
        "static": to_b64(f"{brain_dir}/owluko_veo_idle_static.png"),
        "desc": "Vidéo Veo 3.1 : Clignement doux des yeux ambrés, respiration corporelle subtile duveteuse."
    },
    {
        "id": "luneko",
        "name": "Luneko",
        "role": "Chat Tabby Roux",
        "color": "#FB923C",
        "video": to_b64("mascots/luneko/assets/00_idle/looped_video.mp4"),
        "anim": to_b64(f"{brain_dir}/luneko_veo_idle_anim.gif"),
        "static": to_b64(f"{brain_dir}/luneko_veo_idle_static.png"),
        "desc": "Vidéo Veo 3.1 : Respiration féline calme, clignement doux des yeux et torse blanc plein."
    },
    {
        "id": "usako",
        "name": "Usako",
        "role": "Lapin Zen",
        "color": "#10B981",
        "video": to_b64("mascots/usako/assets/00_idle/looped_video.mp4"),
        "anim": to_b64(f"{brain_dir}/usako_veo_idle_anim.gif"),
        "static": to_b64(f"{brain_dir}/usako_veo_idle_static.png"),
        "desc": "Vidéo Veo 3.1 : Respiration corporelle discrète, clignement doux, avec sa marque brune signature."
    },
    {
        "id": "inuko",
        "name": "Inuko",
        "role": "Doberman Gardien",
        "color": "#F43F5E",
        "video": to_b64("mascots/inuko/assets/00_idle/looped_video.mp4"),
        "anim": to_b64(f"{brain_dir}/inuko_veo_idle_anim.gif"),
        "static": to_b64(f"{brain_dir}/inuko_veo_idle_static.png"),
        "desc": "Vidéo Veo 3.1 : Posture assise noble et sobre, respiration naturelle et regard vigilant."
    },
    {
        "id": "hatoko",
        "name": "Hatoko",
        "role": "Pigeon Voyageur",
        "color": "#A855F7",
        "video": to_b64("mascots/hatoko/assets/00_idle/looped_video.mp4"),
        "anim": to_b64(f"{brain_dir}/hatoko_veo_idle_anim.gif"),
        "static": to_b64(f"{brain_dir}/hatoko_veo_idle_static.png"),
        "desc": "Vidéo Veo 3.1 : Respiration corporelle naturelle, sacoche fermée propre sans papier qui dépasse."
    }
]

mascots_json = json.dumps(mascots_data)

html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=3.0, user-scalable=yes">
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    body {{
      background: #121214;
      color: #F4F4F5;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      margin: 0;
      padding: 12px;
    }}
    .checkerboard {{
      background-color: #1a1a1e;
      background-image: linear-gradient(45deg, #242429 25%, transparent 25%),
                        linear-gradient(-45deg, #242429 25%, transparent 25%),
                        linear-gradient(45deg, transparent 75%, #242429 75%),
                        linear-gradient(-45deg, transparent 75%, #242429 75%);
      background-size: 20px 20px;
      background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
    }}
    .bg-pure-dark {{ background-color: #121214 !important; }}
    .bg-pure-light {{ background-color: #FFFFFF !important; }}
    .bg-zinc-card {{ background-color: #18181B; }}
    .mascot-btn.active {{
      border-color: #00E5FF;
      background: rgba(0, 229, 255, 0.16);
      color: #FFFFFF;
    }}
    video {{
      border-radius: 12px;
      outline: none;
    }}
  </style>
</head>
<body class="antialiased">
  <div class="max-w-2xl mx-auto space-y-4">
    <!-- Header -->
    <div class="bg-zinc-card border border-zinc-800 rounded-xl p-4 shadow-lg flex items-center justify-between">
      <div>
        <div class="flex items-center gap-2">
          <span class="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse"></span>
          <span class="text-[10px] uppercase font-bold tracking-wider text-cyan-400">Vraies Vidéos Google Veo 3.1 (4.0s @ 24 FPS)</span>
        </div>
        <h1 class="text-base font-bold text-white mt-0.5">Moodboard : État 00_idle (Vraie IA Google Veo 3.1)</h1>
        <p class="text-xs text-zinc-400 mt-1">Évolution complète : Vidéo Source MP4 + Animation Transparente Détourée.</p>
      </div>
      <span class="text-xs bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 px-3 py-1 rounded-full font-bold">
        Veo 3.1 🎬
      </span>
    </div>

    <!-- Quick Mascot Selector Bar -->
    <div class="flex gap-2 overflow-x-auto pb-1.5 scrollbar-none">
      <button onclick="selectMascot(0)" id="btn-0" class="mascot-btn active flex items-center gap-2 px-3 py-2 rounded-lg border border-zinc-700 bg-zinc-800/80 text-xs font-semibold whitespace-nowrap transition-all">
        <span>🤖</span> AItuko
      </button>
      <button onclick="selectMascot(1)" id="btn-1" class="mascot-btn flex items-center gap-2 px-3 py-2 rounded-lg border border-zinc-700 bg-zinc-800/80 text-xs font-semibold whitespace-nowrap transition-all">
        <span>🦉</span> Owluko
      </button>
      <button onclick="selectMascot(2)" id="btn-2" class="mascot-btn flex items-center gap-2 px-3 py-2 rounded-lg border border-zinc-700 bg-zinc-800/80 text-xs font-semibold whitespace-nowrap transition-all">
        <span>🐱</span> Luneko
      </button>
      <button onclick="selectMascot(3)" id="btn-3" class="mascot-btn flex items-center gap-2 px-3 py-2 rounded-lg border border-zinc-700 bg-zinc-800/80 text-xs font-semibold whitespace-nowrap transition-all">
        <span>🐰</span> Usako
      </button>
      <button onclick="selectMascot(4)" id="btn-4" class="mascot-btn flex items-center gap-2 px-3 py-2 rounded-lg border border-zinc-700 bg-zinc-800/80 text-xs font-semibold whitespace-nowrap transition-all">
        <span>🐕</span> Inuko
      </button>
      <button onclick="selectMascot(5)" id="btn-5" class="mascot-btn flex items-center gap-2 px-3 py-2 rounded-lg border border-zinc-700 bg-zinc-800/80 text-xs font-semibold whitespace-nowrap transition-all">
        <span>🕊️</span> Hatoko
      </button>
    </div>

    <!-- Dual View: Real MP4 Video + Transparent Loop -->
    <div class="bg-zinc-card border border-zinc-800 rounded-xl p-4 shadow-xl">
      <div class="flex items-center justify-between pb-3 border-b border-zinc-800">
        <div>
          <h2 id="detail-name" class="text-base font-bold text-white flex items-center gap-2">AItuko</h2>
          <p id="detail-role" class="text-xs text-zinc-400">Robot Porcelaine</p>
        </div>
        <div class="flex items-center gap-1.5">
          <button onclick="setViewMode('video')" id="tab-video-btn" class="px-2.5 py-1 text-xs rounded bg-cyan-500 text-black font-bold">Vidéo MP4 Veo 3.1</button>
          <button onclick="setViewMode('anim')" id="tab-anim-btn" class="px-2.5 py-1 text-xs rounded bg-zinc-800 text-zinc-400 font-medium">Sticker Détouré</button>
          <button onclick="setViewMode('static')" id="tab-static-btn" class="px-2.5 py-1 text-xs rounded bg-zinc-800 text-zinc-400 font-medium">Image Statique</button>
        </div>
      </div>

      <!-- Video Container -->
      <div id="video-container" class="my-4 flex items-center justify-center bg-black/60 rounded-xl p-2 border border-zinc-800">
        <video id="main-video" class="w-full max-h-[380px] object-contain rounded-lg shadow-2xl" autoplay loop muted playsinline controls>
          <source id="video-source" src="data:video/mp4;base64,{mascots_data[0]['video']}" type="video/mp4">
        </video>
      </div>

      <!-- Transparent Sticker Container (Hidden by default, toggleable) -->
      <div id="anim-container" class="hidden my-4 flex items-center justify-center bg-pure-dark rounded-xl p-6 border border-zinc-800 min-h-[320px]">
        <img id="main-anim-img" src="data:image/gif;base64,{mascots_data[0]['anim']}" class="w-72 h-72 object-contain" alt="Sticker Détouré">
      </div>

      <!-- Static Container (Hidden by default, toggleable) -->
      <div id="static-container" class="hidden my-4 flex items-center justify-center bg-pure-dark rounded-xl p-6 border border-zinc-800 min-h-[320px]">
        <img id="main-static-img" src="data:image/png;base64,{mascots_data[0]['static']}" class="w-72 h-72 object-contain" alt="Sticker Statique">
      </div>

      <p id="detail-desc" class="text-xs text-zinc-300 mt-2 p-3 bg-zinc-900/60 rounded-lg border border-zinc-800/80 leading-relaxed">
        {mascots_data[0]['desc']}
      </p>
    </div>

    <!-- 6 Mascots Quick Switcher Grid -->
    <div class="bg-zinc-card border border-zinc-800 rounded-xl p-4 shadow-lg space-y-3">
      <div class="flex items-center justify-between">
        <h3 class="text-xs font-bold uppercase tracking-wider text-zinc-300">Les 6 Mascottes Générées par Google Veo 3.1</h3>
        <span class="text-[10px] text-cyan-400 font-mono">100% IA Veo 3.1</span>
      </div>
      <div class="grid grid-cols-3 md:grid-cols-6 gap-2">
        <div onclick="selectMascot(0)" class="cursor-pointer bg-zinc-900/80 hover:border-cyan-500 p-2 rounded-lg border border-zinc-800 text-center transition-all">
          <p class="text-[10px] font-bold text-cyan-400 mb-1">AItuko</p>
          <img src="data:image/png;base64,{mascots_data[0]['static']}" class="w-16 h-16 mx-auto object-contain" alt="AItuko">
          <span class="text-[9px] text-zinc-500 mt-1 block">Regarder ▶</span>
        </div>
        <div onclick="selectMascot(1)" class="cursor-pointer bg-zinc-900/80 hover:border-amber-500 p-2 rounded-lg border border-zinc-800 text-center transition-all">
          <p class="text-[10px] font-bold text-amber-400 mb-1">Owluko</p>
          <img src="data:image/png;base64,{mascots_data[1]['static']}" class="w-16 h-16 mx-auto object-contain" alt="Owluko">
          <span class="text-[9px] text-zinc-500 mt-1 block">Regarder ▶</span>
        </div>
        <div onclick="selectMascot(2)" class="cursor-pointer bg-zinc-900/80 hover:border-orange-500 p-2 rounded-lg border border-zinc-800 text-center transition-all">
          <p class="text-[10px] font-bold text-orange-400 mb-1">Luneko</p>
          <img src="data:image/png;base64,{mascots_data[2]['static']}" class="w-16 h-16 mx-auto object-contain" alt="Luneko">
          <span class="text-[9px] text-zinc-500 mt-1 block">Regarder ▶</span>
        </div>
        <div onclick="selectMascot(3)" class="cursor-pointer bg-zinc-900/80 hover:border-emerald-500 p-2 rounded-lg border border-zinc-800 text-center transition-all">
          <p class="text-[10px] font-bold text-emerald-400 mb-1">Usako</p>
          <img src="data:image/png;base64,{mascots_data[3]['static']}" class="w-16 h-16 mx-auto object-contain" alt="Usako">
          <span class="text-[9px] text-zinc-500 mt-1 block">Regarder ▶</span>
        </div>
        <div onclick="selectMascot(4)" class="cursor-pointer bg-zinc-900/80 hover:border-rose-500 p-2 rounded-lg border border-zinc-800 text-center transition-all">
          <p class="text-[10px] font-bold text-rose-400 mb-1">Inuko</p>
          <img src="data:image/png;base64,{mascots_data[4]['static']}" class="w-16 h-16 mx-auto object-contain" alt="Inuko">
          <span class="text-[9px] text-zinc-500 mt-1 block">Regarder ▶</span>
        </div>
        <div onclick="selectMascot(5)" class="cursor-pointer bg-zinc-900/80 hover:border-purple-500 p-2 rounded-lg border border-zinc-800 text-center transition-all">
          <p class="text-[10px] font-bold text-purple-400 mb-1">Hatoko</p>
          <img src="data:image/png;base64,{mascots_data[5]['static']}" class="w-16 h-16 mx-auto object-contain" alt="Hatoko">
          <span class="text-[9px] text-zinc-500 mt-1 block">Regarder ▶</span>
        </div>
      </div>
    </div>
  </div>

  <script>
    const mascots = {mascots_json};
    let currentIndex = 0;
    let currentMode = 'video';

    function selectMascot(index) {{
      currentIndex = index;
      const m = mascots[index];
      
      document.querySelectorAll('.mascot-btn').forEach((btn, idx) => {{
        if (idx === index) {{
          btn.classList.add('active');
        }} else {{
          btn.classList.remove('active');
        }}
      }});

      document.getElementById('detail-name').innerText = m.name;
      document.getElementById('detail-role').innerText = m.role;
      document.getElementById('detail-desc').innerText = m.desc;
      
      const video = document.getElementById('main-video');
      video.src = 'data:video/mp4;base64,' + m.video;
      video.load();
      video.play().catch(e => console.log('Autoplay blocked:', e));

      document.getElementById('main-anim-img').src = 'data:image/gif;base64,' + m.anim;
      document.getElementById('main-static-img').src = 'data:image/png;base64,' + m.static;
    }}

    function setViewMode(mode) {{
      currentMode = mode;
      document.getElementById('tab-video-btn').className = "px-2.5 py-1 text-xs rounded bg-zinc-800 text-zinc-400 font-medium";
      document.getElementById('tab-anim-btn').className = "px-2.5 py-1 text-xs rounded bg-zinc-800 text-zinc-400 font-medium";
      document.getElementById('tab-static-btn').className = "px-2.5 py-1 text-xs rounded bg-zinc-800 text-zinc-400 font-medium";

      document.getElementById('video-container').classList.add('hidden');
      document.getElementById('anim-container').classList.add('hidden');
      document.getElementById('static-container').classList.add('hidden');

      if (mode === 'video') {{
        document.getElementById('tab-video-btn').className = "px-2.5 py-1 text-xs rounded bg-cyan-500 text-black font-bold";
        document.getElementById('video-container').classList.remove('hidden');
        document.getElementById('main-video').play();
      }} else if (mode === 'anim') {{
        document.getElementById('tab-anim-btn').className = "px-2.5 py-1 text-xs rounded bg-cyan-500 text-black font-bold";
        document.getElementById('anim-container').classList.remove('hidden');
      }} else {{
        document.getElementById('tab-static-btn').className = "px-2.5 py-1 text-xs rounded bg-cyan-500 text-black font-bold";
        document.getElementById('static-container').classList.remove('hidden');
      }}
    }}
  </script>
</body>
</html>
"""

with open("/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68/authentic_veo_moodboard_widget.html", "w") as f:
    f.write(html_content)

print("Saved authentic_veo_moodboard_widget.html!")
