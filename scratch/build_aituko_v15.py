import sys
sys.path.append(".")
import cv2, numpy as np
from PIL import Image
from scripts.benchmark_aituko_fidelity import render_svg_chrome, evaluate_aituko

ref = np.array(Image.open("mascots/aituko/aituko_master_exact_512.png").convert("RGBA"))
alpha = (ref[:, :, 3] > 20).astype(np.uint8) * 255
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(alpha)

def get_path(mask, eps=0.7):
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
    approx = cv2.approxPolyDP(cnts[0], eps, True)[:, 0, :]
    return "M " + " L ".join([f"{p[0]} {p[1]}" for p in approx]) + " Z"

# Exact component contours
c1_d = get_path((labels == 1).astype(np.uint8)*255, 0.7) # Head + Torso
lwing_d = get_path((labels == 3).astype(np.uint8)*255, 0.7) # Left Winglet
rwing_d = get_path((labels == 2).astype(np.uint8)*255, 0.7) # Right Winglet
lfoot_d = get_path((labels == 4).astype(np.uint8)*255, 0.7) # Left Foot
rfoot_d = get_path((labels == 5).astype(np.uint8)*255, 0.7) # Right Foot
shadow_d = get_path((labels == 6).astype(np.uint8)*255, 0.8) # Shadow

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" style="background: transparent;">
  <defs>
    <!-- Master Head+Torso Clip (IoU >= 99.6%) -->
    <clipPath id="bodyClip">
      <path d="{c1_d}" />
    </clipPath>

    <!-- Head Porcelain Dome -->
    <radialGradient id="headDome" cx="50%" cy="20%" r="75%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="30%" stop-color="#FAF8F4" />
      <stop offset="60%" stop-color="#EDE6DC" />
      <stop offset="85%" stop-color="#D4C8BC" />
      <stop offset="100%" stop-color="#A89C90" />
    </radialGradient>

    <!-- Obsidian Visor -->
    <linearGradient id="visorGlass" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#6B635B" />
      <stop offset="12%" stop-color="#423D37" />
      <stop offset="25%" stop-color="#181D26" />
      <stop offset="50%" stop-color="#0D1017" />
      <stop offset="100%" stop-color="#06080C" />
    </linearGradient>

    <!-- Torso Cylindrical Porcelain -->
    <linearGradient id="torsoGrad" x1="0%" y1="35%" x2="100%" y2="35%">
      <stop offset="0%" stop-color="#A89B8E" />
      <stop offset="12%" stop-color="#FFFDF5" />
      <stop offset="22%" stop-color="#FAF7F2" />
      <stop offset="35%" stop-color="#D7CCC3" />
      <stop offset="55%" stop-color="#C0B5AE" />
      <stop offset="75%" stop-color="#BAAEA6" />
      <stop offset="88%" stop-color="#DCD4CA" />
      <stop offset="100%" stop-color="#8E8278" />
    </linearGradient>

    <!-- Chest AO Shadow under collar (Y in [204, 240]) -->
    <radialGradient id="chestAOGrad" cx="50%" cy="15%" r="85%">
      <stop offset="0%" stop-color="#423830" stop-opacity="0.68" />
      <stop offset="40%" stop-color="#65594E" stop-opacity="0.48" />
      <stop offset="75%" stop-color="#928476" stop-opacity="0.22" />
      <stop offset="100%" stop-color="#BAACA0" stop-opacity="0.0" />
    </radialGradient>

    <!-- Pelvis Base AO Shadow Calibrated -->
    <radialGradient id="pelvisAOGrad" cx="50%" cy="80%" r="65%">
      <stop offset="0%" stop-color="#423932" stop-opacity="0.65" />
      <stop offset="45%" stop-color="#655950" stop-opacity="0.35" />
      <stop offset="100%" stop-color="#8E8278" stop-opacity="0.0" />
    </radialGradient>

    <!-- Torso Vertical Shading Overlay -->
    <linearGradient id="torsoVertGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.10" />
      <stop offset="15%" stop-color="#FFFFFF" stop-opacity="0.05" />
      <stop offset="60%" stop-color="#FFFFFF" stop-opacity="0.0" />
      <stop offset="85%" stop-color="#000000" stop-opacity="0.18" />
      <stop offset="100%" stop-color="#000000" stop-opacity="0.40" />
    </linearGradient>

    <!-- Left Winglet Pod -->
    <linearGradient id="lpodGrad" x1="10%" y1="15%" x2="90%" y2="85%">
      <stop offset="0%" stop-color="#EAE3D9" />
      <stop offset="25%" stop-color="#D8CFC5" />
      <stop offset="55%" stop-color="#B8ADA2" />
      <stop offset="85%" stop-color="#968C81" />
      <stop offset="100%" stop-color="#72685E" />
    </linearGradient>

    <!-- Right Winglet Pod -->
    <linearGradient id="rpodGrad" x1="75%" y1="10%" x2="35%" y2="95%">
      <stop offset="0%" stop-color="#E2D8CE" />
      <stop offset="35%" stop-color="#C2B6AA" />
      <stop offset="70%" stop-color="#9E9286" />
      <stop offset="100%" stop-color="#685E54" />
    </linearGradient>

    <!-- Feet Pods -->
    <linearGradient id="footGrad" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#D0C7C2" />
      <stop offset="35%" stop-color="#B6ACA6" />
      <stop offset="70%" stop-color="#8A7F7A" />
      <stop offset="100%" stop-color="#5E5650" />
    </linearGradient>

    <!-- Cyan Glowing Eyes -->
    <linearGradient id="cyanGlow" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#E6FFFF" />
      <stop offset="40%" stop-color="#00F9FA" />
      <stop offset="100%" stop-color="#00E5F5" />
    </linearGradient>

    <!-- Ground Contact Shadow Calibrated -->
    <radialGradient id="groundShadow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.61" />
      <stop offset="50%" stop-color="#000000" stop-opacity="0.48" />
      <stop offset="85%" stop-color="#000000" stop-opacity="0.25" />
      <stop offset="92%" stop-color="#000000" stop-opacity="0.18" />
      <stop offset="100%" stop-color="#000000" stop-opacity="0.10" />
    </radialGradient>
  </defs>

  <!-- 0. Ground Contact Shadow (Exact Contour IoU >= 99%) -->
  <path d="{shadow_d}" fill="url(#groundShadow)" />

  <!-- 1. Feet Pods (Exact Contours IoU >= 98.7%) -->
  <path d="{lfoot_d}" fill="url(#footGrad)" />
  <path d="{rfoot_d}" fill="url(#footGrad)" />
  <ellipse cx="218" cy="430" rx="8" ry="4" fill="#FFFFFF" opacity="0.18" />
  <ellipse cx="296" cy="430" rx="8" ry="4" fill="#FFFFFF" opacity="0.12" />

  <!-- 2. Floating Winglet Pods (Exact Contours IoU >= 98.8%) -->
  <path d="{lwing_d}" fill="url(#lpodGrad)" />
  <path d="{rwing_d}" fill="url(#rpodGrad)" />

  <!-- 3. Head & Torso Assembly (Clipped to Exact 76-pt Silhouette IoU = 99.67%) -->
  <g clip-path="url(#bodyClip)">
    <!-- Base Fill -->
    <path d="{c1_d}" fill="url(#torsoGrad)" />

    <!-- Head Dome -->
    <ellipse cx="257" cy="122" rx="100" ry="82" fill="url(#headDome)" />
    <ellipse cx="256" cy="52" rx="46" ry="10" fill="#FFFFFF" opacity="0.85" />

    <!-- Torso Volume -->
    <rect x="185" y="205" width="144" height="205" rx="55" fill="url(#torsoGrad)" />
    <rect x="185" y="205" width="144" height="205" rx="55" fill="url(#torsoVertGrad)" />
    <!-- Chest AO Shadow under collar -->
    <ellipse cx="256" cy="214" rx="46" ry="20" fill="url(#chestAOGrad)" />
    <!-- Pelvis Base AO Shadow -->
    <ellipse cx="256" cy="402" rx="35" ry="10" fill="url(#pelvisAOGrad)" />

    <!-- Subtle Chin Contact Shadow -->
    <ellipse cx="257" cy="207" rx="24" ry="6" fill="#5A4E44" opacity="0.45" />

    <!-- Obsidian Visor -->
    <path d="M 188.00 87.00 C 184.67 92.17, 182.67 98.17, 181.00 103.00 C 179.33 107.83, 178.67 108.50, 178.00 116.00 C 177.33 123.50, 176.50 140.50, 177.00 148.00 C 177.50 155.50, 178.83 157.17, 181.00 161.00 C 183.17 164.83, 186.17 168.33, 190.00 171.00 C 193.83 173.67, 198.17 175.33, 204.00 177.00 C 209.83 178.67, 212.83 180.17, 225.00 181.00 C 237.17 181.83, 262.17 182.83, 277.00 182.00 C 291.83 181.17, 305.83 178.00, 314.00 176.00 C 322.17 174.00, 322.83 172.33, 326.00 170.00 C 329.17 167.67, 331.17 165.67, 333.00 162.00 C 334.83 158.33, 336.33 154.50, 337.00 148.00 C 337.67 141.50, 337.67 130.33, 337.00 123.00 C 336.33 115.67, 335.33 110.83, 333.00 104.00 C 330.67 97.17, 325.67 86.83, 323.00 82.00 C 320.33 77.17, 319.83 77.50, 317.00 75.00 C 314.17 72.50, 310.67 69.33, 306.00 67.00 C 301.33 64.67, 295.50 62.50, 289.00 61.00 C 282.50 59.50, 276.83 58.17, 267.00 58.00 C 257.17 57.83, 240.00 58.33, 230.00 60.00 C 220.00 61.67, 211.83 66.00, 207.00 68.00 C 202.17 70.00, 204.17 68.83, 201.00 72.00 C 197.83 75.17, 191.33 81.83, 188.00 87.00 Z" fill="url(#visorGlass)" stroke="#2A3245" stroke-width="0.8" />

    <!-- Cyan Eyes -->
    <path d="M 202.00 125.00 C 201.17 127.83, 201.83 130.50, 202.00 132.00 C 202.17 133.50, 202.50 133.67, 203.00 134.00 C 203.50 134.33, 203.67 134.83, 205.00 134.00 C 206.33 133.17, 209.00 130.17, 211.00 129.00 C 213.00 127.83, 214.33 127.17, 217.00 127.00 C 219.67 126.83, 224.00 126.83, 227.00 128.00 C 230.00 129.17, 233.33 133.00, 235.00 134.00 C 236.67 135.00, 236.50 134.33, 237.00 134.00 C 237.50 133.67, 238.00 134.33, 238.00 132.00 C 238.00 129.67, 238.00 123.00, 237.00 120.00 C 236.00 117.00, 234.00 115.67, 232.00 114.00 C 230.00 112.33, 228.00 110.67, 225.00 110.00 C 222.00 109.33, 217.00 109.17, 214.00 110.00 C 211.00 110.83, 209.00 112.50, 207.00 115.00 C 205.00 117.50, 202.83 122.17, 202.00 125.00 Z" fill="url(#cyanGlow)" />
    <path d="M 277.00 120.00 C 276.00 121.67, 277.33 121.83, 277.00 123.00 C 276.67 124.17, 275.33 125.67, 275.00 127.00 C 274.67 128.33, 274.67 129.83, 275.00 131.00 C 275.33 132.17, 276.33 133.50, 277.00 134.00 C 277.67 134.50, 278.00 134.67, 279.00 134.00 C 280.00 133.33, 281.17 131.17, 283.00 130.00 C 284.83 128.83, 287.83 127.50, 290.00 127.00 C 292.17 126.50, 293.83 126.67, 296.00 127.00 C 298.17 127.33, 300.83 127.83, 303.00 129.00 C 305.17 130.17, 307.50 133.50, 309.00 134.00 C 310.50 134.50, 311.50 133.83, 312.00 132.00 C 312.50 130.17, 312.50 125.50, 312.00 123.00 C 311.50 120.50, 310.50 118.83, 309.00 117.00 C 307.50 115.17, 305.00 113.17, 303.00 112.00 C 301.00 110.83, 299.83 110.17, 297.00 110.00 C 294.17 109.83, 288.33 110.50, 286.00 111.00 C 283.67 111.50, 284.50 111.50, 283.00 113.00 C 281.50 114.50, 278.00 118.33, 277.00 120.00 Z" fill="url(#cyanGlow)" />
  </g>
</svg>"""

with open("scratch/test_aituko_calibrated_v15.svg", "w") as f:
    f.write(svg)

png = render_svg_chrome("scratch/test_aituko_calibrated_v15.svg", "scratch/test_aituko_calibrated_v15.png")
res = evaluate_aituko(png)
