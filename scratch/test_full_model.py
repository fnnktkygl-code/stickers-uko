import os, sys
sys.path.append(".")
import cv2, numpy as np
from PIL import Image
from scripts.benchmark_owluko_fidelity import compute_ssim_numpy, render_svg, evaluate_fidelity

with open("scratch/owluko_body_path_131.txt", "r") as f:
    body_d = f.read().strip()

def build_svg(params):
    # Unpack params
    # Body gradient
    bg_s0 = params.get('bg_s0', '#E5DDD5')
    bg_s1 = params.get('bg_s1', '#DDD5CD')
    bg_s2 = params.get('bg_s2', '#D4C9BD')
    bg_s3 = params.get('bg_s3', '#BAABA0')
    bg_s4 = params.get('bg_s4', '#9E8C7F')
    bg_s5 = params.get('bg_s5', '#736151')

    # Eyes
    lx = params.get('lx', 195)
    ly = params.get('ly', 155)
    lr = params.get('lr', 24)
    lpx = params.get('lpx', 199)
    lpy = params.get('lpy', 149)
    lpr = params.get('lpr', 13)

    rx = params.get('rx', 311)
    ry = params.get('ry', 155)
    rr = params.get('rr', 24)
    rpx = params.get('rpx', 305)
    rpy = params.get('rpy', 149)
    rpr = params.get('rpr', 13)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" style="background: transparent;">
  <defs>
    <!-- Master Body Gradient -->
    <linearGradient id="bodyGrad" x1="28%" y1="6%" x2="72%" y2="94%">
      <stop offset="0%" stop-color="{bg_s0}" />
      <stop offset="18%" stop-color="{bg_s1}" />
      <stop offset="42%" stop-color="{bg_s2}" />
      <stop offset="65%" stop-color="{bg_s3}" />
      <stop offset="85%" stop-color="{bg_s4}" />
      <stop offset="100%" stop-color="{bg_s5}" />
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

    <!-- Left Wing Rim -->
    <linearGradient id="lWingRim" x1="0%" y1="30%" x2="100%" y2="70%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.5" />
      <stop offset="60%" stop-color="#E5DDD5" stop-opacity="0.2" />
      <stop offset="100%" stop-color="#E5DDD5" stop-opacity="0" />
    </linearGradient>

    <!-- Left Eye Radial -->
    <radialGradient id="amberEyeL" cx="28%" cy="72%" r="72%">
      <stop offset="0%" stop-color="#FDE047" />
      <stop offset="28%" stop-color="#D99B26" />
      <stop offset="62%" stop-color="#8A4807" />
      <stop offset="86%" stop-color="#2D1302" />
      <stop offset="100%" stop-color="#150800" />
    </radialGradient>

    <!-- Right Eye Radial -->
    <radialGradient id="amberEyeR" cx="72%" cy="72%" r="72%">
      <stop offset="0%" stop-color="#FDE047" />
      <stop offset="28%" stop-color="#D99B26" />
      <stop offset="62%" stop-color="#8A4807" />
      <stop offset="86%" stop-color="#2D1302" />
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
      <stop offset="0%" stop-color="#E0D2C4" />
      <stop offset="40%" stop-color="#BCA896" />
      <stop offset="80%" stop-color="#8C7460" />
      <stop offset="100%" stop-color="#5C4635" />
    </linearGradient>
    <linearGradient id="toeGradR" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#D2C4B5" />
      <stop offset="40%" stop-color="#A89482" />
      <stop offset="80%" stop-color="#7C6652" />
      <stop offset="100%" stop-color="#4C3828" />
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

    <!-- Left Flank Rim Highlight -->
    <path d="M 160 210 C 115 240, 92 290, 98 380 C 110 425, 135 445, 155 435 C 135 385, 135 300, 160 210 Z" fill="url(#lWingRim)" />

    <!-- Beak Cast Shadow -->
    <ellipse cx="256" cy="225" rx="16" ry="7" fill="#423022" opacity="0.35" />
  </g>

  <!-- 3. Eye Sockets & Amber Eyes -->
  <!-- Left Eye -->
  <g id="left_eye">
    <!-- Socket Outer Crevice -->
    <circle cx="{lx}" cy="{ly}" r="{lr+3.5}" fill="#402C1B" opacity="0.75" />
    <circle cx="{lx}" cy="{ly}" r="{lr+1.5}" fill="#201004" />
    <!-- Amber Iris -->
    <circle cx="{lx}" cy="{ly}" r="{lr}" fill="url(#amberEyeL)" />
    <!-- Pupil -->
    <circle cx="{lpx}" cy="{lpy}" r="{lpr}" fill="url(#pupilGrad)" />
    <!-- Specular Glints -->
    <ellipse cx="{lx-5}" cy="{ly-6}" rx="3.5" ry="2.5" fill="#FFFFFF" opacity="0.95" />
    <circle cx="{lx+7}" cy="{ly+6}" r="1.8" fill="#FFFFFF" opacity="0.55" />
  </g>

  <!-- Right Eye -->
  <g id="right_eye">
    <!-- Socket Outer Crevice -->
    <circle cx="{rx}" cy="{ry}" r="{rr+3.5}" fill="#402C1B" opacity="0.75" />
    <circle cx="{rx}" cy="{ry}" r="{rr+1.5}" fill="#201004" />
    <!-- Amber Iris -->
    <circle cx="{rx}" cy="{ry}" r="{rr}" fill="url(#amberEyeR)" />
    <!-- Pupil -->
    <circle cx="{rpx}" cy="{rpy}" r="{rpr}" fill="url(#pupilGrad)" />
    <!-- Specular Glints -->
    <ellipse cx="{rx-5}" cy="{ly-6}" rx="3.5" ry="2.5" fill="#FFFFFF" opacity="0.95" />
    <circle cx="{rx+7}" cy="{ry+6}" r="1.8" fill="#FFFFFF" opacity="0.55" />
  </g>

  <!-- 4. Beak (Porcelain Amber) -->
  <g id="beak">
    <path d="M 256 168 C 267 184, 268 206, 256 218 C 244 206, 245 184, 256 168 Z" fill="url(#beakGrad)" stroke="#4A3220" stroke-width="1.2" />
    <!-- Beak Ridge Highlight -->
    <path d="M 256 172 C 259 184, 259 200, 256 212" stroke="#FFFFFF" stroke-width="1.2" stroke-linecap="round" opacity="0.45" fill="none" />
  </g>

  <!-- 5. Grounded Feet with 3 Rounded Toes (Resting Y in [450, 492]) -->
  <g id="feet">
    <!-- Left Foot -->
    <g id="left_foot">
      <!-- Outer Toe 1 -->
      <path d="M 158 472 C 158 460, 180 460, 182 472 L 183 490 L 158 490 Z" fill="url(#toeGradL)" />
      <!-- Middle Toe 2 -->
      <path d="M 181 462 C 181 448, 207 448, 208 462 L 209 491 L 181 491 Z" fill="url(#toeGradL)" />
      <!-- Inner Toe 3 -->
      <path d="M 207 468 C 207 456, 233 456, 234 468 L 235 490 L 207 490 Z" fill="url(#toeGradL)" />

      <!-- Toe Crevices (Ambient Shadows) -->
      <path d="M 181 464 L 182 490" stroke="#25170B" stroke-width="2.5" stroke-linecap="round" />
      <path d="M 207 466 L 208 490" stroke="#25170B" stroke-width="2.5" stroke-linecap="round" />

      <!-- Toe Highlights -->
      <ellipse cx="170" cy="466" rx="6" ry="2.5" fill="#FFFFFF" opacity="0.35" />
      <ellipse cx="195" cy="456" rx="7" ry="2.5" fill="#FFFFFF" opacity="0.40" />
      <ellipse cx="220" cy="464" rx="6" ry="2.5" fill="#FFFFFF" opacity="0.35" />

      <!-- Ground Contact Occlusion -->
      <path d="M 156 489 L 236 489" stroke="#120903" stroke-width="2" opacity="0.85" />
    </g>

    <!-- Right Foot -->
    <g id="right_foot">
      <!-- Inner Toe 1 -->
      <path d="M 276 468 C 276 456, 303 456, 303 468 L 304 490 L 276 490 Z" fill="url(#toeGradR)" />
      <!-- Middle Toe 2 -->
      <path d="M 302 462 C 302 448, 329 448, 329 462 L 330 491 L 302 491 Z" fill="url(#toeGradR)" />
      <!-- Outer Toe 3 -->
      <path d="M 328 472 C 328 460, 352 460, 352 472 L 353 490 L 328 490 Z" fill="url(#toeGradR)" />

      <!-- Toe Crevices (Ambient Shadows) -->
      <path d="M 303 466 L 303 490" stroke="#25170B" stroke-width="2.5" stroke-linecap="round" />
      <path d="M 329 466 L 329 490" stroke="#25170B" stroke-width="2.5" stroke-linecap="round" />

      <!-- Toe Highlights -->
      <ellipse cx="290" cy="464" rx="6" ry="2.5" fill="#FFFFFF" opacity="0.35" />
      <ellipse cx="316" cy="456" rx="7" ry="2.5" fill="#FFFFFF" opacity="0.40" />
      <ellipse cx="340" cy="466" rx="6" ry="2.5" fill="#FFFFFF" opacity="0.35" />

      <!-- Ground Contact Occlusion -->
      <path d="M 275 489 L 354 489" stroke="#120903" stroke-width="2" opacity="0.85" />
    </g>
  </g>
</svg>"""
    return svg

# Test render
svg_content = build_svg({})
test_svg_path = "scratch/test_model_v1.svg"
with open(test_svg_path, "w") as f:
    f.write(svg_content)

out_png = render_svg(test_svg_path, "scratch/test_model_v1.png")
res = evaluate_fidelity(out_png)
