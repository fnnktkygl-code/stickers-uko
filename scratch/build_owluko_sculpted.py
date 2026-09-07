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

def create_sculpted_owluko(path="scratch/test_owluko_sculpted.svg"):
    # Precise 126-point boundary silhouette
    sil_d = "M 272 40 L 237 40 L 216 44 L 207 48 L 201 49 L 185 57 L 168 69 L 155 82 L 147 94 L 145 95 L 132 119 L 126 134 L 124 145 L 120 155 L 120 162 L 116 174 L 115 183 L 103 194 L 95 213 L 92 231 L 90 235 L 90 246 L 88 255 L 87 271 L 90 314 L 96 339 L 105 359 L 109 363 L 110 366 L 119 374 L 127 377 L 132 382 L 144 400 L 151 407 L 168 421 L 186 430 L 192 437 L 188 451 L 183 459 L 178 462 L 164 465 L 158 470 L 155 479 L 157 485 L 160 488 L 169 489 L 176 485 L 180 485 L 186 489 L 198 489 L 206 485 L 214 485 L 220 489 L 224 489 L 231 486 L 233 482 L 231 469 L 221 461 L 217 451 L 218 445 L 224 441 L 242 443 L 293 441 L 297 446 L 297 455 L 293 461 L 283 470 L 280 476 L 280 484 L 283 488 L 293 489 L 300 485 L 308 485 L 314 489 L 324 489 L 329 485 L 337 485 L 340 487 L 349 488 L 352 487 L 356 483 L 356 474 L 351 466 L 338 462 L 329 456 L 323 442 L 323 434 L 327 429 L 334 427 L 337 424 L 344 421 L 356 411 L 372 395 L 380 382 L 385 377 L 391 376 L 397 373 L 404 366 L 407 358 L 411 353 L 411 350 L 416 339 L 416 334 L 421 317 L 424 290 L 424 260 L 420 228 L 416 217 L 416 213 L 409 197 L 409 194 L 396 183 L 392 166 L 391 155 L 389 152 L 385 135 L 382 130 L 379 120 L 364 93 L 347 73 L 331 60 L 311 50 L 305 49 L 293 44 L 277 42 Z"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" style="background: transparent;">
  <defs>
    <!-- Master Body Silhouette Clip -->
    <clipPath id="bodyClip">
      <path d="{sil_d}" />
    </clipPath>

    <!-- Master Porcelain Body Gradient (Luminous Porcelain Egg) -->
    <linearGradient id="bodyGrad" x1="26%" y1="5%" x2="74%" y2="95%">
      <stop offset="0%" stop-color="#FCF4EB" />
      <stop offset="16%" stop-color="#F7ECE0" />
      <stop offset="38%" stop-color="#E8D7C7" />
      <stop offset="62%" stop-color="#D5C1AF" />
      <stop offset="82%" stop-color="#A89280" />
      <stop offset="100%" stop-color="#6E5948" />
    </linearGradient>

    <!-- Cranial Dome Specular Highlight -->
    <radialGradient id="cranialHl" cx="44%" cy="16%" r="36%">
      <stop offset="0%" stop-color="#FFFDF9" stop-opacity="0.38" />
      <stop offset="50%" stop-color="#F8EFE5" stop-opacity="0.14" />
      <stop offset="100%" stop-color="#ECE0D4" stop-opacity="0" />
    </radialGradient>

    <!-- Upper Right Head Ambient Falloff -->
    <radialGradient id="headRightShadow" cx="72%" cy="18%" r="42%">
      <stop offset="0%" stop-color="#7A6250" stop-opacity="0.25" />
      <stop offset="65%" stop-color="#7A6250" stop-opacity="0.10" />
      <stop offset="100%" stop-color="#7A6250" stop-opacity="0" />
    </radialGradient>

    <!-- Breast / Chest Soft Illumination -->
    <radialGradient id="chestHl" cx="44%" cy="50%" r="42%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.22" />
      <stop offset="55%" stop-color="#F8EFE7" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#E2D4C6" stop-opacity="0" />
    </radialGradient>

    <!-- Left Wing Lateral Soft Highlight -->
    <linearGradient id="lWingGrad" x1="0%" y1="20%" x2="100%" y2="80%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.26" />
      <stop offset="40%" stop-color="#F8EFE5" stop-opacity="0.10" />
      <stop offset="100%" stop-color="#DECFC0" stop-opacity="0" />
    </linearGradient>

    <!-- Right Flank Ambient Occlusion -->
    <linearGradient id="rWingShadow" x1="0%" y1="20%" x2="100%" y2="80%">
      <stop offset="0%" stop-color="#D4C2B0" stop-opacity="0.0" />
      <stop offset="45%" stop-color="#A8927E" stop-opacity="0.28" />
      <stop offset="100%" stop-color="#6B5442" stop-opacity="0.62" />
    </linearGradient>

    <!-- Facial Disc Orbital Socket Soft Depressions -->
    <radialGradient id="lOrbitGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#8E7562" stop-opacity="0.15" />
      <stop offset="70%" stop-color="#8E7562" stop-opacity="0.06" />
      <stop offset="100%" stop-color="#8E7562" stop-opacity="0.0" />
    </radialGradient>
    <radialGradient id="rOrbitGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#785F4D" stop-opacity="0.25" />
      <stop offset="75%" stop-color="#785F4D" stop-opacity="0.10" />
      <stop offset="100%" stop-color="#785F4D" stop-opacity="0.0" />
    </radialGradient>

    <!-- Left Amber Iris (Glowing Translucent Amber Liquid) -->
    <radialGradient id="amberEyeL" cx="44%" cy="65%" r="60%">
      <stop offset="0%" stop-color="#E5A035" />
      <stop offset="35%" stop-color="#C27A22" />
      <stop offset="70%" stop-color="#6E3A10" />
      <stop offset="100%" stop-color="#3A1C06" />
    </radialGradient>

    <!-- Right Amber Iris (Shadow Side Translucent Amber) -->
    <radialGradient id="amberEyeR" cx="48%" cy="65%" r="60%">
      <stop offset="0%" stop-color="#CE8828" />
      <stop offset="35%" stop-color="#A86218" />
      <stop offset="70%" stop-color="#5C2E0C" />
      <stop offset="100%" stop-color="#301504" />
    </radialGradient>

    <!-- Left Porcelain Eyelid Hood (3D Bulging Fold) -->
    <linearGradient id="eyelidHoodL" x1="45%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#FAF0E6" />
      <stop offset="40%" stop-color="#FFF8F0" />
      <stop offset="75%" stop-color="#EAD8C7" />
      <stop offset="92%" stop-color="#C2A690" />
      <stop offset="100%" stop-color="#7A5438" />
    </linearGradient>

    <!-- Right Porcelain Eyelid Hood -->
    <linearGradient id="eyelidHoodR" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#E5D6C6" />
      <stop offset="40%" stop-color="#EDE0D2" />
      <stop offset="75%" stop-color="#D2BCAB" />
      <stop offset="92%" stop-color="#A0836D" />
      <stop offset="100%" stop-color="#664225" />
    </linearGradient>

    <!-- Eyelid Margin Cast Shadow on Eyeball -->
    <linearGradient id="eyeShadow" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#140601" stop-opacity="0.85" />
      <stop offset="50%" stop-color="#3A1A04" stop-opacity="0.45" />
      <stop offset="100%" stop-color="#7C3B07" stop-opacity="0" />
    </linearGradient>

    <!-- Seamless Rounded Porcelain Beak Cone -->
    <linearGradient id="beakGrad" x1="20%" y1="0%" x2="80%" y2="100%">
      <stop offset="0%" stop-color="#FBF0E4" />
      <stop offset="25%" stop-color="#EBD8C6" />
      <stop offset="65%" stop-color="#B89C84" />
      <stop offset="100%" stop-color="#785E4A" />
    </linearGradient>

    <!-- Soft Under-Beak Ambient Shadow -->
    <radialGradient id="beakTipShadow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#6B503D" stop-opacity="0.35" />
      <stop offset="60%" stop-color="#6B503D" stop-opacity="0.14" />
      <stop offset="100%" stop-color="#6B503D" stop-opacity="0" />
    </radialGradient>

    <!-- Continuous Organic Feet Gradients (Keylight Left, Ambient Right) -->
    <linearGradient id="lFootGrad" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#8A725D" />
      <stop offset="25%" stop-color="#B09882" />
      <stop offset="65%" stop-color="#D7BEA8" />
      <stop offset="85%" stop-color="#B49C86" />
      <stop offset="100%" stop-color="#745C48" />
    </linearGradient>
    <linearGradient id="rFootGrad" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#6E5642" />
      <stop offset="25%" stop-color="#8E755E" />
      <stop offset="65%" stop-color="#B29A84" />
      <stop offset="85%" stop-color="#907862" />
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
    <!-- Left Wing Subtle Soft Furrow -->
    <path d="M 125 185 C 135 225, 138 280, 130 355 C 128 370, 122 385, 118 395" stroke="#B8A492" stroke-width="2.0" stroke-linecap="round" opacity="0.25" fill="none" />

    <!-- Right Flank Ambient Occlusion -->
    <path d="M 330 180 C 375 210, 424 265, 420 345 C 416 385, 375 420, 345 425 C 380 395, 385 300, 345 200 Z" fill="url(#rWingShadow)" />
    <!-- Right Wing Subtle Soft Furrow -->
    <path d="M 368 185 C 362 225, 362 280, 368 355 C 370 370, 375 385, 380 395" stroke="#66503E" stroke-width="2.5" stroke-linecap="round" opacity="0.30" fill="none" />

    <!-- Lower Belly Ambient Shading (Softened natural porcelain curve) -->
    <ellipse cx="254" cy="405" rx="85" ry="28" fill="#755F4E" opacity="0.20" />
    <ellipse cx="256" cy="432" rx="55" ry="12" fill="#523D2C" opacity="0.20" />

    <!-- Feet 3D Modeling (Seamless Organic Avian Feet) -->
    <!-- Left Foot Whole Organic Mesh -->
    <path d="M 155 479 L 157 485 L 160 488 L 169 489 L 176 485 L 180 485 L 186 489 L 198 489 L 206 485 L 214 485 L 220 489 L 228 488 L 231 486 L 233 482 L 231 469 L 227 465 L 225 465 L 219 458 L 217 451 L 217 447 L 221 442 L 224 441 L 239 442 L 239 435 L 191 435 L 192 439 L 190 442 L 190 445 L 185 457 L 178 462 L 174 462 L 171 464 L 167 464 L 162 466 L 158 470 Z" fill="url(#lFootGrad)" />
    <!-- Left Foot Knuckle Highlights (Calibrated to Ref Peaks: 163, 187, 218) -->
    <ellipse cx="163" cy="473" rx="8.0" ry="5.0" fill="#FFFFFF" opacity="0.26" />
    <ellipse cx="187" cy="476" rx="9.0" ry="6.0" fill="#FFFFFF" opacity="0.30" />
    <ellipse cx="218" cy="477" rx="8.0" ry="5.0" fill="#FFFFFF" opacity="0.26" />
    <!-- Left Foot Soft Crevices -->
    <ellipse cx="172" cy="470" rx="3.0" ry="10" fill="#2D1B0E" opacity="0.28" />
    <ellipse cx="208" cy="470" rx="3.0" ry="10" fill="#2D1B0E" opacity="0.28" />

    <!-- Right Foot Whole Organic Mesh -->
    <path d="M 270 435 L 270 442 L 293 441 L 297 446 L 297 455 L 293 461 L 283 470 L 280 476 L 280 484 L 283 488 L 293 489 L 300 485 L 308 485 L 314 489 L 324 489 L 329 485 L 337 485 L 340 487 L 349 488 L 352 487 L 356 483 L 356 474 L 353 468 L 351 466 L 338 462 L 332 459 L 329 456 L 323 442 L 323 435 Z" fill="url(#rFootGrad)" />
    <!-- Right Foot Knuckle Highlights (Calibrated to Ref Peaks: 286, 323, 346) -->
    <ellipse cx="286" cy="477" rx="7.5" ry="4.5" fill="#FFFFFF" opacity="0.18" />
    <ellipse cx="323" cy="466" rx="8.5" ry="5.5" fill="#FFFFFF" opacity="0.25" />
    <ellipse cx="346" cy="472" rx="7.5" ry="4.5" fill="#FFFFFF" opacity="0.18" />
    <!-- Right Foot Soft Crevices -->
    <ellipse cx="298" cy="471" rx="3.0" ry="10" fill="#25160A" opacity="0.30" />
    <ellipse cx="339" cy="472" rx="3.0" ry="10" fill="#25160A" opacity="0.30" />
  </g>

  <!-- 3. Facial Depressions & Eye Orbits (Heart-Shaped Facial Disc) -->
  <ellipse cx="195" cy="155" rx="42" ry="36" fill="url(#lOrbitGrad)" />
  <ellipse cx="312" cy="155" rx="42" ry="36" fill="url(#rOrbitGrad)" />

  <!-- 4. Sleepy Hooded Glassy Amber Eyes (True Large Round Sleepy Eyes) -->
  <!-- LEFT EYE -->
  <g id="left_eye">
    <!-- Amber Iris Sphere (True Large Round Aperture: Height 32px) -->
    <path d="M 165 146 C 175 143, 205 144, 225 154 C 224 165, 218 174, 208 178 C 196 182, 180 180, 172 172 C 166 164, 164 154, 165 146 Z" fill="url(#amberEyeL)" />
    
    <!-- Pupil / Deep Core -->
    <ellipse cx="195" cy="160" rx="9.5" ry="11" fill="#1C0A02" opacity="0.80" />
    
    <!-- Glowing Amber Lower Half-Moon Subsurface Scattering -->
    <path d="M 170 162 C 180 174, 204 176, 218 166 C 214 175, 198 181, 185 180 C 176 178, 171 170, 170 162 Z" fill="#FFA726" opacity="0.65" />

    <!-- Eyelid Cast Shadow onto Eyeball -->
    <path d="M 165 146 C 175 143, 205 144, 225 154 C 223 161, 208 158, 195 156 C 182 154, 168 155, 165 146 Z" fill="url(#eyeShadow)" />

    <!-- Specular Reflection Glint (Calibrated to Ref: X=220, Y=175) -->
    <ellipse cx="220" cy="175" rx="2.8" ry="3.8" fill="#FFFFFF" opacity="0.95" />
    <ellipse cx="220" cy="175" rx="4.5" ry="5.5" fill="#FFE8A5" opacity="0.40" />

    <!-- Soft Keylight Upper Glint beneath Eyelid Margin -->
    <ellipse cx="180" cy="150" rx="2.5" ry="1.8" fill="#FFFFFF" opacity="0.55" />

    <!-- Porcelain Upper Eyelid Hood (Bulging 3D Fold) -->
    <path d="M 164 136 C 170 118, 218 120, 226 142 C 226 148, 225 154, 225 154 C 205 144, 175 143, 165 146 C 164 142, 164 138, 164 136 Z" fill="url(#eyelidHoodL)" />
    <!-- Eyelid Hood Diffuse Keylight Peak -->
    <ellipse cx="195" cy="132" rx="14" ry="6" fill="#FFFFFF" opacity="0.22" />
  </g>

  <!-- RIGHT EYE -->
  <g id="right_eye">
    <!-- Amber Iris Sphere -->
    <path d="M 282 154 C 300 144, 330 143, 338 146 C 340 154, 338 164, 332 172 C 322 180, 308 182, 298 178 C 288 173, 282 163, 282 154 Z" fill="url(#amberEyeR)" />
    
    <!-- Pupil / Deep Core -->
    <ellipse cx="312" cy="160" rx="9.5" ry="11" fill="#140601" opacity="0.80" />
    
    <!-- Glowing Amber Lower Half-Moon -->
    <path d="M 288 165 C 300 176, 322 175, 331 163 C 328 172, 316 179, 304 179 C 295 177, 289 171, 288 165 Z" fill="#F59E1B" opacity="0.55" />

    <!-- Eyelid Cast Shadow -->
    <path d="M 282 154 C 300 144, 330 143, 338 146 C 336 154, 324 153, 310 154 C 298 155, 285 158, 282 154 Z" fill="url(#eyeShadow)" />

    <!-- Specular Reflection Glint (Calibrated to Ref: X=326, Y=165) -->
    <ellipse cx="326" cy="165" rx="2.8" ry="3.8" fill="#FFC47B" opacity="0.92" />
    <ellipse cx="326" cy="165" rx="1.4" ry="2.0" fill="#FFFFFF" opacity="0.95" />

    <!-- Porcelain Upper Eyelid Hood -->
    <path d="M 281 142 C 288 120, 336 118, 340 136 C 340 140, 338 146, 338 146 C 330 143, 300 144, 282 154 C 281 150, 281 145, 281 142 Z" fill="url(#eyelidHoodR)" />
    <!-- Eyelid Hood Diffuse Highlight -->
    <ellipse cx="312" cy="132" rx="13" ry="5" fill="#FFFFFF" opacity="0.16" />
  </g>

  <!-- 5. Seamless Rounded Porcelain Beak Cone (Nestled snugly between eyes) -->
  <g id="beak">
    <!-- Cast Shadow beneath beak tip onto breast -->
    <ellipse cx="254" cy="204" rx="12" ry="6" fill="url(#beakTipShadow)" />
    <!-- Rounded Porcelain Beak Cone (Starts Y=146, rounded tip at Y=201) -->
    <path d="M 248 146 C 252 144, 256 144, 260 146 C 265 154, 266 170, 265 186 C 264 195, 260 201, 254 201 C 248 201, 244 195, 243 186 C 242 170, 243 154, 248 146 Z" fill="url(#beakGrad)" />
    <!-- Beak Longitudinal Highlight Ridge -->
    <path d="M 253 148 C 253 162, 253 182, 253 198" stroke="#FFFFFF" stroke-width="1.2" stroke-linecap="round" opacity="0.38" fill="none" />
    <!-- Right Beak Flank Ambient Shadow -->
    <path d="M 254 148 C 258 158, 264 172, 264 186 C 264 194, 260 199, 256 200 C 261 197, 264 191, 264 184 C 264 170, 260 156, 254 148 Z" fill="#6E523E" opacity="0.32" />
  </g>
</svg>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    return path

if __name__ == "__main__":
    svg_path = create_sculpted_owluko()
    rendered = render_svg_chrome(svg_path, "scratch/temp_owluko_sculpted.png")
    res = evaluate(rendered)
    print(f"[SCULPTED] IoU: {res['iou']*100:.2f}%, SSIM: {res['ssim']*100:.2f}%, NCC: {res['ncc']*100:.2f}%, Delta E: {res['delta_e']:.2f}, MSE: {res['mse']:.1f}")
