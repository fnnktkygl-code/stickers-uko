import sys
sys.path.append(".")
from scripts.benchmark_owluko_fidelity import render_svg, evaluate_fidelity

with open("scratch/owluko_body_path_131.txt", "r") as f:
    body_d = f.read().strip()

# Let us build SVG with subtle glossy glints and calibrated amber gradient
def build_calibrated_svg(glint_opacity=0.0):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" style="background: transparent;">
  <defs>
    <!-- Master Body Gradient -->
    <linearGradient id="bodyGrad" x1="30%" y1="6%" x2="65%" y2="92%">
      <stop offset="0%" stop-color="#E5DDD5" />
      <stop offset="18%" stop-color="#DDD5CD" />
      <stop offset="42%" stop-color="#D4C9BD" />
      <stop offset="65%" stop-color="#BAABA0" />
      <stop offset="85%" stop-color="#9E8C7F" />
      <stop offset="100%" stop-color="#736151" />
    </linearGradient>

    <!-- Cranial Highlight -->
    <radialGradient id="cranialHl" cx="42%" cy="20%" r="48%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.65" />
      <stop offset="45%" stop-color="#F5EFEA" stop-opacity="0.22" />
      <stop offset="100%" stop-color="#DED6CE" stop-opacity="0" />
    </radialGradient>

    <!-- Chest Soft Illumination -->
    <radialGradient id="chestHl" cx="44%" cy="48%" r="40%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.25" />
      <stop offset="50%" stop-color="#ECE5DC" stop-opacity="0.10" />
      <stop offset="100%" stop-color="#DED6CE" stop-opacity="0" />
    </radialGradient>

    <!-- Wing Shadow -->
    <linearGradient id="rWingShadow" x1="10%" y1="20%" x2="90%" y2="80%">
      <stop offset="0%" stop-color="#C5B8AC" stop-opacity="0.2" />
      <stop offset="50%" stop-color="#8E7E70" stop-opacity="0.6" />
      <stop offset="100%" stop-color="#554436" stop-opacity="0.85" />
    </linearGradient>

    <!-- Left Flank Shading (gets dark at bottom!) -->
    <linearGradient id="lFlankShadow" x1="50%" y1="40%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#B8A999" stop-opacity="0" />
      <stop offset="60%" stop-color="#8E7D6D" stop-opacity="0.5" />
      <stop offset="100%" stop-color="#5C483A" stop-opacity="0.85" />
    </linearGradient>

    <!-- Left Eye Radial -->
    <radialGradient id="amberEyeL" cx="25%" cy="75%" r="70%">
      <stop offset="0%" stop-color="#FDE047" />
      <stop offset="25%" stop-color="#D99B26" />
      <stop offset="55%" stop-color="#8A4807" />
      <stop offset="85%" stop-color="#2D1302" />
      <stop offset="100%" stop-color="#150800" />
    </radialGradient>

    <!-- Right Eye Radial -->
    <radialGradient id="amberEyeR" cx="75%" cy="75%" r="70%">
      <stop offset="0%" stop-color="#FDE047" />
      <stop offset="25%" stop-color="#D99B26" />
      <stop offset="55%" stop-color="#8A4807" />
      <stop offset="85%" stop-color="#2D1302" />
      <stop offset="100%" stop-color="#150800" />
    </radialGradient>

    <!-- Pupil -->
    <radialGradient id="pupilGrad" cx="42%" cy="42%" r="52%">
      <stop offset="0%" stop-color="#080402" />
      <stop offset="75%" stop-color="#180A03" />
      <stop offset="100%" stop-color="#2C1204" />
    </radialGradient>

    <!-- Beak Gradient -->
    <linearGradient id="beakGrad" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#D5C5B5" />
      <stop offset="35%" stop-color="#B89B82" />
      <stop offset="70%" stop-color="#9E7E65" />
      <stop offset="100%" stop-color="#6E503A" />
    </linearGradient>

    <!-- Toe Gradients -->
    <linearGradient id="toeGradL" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#C9BAAA" />
      <stop offset="45%" stop-color="#A89482" />
      <stop offset="80%" stop-color="#7A6452" />
      <stop offset="100%" stop-color="#4A3626" />
    </linearGradient>
    <linearGradient id="toeGradR" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#8A7664" />
      <stop offset="45%" stop-color="#6E5A48" />
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
    <ellipse cx="250" cy="115" rx="145" ry="90" fill="url(#cranialHl)" />
    
    <!-- Chest Illumination -->
    <ellipse cx="245" cy="285" rx="110" ry="85" fill="url(#chestHl)" />

    <!-- Right Flank Ambient Occlusion -->
    <path d="M 330 200 C 380 230, 424 290, 412 380 C 395 435, 360 455, 335 440 C 365 390, 370 300, 330 200 Z" fill="url(#rWingShadow)" />

    <!-- Left Flank Lower Shading -->
    <path d="M 160 260 C 115 280, 92 320, 98 385 C 110 425, 135 445, 155 435 C 135 385, 135 330, 160 260 Z" fill="url(#lFlankShadow)" />

    <!-- Beak Cast Shadow -->
    <ellipse cx="256" cy="225" rx="16" ry="7" fill="#423022" opacity="0.35" />

    <!-- Grounded Feet with 3 Rounded Toes (Inside ClipPath so IoU stays >= 99.27%) -->
    <g id="feet">
      <!-- Left Foot -->
      <g id="left_foot">
        <path d="M 158 472 C 158 460, 180 460, 182 472 L 183 490 L 158 490 Z" fill="url(#toeGradL)" />
        <path d="M 181 462 C 181 448, 207 448, 208 462 L 209 491 L 181 491 Z" fill="url(#toeGradL)" />
        <path d="M 207 468 C 207 456, 233 456, 234 468 L 235 490 L 207 490 Z" fill="url(#toeGradL)" />
        <!-- Toe Crevices -->
        <path d="M 181 464 L 182 490" stroke="#25170B" stroke-width="2.5" stroke-linecap="round" />
        <path d="M 207 466 L 208 490" stroke="#25170B" stroke-width="2.5" stroke-linecap="round" />
        <!-- Toe Highlights -->
        <ellipse cx="170" cy="466" rx="6" ry="2.5" fill="#FFFFFF" opacity="0.18" />
        <ellipse cx="195" cy="456" rx="7" ry="2.5" fill="#FFFFFF" opacity="0.22" />
        <ellipse cx="220" cy="464" rx="6" ry="2.5" fill="#FFFFFF" opacity="0.18" />
      </g>

      <!-- Right Foot -->
      <g id="right_foot">
        <path d="M 276 468 C 276 456, 303 456, 303 468 L 304 490 L 276 490 Z" fill="url(#toeGradR)" />
        <path d="M 302 462 C 302 448, 329 448, 329 462 L 330 491 L 302 491 Z" fill="url(#toeGradR)" />
        <path d="M 328 472 C 328 460, 352 460, 352 472 L 353 490 L 328 490 Z" fill="url(#toeGradR)" />
        <!-- Toe Crevices -->
        <path d="M 303 466 L 303 490" stroke="#1D1208" stroke-width="2.5" stroke-linecap="round" />
        <path d="M 329 466 L 329 490" stroke="#1D1208" stroke-width="2.5" stroke-linecap="round" />
        <!-- Toe Highlights -->
        <ellipse cx="290" cy="464" rx="6" ry="2.5" fill="#FFFFFF" opacity="0.10" />
        <ellipse cx="316" cy="456" rx="7" ry="2.5" fill="#FFFFFF" opacity="0.12" />
        <ellipse cx="340" cy="466" rx="6" ry="2.5" fill="#FFFFFF" opacity="0.10" />
      </g>
    </g>
  </g>

  <!-- 3. Eye Sockets & Amber Eyes -->
  <!-- Left Eye -->
  <g id="left_eye">
    <!-- Socket Rim -->
    <circle cx="195" cy="155" r="26.5" fill="#402C1B" opacity="0.65" />
    <circle cx="195" cy="155" r="24.5" fill="#201004" />
    <!-- Amber Iris -->
    <circle cx="195" cy="155" r="23" fill="url(#amberEyeL)" />
    <!-- Pupil -->
    <circle cx="198" cy="150" r="13" fill="url(#pupilGrad)" />
    <!-- Specular Highlight (Subtle glossy glint) -->
    <ellipse cx="190" cy="148" rx="2.5" ry="1.8" fill="#FFFFFF" opacity="{glint_opacity}" />
    <circle cx="203" cy="160" r="1.2" fill="#FFFFFF" opacity="{glint_opacity * 0.6}" />
  </g>

  <!-- Right Eye -->
  <g id="right_eye">
    <!-- Socket Rim -->
    <circle cx="310" cy="155" r="26.5" fill="#402C1B" opacity="0.65" />
    <circle cx="310" cy="155" r="24.5" fill="#201004" />
    <!-- Amber Iris -->
    <circle cx="310" cy="155" r="23" fill="url(#amberEyeR)" />
    <!-- Pupil -->
    <circle cx="305" cy="150" r="13" fill="url(#pupilGrad)" />
    <!-- Specular Highlight -->
    <ellipse cx="304" cy="148" rx="2.5" ry="1.8" fill="#FFFFFF" opacity="{glint_opacity}" />
    <circle cx="318" cy="160" r="1.2" fill="#FFFFFF" opacity="{glint_opacity * 0.6}" />
  </g>

  <!-- 4. Beak (Porcelain Amber) -->
  <g id="beak">
    <path d="M 256 168 C 267 184, 268 206, 256 218 C 244 206, 245 184, 256 168 Z" fill="url(#beakGrad)" stroke="#4A3220" stroke-width="1.2" />
    <path d="M 256 172 C 259 184, 259 200, 256 212" stroke="#FFFFFF" stroke-width="1.0" stroke-linecap="round" opacity="0.3" fill="none" />
  </g>
</svg>"""
    return svg

for op in [0.0, 0.25, 0.5]:
    svg = build_calibrated_svg(op)
    with open("scratch/test_calib_eye.svg", "w") as f:
        f.write(svg)
    out_png = render_svg("scratch/test_calib_eye.svg", f"scratch/test_calib_{op}.png")
    print(f"\n--- Testing Glint Opacity {op} ---")
    evaluate_fidelity(out_png)
