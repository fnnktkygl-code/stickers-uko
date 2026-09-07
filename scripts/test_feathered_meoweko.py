import cv2, numpy as np, subprocess
from PIL import Image
from scripts.benchmark_meoweko_fidelity import benchmark_svg

# Load reference
ref = Image.open("mascots/meoweko/meoweko_master_exact_512.png").convert("RGBA")
arr = np.array(ref)
r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]

from scripts.build_meoweko_vector_perfect import get_smooth_svg_path

body_path = get_smooth_svg_path(a > 20, epsilon=0.9, min_area=5000)
tail_mask = np.zeros_like(a, dtype=bool)
tail_mask[395:485, 115:205] = (a[395:485, 115:205] > 20) & (r[395:485, 115:205] > 120) & (b[395:485, 115:205] < 95)
tail_path = get_smooth_svg_path(tail_mask, epsilon=0.8, min_area=300)

hsv = cv2.cvtColor(arr[:, :, :3], cv2.COLOR_RGB2HSV)
h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
ginger_mask = (a > 20) & (s > 75) & (h >= 5) & (h <= 30)
white_mask = (a > 20) & ~ginger_mask
eye_dark = (v < 45) & (a > 20)
white_mask[eye_dark] = False
white_mask = cv2.morphologyEx(white_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))) > 0
white_coat_path = get_smooth_svg_path(white_mask, epsilon=1.0, min_area=5000)

# Inner ear paths
ear_l_mask = np.zeros_like(a, dtype=bool)
ear_l_mask[55:130, 160:215] = (a[55:130, 160:215] > 20) & (r[55:130, 160:215] > 180) & (g[55:130, 160:215] < 170) & (b[55:130, 160:215] > 120)
ear_l_path = get_smooth_svg_path(ear_l_mask, epsilon=0.8, min_area=80)

ear_r_mask = np.zeros_like(a, dtype=bool)
ear_r_mask[55:130, 330:385] = (a[55:130, 330:385] > 20) & (r[55:130, 330:385] > 180) & (g[55:130, 330:385] < 170) & (b[55:130, 330:385] > 120)
ear_r_path = get_smooth_svg_path(ear_r_mask, epsilon=0.8, min_area=80)

def generate_svg(blur_std=1.2):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <!-- Soft filters for volumetric porcelain occlusion -->
    <filter id="softAo" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="5.0" />
    </filter>
    <filter id="deepAo" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="9.0" />
    </filter>
    <filter id="fineAo" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.2" />
    </filter>
    <filter id="featherEdge" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="{blur_std}" />
    </filter>

    <!-- Clip path to keep inside silhouette -->
    <clipPath id="bodyClip">
      <path d="{body_path}" />
    </clipPath>

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
    <radialGradient id="creamCoatGrad" cx="50%" cy="26%" r="74%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="40%" stop-color="#FAF7F2" />
      <stop offset="75%" stop-color="#ECE4D6" />
      <stop offset="100%" stop-color="#DACFBD" />
    </radialGradient>

    <!-- Front Leg Cylindrical Highlights -->
    <linearGradient id="legLGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#E2D6C4" stop-opacity="0.6" />
      <stop offset="45%" stop-color="#FFFFFF" stop-opacity="0.9" />
      <stop offset="100%" stop-color="#D5C7B2" stop-opacity="0.7" />
    </linearGradient>
    <linearGradient id="legRGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#D5C7B2" stop-opacity="0.7" />
      <stop offset="55%" stop-color="#FFFFFF" stop-opacity="0.9" />
      <stop offset="100%" stop-color="#E2D6C4" stop-opacity="0.6" />
    </linearGradient>

    <!-- Amber Irises with golden bottom crescent -->
    <radialGradient id="irisL" cx="55%" cy="62%" r="56%">
      <stop offset="0%" stop-color="#FFF982" />
      <stop offset="35%" stop-color="#F3BD28" />
      <stop offset="70%" stop-color="#A56E10" />
      <stop offset="100%" stop-color="#351C02" />
    </radialGradient>
    <radialGradient id="irisR" cx="45%" cy="62%" r="56%">
      <stop offset="0%" stop-color="#FFF982" />
      <stop offset="35%" stop-color="#F3BD28" />
      <stop offset="70%" stop-color="#A56E10" />
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
      <stop offset="0%" stop-color="#ECA094" />
      <stop offset="100%" stop-color="#D77D70" />
    </linearGradient>

    <!-- Soft porcelain chest highlight -->
    <radialGradient id="chestHighlight" cx="50%" cy="30%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.85" />
      <stop offset="60%" stop-color="#FFFFFF" stop-opacity="0.20" />
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.0" />
    </radialGradient>

    <radialGradient id="crownHighlight" cx="50%" cy="20%" r="60%">
      <stop offset="0%" stop-color="#FFE2BC" stop-opacity="0.6" />
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
  <ellipse cx="188" cy="425" rx="36" ry="42" fill="#722702" opacity="0.40" filter="url(#deepAo)" />
  <ellipse cx="352" cy="425" rx="36" ry="42" fill="#722702" opacity="0.40" filter="url(#deepAo)" />

  <!-- 4. Inner Ear Cavities -->
  <path d="{ear_l_path}" fill="url(#earCavityL)" stroke="#B64534" stroke-width="0.8" />
  <path d="{ear_r_path}" fill="url(#earCavityR)" stroke="#B64534" stroke-width="0.8" />
  <!-- Sculpted Ear Tufts -->
  <path d="M 172 98 C 178 100, 184 96, 189 92" stroke="#FAF7F2" stroke-width="1.8" stroke-linecap="round" fill="none" opacity="0.9" />
  <path d="M 170 108 C 176 110, 182 106, 187 102" stroke="#FAF7F2" stroke-width="1.8" stroke-linecap="round" fill="none" opacity="0.9" />
  <path d="M 372 98 C 366 100, 360 96, 355 92" stroke="#FAF7F2" stroke-width="1.8" stroke-linecap="round" fill="none" opacity="0.9" />
  <path d="M 374 108 C 368 110, 362 106, 357 102" stroke="#FAF7F2" stroke-width="1.8" stroke-linecap="round" fill="none" opacity="0.9" />

  <!-- 5. Forehead Tabby Markings (Soft curved bands) -->
  <path d="M 271.5 73 C 275 73, 276 82, 276 98 C 276 112, 273.5 120, 271.5 120 C 269.5 120, 267 112, 267 98 C 267 82, 268 73, 271.5 73 Z" fill="#B24E0C" opacity="0.65" filter="url(#fineAo)" />
  <path d="M 243 82 C 246 81, 250 86, 252 100 C 254 114, 253 122, 251 123 C 249 124, 245 120, 243 106 C 241 94, 241 83, 243 82 Z" fill="#B24E0C" opacity="0.60" filter="url(#fineAo)" />
  <path d="M 300 82 C 302 83, 302 94, 300 106 C 298 120, 294 124, 292 123 C 290 122, 289 114, 291 100 C 293 86, 297 81, 300 82 Z" fill="#B24E0C" opacity="0.60" filter="url(#fineAo)" />

  <!-- 6. Complete White Fur Coat with Soft Diffuse Edge -->
  <g clip-path="url(#bodyClip)">
    <path d="{white_coat_path}" fill="url(#creamCoatGrad)" filter="url(#featherEdge)" />
  </g>

  <!-- Soft porcelain ambient occlusion in neck crease under chin -->
  <ellipse cx="271.5" cy="245" rx="52" ry="14" fill="#8C7A68" opacity="0.38" filter="url(#softAo)" />

  <!-- Front Cylindrical Legs Highlights -->
  <path d="M 224 370 C 224 400, 222 450, 220 480 L 262 480 C 264 450, 266 400, 266 370 Z" fill="url(#legLGrad)" opacity="0.8" />
  <path d="M 276 370 C 276 400, 278 450, 280 480 L 322 480 C 320 450, 318 400, 318 370 Z" fill="url(#legRGrad)" opacity="0.8" />

  <!-- Soft porcelain ambient occlusion groove between front legs -->
  <path d="M 271.5 375 C 270 410, 272 445, 271.5 488" stroke="#7D6A56" stroke-width="4.2" stroke-linecap="round" fill="none" opacity="0.60" filter="url(#fineAo)" />

  <!-- Chest diffuse highlight -->
  <ellipse cx="271.5" cy="320" rx="38" ry="50" fill="url(#chestHighlight)" />

  <!-- 7. Paw Toe Crevices (Grounded on Y=490) -->
  <!-- Left paw toes -->
  <path d="M 235 466 C 235 476, 235 484, 235 490" stroke="#8C7A68" stroke-width="1.8" stroke-linecap="round" fill="none" opacity="0.65" />
  <path d="M 252 466 C 252 476, 252 484, 252 490" stroke="#8C7A68" stroke-width="1.8" stroke-linecap="round" fill="none" opacity="0.65" />
  <!-- Right paw toes -->
  <path d="M 291 466 C 291 476, 291 484, 291 490" stroke="#8C7A68" stroke-width="1.8" stroke-linecap="round" fill="none" opacity="0.65" />
  <path d="M 308 466 C 308 476, 308 484, 308 490" stroke="#8C7A68" stroke-width="1.8" stroke-linecap="round" fill="none" opacity="0.65" />

  <!-- 8. Glassy Amber Orb Eyes (Calibrated Position & Glints) -->
  <!-- Left Eye: Center (223.5, 178.5) -->
  <g transform="translate(223.5, 178.5) rotate(-5)">
    <!-- Dark Eyeliner Socket -->
    <ellipse cx="0" cy="0" rx="26.5" ry="27.5" fill="#1C1004" />
    <!-- Glowing Amber Iris -->
    <ellipse cx="0" cy="0" rx="25.0" ry="26.0" fill="url(#irisL)" />
    <!-- Black Pupil -->
    <ellipse cx="0.0" cy="0" rx="17.0" ry="18.0" fill="#0C0702" />
    <!-- Diffuse Pearl Specular Glint at (233.3 - 223.5, 161.8 - 178.5) = (9.8, -16.7) -->
    <circle cx="9.8" cy="-16.7" r="5.5" fill="#DCD3CC" opacity="0.92" />
    <!-- Secondary soft ambient reflection -->
    <circle cx="-5.0" cy="12.0" r="3.0" fill="#FFEAA0" opacity="0.55" />
  </g>

  <!-- Right Eye: Center (316.5, 176.0) -->
  <g transform="translate(316.5, 176.0) rotate(5)">
    <!-- Dark Eyeliner Socket -->
    <ellipse cx="0" cy="0" rx="26.5" ry="27.5" fill="#1C1004" />
    <!-- Glowing Amber Iris -->
    <ellipse cx="0" cy="0" rx="25.0" ry="26.0" fill="url(#irisR)" />
    <!-- Black Pupil -->
    <ellipse cx="0.0" cy="0" rx="17.0" ry="18.0" fill="#0C0702" />
    <!-- Diffuse Pearl Specular Glint at (325.0 - 316.5, 162.7 - 176.0) = (8.5, -13.3) -->
    <circle cx="8.5" cy="-13.3" r="5.5" fill="#DCD3CC" opacity="0.92" />
    <!-- Secondary soft ambient reflection -->
    <circle cx="-5.0" cy="12.0" r="3.0" fill="#FFEAA0" opacity="0.55" />
  </g>

  <!-- 9. Whisker Pads (Muzzle Mounds) & Soft Nose -->
  <!-- Whisker pad left & right mounds -->
  <ellipse cx="258" cy="214" rx="15" ry="12" fill="#FAF7F2" opacity="0.92" />
  <ellipse cx="285" cy="214" rx="15" ry="12" fill="#FAF7F2" opacity="0.92" />

  <!-- Button Nose at (271.6, 198.2) -->
  <path d="M 261 195 C 265 192, 278 192, 282 195 C 286 200, 278 206, 271.6 206 C 265 206, 257 200, 261 195 Z" fill="url(#noseGrad)" stroke="#B65A4C" stroke-width="0.8" />
  <ellipse cx="271.6" cy="196" rx="3.5" ry="1.5" fill="#FFFFFF" opacity="0.5" />

  <!-- Philtrum & Mouth Line ω -->
  <path d="M 271.6 206 L 271.6 215" stroke="#7A6857" stroke-width="1.4" stroke-linecap="round" fill="none" />
  <path d="M 250 222 C 256 226, 265 224, 271.6 215 C 278 224, 287 226, 293 222" stroke="#7A6857" stroke-width="1.4" stroke-linecap="round" fill="none" />

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
    return svg

for b_val in [0.8, 1.2, 1.8, 2.5]:
    svg_code = generate_svg(b_val)
    path = f"scratch/meoweko_feather_{b_val}.svg"
    with open(path, "w") as f:
        f.write(svg_code)
    print(f"Testing blur={b_val}:")
    benchmark_svg(path)
