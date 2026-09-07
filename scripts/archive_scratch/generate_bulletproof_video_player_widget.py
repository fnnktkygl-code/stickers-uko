import base64
import json
import os

brain_dir = "/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68"

def to_b64(filepath):
    with open(filepath, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

mascots = [
    {
        "id": "aituko",
        "name": "AItuko",
        "role": "Robot Porcelaine",
        "color": "#00E5FF",
        "video": to_b64("assets/00_idle/looped_video.mp4"),
        "static": to_b64("assets/00_idle/static.png"),
        "desc": "Vidéo Veo 3.1 : Yeux cyan (#00E5FF) qui clignent naturellement, micro-mouvements des bras et du corps en porcelaine."
    },
    {
        "id": "owluko",
        "name": "Owluko",
        "role": "Chouette Savante",
        "color": "#F59E0B",
        "video": to_b64("mascots/owluko/assets/00_idle/looped_video.mp4"),
        "static": to_b64("mascots/owluko/assets/00_idle/static.png"),
        "desc": "Vidéo Veo 3.1 : Clignement doux des yeux dorés ambrés, respiration corporelle 3D, micro-balancement bienveillant."
    },
    {
        "id": "luneko",
        "name": "Luneko",
        "role": "Chat Tabby Roux",
        "color": "#FB923C",
        "video": to_b64("mascots/luneko/assets/00_idle/looped_video.mp4"),
        "static": to_b64("mascots/luneko/assets/00_idle/static.png"),
        "desc": "Vidéo Veo 3.1 : Respiration féline 3D vivante, clignement des yeux, queue souple et torse blanc solide."
    },
    {
        "id": "usako",
        "name": "Usako",
        "role": "Lapin Zen",
        "color": "#10B981",
        "video": to_b64("mascots/usako/assets/00_idle/looped_video.mp4"),
        "static": to_b64("mascots/usako/assets/00_idle/static.png"),
        "desc": "Vidéo Veo 3.1 : Respiration corporelle 3D, micro-mouvement des longues oreilles, clignement doux et sa marque brune signature."
    },
    {
        "id": "inuko",
        "name": "Inuko",
        "role": "Doberman Gardien",
        "color": "#F43F5E",
        "video": to_b64("mascots/inuko/assets/00_idle/looped_video.mp4"),
        "static": to_b64("mascots/inuko/assets/00_idle/static.png"),
        "desc": "Vidéo Veo 3.1 : Posture fière et vivante, respiration pectorale réaliste, regard vigilant et clignement naturel."
    },
    {
        "id": "hatoko",
        "name": "Hatoko",
        "role": "Pigeon Voyageur",
        "color": "#A855F7",
        "video": to_b64("mascots/hatoko/assets/00_idle/looped_video.mp4"),
        "static": to_b64("mascots/hatoko/assets/00_idle/static.png"),
        "desc": "Vidéo Veo 3.1 : Respiration duveteuse, clignement joyeux, sacoche en cuir fermée propre sans débordement."
    }
]

mascots_json = json.dumps(mascots)

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
          <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
          <span class="text-[10px] uppercase font-bold tracking-wider text-emerald-400">Lecteur Vidéo Veo 3.1 HD (MP4 Natif)</span>
        </div>
        <h1 class="text-base font-bold text-white mt-0.5">Vidéos Sources Veo 3.1 : État 00_idle (4.0s @ 24fps)</h1>
        <p class="text-xs text-zinc-400 mt-1">Lecture vidéo native fluide à 100% avec accélération matérielle.</p>
      </div>
      <span class="text-xs bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 px-3 py-1 rounded-full font-bold">
        MP4 Natif ▶️
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

    <!-- Video Player Viewport -->
    <div class="bg-zinc-card border border-zinc-800 rounded-xl p-4 shadow-xl">
      <div class="flex items-center justify-between pb-3 border-b border-zinc-800">
        <div>
          <h2 id="detail-name" class="text-base font-bold text-white flex items-center gap-2">AItuko</h2>
          <p id="detail-role" class="text-xs text-zinc-400">Robot Porcelaine</p>
        </div>
        <div class="flex items-center gap-2">
          <button onclick="restartVideo()" class="px-2.5 py-1 text-xs bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded font-medium">Rejouer ↺</button>
          <span class="text-[11px] font-mono text-cyan-400 bg-cyan-950/60 border border-cyan-800 px-2 py-0.5 rounded">4.0s Loop</span>
        </div>
      </div>

      <!-- Native Video Tag -->
      <div class="my-4 flex items-center justify-center bg-black/60 rounded-xl p-2 border border-zinc-800">
        <video id="main-video" class="w-full max-h-[380px] object-contain rounded-lg shadow-2xl" autoplay loop muted playsinline controls>
          <source id="video-source" src="data:video/mp4;base64,{mascots[0]['video']}" type="video/mp4">
        </video>
      </div>

      <p id="detail-desc" class="text-xs text-zinc-300 mt-2 p-3 bg-zinc-900/60 rounded-lg border border-zinc-800/80 leading-relaxed">
        {mascots[0]['desc']}
      </p>
    </div>

    <!-- 6 Mascots Video Grid -->
    <div class="bg-zinc-card border border-zinc-800 rounded-xl p-4 shadow-lg space-y-3">
      <div class="flex items-center justify-between">
        <h3 class="text-xs font-bold uppercase tracking-wider text-zinc-300">Toutes les Vidéos Veo 3.1 en Direct (Cliquez pour afficher)</h3>
        <span class="text-[10px] text-cyan-400 font-mono">6 Mascottes</span>
      </div>
      <div class="grid grid-cols-3 md:grid-cols-6 gap-2">
        <div onclick="selectMascot(0)" class="cursor-pointer bg-zinc-900/80 hover:border-cyan-500 p-2 rounded-lg border border-zinc-800 text-center transition-all">
          <p class="text-[10px] font-bold text-cyan-400 mb-1">AItuko</p>
          <img src="data:image/png;base64,{mascots[0]['static']}" class="w-16 h-16 mx-auto object-contain" alt="AItuko">
          <span class="text-[9px] text-zinc-500 mt-1 block">Voir Vidéo ▶</span>
        </div>
        <div onclick="selectMascot(1)" class="cursor-pointer bg-zinc-900/80 hover:border-amber-500 p-2 rounded-lg border border-zinc-800 text-center transition-all">
          <p class="text-[10px] font-bold text-amber-400 mb-1">Owluko</p>
          <img src="data:image/png;base64,{mascots[1]['static']}" class="w-16 h-16 mx-auto object-contain" alt="Owluko">
          <span class="text-[9px] text-zinc-500 mt-1 block">Voir Vidéo ▶</span>
        </div>
        <div onclick="selectMascot(2)" class="cursor-pointer bg-zinc-900/80 hover:border-orange-500 p-2 rounded-lg border border-zinc-800 text-center transition-all">
          <p class="text-[10px] font-bold text-orange-400 mb-1">Luneko</p>
          <img src="data:image/png;base64,{mascots[2]['static']}" class="w-16 h-16 mx-auto object-contain" alt="Luneko">
          <span class="text-[9px] text-zinc-500 mt-1 block">Voir Vidéo ▶</span>
        </div>
        <div onclick="selectMascot(3)" class="cursor-pointer bg-zinc-900/80 hover:border-emerald-500 p-2 rounded-lg border border-zinc-800 text-center transition-all">
          <p class="text-[10px] font-bold text-emerald-400 mb-1">Usako</p>
          <img src="data:image/png;base64,{mascots[3]['static']}" class="w-16 h-16 mx-auto object-contain" alt="Usako">
          <span class="text-[9px] text-zinc-500 mt-1 block">Voir Vidéo ▶</span>
        </div>
        <div onclick="selectMascot(4)" class="cursor-pointer bg-zinc-900/80 hover:border-rose-500 p-2 rounded-lg border border-zinc-800 text-center transition-all">
          <p class="text-[10px] font-bold text-rose-400 mb-1">Inuko</p>
          <img src="data:image/png;base64,{mascots[4]['static']}" class="w-16 h-16 mx-auto object-contain" alt="Inuko">
          <span class="text-[9px] text-zinc-500 mt-1 block">Voir Vidéo ▶</span>
        </div>
        <div onclick="selectMascot(5)" class="cursor-pointer bg-zinc-900/80 hover:border-purple-500 p-2 rounded-lg border border-zinc-800 text-center transition-all">
          <p class="text-[10px] font-bold text-purple-400 mb-1">Hatoko</p>
          <img src="data:image/png;base64,{mascots[5]['static']}" class="w-16 h-16 mx-auto object-contain" alt="Hatoko">
          <span class="text-[9px] text-zinc-500 mt-1 block">Voir Vidéo ▶</span>
        </div>
      </div>
    </div>
  </div>

  <script>
    const mascots = {mascots_json};
    let currentIndex = 0;

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
    }}

    function restartVideo() {{
      const video = document.getElementById('main-video');
      video.currentTime = 0;
      video.play();
    }}
  </script>
</body>
</html>
"""

with open("/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68/video_player_widget.html", "w") as f:
    f.write(html_content)

print("Saved video_player_widget.html successfully!")
