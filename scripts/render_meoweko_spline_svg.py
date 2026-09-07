#!/usr/bin/env python3
import os
import subprocess
import cv2
import numpy as np
from PIL import Image

def get_contour_pts(mask, eps=0.8, min_area=30):
    cnts, _ = cv2.findContours(mask.astype(np.uint8)*255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    valid = [c for c in cnts if cv2.contourArea(c) > min_area]
    if not valid:
        return []
    c = max(valid, key=cv2.contourArea)
    approx = cv2.approxPolyDP(c, eps, True)
    pts = approx.reshape(-1, 2)
    return [(float(p[0]), float(p[1])) for p in pts]

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

# 1. Total Silhouette
body_pts = get_contour_pts(a > 30, eps=0.8, min_area=5000)
spline_body = points_to_svg_cubic_spline(body_pts)

# 2. Tail
tail_mask = np.zeros_like(a, dtype=bool)
tail_mask[400:485, 110:205] = (a[400:485, 110:205] > 30) & (r[400:485, 110:205] > 130) & (b[400:485, 110:205] < 100)
tail_mask = cv2.morphologyEx(tail_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))) > 0
tail_pts = get_contour_pts(tail_mask, eps=0.8, min_area=500)
spline_tail = points_to_svg_cubic_spline(tail_pts)

# 3. Flanks
flank_l_mask = np.zeros_like(a, dtype=bool)
flank_l_mask[330:455, 145:230] = (a[330:455, 145:230] > 30) & (r[330:455, 145:230] > 140) & (b[330:455, 145:230] < 120)
flank_l_mask = cv2.morphologyEx(flank_l_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))) > 0
spline_flank_l = points_to_svg_cubic_spline(get_contour_pts(flank_l_mask, eps=0.8, min_area=500))

flank_r_mask = np.zeros_like(a, dtype=bool)
flank_r_mask[330:460, 290:380] = (a[330:460, 290:380] > 30) & (r[330:460, 290:380] > 140) & (b[330:460, 290:380] < 120)
flank_r_mask = cv2.morphologyEx(flank_r_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))) > 0
spline_flank_r = points_to_svg_cubic_spline(get_contour_pts(flank_r_mask, eps=0.8, min_area=500))

# 4. Central Cream Chest & Legs
chest_mask = np.zeros_like(a, dtype=bool)
chest_mask[240:490, 185:330] = (a[240:490, 185:330] > 30) & (r[240:490, 185:330] > 175) & (g[240:490, 185:330] > 170) & (b[240:490, 185:330] > 160)
chest_mask = cv2.morphologyEx(chest_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))) > 0
spline_chest = points_to_svg_cubic_spline(get_contour_pts(chest_mask, eps=0.8, min_area=2000))

# 5. Paws
paw_l_mask = np.zeros_like(a, dtype=bool)
paw_l_mask[440:491, 185:260] = chest_mask[440:491, 185:260]
spline_paw_l = points_to_svg_cubic_spline(get_contour_pts(paw_l_mask, eps=0.5, min_area=300))

paw_r_mask = np.zeros_like(a, dtype=bool)
paw_r_mask[440:491, 260:335] = chest_mask[440:491, 260:335]
spline_paw_r = points_to_svg_cubic_spline(get_contour_pts(paw_r_mask, eps=0.5, min_area=300))

# 6. Head
head_mask = np.zeros_like(a, dtype=bool)
head_mask[40:275, 150:395] = (a[40:275, 150:395] > 30)
spline_head = points_to_svg_cubic_spline(get_contour_pts(head_mask, eps=0.8, min_area=5000))

# 7. Inner Ears
ear_l_mask = np.zeros_like(a, dtype=bool)
ear_l_roi = img[65:145, 160:220]
ear_l_mask[65:145, 160:220] = (ear_l_roi[:,:,3] > 30) & (ear_l_roi[:,:,2] > 180) & (ear_l_roi[:,:,1] > 110) & (ear_l_roi[:,:,1] < 170) & (ear_l_roi[:,:,0] > 80)
ear_l_mask = cv2.morphologyEx(ear_l_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))) > 0
spline_ear_l = points_to_svg_cubic_spline(get_contour_pts(ear_l_mask, eps=0.6, min_area=100))

ear_r_mask = np.zeros_like(a, dtype=bool)
ear_r_roi = img[65:145, 335:385]
ear_r_mask[65:145, 335:385] = (ear_r_roi[:,:,3] > 30) & (ear_r_roi[:,:,2] > 180) & (ear_r_roi[:,:,1] > 110) & (ear_r_roi[:,:,1] < 170) & (ear_r_roi[:,:,0] > 80)
ear_r_mask = cv2.morphologyEx(ear_r_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))) > 0
spline_ear_r = points_to_svg_cubic_spline(get_contour_pts(ear_r_mask, eps=0.6, min_area=100))

# 8. Eyes
eye_l_dark = (a[140:215, 180:255] > 30) & (r[140:215, 180:255] < 75) & (g[140:215, 180:255] < 75) & (b[140:215, 180:255] < 75)
eye_l_iris = (a[140:215, 180:255] > 30) & (r[140:215, 180:255] > 90) & (g[140:215, 180:255] > 80) & (b[140:215, 180:255] < 85)
eye_l_mask = np.zeros_like(a, dtype=bool)
eye_l_mask[140:215, 180:255] = eye_l_dark | eye_l_iris
eye_l_mask = cv2.morphologyEx(eye_l_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))) > 0
spline_eye_l = points_to_svg_cubic_spline(get_contour_pts(eye_l_mask, eps=0.5, min_area=500))

eye_r_dark = (a[140:215, 290:360] > 30) & (r[140:215, 290:360] < 75) & (g[140:215, 290:360] < 75) & (b[140:215, 290:360] < 75)
eye_r_iris = (a[140:215, 290:360] > 30) & (r[140:215, 290:360] > 90) & (g[140:215, 290:360] > 80) & (b[140:215, 290:360] < 85)
eye_r_mask = np.zeros_like(a, dtype=bool)
eye_r_mask[140:215, 290:360] = eye_r_dark | eye_r_iris
eye_r_mask = cv2.morphologyEx(eye_r_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))) > 0
spline_eye_r = points_to_svg_cubic_spline(get_contour_pts(eye_r_mask, eps=0.5, min_area=500))

# Pupils
pupil_l_mask = np.zeros_like(a, dtype=bool)
pupil_l_mask[150:195, 205:245] = (a[150:195, 205:245] > 30) & (r[150:195, 205:245] < 60) & (g[150:195, 205:245] < 60) & (b[150:195, 205:245] < 60)
pupil_l_mask = cv2.morphologyEx(pupil_l_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))) > 0
spline_pupil_l = points_to_svg_cubic_spline(get_contour_pts(pupil_l_mask, eps=0.5, min_area=200))

pupil_r_mask = np.zeros_like(a, dtype=bool)
pupil_r_mask[150:195, 300:340] = (a[150:195, 300:340] > 30) & (r[150:195, 300:340] < 60) & (g[150:195, 300:340] < 60) & (b[150:195, 300:340] < 60)
pupil_r_mask = cv2.morphologyEx(pupil_r_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))) > 0
spline_pupil_r = points_to_svg_cubic_spline(get_contour_pts(pupil_r_mask, eps=0.5, min_area=200))

# 9. White face & blaze
face_white_mask = np.zeros_like(a, dtype=bool)
face_white_mask[80:260, 150:390] = (a[80:260, 150:390] > 30) & (r[80:260, 150:390] > 185) & (g[80:260, 150:390] > 180) & (b[80:260, 150:390] > 170)
face_white_mask[eye_l_mask] = False
face_white_mask[eye_r_mask] = False
face_white_mask = cv2.morphologyEx(face_white_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))) > 0
spline_face_white = points_to_svg_cubic_spline(get_contour_pts(face_white_mask, eps=0.8, min_area=2000))

# 10. Ginger Crown & Temples
ginger_head_mask = np.zeros_like(a, dtype=bool)
ginger_head_mask[40:260, 150:395] = (a[40:260, 150:395] > 30) & (~face_white_mask[40:260, 150:395]) & (~eye_l_mask[40:260, 150:395]) & (~eye_r_mask[40:260, 150:395])
ginger_head_mask = cv2.morphologyEx(ginger_head_mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))) > 0
spline_ginger_head = points_to_svg_cubic_spline(get_contour_pts(ginger_head_mask, eps=0.8, min_area=3000))

# Build SVG
svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <!-- Multi-stop porcelain and fur shaders -->
    <linearGradient id="gingerBody" x1="20%" y1="10%" x2="80%" y2="90%">
      <stop offset="0%" stop-color="#F6A85D" />
      <stop offset="35%" stop-color="#E58535" />
      <stop offset="70%" stop-color="#D06E22" />
      <stop offset="100%" stop-color="#B35212" />
    </linearGradient>

    <linearGradient id="gingerTail" x1="10%" y1="20%" x2="90%" y2="80%">
      <stop offset="0%" stop-color="#E58535" />
      <stop offset="60%" stop-color="#CB671E" />
      <stop offset="100%" stop-color="#A7480C" />
    </linearGradient>

    <radialGradient id="creamPorcelain" cx="45%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="45%" stop-color="#FAF7F2" />
      <stop offset="80%" stop-color="#EDE6D9" />
      <stop offset="100%" stop-color="#DACFBE" />
    </radialGradient>

    <radialGradient id="pinkEarCavity" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#FDC9BC" />
      <stop offset="50%" stop-color="#F8A796" />
      <stop offset="85%" stop-color="#E88270" />
      <stop offset="100%" stop-color="#D46855" />
    </radialGradient>

    <radialGradient id="amberIrisL" cx="60%" cy="65%" r="55%">
      <stop offset="0%" stop-color="#FEE665" />
      <stop offset="35%" stop-color="#DEB02C" />
      <stop offset="70%" stop-color="#9C7216" />
      <stop offset="100%" stop-color="#3D2605" />
    </radialGradient>

    <radialGradient id="amberIrisR" cx="40%" cy="65%" r="55%">
      <stop offset="0%" stop-color="#FEE665" />
      <stop offset="35%" stop-color="#DEB02C" />
      <stop offset="70%" stop-color="#9C7216" />
      <stop offset="100%" stop-color="#3D2605" />
    </radialGradient>

    <radialGradient id="specularGlint" cx="40%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="1" />
      <stop offset="80%" stop-color="#FFFFFF" stop-opacity="0.9" />
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0" />
    </radialGradient>

    <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="1.2" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <rect width="512" height="512" fill="#0B0F17" />

  <!-- 1. Tail (Behind Flank) -->
  <path d="{spline_tail}" fill="url(#gingerTail)" stroke="#9A420A" stroke-width="0.8" />

  <!-- 2. Left and Right Flanks -->
  <path d="{spline_flank_l}" fill="url(#gingerBody)" stroke="#9A420A" stroke-width="0.8" />
  <path d="{spline_flank_r}" fill="url(#gingerBody)" stroke="#9A420A" stroke-width="0.8" />

  <!-- 3. Central Cream Chest & Body -->
  <path d="{spline_chest}" fill="url(#creamPorcelain)" stroke="#C8BEAD" stroke-width="0.8" />

  <!-- 4. Front Paws (Grounded, flat baseline Y=491) -->
  <path d="{spline_paw_l}" fill="url(#creamPorcelain)" stroke="#C8BEAD" stroke-width="0.9" />
  <!-- Left Paw Toe Clefts -->
  <path d="M 210 468 C 210 478, 209 484, 208 490" stroke="#B8AC98" stroke-width="1.2" fill="none" stroke-linecap="round" />
  <path d="M 233 468 C 234 478, 235 484, 236 490" stroke="#B8AC98" stroke-width="1.2" fill="none" stroke-linecap="round" />

  <path d="{spline_paw_r}" fill="url(#creamPorcelain)" stroke="#C8BEAD" stroke-width="0.9" />
  <!-- Right Paw Toe Clefts -->
  <path d="M 284 468 C 283 478, 282 484, 281 490" stroke="#B8AC98" stroke-width="1.2" fill="none" stroke-linecap="round" />
  <path d="M 307 468 C 308 478, 309 484, 310 490" stroke="#B8AC98" stroke-width="1.2" fill="none" stroke-linecap="round" />

  <!-- 5. Head Base & Ginger Crown -->
  <path d="{spline_head}" fill="url(#creamPorcelain)" stroke="#C8BEAD" stroke-width="0.8" />
  <path d="{spline_ginger_head}" fill="url(#gingerBody)" />

  <!-- Forehead Tabby Stripes -->
  <path d="M 268 85 C 269 110, 270 125, 271 142" stroke="#CB671E" stroke-width="7" stroke-linecap="round" fill="none" opacity="0.8" />
  <path d="M 245 92 C 248 112, 252 125, 255 138" stroke="#CB671E" stroke-width="6" stroke-linecap="round" fill="none" opacity="0.75" />
  <path d="M 292 92 C 289 112, 285 125, 282 138" stroke="#CB671E" stroke-width="6" stroke-linecap="round" fill="none" opacity="0.75" />

  <!-- Inner Ear Cavities -->
  <path d="{spline_ear_l}" fill="url(#pinkEarCavity)" stroke="#C85A48" stroke-width="0.8" />
  <!-- Left Ear Tufts -->
  <path d="M 188 120 C 182 118, 178 122, 172 124" stroke="#FAF7F2" stroke-width="2.5" stroke-linecap="round" fill="none" />
  <path d="M 192 128 C 185 127, 180 131, 175 133" stroke="#FAF7F2" stroke-width="2.2" stroke-linecap="round" fill="none" />

  <path d="{spline_ear_r}" fill="url(#pinkEarCavity)" stroke="#C85A48" stroke-width="0.8" />
  <!-- Right Ear Tufts -->
  <path d="M 348 120 C 354 118, 358 122, 364 124" stroke="#FAF7F2" stroke-width="2.5" stroke-linecap="round" fill="none" />
  <path d="M 344 128 C 351 127, 356 131, 361 133" stroke="#FAF7F2" stroke-width="2.2" stroke-linecap="round" fill="none" />

  <!-- White Forehead Blaze & Chubby Cheeks -->
  <path d="{spline_face_white}" fill="url(#creamPorcelain)" />

  <!-- 6. Amber Eyes -->
  <!-- Left Eye -->
  <g id="leftEyeGroup">
    <path d="{spline_eye_l}" fill="url(#amberIrisL)" stroke="#261704" stroke-width="2.5" />
    <path d="{spline_pupil_l}" fill="#110A03" />
    <!-- Main Specular Highlight -->
    <circle cx="218" cy="162" r="7.5" fill="#FFFFFF" />
    <!-- Secondary Specular Highlight -->
    <circle cx="230" cy="180" r="3.2" fill="#FFFFFF" opacity="0.7" />
  </g>

  <!-- Right Eye -->
  <g id="rightEyeGroup">
    <path d="{spline_eye_r}" fill="url(#amberIrisR)" stroke="#261704" stroke-width="2.5" />
    <path d="{spline_pupil_r}" fill="#110A03" />
    <!-- Main Specular Highlight -->
    <circle cx="312" cy="162" r="7.5" fill="#FFFFFF" />
    <!-- Secondary Specular Highlight -->
    <circle cx="324" cy="180" r="3.2" fill="#FFFFFF" opacity="0.7" />
  </g>

  <!-- 7. Nose & Mouth -->
  <!-- Soft peach nose -->
  <path d="M 264 195 C 267 193, 275 193, 278 195 C 280 197, 274 204, 271 204 C 268 204, 262 197, 264 195 Z" fill="#F89E8C" stroke="#E27560" stroke-width="0.8" />
  <!-- Feline mouth line ω -->
  <path d="M 271 204 L 271 209" stroke="#948475" stroke-width="1.2" stroke-linecap="round" fill="none" />
  <path d="M 260 212 C 264 215, 268 214, 271 209 C 274 214, 278 215, 282 212" stroke="#948475" stroke-width="1.2" stroke-linecap="round" fill="none" />

  <!-- 8. Delicate Whiskers -->
  <!-- Left Whiskers -->
  <path d="M 248 206 C 220 205, 195 212, 178 218" stroke="#FFFFFF" stroke-width="1.2" stroke-linecap="round" fill="none" opacity="0.9" />
  <path d="M 246 211 C 218 214, 192 225, 182 233" stroke="#FFFFFF" stroke-width="1.2" stroke-linecap="round" fill="none" opacity="0.9" />
  <path d="M 247 217 C 222 225, 202 239, 190 248" stroke="#FFFFFF" stroke-width="1.1" stroke-linecap="round" fill="none" opacity="0.85" />

  <!-- Right Whiskers -->
  <path d="M 294 206 C 322 205, 347 212, 364 218" stroke="#FFFFFF" stroke-width="1.2" stroke-linecap="round" fill="none" opacity="0.9" />
  <path d="M 296 211 C 324 214, 350 225, 360 233" stroke="#FFFFFF" stroke-width="1.2" stroke-linecap="round" fill="none" opacity="0.9" />
  <path d="M 295 217 C 320 225, 340 239, 352 248" stroke="#FFFFFF" stroke-width="1.1" stroke-linecap="round" fill="none" opacity="0.85" />
</svg>"""

out_svg = "scratch/meoweko_exact_spline_test.svg"
with open(out_svg, "w") as f:
    f.write(svg_content)
print(f"✅ Saved {out_svg}")

preview_png = "scratch/meoweko_exact_spline_preview.png"
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
print(f"✅ Rendered {preview_png}")

# Create side-by-side
ref = Image.open("mascots/meoweko/meoweko_master_exact_512.png").convert("RGBA")
vec = Image.open(preview_png).convert("RGBA")
comp = Image.new("RGBA", (1024, 512), (11, 15, 23, 255))
comp.paste(ref, (0, 0), ref.split()[3])
comp.paste(vec, (512, 0), vec.split()[3])
comp_path = "scratch/meoweko_spline_side_by_side.png"
comp.save(comp_path, "PNG")
print(f"✅ Saved comparison to {comp_path}")
