import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Master Rig SVG Template (AItuko Pure Vector Model - STRICTLY NO HANDS)
def get_rig_svg(svg_id, shadow_id, pods_id, torso_id, head_id, eyes_id, larm_id, rarm_id):
    return f'''<svg id="{svg_id}" viewBox="0 0 512 512" class="w-full h-full drop-shadow-md overflow-visible">
            <defs>
              <linearGradient id="{svg_id}_porcelainGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#FFFFFF" />
                <stop offset="35%" stop-color="#F8FAFC" />
                <stop offset="70%" stop-color="#E2E8F0" />
                <stop offset="100%" stop-color="#CBD5E1" />
              </linearGradient>

              <radialGradient id="{svg_id}_headDomeGrad" cx="38%" cy="25%" r="70%">
                <stop offset="0%" stop-color="#FFFFFF" />
                <stop offset="45%" stop-color="#F8FAFC" />
                <stop offset="80%" stop-color="#E2E8F0" />
                <stop offset="100%" stop-color="#CBD5E1" />
              </radialGradient>

              <linearGradient id="{svg_id}_neckGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#CBD5E1" />
                <stop offset="25%" stop-color="#F8FAFC" />
                <stop offset="50%" stop-color="#FFFFFF" />
                <stop offset="80%" stop-color="#E2E8F0" />
                <stop offset="100%" stop-color="#CBD5E1" />
              </linearGradient>

              <linearGradient id="{svg_id}_podGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#CBD5E1" />
                <stop offset="30%" stop-color="#FFFFFF" />
                <stop offset="70%" stop-color="#F8FAFC" />
                <stop offset="100%" stop-color="#CBD5E1" />
              </linearGradient>

              <radialGradient id="{svg_id}_footGrad" cx="40%" cy="30%" r="65%">
                <stop offset="0%" stop-color="#FFFFFF" />
                <stop offset="55%" stop-color="#F1F5F9" />
                <stop offset="100%" stop-color="#CBD5E1" />
              </radialGradient>

              <radialGradient id="{svg_id}_visorGlassGrad" cx="50%" cy="35%" r="65%">
                <stop offset="0%" stop-color="#181B26" />
                <stop offset="60%" stop-color="#10121A" />
                <stop offset="100%" stop-color="#090A0F" />
              </radialGradient>

              <linearGradient id="{svg_id}_visorArcReflection" x1="20%" y1="0%" x2="80%" y2="100%">
                <stop offset="0%" stop-color="#94A3B8" stop-opacity="0.45" />
                <stop offset="40%" stop-color="#64748B" stop-opacity="0.25" />
                <stop offset="100%" stop-color="#334155" stop-opacity="0.0" />
              </linearGradient>

              <linearGradient id="{svg_id}_specularStreak" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0" />
                <stop offset="50%" stop-color="#FFFFFF" stop-opacity="0.95" />
                <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0" />
              </linearGradient>

              <radialGradient id="{svg_id}_shadowGrad" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stop-color="#0F172A" stop-opacity="0.32" />
                <stop offset="50%" stop-color="#0F172A" stop-opacity="0.14" />
                <stop offset="100%" stop-color="#0F172A" stop-opacity="0" />
              </radialGradient>

              <filter id="{svg_id}_cyanGlow" x="-50%" y="-50%" width="200%" height="200%">
                <feGaussianBlur in="SourceGraphic" stdDeviation="5" result="blur1" />
                <feGaussianBlur in="SourceGraphic" stdDeviation="12" result="blur2" />
                <feMerge>
                  <feMergeNode in="blur2" />
                  <feMergeNode in="blur1" />
                  <feMergeNode in="SourceGraphic" />
                </feMerge>
              </filter>
            </defs>

            <!-- 1. Ombre de sustentation dynamique (au sol) -->
            <ellipse id="{shadow_id}" cx="256" cy="468" rx="90" ry="14" fill="url(#{svg_id}_shadowGrad)" class="aituko-shadow-anim" />

            <!-- 2. Pods de sustentation (petits pieds flottants sous le torse) -->
            <g id="{pods_id}" class="aituko-pods-anim">
              <g transform="translate(228, 412) rotate(-10)">
                <rect x="-19" y="-23" width="38" height="46" rx="19" fill="#CBD5E1" />
                <rect x="-17" y="-22" width="34" height="44" rx="17" fill="url(#{svg_id}_footGrad)" />
                <ellipse cx="-3" cy="-12" rx="9" ry="4" fill="#FFFFFF" opacity="0.85" />
              </g>
              <g transform="translate(284, 412) rotate(10)">
                <rect x="-19" y="-23" width="38" height="46" rx="19" fill="#CBD5E1" />
                <rect x="-17" y="-22" width="34" height="44" rx="17" fill="url(#{svg_id}_footGrad)" />
                <ellipse cx="-3" cy="-12" rx="9" ry="4" fill="#FFFFFF" opacity="0.85" />
              </g>
            </g>

            <!-- 3. Cou svelte (jonction tête-torse) -->
            <g id="{svg_id}_neck" class="aituko-neck-anim">
              <rect x="238" y="192" width="36" height="22" rx="10" fill="#CBD5E1" />
              <rect x="240" y="193" width="32" height="20" rx="9" fill="url(#{svg_id}_neckGrad)" />
              <ellipse cx="256" cy="193" rx="16" ry="3" fill="#0F172A" opacity="0.25" />
            </g>

            <!-- 4. Torse capsule lisse porcelaine (124x176 à Y=298) -->
            <g id="{torso_id}" class="aituko-torso-anim">
              <rect x="192" y="208" width="128" height="180" rx="64" fill="#CBD5E1" />
              <rect x="194" y="210" width="124" height="176" rx="62" fill="url(#{svg_id}_porcelainGrad)" />
              <rect x="195" y="222" width="38" height="152" rx="19" fill="#E2E8F0" opacity="0.45" />
              <rect x="300" y="232" width="12" height="124" rx="6" fill="url(#{svg_id}_specularStreak)" />
              <ellipse cx="256" cy="226" rx="36" ry="8" fill="#FFFFFF" opacity="0.6" />
              <ellipse cx="256" cy="210" rx="30" ry="6" fill="#0F172A" opacity="0.22" />
            </g>

            <!-- 5. Tête oblate porcelaine avec visière sombre et yeux cyan -->
            <g id="{head_id}" class="aituko-head-anim">
              <rect x="136" y="42" width="240" height="168" rx="74" fill="#CBD5E1" />
              <rect x="138" y="44" width="236" height="164" rx="72" fill="url(#{svg_id}_headDomeGrad)" />
              <ellipse cx="242" cy="60" rx="55" ry="12" fill="#FFFFFF" opacity="0.90" />
              <ellipse cx="162" cy="118" rx="12" ry="26" fill="#E2E8F0" opacity="0.4" />
              <ellipse cx="346" cy="100" rx="8" ry="22" transform="rotate(16 346 100)" fill="#FFFFFF" opacity="0.65" />
              <ellipse cx="256" cy="204" rx="46" ry="6" fill="#CBD5E1" opacity="0.5" />

              <!-- Visière en verre noir poli concave -->
              <rect x="160" y="61" width="192" height="130" rx="58" fill="#090A0F" />
              <rect x="162" y="63" width="188" height="126" rx="56" fill="url(#{svg_id}_visorGlassGrad)" stroke="#1F2433" stroke-width="1.5" />
              <path d="M 182, 102 C 205, 78 245, 72 292, 78 C 272, 82 222, 88 198, 112 Z" fill="url(#{svg_id}_visorArcReflection)" />
              <ellipse cx="256" cy="79" rx="42" ry="6" fill="#FFFFFF" opacity="0.20" />

              <!-- Yeux Cyan Électriques dynamiques (^ ^) -->
              <g id="{eyes_id}" class="aituko-eyes-blink aituko-eyes-glow transition-transform duration-75">
                <g id="{eyes_id}_arches">
                  <path d="M 194, 131 C 199, 116 225, 116 230, 131" stroke="#00F0FF" stroke-width="16" stroke-linecap="round" fill="none" opacity="0.4" filter="url(#{svg_id}_cyanGlow)" />
                  <path d="M 194, 131 C 199, 116 225, 116 230, 131" stroke="#00F0FF" stroke-width="8.5" stroke-linecap="round" fill="none" />
                  <path d="M 194, 131 C 199, 116 225, 116 230, 131" stroke="#E0F7FF" stroke-width="3.2" stroke-linecap="round" fill="none" />

                  <path d="M 278, 131 C 283, 116 309, 116 314, 131" stroke="#00F0FF" stroke-width="16" stroke-linecap="round" fill="none" opacity="0.4" filter="url(#{svg_id}_cyanGlow)" />
                  <path d="M 278, 131 C 283, 116 309, 116 314, 131" stroke="#00F0FF" stroke-width="8.5" stroke-linecap="round" fill="none" />
                  <path d="M 278, 131 C 283, 116 309, 116 314, 131" stroke="#E0F7FF" stroke-width="3.2" stroke-linecap="round" fill="none" />
                </g>
              </g>
            </g>

            <!-- 6. Pods latéraux flottants (ailerons/propulseurs — STRICTEMENT SANS MAINS) -->
            <g id="{larm_id}" class="aituko-left-arm-anim transition-all duration-300">
              <rect x="-19" y="-56" width="38" height="112" rx="19" fill="#CBD5E1" />
              <rect x="-17" y="-54" width="34" height="108" rx="17" fill="url(#{svg_id}_podGrad)" />
              <rect x="-12" y="-42" width="6" height="74" rx="3" fill="url(#{svg_id}_specularStreak)" />
              <rect x="6" y="-38" width="9" height="80" rx="4.5" fill="#CBD5E1" opacity="0.35" />
            </g>
            <g id="{rarm_id}" class="aituko-right-arm-anim transition-all duration-300">
              <rect x="-19" y="-56" width="38" height="112" rx="19" fill="#CBD5E1" />
              <rect x="-17" y="-54" width="34" height="108" rx="17" fill="url(#{svg_id}_podGrad)" />
              <rect x="6" y="-42" width="6" height="74" rx="3" fill="url(#{svg_id}_specularStreak)" />
              <rect x="-15" y="-38" width="9" height="80" rx="4.5" fill="#CBD5E1" opacity="0.35" />
            </g>
          </svg>'''

# Replace demoAitukoSvg
demo_svg_pattern = r'<svg id="demoAitukoSvg".*?</svg>'
new_demo_svg = get_rig_svg("demoAitukoSvg", "demoShadow", "demoPods", "demoAitukoFloat", "demoHeadGroup", "demoEyesGroup", "demoLeftHand", "demoRightHand")
match_demo = re.search(demo_svg_pattern, content, re.DOTALL)
if match_demo:
    content = content[:match_demo.start()] + new_demo_svg + content[match_demo.end():]
    print("✅ demoAitukoSvg updated in index.html")
else:
    print("⚠️ demoAitukoSvg pattern not found")

# Replace interactiveAitukoSvg
inter_svg_pattern = r'<svg id="aitukoInteractiveSvg".*?</svg>'
new_inter_svg = get_rig_svg("aitukoInteractiveSvg", "interactiveShadow", "interactivePods", "interactiveTorso", "interactiveHeadGroup", "interactiveEyesGroup", "interactiveLeftHand", "interactiveRightHand")
match_inter = re.search(inter_svg_pattern, content, re.DOTALL)
if match_inter:
    content = content[:match_inter.start()] + new_inter_svg + content[match_inter.end():]
    print("✅ aitukoInteractiveSvg updated in index.html")
else:
    print("⚠️ aitukoInteractiveSvg pattern not found")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
