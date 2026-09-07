import sys, os
sys.path.append(".")
import cv2, numpy as np
from PIL import Image
from scripts.benchmark_owluko_fidelity import render_svg, evaluate_fidelity

with open("scratch/owluko_body_path_131.txt", "r") as f:
    body_d = f.read().strip()

def test_config(
    body_x1=26, body_y1=5, body_x2=68, body_y2=95,
    s0="#E5DDD5", s1="#DDD5CD", s2="#D4C9BD", s3="#B4A596", s4="#8A7768", s5="#4A3A2C",
    cranial_op=0.45, cranial_r=46,
    chest_op=0.20, chest_cy=280,
    r_wing_op=0.75,
    l_shadow_op=0.60,
    l_eye_r=23, r_eye_r=23
):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" style="background: transparent;">
  <defs>
    <!-- Master Body Gradient -->
    <linearGradient id="bodyGrad" x1="{body_x1}%" y1="{body_y1}%" x2="{body_x2}%" y2="{body_y2}%">
      <stop offset="0%" stop-color="{s0}" />
      <stop offset="16%" stop-color="{s1}" />
      <stop offset="38%" stop-color="{s2}" />
      <stop offset="62%" stop-color="{s3}" />
      <stop offset="82%" stop-color="{s4}" />
      <stop offset="100%" stop-color="{s5}" />
    </linearGradient>

    <!-- Cranial Highlight -->
    <radialGradient id="cranialHl" cx="42%" cy="20%" r="{cranial_r}%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="{cranial_op}" />
      <stop offset="45%" stop-color="#F5EFEA" stop-opacity="{cranial_op * 0.35}" />
      <stop offset="100%" stop-color="#DED6CE" stop-opacity="0" />
    </radialGradient>

    <!-- Chest Soft Illumination -->
    <radialGradient id="chestHl" cx="44%" cy="48%" r="42%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="{chest_op}" />
      <stop offset="50%" stop-color="#ECE5DC" stop-opacity="{chest_op * 0.4}" />
      <stop offset="100%" stop-color="#DED6CE" stop-opacity="0" />
    </radialGradient>

    <!-- Wing Shadow -->
    <linearGradient id="rWingShadow" x1="10%" y1="20%" x2="90%" y2="80%">
      <stop offset="0%" stop-color="#C5B8AC" stop-opacity="0.15" />
      <stop offset="45%" stop-color="#8E7E70" stop-opacity="{r_wing_op * 0.7}" />
      <stop offset="100%" stop-color="#48382A" stop-opacity="{r_wing_op}" />
    </linearGradient>

    <!-- Left Flank Shading -->
    <linearGradient id="lFlankShadow" x1="50%" y1="35%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#B8A999" stop-opacity="0" />
      <stop offset="55%" stop-color="#8E7D6D" stop-opacity="{l_shadow_op * 0.5}" />
      <stop offset="100%" stop-color="#483628" stop-opacity="{l_shadow_op}" />
    </linearGradient>

    <!-- Left Flank Upper Specular (Chest/Wing rim) -->
    <linearGradient id="lWingRim" x1="0%" y1="20%" x2="100%" y2="80%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.30" />
      <stop offset="50%" stop-color="#E5DDD5" stop-opacity="0.10" />
      <stop offset="100%" stop-color="#E5DDD5" stop-opacity="0" />
    </linearGradient>

    <!-- Left Eye Radial -->
    <radialGradient id="amberEyeL" cx="24%" cy="74%" r="72%">
      <stop offset="0%" stop-color="#FDE047" />
      <stop offset="25%" stop-color="#D99B26" />
      <stop offset="55%" stop-color="#8A4807" />
      <stop offset="85%" stop-color="#2D1302" />
      <stop offset="100%" stop-color="#150800" />
    </radialGradient>

    <!-- Right Eye Radial (Deeper amber in shadow) -->
    <radialGradient id="amberEyeR" cx="74%" cy="74%" r="72%">
      <stop offset="0%" stop-color="#FBC02D" />
      <stop offset="25%" stop-color="#C78518" />
      <stop offset="55%" stop-color="#7B3E05" />
      <stop offset="85%" stop-color="#261001" />
      <stop offset="100%" stop-color="#120600" />
    </radialGradient>

    <!-- Pupil -->
    <radialGradient id="pupilGrad" cx="42%" cy="42%" r="52%">
      <stop offset="0%" stop-color="#080402" />
      <stop offset="75%" stop-color="#180A03" />
      <stop offset="100%" stop-color="#2C1204" />
    </radialGradient>

    <!-- Beak Gradient -->
    <linearGradient id="beakGrad" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#D0C0B0" />
      <stop offset="35%" stop-color="#B2957C" />
      <stop offset="70%" stop-color="#96775E" />
      <stop offset="100%" stop-color="#644732" />
    </linearGradient>

    <!-- Toe Gradients -->
    <linearGradient id="toeGradL" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#C9BAAA" />
      <stop offset="45%" stop-color="#A89482" />
      <stop offset="80%" stop-color="#7A6452" />
      <stop offset="100%" stop-color="#4A3626" />
    </linearGradient>
    <linearGradient id="toeGradR" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#857260" />
      <stop offset="45%" stop-color="#6A5644" />
      <stop offset="80%" stop-color="#4E3D2E" />
      <stop offset="100%" stop-color="#302014" />
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
    <ellipse cx="242" cy="{chest_cy}" rx="108" ry="82" fill="url(#chestHl)" />

    <!-- Left Flank Upper Specular Rim -->
    <path d="M 155 190 C 110 215, 92 255, 96 310 C 110 330, 130 320, 145 290 C 130 250, 135 220, 155 190 Z" fill="url(#lWingRim)" />

    <!-- Right Flank Ambient Occlusion -->
    <path d="M 330 195 C 380 225, 424 285, 412 380 C 395 435, 360 455, 335 440 C 365 390, 370 300, 330 195 Z" fill="url(#rWingShadow)" />

    <!-- Left Flank Lower Shading -->
    <path d="M 160 260 C 115 280, 92 320, 98 385 C 110 425, 135 445, 155 435 C 135 385, 135 330, 160 260 Z" fill="url(#lFlankShadow)" />

    <!-- Beak Cast Shadow -->
    <ellipse cx="256" cy="225" rx="15" ry="7" fill="#3D2B1E" opacity="0.32" />

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
        <ellipse cx="170" cy="466" rx="5" ry="2.0" fill="#FFFFFF" opacity="0.14" />
        <ellipse cx="195" cy="456" rx="6" ry="2.0" fill="#FFFFFF" opacity="0.18" />
        <ellipse cx="220" cy="464" rx="5" ry="2.0" fill="#FFFFFF" opacity="0.14" />
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
        <ellipse cx="290" cy="464" rx="5" ry="2.0" fill="#FFFFFF" opacity="0.08" />
        <ellipse cx="316" cy="456" rx="6" ry="2.0" fill="#FFFFFF" opacity="0.10" />
        <ellipse cx="340" cy="466" rx="5" ry="2.0" fill="#FFFFFF" opacity="0.08" />
      </g>
    </g>
  </g>

  <!-- 3. Eye Sockets & Amber Eyes -->
  <!-- Left Eye -->
  <g id="left_eye">
    <!-- Socket Rim -->
    <circle cx="195" cy="155" r="{l_eye_r+3.5}" fill="#402C1B" opacity="0.65" />
    <circle cx="195" cy="155" r="{l_eye_r+1.5}" fill="#201004" />
    <!-- Amber Iris -->
    <circle cx="195" cy="155" r="{l_eye_r}" fill="url(#amberEyeL)" />
    <!-- Pupil -->
    <circle cx="198" cy="150" r="13" fill="url(#pupilGrad)" />
  </g>

  <!-- Right Eye -->
  <g id="right_eye">
    <!-- Socket Rim (Darker on shaded right side) -->
    <circle cx="310" cy="155" r="{r_eye_r+3.5}" fill="#332012" opacity="0.75" />
    <circle cx="310" cy="155" r="{r_eye_r+1.5}" fill="#180A02" />
    <!-- Amber Iris -->
    <circle cx="310" cy="155" r="{r_eye_r}" fill="url(#amberEyeR)" />
    <!-- Pupil -->
    <circle cx="305" cy="150" r="13" fill="url(#pupilGrad)" />
  </g>

  <!-- 4. Beak (Porcelain Amber) -->
  <g id="beak">
    <path d="M 256 168 C 267 184, 268 206, 256 218 C 244 206, 245 184, 256 168 Z" fill="url(#beakGrad)" stroke="#4A3220" stroke-width="1.2" />
    <path d="M 256 172 C 259 184, 259 200, 256 212" stroke="#FFFFFF" stroke-width="0.9" stroke-linecap="round" opacity="0.25" fill="none" />
  </g>
</svg>"""
    return svg

svg_content = test_config()
with open("scratch/test_opt_step.svg", "w") as f:
    f.write(svg_content)
out_png = render_svg("scratch/test_opt_step.svg", "scratch/test_opt_step.png")
evaluate_fidelity(out_png)
