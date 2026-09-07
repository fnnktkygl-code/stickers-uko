import os, sys, subprocess
import cv2, numpy as np
from PIL import Image

def get_smooth_svg_path(mask, epsilon=1.0, min_area=200):
    mask_clean = cv2.morphologyEx(mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    cnts, _ = cv2.findContours(mask_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    valid = [c for c in cnts if cv2.contourArea(c) > min_area]
    if not valid:
        return ""
    c = max(valid, key=cv2.contourArea)
    approx = cv2.approxPolyDP(c, epsilon, True)
    pts = approx.reshape(-1, 2)
    n = len(pts)
    if n < 3:
        return ""
    d = [f"M {pts[0][0]} {pts[0][1]}"]
    for i in range(n):
        p_prev = pts[(i - 1) % n]
        p_curr = pts[i]
        p_next = pts[(i + 1) % n]
        p_next2 = pts[(i + 2) % n]
        c1_x = p_curr[0] + (p_next[0] - p_prev[0]) / 6.0
        c1_y = p_curr[1] + (p_next[1] - p_prev[1]) / 6.0
        c2_x = p_next[0] - (p_next2[0] - p_curr[0]) / 6.0
        c2_y = p_next[1] - (p_next2[1] - p_curr[1]) / 6.0
        d.append(f"C {c1_x:.1f} {c1_y:.1f}, {c2_x:.1f} {c2_y:.1f}, {p_next[0]} {p_next[1]}")
    d.append("Z")
    return " ".join(d)

ref = Image.open("mascots/meoweko/meoweko_master_exact_512.png").convert("RGBA")
arr = np.array(ref)
r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]

# 1. Outer full body silhouette
body_path = get_smooth_svg_path(a > 20, epsilon=0.9, min_area=5000)

# 2. Tail path
tail_mask = np.zeros_like(a, dtype=bool)
tail_mask[395:485, 115:205] = (a[395:485, 115:205] > 20) & (r[395:485, 115:205] > 120) & (b[395:485, 115:205] < 95)
tail_path = get_smooth_svg_path(tail_mask, epsilon=0.8, min_area=300)

# 3. Continuous White Fur (Face + Blaze + Cheeks + Bib + Legs + Paws)
hsv = cv2.cvtColor(arr[:, :, :3], cv2.COLOR_RGB2HSV)
h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
ginger_mask = (a > 20) & (s > 75) & (h >= 5) & (h <= 30)
white_mask = (a > 20) & ~ginger_mask
# Remove eyes from white mask
eye_dark = (v < 45) & (a > 20)
white_mask[eye_dark] = False
# Morphology to make continuous
white_mask = cv2.morphologyEx(white_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))) > 0
white_coat_path = get_smooth_svg_path(white_mask, epsilon=1.0, min_area=5000)

# 4. Inner Ear Cavities
ear_l_mask = np.zeros_like(a, dtype=bool)
ear_l_mask[55:130, 160:215] = (a[55:130, 160:215] > 20) & (r[55:130, 160:215] > 180) & (g[55:130, 160:215] < 170) & (b[55:130, 160:215] > 120)
ear_l_path = get_smooth_svg_path(ear_l_mask, epsilon=0.8, min_area=80)

ear_r_mask = np.zeros_like(a, dtype=bool)
ear_r_mask[55:130, 330:385] = (a[55:130, 330:385] > 20) & (r[55:130, 330:385] > 180) & (g[55:130, 330:385] < 170) & (b[55:130, 330:385] > 120)
ear_r_path = get_smooth_svg_path(ear_r_mask, epsilon=0.8, min_area=80)

# 5. Build High-Fidelity SVG
svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <!-- Soft filters for volumetric porcelain occlusion -->
    <filter id="softAo" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="4.0" />
    </filter>
    <filter id="deepAo" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="8.0" />
    </filter>
    <filter id="fineAo" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.0" />
    </filter>
    <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="1.5" />
    </filter>

    <!-- Ginger coat volumetric gradients -->
    <linearGradient id="gingerBodyGrad" x1="25%" y1="10%" x2="75%" y2="90%">
      <stop offset="0%" stop-color="#F9B36E" />
      <stop offset="28%" stop-color="#EC8E3E" />
      <stop offset="68%" stop-color="#D37120" />
      <stop offset="100%" stop-color="#AA4808" />
    </linearGradient>

    <linearGradient id="tailGrad" x1="15%" y1="20%" x2="85%" y2="80%">
      <stop offset="0%" stop-color="#F29F52" />
      <stop offset="45%" stop-color="#DB7825" />
      <stop offset="85%" stop-color="#B2500E" />
      <stop offset="100%" stop-color="#803004" />
    </linearGradient>

    <!-- Cream-white porcelain ceramic gradient -->
    <radialGradient id="creamCoatGrad" cx="50%" cy="28%" r="72%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="42%" stop-color="#FAF7F2" />
      <stop offset="78%" stop-color="#EFE7DB" />
      <stop offset="100%" stop-color="#DCD0BD" />
    </radialGradient>

    <!-- Left & Right Amber Irises -->
    <radialGradient id="irisL" cx="60%" cy="65%" r="58%">
      <stop offset="0%" stop-color="#FFF578" />
      <stop offset="38%" stop-color="#E5B020" />
      <stop offset="72%" stop-color="#9C680E" />
      <stop offset="100%" stop-color="#351C02" />
    </radialGradient>
    <radialGradient id="irisR" cx="40%" cy="65%" r="58%">
      <stop offset="0%" stop-color="#FFF578" />
      <stop offset="38%" stop-color="#E5B020" />
      <stop offset="72%" stop-color="#9C680E" />
      <stop offset="100%" stop-color="#351C02" />
    </radialGradient>

    <!-- Ear cavities -->
    <radialGradient id="earCavityL" cx="40%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#FDCABC" />
      <stop offset="45%" stop-color="#F7A594" />
      <stop offset="80%" stop-color="#E57D6B" />
      <stop offset="100%" stop-color="#C5503C" />
    </radialGradient>
    <radialGradient id="earCavityR" cx="60%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#FDCABC" />
      <stop offset="45%" stop-color="#F7A594" />
      <stop offset="80%" stop-color="#E57D6B" />
      <stop offset="100%" stop-color="#C5503C" />
    </radialGradient>

    <!-- Button nose -->
    <linearGradient id="noseGrad" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#F9A49A" />
      <stop offset="100%" stop-color="#E8786B" />
    </linearGradient>

    <!-- Soft porcelain chest highlight -->
    <radialGradient id="chestHighlight" cx="50%" cy="30%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.85" />
      <stop offset="60%" stop-color="#FFFFFF" stop-opacity="0.20" />
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.0" />
    </radialGradient>

    <!-- Head crown highlight -->
    <radialGradient id="crownHighlight" cx="50%" cy="20%" r="60%">
      <stop offset="0%" stop-color="#FFE0B2" stop-opacity="0.65" />
      <stop offset="70%" stop-color="#F9B36E" stop-opacity="0.0" />
    </radialGradient>
  </defs>

  <!-- 1. Tail (Behind Left Haunch) -->
  <path d="{tail_path}" fill="url(#tailGrad)" stroke="#883304" stroke-width="0.8" />

  <!-- 2. Master Outer Silhouette (Ginger Ceramic Body) -->
  <path d="{body_path}" fill="url(#gingerBodyGrad)" stroke="#883304" stroke-width="0.8" />

  <!-- Crown soft specular luster -->
  <ellipse cx="271.5" cy="85" rx="55" ry="30" fill="url(#crownHighlight)" />

  <!-- 3. Flank Ambient Occlusion & Cylindrical Shadow -->
  <ellipse cx="190" cy="425" rx="35" ry="40" fill="#7D2B03" opacity="0.32" filter="url(#deepAo)" />
  <ellipse cx="350" cy="425" rx="35" ry="40" fill="#7D2B03" opacity="0.32" filter="url(#deepAo)" />

  <!-- 4. Inner Ear Cavities -->
  <path d="{ear_l_path}" fill="url(#earCavityL)" stroke="#B64534" stroke-width="0.8" />
  <path d="{ear_r_path}" fill="url(#earCavityR)" stroke="#B64534" stroke-width="0.8" />
  <!-- Sculpted Ear Tufts -->
  <path d="M 172 98 C 178 100, 184 96, 189 92" stroke="#FAF7F2" stroke-width="1.8" stroke-linecap="round" fill="none" opacity="0.9" />
  <path d="M 170 108 C 176 110, 182 106, 187 102" stroke="#FAF7F2" stroke-width="1.8" stroke-linecap="round" fill="none" opacity="0.9" />
  <path d="M 372 98 C 366 100, 360 96, 355 92" stroke="#FAF7F2" stroke-width="1.8" stroke-linecap="round" fill="none" opacity="0.9" />
  <path d="M 374 108 C 368 110, 362 106, 357 102" stroke="#FAF7F2" stroke-width="1.8" stroke-linecap="round" fill="none" opacity="0.9" />

  <!-- 5. Forehead Tabby Markings -->
  <path d="M 271.5 73 C 275 73, 276 82, 276 98 C 276 112, 273.5 120, 271.5 120 C 269.5 120, 267 112, 267 98 C 267 82, 268 73, 271.5 73 Z" fill="#B24E0C" opacity="0.75" />
  <path d="M 243 82 C 246 81, 250 86, 252 100 C 254 114, 253 122, 251 123 C 249 124, 245 120, 243 106 C 241 94, 241 83, 243 82 Z" fill="#B24E0C" opacity="0.70" />
  <path d="M 300 82 C 302 83, 302 94, 300 106 C 298 120, 294 124, 292 123 C 290 122, 289 114, 291 100 C 293 86, 297 81, 300 82 Z" fill="#B24E0C" opacity="0.70" />

  <!-- 6. Complete White Fur Coat (Face, Cheeks, Blaze, Bib, Legs, Paws) -->
  <path d="{white_coat_path}" fill="url(#creamCoatGrad)" stroke="#C6BAA8" stroke-width="0.8" />

  <!-- Soft porcelain ambient occlusion in neck crease under chin -->
  <ellipse cx="271.5" cy="245" rx="50" ry="14" fill="#8C7A68" opacity="0.35" filter="url(#softAo)" />

  <!-- Soft porcelain ambient occlusion groove between front legs -->
  <path d="M 271.5 375 C 271.5 410, 271.5 450, 271.5 488" stroke="#8C7A68" stroke-width="3.5" stroke-linecap="round" fill="none" opacity="0.45" filter="url(#fineAo)" />

  <!-- Chest diffuse highlight -->
  <ellipse cx="271.5" cy="320" rx="38" ry="50" fill="url(#chestHighlight)" />

  <!-- 7. Paw Toe Crevices (Grounded on Y=490) -->
  <!-- Left paw toes -->
  <path d="M 233 468 C 233 478, 233 485, 233 490" stroke="#8C7A68" stroke-width="1.8" stroke-linecap="round" fill="none" opacity="0.65" />
  <path d="M 252 468 C 252 478, 252 485, 252 490" stroke="#8C7A68" stroke-width="1.8" stroke-linecap="round" fill="none" opacity="0.65" />
  <!-- Right paw toes -->
  <path d="M 291 468 C 291 478, 291 485, 291 490" stroke="#8C7A68" stroke-width="1.8" stroke-linecap="round" fill="none" opacity="0.65" />
  <path d="M 310 468 C 310 478, 310 485, 310 490" stroke="#8C7A68" stroke-width="1.8" stroke-linecap="round" fill="none" opacity="0.65" />

  <!-- 8. Glassy Amber Orb Eyes -->
  <!-- Left Eye: Center (220, 174) -->
  <g transform="translate(220, 174) rotate(-5)">
    <!-- Dark Eyeliner Socket -->
    <ellipse cx="0" cy="0" rx="27" ry="28" fill="#1C1004" />
    <!-- Glowing Amber Iris -->
    <ellipse cx="0" cy="0" rx="25.5" ry="26.5" fill="url(#irisL)" />
    <!-- Black Pupil -->
    <ellipse cx="0.5" cy="0" rx="18.5" ry="19.5" fill="#080401" />
    <!-- Crisp Primary Specular Glint -->
    <circle cx="5" cy="-7" r="7.5" fill="#FFFFFF" />
    <!-- Secondary Specular Glint -->
    <circle cx="-6" cy="11" r="3.2" fill="#FFFFFF" opacity="0.6" />
  </g>

  <!-- Right Eye: Center (320, 174) -->
  <g transform="translate(320, 174) rotate(5)">
    <!-- Dark Eyeliner Socket -->
    <ellipse cx="0" cy="0" rx="27" ry="28" fill="#1C1004" />
    <!-- Glowing Amber Iris -->
    <ellipse cx="0" cy="0" rx="25.5" ry="26.5" fill="url(#irisR)" />
    <!-- Black Pupil -->
    <ellipse cx="-0.5" cy="0" rx="18.5" ry="19.5" fill="#080401" />
    <!-- Crisp Primary Specular Glint -->
    <circle cx="5" cy="-7" r="7.5" fill="#FFFFFF" />
    <!-- Secondary Specular Glint -->
    <circle cx="-6" cy="11" r="3.2" fill="#FFFFFF" opacity="0.6" />
  </g>

  <!-- 9. Whisker Pads (Muzzle Mounds) & Soft Nose -->
  <!-- Whisker pad left & right mounds -->
  <ellipse cx="258" cy="214" rx="15" ry="12" fill="#FAF7F2" opacity="0.9" />
  <ellipse cx="285" cy="214" rx="15" ry="12" fill="#FAF7F2" opacity="0.9" />

  <!-- Button Nose -->
  <path d="M 262 196 C 266 194, 277 194, 281 196 C 285 200, 278 207, 271.5 207 C 265 207, 258 200, 262 196 Z" fill="url(#noseGrad)" stroke="#DF6E62" stroke-width="0.8" />
  <ellipse cx="271.5" cy="197" rx="3.5" ry="1.5" fill="#FFFFFF" opacity="0.6" />

  <!-- Philtrum & Mouth Line ω -->
  <path d="M 271.5 207 L 271.5 215" stroke="#7A6857" stroke-width="1.4" stroke-linecap="round" fill="none" />
  <path d="M 250 222 C 256 226, 265 224, 271.5 215 C 278 224, 287 226, 293 222" stroke="#7A6857" stroke-width="1.4" stroke-linecap="round" fill="none" />

  <!-- 10. Delicate Porcelain Feline Whiskers -->
  <!-- Left Whiskers -->
  <path d="M 248 214 C 222 213, 198 218, 180 220" stroke="#FAF7F2" stroke-width="1.4" stroke-linecap="round" fill="none" opacity="0.95" />
  <path d="M 246 220 C 220 222, 196 230, 178 236" stroke="#FAF7F2" stroke-width="1.4" stroke-linecap="round" fill="none" opacity="0.95" />
  <path d="M 247 226 C 224 233, 204 242, 190 250" stroke="#FAF7F2" stroke-width="1.2" stroke-linecap="round" fill="none" opacity="0.90" />
  
  <!-- Right Whiskers -->
  <path d="M 295 214 C 321 213, 345 218, 363 220" stroke="#FAF7F2" stroke-width="1.4" stroke-linecap="round" fill="none" opacity="0.95" />
  <path d="M 297 220 C 323 222, 347 230, 365 236" stroke="#FAF7F2" stroke-width="1.4" stroke-linecap="round" fill="none" opacity="0.95" />
  <path d="M 296 226 C 319 233, 339 242, 353 250" stroke="#FAF7F2" stroke-width="1.2" stroke-linecap="round" fill="none" opacity="0.90" />
</svg>"""

out_svg = "scratch/meoweko_vector_continuous.svg"
with open(out_svg, "w") as f:
    f.write(svg)
print(f"Saved {out_svg}")
