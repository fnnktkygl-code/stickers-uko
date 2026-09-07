import json
import os

# Read generated idle lottie json
with open('assets/00_idle/lottie.json', 'r', encoding='utf-8') as f:
    idle_lottie = json.load(f)

# Read waving lottie json
with open('assets/01_waving/lottie.json', 'r', encoding='utf-8') as f:
    waving_lottie = json.load(f)

# Read celebration lottie json
with open('assets/02_celebrating/lottie.json', 'r', encoding='utf-8') as f:
    celeb_lottie = json.load(f)

# Read thinking lottie json
with open('assets/03_ai_thinking/lottie.json', 'r', encoding='utf-8') as f:
    thinking_lottie = json.load(f)

# Read error lottie json
with open('assets/04_error_404/lottie.json', 'r', encoding='utf-8') as f:
    error_lottie = json.load(f)

# Read sleeping lottie json
with open('assets/06_sleeping/lottie.json', 'r', encoding='utf-8') as f:
    sleeping_lottie = json.load(f)

# Read idea lottie json
with open('assets/10_idea/lottie.json', 'r', encoding='utf-8') as f:
    idea_lottie = json.load(f)

# Read security lottie json
with open('assets/11_security/lottie.json', 'r', encoding='utf-8') as f:
    security_lottie = json.load(f)

lottie_bundle = {
    "00_idle": idle_lottie,
    "01_waving": waving_lottie,
    "02_celebrating": celeb_lottie,
    "03_ai_thinking": thinking_lottie,
    "04_error_404": error_lottie,
    "06_sleeping": sleeping_lottie,
    "10_idea": idea_lottie,
    "11_security": security_lottie
}

html_template = f'''<!DOCTYPE html>
<html lang="fr" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AItuko Vector Master Suite & Interactive 3D Fidelity Rig</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.12.2/lottie.min.js"></script>
  <style>
    :root {{
      --background: #0B0F17;
      --card: #131A26;
      --card-hover: #1A2333;
      --border: #222F44;
      --foreground: #F8FAFC;
      --muted: #94A3B8;
      --cyan: #00F0FF;
      --cyan-glow: rgba(0, 240, 255, 0.4);
    }}
    body {{
      background-color: var(--background);
      color: var(--foreground);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}
    .glow-cyan {{
      filter: drop-shadow(0 0 16px var(--cyan-glow));
    }}
    .panel-glass {{
      background: rgba(19, 26, 38, 0.75);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border);
    }}
    /* Custom scrollbars */
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: #2A3B53; border-radius: 3px; }}
  </style>
</head>
<body class="min-h-screen p-4 sm:p-6 lg:p-8 flex flex-col items-center justify-start">

  <div class="w-full max-w-6xl space-y-6">
    
    <!-- Header -->
    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-4 border-b border-[var(--border)]">
      <div>
        <div class="flex items-center gap-3">
          <span class="px-2.5 py-1 rounded-full text-xs font-semibold bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 tracking-wide uppercase">Vector 4.0s Harmonic Engine</span>
          <span class="px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">100% 3D Porcelain Fidelity</span>
        </div>
        <h1 class="text-2xl sm:text-3xl font-bold tracking-tight mt-2 text-white flex items-center gap-2">
          AItuko Interactive Vector Mascot & Lottie Suite
        </h1>
        <p class="text-sm text-[var(--muted)] mt-1">
          Modélisation vectorielle pièce-par-pièce & cinématique harmonique 4.0s (120 frames @ 30fps) conforme au modèle 3D original.
        </p>
      </div>

      <div class="flex items-center gap-2">
        <button onclick="toggleViewMode('interactive')" id="btnInteractive" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-cyan-500 text-black shadow-lg shadow-cyan-500/20 transition">
          🎮 Rig Interactif
        </button>
        <button onclick="toggleViewMode('lottie')" id="btnLottie" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-[var(--card)] hover:bg-[var(--card-hover)] text-[var(--muted)] border border-[var(--border)] transition">
          🎬 Lecteur Lottie (JSON)
        </button>
        <button onclick="toggleViewMode('compare')" id="btnCompare" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-[var(--card)] hover:bg-[var(--card-hover)] text-[var(--muted)] border border-[var(--border)] transition">
          🔍 Comparatif 3D Réel
        </button>
      </div>
    </div>

    <!-- MAIN STAGE -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">

      <!-- LEFT: Mascot Viewer (Canvas & Stage) -->
      <div class="lg:col-span-7 panel-glass rounded-2xl p-6 flex flex-col items-center justify-between min-h-[520px] relative overflow-hidden">
        
        <!-- Top Stage Status Bar -->
        <div class="w-full flex items-center justify-between text-xs text-[var(--muted)] pb-2 z-10">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
            <span id="stageStatusText" class="font-mono text-emerald-400">Kinematics: 4.0s Harmonic Float</span>
          </div>
          <div class="font-mono text-[11px] bg-black/40 px-2 py-0.5 rounded border border-white/5">
            Dimensions: 512x512 Pure SVG
          </div>
        </div>

        <!-- 1. Interactive Vector Rig View -->
        <div id="interactiveContainer" class="w-full flex-1 flex flex-col items-center justify-center relative py-4">
          
          <!-- Floating Dialogue Cloud -->
          <div id="mascotBubble" class="mb-2 px-3 py-1.5 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-xs font-medium tracking-wide flex items-center gap-2 shadow-lg transition-all duration-300">
            <span id="mascotSpeech">Je suis AItuko. Bougez votre souris pour orienter mon regard ! ✨</span>
          </div>

          <!-- The Articulated SVG Rig -->
          <div class="relative w-[320px] h-[320px] sm:w-[380px] sm:h-[380px] cursor-pointer" onclick="onMascotClick()" title="Cliquez pour interagir !">
            <svg id="aitukoRigSvg" viewBox="0 0 512 512" class="w-full h-full select-none overflow-visible">
              <defs>
                <!-- 3D Studio Porcelain Shaders -->
                <linearGradient id="porcelainGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stop-color="#FFFFFF" />
                  <stop offset="35%" stop-color="#F8FAFC" />
                  <stop offset="70%" stop-color="#E2E8F0" />
                  <stop offset="100%" stop-color="#CBD5E1" />
                </linearGradient>

                <radialGradient id="headDomeGrad" cx="38%" cy="25%" r="70%">
                  <stop offset="0%" stop-color="#FFFFFF" />
                  <stop offset="45%" stop-color="#F8FAFC" />
                  <stop offset="80%" stop-color="#E2E8F0" />
                  <stop offset="100%" stop-color="#CBD5E1" />
                </radialGradient>

                <linearGradient id="specularStreak" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0" />
                  <stop offset="50%" stop-color="#FFFFFF" stop-opacity="0.95" />
                  <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0" />
                </linearGradient>

                <linearGradient id="armPorcelainGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stop-color="#E2E8F0" />
                  <stop offset="30%" stop-color="#FFFFFF" />
                  <stop offset="70%" stop-color="#F8FAFC" />
                  <stop offset="100%" stop-color="#CBD5E1" />
                </linearGradient>

                <radialGradient id="podGrad" cx="40%" cy="30%" r="65%">
                  <stop offset="0%" stop-color="#FFFFFF" />
                  <stop offset="50%" stop-color="#F1F5F9" />
                  <stop offset="100%" stop-color="#CBD5E1" />
                </radialGradient>

                <!-- Deep Obsidian Curved Glass Visor -->
                <radialGradient id="visorGlassGrad" cx="50%" cy="35%" r="65%">
                  <stop offset="0%" stop-color="#181B26" />
                  <stop offset="60%" stop-color="#10121A" />
                  <stop offset="100%" stop-color="#090A0F" />
                </radialGradient>

                <linearGradient id="visorArcReflection" x1="20%" y1="0%" x2="80%" y2="100%">
                  <stop offset="0%" stop-color="#94A3B8" stop-opacity="0.45" />
                  <stop offset="40%" stop-color="#64748B" stop-opacity="0.25" />
                  <stop offset="100%" stop-color="#334155" stop-opacity="0.0" />
                </linearGradient>

                <!-- Electric Cyan Neon Bloom -->
                <filter id="cyanGlow" x="-50%" y="-50%" width="200%" height="200%">
                  <feGaussianBlur in="SourceGraphic" stdDeviation="6" result="blur1" />
                  <feGaussianBlur in="SourceGraphic" stdDeviation="14" result="blur2" />
                  <feMerge>
                    <feMergeNode in="blur2" />
                    <feMergeNode in="blur1" />
                    <feMergeNode in="SourceGraphic" />
                  </feMerge>
                </filter>

                <!-- Ambient Shadow -->
                <radialGradient id="shadowGrad" cx="50%" cy="50%" r="50%">
                  <stop offset="0%" stop-color="#0F172A" stop-opacity="0.32" />
                  <stop offset="50%" stop-color="#0F172A" stop-opacity="0.14" />
                  <stop offset="100%" stop-color="#0F172A" stop-opacity="0" />
                </radialGradient>
              </defs>

              <!-- 1. Ground Shadow (Coupled with elevation) -->
              <ellipse id="groundShadow" cx="256" cy="495" rx="90" ry="13" fill="url(#shadowGrad)" />

              <!-- Master Floating Entity Group -->
              <g id="masterFloatRig">
                
                <!-- 2. Support Pods (Feet) -->
                <g id="podsGroup">
                  <!-- Left Pod -->
                  <g id="leftPod" transform="translate(211, 479) rotate(-8)">
                    <rect x="-27" y="-29" width="54" height="58" rx="27" fill="#CBD5E1" />
                    <rect x="-25" y="-28" width="50" height="54" rx="25" fill="url(#podGrad)" />
                    <ellipse cx="-4" cy="-18" rx="12" ry="5" fill="#FFFFFF" opacity="0.85" />
                  </g>
                  <!-- Right Pod -->
                  <g id="rightPod" transform="translate(301, 479) rotate(8)">
                    <rect x="-27" y="-29" width="54" height="58" rx="27" fill="#CBD5E1" />
                    <rect x="-25" y="-28" width="50" height="54" rx="25" fill="url(#podGrad)" />
                    <ellipse cx="-4" cy="-18" rx="12" ry="5" fill="#FFFFFF" opacity="0.85" />
                  </g>
                </g>

                <!-- 3. Porcelain Torso -->
                <g id="torsoGroup">
                  <!-- Outer Shadow Rim -->
                  <rect x="151" y="180" width="210" height="270" rx="90" fill="#CBD5E1" />
                  <!-- Main Porcelain Shell -->
                  <rect x="153" y="181" width="206" height="265" rx="88" fill="url(#porcelainGrad)" />
                  <!-- Left Flank Soft Diffuse Shade -->
                  <rect x="155" y="196" width="65" height="235" rx="32" fill="#E2E8F0" opacity="0.45" />
                  <!-- Right Flank Specular Gloss Streak -->
                  <rect x="331" y="215" width="18" height="180" rx="9" fill="url(#specularStreak)" />
                  <!-- Top Shoulder Soft Glow -->
                  <ellipse cx="256" cy="205" rx="55" ry="12" fill="#FFFFFF" opacity="0.5" />
                  <!-- Under-chin Neck Shadow -->
                  <ellipse cx="256" cy="183" rx="48" ry="9" fill="#0F172A" opacity="0.28" />
                </g>

                <!-- 4. Porcelain Head Dome -->
                <g id="headGroup" transform-origin="256 183">
                  <!-- Head Base Shadow Rim -->
                  <rect x="132" y="4" width="248" height="190" rx="76" fill="#CBD5E1" />
                  <!-- Main Porcelain Helmet Shell -->
                  <rect x="133.5" y="5.5" width="245" height="187" rx="75" fill="url(#headDomeGrad)" />
                  <!-- Crown Specular Highlight -->
                  <ellipse cx="238" cy="25" rx="58" ry="13" fill="#FFFFFF" opacity="0.90" />
                  <!-- Left Cheek Ambient Soft Shade -->
                  <ellipse cx="160" cy="89" rx="13" ry="30" fill="#E2E8F0" opacity="0.4" />
                  <!-- Right Temple Specular Gloss -->
                  <ellipse cx="352" cy="69" rx="9" ry="24" transform="rotate(18, 352, 69)" fill="#FFFFFF" opacity="0.65" />
                  <!-- Chin Ambient Soft Rim -->
                  <ellipse cx="256" cy="183" rx="52" ry="7" fill="#CBD5E1" opacity="0.5" />

                  <!-- 5. Visor Faceplate -->
                  <g id="visorGroup">
                    <!-- Visor Bezel Frame -->
                    <rect x="156" y="24" width="200" height="150" rx="67" fill="#090A0F" />
                    <!-- Obsidian Glass -->
                    <rect x="157.5" y="25.5" width="197" height="147" rx="65" fill="url(#visorGlassGrad)" stroke="#1F2433" stroke-width="1.5" />
                    <!-- Curved Specular Arc Reflection -->
                    <path d="M 180, 72 C 205, 42 245, 36 295, 44 C 275, 48 220, 56 195, 84 Z" fill="url(#visorArcReflection)" />
                    <ellipse cx="256" cy="46" rx="48" ry="7" fill="#FFFFFF" opacity="0.20" />
                    
                    <!-- 6. Electric Cyan Neon Eyes (Gaze-tracking & morphing) -->
                    <g id="eyesGazeGroup">
                      <!-- Left Eye Group -->
                      <g id="leftEyeRig" transform-origin="211 99">
                        <path id="leftEyeBloom" d="M 190, 105 C 195, 88 227, 88 232, 105" stroke="#00F0FF" stroke-width="18" stroke-linecap="round" fill="none" opacity="0.4" filter="url(#cyanGlow)" />
                        <path id="leftEyeCore" d="M 190, 105 C 195, 88 227, 88 232, 105" stroke="#00F0FF" stroke-width="9.5" stroke-linecap="round" fill="none" />
                        <path id="leftEyeLaser" d="M 190, 105 C 195, 88 227, 88 232, 105" stroke="#E0F7FF" stroke-width="3.5" stroke-linecap="round" fill="none" />
                      </g>
                      <!-- Right Eye Group -->
                      <g id="rightEyeRig" transform-origin="301 99">
                        <path id="rightEyeBloom" d="M 280, 105 C 285, 88 317, 88 322, 105" stroke="#00F0FF" stroke-width="18" stroke-linecap="round" fill="none" opacity="0.4" filter="url(#cyanGlow)" />
                        <path id="rightEyeCore" d="M 280, 105 C 285, 88 317, 88 322, 105" stroke="#00F0FF" stroke-width="9.5" stroke-linecap="round" fill="none" />
                        <path id="rightEyeLaser" d="M 280, 105 C 285, 88 317, 88 322, 105" stroke="#E0F7FF" stroke-width="3.5" stroke-linecap="round" fill="none" />
                      </g>
                    </g>
                  </g>
                </g>

                <!-- 7. Floating Left Arm -->
                <g id="leftArmGroup" transform="translate(132, 333)" transform-origin="0 -50">
                  <rect x="-28" y="-70" width="56" height="140" rx="28" fill="#CBD5E1" />
                  <rect x="-26" y="-68" width="52" height="136" rx="26" fill="url(#armPorcelainGrad)" />
                  <rect x="-17" y="-55" width="8" height="88" rx="4" fill="url(#specularStreak)" />
                  <rect x="10" y="-48" width="14" height="96" rx="7" fill="#CBD5E1" opacity="0.35" />
                </g>

                <!-- 8. Floating Right Arm -->
                <g id="rightArmGroup" transform="translate(380, 333)" transform-origin="0 -50">
                  <rect x="-28" y="-70" width="56" height="140" rx="28" fill="#CBD5E1" />
                  <rect x="-26" y="-68" width="52" height="136" rx="26" fill="url(#armPorcelainGrad)" />
                  <rect x="9" y="-55" width="8" height="88" rx="4" fill="url(#specularStreak)" />
                  <rect x="-24" y="-48" width="14" height="96" rx="7" fill="#CBD5E1" opacity="0.35" />
                </g>

                <!-- Holographic Props Container -->
                <g id="holoProps"></g>
              </g>
            </svg>
          </div>

          <div class="text-[11px] text-[var(--muted)] font-mono mt-2">
            Pointez ou glissez pour orienter la tête et les yeux &bull; Cliquez pour faire réagir
          </div>
        </div>

        <!-- 2. Lottie Player View (Hidden by default) -->
        <div id="lottieContainer" class="w-full flex-1 hidden flex-col items-center justify-center relative py-4">
          <div id="lottiePlayerBox" class="w-[320px] h-[320px] sm:w-[380px] sm:h-[380px]"></div>
          
          <!-- Lottie Controls Bar -->
          <div class="w-full max-w-md mt-4 p-2 rounded-xl bg-black/40 border border-[var(--border)] flex items-center justify-between gap-3 text-xs">
            <button onclick="toggleLottiePlay()" id="lottiePlayBtn" class="px-2.5 py-1 rounded bg-cyan-500 text-black font-semibold">Pause</button>
            <input type="range" id="lottieTimeline" min="0" max="119" value="0" class="flex-1 accent-cyan-400 cursor-pointer" oninput="onLottieSeek(event)">
            <span id="lottieFrameText" class="font-mono text-[11px] w-14 text-right">0 / 120</span>
            <select id="lottieSpeedSelect" onchange="onLottieSpeedChange(event)" class="bg-[var(--card)] text-white text-[11px] rounded px-1.5 py-1 border border-[var(--border)]">
              <option value="0.5">0.5x</option>
              <option value="1.0" selected>1.0x</option>
              <option value="1.5">1.5x</option>
              <option value="2.0">2.0x</option>
            </select>
          </div>
        </div>

        <!-- 3. Side-by-Side 3D Comparison View (Hidden by default) -->
        <div id="compareContainer" class="w-full flex-1 hidden flex-col items-center justify-center relative py-4">
          <div class="grid grid-cols-2 gap-4 w-full max-w-lg items-center">
            <div class="flex flex-col items-center">
              <span class="text-xs font-semibold text-cyan-400 mb-1">Rendu 3D Original (Référence)</span>
              <div class="w-full aspect-square rounded-xl bg-black/40 border border-white/10 p-2 flex items-center justify-center">
                <img src="aituko_3d_master_crop_512.png" alt="AItuko 3D Master" class="w-full h-full object-contain drop-shadow-xl" />
              </div>
            </div>
            <div class="flex flex-col items-center">
              <span class="text-xs font-semibold text-emerald-400 mb-1">Modèle Vectoriel Pur (Lottie/SVG)</span>
              <div class="w-full aspect-square rounded-xl bg-black/40 border border-emerald-500/30 p-2 flex items-center justify-center relative">
                <div id="compareLottieBox" class="w-full h-full"></div>
              </div>
            </div>
          </div>
          <div class="mt-4 text-xs text-[var(--muted)] text-center max-w-md">
            Superposition parfaite des proportions : dôme oblate 245x187, visière incurvée 197x147, yeux néon à Y=100, pods et bras flottants indépendants.
          </div>
        </div>

      </div>

      <!-- RIGHT: Interactive Controls, States & In-App Simulator -->
      <div class="lg:col-span-5 space-y-6">

        <!-- Quick State Switcher (13 States) -->
        <div class="panel-glass rounded-2xl p-5 space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <span>🎭</span> États & Animations
            </h3>
            <span class="text-[11px] text-cyan-400 font-mono">13 États Disponibles</span>
          </div>

          <div class="grid grid-cols-3 gap-2 text-xs">
            <button onclick="switchState('00_idle')" class="state-btn py-2 px-2 rounded-lg bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-semibold transition text-center" data-state="00_idle">00_idle</button>
            <button onclick="switchState('01_waving')" class="state-btn py-2 px-2 rounded-lg bg-[var(--card)] hover:bg-[var(--card-hover)] border border-[var(--border)] text-[var(--muted)] hover:text-white font-medium transition text-center" data-state="01_waving">01_waving</button>
            <button onclick="switchState('02_celebrating')" class="state-btn py-2 px-2 rounded-lg bg-[var(--card)] hover:bg-[var(--card-hover)] border border-[var(--border)] text-[var(--muted)] hover:text-white font-medium transition text-center" data-state="02_celebrating">02_success</button>
            <button onclick="switchState('03_ai_thinking')" class="state-btn py-2 px-2 rounded-lg bg-[var(--card)] hover:bg-[var(--card-hover)] border border-[var(--border)] text-[var(--muted)] hover:text-white font-medium transition text-center" data-state="03_ai_thinking">03_thinking</button>
            <button onclick="switchState('04_error_404')" class="state-btn py-2 px-2 rounded-lg bg-[var(--card)] hover:bg-[var(--card-hover)] border border-[var(--border)] text-[var(--muted)] hover:text-white font-medium transition text-center" data-state="04_error_404">04_error</button>
            <button onclick="switchState('05_thumbs_up')" class="state-btn py-2 px-2 rounded-lg bg-[var(--card)] hover:bg-[var(--card-hover)] border border-[var(--border)] text-[var(--muted)] hover:text-white font-medium transition text-center" data-state="05_thumbs_up">05_thumbs_up</button>
            <button onclick="switchState('06_sleeping')" class="state-btn py-2 px-2 rounded-lg bg-[var(--card)] hover:bg-[var(--card-hover)] border border-[var(--border)] text-[var(--muted)] hover:text-white font-medium transition text-center" data-state="06_sleeping">06_sleeping</button>
            <button onclick="switchState('07_pointing')" class="state-btn py-2 px-2 rounded-lg bg-[var(--card)] hover:bg-[var(--card-hover)] border border-[var(--border)] text-[var(--muted)] hover:text-white font-medium transition text-center" data-state="07_pointing">07_pointing</button>
            <button onclick="switchState('08_searching')" class="state-btn py-2 px-2 rounded-lg bg-[var(--card)] hover:bg-[var(--card-hover)] border border-[var(--border)] text-[var(--muted)] hover:text-white font-medium transition text-center" data-state="08_searching">08_searching</button>
            <button onclick="switchState('09_loading')" class="state-btn py-2 px-2 rounded-lg bg-[var(--card)] hover:bg-[var(--card-hover)] border border-[var(--border)] text-[var(--muted)] hover:text-white font-medium transition text-center" data-state="09_loading">09_loading</button>
            <button onclick="switchState('10_idea')" class="state-btn py-2 px-2 rounded-lg bg-[var(--card)] hover:bg-[var(--card-hover)] border border-[var(--border)] text-[var(--muted)] hover:text-white font-medium transition text-center" data-state="10_idea">10_idea (Eureka)</button>
            <button onclick="switchState('11_security')" class="state-btn py-2 px-2 rounded-lg bg-[var(--card)] hover:bg-[var(--card-hover)] border border-[var(--border)] text-[var(--muted)] hover:text-white font-medium transition text-center" data-state="11_security">11_security</button>
            <button onclick="switchState('12_goodbye')" class="state-btn py-2 px-2 rounded-lg bg-[var(--card)] hover:bg-[var(--card-hover)] border border-[var(--border)] text-[var(--muted)] hover:text-white font-medium transition text-center" data-state="12_goodbye">12_goodbye</button>
            <button onclick="switchState('peek')" class="state-btn col-span-2 py-2 px-2 rounded-lg bg-amber-500/10 hover:bg-amber-500/20 border border-amber-500/30 text-amber-300 font-semibold transition text-center" data-state="peek">🙈 Peek (Mot de passe)</button>
          </div>
        </div>

        <!-- In-App Interactive Form Simulator -->
        <div class="panel-glass rounded-2xl p-5 space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <span>📱</span> Simulateur In-App Réactif
            </h3>
            <span class="text-[11px] text-emerald-400 font-mono">Démo Temps Réel</span>
          </div>
          <p class="text-xs text-[var(--muted)]">
            Testez l'interactivité réelle d'AItuko dans une application moderne (connexion, saisie, validation) :
          </p>

          <div class="space-y-3">
            <div>
              <label class="block text-[11px] font-medium text-[var(--muted)] mb-1">Identifiant / Email</label>
              <input 
                type="text" 
                id="emailInput"
                placeholder="richard@stickersuko.com" 
                oninput="onAppType(event)"
                class="w-full px-3 py-2 text-xs rounded-xl bg-black/30 border border-[var(--border)] text-white placeholder-slate-500 focus:outline-none focus:border-cyan-400 transition"
              />
            </div>

            <div>
              <label class="block text-[11px] font-medium text-[var(--muted)] mb-1">Mot de passe (se cache les yeux !)</label>
              <div class="relative">
                <input 
                  type="password" 
                  id="passwordInput"
                  placeholder="••••••••••••" 
                  onfocus="switchState('peek')"
                  onblur="if(!document.getElementById('emailInput').matches(':focus')) switchState('00_idle')"
                  class="w-full px-3 py-2 text-xs rounded-xl bg-black/30 border border-[var(--border)] text-white placeholder-slate-500 focus:outline-none focus:border-cyan-400 transition pr-10"
                />
                <button type="button" onclick="togglePasswordPeek()" class="absolute right-2.5 top-2 text-xs text-slate-400 hover:text-cyan-400 transition">
                  👁️
                </button>
              </div>
            </div>

            <div class="flex items-center gap-2 pt-1">
              <button onclick="onAppSubmit(true)" class="flex-1 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-black font-bold text-xs shadow-lg shadow-emerald-500/20 transition">
                Valider (Succès)
              </button>
              <button onclick="onAppSubmit(false)" class="flex-1 py-2 rounded-xl bg-rose-500/20 hover:bg-rose-500/30 border border-rose-500/40 text-rose-300 font-bold text-xs transition">
                Erreur (404)
              </button>
            </div>
          </div>
        </div>

        <!-- Anatomical Breakdown Specs -->
        <div class="panel-glass rounded-2xl p-5 space-y-3">
          <h3 class="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <span>📐</span> Spécifications Anatomiques 3D
          </h3>
          <div class="grid grid-cols-2 gap-2 text-[11px] font-mono">
            <div class="p-2 rounded-lg bg-black/30 border border-white/5">
              <span class="text-[var(--muted)]">Dôme Casque:</span><br/>
              <strong class="text-cyan-400">245 &times; 187 px</strong> (r=75)
            </div>
            <div class="p-2 rounded-lg bg-black/30 border border-white/5">
              <span class="text-[var(--muted)]">Visière Obsidienne:</span><br/>
              <strong class="text-cyan-400">197 &times; 147 px</strong> (r=65)
            </div>
            <div class="p-2 rounded-lg bg-black/30 border border-white/5">
              <span class="text-[var(--muted)]">Yeux Électriques:</span><br/>
              <strong class="text-cyan-400">48 &times; 31 px</strong> (Y=99)
            </div>
            <div class="p-2 rounded-lg bg-black/30 border border-white/5">
              <span class="text-[var(--muted)]">Torso Porcelaine:</span><br/>
              <strong class="text-cyan-400">206 &times; 265 px</strong> (Y=315)
            </div>
            <div class="p-2 rounded-lg bg-black/30 border border-white/5">
              <span class="text-[var(--muted)]">Bras Flottants:</span><br/>
              <strong class="text-cyan-400">54 &times; 138 px</strong> (&plusmn;124px)
            </div>
            <div class="p-2 rounded-lg bg-black/30 border border-white/5">
              <span class="text-[var(--muted)]">Pods Sustentation:</span><br/>
              <strong class="text-cyan-400">54 &times; 58 px</strong> (Y=479)
            </div>
          </div>
        </div>

      </div>

    </div>

  </div>

  <script>
    // Embedded Lottie JSON Bundle for Instant Playback
    const LOTTIE_DATA = {json.dumps(lottie_bundle)};

    let currentState = '00_idle';
    let lottieAnim = null;
    let compareAnim = null;
    let viewMode = 'interactive';

    // Kinematic Simulation Clock
    let startTime = performance.now();
    let mouseX = 256, mouseY = 256;
    let targetEyeX = 0, targetEyeY = 0;
    let currentEyeX = 0, currentEyeY = 0;
    let isBlinking = false;
    let lastBlinkTime = performance.now();
    let nextBlinkDelay = 3000;
    let isPeekRevealed = false;

    // Elements
    const masterFloat = document.getElementById('masterFloatRig');
    const groundShadow = document.getElementById('groundShadow');
    const headGroup = document.getElementById('headGroup');
    const eyesGazeGroup = document.getElementById('eyesGazeGroup');
    const leftEyeRig = document.getElementById('leftEyeRig');
    const rightEyeRig = document.getElementById('rightEyeRig');
    const leftArmGroup = document.getElementById('leftArmGroup');
    const rightArmGroup = document.getElementById('rightArmGroup');
    const podsGroup = document.getElementById('podsGroup');
    const holoProps = document.getElementById('holoProps');
    const mascotSpeech = document.getElementById('mascotSpeech');

    // 1. Natural Sinusoidal Kinematics Engine (Runs 60fps via requestAnimationFrame)
    function animateLoop(now) {{
      const elapsed = (now - startTime) / 1000.0;
      
      if (viewMode === 'interactive') {{
        // Harmonic 4.0s loop cycle
        const period = 4.0;
        const phase = (elapsed % period) / period;
        const rad = phase * 2 * Math.PI;

        // Torso & Body Levitation: apex at -18px, nadir at +16px
        const yFloat = -17 * Math.sin(rad);
        
        // Head Curiosity Sway & Inertial Lag (0.05 phase delay)
        const headPitch = -2.2 * Math.sin((phase - 0.05) * 2 * Math.PI);
        
        // Arms Flaring & Inertial Hover Swing (0.08 phase delay)
        const armSpanFlare = 5.5 * Math.sin(rad); // flares out at apex
        const armTiltL = -7 - 4.5 * Math.sin((phase - 0.08) * 2 * Math.PI);
        const armTiltR = 7 + 4.5 * Math.sin((phase - 0.08) * 2 * Math.PI);

        // Ground Shadow Dynamic Coupling (expands/darkens at nadir, contracts/fades at apex)
        const shadowScale = 1.0 - 0.18 * Math.sin(rad);
        const shadowOpacity = 0.80 - 0.25 * Math.sin(rad);

        // Apply transforms according to state
        if (currentState === '00_idle') {{
          masterFloat.setAttribute('transform', `translate(0, ${{yFloat.toFixed(2)}})`);
          headGroup.setAttribute('transform', `rotate(${{headPitch.toFixed(2)}}, 256, 183)`);
          leftArmGroup.setAttribute('transform', `translate(${{(132 - armSpanFlare).toFixed(2)}}, 333) rotate(${{armTiltL.toFixed(2)}})`);
          rightArmGroup.setAttribute('transform', `translate(${{(380 + armSpanFlare).toFixed(2)}}, 333) rotate(${{armTiltR.toFixed(2)}})`);
          groundShadow.setAttribute('transform', `scale(${{shadowScale.toFixed(3)}})`);
          groundShadow.setAttribute('transform-origin', '256 495');
          groundShadow.setAttribute('opacity', shadowOpacity.toFixed(2));
        }} else if (currentState === '06_sleeping') {{
          const sleepFloat = -10 * Math.sin((elapsed % 6.0) / 6.0 * 2 * Math.PI);
          masterFloat.setAttribute('transform', `translate(0, ${{sleepFloat.toFixed(2)}})`);
          headGroup.setAttribute('transform', 'rotate(8.5, 256, 183)');
          leftArmGroup.setAttribute('transform', 'translate(132, 338) rotate(-4)');
          rightArmGroup.setAttribute('transform', 'translate(380, 338) rotate(4)');
        }} else if (currentState === 'peek') {{
          masterFloat.setAttribute('transform', `translate(0, ${{yFloat.toFixed(2)}})`);
          headGroup.setAttribute('transform', 'rotate(0, 256, 183)');
          if (isPeekRevealed) {{
            // Slightly spread hands to peek
            leftArmGroup.setAttribute('transform', 'translate(182, 195) rotate(45)');
            rightArmGroup.setAttribute('transform', 'translate(330, 195) rotate(-45)');
          }} else {{
            // Hands fully covering eyes
            leftArmGroup.setAttribute('transform', 'translate(208, 180) rotate(60)');
            rightArmGroup.setAttribute('transform', 'translate(304, 180) rotate(-60)');
          }}
        }}

        // Smooth Cursor Eye & Head Tracking
        currentEyeX += (targetEyeX - currentEyeX) * 0.12;
        currentEyeY += (targetEyeY - currentEyeY) * 0.12;
        eyesGazeGroup.setAttribute('transform', `translate(${{currentEyeX.toFixed(2)}}, ${{currentEyeY.toFixed(2)}})`);

        // Natural Autonomous Blinking Engine
        if (currentState !== '06_sleeping' && currentState !== 'peek') {{
          if (!isBlinking && now - lastBlinkTime > nextBlinkDelay) {{
            triggerNaturalBlink();
            lastBlinkTime = now;
            nextBlinkDelay = 2500 + Math.random() * 3000;
          }}
        }}
      }}

      requestAnimationFrame(animateLoop);
    }}
    requestAnimationFrame(animateLoop);

    // 2. Natural Double-Blink Routine
    function triggerNaturalBlink() {{
      isBlinking = true;
      leftEyeRig.style.transition = 'transform 0.06s ease-in';
      rightEyeRig.style.transition = 'transform 0.06s ease-in';
      leftEyeRig.style.transform = 'scaleY(0.08)';
      rightEyeRig.style.transform = 'scaleY(0.08)';
      
      setTimeout(() => {{
        leftEyeRig.style.transition = 'transform 0.08s ease-out';
        rightEyeRig.style.transition = 'transform 0.08s ease-out';
        leftEyeRig.style.transform = 'scaleY(1.0)';
        rightEyeRig.style.transform = 'scaleY(1.0)';
        
        // 35% chance of realistic immediate double-blink
        if (Math.random() < 0.35) {{
          setTimeout(() => {{
            leftEyeRig.style.transform = 'scaleY(0.12)';
            rightEyeRig.style.transform = 'scaleY(0.12)';
            setTimeout(() => {{
              leftEyeRig.style.transform = 'scaleY(1.0)';
              rightEyeRig.style.transform = 'scaleY(1.0)';
              isBlinking = false;
            }}, 70);
          }}, 120);
        }} else {{
          isBlinking = false;
        }}
      }}, 70);
    }}

    // 3. Mouse & Pointer Tracking
    window.addEventListener('mousemove', (e) => {{
      const rect = document.getElementById('aitukoRigSvg').getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height * 0.35; // Head height
      
      const dx = (e.clientX - centerX) / (rect.width / 2);
      const dy = (e.clientY - centerY) / (rect.height / 2);
      
      // Clamp eye tracking safely inside visor boundaries
      targetEyeX = Math.max(-16, Math.min(16, dx * 16));
      targetEyeY = Math.max(-10, Math.min(10, dy * 10));
    }});

    // 4. State Switcher
    function switchState(st) {{
      currentState = st;
      
      // Update UI buttons
      document.querySelectorAll('.state-btn').forEach(btn => {{
        if (btn.getAttribute('data-state') === st) {{
          btn.className = 'state-btn py-2 px-2 rounded-lg bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-semibold transition text-center';
        }} else {{
          btn.className = 'state-btn py-2 px-2 rounded-lg bg-[var(--card)] hover:bg-[var(--card-hover)] border border-[var(--border)] text-[var(--muted)] hover:text-white font-medium transition text-center';
        }}
      }});

      // Clear Holo Props
      holoProps.innerHTML = '';
      leftArmGroup.style.transition = 'transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)';
      rightArmGroup.style.transition = 'transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)';
      headGroup.style.transition = 'transform 0.4s ease-out';

      // Set Eyes Shape
      setEyeShape('arch');

      if (st === '00_idle') {{
        mascotSpeech.innerText = "Mode repos flottant. Je surveille tout avec attention ! 👀";
      }} else if (st === '01_waving') {{
        mascotSpeech.innerText = "Bonjour ! Bienvenue sur Stickers Uko ! 👋";
        headGroup.style.transform = 'rotate(4deg, 256, 183)';
        rightArmGroup.style.transform = 'translate(390px, 250px) rotate(-18deg)';
      }} else if (st === '02_celebrating') {{
        mascotSpeech.innerText = "Hourra ! Opération réussie avec brio ! 🎉";
        leftArmGroup.style.transform = 'translate(110px, 235px) rotate(-48deg)';
        rightArmGroup.style.transform = 'translate(400px, 235px) rotate(48deg)';
        spawnConfetti();
      }} else if (st === '03_ai_thinking') {{
        mascotSpeech.innerText = "Analyse en cours... Les flux d'IA sont optimisés. 🧠";
        setEyeShape('pill');
        headGroup.style.transform = 'rotate(-6deg, 256, 183)';
        rightArmGroup.style.transform = 'translate(340px, 260px) rotate(-32deg)';
        spawnOrbitCubes();
      }} else if (st === '04_error_404') {{
        mascotSpeech.innerText = "Oups ! Quelque chose d'inattendu est survenu. ⚠️";
        setEyeShape('question');
        headGroup.style.transform = 'rotate(5deg, 256, 183)';
        leftArmGroup.style.transform = 'translate(132px, 340px) rotate(16deg)';
        rightArmGroup.style.transform = 'translate(380px, 340px) rotate(-16deg)';
        spawn404Badge();
      }} else if (st === '05_thumbs_up') {{
        mascotSpeech.innerText = "Tout est validé à 100% ! Excellent travail. 👍";
        rightArmGroup.style.transform = 'translate(390px, 275px) rotate(40deg)';
        spawnSuccessTick();
      }} else if (st === '06_sleeping') {{
        mascotSpeech.innerText = "Zzz... En veille pour préserver l'énergie... 💤";
        setEyeShape('line');
        spawnZzz();
      }} else if (st === '07_pointing') {{
        mascotSpeech.innerText = "Regardez ici : l'action requise est juste devant vous ! 🎯";
        rightArmGroup.style.transform = 'translate(410px, 290px) rotate(52deg)';
        spawnReticle();
      }} else if (st === '08_searching') {{
        mascotSpeech.innerText = "Recherche radar en cours... Scan des données à 360° ! 🔍";
        spawnRadarWave();
      }} else if (st === '09_loading') {{
        mascotSpeech.innerText = "Chargement des modules haute-fidélité... ⏳";
        spawnGyroRings();
      }} else if (st === '10_idea') {{
        mascotSpeech.innerText = "Eurêka ! J'ai trouvé la solution parfaite ! 💡";
        spawnIdeaBulb();
      }} else if (st === '11_security') {{
        mascotSpeech.innerText = "Bouclier de sécurité actif : vos données sont impénétrables ! 🛡️";
        setEyeShape('guardian');
        spawnSecurityShield();
      }} else if (st === '12_goodbye') {{
        mascotSpeech.innerText = "À très bientôt pour de nouvelles aventures ! 👋";
        setEyeShape('down_arch');
        rightArmGroup.style.transform = 'translate(390px, 260px) rotate(22deg)';
      }} else if (st === 'peek') {{
        mascotSpeech.innerText = "Chut ! Je me cache les yeux pour ne pas voir votre mot de passe ! 🙈";
      }}

      // Also sync Lottie player if active
      if (LOTTIE_DATA[st] && lottieAnim) {{
        loadLottieState(st);
      }}
    }}

    function setEyeShape(type) {{
      const lb = document.getElementById('leftEyeBloom');
      const lc = document.getElementById('leftEyeCore');
      const ll = document.getElementById('leftEyeLaser');
      const rb = document.getElementById('rightEyeBloom');
      const rc = document.getElementById('rightEyeCore');
      const rl = document.getElementById('rightEyeLaser');

      if (type === 'arch') {{
        const ld = "M 190, 105 C 195, 88 227, 88 232, 105";
        const rd = "M 280, 105 C 285, 88 317, 88 322, 105";
        lb.setAttribute('d', ld); lc.setAttribute('d', ld); ll.setAttribute('d', ld);
        rb.setAttribute('d', rd); rc.setAttribute('d', rd); rl.setAttribute('d', rd);
        lb.setAttribute('stroke-width', '18'); lc.setAttribute('stroke-width', '9.5');
      }} else if (type === 'down_arch') {{
        const ld = "M 190, 93 C 195, 110 227, 110 232, 93";
        const rd = "M 280, 93 C 285, 110 317, 110 322, 93";
        lb.setAttribute('d', ld); lc.setAttribute('d', ld); ll.setAttribute('d', ld);
        rb.setAttribute('d', rd); rc.setAttribute('d', rd); rl.setAttribute('d', rd);
      }} else if (type === 'line') {{
        const ld = "M 190, 100 L 232, 100";
        const rd = "M 280, 100 L 322, 100";
        lb.setAttribute('d', ld); lc.setAttribute('d', ld); ll.setAttribute('d', ld);
        rb.setAttribute('d', rd); rc.setAttribute('d', rd); rl.setAttribute('d', rd);
        lb.setAttribute('stroke-width', '14'); lc.setAttribute('stroke-width', '7');
      }} else if (type === 'question') {{
        const ld = "M 200, 90 C 205, 82 217, 82 220, 92 C 220, 98 211, 102 211, 108";
        const rd = "M 290, 90 C 295, 82 307, 82 310, 92 C 310, 98 301, 102 301, 108";
        lb.setAttribute('d', ld); lc.setAttribute('d', ld); ll.setAttribute('d', ld);
        rb.setAttribute('d', rd); rc.setAttribute('d', rd); rl.setAttribute('d', rd);
      }} else if (type === 'guardian') {{
        const ld = "M 192, 95 L 230, 105";
        const rd = "M 320, 95 L 282, 105";
        lb.setAttribute('d', ld); lc.setAttribute('d', ld); ll.setAttribute('d', ld);
        rb.setAttribute('d', rd); rc.setAttribute('d', rd); rl.setAttribute('d', rd);
        lb.setAttribute('stroke-width', '16'); lc.setAttribute('stroke-width', '8.5');
      }} else if (type === 'pill') {{
        const ld = "M 211, 90 L 211, 108";
        const rd = "M 301, 90 L 301, 108";
        lb.setAttribute('d', ld); lc.setAttribute('d', ld); ll.setAttribute('d', ld);
        rb.setAttribute('d', rd); rc.setAttribute('d', rd); rl.setAttribute('d', rd);
        lb.setAttribute('stroke-width', '24'); lc.setAttribute('stroke-width', '16');
      }}
    }}

    // Vector Props Spawners
    function spawnConfetti() {{
      const colors = ['#EC4899', '#F59E0B', '#10B981', '#6366F1', '#00F0FF', '#F43F5E'];
      let html = '';
      for (let i = 0; i < 14; i++) {{
        const ang = (i / 14.0) * Math.PI * 2;
        const d = 110 + (i % 3) * 30;
        const cx = 256 + Math.cos(ang) * d;
        const cy = 200 + Math.sin(ang) * (d * 0.6);
        html += `<rect x="${{cx}}" y="${{cy}}" width="10" height="6" rx="2" fill="${{colors[i % colors.length]}}" transform="rotate(${{i * 25}}, ${{cx}}, ${{cy}})" opacity="0.9" />`;
      }}
      holoProps.innerHTML = html;
    }}

    function spawnOrbitCubes() {{
      let html = '';
      for (let i = 0; i < 3; i++) {{
        const ang = (i / 3.0) * Math.PI * 2;
        const cx = 256 + Math.cos(ang) * 115;
        const cy = 99 + Math.sin(ang) * 36;
        html += `
          <g transform="translate(${{cx}}, ${{cy}})">
            <rect x="-10" y="-10" width="20" height="20" rx="4" fill="#00F0FF" opacity="0.3" filter="url(#cyanGlow)" />
            <rect x="-7" y="-7" width="14" height="14" rx="3" fill="#00F0FF" />
            <rect x="-4" y="-4" width="5" height="5" rx="1" fill="#E0F7FF" />
          </g>
        `;
      }}
      holoProps.innerHTML = html;
    }}

    function spawn404Badge() {{
      holoProps.innerHTML = `
        <g transform="translate(256, 320)">
          <rect x="-44" y="-21" width="88" height="42" rx="10" fill="#180808" stroke="#EF4444" stroke-width="2.5" />
          <text x="0" y="7" font-family="monospace" font-size="20" font-weight="bold" fill="#EF4444" text-anchor="middle">404</text>
        </g>
      `;
    }}

    function spawnSuccessTick() {{
      holoProps.innerHTML = `
        <g transform="translate(256, 65)">
          <ellipse cx="0" cy="0" rx="38" ry="38" fill="#10B981" opacity="0.25" filter="url(#cyanGlow)" />
          <path d="M -16, 2 L -5, 14 L 18, -12" stroke="#10B981" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" fill="none" />
          <path d="M -16, 2 L -5, 14 L 18, -12" stroke="#D1FAE5" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none" />
        </g>
      `;
    }}

    function spawnZzz() {{
      holoProps.innerHTML = `
        <g fill="#00F0FF">
          <text x="295" y="60" font-family="monospace" font-size="22" font-weight="bold" opacity="0.85">Z</text>
          <text x="315" y="42" font-family="monospace" font-size="16" font-weight="bold" opacity="0.65">z</text>
          <text x="330" y="28" font-family="monospace" font-size="12" font-weight="bold" opacity="0.45">z</text>
        </g>
      `;
    }}

    function spawnReticle() {{
      holoProps.innerHTML = `
        <g transform="translate(435, 275)">
          <ellipse cx="0" cy="0" rx="20" ry="20" stroke="#00F0FF" stroke-width="2.5" fill="none" filter="url(#cyanGlow)" />
          <line x1="-12" y1="0" x2="12" y2="0" stroke="#E0F7FF" stroke-width="2" />
          <line x1="0" y1="-12" x2="0" y2="12" stroke="#E0F7FF" stroke-width="2" />
        </g>
      `;
    }}

    function spawnRadarWave() {{
      holoProps.innerHTML = `
        <g transform="translate(256, 125)">
          <ellipse cx="0" cy="25" rx="60" ry="25" fill="#00F0FF" opacity="0.12" />
          <ellipse cx="0" cy="15" rx="35" ry="13" stroke="#00F0FF" stroke-width="2.5" fill="none" />
          <ellipse cx="0" cy="28" rx="55" ry="21" stroke="#00E5FF" stroke-width="1.5" fill="none" />
          <line x1="0" y1="-5" x2="0" y2="55" stroke="#E0F7FF" stroke-width="2" />
        </g>
      `;
    }}

    function spawnGyroRings() {{
      holoProps.innerHTML = `
        <g transform="translate(256, 315)">
          <ellipse cx="0" cy="0" rx="77" ry="27" stroke="#00F0FF" stroke-width="3" fill="none" filter="url(#cyanGlow)" />
          <ellipse cx="0" cy="0" rx="67" ry="22" stroke="#00E5FF" stroke-width="2" fill="none" transform="rotate(45)" />
        </g>
      `;
    }}

    function spawnIdeaBulb() {{
      holoProps.innerHTML = `
        <g transform="translate(256, 45)">
          <ellipse cx="0" cy="-6" rx="36" ry="36" fill="#F59E0B" opacity="0.3" filter="url(#cyanGlow)" />
          <ellipse cx="0" cy="-6" rx="20" ry="20" fill="#F59E0B" />
          <ellipse cx="0" cy="-8" rx="9" ry="9" fill="#FFFFFF" />
          <rect x="-8" y="12" width="16" height="10" rx="2" fill="#78350F" />
          <line x1="0" y1="-34" x2="0" y2="-46" stroke="#FBBF24" stroke-width="3" stroke-linecap="round" />
          <line x1="-30" y1="-6" x2="-42" y2="-6" stroke="#FBBF24" stroke-width="3" stroke-linecap="round" />
          <line x1="30" y1="-6" x2="42" y2="-6" stroke="#FBBF24" stroke-width="3" stroke-linecap="round" />
        </g>
      `;
    }}

    function spawnSecurityShield() {{
      holoProps.innerHTML = `
        <g transform="translate(256, 305)">
          <path d="M 0, -55 L 48, -26 L 48, 26 L 0, 55 L -48, 26 L -48, -26 Z" fill="#00F0FF" opacity="0.18" stroke="#00F0FF" stroke-width="3.5" filter="url(#cyanGlow)" />
          <rect x="-12" y="5" width="24" height="18" rx="4" fill="#E0F7FF" />
          <ellipse cx="0" cy="-5" rx="8" ry="8" stroke="#E0F7FF" stroke-width="3.5" fill="none" />
        </g>
      `;
    }}

    function togglePasswordPeek() {{
      isPeekRevealed = !isPeekRevealed;
      const pwd = document.getElementById('passwordInput');
      pwd.type = isPeekRevealed ? 'text' : 'password';
      if (isPeekRevealed) {{
        mascotSpeech.innerText = "Oh ! Je jette un œil discret entre mes doigts ! 👀";
      }} else {{
        mascotSpeech.innerText = "Je ferme bien les doigts, je ne regarde rien ! 🙈";
      }}
    }}

    function onMascotClick() {{
      triggerNaturalBlink();
      mascotSpeech.innerText = "Bip boop ! Rigueur maximale : 100% vectoriel et 0 pixelisation ! ⚡";
    }}

    function onAppType(e) {{
      targetEyeX = Math.max(-14, Math.min(14, (e.target.value.length % 10 - 5) * 3));
      mascotSpeech.innerText = `Saisie en cours : "${{e.target.value.slice(-15)}}"... Je valide chaque caractère ! ✍️`;
    }}

    function onAppSubmit(success) {{
      if (success) {{
        switchState('02_celebrating');
      }} else {{
        switchState('04_error_404');
      }}
    }}

    // 5. View Mode Switcher (Rig vs Lottie Player vs Compare)
    function toggleViewMode(mode) {{
      viewMode = mode;
      document.getElementById('interactiveContainer').classList.toggle('hidden', mode !== 'interactive');
      document.getElementById('lottieContainer').classList.toggle('hidden', mode !== 'lottie');
      document.getElementById('compareContainer').classList.toggle('hidden', mode !== 'compare');

      document.getElementById('btnInteractive').className = mode === 'interactive' 
        ? 'px-3 py-1.5 rounded-lg text-xs font-semibold bg-cyan-500 text-black shadow-lg shadow-cyan-500/20 transition'
        : 'px-3 py-1.5 rounded-lg text-xs font-semibold bg-[var(--card)] hover:bg-[var(--card-hover)] text-[var(--muted)] border border-[var(--border)] transition';
      
      document.getElementById('btnLottie').className = mode === 'lottie' 
        ? 'px-3 py-1.5 rounded-lg text-xs font-semibold bg-cyan-500 text-black shadow-lg shadow-cyan-500/20 transition'
        : 'px-3 py-1.5 rounded-lg text-xs font-semibold bg-[var(--card)] hover:bg-[var(--card-hover)] text-[var(--muted)] border border-[var(--border)] transition';

      document.getElementById('btnCompare').className = mode === 'compare' 
        ? 'px-3 py-1.5 rounded-lg text-xs font-semibold bg-cyan-500 text-black shadow-lg shadow-cyan-500/20 transition'
        : 'px-3 py-1.5 rounded-lg text-xs font-semibold bg-[var(--card)] hover:bg-[var(--card-hover)] text-[var(--muted)] border border-[var(--border)] transition';

      if (mode === 'lottie' && !lottieAnim) {{
        initLottiePlayer();
      }}
      if (mode === 'compare' && !compareAnim) {{
        initComparePlayer();
      }}
    }}

    function initLottiePlayer() {{
      const container = document.getElementById('lottiePlayerBox');
      container.innerHTML = '';
      lottieAnim = lottie.loadAnimation({{
        container: container,
        renderer: 'svg',
        loop: true,
        autoplay: true,
        animationData: LOTTIE_DATA[currentState] || LOTTIE_DATA['00_idle']
      }});

      lottieAnim.addEventListener('enterFrame', (e) => {{
        const slider = document.getElementById('lottieTimeline');
        const text = document.getElementById('lottieFrameText');
        const cur = Math.round(e.currentTime);
        slider.value = cur;
        text.innerText = `${{cur}} / 120`;
      }});
    }}

    function initComparePlayer() {{
      const container = document.getElementById('compareLottieBox');
      container.innerHTML = '';
      compareAnim = lottie.loadAnimation({{
        container: container,
        renderer: 'svg',
        loop: true,
        autoplay: true,
        animationData: LOTTIE_DATA['00_idle']
      }});
    }}

    function loadLottieState(st) {{
      if (lottieAnim && LOTTIE_DATA[st]) {{
        lottieAnim.destroy();
        const container = document.getElementById('lottiePlayerBox');
        container.innerHTML = '';
        lottieAnim = lottie.loadAnimation({{
          container: container,
          renderer: 'svg',
          loop: true,
          autoplay: true,
          animationData: LOTTIE_DATA[st]
        }});
      }}
    }}

    function toggleLottiePlay() {{
      if (!lottieAnim) return;
      const btn = document.getElementById('lottiePlayBtn');
      if (lottieAnim.isPaused) {{
        lottieAnim.play();
        btn.innerText = 'Pause';
      }} else {{
        lottieAnim.pause();
        btn.innerText = 'Play';
      }}
    }}

    function onLottieSeek(e) {{
      if (!lottieAnim) return;
      lottieAnim.goToAndStop(parseInt(e.target.value), true);
    }}

    function onLottieSpeedChange(e) {{
      if (!lottieAnim) return;
      lottieAnim.setSpeed(parseFloat(e.target.value));
    }}
  </script>
</body>
</html>'''

out_path = '/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68/aituko_vector_interactive_demo.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f'Successfully built interactive demo artifact: {out_path} ({os.path.getsize(out_path)/1024:.1f} KB)')
