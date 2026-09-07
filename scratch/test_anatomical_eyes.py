import sys
sys.path.append(".")
from scripts.benchmark_owluko_fidelity import render_svg, evaluate_fidelity

with open("scratch/owluko_body_path_131.txt", "r") as f:
    body_d = f.read().strip()

def build_svg_anatomical_eyes():
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" style="background: transparent;">
  <defs>
    <!-- Master Body Gradient -->
    <linearGradient id="bodyGrad" x1="28%" y1="5%" x2="68%" y2="95%">
      <stop offset="0%" stop-color="#E8E0D8" />
      <stop offset="16%" stop-color="#DDD5CD" />
      <stop offset="38%" stop-color="#D4C9BD" />
      <stop offset="60%" stop-color="#BAABA0" />
      <stop offset="82%" stop-color="#9E8C7F" />
      <stop offset="100%" stop-color="#685648" />
    </linearGradient>

    <!-- Cranial Highlight -->
    <radialGradient id="cranialHl" cx="38%" cy="16%" r="35%">
      <stop offset="0%" stop-color="#FFF2E6" stop-opacity="0.50" />
      <stop offset="50%" stop-color="#F5EFEA" stop-opacity="0.18" />
      <stop offset="100%" stop-color="#DED6CE" stop-opacity="0" />
    </radialGradient>

    <!-- Chest Soft Illumination -->
    <radialGradient id="chestHl" cx="44%" cy="48%" r="44%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.18" />
      <stop offset="50%" stop-color="#ECE5DC" stop-opacity="0.06" />
      <stop offset="100%" stop-color="#DED6CE" stop-opacity="0" />
    </radialGradient>

    <!-- Wing Shadow -->
    <linearGradient id="rWingShadow" x1="10%" y1="20%" x2="90%" y2="80%">
      <stop offset="0%" stop-color="#C5B8AC" stop-opacity="0.15" />
      <stop offset="45%" stop-color="#8E7E70" stop-opacity="0.42" />
      <stop offset="100%" stop-color="#554436" stop-opacity="0.65" />
    </linearGradient>

    <!-- Left Flank Shading -->
    <linearGradient id="lFlankShadow" x1="50%" y1="35%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#B8A999" stop-opacity="0" />
      <stop offset="55%" stop-color="#8E7D6D" stop-opacity="0.25" />
      <stop offset="100%" stop-color="#554234" stop-opacity="0.55" />
    </linearGradient>

    <!-- Left Flank Upper Specular -->
    <linearGradient id="lWingRim" x1="0%" y1="20%" x2="100%" y2="80%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.30" />
      <stop offset="50%" stop-color="#E5DDD5" stop-opacity="0.10" />
      <stop offset="100%" stop-color="#E5DDD5" stop-opacity="0" />
    </linearGradient>

    <!-- Left Eye Radial (Amber Iris) -->
    <radialGradient id="amberEyeL" cx="28%" cy="75%" r="68%">
      <stop offset="0%" stop-color="#FDE047" />
      <stop offset="35%" stop-color="#D99B26" />
      <stop offset="70%" stop-color="#8A4807" />
      <stop offset="90%" stop-color="#321503" />
      <stop offset="100%" stop-color="#1A0A02" />
    </radialGradient>

    <!-- Right Eye Radial (Amber Iris) -->
    <radialGradient id="amberEyeR" cx="78%" cy="75%" r="68%">
      <stop offset="0%" stop-color="#FFD54F" />
      <stop offset="35%" stop-color="#E69500" />
      <stop offset="70%" stop-color="#9E5604" />
      <stop offset="90%" stop-color="#3A1A04" />
      <stop offset="100%" stop-color="#1A0A02" />
    </radialGradient>

    <!-- Pupil -->
    <radialGradient id="pupilGrad" cx="45%" cy="35%" r="55%">
      <stop offset="0%" stop-color="#080402" />
      <stop offset="75%" stop-color="#180A03" />
      <stop offset="100%" stop-color="#281003" />
    </radialGradient>

    <!-- Beak Gradient -->
    <linearGradient id="beakGrad" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#D0C0B0" />
      <stop offset="35%" stop-color="#B2957C" />
      <stop offset="70%" stop-color="#96775E" />
      <stop offset="100%" stop-color="#644732" />
    </linearGradient>

    <!-- Precise Left Foot Toe Gradients -->
    <linearGradient id="lToe1" x1="20%" y1="0%" x2="80%" y2="100%">
      <stop offset="0%" stop-color="#D8C9BB" />
      <stop offset="35%" stop-color="#B8A391" />
      <stop offset="75%" stop-color="#7C6552" />
      <stop offset="100%" stop-color="#4C3626" />
    </linearGradient>
    <linearGradient id="lToe2" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#E8DDD1" />
      <stop offset="35%" stop-color="#C2AD9A" />
      <stop offset="75%" stop-color="#846C58" />
      <stop offset="100%" stop-color="#503A28" />
    </linearGradient>
    <linearGradient id="lToe3" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#D0C0B0" />
      <stop offset="35%" stop-color="#AE9885" />
      <stop offset="75%" stop-color="#745E4C" />
      <stop offset="100%" stop-color="#443020" />
    </linearGradient>

    <!-- Precise Right Foot Toe Gradients -->
    <linearGradient id="rToe1" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#9A8673" />
      <stop offset="40%" stop-color="#756250" />
      <stop offset="80%" stop-color="#524030" />
      <stop offset="100%" stop-color="#322214" />
    </linearGradient>
    <linearGradient id="rToe2" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#AC9885" />
      <stop offset="40%" stop-color="#84705E" />
      <stop offset="80%" stop-color="#5C4938" />
      <stop offset="100%" stop-color="#3A281A" />
    </linearGradient>
    <linearGradient id="rToe3" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#9E8A77" />
      <stop offset="40%" stop-color="#786553" />
      <stop offset="80%" stop-color="#544232" />
      <stop offset="100%" stop-color="#342416" />
    </linearGradient>

    <!-- Master Body Clip -->
    <clipPath id="bodyClip">
      <path d="{body_d}" />
    </clipPath>
  </defs>

  <!-- 1. Master Body Silhouette (Exact IoU >= 99%) -->
  <path d="{body_d}" fill="url(#bodyGrad)" />

  <!-- 2. Clipped 3D Surface Overlays -->
  <g clip-path="url(#bodyClip)">
    <!-- Cranial Specular Dome -->
    <ellipse cx="225" cy="85" rx="105" ry="55" fill="url(#cranialHl)" />
    
    <!-- Chest Illumination -->
    <ellipse cx="242" cy="280" rx="108" ry="82" fill="url(#chestHl)" />

    <!-- Left Flank Upper Specular Rim -->
    <path d="M 155 190 C 110 215, 92 255, 96 310 C 110 330, 130 320, 145 290 C 130 250, 135 220, 155 190 Z" fill="url(#lWingRim)" />

    <!-- Right Flank Ambient Occlusion -->
    <path d="M 330 195 C 380 225, 424 285, 412 380 C 395 435, 360 455, 335 440 C 365 390, 370 300, 330 195 Z" fill="url(#rWingShadow)" />

    <!-- Left Flank Lower Shading -->
    <path d="M 160 260 C 115 280, 92 320, 98 385 C 110 425, 135 445, 155 435 C 135 385, 135 330, 160 260 Z" fill="url(#lFlankShadow)" />

    <!-- Beak Cast Shadow -->
    <ellipse cx="256" cy="225" rx="15" ry="7" fill="#3D2B1E" opacity="0.32" />

    <!-- Grounded Feet with 3 Anatomical Rounded Toes -->
    <g id="feet">
      <!-- Left Foot 3 Rounded Toes -->
      <path d="M 157 470 C 157 460, 180 460, 180 470 L 180 491 L 157 491 Z" fill="url(#lToe1)" />
      <path d="M 180 458 C 180 446, 208 446, 208 458 L 209 491 L 180 491 Z" fill="url(#lToe2)" />
      <path d="M 208 468 C 208 458, 233 458, 233 468 L 235 491 L 208 491 Z" fill="url(#lToe3)" />

      <!-- Left Foot Deep Ambient Crevices -->
      <path d="M 180 462 L 180 491" stroke="#1D1208" stroke-width="3.5" stroke-linecap="round" />
      <path d="M 208 462 L 209 491" stroke="#1D1208" stroke-width="4.0" stroke-linecap="round" />

      <!-- Left Toe Specular Ridges -->
      <ellipse cx="168" cy="466" rx="5" ry="2.2" fill="#FFFFFF" opacity="0.25" />
      <ellipse cx="194" cy="456" rx="7" ry="2.5" fill="#FFFFFF" opacity="0.35" />
      <ellipse cx="220" cy="466" rx="5" ry="2.2" fill="#FFFFFF" opacity="0.25" />

      <!-- Right Foot 3 Rounded Toes -->
      <path d="M 277 468 C 277 458, 303 458, 303 468 L 303 491 L 277 491 Z" fill="url(#rToe1)" />
      <path d="M 302 458 C 302 446, 331 446, 331 458 L 331 491 L 302 491 Z" fill="url(#rToe2)" />
      <path d="M 328 470 C 328 460, 352 460, 352 470 L 353 491 L 328 491 Z" fill="url(#rToe3)" />

      <!-- Right Foot Deep Ambient Crevices -->
      <path d="M 303 462 L 303 491" stroke="#120A04" stroke-width="4.0" stroke-linecap="round" />
      <path d="M 331 462 L 331 491" stroke="#120A04" stroke-width="4.0" stroke-linecap="round" />

      <!-- Right Toe Specular Ridges -->
      <ellipse cx="290" cy="466" rx="5" ry="2.0" fill="#FFFFFF" opacity="0.10" />
      <ellipse cx="317" cy="456" rx="7" ry="2.2" fill="#FFFFFF" opacity="0.15" />
      <ellipse cx="341" cy="466" rx="5" ry="2.0" fill="#FFFFFF" opacity="0.10" />

      <!-- Ground Contact Baseline Occlusion Shadows (Y=489-491) -->
      <path d="M 156 490 L 235 490" stroke="#080402" stroke-width="2.5" opacity="0.9" />
      <path d="M 276 490 L 354 490" stroke="#080402" stroke-width="2.5" opacity="0.9" />
    </g>
  </g>

  <!-- 3. Eye Sockets & Amber Eyes -->
  <!-- Left Eye -->
  <g id="left_eye">
    <!-- Amber Iris (Full lower crescent) -->
    <ellipse cx="196" cy="159" rx="25" ry="17.5" fill="url(#amberEyeL)" />
    <!-- Obsidian Pupil (Upper Center) -->
    <ellipse cx="197" cy="151" rx="15" ry="10" fill="url(#pupilGrad)" />
    <!-- Upper Brow Socket Crease -->
    <path d="M 172 155 C 176 140, 218 140, 221 155" stroke="#251204" stroke-width="2.2" fill="none" opacity="0.8" />
  </g>

  <!-- Right Eye -->
  <g id="right_eye">
    <!-- Amber Iris (Full lower crescent) -->
    <ellipse cx="309" cy="159" rx="26" ry="17.5" fill="url(#amberEyeR)" />
    <!-- Obsidian Pupil (Upper Center) -->
    <ellipse cx="306" cy="151" rx="15" ry="10" fill="url(#pupilGrad)" />
    <!-- Upper Brow Socket Crease -->
    <path d="M 284 155 C 288 140, 332 140, 335 155" stroke="#1A0A02" stroke-width="2.2" fill="none" opacity="0.85" />
  </g>

  <!-- 4. Beak (Porcelain Amber) -->
  <g id="beak">
    <path d="M 256 168 C 267 184, 268 206, 256 218 C 244 206, 245 184, 256 168 Z" fill="url(#beakGrad)" stroke="#4A3220" stroke-width="1.2" />
    <path d="M 256 172 C 259 184, 259 200, 256 212" stroke="#FFFFFF" stroke-width="0.9" stroke-linecap="round" opacity="0.25" fill="none" />
  </g>
</svg>"""
    return svg

svg_content = build_svg_anatomical_eyes()
with open("scratch/test_anatomical_eyes.svg", "w") as f:
    f.write(svg_content)
out_png = render_svg("scratch/test_anatomical_eyes.svg", "scratch/test_anatomical_eyes.png")
evaluate_fidelity(out_png)
