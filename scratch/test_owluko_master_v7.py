import sys
sys.path.append(".")
import cv2, numpy as np
from PIL import Image
from scripts.benchmark_owluko_fidelity import render_svg, evaluate_fidelity
from scratch.calibrate_face import eval_face_svg
from scratch.test_feet import eval_feet_svg

with open("scratch/owluko_exact_silhouette.txt", "r") as f:
    sil_d = f.read().strip()

def build_v7_svg():
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
      <stop offset="80%" stop-color="#A5907E" />
      <stop offset="100%" stop-color="#6B5747" />
    </linearGradient>

    <!-- Cranial Dome Specular Highlight (Centered at 215, 85) -->
    <radialGradient id="cranialHl" cx="42%" cy="17%" r="35%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.45" />
      <stop offset="45%" stop-color="#FBF4ED" stop-opacity="0.18" />
      <stop offset="100%" stop-color="#ECE0D4" stop-opacity="0" />
    </radialGradient>

    <!-- Upper Right Head Shadow (Soft ambient falloff on shadow side) -->
    <radialGradient id="headRightShadow" cx="72%" cy="20%" r="45%">
      <stop offset="0%" stop-color="#7A6250" stop-opacity="0.30" />
      <stop offset="55%" stop-color="#7A6250" stop-opacity="0.14" />
      <stop offset="100%" stop-color="#7A6250" stop-opacity="0" />
    </radialGradient>

    <!-- Breast / Chest Soft Illumination -->
    <radialGradient id="chestHl" cx="44%" cy="50%" r="40%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.25" />
      <stop offset="50%" stop-color="#F8EFE7" stop-opacity="0.10" />
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
      <stop offset="45%" stop-color="#A8927E" stop-opacity="0.30" />
      <stop offset="100%" stop-color="#6B5442" stop-opacity="0.65" />
    </linearGradient>

    <!-- Left Amber Iris (Vertical Liquid Amber Gradient) -->
    <linearGradient id="amberEyeL" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#4A2406" />
      <stop offset="25%" stop-color="#552B08" />
      <stop offset="55%" stop-color="#7B4A18" />
      <stop offset="75%" stop-color="#B87B2E" />
      <stop offset="90%" stop-color="#D89B55" />
      <stop offset="100%" stop-color="#9C6A3C" />
    </linearGradient>

    <!-- Right Amber Iris (Vertical Gradient in Soft Shadow) -->
    <linearGradient id="amberEyeR" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#381803" />
      <stop offset="25%" stop-color="#462206" />
      <stop offset="55%" stop-color="#6C3E12" />
      <stop offset="75%" stop-color="#A66D24" />
      <stop offset="90%" stop-color="#C58C47" />
      <stop offset="100%" stop-color="#8C5C30" />
    </linearGradient>

    <!-- Left Porcelain Eyelid Hood -->
    <linearGradient id="eyelidHoodL" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#FFF9F4" />
      <stop offset="50%" stop-color="#F4E7DC" />
      <stop offset="80%" stop-color="#DEC4AF" />
      <stop offset="95%" stop-color="#E2BA96" />
      <stop offset="100%" stop-color="#8C562A" />
    </linearGradient>

    <!-- Right Porcelain Eyelid Hood (In soft warm shadow) -->
    <linearGradient id="eyelidHoodR" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#EFE0D2" />
      <stop offset="50%" stop-color="#DCBEAA" />
      <stop offset="80%" stop-color="#C2A28C" />
      <stop offset="95%" stop-color="#CA9E7C" />
      <stop offset="100%" stop-color="#73421A" />
    </linearGradient>

    <!-- Eyelid Cast Shadow on Eyeball -->
    <linearGradient id="eyeShadow" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#0E0401" stop-opacity="0.85" />
      <stop offset="50%" stop-color="#2D1302" stop-opacity="0.50" />
      <stop offset="100%" stop-color="#6E3406" stop-opacity="0" />
    </linearGradient>

    <!-- Seamless Porcelain Beak Gradient -->
    <linearGradient id="beakGrad" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#F2E4D6" />
      <stop offset="35%" stop-color="#D7BFAF" />
      <stop offset="70%" stop-color="#A88E77" />
      <stop offset="100%" stop-color="#78604C" />
    </linearGradient>

    <!-- Soft Under-Beak Ambient Shadow -->
    <radialGradient id="beakTipShadow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#6B503D" stop-opacity="0.45" />
      <stop offset="60%" stop-color="#6B503D" stop-opacity="0.18" />
      <stop offset="100%" stop-color="#6B503D" stop-opacity="0" />
    </radialGradient>

    <!-- Soft Right Orbit Shadow -->
    <radialGradient id="rightOrbitShadow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#806856" stop-opacity="0.28" />
      <stop offset="65%" stop-color="#806856" stop-opacity="0.10" />
      <stop offset="100%" stop-color="#806856" stop-opacity="0" />
    </radialGradient>

    <!-- Individual Toe Gradients -->
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
    <ellipse cx="215" cy="85" rx="95" ry="65" fill="url(#cranialHl)" />

    <!-- Upper Right Head Shadow -->
    <ellipse cx="335" cy="90" rx="90" ry="70" fill="url(#headRightShadow)" />

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

    <!-- Lower Belly Shading Gradient -->
    <ellipse cx="254" cy="405" rx="85" ry="30" fill="#755F4E" opacity="0.25" />
    <ellipse cx="256" cy="442" rx="65" ry="18" fill="#523D2C" opacity="0.35" />

    <!-- Feet 3D Modeling -->
    <!-- Left Leg Ankle & Stem -->
    <path d="M 191 435 C 191 445, 185 455, 180 462 L 225 462 C 220 455, 218 445, 221 435 Z" fill="url(#lToe2)" />
    <!-- Left Foot 3 Bulbous Toes -->
    <path d="M 155 479 L 157 485 L 160 488 L 169 489 L 176 485 L 180 485 L 178 462 L 171 464 L 162 466 L 158 470 Z" fill="url(#lToe1)" />
    <path d="M 180 485 L 186 489 L 198 489 L 206 485 L 208 456 L 195 452 L 185 457 L 178 462 Z" fill="url(#lToe2)" />
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
    <path d="M 283 470 L 280 476 L 280 484 L 283 488 L 293 489 L 300 485 L 297 455 L 290 462 Z" fill="url(#rToe1)" />
    <path d="M 300 485 L 308 485 L 314 489 L 324 489 L 329 485 L 330 455 L 315 452 L 302 458 Z" fill="url(#rToe2)" />
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

  <!-- 3. Facial Depressions & Shading -->
  <!-- Inner Right Orbit Wall / Right Beak Flank Soft Shadow -->
  <ellipse cx="272" cy="165" rx="22" ry="26" fill="url(#rightOrbitShadow)" />

  <!-- 4. Sleepy Hooded Glassy Amber Eyes -->
  <!-- Left Eye -->
  <g id="left_eye">
    <!-- Amber Iris (Exact Half-Moon Aperture) -->
    <path d="M 166 142 C 168 152, 172 165, 178 172 C 184 177, 195 178, 204 176 C 213 172, 220 160, 224 147 C 215 145, 202 143, 195 142 C 185 144, 176 143, 166 142 Z" fill="url(#amberEyeL)" />
    <!-- Pupil in upper center of aperture -->
    <ellipse cx="195" cy="153" rx="8.5" ry="6.5" fill="#1C0A02" opacity="0.80" />
    <!-- Golden Amber Inner Glow Arc -->
    <path d="M 178 168 C 185 175, 202 175, 208 168" stroke="#FFE275" stroke-width="2.2" stroke-linecap="round" opacity="0.75" fill="none" />
    <!-- Eyelid Cast Shadow on eyeball -->
    <path d="M 166 142 L 176 143 L 185 144 L 195 142 L 202 143 L 215 145 L 224 147 L 223 153 L 195 149 L 166 148 Z" fill="url(#eyeShadow)" />
    <!-- Specular Reflection Glint -->
    <ellipse cx="180" cy="163" rx="3.0" ry="2.0" fill="#FFF0C2" opacity="0.95" />
    <circle cx="180" cy="163" r="1.3" fill="#FFFFFF" opacity="0.95" />
    <!-- Porcelain Upper Eyelid Hood (Round Arched Dome Covering Top Half) -->
    <path d="M 166 142 C 168 112, 220 112, 224 147 C 215 145, 202 143, 195 142 C 185 144, 176 143, 166 142 Z" fill="url(#eyelidHoodL)" />
  </g>

  <!-- Right Eye -->
  <g id="right_eye">
    <!-- Amber Iris -->
    <path d="M 284 147 C 288 160, 295 172, 304 176 C 313 178, 324 177, 330 172 C 336 165, 338 152, 340 142 C 330 143, 322 144, 312 142 C 305 143, 294 145, 284 147 Z" fill="url(#amberEyeR)" />
    <!-- Pupil -->
    <ellipse cx="312" cy="153" rx="8.5" ry="6.5" fill="#140601" opacity="0.80" />
    <!-- Golden Amber Inner Glow Arc -->
    <path d="M 296 168 C 303 175, 318 175, 324 168" stroke="#FCD65C" stroke-width="2.2" stroke-linecap="round" opacity="0.65" fill="none" />
    <!-- Eyelid Cast Shadow -->
    <path d="M 284 147 L 294 145 L 305 143 L 312 142 L 322 144 L 330 143 L 340 142 L 339 148 L 312 149 L 284 153 Z" fill="url(#eyeShadow)" />
    <!-- Specular Reflection Glint -->
    <ellipse cx="298" cy="163" rx="2.8" ry="2.0" fill="#FFE8AA" opacity="0.85" />
    <circle cx="298" cy="163" r="1.2" fill="#FFFFFF" opacity="0.90" />
    <!-- Porcelain Upper Eyelid Hood -->
    <path d="M 284 147 C 288 112, 338 112, 340 142 C 330 143, 322 144, 312 142 C 305 143, 294 145, 284 147 Z" fill="url(#eyelidHoodR)" />
  </g>

  <!-- 5. Seamless Rounded Porcelain Beak Droplet -->
  <g id="beak">
    <!-- Cast Shadow beneath beak tip onto breast -->
    <ellipse cx="254" cy="216" rx="18" ry="10" fill="url(#beakTipShadow)" />
    <!-- Beak Body Teardrop/Cone -->
    <path d="M 254 162 C 247 172, 241 185, 242 196 C 243 206, 247 215, 254 215 C 261 215, 265 206, 266 196 C 267 185, 261 172, 254 162 Z" fill="url(#beakGrad)" />
    <!-- Beak Longitudinal Highlight Ridge -->
    <path d="M 254 164 C 255 178, 255 198, 254 211" stroke="#FFFFFF" stroke-width="1.2" stroke-linecap="round" opacity="0.30" fill="none" />
  </g>
</svg>"""
    return svg

if __name__ == "__main__":
    svg = build_v7_svg()
    with open("scratch/test_owluko_master_v7.svg", "w") as f:
        f.write(svg)
    png = render_svg("scratch/test_owluko_master_v7.svg", "scratch/test_owluko_master_v7.png")
    evaluate_fidelity(png, out_board_path="scratch/owluko_fidelity_audit_v7.png", title="OWLUKO MASTER V7 TRUE PORCELAIN")
    eval_face_svg("scratch/test_owluko_master_v7.svg")
    eval_feet_svg("scratch/test_owluko_master_v7.svg")
