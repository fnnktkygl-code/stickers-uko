import base64
import json
import os

mb_dir = "preview/moodboards/00_idle"

def to_b64(filepath):
    with open(filepath, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

mascots_data = [
    {
        "id": "aituko",
        "name": "AItuko",
        "role": "Robot Porcelaine",
        "color": "#00E5FF",
        "desc": "Porcelaine blanche pure, yeux et sourire cyan électrique #00E5FF, respiration douce.",
        "static": to_b64(f"{mb_dir}/aituko_static.png"),
        "anim": to_b64(f"{mb_dir}/aituko_animated.gif")
    },
    {
        "id": "owluko",
        "name": "Owluko",
        "role": "Chouette Savante",
        "color": "#F59E0B",
        "desc": "Plumes duveteuses crème, grand regard chaleureux ambré, micro-balancement bienveillant.",
        "static": to_b64(f"{mb_dir}/owluko_static.png"),
        "anim": to_b64(f"{mb_dir}/owluko_animated.gif")
    },
    {
        "id": "luneko",
        "name": "Luneko",
        "role": "Chat Tabby Roux",
        "color": "#FB923C",
        "desc": "Pelage roux tigré, torse blanc 100% plein et solide, queue souple et regard félin curieux.",
        "static": to_b64(f"{mb_dir}/luneko_static.png"),
        "anim": to_b64(f"{mb_dir}/luneko_animated.gif")
    },
    {
        "id": "usako",
        "name": "Usako",
        "role": "Lapin Zen",
        "color": "#10B981",
        "desc": "Fourrure blanche crème avec sa tache brune authentique signature, bandeau vert sauge feuille.",
        "static": to_b64(f"{mb_dir}/usako_static.png"),
        "anim": to_b64(f"{mb_dir}/usako_animated.gif")
    },
    {
        "id": "inuko",
        "name": "Inuko",
        "role": "Doberman Gardien",
        "color": "#F43F5E",
        "desc": "Robe noire et feu noble, posture assise fière et protectrice, regard vigilant.",
        "static": to_b64(f"{mb_dir}/inuko_static.png"),
        "anim": to_b64(f"{mb_dir}/inuko_animated.gif")
    },
    {
        "id": "hatoko",
        "name": "Hatoko",
        "role": "Pigeon Voyageur",
        "color": "#A855F7",
        "desc": "Plumage gris tourterelle doux, sacoche facteur en cuir propre et fermée sans débordement.",
        "static": to_b64(f"{mb_dir}/hatoko_static.png"),
        "anim": to_b64(f"{mb_dir}/hatoko_animated.gif")
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
      touch-action: pan-x pan-y pinch-zoom;
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
    .zoom-container {{
      overflow: auto;
      -webkit-overflow-scrolling: touch;
      touch-action: pan-x pan-y pinch-zoom;
    }}
    .mascot-btn.active {{
      border-color: #00E5FF;
      background: rgba(0, 229, 255, 0.16);
      color: #FFFFFF;
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
          <span class="text-[10px] uppercase font-bold tracking-wider text-emerald-400">Boucle Animée Active (24 FPS)</span>
        </div>
        <h1 class="text-base font-bold text-white mt-0.5">Moodboard Animé : État 00_idle (Présence / Respiration)</h1>
        <p class="text-xs text-zinc-400 mt-1">L'animation joue en direct par défaut. Touchez pour zoomer et changer de mascotte.</p>
      </div>
      <span class="text-xs bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 px-3 py-1 rounded-full font-bold">
        Live Motion ▶️
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

    <!-- Main Live Animation Viewport -->
    <div class="bg-zinc-card border border-zinc-800 rounded-xl p-4 shadow-xl">
      <div class="flex items-center justify-between pb-3 border-b border-zinc-800">
        <div>
          <h2 id="detail-name" class="text-base font-bold text-white flex items-center gap-2">AItuko</h2>
          <p id="detail-role" class="text-xs text-zinc-400">Robot Porcelaine</p>
        </div>
        
        <!-- Controls: Background + Mode -->
        <div class="flex items-center gap-1.5">
          <button onclick="setPreviewBg('dark')" id="bg-btn-dark" class="px-2.5 py-1 text-[11px] rounded bg-cyan-500 text-black font-bold">Sombre</button>
          <button onclick="setPreviewBg('light')" id="bg-btn-light" class="px-2.5 py-1 text-[11px] rounded bg-zinc-800 text-zinc-400 font-medium">Clair</button>
          <button onclick="setPreviewBg('checker')" id="bg-btn-checker" class="px-2.5 py-1 text-[11px] rounded bg-zinc-800 text-zinc-400 font-medium">Damier</button>
          <button onclick="toggleAnim()" id="anim-toggle-btn" class="px-2.5 py-1 text-[11px] rounded bg-emerald-500/20 text-emerald-400 font-bold border border-emerald-500/30">Animé (En cours ▶️)</button>
        </div>
      </div>

      <!-- Zoomable Animated Viewport -->
      <div id="preview-canvas-box" class="zoom-container relative bg-pure-dark rounded-xl border border-zinc-800 my-4 flex items-center justify-center p-6 min-h-[340px]">
        <img id="detail-img" src="data:image/gif;base64,{mascots_data[0]['anim']}" class="w-72 h-72 md:w-80 md:h-80 object-contain transition-transform duration-200" alt="Mascot Live Animation">
      </div>

      <!-- Zoom Bar -->
      <div class="flex items-center justify-between bg-zinc-900/90 rounded-lg p-2.5 border border-zinc-800 text-xs">
        <span class="text-zinc-400 text-[11px]">Niveau de Zoom :</span>
        <div class="flex items-center gap-2">
          <button onclick="adjustZoom(-0.25)" class="w-7 h-7 rounded bg-zinc-800 hover:bg-zinc-700 font-bold text-sm text-zinc-200 flex items-center justify-center">-</button>
          <span id="zoom-level-text" class="font-mono text-cyan-400 font-bold w-12 text-center">100%</span>
          <button onclick="adjustZoom(0.25)" class="w-7 h-7 rounded bg-zinc-800 hover:bg-zinc-700 font-bold text-sm text-zinc-200 flex items-center justify-center">+</button>
          <button onclick="resetZoom()" class="px-2 py-1 rounded bg-zinc-800 hover:bg-zinc-700 text-[11px] text-zinc-400">Reset</button>
        </div>
      </div>

      <p id="detail-desc" class="text-xs text-zinc-300 mt-3 p-3 bg-zinc-900/60 rounded-lg border border-zinc-800/80 leading-relaxed">
        {mascots_data[0]['desc']}
      </p>
    </div>

    <!-- 6 Mascots Live Multi-Stream Grid -->
    <div class="bg-zinc-card border border-zinc-800 rounded-xl p-4 shadow-lg space-y-3">
      <div class="flex items-center justify-between">
        <h3 class="text-xs font-bold uppercase tracking-wider text-zinc-300">Les 6 Mascottes Animées en Direct</h3>
        <span class="text-[10px] text-emerald-400 font-mono">6 Loops Synchronisés</span>
      </div>
      <div class="grid grid-cols-3 md:grid-cols-6 gap-2">
        <div onclick="selectMascot(0)" class="cursor-pointer bg-zinc-900/80 hover:border-cyan-500 p-2 rounded-lg border border-zinc-800 text-center transition-all">
          <p class="text-[10px] font-bold text-cyan-400 mb-1">AItuko</p>
          <img src="data:image/gif;base64,{mascots_data[0]['anim']}" class="w-20 h-20 mx-auto object-contain" alt="AItuko Animé">
        </div>
        <div onclick="selectMascot(1)" class="cursor-pointer bg-zinc-900/80 hover:border-amber-500 p-2 rounded-lg border border-zinc-800 text-center transition-all">
          <p class="text-[10px] font-bold text-amber-400 mb-1">Owluko</p>
          <img src="data:image/gif;base64,{mascots_data[1]['anim']}" class="w-20 h-20 mx-auto object-contain" alt="Owluko Animé">
        </div>
        <div onclick="selectMascot(2)" class="cursor-pointer bg-zinc-900/80 hover:border-orange-500 p-2 rounded-lg border border-zinc-800 text-center transition-all">
          <p class="text-[10px] font-bold text-orange-400 mb-1">Luneko</p>
          <img src="data:image/gif;base64,{mascots_data[2]['anim']}" class="w-20 h-20 mx-auto object-contain" alt="Luneko Animé">
        </div>
        <div onclick="selectMascot(3)" class="cursor-pointer bg-zinc-900/80 hover:border-emerald-500 p-2 rounded-lg border border-zinc-800 text-center transition-all">
          <p class="text-[10px] font-bold text-emerald-400 mb-1">Usako</p>
          <img src="data:image/gif;base64,{mascots_data[3]['anim']}" class="w-20 h-20 mx-auto object-contain" alt="Usako Animé">
        </div>
        <div onclick="selectMascot(4)" class="cursor-pointer bg-zinc-900/80 hover:border-rose-500 p-2 rounded-lg border border-zinc-800 text-center transition-all">
          <p class="text-[10px] font-bold text-rose-400 mb-1">Inuko</p>
          <img src="data:image/gif;base64,{mascots_data[4]['anim']}" class="w-20 h-20 mx-auto object-contain" alt="Inuko Animé">
        </div>
        <div onclick="selectMascot(5)" class="cursor-pointer bg-zinc-900/80 hover:border-purple-500 p-2 rounded-lg border border-zinc-800 text-center transition-all">
          <p class="text-[10px] font-bold text-purple-400 mb-1">Hatoko</p>
          <img src="data:image/gif;base64,{mascots_data[5]['anim']}" class="w-20 h-20 mx-auto object-contain" alt="Hatoko Animé">
        </div>
      </div>
    </div>
  </div>

  <script>
    const mascots = {mascots_json};
    let currentIndex = 0;
    let isAnimated = true;  // DEFAULT TO ANIMATED ON LOAD!
    let currentZoom = 1.0;

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
      
      updateImageSrc();
      resetZoom();
    }}

    function updateImageSrc() {{
      const m = mascots[currentIndex];
      const img = document.getElementById('detail-img');
      img.src = isAnimated ? 'data:image/gif;base64,' + m.anim : 'data:image/png;base64,' + m.static;
    }}

    function toggleAnim() {{
      isAnimated = !isAnimated;
      const btn = document.getElementById('anim-toggle-btn');
      if (isAnimated) {{
        btn.innerText = "Animé (En cours ▶️)";
        btn.className = "px-2.5 py-1 text-[11px] rounded bg-emerald-500/20 text-emerald-400 font-bold border border-emerald-500/30";
      }} else {{
        btn.innerText = "Mode Statique (PNG)";
        btn.className = "px-2.5 py-1 text-[11px] rounded bg-zinc-800 text-zinc-400 font-medium border border-zinc-700";
      }}
      updateImageSrc();
    }}

    function setPreviewBg(type) {{
      const box = document.getElementById('preview-canvas-box');
      box.className = "zoom-container relative rounded-xl border border-zinc-800 my-4 flex items-center justify-center p-6 min-h-[340px] ";
      
      document.getElementById('bg-btn-dark').className = "px-2.5 py-1 text-[11px] rounded bg-zinc-800 text-zinc-400 font-medium";
      document.getElementById('bg-btn-light').className = "px-2.5 py-1 text-[11px] rounded bg-zinc-800 text-zinc-400 font-medium";
      document.getElementById('bg-btn-checker').className = "px-2.5 py-1 text-[11px] rounded bg-zinc-800 text-zinc-400 font-medium";

      if (type === 'dark') {{
        box.classList.add('bg-pure-dark');
        document.getElementById('bg-btn-dark').className = "px-2.5 py-1 text-[11px] rounded bg-cyan-500 text-black font-bold";
      }} else if (type === 'light') {{
        box.classList.add('bg-pure-light');
        document.getElementById('bg-btn-light').className = "px-2.5 py-1 text-[11px] rounded bg-cyan-500 text-black font-bold";
      }} else {{
        box.classList.add('checkerboard');
        document.getElementById('bg-btn-checker').className = "px-2.5 py-1 text-[11px] rounded bg-cyan-500 text-black font-bold";
      }}
    }}

    function adjustZoom(delta) {{
      currentZoom = Math.min(Math.max(0.5, currentZoom + delta), 3.0);
      applyZoom();
    }}

    function resetZoom() {{
      currentZoom = 1.0;
      applyZoom();
    }}

    function applyZoom() {{
      const img = document.getElementById('detail-img');
      img.style.transform = `scale(${{currentZoom}})`;
      document.getElementById('zoom-level-text').innerText = Math.round(currentZoom * 100) + '%';
    }}
  </script>
</body>
</html>
"""

with open("/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68/zoomable_moodboard_widget.html", "w") as f:
    f.write(html_content)

print("Saved live animated zoomable widget!")
