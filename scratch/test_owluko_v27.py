import os, sys, re, subprocess, cv2, numpy as np
from PIL import Image

def compute_ssim_numpy(img1, img2):
    C1 = (0.01 * 255)**2
    C2 = (0.03 * 255)**2
    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)
    kernel = cv2.getGaussianKernel(11, 1.5)
    window = np.outer(kernel, kernel.transpose())
    mu1 = cv2.filter2D(img1, -1, window)[5:-5, 5:-5]
    mu2 = cv2.filter2D(img2, -1, window)[5:-5, 5:-5]
    mu1_sq = mu1**2
    mu2_sq = mu2**2
    mu1_mu2 = mu1 * mu2
    sigma1_sq = cv2.filter2D(img1**2, -1, window)[5:-5, 5:-5] - mu1_sq
    sigma2_sq = cv2.filter2D(img2**2, -1, window)[5:-5, 5:-5] - mu2_sq
    sigma12 = cv2.filter2D(img1 * img2, -1, window)[5:-5, 5:-5] - mu1_mu2
    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))
    return ssim_map

def render_svg_chrome(svg_str, out_png="scratch/temp_owluko_v27.png"):
    abs_out = os.path.abspath(out_png)
    html_wrap = "scratch/temp_wrap_v27.html"
    with open(html_wrap, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html><html><head><style>
html, body {{ margin: 0; padding: 0; width: 512px; height: 512px; overflow: hidden; background: transparent; }}
svg {{ display: block; width: 512px; height: 512px; }}
</style></head><body>{svg_str}</body></html>""")
    cmd = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--screenshot={abs_out}",
        "--window-size=512,512",
        "--default-background-color=00000000",
        f"file://{os.path.abspath(html_wrap)}"
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return abs_out

def evaluate(rendered_png, ref_png="mascots/owluko/owluko_master_exact_512.png"):
    ref = np.array(Image.open(ref_png).convert("RGBA"))
    vec = np.array(Image.open(rendered_png).convert("RGBA"))
    inter = (ref[:, :, 3] > 20) & (vec[:, :, 3] > 20)
    iou = inter.sum() / (((ref[:, :, 3] > 20) | (vec[:, :, 3] > 20)).sum() + 1e-6)

    ref_gray = cv2.cvtColor(ref[:, :, :3], cv2.COLOR_BGR2GRAY)
    vec_gray = cv2.cvtColor(vec[:, :, :3], cv2.COLOR_BGR2GRAY)
    ssim_map = compute_ssim_numpy(ref_gray, vec_gray)
    ssim_val = np.pad(ssim_map, 5, mode='edge')[inter].mean()

    ref_flat = ref[:, :, :3][inter].astype(np.float32).ravel()
    vec_flat = vec[:, :, :3][inter].astype(np.float32).ravel()
    ncc = np.corrcoef(ref_flat, vec_flat)[0, 1]

    ref_lab = cv2.cvtColor(ref[:, :, :3], cv2.COLOR_BGR2LAB).astype(np.float32)
    vec_lab = cv2.cvtColor(vec[:, :, :3], cv2.COLOR_BGR2LAB).astype(np.float32)
    delta_e = np.sqrt(np.sum((ref_lab - vec_lab)**2, axis=2))[inter].mean()
    mse = np.mean((ref[:, :, :3][inter].astype(np.float32) - vec[:, :, :3][inter].astype(np.float32))**2)

    return {"iou": iou, "ssim": ssim_val, "ncc": ncc, "delta_e": delta_e, "mse": mse}

sil_d = "M 272 40 L 237 40 L 216 44 L 207 48 L 201 49 L 185 57 L 168 69 L 155 82 L 147 94 L 145 95 L 132 119 L 126 134 L 124 145 L 120 155 L 120 162 L 116 174 L 115 183 L 103 194 L 95 213 L 92 231 L 90 235 L 90 246 L 88 255 L 87 271 L 90 314 L 96 339 L 105 359 L 109 363 L 110 366 L 119 374 L 127 377 L 132 382 L 144 400 L 151 407 L 168 421 L 186 430 L 192 437 L 188 451 L 183 459 L 178 462 L 164 465 L 158 470 L 155 479 L 157 485 L 160 488 L 169 489 L 176 485 L 180 485 L 186 489 L 198 489 L 206 485 L 214 485 L 220 489 L 224 489 L 231 486 L 233 482 L 231 469 L 221 461 L 217 451 L 218 445 L 224 441 L 242 443 L 293 441 L 297 446 L 297 455 L 293 461 L 283 470 L 280 476 L 280 484 L 283 488 L 293 489 L 300 485 L 308 485 L 314 489 L 324 489 L 329 485 L 337 485 L 340 487 L 349 488 L 352 487 L 356 483 L 356 474 L 351 466 L 338 462 L 329 456 L 323 442 L 323 434 L 327 429 L 334 427 L 337 424 L 344 421 L 356 411 L 372 395 L 380 382 L 385 377 L 391 376 L 397 373 L 404 366 L 407 358 L 411 353 L 411 350 L 416 339 L 416 334 L 421 317 L 424 290 L 424 260 L 420 228 L 416 217 L 416 213 L 409 197 L 409 194 L 396 183 L 392 166 L 391 155 L 389 152 L 385 135 L 382 130 L 379 120 L 364 93 L 347 73 L 331 60 L 311 50 L 305 49 L 293 44 L 277 42 Z"

svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" style="background: transparent;">
  <defs>
    <!-- Master Body Silhouette Clip -->
    <clipPath id="bodyClip">
      <path d="{sil_d}" />
    </clipPath>

    <!-- Master Porcelain Body Gradient -->
    <linearGradient id="bodyGrad" x1="26%" y1="5%" x2="74%" y2="95%">
      <stop offset="0%" stop-color="#FBF2E8" />
      <stop offset="16%" stop-color="#F4E7DA" />
      <stop offset="36%" stop-color="#E6D4C4" />
      <stop offset="60%" stop-color="#D5C1AF" />
      <stop offset="80%" stop-color="#A5907E" />
      <stop offset="100%" stop-color="#6B5747" />
    </linearGradient>

    <!-- Cranial Dome Specular Highlight -->
    <radialGradient id="cranialHl" cx="42%" cy="17%" r="35%">
      <stop offset="0%" stop-color="#FFFDF9" stop-opacity="0.32" />
      <stop offset="50%" stop-color="#F7EEE4" stop-opacity="0.12" />
      <stop offset="100%" stop-color="#ECE0D4" stop-opacity="0" />
    </radialGradient>

    <!-- Upper Right Head Shadow -->
    <radialGradient id="headRightShadow" cx="72%" cy="18%" r="42%">
      <stop offset="0%" stop-color="#7A6250" stop-opacity="0.30" />
      <stop offset="60%" stop-color="#7A6250" stop-opacity="0.12" />
      <stop offset="100%" stop-color="#7A6250" stop-opacity="0" />
    </radialGradient>

    <!-- Soft Right Brow Ambient Falloff (Natural shadow, no hard boundary) -->
    <radialGradient id="rBrowSoft" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#806856" stop-opacity="0.22" />
      <stop offset="70%" stop-color="#806856" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#806856" stop-opacity="0" />
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

    <!-- Left Amber Iris -->
    <linearGradient id="amberEyeL" x1="50%" y1="10%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#4E280C" />
      <stop offset="40%" stop-color="#6B3A12" />
      <stop offset="70%" stop-color="#B87D2A" />
      <stop offset="90%" stop-color="#EAA648" />
      <stop offset="100%" stop-color="#D48E32" />
    </linearGradient>

    <!-- Right Amber Iris -->
    <linearGradient id="amberEyeR" x1="50%" y1="10%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#3D1D06" />
      <stop offset="40%" stop-color="#552C0D" />
      <stop offset="70%" stop-color="#9C6320" />
      <stop offset="90%" stop-color="#D69738" />
      <stop offset="100%" stop-color="#B87724" />
    </linearGradient>

    <!-- Pupil -->
    <radialGradient id="pupilGrad" cx="50%" cy="45%" r="50%">
      <stop offset="0%" stop-color="#180A03" />
      <stop offset="70%" stop-color="#341806" />
      <stop offset="100%" stop-color="#5A2E0C" stop-opacity="0" />
    </radialGradient>

    <!-- Left Porcelain Eyelid Hood -->
    <linearGradient id="eyelidHoodL" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#FFF9F4" />
      <stop offset="55%" stop-color="#F4E7DC" />
      <stop offset="85%" stop-color="#DCBEA8" />
      <stop offset="100%" stop-color="#C2A28C" />
    </linearGradient>

    <!-- Right Porcelain Eyelid Hood -->
    <linearGradient id="eyelidHoodR" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#EFE0D2" />
      <stop offset="55%" stop-color="#DCBEAA" />
      <stop offset="85%" stop-color="#BF9E88" />
      <stop offset="100%" stop-color="#A5846E" />
    </linearGradient>

    <!-- Eyelid Cast Shadow on Eyeball -->
    <linearGradient id="eyeShadow" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#140602" stop-opacity="0.75" />
      <stop offset="70%" stop-color="#3A1A04" stop-opacity="0.30" />
      <stop offset="100%" stop-color="#7C3B07" stop-opacity="0" />
    </linearGradient>

    <!-- Seamless Porcelain Beak Gradient -->
    <linearGradient id="beakGrad" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#F6EAE0" />
      <stop offset="35%" stop-color="#DFCBBD" />
      <stop offset="70%" stop-color="#B29983" />
      <stop offset="100%" stop-color="#7E6652" />
    </linearGradient>

    <!-- Soft Under-Beak Ambient Shadow -->
    <radialGradient id="beakTipShadow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#6B503D" stop-opacity="0.40" />
      <stop offset="60%" stop-color="#6B503D" stop-opacity="0.15" />
      <stop offset="100%" stop-color="#6B503D" stop-opacity="0" />
    </radialGradient>

    <!-- Soft Right Orbit Shadow -->
    <radialGradient id="rightOrbitShadow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#806856" stop-opacity="0.25" />
      <stop offset="65%" stop-color="#806856" stop-opacity="0.10" />
      <stop offset="100%" stop-color="#806856" stop-opacity="0" />
    </radialGradient>

    <!-- Continuous Volumetric Feet Gradients -->
    <linearGradient id="lFootGrad" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#806B58" />
      <stop offset="30%" stop-color="#A28974" />
      <stop offset="70%" stop-color="#C8B19C" />
      <stop offset="90%" stop-color="#B09883" />
      <stop offset="100%" stop-color="#78614E" />
    </linearGradient>
    <linearGradient id="rFootGrad" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#6E5745" />
      <stop offset="30%" stop-color="#88705C" />
      <stop offset="70%" stop-color="#AB937F" />
      <stop offset="90%" stop-color="#947C68" />
      <stop offset="100%" stop-color="#624E3D" />
    </linearGradient>
  </defs>

  <!-- 1. Master Base Silhouette Capsule -->
  <path d="{sil_d}" fill="url(#bodyGrad)" />

  <!-- 2. Clipped Body 3D Volume Layers -->
  <g clip-path="url(#bodyClip)">
    <!-- Cranial Specular Dome -->
    <ellipse cx="200" cy="87" rx="95" ry="65" fill="url(#cranialHl)" />

    <!-- Upper Right Head Shadow -->
    <ellipse cx="340" cy="95" rx="90" ry="70" fill="url(#headRightShadow)" />
    <!-- Subtle Right Forehead Transition -->
    <ellipse cx="310" cy="118" rx="55" ry="32" fill="url(#rBrowSoft)" />

    <!-- Breast / Chest Soft Illumination -->
    <ellipse cx="244" cy="270" rx="115" ry="88" fill="url(#chestHl)" />

    <!-- Left Wing Lateral Highlight -->
    <path d="M 88 180 C 88 180, 115 190, 118 270 C 120 340, 95 380, 95 380 C 86 340, 86 230, 88 180 Z" fill="url(#lWingGrad)" />
    <!-- Left Wing Soft Furrow -->
    <path d="M 125 185 C 135 225, 138 280, 130 355 C 128 370, 122 385, 118 395" stroke="#B8A492" stroke-width="2.2" stroke-linecap="round" opacity="0.25" fill="none" />

    <!-- Right Flank Ambient Occlusion -->
    <path d="M 330 180 C 375 210, 424 265, 420 345 C 416 385, 375 420, 345 425 C 380 395, 385 300, 345 200 Z" fill="url(#rWingShadow)" />
    <!-- Right Wing Furrow -->
    <path d="M 368 185 C 362 225, 362 280, 368 355 C 370 370, 375 385, 380 395" stroke="#66503E" stroke-width="2.5" stroke-linecap="round" opacity="0.32" fill="none" />

    <!-- Lower Belly Shading Gradient -->
    <ellipse cx="254" cy="405" rx="85" ry="30" fill="#755F4E" opacity="0.25" />

    <!-- Feet 3D Modeling (Seamless Organic Avian Feet) -->
    <!-- Left Foot Whole Organic Mesh -->
    <path d="M 155 479 L 157 485 L 160 488 L 169 489 L 176 485 L 180 485 L 186 489 L 198 489 L 206 485 L 214 485 L 220 489 L 228 488 L 231 486 L 233 482 L 231 469 L 227 465 L 225 465 L 219 458 L 217 451 L 217 447 L 221 442 L 224 441 L 239 442 L 239 435 L 191 435 L 192 439 L 190 442 L 190 445 L 185 457 L 178 462 L 174 462 L 171 464 L 167 464 L 162 466 L 158 470 Z" fill="url(#lFootGrad)" />
    <!-- Left Foot Knuckle Highlights -->
    <ellipse cx="164" cy="476" rx="7.5" ry="4.5" fill="#FFFFFF" opacity="0.22" />
    <ellipse cx="189" cy="469" rx="8.5" ry="5.5" fill="#FFFFFF" opacity="0.26" />
    <ellipse cx="220" cy="476" rx="7.5" ry="4.5" fill="#FFFFFF" opacity="0.20" />
    <!-- Left Foot Soft Crevices -->
    <ellipse cx="179" cy="475" rx="2.5" ry="9" fill="#2D1B0E" opacity="0.22" />
    <ellipse cx="206" cy="473" rx="2.5" ry="9" fill="#2D1B0E" opacity="0.22" />

    <!-- Right Foot Whole Organic Mesh -->
    <path d="M 270 435 L 270 442 L 293 441 L 297 446 L 297 455 L 293 461 L 283 470 L 280 476 L 280 484 L 283 488 L 293 489 L 300 485 L 308 485 L 314 489 L 324 489 L 329 485 L 337 485 L 340 487 L 349 488 L 352 487 L 356 483 L 356 474 L 353 468 L 351 466 L 338 462 L 332 459 L 329 456 L 323 442 L 323 435 Z" fill="url(#rFootGrad)" />
    <!-- Right Foot Knuckle Highlights -->
    <ellipse cx="288" cy="476" rx="7.5" ry="4.5" fill="#FFFFFF" opacity="0.18" />
    <ellipse cx="315" cy="469" rx="8.5" ry="5.5" fill="#FFFFFF" opacity="0.22" />
    <ellipse cx="345" cy="476" rx="7.5" ry="4.5" fill="#FFFFFF" opacity="0.16" />
    <!-- Right Foot Soft Crevices -->
    <ellipse cx="304" cy="473" rx="2.5" ry="9" fill="#25160A" opacity="0.22" />
    <ellipse cx="330" cy="475" rx="2.5" ry="9" fill="#25160A" opacity="0.22" />
  </g>

  <!-- 3. Facial Depressions & Shading -->
  <!-- Inner Right Orbit Wall -->
  <ellipse cx="272" cy="165" rx="22" ry="26" fill="url(#rightOrbitShadow)" />

  <!-- 4. Sleepy Hooded Glassy Amber Eyes -->
  <!-- Left Eye -->
  <g id="left_eye">
    <!-- Amber Iris (Half-Moon Aperture) -->
    <path d="M 169 142 L 167 150 L 169 163 L 174 171 L 180 176 L 185 178 L 199 179 L 206 176 L 214 170 L 219 164 L 223 156 L 224 148 L 215 143 L 190 139 L 177 140 Z" fill="url(#amberEyeL)" />
    <!-- Pupil -->
    <ellipse cx="196" cy="155" rx="14" ry="12" fill="url(#pupilGrad)" />
    <!-- Lower Golden Luminous Rim -->
    <path d="M 176 170 C 182 176, 194 178, 206 177 C 214 176, 220 171, 222 165 C 218 171, 208 174, 196 174 C 186 174, 180 171, 176 170 Z" fill="#FFE294" opacity="0.65" />
    <!-- Eyelid Cast Shadow on eyeball -->
    <path d="M 169 142 L 177 140 L 190 139 L 215 143 L 224 148 L 223 152 L 190 146 L 168 147 Z" fill="url(#eyeShadow)" />
    
    <!-- Specular Reflection Glint (Calibrated to Ref X=185.5, Y=142.5) -->
    <ellipse cx="186" cy="143" rx="2.5" ry="2.0" fill="#FFFFFF" opacity="0.92" />
    <ellipse cx="186" cy="143" rx="4.0" ry="3.0" fill="#FFF8E0" opacity="0.40" />

    <!-- Porcelain Upper Eyelid Hood (Round Arched Dome) -->
    <path d="M 166 142 C 168 112, 218 112, 224 148 L 215 143 L 190 139 L 177 140 Z" fill="url(#eyelidHoodL)" />
    <!-- Eyelid Lower Porcelain Edge Highlight -->
    <path d="M 167 143 C 182 141, 205 142, 223 147" stroke="#FFFDF8" stroke-width="1.0" stroke-linecap="round" opacity="0.55" fill="none" />
  </g>

  <!-- Right Eye -->
  <g id="right_eye">
    <!-- Amber Iris -->
    <path d="M 282 144 L 279 146 L 280 155 L 282 162 L 292 174 L 294 174 L 303 179 L 316 180 L 327 176 L 337 166 L 340 151 L 339 145 L 334 141 L 313 139 L 296 141 Z" fill="url(#amberEyeR)" />
    <!-- Pupil -->
    <ellipse cx="314" cy="155" rx="14" ry="12" fill="url(#pupilGrad)" />
    <!-- Lower Golden Luminous Rim -->
    <path d="M 292 171 C 298 177, 310 179, 324 177 C 333 175, 338 170, 340 164 C 336 170, 326 173, 314 173 C 304 173, 296 171, 292 171 Z" fill="#FFDC85" opacity="0.70" />
    <!-- Eyelid Cast Shadow -->
    <path d="M 285 145 L 296 141 L 313 139 L 334 141 L 339 145 L 338 150 L 313 146 L 284 149 Z" fill="url(#eyeShadow)" />

    <!-- Specular Highlight Glint (Top rim) -->
    <ellipse cx="304" cy="144" rx="2.2" ry="1.8" fill="#FFE8C2" opacity="0.70" />
    <!-- Luminous Golden Amber Caustic Reflection in Lower Right Iris -->
    <ellipse cx="327" cy="164" rx="3.5" ry="4.0" fill="#FFC966" opacity="0.85" />
    <ellipse cx="327" cy="164" rx="1.6" ry="2.0" fill="#FFFFFF" opacity="0.90" />

    <!-- Porcelain Upper Eyelid Hood -->
    <path d="M 284 144 C 286 112, 336 112, 340 145 L 334 141 L 313 139 L 296 141 Z" fill="url(#eyelidHoodR)" />
    <!-- Eyelid Lower Porcelain Edge Highlight -->
    <path d="M 286 144 C 303 141, 324 142, 339 145" stroke="#F6ECE0" stroke-width="1.0" stroke-linecap="round" opacity="0.50" fill="none" />
  </g>

  <!-- 5. Seamless Rounded Porcelain Beak Cone -->
  <g id="beak">
    <!-- Cast Shadow beneath beak tip onto breast -->
    <ellipse cx="254" cy="208" rx="15" ry="7" fill="url(#beakTipShadow)" />
    <!-- Beak Body Teardrop/Cone (starts at Y=146 between eyes, ends at Y=204) -->
    <path d="M 254 146 C 246 156, 241 175, 242 189 C 243 198, 247 205, 254 205 C 261 205, 265 198, 266 189 C 267 175, 262 156, 254 146 Z" fill="url(#beakGrad)" />
    <!-- Beak Longitudinal Highlight Ridge -->
    <path d="M 253 148 C 253 162, 252 182, 253 200" stroke="#FFFFFF" stroke-width="1.3" stroke-linecap="round" opacity="0.32" fill="none" />
  </g>
</svg>"""

rendered_png = render_svg_chrome(svg_content)
res = evaluate(rendered_png)
print(f"[V27] IoU: {res['iou']*100:.2f}%, SSIM: {res['ssim']*100:.2f}%, NCC: {res['ncc']*100:.2f}%, Delta E: {res['delta_e']:.2f}, MSE: {res['mse']:.1f}")

with open("mascots/owluko/owluko_master_exact_512.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)
