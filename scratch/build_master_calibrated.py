import sys
sys.path.append(".")
from scripts.benchmark_owluko_fidelity import render_svg, evaluate_fidelity

with open("scratch/owluko_body_path_131.txt", "r") as f:
    body_d = f.read().strip()

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" style="background: transparent;">
  <defs>
    <!-- Master Body Gradient (Calibrated Warm Porcelain Studio) -->
    <linearGradient id="bodyGrad" x1="34%" y1="5%" x2="65%" y2="90%">
      <stop offset="0%" stop-color="#E8E0D8" />
      <stop offset="16%" stop-color="#DDD5CD" />
      <stop offset="38%" stop-color="#DFD5CB" />
      <stop offset="60%" stop-color="#C8BCB1" />
      <stop offset="82%" stop-color="#A59587" />
      <stop offset="100%" stop-color="#726052" />
    </linearGradient>

    <!-- Cranial Specular Dome -->
    <radialGradient id="cranialHl" cx="38%" cy="16%" r="35%">
      <stop offset="0%" stop-color="#FFF2E6" stop-opacity="0.48" />
      <stop offset="50%" stop-color="#F5EFEA" stop-opacity="0.16" />
      <stop offset="100%" stop-color="#DED6CE" stop-opacity="0" />
    </radialGradient>

    <!-- Chest Soft Illumination -->
    <radialGradient id="chestHl" cx="42%" cy="45%" r="48%">
      <stop offset="0%" stop-color="#FFF5EC" stop-opacity="0.32" />
      <stop offset="55%" stop-color="#F2E6DC" stop-opacity="0.12" />
      <stop offset="100%" stop-color="#DED6CE" stop-opacity="0" />
    </radialGradient>

    <!-- Right Brow & Temple Ambient Shadow -->
    <linearGradient id="rHeadShadow" x1="0%" y1="20%" x2="100%" y2="80%">
      <stop offset="0%" stop-color="#C5B8AC" stop-opacity="0" />
      <stop offset="50%" stop-color="#8E7E70" stop-opacity="0.25" />
      <stop offset="100%" stop-color="#554436" stop-opacity="0.50" />
    </linearGradient>

    <!-- Right Flank Ambient Occlusion Shadow -->
    <linearGradient id="rWingShadow" x1="10%" y1="20%" x2="90%" y2="80%">
      <stop offset="0%" stop-color="#C5B8AC" stop-opacity="0.10" />
      <stop offset="45%" stop-color="#9E8E80" stop-opacity="0.30" />
      <stop offset="100%" stop-color="#706050" stop-opacity="0.35" />
    </linearGradient>

    <!-- Left Flank Shading -->
    <linearGradient id="lFlankShadow" x1="50%" y1="35%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#B8A999" stop-opacity="0" />
      <stop offset="55%" stop-color="#8E7D6D" stop-opacity="0.20" />
      <stop offset="100%" stop-color="#554234" stop-opacity="0.45" />
    </linearGradient>

    <!-- Left Flank Upper Specular Rim -->
    <linearGradient id="lWingRim" x1="0%" y1="20%" x2="100%" y2="80%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.25" />
      <stop offset="50%" stop-color="#E5DDD5" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#E5DDD5" stop-opacity="0" />
    </linearGradient>

    <!-- Cheek Radial Highlights -->
    <radialGradient id="leftCheekGlow" cx="45%" cy="45%" r="50%">
      <stop offset="0%" stop-color="#FFF4E8" stop-opacity="0.50" />
      <stop offset="60%" stop-color="#F5E8DC" stop-opacity="0.20" />
      <stop offset="100%" stop-color="#E8DDD5" stop-opacity="0" />
    </radialGradient>

    <radialGradient id="rightCheekGlow" cx="50%" cy="45%" r="50%">
      <stop offset="0%" stop-color="#FFE8D2" stop-opacity="0.25" />
      <stop offset="60%" stop-color="#F0DDD0" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#E8DDD5" stop-opacity="0" />
    </radialGradient>

    <!-- Left Eye Radial (Amber Iris) -->
    <radialGradient id="amberEyeL" cx="20%" cy="80%" r="75%">
      <stop offset="0%" stop-color="#FDE047" />
      <stop offset="25%" stop-color="#D99B26" />
      <stop offset="55%" stop-color="#8A4807" />
      <stop offset="85%" stop-color="#2D1302" />
      <stop offset="100%" stop-color="#150800" />
    </radialGradient>

    <!-- Right Eye Radial (Amber Iris) -->
    <radialGradient id="amberEyeR" cx="82%" cy="78%" r="75%">
      <stop offset="0%" stop-color="#FFD54F" />
      <stop offset="25%" stop-color="#FFA000" />
      <stop offset="55%" stop-color="#B26A00" />
      <stop offset="82%" stop-color="#3E1C02" />
      <stop offset="100%" stop-color="#180A02" />
    </radialGradient>

    <!-- Pupil (Bronze Obsidian) -->
    <radialGradient id="pupilGrad" cx="45%" cy="40%" r="55%">
      <stop offset="0%" stop-color="#24140A" />
      <stop offset="70%" stop-color="#352014" />
      <stop offset="100%" stop-color="#462C1C" />
    </radialGradient>

    <!-- Beak Gradient -->
    <linearGradient id="beakGrad" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#D0C0B0" />
      <stop offset="35%" stop-color="#B2957C" />
      <stop offset="70%" stop-color="#96775E" />
      <stop offset="100%" stop-color="#644732" />
    </linearGradient>

    <!-- Master Body Clip (Exact Contour IoU >= 98.4%) -->
    <clipPath id="bodyClip">
      <path d="{body_d}" />
    </clipPath>
  </defs>

  <!-- 1. Master Body Silhouette -->
  <path d="{body_d}" fill="url(#bodyGrad)" />

  <!-- 2. Clipped 3D Surface Overlays -->
  <g clip-path="url(#bodyClip)">
    <!-- Cranial Specular Dome -->
    <ellipse cx="225" cy="85" rx="105" ry="55" fill="url(#cranialHl)" />
    
    <!-- Chest Illumination -->
    <ellipse cx="236" cy="255" rx="125" ry="95" fill="url(#chestHl)" />

    <!-- Right Brow & Temple Shading -->
    <path d="M 265 75 C 330 80, 395 105, 405 180 C 375 180, 330 160, 290 140 C 270 120, 260 95, 265 75 Z" fill="url(#rHeadShadow)" />

    <!-- Left Flank Upper Specular Rim -->
    <path d="M 155 190 C 110 215, 92 255, 96 310 C 110 330, 130 320, 145 290 C 130 250, 135 220, 155 190 Z" fill="url(#lWingRim)" />

    <!-- Right Flank Ambient Occlusion -->
    <path d="M 330 195 C 380 225, 424 285, 412 380 C 395 435, 360 455, 335 440 C 365 390, 370 300, 330 195 Z" fill="url(#rWingShadow)" />

    <!-- Left Flank Lower Shading -->
    <path d="M 160 260 C 115 280, 92 320, 98 385 C 110 425, 135 445, 155 435 C 135 385, 135 330, 160 260 Z" fill="url(#lFlankShadow)" />

    <!-- Facial Cheek Volumes -->
    <ellipse cx="135" cy="160" rx="30" ry="34" fill="url(#leftCheekGlow)" />
    <ellipse cx="378" cy="158" rx="30" ry="34" fill="url(#rightCheekGlow)" />

    <!-- Beak Cast Shadow -->
    <ellipse cx="256" cy="225" rx="15" ry="7" fill="#3D2B1E" opacity="0.30" />

    <!-- Grounded Feet with 3 Rounded Toes -->
    <g id="feet">
      <!-- Left Foot Ambient Shading -->
      <path d="M 156 455 C 156 445, 235 445, 235 455 L 235 491 L 156 491 Z" fill="#8E7864" opacity="0.35" />

      <!-- Left Foot 3 Rounded Toe Highlights -->
      <ellipse cx="168" cy="474" rx="9" ry="8" fill="#E8DDD1" opacity="0.45" />
      <ellipse cx="194" cy="466" rx="11" ry="10" fill="#FFF2E6" opacity="0.55" />
      <ellipse cx="220" cy="474" rx="9" ry="8" fill="#DFD2C4" opacity="0.45" />

      <!-- Left Foot Crevices -->
      <path d="M 181 462 L 181 491" stroke="#25160A" stroke-width="2.5" opacity="0.65" stroke-linecap="round" />
      <path d="M 208 462 L 208 491" stroke="#25160A" stroke-width="3.0" opacity="0.65" stroke-linecap="round" />

      <!-- Left Foot Ground Occlusion -->
      <path d="M 156 490 L 235 490" stroke="#080402" stroke-width="2.5" opacity="0.9" />

      <!-- Right Foot Ambient Shading -->
      <path d="M 276 455 C 276 445, 353 445, 353 455 L 353 491 L 276 491 Z" fill="#523E2E" opacity="0.45" />

      <!-- Right Foot 3 Rounded Toe Highlights -->
      <ellipse cx="290" cy="474" rx="8" ry="7" fill="#B5A08C" opacity="0.30" />
      <ellipse cx="317" cy="466" rx="10" ry="9" fill="#C4B09C" opacity="0.35" />
      <ellipse cx="341" cy="474" rx="8" ry="7" fill="#B8A490" opacity="0.30" />

      <!-- Right Foot Crevices -->
      <path d="M 303 462 L 303 491" stroke="#180C04" stroke-width="2.5" opacity="0.70" stroke-linecap="round" />
      <path d="M 330 462 L 330 491" stroke="#180C04" stroke-width="2.5" opacity="0.70" stroke-linecap="round" />

      <!-- Right Foot Ground Occlusion -->
      <path d="M 276 490 L 354 490" stroke="#080402" stroke-width="2.5" opacity="0.9" />
    </g>
  </g>

  <!-- 3. Eye Sockets & Amber Eyes -->
  <!-- Left Eye -->
  <g id="left_eye">
    <!-- Brow Crevice / Socket Rim -->
    <ellipse cx="194" cy="157" rx="26" ry="18.5" fill="#3D2817" opacity="0.65" />
    <ellipse cx="194" cy="157" rx="24" ry="17" fill="#1C0C02" />
    <!-- Amber Iris -->
    <ellipse cx="194" cy="157" rx="23" ry="16" fill="url(#amberEyeL)" />
    <!-- Pupil -->
    <ellipse cx="195" cy="153" rx="14" ry="10.5" fill="url(#pupilGrad)" />
  </g>

  <!-- Right Eye -->
  <g id="right_eye">
    <!-- Brow Crevice / Socket Rim -->
    <ellipse cx="311" cy="158" rx="27.5" ry="19" fill="#301A0D" opacity="0.75" />
    <ellipse cx="311" cy="158" rx="25.5" ry="17.5" fill="#180A02" />
    <!-- Amber Iris -->
    <ellipse cx="311" cy="158" rx="24.5" ry="16.5" fill="url(#amberEyeR)" />
    <!-- Pupil -->
    <ellipse cx="309" cy="154" rx="14" ry="10.5" fill="url(#pupilGrad)" />
  </g>

  <!-- 4. Beak (Porcelain Amber) -->
  <g id="beak">
    <path d="M 256 168 C 267 184, 268 206, 256 218 C 244 206, 245 184, 256 168 Z" fill="url(#beakGrad)" />
    <path d="M 256 172 C 259 184, 259 200, 256 212" stroke="#FFFFFF" stroke-width="0.9" stroke-linecap="round" opacity="0.25" fill="none" />
  </g>
</svg>"""

with open("scratch/owluko_master_calibrated.svg", "w") as f:
    f.write(svg)

out_png = render_svg("scratch/owluko_master_calibrated.svg", "scratch/owluko_master_calibrated.png")
res = evaluate_fidelity(out_png)
