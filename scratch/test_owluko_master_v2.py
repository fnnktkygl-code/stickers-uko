import sys
sys.path.append(".")
import cv2, numpy as np
from PIL import Image
from scripts.benchmark_owluko_fidelity import render_svg, evaluate_fidelity
from scratch.calibrate_face import eval_face_svg

with open("scratch/owluko_exact_silhouette.txt", "r") as f:
    sil_d = f.read().strip()

def build_v2_svg():
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" style="background: transparent;">
  <defs>
    <!-- Master Body Silhouette Clip -->
    <clipPath id="bodyClip">
      <path d="{sil_d}" />
    </clipPath>

    <!-- Master Porcelain Body Gradient (Warm studio key light from upper left) -->
    <linearGradient id="bodyGrad" x1="28%" y1="6%" x2="72%" y2="94%">
      <stop offset="0%" stop-color="#FFF9F2" />
      <stop offset="18%" stop-color="#FBF0E4" />
      <stop offset="38%" stop-color="#EFE0D2" />
      <stop offset="62%" stop-color="#D7C3B2" />
      <stop offset="82%" stop-color="#AF9A88" />
      <stop offset="100%" stop-color="#735F4F" />
    </linearGradient>

    <!-- Cranial Dome Specular Highlight -->
    <radialGradient id="cranialHl" cx="44%" cy="18%" r="42%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.45" />
      <stop offset="50%" stop-color="#FCF6EF" stop-opacity="0.18" />
      <stop offset="100%" stop-color="#EDE0D4" stop-opacity="0" />
    </radialGradient>

    <!-- Breast / Chest Soft Illumination -->
    <radialGradient id="chestHl" cx="45%" cy="50%" r="40%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.22" />
      <stop offset="55%" stop-color="#F8EFE6" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#E2D4C6" stop-opacity="0" />
    </radialGradient>

    <!-- Left Wing Lateral Highlight -->
    <linearGradient id="lWingGrad" x1="0%" y1="20%" x2="100%" y2="80%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.30" />
      <stop offset="40%" stop-color="#F8EFE5" stop-opacity="0.12" />
      <stop offset="100%" stop-color="#DECFC0" stop-opacity="0" />
    </linearGradient>

    <!-- Right Flank Ambient Shadow -->
    <linearGradient id="rWingShadow" x1="0%" y1="20%" x2="100%" y2="80%">
      <stop offset="0%" stop-color="#D4C2B0" stop-opacity="0.0" />
      <stop offset="45%" stop-color="#A8927E" stop-opacity="0.25" />
      <stop offset="100%" stop-color="#6E5745" stop-opacity="0.55" />
    </linearGradient>

    <!-- Left Amber Iris -->
    <radialGradient id="amberEyeL" cx="30%" cy="80%" r="75%">
      <stop offset="0%" stop-color="#FFE266" />
      <stop offset="28%" stop-color="#E5A625" />
      <stop offset="65%" stop-color="#8C4E0A" />
      <stop offset="100%" stop-color="#2A1404" />
    </radialGradient>

    <!-- Right Amber Iris -->
    <radialGradient id="amberEyeR" cx="70%" cy="80%" r="75%">
      <stop offset="0%" stop-color="#F7D452" />
      <stop offset="28%" stop-color="#CF901E" />
      <stop offset="65%" stop-color="#7B4208" />
      <stop offset="100%" stop-color="#200E02" />
    </radialGradient>

    <!-- Pupil -->
    <radialGradient id="pupilGrad" cx="45%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#120701" />
      <stop offset="70%" stop-color="#301604" />
      <stop offset="100%" stop-color="#552C0C" />
    </radialGradient>

    <!-- Left Porcelain Eyelid Hood -->
    <linearGradient id="eyelidHoodL" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#FFF8F2" />
      <stop offset="60%" stop-color="#F4E8DC" />
      <stop offset="85%" stop-color="#E2D0C0" />
      <stop offset="100%" stop-color="#7A4C22" />
    </linearGradient>

    <!-- Right Porcelain Eyelid Hood -->
    <linearGradient id="eyelidHoodR" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#FBF2E8" />
      <stop offset="60%" stop-color="#EADCCE" />
      <stop offset="85%" stop-color="#D4C0B0" />
      <stop offset="100%" stop-color="#6B3F1B" />
    </linearGradient>

    <!-- Eyelid Cast Shadow on Eyeball -->
    <linearGradient id="eyeShadow" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#150801" stop-opacity="0.90" />
      <stop offset="60%" stop-color="#3A1A04" stop-opacity="0.55" />
      <stop offset="100%" stop-color="#7C3B07" stop-opacity="0" />
    </linearGradient>

    <!-- Seamless Porcelain Beak Gradient -->
    <linearGradient id="beakGrad" x1="35%" y1="0%" x2="65%" y2="100%">
      <stop offset="0%" stop-color="#F4E8DC" />
      <stop offset="35%" stop-color="#D9C2AD" />
      <stop offset="75%" stop-color="#AF9680" />
      <stop offset="100%" stop-color="#806854" />
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

  <!-- 1. Master Base Silhouette Capsule -->
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
    <path d="M 125 185 C 135 225, 138 280, 130 355 C 128 370, 122 385, 118 395" stroke="#B8A492" stroke-width="2.5" stroke-linecap="round" opacity="0.30" fill="none" />

    <!-- Right Flank Ambient Occlusion -->
    <path d="M 330 180 C 375 210, 424 265, 420 345 C 416 385, 375 420, 345 425 C 380 395, 385 300, 345 200 Z" fill="url(#rWingShadow)" />
    <!-- Right Wing Furrow -->
    <path d="M 368 185 C 362 225, 362 280, 368 355 C 370 370, 375 385, 380 395" stroke="#66503E" stroke-width="3" stroke-linecap="round" opacity="0.40" fill="none" />

    <!-- Belly Bottom Shadow -->
    <ellipse cx="256" cy="442" rx="65" ry="18" fill="#584332" opacity="0.35" />

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

    <!-- Ground Contact Baseline Shadows Y=489 -->
    <line x1="155" y1="489" x2="234" y2="489" stroke="#25170D" stroke-width="3" />
    <line x1="280" y1="489" x2="356" y2="489" stroke="#1D1108" stroke-width="3" />
  </g>

  <!-- 3. Soft Facial Hollows (Delicate porcelain shading) -->
  <ellipse cx="195" cy="148" rx="42" ry="36" fill="#B39B88" opacity="0.12" />
  <ellipse cx="312" cy="148" rx="42" ry="36" fill="#8C7360" opacity="0.18" />

  <!-- 4. Sleepy Hooded Glassy Amber Eyes -->
  <!-- Left Eye -->
  <g id="left_eye">
    <!-- Socket Rim Groove -->
    <path d="M 166 141 C 165 166, 175 180, 195 180 C 215 180, 224 166, 223 143 C 205 141, 185 140, 166 141 Z" fill="#251408" />
    <!-- Amber Iris (Half-Moon Sliced Aperture) -->
    <path d="M 167 142 C 166 164, 176 178, 195 178 C 214 178, 222 164, 221 144 C 205 141, 185 141, 167 142 Z" fill="url(#amberEyeL)" />
    <!-- Pupil centered in lower iris -->
    <ellipse cx="195" cy="159" rx="14" ry="11" fill="url(#pupilGrad)" />
    <!-- Golden Amber Inner Glow Arc -->
    <path d="M 176 168 C 184 176, 206 176, 214 168" stroke="#FFDE66" stroke-width="2.5" stroke-linecap="round" opacity="0.75" fill="none" />
    <!-- Eyelid Cast Shadow on eyeball -->
    <path d="M 167 142 C 185 141, 205 141, 221 144 L 221 154 C 205 152, 185 151, 167 152 Z" fill="url(#eyeShadow)" />
    <!-- Specular Reflection Glint -->
    <circle cx="180" cy="164" r="3.0" fill="#FFEBB0" opacity="0.95" />
    <circle cx="180" cy="164" r="5.0" fill="#FFFFFF" opacity="0.30" />
    <!-- Porcelain Upper Eyelid Hood (Round Arched Dome) -->
    <path d="M 165 141 C 170 110, 219 110, 224 143 C 205 144, 185 143, 165 141 Z" fill="url(#eyelidHoodL)" />
    <path d="M 165 141 C 185 143, 205 143, 224 144" stroke="#4A2B11" stroke-width="1.2" stroke-linecap="round" fill="none" />
    <!-- Eyelid Top Crease -->
    <path d="M 170 120 C 185 114, 205 114, 220 122" stroke="#B8A494" stroke-width="1.2" stroke-linecap="round" opacity="0.40" fill="none" />
  </g>

  <!-- Right Eye -->
  <g id="right_eye">
    <!-- Socket Rim Groove -->
    <path d="M 284 143 C 283 166, 292 180, 312 180 C 332 180, 340 166, 339 141 C 322 140, 302 141, 284 143 Z" fill="#1C0D04" />
    <!-- Amber Iris -->
    <path d="M 285 144 C 284 164, 293 178, 312 178 C 331 178, 338 164, 337 142 C 322 141, 302 141, 285 144 Z" fill="url(#amberEyeR)" />
    <!-- Pupil centered in lower iris -->
    <ellipse cx="312" cy="159" rx="14" ry="11" fill="url(#pupilGrad)" />
    <!-- Golden Amber Inner Glow Arc -->
    <path d="M 294 168 C 302 176, 322 176, 330 168" stroke="#FFCE48" stroke-width="2.5" stroke-linecap="round" opacity="0.65" fill="none" />
    <!-- Eyelid Cast Shadow -->
    <path d="M 285 144 C 302 141, 322 141, 337 142 L 337 152 C 322 151, 302 152, 285 154 Z" fill="url(#eyeShadow)" />
    <!-- Specular Reflection Glint -->
    <circle cx="298" cy="164" r="2.8" fill="#FFE299" opacity="0.85" />
    <circle cx="298" cy="164" r="4.5" fill="#FFFFFF" opacity="0.25" />
    <!-- Porcelain Upper Eyelid Hood -->
    <path d="M 283 144 C 288 110, 335 110, 340 141 C 322 143, 302 144, 283 144 Z" fill="url(#eyelidHoodR)" />
    <path d="M 283 144 C 302 143, 322 143, 340 141" stroke="#3D200A" stroke-width="1.2" stroke-linecap="round" fill="none" />
    <!-- Eyelid Top Crease -->
    <path d="M 288 122 C 302 114, 322 114, 335 120" stroke="#8C7360" stroke-width="1.2" stroke-linecap="round" opacity="0.45" fill="none" />
  </g>

  <!-- 5. Seamless Rounded Porcelain Beak Droplet -->
  <g id="beak">
    <!-- Cast Shadow beneath beak tip onto breast -->
    <ellipse cx="254" cy="216" rx="14" ry="7" fill="#6E523E" opacity="0.32" />
    <!-- Beak Body Teardrop/Cone -->
    <path d="M 254 162 C 247 172, 241 185, 242 196 C 243 206, 247 215, 254 215 C 261 215, 265 206, 266 196 C 267 185, 261 172, 254 162 Z" fill="url(#beakGrad)" stroke="#B39B86" stroke-width="0.7" />
    <!-- Beak Longitudinal Highlight Ridge -->
    <path d="M 254 164 C 255 178, 255 198, 254 211" stroke="#FFFFFF" stroke-width="1.2" stroke-linecap="round" opacity="0.35" fill="none" />
  </g>
</svg>"""
    return svg

if __name__ == "__main__":
    svg = build_v2_svg()
    with open("scratch/test_owluko_master_v2.svg", "w") as f:
        f.write(svg)
    png = render_svg("scratch/test_owluko_master_v2.svg", "scratch/test_owluko_master_v2.png")
    evaluate_fidelity(png, out_board_path="scratch/owluko_fidelity_audit_v2.png", title="OWLUKO MASTER V2 REFINEMENT")
    eval_face_svg("scratch/test_owluko_master_v2.svg")
