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

def create_v23(path="scratch/test_owluko_v23.svg"):
    sil_d = "M 272 40 L 237 40 L 216 44 L 207 48 L 201 49 L 185 57 L 168 69 L 155 82 L 147 94 L 145 95 L 132 119 L 126 134 L 124 145 L 120 155 L 120 162 L 116 174 L 115 183 L 103 194 L 95 213 L 92 231 L 90 235 L 90 246 L 88 255 L 87 271 L 90 314 L 96 339 L 105 359 L 109 363 L 110 366 L 119 374 L 127 377 L 132 382 L 144 400 L 151 407 L 168 421 L 186 430 L 192 437 L 188 451 L 183 459 L 178 462 L 164 465 L 158 470 L 155 479 L 157 485 L 160 488 L 169 489 L 176 485 L 180 485 L 186 489 L 198 489 L 206 485 L 214 485 L 220 489 L 224 489 L 231 486 L 233 482 L 231 469 L 221 461 L 217 451 L 218 445 L 224 441 L 242 443 L 293 441 L 297 446 L 297 455 L 293 461 L 283 470 L 280 476 L 280 484 L 283 488 L 293 489 L 300 485 L 308 485 L 314 489 L 324 489 L 329 485 L 337 485 L 340 487 L 349 488 L 352 487 L 356 483 L 356 474 L 351 466 L 338 462 L 329 456 L 323 442 L 323 434 L 327 429 L 334 427 L 337 424 L 344 421 L 356 411 L 372 395 L 380 382 L 385 377 L 391 376 L 397 373 L 404 366 L 407 358 L 411 353 L 411 350 L 416 339 L 416 334 L 421 317 L 424 290 L 424 260 L 420 228 L 416 217 L 416 213 L 409 197 L 409 194 L 396 183 L 392 166 L 391 155 L 389 152 L 385 135 L 382 130 L 379 120 L 364 93 L 347 73 L 331 60 L 311 50 L 305 49 L 293 44 L 277 42 Z"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" style="background: transparent;">
  <defs>
    <!-- Master Body Silhouette Clip -->
    <clipPath id="bodyClip">
      <path d="{sil_d}" />
    </clipPath>

    <!-- Master Porcelain Body Gradient (Clean, Luminous, Continuous Egg) -->
    <linearGradient id="bodyGrad" x1="26%" y1="5%" x2="74%" y2="95%">
      <stop offset="0%" stop-color="#FCF5EC" />
      <stop offset="15%" stop-color="#F7ECE0" />
      <stop offset="36%" stop-color="#E8D7C7" />
      <stop offset="60%" stop-color="#D5C1AF" />
      <stop offset="80%" stop-color="#A89280" />
      <stop offset="100%" stop-color="#6B5747" />
    </linearGradient>

    <!-- Cranial Dome Specular Highlight -->
    <radialGradient id="cranialHl" cx="42%" cy="17%" r="35%">
      <stop offset="0%" stop-color="#FFFDF9" stop-opacity="0.35" />
      <stop offset="50%" stop-color="#F7EEE4" stop-opacity="0.12" />
      <stop offset="100%" stop-color="#ECE0D4" stop-opacity="0" />
    </radialGradient>

    <!-- Upper Right Head Soft Falloff -->
    <radialGradient id="headRightShadow" cx="72%" cy="18%" r="42%">
      <stop offset="0%" stop-color="#7A6250" stop-opacity="0.22" />
      <stop offset="60%" stop-color="#7A6250" stop-opacity="0.10" />
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
      <stop offset="45%" stop-color="#A8927E" stop-opacity="0.28" />
      <stop offset="100%" stop-color="#6B5442" stop-opacity="0.62" />
    </linearGradient>

    <!-- Translucent Honey Amber Iris (Left Eye) -->
    <radialGradient id="amberEyeL" cx="42%" cy="65%" r="62%">
      <stop offset="0%" stop-color="#D69B3E" />
      <stop offset="35%" stop-color="#B38B44" />
      <stop offset="70%" stop-color="#674A16" />
      <stop offset="100%" stop-color="#381D06" />
    </radialGradient>

    <!-- Translucent Honey Amber Iris (Right Eye) -->
    <radialGradient id="amberEyeR" cx="48%" cy="65%" r="62%">
      <stop offset="0%" stop-color="#BA934B" />
      <stop offset="35%" stop-color="#9E7538" />
      <stop offset="70%" stop-color="#55340C" />
      <stop offset="100%" stop-color="#2D1503" />
    </radialGradient>

    <!-- Porcelain Cream Eyelid Hoods -->
    <linearGradient id="eyelidHoodL" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#FAF1E6" />
      <stop offset="50%" stop-color="#F3E5D8" />
      <stop offset="85%" stop-color="#DEC9B6" />
      <stop offset="100%" stop-color="#88644A" />
    </linearGradient>

    <linearGradient id="eyelidHoodR" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#EDE2D4" />
      <stop offset="50%" stop-color="#E2D2C2" />
      <stop offset="85%" stop-color="#CBB3A0" />
      <stop offset="100%" stop-color="#765238" />
    </linearGradient>

    <!-- Eyelid Cast Shadow on Eyeball -->
    <linearGradient id="eyeShadow" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#140601" stop-opacity="0.82" />
      <stop offset="55%" stop-color="#3A1A04" stop-opacity="0.45" />
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
      <stop offset="0%" stop-color="#6B503D" stop-opacity="0.40" />
      <stop offset="60%" stop-color="#6B503D" stop-opacity="0.16" />
      <stop offset="100%" stop-color="#6B503D" stop-opacity="0" />
    </radialGradient>

    <!-- Facial Disc Subtle Ambient Occlusions -->
    <radialGradient id="lOrbitGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#8E7562" stop-opacity="0.12" />
      <stop offset="70%" stop-color="#8E7562" stop-opacity="0.04" />
      <stop offset="100%" stop-color="#8E7562" stop-opacity="0.0" />
    </radialGradient>
    <radialGradient id="rOrbitGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#785F4D" stop-opacity="0.22" />
      <stop offset="75%" stop-color="#785F4D" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#785F4D" stop-opacity="0.0" />
    </radialGradient>

    <!-- Feet Volumetric Gradients -->
    <linearGradient id="lFootGrad" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#8C745E" />
      <stop offset="30%" stop-color="#B29A84" />
      <stop offset="65%" stop-color="#D7BEA8" />
      <stop offset="85%" stop-color="#B49C86" />
      <stop offset="100%" stop-color="#745C48" />
    </linearGradient>
    <linearGradient id="rFootGrad" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#6E5642" />
      <stop offset="30%" stop-color="#8E755E" />
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
    <!-- Left Wing Subtle Furrow Line -->
    <path d="M 125 185 C 135 225, 138 280, 130 355 C 128 370, 122 385, 118 395" stroke="#B8A492" stroke-width="2.2" stroke-linecap="round" opacity="0.22" fill="none" />

    <!-- Right Flank Ambient Occlusion -->
    <path d="M 330 180 C 375 210, 424 265, 420 345 C 416 385, 375 420, 345 425 C 380 395, 385 300, 345 200 Z" fill="url(#rWingShadow)" />
    <!-- Right Wing Subtle Furrow Line -->
    <path d="M 368 185 C 362 225, 362 280, 368 355 C 370 370, 375 385, 380 395" stroke="#66503E" stroke-width="2.6" stroke-linecap="round" opacity="0.32" fill="none" />

    <!-- Feet 3D Modeling (Seamless Organic Avian Feet) -->
    <!-- Left Foot Whole Organic Mesh -->
    <path d="M 155 479 L 157 485 L 160 488 L 169 489 L 176 485 L 180 485 L 186 489 L 198 489 L 206 485 L 214 485 L 220 489 L 228 488 L 231 486 L 233 482 L 231 469 L 227 465 L 225 465 L 219 458 L 217 451 L 217 447 L 221 442 L 224 441 L 239 442 L 239 435 L 191 435 L 192 439 L 190 442 L 190 445 L 185 457 L 178 462 L 174 462 L 171 464 L 167 464 L 162 466 L 158 470 Z" fill="url(#lFootGrad)" />
    <!-- Left Foot Knuckle Highlights (Calibrated to Ref Peaks: 163, 187, 218) -->
    <ellipse cx="163" cy="473" rx="7.5" ry="4.5" fill="#FFFFFF" opacity="0.25" />
    <ellipse cx="187" cy="476" rx="8.5" ry="5.5" fill="#FFFFFF" opacity="0.30" />
    <ellipse cx="218" cy="477" rx="7.5" ry="4.5" fill="#FFFFFF" opacity="0.25" />
    <!-- Left Foot Soft Crevices -->
    <ellipse cx="172" cy="470" rx="2.8" ry="10" fill="#2D1B0E" opacity="0.25" />
    <ellipse cx="208" cy="470" rx="2.8" ry="10" fill="#2D1B0E" opacity="0.25" />

    <!-- Right Foot Whole Organic Mesh -->
    <path d="M 270 435 L 270 442 L 293 441 L 297 446 L 297 455 L 293 461 L 283 470 L 280 476 L 280 484 L 283 488 L 293 489 L 300 485 L 308 485 L 314 489 L 324 489 L 329 485 L 337 485 L 340 487 L 349 488 L 352 487 L 356 483 L 356 474 L 353 468 L 351 466 L 338 462 L 332 459 L 329 456 L 323 442 L 323 435 Z" fill="url(#rFootGrad)" />
    <!-- Right Foot Knuckle Highlights (Calibrated to Ref Peaks: 286, 323, 346) -->
    <ellipse cx="286" cy="477" rx="7.5" ry="4.5" fill="#FFFFFF" opacity="0.18" />
    <ellipse cx="323" cy="466" rx="8.5" ry="5.5" fill="#FFFFFF" opacity="0.25" />
    <ellipse cx="346" cy="472" rx="7.5" ry="4.5" fill="#FFFFFF" opacity="0.18" />
    <!-- Right Foot Soft Crevices -->
    <ellipse cx="298" cy="471" rx="2.8" ry="10" fill="#25160A" opacity="0.28" />
    <ellipse cx="339" cy="472" rx="2.8" ry="10" fill="#25160A" opacity="0.28" />
  </g>

  <!-- 3. Facial Depressions (Soft Heart-Shaped Facial Disc) -->
  <ellipse cx="195" cy="155" rx="38" ry="32" fill="url(#lOrbitGrad)" />
  <ellipse cx="312" cy="155" rx="38" ry="32" fill="url(#rOrbitGrad)" />

  <!-- 4. Sleepy Hooded Glassy Amber Eyes -->
  <!-- Left Eye -->
  <g id="left_eye">
    <!-- Lower Socket Soft Rim / Eyeball Rim Shadow -->
    <path d="M 166 145 C 165 156, 168 166, 174 173 C 182 181, 196 182, 208 179 C 218 175, 224 164, 224 147" stroke="#A88E78" stroke-width="1.8" stroke-linecap="round" opacity="0.35" fill="none" />
    <!-- Amber Iris -->
    <path d="M 166 145 C 176 140, 204 140, 224 147 C 224 163, 218 174, 208 178 C 196 181, 180 180, 172 172 C 166 164, 165 154, 166 145 Z" fill="url(#amberEyeL)" />
    <!-- Pupil Core -->
    <ellipse cx="195" cy="158" rx="8.5" ry="10" fill="#220E03" opacity="0.75" />
    <!-- Glowing Honey Crescent -->
    <path d="M 172 162 C 182 174, 204 176, 218 166 C 214 175, 198 181, 185 180 C 176 178, 172 170, 172 162 Z" fill="#D69B3E" opacity="0.60" />
    <!-- Eyelid Cast Shadow on eyeball -->
    <path d="M 166 145 C 176 140, 204 140, 224 147 C 223 154, 208 152, 195 150 C 182 148, 168 151, 166 145 Z" fill="url(#eyeShadow)" />
    <!-- Specular Reflection Glint (Calibrated to Ref: X=220, Y=175) -->
    <ellipse cx="220" cy="175" rx="2.6" ry="3.6" fill="#FFFFFF" opacity="0.95" />
    <ellipse cx="220" cy="175" rx="4.2" ry="5.2" fill="#FFE8A5" opacity="0.38" />
    <!-- Porcelain Upper Eyelid Hood -->
    <path d="M 164 136 C 170 118, 218 120, 226 140 C 226 144, 224 147, 224 147 C 204 140, 176 140, 166 145 C 164 142, 164 138, 164 136 Z" fill="url(#eyelidHoodL)" />
  </g>

  <!-- Right Eye -->
  <g id="right_eye">
    <!-- Lower Socket Soft Rim -->
    <path d="M 280 143 C 280 160, 286 172, 296 178 C 306 182, 320 181, 330 174 C 336 168, 340 156, 340 144" stroke="#8E7562" stroke-width="1.8" stroke-linecap="round" opacity="0.40" fill="none" />
    <!-- Amber Iris -->
    <path d="M 280 143 C 298 138, 328 137, 340 144 C 340 156, 336 168, 330 174 C 320 181, 306 182, 296 178 C 286 172, 280 160, 280 143 Z" fill="url(#amberEyeR)" />
    <!-- Pupil Core -->
    <ellipse cx="312" cy="158" rx="8.5" ry="10" fill="#180802" opacity="0.75" />
    <!-- Glowing Honey Crescent -->
    <path d="M 288 165 C 300 176, 322 175, 331 163 C 328 172, 316 179, 304 179 C 295 177, 289 171, 288 165 Z" fill="#BA934B" opacity="0.55" />
    <!-- Eyelid Cast Shadow -->
    <path d="M 280 143 C 298 138, 328 137, 340 144 C 338 152, 324 150, 310 151 C 298 152, 285 153, 280 143 Z" fill="url(#eyeShadow)" />
    <!-- Specular Reflection Glint (Calibrated to Ref: X=326, Y=165) -->
    <ellipse cx="326" cy="165" rx="2.6" ry="3.6" fill="#FFC47B" opacity="0.92" />
    <ellipse cx="326" cy="165" rx="1.3" ry="2.0" fill="#FFFFFF" opacity="0.95" />
    <!-- Porcelain Upper Eyelid Hood -->
    <path d="M 278 138 C 286 118, 334 117, 342 136 C 342 140, 340 144, 340 144 C 328 137, 298 138, 280 143 C 279 141, 278 139, 278 138 Z" fill="url(#eyelidHoodR)" />
  </g>

  <!-- 5. Seamless Rounded Porcelain Beak Cone -->
  <g id="beak">
    <!-- Cast Shadow beneath beak tip onto breast -->
    <ellipse cx="254" cy="207" rx="13" ry="6" fill="url(#beakTipShadow)" />
    <!-- Rounded Porcelain Beak Cone -->
    <path d="M 246 146 C 251 144, 257 144, 262 146 C 266 154, 267 170, 266 186 C 265 197, 260 204, 254 204 C 248 204, 243 197, 242 186 C 241 170, 242 154, 246 146 Z" fill="url(#beakGrad)" />
    <!-- Longitudinal Highlight Ridge -->
    <path d="M 253 148 C 253 162, 253 182, 253 200" stroke="#FFFFFF" stroke-width="1.2" stroke-linecap="round" opacity="0.32" fill="none" />
    <!-- Right Beak Flank Ambient Shadow -->
    <path d="M 254 148 C 258 158, 264 172, 264 186 C 264 196, 260 202, 256 203 C 261 200, 264 193, 264 186 C 264 170, 260 156, 254 148 Z" fill="#6E523E" opacity="0.30" />
  </g>
</svg>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    return path

if __name__ == "__main__":
    svg_path = create_v23()
    rendered = render_svg_chrome(svg_path, "scratch/temp_owluko_v23.png")
    res = evaluate(rendered)
    print(f"[V23] IoU: {res['iou']*100:.2f}%, SSIM: {res['ssim']*100:.2f}%, NCC: {res['ncc']*100:.2f}%, Delta E: {res['delta_e']:.2f}, MSE: {res['mse']:.1f}")
