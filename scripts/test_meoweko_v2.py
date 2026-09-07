import re, sys
sys.path.append('scripts')
from benchmark_meoweko_fidelity import benchmark_svg
from build_flawless_meoweko_idle import (
    BODY_SILHOUETTE_PTS, TAIL_PTS, FLANK_L_PTS, FLANK_R_PTS,
    WHITE_COAT_PTS, EAR_R_PTS, points_to_svg_cubic_spline
)

# Symmetrical Left Ear points:
ear_l_pts = [[round(543.0 - p[0], 1), p[1]] for p in reversed(EAR_R_PTS)]

spline_body = points_to_svg_cubic_spline(BODY_SILHOUETTE_PTS)
spline_tail = points_to_svg_cubic_spline(TAIL_PTS)
spline_flank_l = points_to_svg_cubic_spline(FLANK_L_PTS)
spline_flank_r = points_to_svg_cubic_spline(FLANK_R_PTS)
spline_white = points_to_svg_cubic_spline(WHITE_COAT_PTS)
spline_ear_l = points_to_svg_cubic_spline(ear_l_pts)
spline_ear_r = points_to_svg_cubic_spline(EAR_R_PTS)

def build_svg(p):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <!-- 1. TAIL GRADIENT -->
    <linearGradient id="gingerTail" x1="15%" y1="25%" x2="85%" y2="75%">
      <stop offset="0%" stop-color="{p['tail_0']}" />
      <stop offset="40%" stop-color="{p['tail_1']}" />
      <stop offset="75%" stop-color="{p['tail_2']}" />
      <stop offset="100%" stop-color="{p['tail_3']}" />
    </linearGradient>

    <!-- 2. GINGER BODY GRADIENT -->
    <linearGradient id="gingerBody" x1="25%" y1="15%" x2="75%" y2="85%">
      <stop offset="0%" stop-color="{p['body_0']}" />
      <stop offset="30%" stop-color="{p['body_1']}" />
      <stop offset="65%" stop-color="{p['body_2']}" />
      <stop offset="100%" stop-color="{p['body_3']}" />
    </linearGradient>

    <!-- 3. WHITE COAT PORCELAIN GRADIENT -->
    <radialGradient id="whiteCoatGrad" cx="{p['chest_cx']}" cy="{p['chest_cy']}" r="{p['chest_r']}">
      <stop offset="0%" stop-color="{p['chest_0']}" />
      <stop offset="35%" stop-color="{p['chest_1']}" />
      <stop offset="70%" stop-color="{p['chest_2']}" />
      <stop offset="100%" stop-color="{p['chest_3']}" />
    </radialGradient>

    <!-- 4. INNER EAR CAVITIES -->
    <radialGradient id="earCavityL" cx="40%" cy="35%" r="65%">
      <stop offset="0%" stop-color="{p['earL_0']}" />
      <stop offset="45%" stop-color="{p['earL_1']}" />
      <stop offset="80%" stop-color="{p['earL_2']}" />
      <stop offset="100%" stop-color="{p['earL_3']}" />
    </radialGradient>

    <radialGradient id="earCavityR" cx="60%" cy="35%" r="65%">
      <stop offset="0%" stop-color="{p['earR_0']}" />
      <stop offset="45%" stop-color="{p['earR_1']}" />
      <stop offset="80%" stop-color="{p['earR_2']}" />
      <stop offset="100%" stop-color="{p['earR_3']}" />
    </radialGradient>

    <!-- 5. FLANK SHADING -->
    <radialGradient id="flankL" cx="30%" cy="50%" r="70%">
      <stop offset="0%" stop-color="{p['flankL_0']}" />
      <stop offset="50%" stop-color="{p['flankL_1']}" />
      <stop offset="100%" stop-color="{p['flankL_2']}" />
    </radialGradient>

    <radialGradient id="flankR" cx="70%" cy="50%" r="70%">
      <stop offset="0%" stop-color="{p['flankR_0']}" />
      <stop offset="50%" stop-color="{p['flankR_1']}" />
      <stop offset="100%" stop-color="{p['flankR_2']}" />
    </radialGradient>

    <!-- 6. VOLUMETRIC LEGS GRADIENTS -->
    <linearGradient id="legLeftGrad" x1="228" y1="430" x2="271" y2="430" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="{p['legL_0']}" />
      <stop offset="30%" stop-color="{p['legL_1']}" />
      <stop offset="65%" stop-color="{p['legL_2']}" />
      <stop offset="88%" stop-color="{p['legL_3']}" />
      <stop offset="100%" stop-color="{p['legL_4']}" />
    </linearGradient>

    <linearGradient id="legRightGrad" x1="271" y1="430" x2="314" y2="430" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="{p['legR_0']}" />
      <stop offset="15%" stop-color="{p['legR_1']}" />
      <stop offset="50%" stop-color="{p['legR_2']}" />
      <stop offset="85%" stop-color="{p['legR_3']}" />
      <stop offset="100%" stop-color="{p['legR_4']}" />
    </linearGradient>

    <!-- Crease -->
    <linearGradient id="creaseGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{p['crease_0']}" stop-opacity="0.4" />
      <stop offset="40%" stop-color="{p['crease_1']}" stop-opacity="0.85" />
      <stop offset="85%" stop-color="{p['crease_2']}" stop-opacity="0.95" />
      <stop offset="100%" stop-color="{p['crease_3']}" stop-opacity="1.0" />
    </linearGradient>

    <!-- 7. TOE PADS -->
    <linearGradient id="toeLGrad" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="{p['toeL_0']}" />
      <stop offset="60%" stop-color="{p['toeL_1']}" />
      <stop offset="100%" stop-color="{p['toeL_2']}" />
    </linearGradient>
    <linearGradient id="toeRGrad" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="{p['toeR_0']}" />
      <stop offset="60%" stop-color="{p['toeR_1']}" />
      <stop offset="100%" stop-color="{p['toeR_2']}" />
    </linearGradient>

    <!-- 8. GLASSY AMBER IRIS -->
    <radialGradient id="amberIrisL" cx="42%" cy="38%" r="60%">
      <stop offset="0%" stop-color="{p['iris_0']}" />
      <stop offset="40%" stop-color="{p['iris_1']}" />
      <stop offset="75%" stop-color="{p['iris_2']}" />
      <stop offset="100%" stop-color="{p['iris_3']}" />
    </radialGradient>

    <radialGradient id="amberIrisR" cx="58%" cy="38%" r="60%">
      <stop offset="0%" stop-color="{p['iris_0']}" />
      <stop offset="40%" stop-color="{p['iris_1']}" />
      <stop offset="75%" stop-color="{p['iris_2']}" />
      <stop offset="100%" stop-color="{p['iris_3']}" />
    </radialGradient>

    <!-- 9. NOSE -->
    <linearGradient id="noseGrad" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="{p['nose_0']}" />
      <stop offset="100%" stop-color="{p['nose_1']}" />
    </linearGradient>

    <!-- Cheeks diffuse blend overlays -->
    <radialGradient id="cheekBlendL" cx="20%" cy="50%" r="70%">
      <stop offset="0%" stop-color="{p['cheekL_col']}" stop-opacity="0.90" />
      <stop offset="40%" stop-color="{p['cheekL_col']}" stop-opacity="0.65" />
      <stop offset="75%" stop-color="{p['cheekL_col']}" stop-opacity="0.25" />
      <stop offset="100%" stop-color="{p['cheekL_col']}" stop-opacity="0.0" />
    </radialGradient>

    <radialGradient id="cheekBlendR" cx="80%" cy="50%" r="70%">
      <stop offset="0%" stop-color="{p['cheekR_col']}" stop-opacity="0.90" />
      <stop offset="40%" stop-color="{p['cheekR_col']}" stop-opacity="0.65" />
      <stop offset="75%" stop-color="{p['cheekR_col']}" stop-opacity="0.25" />
      <stop offset="100%" stop-color="{p['cheekR_col']}" stop-opacity="0.0" />
    </radialGradient>

    <!-- Keyframe Animations -->
    <style>
      @keyframes breathe_pos {{
        0%, 50%, 100% {{ transform: translateY(0px); }}
        25% {{ transform: translateY(2.0px); }}
        75% {{ transform: translateY(-2.0px); }}
      }}
      @keyframes breathe_scale {{
        0%, 50%, 100% {{ transform: scale(1.0, 1.0); }}
        25% {{ transform: scale(1.008, 0.992); }}
        75% {{ transform: scale(0.992, 1.008); }}
      }}
      @keyframes tail_sway {{
        0%, 100% {{ transform: rotate(-3.5deg); }}
        50% {{ transform: rotate(3.5deg); }}
      }}
      @keyframes ear_twitch {{
        0%, 38%, 52%, 100% {{ transform: rotate(0deg); }}
        42% {{ transform: rotate(-2.2deg); }}
        47% {{ transform: rotate(1.8deg); }}
      }}
      @keyframes eye_blink {{
        0%, 15%, 26%, 60%, 75%, 100% {{ transform: scaleY(1); }}
        18%, 23%, 68%, 73% {{ transform: scaleY(0.08); }}
      }}

      .anim-torso {{
        transform-box: view-box;
        transform-origin: 271.5px 360px;
        animation: breathe_pos 4s ease-in-out infinite, breathe_scale 4s ease-in-out infinite;
      }}
      .anim-head {{
        transform-box: view-box;
        transform-origin: 271.5px 180px;
        animation: ear_twitch 4s ease-in-out infinite;
      }}
      .anim-tail {{
        transform-box: view-box;
        transform-origin: 185px 445px;
        animation: tail_sway 4s ease-in-out infinite;
      }}
      .anim-eyes {{
        transform-box: view-box;
        transform-origin: 271.5px 169px;
        animation: eye_blink 4s cubic-bezier(0.45, 0.05, 0.55, 0.95) infinite;
      }}
    </style>
  </defs>

  <!-- 1. TAIL -->
  <g class="anim-tail">
    <path d="{spline_tail}" fill="url(#gingerTail)" stroke="#6C2A08" stroke-width="0.7" />
  </g>

  <!-- 2. GINGER SILHOUETTE SHELL -->
  <g class="anim-torso">
    <path d="{spline_body}" fill="url(#gingerBody)" stroke="#78340E" stroke-width="0.7" />

    <!-- 3. FLANKS -->
    <path d="{spline_flank_l}" fill="url(#flankL)" opacity="0.95" />
    <path d="{spline_flank_r}" fill="url(#flankR)" opacity="0.95" />

    <!-- 4. INNER EARS & TABBY STRIPES -->
    <g class="anim-head">
      <path d="{spline_ear_l}" fill="url(#earCavityL)" stroke="#924032" stroke-width="0.7" />
      <path d="{spline_ear_r}" fill="url(#earCavityR)" stroke="#924032" stroke-width="0.7" />

      <!-- Forehead Tabby Stripes -->
      <path d="M 271.5 73 C 274.5 73, 275.5 82, 275 95 C 274.5 106, 273 115, 271.5 115 C 270 115, 268.5 106, 268 95 C 267.5 82, 268.5 73, 271.5 73 Z" fill="{p['stripe_col']}" opacity="0.80" />
      <path d="M 244 82 C 247 81, 250 86, 252 98 C 253.5 108, 253 116, 251 117 C 249 118, 246 113, 244 102 C 242 92, 242 83, 244 82 Z" fill="{p['stripe_col']}" opacity="0.75" />
      <path d="M 299 82 C 301 83, 301 92, 299 102 C 297 113, 294 118, 292 117 C 290 116, 289.5 108, 291 98 C 293 86, 297 81, 299 82 Z" fill="{p['stripe_col']}" opacity="0.75" />
    </g>

    <!-- 5. WHITE PORCELAIN FUR COAT (Seamless with stroke=none) -->
    <path d="{spline_white}" fill="url(#whiteCoatGrad)" stroke="none" />

    <!-- Cheeks Ginger Blend Overlays (Diffuse blending) -->
    <path d="M 158 170 C 156 195, 166 230, 185 245 C 205 240, 218 215, 218 190 C 218 168, 185 158, 158 170 Z" fill="url(#cheekBlendL)" />
    <path d="M 384 170 C 386 195, 376 230, 357 245 C 337 240, 324 215, 324 190 C 324 168, 357 158, 384 170 Z" fill="url(#cheekBlendR)" />

    <!-- 6. VOLUMETRIC FRONT LEGS -->
    <path d="M 235 375 C 228 400, 222 435, 228 472 L 271 472 L 271 375 Z" fill="url(#legLeftGrad)" opacity="0.95" />
    <path d="M 271 375 L 271 472 L 314 472 C 320 435, 314 400, 307 375 Z" fill="url(#legRightGrad)" opacity="0.95" />
    <!-- Ambient Occlusion Crease -->
    <path d="M 270.2 380 C 270.5 410, 269.0 450, 267.0 488 L 275.0 488 C 273.0 450, 272.5 410, 272.8 380 Z" fill="url(#creaseGrad)" />

    <!-- 7. GROUNDED 3D FRONT & REAR PAWS -->
    <g id="leftPawToes">
      <path d="M 232 490 C 232 468, 244 466, 245 470 L 245 490 Z" fill="url(#toeLGrad)" stroke="#B6A496" stroke-width="0.5" />
      <path d="M 244 490 C 244 464, 258 462, 258 470 L 258 490 Z" fill="url(#toeLGrad)" stroke="#B6A496" stroke-width="0.5" />
      <path d="M 257 490 C 257 465, 270 465, 270 472 L 270 490 Z" fill="url(#toeLGrad)" stroke="#B6A496" stroke-width="0.5" />
      <path d="M 244.5 470 L 244.5 490" stroke="#7A4E3C" stroke-width="1.2" stroke-linecap="round" />
      <path d="M 257.5 470 L 257.5 490" stroke="#7A4E3C" stroke-width="1.2" stroke-linecap="round" />
    </g>

    <g id="rightPawToes">
      <path d="M 273 490 C 273 465, 286 465, 286 472 L 286 490 Z" fill="url(#toeRGrad)" stroke="#AE9E90" stroke-width="0.5" />
      <path d="M 285 490 C 285 464, 299 462, 299 470 L 299 490 Z" fill="url(#toeRGrad)" stroke="#AE9E90" stroke-width="0.5" />
      <path d="M 298 490 C 298 468, 310 466, 310 470 L 310 490 Z" fill="url(#toeRGrad)" stroke="#AE9E90" stroke-width="0.5" />
      <path d="M 285.5 470 L 285.5 490" stroke="#724838" stroke-width="1.2" stroke-linecap="round" />
      <path d="M 298.5 470 L 298.5 490" stroke="#724838" stroke-width="1.2" stroke-linecap="round" />
    </g>

    <path d="M 207 490 C 205 476, 216 470, 226 472 C 230 473, 232 480, 233 490 Z" fill="url(#toeLGrad)" stroke="#B6A496" stroke-width="0.5" />
    <path d="M 336 490 C 338 476, 327 470, 317 472 C 313 473, 311 480, 310 490 Z" fill="url(#toeRGrad)" stroke="#AE9E90" stroke-width="0.5" />

    <!-- 8. GLASSY AMBER ORB EYES -->
    <g class="anim-eyes">
      <g id="eyeL" transform="translate(224.2, 168.5)">
        <ellipse cx="0" cy="0" rx="23.5" ry="22.5" fill="#1A1006" />
        <ellipse cx="0" cy="0" rx="22.0" ry="21.0" fill="url(#amberIrisL)" />
        <ellipse cx="-1.0" cy="1.0" rx="14.0" ry="14.5" fill="#201812" />
        <circle cx="9.1" cy="-6.7" r="4.5" fill="#FFFFFF" opacity="0.95" />
        <circle cx="9.1" cy="-6.7" r="6.5" fill="#FFFFFF" opacity="0.35" />
        <circle cx="-5.5" cy="8.5" r="2.2" fill="#FFD670" opacity="0.45" />
      </g>

      <g id="eyeR" transform="translate(318.4, 169.6)">
        <ellipse cx="0" cy="0" rx="23.5" ry="22.5" fill="#1A1006" />
        <ellipse cx="0" cy="0" rx="22.0" ry="21.0" fill="url(#amberIrisR)" />
        <ellipse cx="-1.0" cy="1.0" rx="14.0" ry="14.5" fill="#201812" />
        <circle cx="6.6" cy="-6.9" r="4.5" fill="#FFFFFF" opacity="0.95" />
        <circle cx="6.6" cy="-6.9" r="6.5" fill="#FFFFFF" opacity="0.35" />
        <circle cx="-5.5" cy="8.5" r="2.2" fill="#FFD670" opacity="0.45" />
      </g>
    </g>

    <!-- 9. NOSE & MOUTH ω -->
    <path d="M 263 195 C 266 193, 277 193, 280 195 C 284 199, 277 205, 271.6 205 C 266 205, 259 199, 263 195 Z" fill="url(#noseGrad)" stroke="#A84838" stroke-width="0.7" />
    <ellipse cx="271.6" cy="196.5" rx="3.0" ry="1.2" fill="#FFFFFF" opacity="0.45" />
    <path d="M 271.5 205 L 271.5 214" stroke="#68483B" stroke-width="1.3" stroke-linecap="round" fill="none" />
    <path d="M 252 221 C 257 225, 266 223, 271.5 214 C 277 223, 286 225, 291 221" stroke="#68483B" stroke-width="1.3" stroke-linecap="round" fill="none" />
    <ellipse cx="271.5" cy="232" rx="10" ry="4" fill="#C4B0A0" opacity="0.40" />
  </g>
</svg>"""
    return svg

params = {
    'tail_0': '#B86B3E', 'tail_1': '#9A5026', 'tail_2': '#783614', 'tail_3': '#54220A',
    'body_0': '#D69368', 'body_1': '#C77E50', 'body_2': '#A86236', 'body_3': '#84421C',
    'chest_cx': '58%', 'chest_cy': '34%', 'chest_r': '65%',
    'chest_0': '#ECE1D6', 'chest_1': '#DFD2C6', 'chest_2': '#C8B8AB', 'chest_3': '#AFA094',
    'earL_0': '#D28876', 'earL_1': '#B66958', 'earL_2': '#924C3C', 'earL_3': '#6E3224',
    'earR_0': '#E09684', 'earR_1': '#C47664', 'earR_2': '#A05444', 'earR_3': '#783628',
    'flankL_0': '#BC6A38', 'flankL_1': '#9E4E20', 'flankL_2': '#743010',
    'flankR_0': '#E09652', 'flankR_1': '#CF803A', 'flankR_2': '#A6541E',
    'legL_0': '#BAA898', 'legL_1': '#DFD1C4', 'legL_2': '#E8DDD2', 'legL_3': '#C8B6A6', 'legL_4': '#88563E',
    'legR_0': '#88563E', 'legR_1': '#BFAFA0', 'legR_2': '#DACCC0', 'legR_3': '#C8B8AB', 'legR_4': '#A69486',
    'crease_0': '#7D4E3C', 'crease_1': '#583222', 'crease_2': '#321A10', 'crease_3': '#1A0B06',
    'toeL_0': '#DACDC0', 'toeL_1': '#C4B4A6', 'toeL_2': '#A29080',
    'toeR_0': '#D4C4B6', 'toeR_1': '#BFADA0', 'toeR_2': '#9C8676',
    'iris_0': '#FFE06E', 'iris_1': '#EAA626', 'iris_2': '#9C5A0C', 'iris_3': '#2D1602',
    'nose_0': '#E49284', 'nose_1': '#C26252',
    'stripe_col': '#98400C',
    'cheekL_col': '#A85222',
    'cheekR_col': '#EA9240'
}

svg = build_svg(params)
with open('scratch/test_meoweko_v2.svg', 'w') as f:
    f.write(svg)

res = benchmark_svg('scratch/test_meoweko_v2.svg')
print("MEOWEKO V2 BENCHMARK:")
for k, v in res.items():
    print(f"  {k}: {v}")
