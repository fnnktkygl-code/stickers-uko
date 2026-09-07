import sys
sys.path.append(".")
from scripts.benchmark_owluko_fidelity import render_svg, evaluate_fidelity

with open("scratch/owluko_body_path_131.txt", "r") as f:
    body_d = f.read().strip()

def build_feet_svg(t_bright=1.0):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" style="background: transparent;">
  <defs>
    <!-- Master Body Gradient -->
    <linearGradient id="bodyGrad" x1="26%" y1="5%" x2="68%" y2="95%">
      <stop offset="0%" stop-color="#E5DDD5" />
      <stop offset="16%" stop-color="#DDD5CD" />
      <stop offset="38%" stop-color="#D4C9BD" />
      <stop offset="62%" stop-color="#B4A596" />
      <stop offset="82%" stop-color="#8A7768" />
      <stop offset="100%" stop-color="#4A3A2C" />
    </linearGradient>

    <!-- Cranial Highlight -->
    <radialGradient id="cranialHl" cx="42%" cy="20%" r="46%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.45" />
      <stop offset="45%" stop-color="#F5EFEA" stop-opacity="0.16" />
      <stop offset="100%" stop-color="#DED6CE" stop-opacity="0" />
    </radialGradient>

    <!-- Chest Soft Illumination -->
    <radialGradient id="chestHl" cx="44%" cy="48%" r="42%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.20" />
      <stop offset="50%" stop-color="#ECE5DC" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#DED6CE" stop-opacity="0" />
    </radialGradient>

    <!-- Wing Shadow -->
    <linearGradient id="rWingShadow" x1="10%" y1="20%" x2="90%" y2="80%">
      <stop offset="0%" stop-color="#C5B8AC" stop-opacity="0.15" />
      <stop offset="45%" stop-color="#8E7E70" stop-opacity="0.52" />
      <stop offset="100%" stop-color="#48382A" stop-opacity="0.75" />
    </linearGradient>

    <!-- Left Flank Shading -->
    <linearGradient id="lFlankShadow" x1="50%" y1="35%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#B8A999" stop-opacity="0" />
      <stop offset="55%" stop-color="#8E7D6D" stop-opacity="0.30" />
      <stop offset="100%" stop-color="#483628" stop-opacity="0.60" />
    </linearGradient>

    <!-- Left Flank Upper Specular -->
    <linearGradient id="lWingRim" x1="0%" y1="20%" x2="100%" y2="80%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.30" />
      <stop offset="50%" stop-color="#E5DDD5" stop-opacity="0.10" />
      <stop offset="100%" stop-color="#E5DDD5" stop-opacity="0" />
    </linearGradient>

    <!-- Left Eye Radial -->
    <radialGradient id="amberEyeL" cx="20%" cy="80%" r="75%">
      <stop offset="0%" stop-color="#FDE047" />
      <stop offset="25%" stop-color="#D99B26" />
      <stop offset="55%" stop-color="#8A4807" />
      <stop offset="85%" stop-color="#2D1302" />
      <stop offset="100%" stop-color="#150800" />
    </radialGradient>

    <!-- Right Eye Radial -->
    <radialGradient id="amberEyeR" cx="82%" cy="78%" r="75%">
      <stop offset="0%" stop-color="#FFD54F" />
      <stop offset="25%" stop-color="#FFA000" />
      <stop offset="55%" stop-color="#B26A00" />
      <stop offset="82%" stop-color="#3E1C02" />
      <stop offset="100%" stop-color="#180A02" />
    </radialGradient>

    <!-- Pupil -->
    <radialGradient id="pupilGrad" cx="45%" cy="40%" r="55%">
      <stop offset="0%" stop-color="#080402" />
      <stop offset="70%" stop-color="#180A03" />
      <stop offset="100%" stop-color="#2C1204" />
    </radialGradient>

    <!-- Beak Gradient -->
    <linearGradient id="beakGrad" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#D0C0B0" />
      <stop offset="35%" stop-color="#B2957C" />
      <stop offset="70%" stop-color="#96775E" />
      <stop offset="100%" stop-color="#644732" />
    </linearGradient>

    <!-- Precise Left Foot Toe Gradients (Light Key Side) -->
    <!-- Toe 1 Outer -->
    <linearGradient id="lToe1" x1="20%" y1="0%" x2="80%" y2="100%">
      <stop offset="0%" stop-color="#D8C9BB" />
      <stop offset="35%" stop-color="#B8A391" />
      <stop offset="75%" stop-color="#7C6552" />
      <stop offset="100%" stop-color="#4C3626" />
    </linearGradient>
    <!-- Toe 2 Middle (Peak Highlight) -->
    <linearGradient id="lToe2" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#E8DDD1" />
      <stop offset="35%" stop-color="#C2AD9A" />
      <stop offset="75%" stop-color="#846C58" />
      <stop offset="100%" stop-color="#503A28" />
    </linearGradient>
    <!-- Toe 3 Inner -->
    <linearGradient id="lToe3" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#D0C0B0" />
      <stop offset="35%" stop-color="#AE9885" />
      <stop offset="75%" stop-color="#745E4C" />
      <stop offset="100%" stop-color="#443020" />
    </linearGradient>

    <!-- Precise Right Foot Toe Gradients (Warm Shadow Side) -->
    <!-- Toe 1 Inner -->
    <linearGradient id="rToe1" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#9A8673" />
      <stop offset="40%" stop-color="#756250" />
      <stop offset="80%" stop-color="#524030" />
      <stop offset="100%" stop-color="#322214" />
    </linearGradient>
    <!-- Toe 2 Middle -->
    <linearGradient id="rToe2" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#AC9885" />
      <stop offset="40%" stop-color="#84705E" />
      <stop offset="80%" stop-color="#5C4938" />
      <stop offset="100%" stop-color="#3A281A" />
    </linearGradient>
    <!-- Toe 3 Outer -->
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
    <ellipse cx="248" cy="112" rx="142" ry="88" fill="url(#cranialHl)" />
    
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

    <!-- Grounded Feet with 3 Anatomical Rounded Toes (Inside ClipPath so IoU stays >= 99.27%) -->
    <g id="feet">
      <!-- Left Foot Base Shadow -->
      <path d="M 156 460 C 156 448, 226 448, 226 460 L 235 491 L 156 491 Z" fill="#423022" />

      <!-- Left Foot 3 Rounded Toes -->
      <!-- Toe 1 Outer (X: 156-182) -->
      <path d="M 157 470 C 157 460, 180 460, 180 470 L 180 491 L 157 491 Z" fill="url(#lToe1)" />
      <!-- Toe 2 Middle (X: 179-209, Longest, Peak at 456) -->
      <path d="M 180 458 C 180 446, 208 446, 208 458 L 209 491 L 180 491 Z" fill="url(#lToe2)" />
      <!-- Toe 3 Inner (X: 207-234) -->
      <path d="M 208 468 C 208 458, 233 458, 233 468 L 235 491 L 208 491 Z" fill="url(#lToe3)" />

      <!-- Left Foot Deep Ambient Crevices -->
      <path d="M 180 462 L 180 491" stroke="#1D1208" stroke-width="3.5" stroke-linecap="round" />
      <path d="M 208 462 L 209 491" stroke="#1D1208" stroke-width="4.0" stroke-linecap="round" />

      <!-- Left Toe Specular Ridges -->
      <ellipse cx="168" cy="466" rx="5" ry="2.2" fill="#FFFFFF" opacity="0.25" />
      <ellipse cx="194" cy="456" rx="7" ry="2.5" fill="#FFFFFF" opacity="0.35" />
      <ellipse cx="220" cy="466" rx="5" ry="2.2" fill="#FFFFFF" opacity="0.25" />

      <!-- Right Foot Base Shadow -->
      <path d="M 276 460 C 276 448, 353 448, 353 460 L 353 491 L 276 491 Z" fill="#2E1E12" />

      <!-- Right Foot 3 Rounded Toes -->
      <!-- Toe 1 Inner (X: 276-304) -->
      <path d="M 277 468 C 277 458, 303 458, 303 468 L 303 491 L 277 491 Z" fill="url(#rToe1)" />
      <!-- Toe 2 Middle (X: 302-332, Longest, Peak at 456) -->
      <path d="M 303 458 C 303 446, 331 446, 331 458 L 331 491 L 303 491 Z" fill="url(#rToe2)" />
      <!-- Toe 3 Outer (X: 330-353) -->
      <path d="M 330 470 C 330 460, 352 460, 352 470 L 353 491 L 330 491 Z" fill="url(#rToe3)" />

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

  <!-- 3. Eye Sockets & Amber Eyes (Elliptical Anatomic Aperture) -->
  <!-- Left Eye -->
  <g id="left_eye">
    <!-- Brow Crevice / Socket Rim -->
    <ellipse cx="196" cy="159" rx="27" ry="19.5" fill="#3D2817" opacity="0.65" />
    <ellipse cx="196" cy="159" rx="25" ry="18" fill="#1C0C02" />
    <!-- Amber Iris -->
    <ellipse cx="196" cy="159" rx="24" ry="17" fill="url(#amberEyeL)" />
    <!-- Pupil -->
    <ellipse cx="197" cy="155" rx="14" ry="11.5" fill="url(#pupilGrad)" />
  </g>

  <!-- Right Eye -->
  <g id="right_eye">
    <!-- Brow Crevice / Socket Rim -->
    <ellipse cx="309" cy="159" rx="28.5" ry="19.5" fill="#301A0D" opacity="0.75" />
    <ellipse cx="309" cy="159" rx="26.5" ry="18" fill="#180A02" />
    <!-- Amber Iris -->
    <ellipse cx="309" cy="159" rx="25.5" ry="17" fill="url(#amberEyeR)" />
    <!-- Pupil -->
    <ellipse cx="307" cy="155" rx="14" ry="11.5" fill="url(#pupilGrad)" />
  </g>

  <!-- 4. Beak (Porcelain Amber) -->
  <g id="beak">
    <path d="M 256 168 C 267 184, 268 206, 256 218 C 244 206, 245 184, 256 168 Z" fill="url(#beakGrad)" stroke="#4A3220" stroke-width="1.2" />
    <path d="M 256 172 C 259 184, 259 200, 256 212" stroke="#FFFFFF" stroke-width="0.9" stroke-linecap="round" opacity="0.25" fill="none" />
  </g>
</svg>"""
    return svg

svg_content = build_feet_svg()
with open("scratch/test_tune_feet.svg", "w") as f:
    f.write(svg_content)
out_png = render_svg("scratch/test_tune_feet.svg", "scratch/test_tune_feet.png")
evaluate_fidelity(out_png)
