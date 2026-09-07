#!/usr/bin/env python3
import os
import subprocess
import cv2
import numpy as np
from PIL import Image

def get_contour_pts(mask, eps=0.6, min_area=30):
    cnts, _ = cv2.findContours(mask.astype(np.uint8)*255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    valid = [c for c in cnts if cv2.contourArea(c) > min_area]
    if not valid:
        return []
    c = max(valid, key=cv2.contourArea)
    approx = cv2.approxPolyDP(c, eps, True)
    pts = approx.reshape(-1, 2)
    return [(round(float(p[0]), 2), round(float(p[1]), 2)) for p in pts]

def points_to_svg_cubic_spline(pts, tension=1.0):
    n = len(pts)
    if n < 3:
        return ""
    c_factor = tension / 6.0
    d = [f"M {pts[0][0]:.2f} {pts[0][1]:.2f}"]
    for i in range(n):
        p_prev = pts[(i - 1) % n]
        p_curr = pts[i]
        p_next = pts[(i + 1) % n]
        p_next2 = pts[(i + 2) % n]
        c1_x = p_curr[0] + (p_next[0] - p_prev[0]) * c_factor
        c1_y = p_curr[1] + (p_next[1] - p_prev[1]) * c_factor
        c2_x = p_next[0] - (p_next2[0] - p_curr[0]) * c_factor
        c2_y = p_next[1] - (p_next2[1] - p_curr[1]) * c_factor
        d.append(f"C {c1_x:.2f} {c1_y:.2f}, {c2_x:.2f} {c2_y:.2f}, {p_next[0]:.2f} {p_next[1]:.2f}")
    d.append("Z")
    return " ".join(d)

img = cv2.imread("mascots/meoweko/meoweko_master_exact_512.png", cv2.IMREAD_UNCHANGED)
b, g, r, a = cv2.split(img)
bgr = cv2.merge([b, g, r])

# 1. Total Silhouette (Base Ginger Porcelain Body)
body_mask = (a > 30)
body_pts = get_contour_pts(body_mask, eps=0.6, min_area=5000)
spline_total_body = points_to_svg_cubic_spline(body_pts)

# 2. Tail contour (Lower Left)
# Extract precise ginger tail
tail_mask = np.zeros_like(a, dtype=bool)
# In region X: [115, 195], Y: [400, 485], tail is where bgr is ginger
tail_roi = img[400:485, 115:195]
t_ginger = (tail_roi[:,:,3] > 30) & (tail_roi[:,:,2] > 130) & (tail_roi[:,:,0] < 105)
tail_mask[400:485, 115:195] = t_ginger
tail_mask = cv2.morphologyEx(tail_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))) > 0
tail_pts = get_contour_pts(tail_mask, eps=0.5, min_area=500)
spline_tail = points_to_svg_cubic_spline(tail_pts)

# 3. Flanks (Left & Right Hindquarters)
flank_l_mask = np.zeros_like(a, dtype=bool)
flank_l_roi = img[330:460, 145:225]
fl_ginger = (flank_l_roi[:,:,3] > 30) & (flank_l_roi[:,:,2] > 140) & (flank_l_roi[:,:,0] < 125)
flank_l_mask[330:460, 145:225] = fl_ginger
flank_l_mask = cv2.morphologyEx(flank_l_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))) > 0
spline_flank_l = points_to_svg_cubic_spline(get_contour_pts(flank_l_mask, eps=0.6, min_area=500))

flank_r_mask = np.zeros_like(a, dtype=bool)
flank_r_roi = img[330:460, 295:380]
fr_ginger = (flank_r_roi[:,:,3] > 30) & (flank_r_roi[:,:,2] > 140) & (flank_r_roi[:,:,0] < 125)
flank_r_mask[330:460, 295:380] = fr_ginger
flank_r_mask = cv2.morphologyEx(flank_r_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))) > 0
spline_flank_r = points_to_svg_cubic_spline(get_contour_pts(flank_r_mask, eps=0.6, min_area=500))

# 4. White Fur Marking (Blaze, Muzzle, Cheeks, Chest, Front Legs, Paws)
# In Meoweko, white coat is where R > G - 10 and B > 140 or BGR is cream/white porcelain
# Let's inspect HSV: S < 55 and V > 160 inside mascot mask
hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
white_cand = (a > 30) & (hsv[:,:,1] < 65) & (hsv[:,:,2] > 150)
# Also include slightly shadowed neck (V > 120, S < 45, Y in [210, 260])
neck_shadow_white = (a > 30) & (hsv[:,:,1] < 45) & (hsv[:,:,2] > 115) & (np.arange(512)[:, None] > 200) & (np.arange(512)[:, None] < 265) & (np.arange(512)[None, :] > 200) & (np.arange(512)[None, :] < 320)
white_total = (white_cand | neck_shadow_white)

# Exclude eyes from white coat
eye_box_l = (np.arange(512)[:, None] > 135) & (np.arange(512)[:, None] < 215) & (np.arange(512)[None, :] > 175) & (np.arange(512)[None, :] < 250)
eye_box_r = (np.arange(512)[:, None] > 135) & (np.arange(512)[:, None] < 215) & (np.arange(512)[None, :] > 290) & (np.arange(512)[None, :] < 365)
white_total[eye_box_l] = False
white_total[eye_box_r] = False

# Fill holes in white coat
white_u8 = cv2.morphologyEx(white_total.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)))
spline_white_coat = points_to_svg_cubic_spline(get_contour_pts(white_u8 > 0, eps=0.6, min_area=3000))

# 5. Inner Ears
# Left Inner Ear
ear_l_roi = img[65:145, 160:220]
el_mask = np.zeros_like(a, dtype=bool)
el_mask[65:145, 160:220] = (ear_l_roi[:,:,3] > 30) & (ear_l_roi[:,:,2] > 180) & (ear_l_roi[:,:,1] > 110) & (ear_l_roi[:,:,1] < 170) & (ear_l_roi[:,:,0] > 80)
el_u8 = cv2.morphologyEx(el_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
spline_ear_l = points_to_svg_cubic_spline(get_contour_pts(el_u8 > 0, eps=0.5, min_area=100))

# Right Inner Ear
ear_r_roi = img[65:145, 335:385]
er_mask = np.zeros_like(a, dtype=bool)
er_mask[65:145, 335:385] = (ear_r_roi[:,:,3] > 30) & (ear_r_roi[:,:,2] > 180) & (ear_r_roi[:,:,1] > 110) & (ear_r_roi[:,:,1] < 170) & (ear_r_roi[:,:,0] > 80)
er_u8 = cv2.morphologyEx(er_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
spline_ear_r = points_to_svg_cubic_spline(get_contour_pts(er_u8 > 0, eps=0.5, min_area=100))

# 6. Amber Eyes
# Left Eye Iris
eye_l_dark = (a[140:215, 180:255] > 30) & (r[140:215, 180:255] < 75) & (g[140:215, 180:255] < 75) & (b[140:215, 180:255] < 75)
eye_l_iris = (a[140:215, 180:255] > 30) & (r[140:215, 180:255] > 90) & (g[140:215, 180:255] > 80) & (b[140:215, 180:255] < 85)
eye_l_total = np.zeros_like(a, dtype=bool)
eye_l_total[140:215, 180:255] = eye_l_dark | eye_l_iris
eye_l_u8 = cv2.morphologyEx(eye_l_total.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
spline_eye_l = points_to_svg_cubic_spline(get_contour_pts(eye_l_u8 > 0, eps=0.4, min_area=500))

# Right Eye Iris
eye_r_dark = (a[140:215, 290:360] > 30) & (r[140:215, 290:360] < 75) & (g[140:215, 290:360] < 75) & (b[140:215, 290:360] < 75)
eye_r_iris = (a[140:215, 290:360] > 30) & (r[140:215, 290:360] > 90) & (g[140:215, 290:360] > 80) & (b[140:215, 290:360] < 85)
eye_r_total = np.zeros_like(a, dtype=bool)
eye_r_total[140:215, 290:360] = eye_r_dark | eye_r_iris
eye_r_u8 = cv2.morphologyEx(eye_r_total.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
spline_eye_r = points_to_svg_cubic_spline(get_contour_pts(eye_r_u8 > 0, eps=0.4, min_area=500))

# Left Pupil
pupil_l_mask = np.zeros_like(a, dtype=bool)
pupil_l_mask[150:195, 205:245] = (a[150:195, 205:245] > 30) & (r[150:195, 205:245] < 60) & (g[150:195, 205:245] < 60) & (b[150:195, 205:245] < 60)
pupil_l_u8 = cv2.morphologyEx(pupil_l_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
spline_pupil_l = points_to_svg_cubic_spline(get_contour_pts(pupil_l_u8 > 0, eps=0.4, min_area=200))

# Right Pupil
pupil_r_mask = np.zeros_like(a, dtype=bool)
pupil_r_mask[150:195, 300:340] = (a[150:195, 300:340] > 30) & (r[150:195, 300:340] < 60) & (g[150:195, 300:340] < 60) & (b[150:195, 300:340] < 60)
pupil_r_u8 = cv2.morphologyEx(pupil_r_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
spline_pupil_r = points_to_svg_cubic_spline(get_contour_pts(pupil_r_u8 > 0, eps=0.4, min_area=200))

# 7. Front Paws Clefts (Scoring individual toes on baseline)
# Left Paw Clefts: X around 208 and 233, Y from 465 to 491
# Right Paw Clefts: X around 284 and 309, Y from 465 to 491
# Central leg divide: X ~ 256, Y from 360 to 475

svg_markup = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <!-- Multi-stop authentic porcelain ceramic shaders -->
    <linearGradient id="gingerCoatMaster" x1="25%" y1="15%" x2="75%" y2="85%">
      <stop offset="0%" stop-color="#F7AD63" />
      <stop offset="30%" stop-color="#EA8835" />
      <stop offset="65%" stop-color="#D26E20" />
      <stop offset="100%" stop-color="#B25010" />
    </linearGradient>

    <linearGradient id="tailGradient" x1="15%" y1="20%" x2="85%" y2="80%">
      <stop offset="0%" stop-color="#EA8835" />
      <stop offset="55%" stop-color="#CD681C" />
      <stop offset="100%" stop-color="#A54708" />
    </linearGradient>

    <radialGradient id="creamPorcelainBody" cx="48%" cy="38%" r="62%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="40%" stop-color="#FAF7F2" />
      <stop offset="75%" stop-color="#ECE5D7" />
      <stop offset="100%" stop-color="#D5C9B6" />
    </radialGradient>

    <radialGradient id="pinkEarCavity" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#FDCABC" />
      <stop offset="45%" stop-color="#F8A796" />
      <stop offset="80%" stop-color="#E88270" />
      <stop offset="100%" stop-color="#CE5C48" />
    </radialGradient>

    <radialGradient id="amberIrisL" cx="62%" cy="65%" r="55%">
      <stop offset="0%" stop-color="#FFF066" />
      <stop offset="35%" stop-color="#E5B52B" />
      <stop offset="70%" stop-color="#9C7314" />
      <stop offset="100%" stop-color="#3A2303" />
    </radialGradient>

    <radialGradient id="amberIrisR" cx="38%" cy="65%" r="55%">
      <stop offset="0%" stop-color="#FFF066" />
      <stop offset="35%" stop-color="#E5B52B" />
      <stop offset="70%" stop-color="#9C7314" />
      <stop offset="100%" stop-color="#3A2303" />
    </radialGradient>

    <radialGradient id="chestSpecularHighlight" cx="50%" cy="30%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.85" />
      <stop offset="50%" stop-color="#FFFFFF" stop-opacity="0.3" />
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.0" />
    </radialGradient>
  </defs>

  <!-- Background -->
  <rect width="512" height="512" fill="#0B0F17" />

  <!-- 1. Tail (Backmost layer, left swish) -->
  <path d="{spline_tail}" fill="url(#tailGradient)" stroke="#92400A" stroke-width="0.9" />

  <!-- 2. Master Silhouette Base (Ginger Ceramic Shell) -->
  <path d="{spline_total_body}" fill="url(#gingerCoatMaster)" stroke="#92400A" stroke-width="0.9" />

  <!-- 3. Left & Right Flank Depths (Shading separation) -->
  <path d="{spline_flank_l}" fill="url(#gingerCoatMaster)" opacity="0.95" />
  <path d="{spline_flank_r}" fill="url(#gingerCoatMaster)" opacity="0.95" />

  <!-- 4. Inner Ear Cavities (Soft Peach Porcelain) -->
  <path d="{spline_ear_l}" fill="url(#pinkEarCavity)" stroke="#BF5340" stroke-width="0.8" />
  <!-- Left Ear Tufts -->
  <path d="M 188 120 C 182 118, 178 122, 172 124" stroke="#FAF7F2" stroke-width="2.8" stroke-linecap="round" fill="none" />
  <path d="M 192 128 C 185 127, 180 131, 175 133" stroke="#FAF7F2" stroke-width="2.4" stroke-linecap="round" fill="none" />

  <path d="{spline_ear_r}" fill="url(#pinkEarCavity)" stroke="#BF5340" stroke-width="0.8" />
  <!-- Right Ear Tufts -->
  <path d="M 348 120 C 354 118, 358 122, 364 124" stroke="#FAF7F2" stroke-width="2.8" stroke-linecap="round" fill="none" />
  <path d="M 344 128 C 351 127, 356 131, 361 133" stroke="#FAF7F2" stroke-width="2.4" stroke-linecap="round" fill="none" />

  <!-- 5. Forehead Tabby Stripes (Ginger / Amber) -->
  <path d="M 268 82 C 269 105, 270 120, 271 138" stroke="#B85210" stroke-width="7.5" stroke-linecap="round" fill="none" opacity="0.8" />
  <path d="M 244 90 C 247 108, 252 120, 255 134" stroke="#B85210" stroke-width="6.5" stroke-linecap="round" fill="none" opacity="0.75" />
  <path d="M 293 90 C 290 108, 285 120, 282 134" stroke="#B85210" stroke-width="6.5" stroke-linecap="round" fill="none" opacity="0.75" />

  <!-- 6. White Fur Coat (Blaze, Chubby Cheeks, Muzzle, Chest, Front Legs, Paws) -->
  <path d="{spline_white_coat}" fill="url(#creamPorcelainBody)" stroke="#C8BEAD" stroke-width="0.9" />

  <!-- Chest Curvature Specular Highlight -->
  <ellipse cx="260" cy="320" rx="38" ry="48" fill="url(#chestSpecularHighlight)" />

  <!-- Vertical Leg Divide & Paw Clefts -->
  <!-- Leg separation crease -->
  <path d="M 256 360 C 256 395, 256 440, 256 478" stroke="#B8AC98" stroke-width="1.6" stroke-linecap="round" fill="none" opacity="0.85" />
  
  <!-- Left Paw Toes (3 rounded toes) -->
  <path d="M 209 466 C 209 476, 208 483, 207 490" stroke="#B8AC98" stroke-width="1.5" stroke-linecap="round" fill="none" />
  <path d="M 232 466 C 233 476, 234 483, 235 490" stroke="#B8AC98" stroke-width="1.5" stroke-linecap="round" fill="none" />

  <!-- Right Paw Toes (3 rounded toes) -->
  <path d="M 285 466 C 284 476, 283 483, 282 490" stroke="#B8AC98" stroke-width="1.5" stroke-linecap="round" fill="none" />
  <path d="M 308 466 C 309 476, 310 483, 311 490" stroke="#B8AC98" stroke-width="1.5" stroke-linecap="round" fill="none" />

  <!-- 7. Glassy Amber Orb Eyes -->
  <!-- Left Eye -->
  <g id="leftEyeGroup">
    <path d="{spline_eye_l}" fill="url(#amberIrisL)" stroke="#221402" stroke-width="2.6" />
    <path d="{spline_pupil_l}" fill="#0F0902" />
    <!-- Crisp White Specular Glint (Upper-Right) -->
    <circle cx="218" cy="162" r="7.5" fill="#FFFFFF" />
    <!-- Secondary Soft Reflection (Lower-Left) -->
    <circle cx="229" cy="180" r="3.2" fill="#FFFFFF" opacity="0.65" />
  </g>

  <!-- Right Eye -->
  <g id="rightEyeGroup">
    <path d="{spline_eye_r}" fill="url(#amberIrisR)" stroke="#221402" stroke-width="2.6" />
    <path d="{spline_pupil_r}" fill="#0F0902" />
    <!-- Crisp White Specular Glint (Upper-Right) -->
    <circle cx="312" cy="162" r="7.5" fill="#FFFFFF" />
    <!-- Secondary Soft Reflection (Lower-Left) -->
    <circle cx="323" cy="180" r="3.2" fill="#FFFFFF" opacity="0.65" />
  </g>

  <!-- 8. Peach Nose & Feline Smile ω -->
  <path d="M 264 195 C 267 193, 275 193, 278 195 C 280 197, 274 204, 271 204 C 268 204, 262 197, 264 195 Z" fill="#F89D8A" stroke="#DF715C" stroke-width="0.9" />
  <path d="M 271 204 L 271 209" stroke="#8E7E6F" stroke-width="1.3" stroke-linecap="round" fill="none" />
  <path d="M 260 212 C 264 215, 268 214, 271 209 C 274 214, 278 215, 282 212" stroke="#8E7E6F" stroke-width="1.3" stroke-linecap="round" fill="none" />

  <!-- 9. Delicate Feline Whiskers -->
  <!-- Left Whiskers -->
  <path d="M 248 206 C 220 205, 195 212, 178 218" stroke="#FFFFFF" stroke-width="1.3" stroke-linecap="round" fill="none" opacity="0.92" />
  <path d="M 246 211 C 218 214, 192 225, 182 233" stroke="#FFFFFF" stroke-width="1.3" stroke-linecap="round" fill="none" opacity="0.92" />
  <path d="M 247 217 C 222 225, 202 239, 190 248" stroke="#FFFFFF" stroke-width="1.1" stroke-linecap="round" fill="none" opacity="0.85" />

  <!-- Right Whiskers -->
  <path d="M 294 206 C 322 205, 347 212, 364 218" stroke="#FFFFFF" stroke-width="1.3" stroke-linecap="round" fill="none" opacity="0.92" />
  <path d="M 296 211 C 324 214, 350 225, 360 233" stroke="#FFFFFF" stroke-width="1.3" stroke-linecap="round" fill="none" opacity="0.92" />
  <path d="M 295 217 C 320 225, 340 239, 352 248" stroke="#FFFFFF" stroke-width="1.1" stroke-linecap="round" fill="none" opacity="0.85" />
</svg>"""

out_svg = "scratch/meoweko_flawless_vector.svg"
with open(out_svg, "w") as f:
    f.write(svg_markup)
print(f"✅ Saved vector SVG: {out_svg} ({len(svg_markup)/1024:.1f} KB)")

preview_png = "scratch/meoweko_flawless_vector_preview.png"
cmd = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "--headless",
    "--disable-gpu",
    f"--screenshot={preview_png}",
    "--window-size=512,512",
    "--default-background-color=00000000",
    f"file://{os.path.abspath(out_svg)}"
]
subprocess.run(cmd, check=True)
print(f"✅ Rendered PNG preview: {preview_png}")

# Create side-by-side comparison
ref = Image.open("mascots/meoweko/meoweko_master_exact_512.png").convert("RGBA")
vec = Image.open(preview_png).convert("RGBA")
comp = Image.new("RGBA", (1024, 512), (11, 15, 23, 255))
comp.paste(ref, (0, 0), ref.split()[3])
comp.paste(vec, (512, 0), vec.split()[3])
comp_path = "scratch/meoweko_flawless_vs_3d_comparison.png"
comp.save(comp_path, "PNG")
print(f"✅ Saved side-by-side comparison to {comp_path}")
