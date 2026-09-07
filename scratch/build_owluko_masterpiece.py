import os, sys, subprocess, re, cv2, numpy as np
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

def render_svg_chrome(svg_path, out_png):
    abs_svg = os.path.abspath(svg_path)
    abs_out = os.path.abspath(out_png)
    html_wrap = f"scratch/temp_wrap_{os.path.basename(svg_path)}.html"
    with open(abs_svg, "r", encoding="utf-8") as f:
        svg_content = f.read()
    svg_content = re.sub(r'style="[^"]*background-color:\s*#[^;"]+;?[^"]*"', 'style="background: transparent; overflow: visible;"', svg_content)
    svg_content = re.sub(r'style="[^"]*background:\s*#[^;"]+;?[^"]*"', 'style="background: transparent; overflow: visible;"', svg_content)
    with open(html_wrap, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html><html><head><style>
html, body {{ margin: 0; padding: 0; width: 512px; height: 512px; overflow: hidden; background: transparent; }}
svg {{ display: block; width: 512px; height: 512px; }}
</style></head><body>{svg_content}</body></html>""")
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
    ref_mask = ref[:, :, 3] > 20
    vec_mask = vec[:, :, 3] > 20
    inter = ref_mask & vec_mask
    iou = inter.sum() / ((ref_mask | vec_mask).sum() + 1e-6)

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
    psnr = 10 * np.log10(255**2 / (mse + 1e-6))
    return {"iou": iou, "ssim": ssim_val, "ncc": ncc, "delta_e": delta_e, "mse": mse, "psnr": psnr}

def create_owluko_v21_svg(path="scratch/test_owluko_v21.svg"):
    sil_d = "M 272 40 L 237 40 L 216 44 L 207 48 L 201 49 L 185 57 L 168 69 L 155 82 L 147 94 L 145 95 L 132 119 L 126 134 L 124 145 L 120 155 L 120 162 L 116 174 L 115 183 L 103 194 L 95 213 L 92 231 L 90 235 L 90 246 L 88 255 L 87 271 L 90 314 L 96 339 L 105 359 L 109 363 L 110 366 L 119 374 L 127 377 L 132 382 L 144 400 L 151 407 L 168 421 L 186 430 L 192 437 L 188 451 L 183 459 L 178 462 L 164 465 L 158 470 L 155 479 L 157 485 L 160 488 L 169 489 L 176 485 L 180 485 L 186 489 L 198 489 L 206 485 L 214 485 L 220 489 L 224 489 L 231 486 L 233 482 L 231 469 L 221 461 L 217 451 L 218 445 L 224 441 L 242 443 L 293 441 L 297 446 L 297 455 L 293 461 L 283 470 L 280 476 L 280 484 L 283 488 L 293 489 L 300 485 L 308 485 L 314 489 L 324 489 L 329 485 L 337 485 L 340 487 L 349 488 L 352 487 L 356 483 L 356 474 L 351 466 L 338 462 L 329 456 L 323 442 L 323 434 L 327 429 L 334 427 L 337 424 L 344 421 L 356 411 L 372 395 L 380 382 L 385 377 L 391 376 L 397 373 L 404 366 L 407 358 L 411 353 L 411 350 L 416 339 L 416 334 L 421 317 L 424 290 L 424 260 L 420 228 L 416 217 L 416 213 L 409 197 L 409 194 L 396 183 L 392 166 L 391 155 L 389 152 L 385 135 L 382 130 L 379 120 L 364 93 L 347 73 L 331 60 L 311 50 L 305 49 L 293 44 L 277 42 Z"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" style="background: transparent;">
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
      <stop offset="0%" stop-color="#7A6250" stop-opacity="0.32" />
      <stop offset="60%" stop-color="#7A6250" stop-opacity="0.14" />
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

    <!-- Left Eye Amber Iris Gradient (Angled with Radial Glow) -->
    <radialGradient id="amberEyeL" cx="42%" cy="60%" r="58%">
      <stop offset="0%" stop-color="#DF9B34" />
      <stop offset="35%" stop-color="#B86F1E" />
      <stop offset="70%" stop-color="#64350E" />
      <stop offset="100%" stop-color="#381B06" />
    </radialGradient>

    <!-- Right Eye Amber Iris Gradient -->
    <radialGradient id="amberEyeR" cx="48%" cy="62%" r="58%">
      <stop offset="0%" stop-color="#C88226" />
      <stop offset="35%" stop-color="#9E5814" />
      <stop offset="70%" stop-color="#552B0A" />
      <stop offset="100%" stop-color="#2D1303" />
    </radialGradient>

    <!-- Left Porcelain Eyelid Hood -->
    <linearGradient id="eyelidHoodL" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#FFF9F4" />
      <stop offset="55%" stop-color="#F4E7DC" />
      <stop offset="85%" stop-color="#DCBEA8" />
      <stop offset="100%" stop-color="#70441D" />
    </linearGradient>

    <!-- Right Porcelain Eyelid Hood -->
    <linearGradient id="eyelidHoodR" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#EFE0D2" />
      <stop offset="55%" stop-color="#DCBEAA" />
      <stop offset="85%" stop-color="#BF9E88" />
      <stop offset="100%" stop-color="#5E3615" />
    </linearGradient>

    <!-- Eyelid Cast Shadow on Eyeball -->
    <linearGradient id="eyeShadow" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#120601" stop-opacity="0.80" />
      <stop offset="60%" stop-color="#3A1A04" stop-opacity="0.45" />
      <stop offset="100%" stop-color="#7C3B07" stop-opacity="0" />
    </linearGradient>

    <!-- Seamless Porcelain Beak Gradient -->
    <linearGradient id="beakGrad" x1="25%" y1="0%" x2="75%" y2="100%">
      <stop offset="0%" stop-color="#FAF0E4" />
      <stop offset="25%" stop-color="#EAD7C5" />
      <stop offset="65%" stop-color="#BA9E86" />
      <stop offset="100%" stop-color="#7A604C" />
    </linearGradient>

    <!-- Soft Under-Beak Ambient Shadow -->
    <radialGradient id="beakTipShadow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#6B503D" stop-opacity="0.45" />
      <stop offset="60%" stop-color="#6B503D" stop-opacity="0.18" />
      <stop offset="100%" stop-color="#6B503D" stop-opacity="0" />
    </radialGradient>

    <!-- Soft Right Orbit Shadow -->
    <radialGradient id="rightOrbitShadow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#806856" stop-opacity="0.30" />
      <stop offset="65%" stop-color="#806856" stop-opacity="0.12" />
      <stop offset="100%" stop-color="#806856" stop-opacity="0" />
    </radialGradient>

    <!-- Right Brow & Forehead Shadow -->
    <radialGradient id="rBrowShadow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#806550" stop-opacity="0.38" />
      <stop offset="60%" stop-color="#806550" stop-opacity="0.18" />
      <stop offset="100%" stop-color="#806550" stop-opacity="0" />
    </radialGradient>

    <!-- True 3D Left Foot Volumetric Cylindrical Gradient -->
    <linearGradient id="lFootGrad" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#806A56" />
      <stop offset="25%" stop-color="#A8907A" />
      <stop offset="65%" stop-color="#D2BAA4" />
      <stop offset="85%" stop-color="#B09680" />
      <stop offset="100%" stop-color="#745C48" />
    </linearGradient>

    <!-- True 3D Right Foot Volumetric Gradient -->
    <linearGradient id="rFootGrad" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#664F3C" />
      <stop offset="25%" stop-color="#886E58" />
      <stop offset="65%" stop-color="#AC947E" />
      <stop offset="85%" stop-color="#8E745E" />
      <stop offset="100%" stop-color="#584230" />
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

    <!-- Breast / Chest Soft Illumination -->
    <ellipse cx="244" cy="270" rx="115" ry="88" fill="url(#chestHl)" />

    <!-- Left Wing Lateral Highlight -->
    <path d="M 88 180 C 88 180, 115 190, 118 270 C 120 340, 95 380, 95 380 C 86 340, 86 230, 88 180 Z" fill="url(#lWingGrad)" />
    <!-- Left Wing Furrow Line -->
    <path d="M 125 185 C 135 225, 138 280, 130 355 C 128 370, 122 385, 118 395" stroke="#B8A492" stroke-width="2.5" stroke-linecap="round" opacity="0.30" fill="none" />

    <!-- Right Flank Ambient Occlusion -->
    <path d="M 330 180 C 375 210, 424 265, 420 345 C 416 385, 375 420, 345 425 C 380 395, 385 300, 345 200 Z" fill="url(#rWingShadow)" />
    <!-- Right Wing Furrow Line -->
    <path d="M 368 185 C 362 225, 362 280, 368 355 C 370 370, 375 385, 380 395" stroke="#66503E" stroke-width="3" stroke-linecap="round" opacity="0.40" fill="none" />

    <!-- Lower Belly Shading Gradient (Softened to avoid leg occlusion) -->
    <ellipse cx="254" cy="405" rx="85" ry="30" fill="#755F4E" opacity="0.22" />
    <ellipse cx="256" cy="432" rx="60" ry="14" fill="#523D2C" opacity="0.25" />

    <!-- Feet 3D Modeling (Seamless Organic Avian Feet) -->
    <!-- Left Foot Whole Organic Mesh -->
    <path d="M 155 479 L 157 485 L 160 488 L 169 489 L 176 485 L 180 485 L 186 489 L 198 489 L 206 485 L 214 485 L 220 489 L 228 488 L 231 486 L 233 482 L 231 469 L 227 465 L 225 465 L 219 458 L 217 451 L 217 447 L 221 442 L 224 441 L 239 442 L 239 435 L 191 435 L 192 439 L 190 442 L 190 445 L 185 457 L 178 462 L 174 462 L 171 464 L 167 464 L 162 466 L 158 470 Z" fill="url(#lFootGrad)" />
    <!-- Left Leg Stub Keylight Highlight (Cylindrical 3D Falloff) -->
    <path d="M 191 437 C 195 442, 196 450, 194 458 C 190 458, 187 450, 188 440 Z" fill="#FFFFFF" opacity="0.22" />
    <!-- Left Foot Knuckle Highlights (Calibrated to Ref Peaks) -->
    <ellipse cx="168" cy="470" rx="8.5" ry="5.5" fill="#FFFFFF" opacity="0.26" />
    <ellipse cx="192" cy="467" rx="9.5" ry="6.5" fill="#FFFFFF" opacity="0.32" />
    <ellipse cx="220" cy="470" rx="8.5" ry="5.5" fill="#FFFFFF" opacity="0.26" />
    <!-- Left Foot Crevices (Calibrated falloffs matching measured values) -->
    <path d="M 180 467 C 181 474, 180 481, 179 485" stroke="#5C4533" stroke-width="2.5" stroke-linecap="round" opacity="0.45" fill="none" />
    <path d="M 207 467 C 208 474, 208 481, 208 485" stroke="#4A3423" stroke-width="2.5" stroke-linecap="round" opacity="0.55" fill="none" />

    <!-- Right Foot Whole Organic Mesh -->
    <path d="M 270 435 L 270 442 L 293 441 L 297 446 L 297 455 L 293 461 L 283 470 L 280 476 L 280 484 L 283 488 L 293 489 L 300 485 L 308 485 L 314 489 L 324 489 L 329 485 L 337 485 L 340 487 L 349 488 L 352 487 L 356 483 L 356 474 L 353 468 L 351 466 L 338 462 L 332 459 L 329 456 L 323 442 L 323 435 Z" fill="url(#rFootGrad)" />
    <!-- Right Foot Knuckle Highlights (Calibrated to Ref Peaks) -->
    <ellipse cx="291" cy="470" rx="8.0" ry="5.0" fill="#FFFFFF" opacity="0.20" />
    <ellipse cx="318" cy="467" rx="9.0" ry="6.0" fill="#FFFFFF" opacity="0.25" />
    <ellipse cx="347" cy="470" rx="8.0" ry="5.0" fill="#FFFFFF" opacity="0.18" />
    <!-- Right Foot Crevices -->
    <path d="M 305 467 C 305 474, 305 481, 305 485" stroke="#3D2B1C" stroke-width="2.5" stroke-linecap="round" opacity="0.50" fill="none" />
    <path d="M 332 467 C 332 474, 332 481, 332 485" stroke="#3D2B1C" stroke-width="2.5" stroke-linecap="round" opacity="0.50" fill="none" />
  </g>

  <!-- 3. Facial Depressions & Shading -->
  <ellipse cx="272" cy="165" rx="22" ry="26" fill="url(#rightOrbitShadow)" />
  <ellipse cx="300" cy="105" rx="55" ry="32" fill="url(#rBrowShadow)" />
  <ellipse cx="195" cy="155" rx="36" ry="30" fill="#9C826E" opacity="0.08" />

  <!-- 4. Sleepy Hooded Glassy Amber Eyes -->
  <!-- Left Eye -->
  <g id="left_eye">
    <!-- Amber Iris Sphere -->
    <path d="M 169 142 L 167 150 L 169 163 L 174 171 L 180 176 L 185 178 L 199 179 L 206 176 L 214 170 L 219 164 L 223 156 L 224 148 L 215 143 L 190 139 L 177 140 Z" fill="url(#amberEyeL)" />
    <!-- Pupil Core Depth -->
    <ellipse cx="196" cy="155" rx="8.5" ry="10" fill="#1C0A02" opacity="0.75" />
    <!-- Lower Glowing Honey Amber Crescent -->
    <path d="M 174 162 C 182 173, 204 175, 218 165 C 213 173, 198 178, 185 177 C 178 175, 174 168, 174 162 Z" fill="#EFA038" opacity="0.55" />
    <!-- Eyelid Cast Shadow on Eyeball -->
    <path d="M 169 142 L 177 140 L 190 139 L 215 143 L 224 148 L 223 154 L 190 148 L 168 149 Z" fill="url(#eyeShadow)" />
    <!-- Specular Reflection Glint (3D Ref: Top-Left under eyelid X=180, Y=145) -->
    <ellipse cx="180" cy="145" rx="3.0" ry="2.2" fill="#FFFFFF" opacity="0.95" />
    <ellipse cx="180" cy="145" rx="4.5" ry="3.2" fill="#FFEBB0" opacity="0.35" />
    <!-- Secondary Soft Glint (Lower Right X=219, Y=170) -->
    <ellipse cx="219" cy="170" rx="2.4" ry="3.2" fill="#FFF2D6" opacity="0.85" />
    <!-- Porcelain Upper Eyelid Hood -->
    <path d="M 166 142 C 168 112, 218 112, 224 148 L 215 143 L 190 139 L 177 140 Z" fill="url(#eyelidHoodL)" />
    <ellipse cx="195" cy="126" rx="14" ry="6" fill="#FFFFFF" opacity="0.18" />
  </g>

  <!-- Right Eye -->
  <g id="right_eye">
    <!-- Amber Iris Sphere -->
    <path d="M 282 144 L 279 146 L 280 155 L 282 162 L 292 174 L 294 174 L 303 179 L 316 180 L 327 176 L 337 166 L 340 151 L 339 145 L 334 141 L 313 139 L 296 141 Z" fill="url(#amberEyeR)" />
    <!-- Pupil Core Depth -->
    <ellipse cx="309" cy="155" rx="8.5" ry="10" fill="#140601" opacity="0.75" />
    <!-- Lower Glowing Crescent -->
    <path d="M 288 165 C 300 175, 320 174, 330 162 C 328 170, 316 177, 304 177 C 295 175, 290 170, 288 165 Z" fill="#E2902A" opacity="0.45" />
    <!-- Eyelid Cast Shadow -->
    <path d="M 285 145 L 296 141 L 313 139 L 334 141 L 339 145 L 338 152 L 313 148 L 284 152 Z" fill="url(#eyeShadow)" />
    <!-- Specular Reflection Glint (3D Ref: X=326, Y=165) -->
    <ellipse cx="326" cy="165" rx="2.6" ry="3.6" fill="#FFFFFF" opacity="0.90" />
    <ellipse cx="326" cy="165" rx="4.0" ry="4.8" fill="#FFE2A0" opacity="0.40" />
    <!-- Porcelain Upper Eyelid Hood -->
    <path d="M 284 144 C 286 112, 336 112, 340 145 L 334 141 L 313 139 L 296 141 Z" fill="url(#eyelidHoodR)" />
    <ellipse cx="310" cy="127" rx="13" ry="5" fill="#FFFFFF" opacity="0.14" />
  </g>

  <!-- 5. Seamless Rounded Porcelain Beak Cone (Y: 148 to 207) -->
  <g id="beak">
    <!-- Cast Shadow beneath beak tip onto breast -->
    <ellipse cx="254" cy="209" rx="14" ry="7" fill="url(#beakTipShadow)" />
    <!-- Full Beak Cone from Brow Saddle Y=148 down to Tip Y=207 -->
    <path d="M 252 148 C 244 156, 240 172, 241 190 C 242 199, 247 207, 254 207 C 261 207, 265 199, 266 190 C 267 172, 263 156, 255 148 Z" fill="url(#beakGrad)" />
    <!-- Longitudinal Soft Ridge Highlight -->
    <path d="M 253 150 C 253 165, 253 188, 253 203" stroke="#FFFFFF" stroke-width="1.2" stroke-linecap="round" opacity="0.35" fill="none" />
    <!-- Right Beak Flank Ambient Shadow -->
    <path d="M 253 150 C 258 160, 263 175, 264 190 C 264 198, 261 204, 256 206 C 262 203, 265 196, 265 188 C 265 172, 261 158, 253 150 Z" fill="#6E523E" opacity="0.32" />
  </g>
</svg>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    return path

if __name__ == "__main__":
    svg_path = create_owluko_v21_svg()
    rendered = render_svg_chrome(svg_path, "scratch/temp_owluko_v21.png")
    res = evaluate(rendered)
    print(f"[V21] IoU: {res['iou']*100:.2f}%, SSIM: {res['ssim']*100:.2f}%, NCC: {res['ncc']*100:.2f}%, Delta E: {res['delta_e']:.2f}, MSE: {res['mse']:.1f}")
