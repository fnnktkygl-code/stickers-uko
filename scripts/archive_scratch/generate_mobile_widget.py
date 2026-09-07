import base64
import os

artifact_dir = "/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68"

def to_b64(filepath):
    with open(filepath, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

owl_dark_b64 = to_b64("preview/owluko_final_flawless_dark_grid.png")
ait_dark_b64 = to_b64("preview/aituko_v2_dark_grid.png")
lun_dark_b64 = to_b64("preview/luneko_final_dark_grid.png")

# Animated GIFs
owl_idle_b64 = to_b64("mascots/owluko/assets/00_idle/animated.gif")
owl_sec_b64 = to_b64("mascots/owluko/assets/11_security/animated.gif")
ait_idle_b64 = to_b64("assets/00_idle/animated.gif")
ait_sec_b64 = to_b64("assets/11_security/animated.gif")
lun_idle_b64 = to_b64("mascots/luneko/assets/00_idle/animated.gif")
lun_sec_b64 = to_b64("mascots/luneko/assets/11_security/animated.gif")

html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      margin: 0;
      padding: 12px;
      background: #121214;
      color: #F4F4F5;
    }}
    .tab-btn {{
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
      border: 1px solid rgba(255,255,255,0.1);
      background: rgba(255,255,255,0.05);
      color: #A1A1AA;
      white-space: nowrap;
    }}
    .tab-btn.active {{
      background: #00E5FF;
      color: #09090B;
      border-color: #00E5FF;
    }}
    .card {{
      background: #18181B;
      border: 1px solid #27272A;
      border-radius: 12px;
      padding: 14px;
      margin-top: 12px;
    }}
  </style>
</head>
<body class="bg-[#121214] text-[#F4F4F5] antialiased">
  <div class="max-w-md mx-auto">
    <!-- Header -->
    <div class="flex items-center justify-between pb-3 border-b border-zinc-800">
      <div>
        <h1 class="text-base font-bold text-white flex items-center gap-2">
          <span>✨ Uko Studio — Revue Mobile</span>
        </h1>
        <p class="text-xs text-zinc-400">Validation 1 par 1 : AItuko, Owluko, Luneko</p>
      </div>
      <span class="text-[10px] bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 px-2 py-0.5 rounded-full font-semibold">
        Cahier des charges actif
      </span>
    </div>

    <!-- Tab Selector -->
    <div class="flex gap-2 mt-3 overflow-x-auto pb-1">
      <button class="tab-btn active" onclick="switchTab('lun')">🐱 Luneko (Nouveau)</button>
      <button class="tab-btn" onclick="switchTab('owl')">🦉 Owluko</button>
      <button class="tab-btn" onclick="switchTab('ait')">🤖 AItuko</button>
      <button class="tab-btn" onclick="switchTab('sec')">🛡️ Sécurité Pure</button>
    </div>

    <!-- TAB 1: Luneko -->
    <div id="tab-lun" class="tab-pane">
      <div class="card">
        <div class="flex items-center justify-between mb-2">
          <h2 class="text-sm font-semibold text-zinc-100">Grille Complète Luneko (12 états + Idle)</h2>
          <span class="text-[11px] text-amber-400 font-bold">100% Solide</span>
        </div>
        <img src="data:image/png;base64,{lun_dark_b64}" class="w-full rounded-lg border border-zinc-800 shadow-md" alt="Luneko Grille">
        <div class="mt-3 space-y-1.5 text-xs text-zinc-300">
          <div class="flex items-center gap-1.5 text-emerald-400 font-medium">
            <span>✓</span> <span>10_idea : Ampoule 3D dorée brillante au-dessus de la tête</span>
          </div>
          <div class="flex items-center gap-1.5 text-emerald-400 font-medium">
            <span>✓</span> <span>08_searching : Loupe 3D orange tenue dans la patte</span>
          </div>
          <div class="flex items-center gap-1.5 text-emerald-400 font-medium">
            <span>✓</span> <span>11_security : Geste de protection pur pattes levées (zéro bouclier)</span>
          </div>
          <div class="flex items-center gap-1.5 text-emerald-400 font-medium">
            <span>✓</span> <span>06_sleeping : Sommeil continu sans réveil</span>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 2: Owluko -->
    <div id="tab-owl" class="tab-pane hidden">
      <div class="card">
        <div class="flex items-center justify-between mb-2">
          <h2 class="text-sm font-semibold text-zinc-100">Grille Complète Owluko</h2>
          <span class="text-[11px] text-zinc-400">512×512</span>
        </div>
        <img src="data:image/png;base64,{owl_dark_b64}" class="w-full rounded-lg border border-zinc-800 shadow-md" alt="Owluko Grille">
        <div class="mt-3 space-y-1.5 text-xs text-zinc-300">
          <div class="flex items-center gap-1.5 text-emerald-400 font-medium">
            <span>✓</span> <span>Loupe 3D unique sur 08 (sans doublon)</span>
          </div>
          <div class="flex items-center gap-1.5 text-emerald-400 font-medium">
            <span>✓</span> <span>Ailes protectrices sur 11 (sans bouclier néon)</span>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 3: AItuko -->
    <div id="tab-ait" class="tab-pane hidden">
      <div class="card">
        <div class="flex items-center justify-between mb-2">
          <h2 class="text-sm font-semibold text-zinc-100">Grille Complète AItuko</h2>
          <span class="text-[11px] text-cyan-400 font-bold">Cyan #00E5FF</span>
        </div>
        <img src="data:image/png;base64,{ait_dark_b64}" class="w-full rounded-lg border border-zinc-800 shadow-md" alt="AItuko Grille">
        <div class="mt-3 space-y-1.5 text-xs text-zinc-300">
          <div class="flex items-center gap-1.5 text-cyan-400 font-medium">
            <span>✓</span> <span>Couleur yeux & sourire unifiée</span>
          </div>
          <div class="flex items-center gap-1.5 text-cyan-400 font-medium">
            <span>✓</span> <span>Mains protectrices levées sur 11 (zéro fumée)</span>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 4: Security Postures -->
    <div id="tab-sec" class="tab-pane hidden">
      <div class="grid grid-cols-3 gap-2 mt-3 text-center">
        <div class="card !mt-0 !p-2">
          <p class="text-[11px] font-semibold text-zinc-300 mb-1">AItuko</p>
          <img src="data:image/gif;base64,{ait_sec_b64}" class="w-20 h-20 mx-auto object-contain" alt="AItuko Sec">
          <span class="text-[9px] text-zinc-500 mt-1 block">Mains levées</span>
        </div>
        <div class="card !mt-0 !p-2">
          <p class="text-[11px] font-semibold text-zinc-300 mb-1">Owluko</p>
          <img src="data:image/gif;base64,{owl_sec_b64}" class="w-20 h-20 mx-auto object-contain" alt="Owluko Sec">
          <span class="text-[9px] text-zinc-500 mt-1 block">Ailes protectrices</span>
        </div>
        <div class="card !mt-0 !p-2">
          <p class="text-[11px] font-semibold text-zinc-300 mb-1">Luneko</p>
          <img src="data:image/gif;base64,{lun_sec_b64}" class="w-20 h-20 mx-auto object-contain" alt="Luneko Sec">
          <span class="text-[9px] text-zinc-500 mt-1 block">Pattes de garde</span>
        </div>
      </div>
    </div>
  </div>

  <script>
    function switchTab(tabId) {{
      document.querySelectorAll('.tab-pane').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
      document.getElementById('tab-' + tabId).classList.remove('hidden');
      event.currentTarget.classList.add('active');
    }}
  </script>
</body>
</html>
"""

with open(f"{artifact_dir}/mobile_review_widget.html", "w") as f:
    f.write(html_content)

print(f"✅ Generated updated mobile widget with Luneko!")
