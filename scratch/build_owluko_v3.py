import sys
sys.path.append(".")
import cv2, numpy as np
from PIL import Image
from scripts.benchmark_owluko_fidelity import render_svg, evaluate_fidelity
from scratch.calibrate_face import eval_face_svg
from scratch.test_feet import eval_feet_svg

with open("scratch/owluko_exact_silhouette.txt", "r") as f:
    sil_d = f.read().strip()

def build_v3_svg():
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" style="background: transparent;">
  <defs>
    <!-- Master Body Silhouette Clip -->
    <clipPath id="bodyClip">
      <path d="{sil_d}" />
    </clipPath>

    <!-- Master Porcelain Body Gradient (Key light from upper-left) -->
    <linearGradient id="bodyGrad" x1="26%" y1="5%" x2="74%" y2="95%">
      <stop offset="0%" stop-color="#FFF8F0" />
      <stop offset="16%" stop-color="#F9EEE2" />
      <stop offset="36%" stop-color="#ECDDD0" />
      <stop offset="60%" stop-color="#D5C1AF" />
      <stop offset="82%" stop-color="#AA9583" />
      <stop offset="100%" stop-color="#705C4C" />
    </linearGradient>

    <!-- Cranial Dome Specular Highlight -->
    <radialGradient id="cranialHl" cx="44%" cy="18%" r="44%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.48" />
      <stop offset="48%" stop-color="#FBF4ED" stop-opacity="0.20" />
      <stop offset="100%" stop-color="#ECE0D4" stop-opacity="0" />
    </radialGradient>

    <!-- Breast / Chest Soft Illumination -->
    <radialGradient id="chestHl" cx="44%" cy="50%" r="42%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.26" />
      <stop offset="50%" stop-color="#F8EFE7" stop-opacity="0.10" />
      <stop offset="100%" stop-color="#E2D4C6" stop-opacity="0" />
    </radialGradient>

    <!-- Left Wing Lateral Highlight -->
    <linearGradient id="lWingGrad" x1="0%" y1="20%" x2="100%" y2="80%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.32" />
      <stop offset="40%" stop-color="#F8EFE5" stop-opacity="0.14" />
      <stop offset="100%" stop-color="#DECFC0" stop-opacity="0" />
    </linearGradient>

    <!-- Right Flank Ambient Shadow -->
    <linearGradient id="rWingShadow" x1="0%" y1="20%" x2="100%" y2="80%">
      <stop offset="0%" stop-color="#D4C2B0" stop-opacity="0.0" />
      <stop offset="45%" stop-color="#A8927E" stop-opacity="0.28" />
      <stop offset="100%" stop-color="#6B5442" stop-opacity="0.60" />
    </linearGradient>

    <!-- Left Amber Iris (Glowing Translucent Honey Amber) -->
    <radialGradient id="amberEyeL" cx="34%" cy="76%" r="72%">
      <stop offset="0%" stop-color="#FFE875" />
      <stop offset="25%" stop-color="#F2B52E" />
      <stop offset="55%" stop-color="#A8620D" />
      <stop offset="85%" stop-color="#451E04" />
      <stop offset="100%" stop-color="#1C0A01" />
    </radialGradient>

    <!-- Right Amber Iris -->
    <radialGradient id="amberEyeR" cx="66%" cy="76%" r="72%">
      <stop offset="0%" stop-color="#FCDA60" />
      <stop offset="25%" stop-color="#DEA124" />
      <stop offset="55%" stop-color="#96520A" />
      <stop offset="85%" stop-color="#3A1803" />
      <stop offset="100%" stop-color="#160801" />
    </radialGradient>

    <!-- Pupil -->
    <radialGradient id="pupilGrad" cx="45%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#150802" />
      <stop offset="65%" stop-color="#381B05" />
      <stop offset="100%" stop-color="#5E310E" />
    </radialGradient>

    <!-- Left Porcelain Eyelid Hood -->
    <linearGradient id="eyelidHoodL" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#FFF9F4" />
      <stop offset="55%" stop-color="#F4E7DC" />
      <stop offset="85%" stop-color="#DCBEA8" />
      <stop offset="100%" stop-color="#6E421B" />
    </linearGradient>

    <!-- Right Porcelain Eyelid Hood (In soft warm shadow) -->
    <linearGradient id="eyelidHoodR" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#EFE0D2" />
      <stop offset="55%" stop-color="#DCBEAA" />
      <stop offset="85%" stop-color="#BF9E88" />
      <stop offset="100%" stop-color="#5E3615" />
    </linearGradient>

    <!-- Eyelid Cast Shadow on Eyeball -->
    <linearGradient id="eyeShadow" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#120601" stop-opacity="0.75" />
      <stop offset="60%" stop-color="#3A1A04" stop-opacity="0.40" />
      <stop offset="100%" stop-color="#7C3B07" stop-opacity="0" />
    </linearGradient>

    <!-- Seamless Porcelain Beak Gradient -->
    <linearGradient id="beakGrad" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#F2E4D6" />
      <stop offset="35%" stop-color="#D7BFAF" />
      <stop offset="70%" stop-color="#A88E77" />
      <stop offset="100%" stop-color="#78604C" />
    </linearGradient>

    <!-- Individual Toe Gradients -->
    <!-- Left Foot Toes -->
    <linearGradient id="lToe1" x1="20%" y1="0%" x2="80%" y2="100%">
      <stop offset="0%" stop-color="#D9C7B6" />
      <stop offset="50%" stop-color="#A5907D" />
      <stop offset="100%" stop-color="#5C4736" />
    </linearGradient>
    <linearGradient id="lToe2" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#E8DBD0" />
      <stop offset="50%" stop-color="#B29E8C" />
      <stop offset="100%" stop-color="#644E3C" />
    </linearGradient>
    <linearGradient id="lToe3" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#CEBEAE" />
      <stop offset="50%" stop-color="#9C8775" />
      <stop offset="100%" stop-color="#564232" />
    </linearGradient>

    <!-- Right Foot Toes -->
    <linearGradient id="rToe1" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#BCA794" />
      <stop offset="50%" stop-color="#8F7A68" />
      <stop offset="100%" stop-color="#4C3A2A" />
    </linearGradient>
    <linearGradient id="rToe2" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#C7B3A1" />
      <stop offset="50%" stop-color="#988472" />
      <stop offset="100%" stop-color="#523F2E" />
    </linearGradient>
    <linearGradient id="rToe3" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#B39E8C" />
      <stop offset="50%" stop-color="#867261" />
      <stop offset="100%" stop-color="#463426" />
    </linearGradient>
  </defs>

  <!-- 1. Master Base Silhouette Capsule -->
  <path d="{sil_d}" fill="url(#bodyGrad)" />

  <!-- 2. Clipped Body 3D Volume Layers -->
  <g clip-path="url(#bodyClip)">
    <!-- Cranial Specular Dome -->
    <ellipse cx="248" cy="96" rx="145" ry="80" fill="url(#cranialHl)" />

    <!-- Breast / Chest Soft Illumination -->
    <ellipse cx="244" cy="270" rx="115" ry="88" fill="url(#chestHl)" />

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
    <!-- Left Leg Ankle & Stem -->
    <path d="M 191 435 C 191 445, 185 455, 180 462 L 225 462 C 220 455, 218 445, 221 435 Z" fill="url(#lToe2)" />
    <!-- Left Foot 3 Bulbous Toes -->
    <!-- Toe 1 Outer -->
    <path d="M 155 479 L 157 485 L 160 488 L 169 489 L 176 485 L 180 485 L 178 462 L 171 464 L 162 466 L 158 470 Z" fill="url(#lToe1)" />
    <!-- Toe 2 Middle -->
    <path d="M 180 485 L 186 489 L 198 489 L 206 485 L 208 456 L 195 452 L 185 457 L 178 462 Z" fill="url(#lToe2)" />
    <!-- Toe 3 Inner -->
    <path d="M 206 485 L 214 485 L 220 489 L 228 488 L 231 486 L 233 482 L 231 469 L 227 465 L 219 458 L 208 460 Z" fill="url(#lToe3)" />
    <!-- Left Toe Knuckles / Highlights -->
    <ellipse cx="168" cy="477" rx="6" ry="3.5" fill="#FFFFFF" opacity="0.22" />
    <ellipse cx="196" cy="470" rx="7" ry="4" fill="#FFFFFF" opacity="0.26" />
    <ellipse cx="221" cy="477" rx="6" ry="3.5" fill="#FFFFFF" opacity="0.20" />
    <!-- Left Toe Crevices -->
    <path d="M 179 462 C 179 472, 178 482, 178 488" stroke="#3D2919" stroke-width="2.5" stroke-linecap="round" />
    <path d="M 208 460 C 208 470, 209 480, 209 488" stroke="#3D2919" stroke-width="2.5" stroke-linecap="round" />
    <!-- Left Foot Contact Baseline Shadows -->
    <ellipse cx="165" cy="488" rx="8" ry="2.0" fill="#1C1006" opacity="0.80" />
    <ellipse cx="196" cy="489" rx="12" ry="2.5" fill="#1C1006" opacity="0.90" />
    <ellipse cx="225" cy="488" rx="8" ry="2.0" fill="#1C1006" opacity="0.80" />

    <!-- Right Leg Ankle & Stem -->
    <path d="M 297 435 C 297 445, 290 455, 285 462 L 330 462 C 326 455, 323 445, 323 435 Z" fill="url(#rToe2)" />
    <!-- Right Foot 3 Bulbous Toes -->
    <!-- Toe 1 Inner -->
    <path d="M 283 470 L 280 476 L 280 484 L 283 488 L 293 489 L 300 485 L 297 455 L 290 462 Z" fill="url(#rToe1)" />
    <!-- Toe 2 Middle -->
    <path d="M 300 485 L 308 485 L 314 489 L 324 489 L 329 485 L 330 455 L 315 452 L 302 458 Z" fill="url(#rToe2)" />
    <!-- Toe 3 Outer -->
    <path d="M 329 485 L 337 485 L 340 487 L 349 488 L 352 487 L 356 483 L 356 474 L 351 466 L 338 462 L 330 460 Z" fill="url(#rToe3)" />
    <!-- Right Toe Knuckles -->
    <ellipse cx="292" cy="477" rx="6" ry="3.5" fill="#FFFFFF" opacity="0.12" />
    <ellipse cx="316" cy="470" rx="7" ry="4" fill="#FFFFFF" opacity="0.15" />
    <ellipse cx="342" cy="477" rx="6" ry="3.5" fill="#FFFFFF" opacity="0.10" />
    <!-- Right Toe Crevices -->
    <path d="M 302 462 C 302 472, 303 482, 303 488" stroke="#2D1D11" stroke-width="2.5" stroke-linecap="round" />
    <path d="M 330 462 C 330 472, 330 482, 330 488" stroke="#2D1D11" stroke-width="2.5" stroke-linecap="round" />
    <!-- Right Foot Contact Baseline Shadows -->
    <ellipse cx="292" cy="488" rx="8" ry="2.0" fill="#150C05" opacity="0.80" />
    <ellipse cx="318" cy="489" rx="12" ry="2.5" fill="#150C05" opacity="0.90" />
    <ellipse cx="345" cy="488" rx="8" ry="2.0" fill="#150C05" opacity="0.80" />
  </g>

  <!-- 3. Facial Depressions & Shading (Eliminates cyan discrepancy) -->
  <!-- Left Eye Socket Soft Shading -->
  <ellipse cx="195" cy="148" rx="42" ry="36" fill="#B39B88" opacity="0.10" />
  <!-- Right Eye Socket Warm Ambient Shadow (Shadow side) -->
  <ellipse cx="314" cy="150" rx="44" ry="38" fill="#8C7360" opacity="0.22" />
  <!-- Inner Right Orbit Wall / Right Beak Flank Shadow -->
  <ellipse cx="274" cy="160" rx="15" ry="20" fill="#826855" opacity="0.35" />
  <ellipse cx="264" cy="182" rx="12" ry="18" fill="#826855" opacity="0.30" />

  <!-- 4. Sleepy Hooded Glassy Amber Eyes -->
  <!-- Left Eye -->
  <g id="left_eye">
    <!-- Socket Rim Groove -->
    <path d="M 166 141 C 165 166, 175 180, 195 180 C 215 180, 224 166, 223 143 C 205 141, 185 140, 166 141 Z" fill="#251408" />
    <!-- Amber Iris (Half-Moon Sliced Aperture) -->
    <path d="M 167 142 C 166 164, 176 178, 195 178 C 214 178, 222 164, 221 144 C 205 141, 185 141, 167 142 Z" fill="url(#amberEyeL)" />
    <!-- Pupil centered in lower iris -->
    <ellipse cx="195" cy="161" rx="11" ry="8.5" fill="url(#pupilGrad)" />
    <!-- Golden Amber Inner Glow Arc -->
    <path d="M 176 168 C 184 176, 206 176, 214 168" stroke="#FFE275" stroke-width="2.5" stroke-linecap="round" opacity="0.80" fill="none" />
    <!-- Eyelid Cast Shadow on eyeball -->
    <path d="M 167 142 C 185 141, 205 141, 221 144 L 221 153 C 205 151, 185 150, 167 151 Z" fill="url(#eyeShadow)" />
    <!-- Specular Reflection Glint -->
    <circle cx="180" cy="164" r="3.2" fill="#FFF0C2" opacity="0.95" />
    <circle cx="180" cy="164" r="5.5" fill="#FFFFFF" opacity="0.35" />
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
    <ellipse cx="312" cy="161" rx="11" ry="8.5" fill="url(#pupilGrad)" />
    <!-- Golden Amber Inner Glow Arc -->
    <path d="M 294 168 C 302 176, 322 176, 330 168" stroke="#FCD65C" stroke-width="2.5" stroke-linecap="round" opacity="0.70" fill="none" />
    <!-- Eyelid Cast Shadow -->
    <path d="M 285 144 C 302 141, 322 141, 337 142 L 337 151 C 322 150, 302 151, 285 153 Z" fill="url(#eyeShadow)" />
    <!-- Specular Reflection Glint -->
    <circle cx="298" cy="164" r="2.8" fill="#FFE8AA" opacity="0.85" />
    <circle cx="298" cy="164" r="5.0" fill="#FFFFFF" opacity="0.25" />
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
    svg = build_v3_svg()
    with open("scratch/test_owluko_master_v3.svg", "w") as f:
        f.write(svg)
    png = render_svg("scratch/test_owluko_master_v3.svg", "scratch/test_owluko_master_v3.png")
    evaluate_fidelity(png, out_board_path="scratch/owluko_fidelity_audit_v3.png", title="OWLUKO MASTER V3 DEEP OPTIMIZATION")
    eval_face_svg("scratch/test_owluko_master_v3.svg")
    eval_feet_svg("scratch/test_owluko_master_v3.svg")
