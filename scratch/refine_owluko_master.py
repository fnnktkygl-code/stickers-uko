import os, sys, re, cv2, numpy as np
from PIL import Image
from scripts.benchmark_owluko_fidelity import render_svg, evaluate_fidelity

with open("scratch/owluko_exact_silhouette.txt", "r") as f:
    sil_d = f.read().strip()

def build_owluko_svg(
    body_x1=28, body_y1=8, body_x2=68, body_y2=92,
    # Body stops
    c0="#FFF7ED", c1="#F8ECE0", c2="#ECDCCE", c3="#CFBCAB", c4="#A6917E", c5="#735E4E",
    # Cranial
    cranial_cx=44, cranial_cy=18, cranial_r=42, cranial_op=0.45,
    # Chest
    chest_cx=46, chest_cy=52, chest_r=38, chest_op=0.25,
    # Flanks
    l_wing_op=0.35, r_wing_op=0.45,
    # Beak
    beak_color="#E0CDBC", beak_shadow="#A68D77",
    # Eyes
    iris_l_c0="#FFE066", iris_l_c1="#E5A625", iris_l_c2="#8C4E0A", iris_l_c3="#2A1404",
    iris_r_c0="#F5D050", iris_r_c1="#CF901E", iris_r_c2="#7B4208", iris_r_c3="#200E02"
):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" style="background: transparent;">
  <defs>
    <!-- Master Body Silhouette Clip -->
    <clipPath id="bodyClip">
      <path d="{sil_d}" />
    </clipPath>

    <!-- 1. Master Porcelain Body Gradient -->
    <linearGradient id="bodyGrad" x1="{body_x1}%" y1="{body_y1}%" x2="{body_x2}%" y2="{body_y2}%">
      <stop offset="0%" stop-color="{c0}" />
      <stop offset="18%" stop-color="{c1}" />
      <stop offset="40%" stop-color="{c2}" />
      <stop offset="65%" stop-color="{c3}" />
      <stop offset="85%" stop-color="{c4}" />
      <stop offset="100%" stop-color="{c5}" />
    </linearGradient>

    <!-- Cranial Dome Specular Highlight -->
    <radialGradient id="cranialHl" cx="{cranial_cx}%" cy="{cranial_cy}%" r="{cranial_r}%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="{cranial_op}" />
      <stop offset="50%" stop-color="#FDF8F3" stop-opacity="{cranial_op * 0.4}" />
      <stop offset="100%" stop-color="#EEDFD3" stop-opacity="0" />
    </radialGradient>

    <!-- Chest Soft Illumination -->
    <radialGradient id="chestHl" cx="{chest_cx}%" cy="{chest_cy}%" r="{chest_r}%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="{chest_op}" />
      <stop offset="55%" stop-color="#F5ECE3" stop-opacity="{chest_op * 0.35}" />
      <stop offset="100%" stop-color="#DECFC2" stop-opacity="0" />
    </radialGradient>

    <!-- Left Wing Rim & Lateral Highlight -->
    <linearGradient id="lWingGrad" x1="0%" y1="20%" x2="100%" y2="80%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="{l_wing_op}" />
      <stop offset="40%" stop-color="#F5ECE2" stop-opacity="{l_wing_op * 0.4}" />
      <stop offset="100%" stop-color="#D9C7B6" stop-opacity="0" />
    </linearGradient>

    <!-- Right Flank Ambient Shadow -->
    <linearGradient id="rWingShadow" x1="0%" y1="20%" x2="100%" y2="80%">
      <stop offset="0%" stop-color="#C5B2A0" stop-opacity="0.05" />
      <stop offset="50%" stop-color="#9C8572" stop-opacity="{r_wing_op * 0.6}" />
      <stop offset="100%" stop-color="#695342" stop-opacity="{r_wing_op}" />
    </linearGradient>

    <!-- Facial Disc Concavity Left -->
    <radialGradient id="faceDiscL" cx="48%" cy="48%" r="52%">
      <stop offset="0%" stop-color="#F5ECE3" stop-opacity="0" />
      <stop offset="65%" stop-color="#DECAC0" stop-opacity="0.25" />
      <stop offset="100%" stop-color="#B89F90" stop-opacity="0.45" />
    </radialGradient>

    <!-- Facial Disc Concavity Right -->
    <radialGradient id="faceDiscR" cx="48%" cy="48%" r="52%">
      <stop offset="0%" stop-color="#E8DDD3" stop-opacity="0" />
      <stop offset="65%" stop-color="#CBB5A8" stop-opacity="0.30" />
      <stop offset="100%" stop-color="#9E8474" stop-opacity="0.55" />
    </radialGradient>

    <!-- Left Amber Iris -->
    <radialGradient id="amberEyeL" cx="30%" cy="80%" r="75%">
      <stop offset="0%" stop-color="{iris_l_c0}" />
      <stop offset="28%" stop-color="{iris_l_c1}" />
      <stop offset="65%" stop-color="{iris_l_c2}" />
      <stop offset="100%" stop-color="{iris_l_c3}" />
    </radialGradient>

    <!-- Right Amber Iris -->
    <radialGradient id="amberEyeR" cx="70%" cy="80%" r="75%">
      <stop offset="0%" stop-color="{iris_r_c0}" />
      <stop offset="28%" stop-color="{iris_r_c1}" />
      <stop offset="65%" stop-color="{iris_r_c2}" />
      <stop offset="100%" stop-color="{iris_r_c3}" />
    </radialGradient>

    <!-- Pupil -->
    <radialGradient id="pupilGrad" cx="45%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#120701" />
      <stop offset="70%" stop-color="#301604" />
      <stop offset="100%" stop-color="#552C0C" />
    </radialGradient>

    <!-- Eyelid Shading Left -->
    <linearGradient id="eyelidL" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#FFF8F2" />
      <stop offset="60%" stop-color="#F2E4D6" />
      <stop offset="90%" stop-color="#DFCAC0" />
      <stop offset="100%" stop-color="#593412" />
    </linearGradient>

    <!-- Eyelid Shading Right -->
    <linearGradient id="eyelidR" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#F7EEE5" />
      <stop offset="60%" stop-color="#E8D7C8" />
      <stop offset="90%" stop-color="#CFB8AC" />
      <stop offset="100%" stop-color="#4C2A0E" />
    </linearGradient>

    <!-- Eyelid Cast Shadow -->
    <linearGradient id="eyeShadow" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#1A0A02" stop-opacity="0.85" />
      <stop offset="50%" stop-color="#3D1C05" stop-opacity="0.45" />
      <stop offset="100%" stop-color="#803D08" stop-opacity="0" />
    </linearGradient>

    <!-- Beak Linear Gradient -->
    <linearGradient id="beakGrad" x1="40%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#F2E5D7" />
      <stop offset="40%" stop-color="{beak_color}" />
      <stop offset="100%" stop-color="{beak_shadow}" />
    </linearGradient>

    <!-- Feet Gradients -->
    <linearGradient id="lFootGrad" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#C5AF9B" />
      <stop offset="50%" stop-color="#9C8470" />
      <stop offset="100%" stop-color="#584332" />
    </linearGradient>

    <linearGradient id="rFootGrad" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#A8927F" />
      <stop offset="50%" stop-color="#846D5B" />
      <stop offset="100%" stop-color="#463425" />
    </linearGradient>
  </defs>

  <!-- 1. Base Silhouette Capsule -->
  <path d="{sil_d}" fill="url(#bodyGrad)" />

  <!-- 2. Clipped Body 3D Volume Layers -->
  <g clip-path="url(#bodyClip)">
    <!-- Cranial Specular Dome -->
    <ellipse cx="248" cy="98" rx="145" ry="80" fill="url(#cranialHl)" />

    <!-- Breast / Chest Soft Illumination -->
    <ellipse cx="244" cy="270" rx="112" ry="85" fill="url(#chestHl)" />

    <!-- Left Wing Lateral Highlight -->
    <path d="M 88 180 C 88 180, 115 190, 118 270 C 120 340, 95 380, 95 380 C 86 340, 86 230, 88 180 Z" fill="url(#lWingGrad)" />
    <!-- Left Wing Furrow / Separation Line -->
    <path d="M 125 185 C 135 225, 138 280, 130 355 C 128 370, 122 385, 118 395" stroke="#B8A492" stroke-width="3" stroke-linecap="round" opacity="0.35" fill="none" />

    <!-- Right Flank Ambient Occlusion -->
    <path d="M 330 180 C 375 210, 424 265, 420 345 C 416 385, 375 420, 345 425 C 380 395, 385 300, 345 200 Z" fill="url(#rWingShadow)" />
    <!-- Right Wing Furrow -->
    <path d="M 368 185 C 362 225, 362 280, 368 355 C 370 370, 375 385, 380 395" stroke="#66503E" stroke-width="3.5" stroke-linecap="round" opacity="0.45" fill="none" />

    <!-- Belly Bottom Shadow -->
    <ellipse cx="256" cy="442" rx="65" ry="18" fill="#584332" opacity="0.40" />

    <!-- Feet 3D Modeling (Clipped within body silhouette) -->
    <!-- Left Leg Stem -->
    <path d="M 190 438 C 190 438, 192 455, 185 464 C 180 470, 175 470, 160 488 L 230 488 C 220 468, 218 455, 218 438 Z" fill="url(#lFootGrad)" />
    <!-- Left Toe Knuckles / Highlights -->
    <ellipse cx="168" cy="478" rx="8" ry="4" fill="#FFFFFF" opacity="0.18" />
    <ellipse cx="196" cy="472" rx="9" ry="5" fill="#FFFFFF" opacity="0.22" />
    <ellipse cx="222" cy="477" rx="8" ry="4" fill="#FFFFFF" opacity="0.16" />
    <!-- Left Toe Crevices -->
    <path d="M 180 464 L 180 489" stroke="#463222" stroke-width="2.5" stroke-linecap="round" />
    <path d="M 208 464 L 208 489" stroke="#463222" stroke-width="2.5" stroke-linecap="round" />

    <!-- Right Leg Stem -->
    <path d="M 296 438 C 296 438, 296 455, 290 464 C 285 470, 280 470, 280 488 L 354 488 C 342 468, 324 455, 324 438 Z" fill="url(#rFootGrad)" />
    <!-- Right Toe Knuckles -->
    <ellipse cx="292" cy="477" rx="8" ry="4" fill="#FFFFFF" opacity="0.10" />
    <ellipse cx="316" cy="472" rx="9" ry="5" fill="#FFFFFF" opacity="0.12" />
    <ellipse cx="342" cy="477" rx="8" ry="4" fill="#FFFFFF" opacity="0.08" />
    <!-- Right Toe Crevices -->
    <path d="M 304 464 L 304 489" stroke="#322216" stroke-width="2.5" stroke-linecap="round" />
    <path d="M 330 464 L 330 489" stroke="#322216" stroke-width="2.5" stroke-linecap="round" />

    <!-- Ground Contact Occlusion Baseline Y=489 -->
    <line x1="155" y1="489" x2="234" y2="489" stroke="#25170D" stroke-width="3" />
    <line x1="280" y1="489" x2="356" y2="489" stroke="#1D1108" stroke-width="3" />
  </g>

  <!-- 3. Facial Mask & Orbital Depressions -->
  <!-- Left Facial Disc (Orbital Concavity) -->
  <ellipse cx="196" cy="158" rx="46" ry="40" fill="url(#faceDiscL)" />
  <!-- Right Facial Disc -->
  <ellipse cx="312" cy="158" rx="46" ry="40" fill="url(#faceDiscR)" />

  <!-- Nose Bridge Highlight between facial discs -->
  <ellipse cx="254" cy="148" rx="10" ry="24" fill="#FFFFFF" opacity="0.30" />

  <!-- 4. Sleepy Hooded Glassy Amber Eyes -->
  <!-- Left Eye -->
  <g id="left_eye">
    <!-- Socket Rim Ambient Shadow -->
    <ellipse cx="195" cy="158" rx="31" ry="25" fill="#422C19" opacity="0.45" />
    <!-- Deep Socket Bed -->
    <path d="M 168 141 C 167 165, 177 178, 195 178 C 213 178, 223 165, 222 143 C 205 141, 185 140, 168 141 Z" fill="#1C0C02" />
    <!-- Amber Iris (Half-Moon Lower Aperture) -->
    <path d="M 169 142 C 168 164, 178 177, 195 177 C 212 177, 221 164, 220 144 C 205 141, 185 141, 169 142 Z" fill="url(#amberEyeL)" />
    <!-- Pupil centered in lower iris -->
    <ellipse cx="195" cy="158" rx="14" ry="11" fill="url(#pupilGrad)" />
    <!-- Golden Amber Inner Glow Arc at bottom of iris -->
    <path d="M 178 168 C 185 175, 205 175, 212 168" stroke="#FFDE66" stroke-width="2" stroke-linecap="round" opacity="0.75" fill="none" />
    <!-- Eyelid Cast Shadow on eyeball -->
    <path d="M 169 142 C 185 141, 205 141, 220 144 L 220 152 C 205 150, 185 149, 169 150 Z" fill="url(#eyeShadow)" />
    <!-- Specular Reflection Glint (Top-left of exposed iris) -->
    <circle cx="180" cy="164" r="3.2" fill="#FFEBB0" opacity="0.95" />
    <circle cx="180" cy="164" r="5.5" fill="#FFFFFF" opacity="0.35" />
    <!-- Porcelain Upper Eyelid Hood -->
    <path d="M 166 141 C 172 118, 218 118, 224 143 C 205 144, 185 143, 166 141 Z" fill="url(#eyelidL)" />
    <!-- Eyelid Crevice Line -->
    <path d="M 167 141 C 185 143, 205 143, 224 144" stroke="#4A2B11" stroke-width="1.2" stroke-linecap="round" fill="none" />
  </g>

  <!-- Right Eye -->
  <g id="right_eye">
    <!-- Socket Rim Ambient Shadow -->
    <ellipse cx="312" cy="158" rx="31" ry="25" fill="#321D0E" opacity="0.55" />
    <!-- Deep Socket Bed -->
    <path d="M 285 143 C 284 165, 294 178, 312 178 C 330 178, 339 165, 338 141 C 322 140, 302 141, 285 143 Z" fill="#150801" />
    <!-- Amber Iris -->
    <path d="M 286 144 C 285 164, 295 177, 312 177 C 329 177, 337 164, 336 142 C 322 141, 302 141, 286 144 Z" fill="url(#amberEyeR)" />
    <!-- Pupil centered in lower iris -->
    <ellipse cx="312" cy="158" rx="14" ry="11" fill="url(#pupilGrad)" />
    <!-- Golden Amber Inner Glow Arc -->
    <path d="M 296 168 C 303 175, 321 175, 328 168" stroke="#FFCE48" stroke-width="2" stroke-linecap="round" opacity="0.65" fill="none" />
    <!-- Eyelid Cast Shadow -->
    <path d="M 286 144 C 302 141, 322 141, 336 142 L 336 150 C 322 149, 302 150, 286 152 Z" fill="url(#eyeShadow)" />
    <!-- Specular Reflection Glint -->
    <circle cx="298" cy="164" r="2.8" fill="#FFE299" opacity="0.85" />
    <circle cx="298" cy="164" r="5.0" fill="#FFFFFF" opacity="0.25" />
    <!-- Porcelain Upper Eyelid Hood -->
    <path d="M 284 144 C 290 118, 334 118, 340 141 C 322 143, 302 144, 284 144 Z" fill="url(#eyelidR)" />
    <!-- Eyelid Crevice Line -->
    <path d="M 284 144 C 302 143, 322 143, 340 141" stroke="#3D200A" stroke-width="1.2" stroke-linecap="round" fill="none" />
  </g>

  <!-- 5. Seamless Porcelain Beak Droplet -->
  <g id="beak">
    <!-- Cast Shadow beneath beak tip onto breast -->
    <ellipse cx="254" cy="214" rx="12" ry="6" fill="#80624D" opacity="0.38" />
    <!-- Beak Body Teardrop/Cone -->
    <path d="M 254 164 C 265 176, 267 196, 254 209 C 241 196, 243 176, 254 164 Z" fill="url(#beakGrad)" stroke="#B39B86" stroke-width="0.8" />
    <!-- Beak Longitudinal Highlight Ridge -->
    <path d="M 254 166 C 256 178, 256 195, 254 206" stroke="#FFFFFF" stroke-width="1.0" stroke-linecap="round" opacity="0.45" fill="none" />
  </g>
</svg>"""
    return svg

if __name__ == "__main__":
    svg = build_owluko_svg()
    with open("scratch/test_owluko_master_v1.svg", "w") as f:
        f.write(svg)
    png = render_svg("scratch/test_owluko_master_v1.svg", "scratch/test_owluko_master_v1.png")
    evaluate_fidelity(png, out_board_path="scratch/owluko_fidelity_audit_v1.png", title="OWLUKO MASTER V1 DEEP RECONSTRUCTION")
