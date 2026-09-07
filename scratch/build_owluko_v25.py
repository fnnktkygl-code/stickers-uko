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

def build_owluko_svg(path="scratch/test_owluko_v25.svg"):
    sil_d = "M 272 40 L 237 40 L 216 44 L 207 48 L 201 49 L 185 57 L 168 69 L 155 82 L 147 94 L 145 95 L 132 119 L 126 134 L 124 145 L 120 155 L 120 162 L 116 174 L 115 183 L 103 194 L 95 213 L 92 231 L 90 235 L 90 246 L 88 255 L 87 271 L 90 314 L 96 339 L 105 359 L 109 363 L 110 366 L 119 374 L 127 377 L 132 382 L 144 400 L 151 407 L 168 421 L 186 430 L 192 437 L 188 451 L 183 459 L 178 462 L 164 465 L 158 470 L 155 479 L 157 485 L 160 488 L 169 489 L 176 485 L 180 485 L 186 489 L 198 489 L 206 485 L 214 485 L 220 489 L 224 489 L 231 486 L 233 482 L 231 469 L 221 461 L 217 451 L 218 445 L 224 441 L 242 443 L 293 441 L 297 446 L 297 455 L 293 461 L 283 470 L 280 476 L 280 484 L 283 488 L 293 489 L 300 485 L 308 485 L 314 489 L 324 489 L 329 485 L 337 485 L 340 487 L 349 488 L 352 487 L 356 483 L 356 474 L 351 466 L 338 462 L 329 456 L 323 442 L 323 434 L 327 429 L 334 427 L 337 424 L 344 421 L 356 411 L 372 395 L 380 382 L 385 377 L 391 376 L 397 373 L 404 366 L 407 358 L 411 353 L 411 350 L 416 339 L 416 334 L 421 317 L 424 290 L 424 260 L 420 228 L 416 217 L 416 213 L 409 197 L 409 194 L 396 183 L 392 166 L 391 155 L 389 152 L 385 135 L 382 130 L 379 120 L 364 93 L 347 73 L 331 60 L 311 50 L 305 49 L 293 44 L 277 42 Z"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" style="background: transparent;">
  <defs>
    <!-- Master Body Silhouette Clip -->
    <clipPath id="bodyClip">
      <path d="{sil_d}" />
    </clipPath>

    <!-- Master Porcelain Body Gradient (Diagonal light from top-left) -->
    <linearGradient id="bodyGrad" x1="26%" y1="5%" x2="74%" y2="95%">
      <stop offset="0%" stop-color="#FCF4EB" />
      <stop offset="20%" stop-color="#F4E6D8" />
      <stop offset="42%" stop-color="#E5D3C2" />
      <stop offset="68%" stop-color="#CFBAA7" />
      <stop offset="85%" stop-color="#AA9481" />
      <stop offset="100%" stop-color="#7B6553" />
    </linearGradient>

    <!-- Cranial Dome Specular Highlight -->
    <radialGradient id="cranialHl" cx="42%" cy="17%" r="35%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.36" />
      <stop offset="50%" stop-color="#F9EFE5" stop-opacity="0.14" />
      <stop offset="100%" stop-color="#EADDCF" stop-opacity="0" />
    </radialGradient>

    <!-- Upper Right Head Soft Ambient Falloff -->
    <radialGradient id="headRightShadow" cx="74%" cy="20%" r="38%">
      <stop offset="0%" stop-color="#8C7461" stop-opacity="0.22" />
      <stop offset="70%" stop-color="#8C7461" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#8C7461" stop-opacity="0" />
    </radialGradient>

    <!-- Breast / Chest Soft Illumination -->
    <radialGradient id="chestHl" cx="44%" cy="48%" r="42%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.28" />
      <stop offset="55%" stop-color="#F9EFE6" stop-opacity="0.10" />
      <stop offset="100%" stop-color="#E2D4C6" stop-opacity="0" />
    </radialGradient>

    <!-- Left Wing Lateral Highlight -->
    <linearGradient id="lWingGrad" x1="0%" y1="20%" x2="100%" y2="80%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.32" />
      <stop offset="45%" stop-color="#F9EFE5" stop-opacity="0.12" />
      <stop offset="100%" stop-color="#DECFC0" stop-opacity="0" />
    </linearGradient>

    <!-- Right Flank Ambient Shadow -->
    <linearGradient id="rWingShadow" x1="0%" y1="20%" x2="100%" y2="80%">
      <stop offset="0%" stop-color="#D4C2B0" stop-opacity="0.0" />
      <stop offset="50%" stop-color="#A8927E" stop-opacity="0.28" />
      <stop offset="100%" stop-color="#6F5846" stop-opacity="0.60" />
    </linearGradient>

    <!-- Lower Belly Soft Ambient Shade -->
    <radialGradient id="bellyShade" cx="50%" cy="40%" r="50%">
      <stop offset="0%" stop-color="#8A705B" stop-opacity="0.35" />
      <stop offset="70%" stop-color="#8A705B" stop-opacity="0.15" />
      <stop offset="100%" stop-color="#8A705B" stop-opacity="0" />
    </radialGradient>

    <!-- Eye Socket Orbital Hollows -->
    <radialGradient id="orbitL" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#D2BBA7" stop-opacity="0.45" />
      <stop offset="70%" stop-color="#D2BBA7" stop-opacity="0.15" />
      <stop offset="100%" stop-color="#D2BBA7" stop-opacity="0" />
    </radialGradient>
    <radialGradient id="orbitR" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#9E816B" stop-opacity="0.55" />
      <stop offset="70%" stop-color="#9E816B" stop-opacity="0.20" />
      <stop offset="100%" stop-color="#9E816B" stop-opacity="0" />
    </radialGradient>

    <!-- Amber Eyeball Optics - Left Eye -->
    <radialGradient id="amberBallL" cx="50%" cy="48%" r="48%">
      <stop offset="0%" stop-color="#3D1C06" />
      <stop offset="45%" stop-color="#552B0A" />
      <stop offset="70%" stop-color="#965D1E" />
      <stop offset="90%" stop-color="#CCA04B" />
      <stop offset="100%" stop-color="#8A5116" />
    </radialGradient>

    <!-- Amber Eyeball Optics - Right Eye -->
    <radialGradient id="amberBallR" cx="48%" cy="48%" r="48%">
      <stop offset="0%" stop-color="#301504" />
      <stop offset="45%" stop-color="#462208" />
      <stop offset="70%" stop-color="#7C4916" />
      <stop offset="90%" stop-color="#B88536" />
      <stop offset="100%" stop-color="#703E10" />
    </radialGradient>

    <!-- Eye Pupil Core -->
    <radialGradient id="pupilCore" cx="45%" cy="45%" r="50%">
      <stop offset="0%" stop-color="#150802" />
      <stop offset="70%" stop-color="#2A1305" />
      <stop offset="100%" stop-color="#441E07" stop-opacity="0" />
    </radialGradient>

    <!-- Luminous Lower Iris Caustics -->
    <linearGradient id="causticsL" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFD685" stop-opacity="0.75" />
      <stop offset="50%" stop-color="#FFA834" stop-opacity="0.55" />
      <stop offset="100%" stop-color="#D97210" stop-opacity="0" />
    </linearGradient>
    <linearGradient id="causticsR" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFC870" stop-opacity="0.80" />
      <stop offset="50%" stop-color="#FF9E26" stop-opacity="0.60" />
      <stop offset="100%" stop-color="#B85E08" stop-opacity="0" />
    </linearGradient>

    <!-- Porcelain Eyelids -->
    <linearGradient id="eyelidL" x1="40%" y1="0%" x2="60%" y2="100%">
      <stop offset="0%" stop-color="#FCF5EC" />
      <stop offset="60%" stop-color="#F2E4D6" />
      <stop offset="90%" stop-color="#DCBEA8" />
      <stop offset="100%" stop-color="#B28C70" />
    </linearGradient>
    <linearGradient id="eyelidR" x1="40%" y1="0%" x2="60%" y2="100%">
      <stop offset="0%" stop-color="#EFE1D4" />
      <stop offset="60%" stop-color="#DEC9B7" />
      <stop offset="90%" stop-color="#BA9880" />
      <stop offset="100%" stop-color="#936D53" />
    </linearGradient>

    <!-- Soft Eyelid Cast Shadow on Eyeball -->
    <linearGradient id="eyelidDropShadow" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#140702" stop-opacity="0.70" />
      <stop offset="60%" stop-color="#2D1305" stop-opacity="0.30" />
      <stop offset="100%" stop-color="#552408" stop-opacity="0" />
    </linearGradient>

    <!-- Porcelain Beak Gradient -->
    <linearGradient id="beakGrad" x1="25%" y1="5%" x2="80%" y2="95%">
      <stop offset="0%" stop-color="#FAF1E7" />
      <stop offset="35%" stop-color="#E6D3C2" />
      <stop offset="70%" stop-color="#BA9E88" />
      <stop offset="100%" stop-color="#886E58" />
    </linearGradient>
    <radialGradient id="beakUnderShadow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#725844" stop-opacity="0.45" />
      <stop offset="60%" stop-color="#725844" stop-opacity="0.18" />
      <stop offset="100%" stop-color="#725844" stop-opacity="0" />
    </radialGradient>

    <!-- Feet Gradients -->
    <linearGradient id="footLGrad" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#CEBCAE" />
      <stop offset="35%" stop-color="#BAA594" />
      <stop offset="70%" stop-color="#8F7866" />
      <stop offset="100%" stop-color="#5C4736" />
    </linearGradient>
    <linearGradient id="footRGrad" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#B5A190" />
      <stop offset="35%" stop-color="#9E8978" />
      <stop offset="70%" stop-color="#776251" />
      <stop offset="100%" stop-color="#4B3929" />
    </linearGradient>
  </defs>

  <!-- 1. Master Base Silhouette Capsule -->
  <path d="{sil_d}" fill="url(#bodyGrad)" />

  <!-- 2. Clipped Body 3D Volume Layers -->
  <g clip-path="url(#bodyClip)">
    <!-- Cranial Specular Dome -->
    <ellipse cx="205" cy="85" rx="95" ry="60" fill="url(#cranialHl)" />

    <!-- Upper Right Head Ambient Falloff -->
    <ellipse cx="345" cy="95" rx="85" ry="65" fill="url(#headRightShadow)" />

    <!-- Breast / Chest Soft Illumination -->
    <ellipse cx="245" cy="275" rx="115" ry="85" fill="url(#chestHl)" />

    <!-- Left Wing Lateral Highlight -->
    <path d="M 88 180 C 88 180, 115 190, 118 270 C 120 340, 95 380, 95 380 C 86 340, 86 230, 88 180 Z" fill="url(#lWingGrad)" />
    <!-- Left Wing Soft Separation Furrow -->
    <path d="M 125 185 C 135 225, 138 280, 130 355 C 128 370, 122 385, 118 395" stroke="#C0AC9B" stroke-width="2.2" stroke-linecap="round" opacity="0.25" fill="none" />

    <!-- Right Flank Ambient Occlusion -->
    <path d="M 330 180 C 375 210, 424 265, 420 345 C 416 385, 375 420, 345 425 C 380 395, 385 300, 345 200 Z" fill="url(#rWingShadow)" />
    <!-- Right Wing Soft Separation Furrow -->
    <path d="M 368 185 C 362 225, 362 280, 368 355 C 370 370, 375 385, 380 395" stroke="#66503E" stroke-width="2.5" stroke-linecap="round" opacity="0.30" fill="none" />

    <!-- Lower Belly Soft Ambient Shade (Smooth, no hard edges) -->
    <ellipse cx="256" cy="425" rx="90" ry="32" fill="url(#bellyShade)" />

    <!-- Feet 3D Organic Avian Meshes -->
    <!-- Left Foot -->
    <path d="M 155 479 L 157 485 L 160 488 L 169 489 L 176 485 L 180 485 L 186 489 L 198 489 L 206 485 L 214 485 L 220 489 L 228 488 L 231 486 L 233 482 L 231 469 L 227 465 L 225 465 L 219 458 L 217 451 L 217 447 L 221 442 L 224 441 L 239 442 L 239 435 L 191 435 L 192 439 L 190 442 L 190 445 L 185 457 L 178 462 L 174 462 L 171 464 L 167 464 L 162 466 L 158 470 Z" fill="url(#footLGrad)" />
    <!-- Left Toes Knuckle Highlights -->
    <ellipse cx="165" cy="475" rx="7" ry="4" fill="#FFFFFF" opacity="0.22" />
    <ellipse cx="190" cy="470" rx="8" ry="5" fill="#FFFFFF" opacity="0.25" />
    <ellipse cx="220" cy="475" rx="7" ry="4" fill="#FFFFFF" opacity="0.20" />
    <!-- Left Toe Soft Interdigital Valleys -->
    <path d="M 179 468 C 179 474, 178 482, 178 485" stroke="#483424" stroke-width="2.5" stroke-linecap="round" opacity="0.28" fill="none" />
    <path d="M 206 467 C 206 473, 206 482, 206 485" stroke="#483424" stroke-width="2.5" stroke-linecap="round" opacity="0.28" fill="none" />

    <!-- Right Foot -->
    <path d="M 270 435 L 270 442 L 293 441 L 297 446 L 297 455 L 293 461 L 283 470 L 280 476 L 280 484 L 283 488 L 293 489 L 300 485 L 308 485 L 314 489 L 324 489 L 329 485 L 337 485 L 340 487 L 349 488 L 352 487 L 356 483 L 356 474 L 353 468 L 351 466 L 338 462 L 332 459 L 329 456 L 323 442 L 323 435 Z" fill="url(#footRGrad)" />
    <!-- Right Toes Knuckle Highlights -->
    <ellipse cx="288" cy="475" rx="7" ry="4" fill="#FFFFFF" opacity="0.18" />
    <ellipse cx="315" cy="470" rx="8" ry="5" fill="#FFFFFF" opacity="0.22" />
    <ellipse cx="345" cy="475" rx="7" ry="4" fill="#FFFFFF" opacity="0.16" />
    <!-- Right Toe Soft Interdigital Valleys -->
    <path d="M 304 467 C 304 473, 304 482, 304 485" stroke="#362416" stroke-width="2.5" stroke-linecap="round" opacity="0.28" fill="none" />
    <path d="M 330 468 C 330 474, 330 482, 330 485" stroke="#362416" stroke-width="2.5" stroke-linecap="round" opacity="0.28" fill="none" />
  </g>

  <!-- 3. Eye Sockets & Eyeballs -->
  <!-- Left Eye Socket Ambient Depression -->
  <ellipse cx="196" cy="154" rx="34" ry="30" fill="url(#orbitL)" />
  <!-- Right Eye Socket Ambient Depression -->
  <ellipse cx="316" cy="154" rx="34" ry="30" fill="url(#orbitR)" />

  <!-- LEFT EYE -->
  <g id="left_eye">
    <!-- Spherical Eyeball Base (Spherical Amber Orb) -->
    <circle cx="196" cy="154" r="29" fill="url(#amberBallL)" />
    <!-- Dark Limbal Ring -->
    <circle cx="196" cy="154" r="28.5" stroke="#251206" stroke-width="1.2" fill="none" opacity="0.65" />
    <!-- Pupil Core -->
    <circle cx="196" cy="154" r="14" fill="url(#pupilCore)" />
    <!-- Lower Iris Luminous Caustics Arc -->
    <path d="M 174 162 C 178 175, 192 181, 206 179 C 216 177, 222 170, 224 163 C 218 172, 208 176, 196 176 C 185 176, 178 171, 174 162 Z" fill="url(#causticsL)" />
    
    <!-- Cast Shadow directly under eyelid rim onto eyeball -->
    <path d="M 168 143 C 182 147, 210 148, 224 145 L 224 153 C 210 156, 182 155, 168 151 Z" fill="url(#eyelidDropShadow)" />
    <!-- Eyelid Shadow Feather line -->
    <path d="M 167 143 C 182 147, 210 148, 224 145" stroke="#1F0B03" stroke-width="1.8" opacity="0.65" fill="none" />

    <!-- Specular Highlight (Crisp White Reflection at X=185.5, Y=142.5) -->
    <ellipse cx="186" cy="143" rx="2.5" ry="2.2" fill="#FFFFFF" opacity="0.95" />
    <ellipse cx="186" cy="143" rx="4.2" ry="3.8" fill="#FFFDF8" opacity="0.45" />

    <!-- Porcelain Upper Eyelid Hood (Overhangs top of eyeball) -->
    <path d="M 167 143 C 168 118, 223 118, 224 145 C 210 148, 182 147, 167 143 Z" fill="url(#eyelidL)" />
    <!-- Soft porcelain brow crease above eyelid -->
    <path d="M 169 133 C 185 125, 208 126, 223 135" stroke="#CBB4A1" stroke-width="1.5" stroke-linecap="round" opacity="0.40" fill="none" />
  </g>

  <!-- RIGHT EYE -->
  <g id="right_eye">
    <!-- Spherical Eyeball Base (Spherical Amber Orb in Soft Shadow) -->
    <circle cx="316" cy="154" r="29" fill="url(#amberBallR)" />
    <!-- Dark Limbal Ring -->
    <circle cx="316" cy="154" r="28.5" stroke="#1A0C04" stroke-width="1.2" fill="none" opacity="0.75" />
    <!-- Pupil Core -->
    <circle cx="316" cy="154" r="14" fill="url(#pupilCore)" />
    <!-- Lower Iris Luminous Caustics Arc (Stronger amber glow on right) -->
    <path d="M 294 162 C 298 175, 312 181, 326 179 C 336 177, 342 170, 344 163 C 338 172, 328 176, 316 176 C 305 176, 298 171, 294 162 Z" fill="url(#causticsR)" />
    
    <!-- Cast Shadow directly under eyelid rim onto eyeball -->
    <path d="M 288 143 C 302 147, 330 148, 344 145 L 344 153 C 330 156, 302 155, 288 151 Z" fill="url(#eyelidDropShadow)" />
    <!-- Eyelid Shadow Feather line -->
    <path d="M 287 143 C 302 147, 330 148, 344 145" stroke="#160802" stroke-width="1.8" opacity="0.70" fill="none" />

    <!-- Specular Highlight Glint (Top rim) -->
    <ellipse cx="304" cy="144" rx="2.2" ry="1.8" fill="#FFE8C2" opacity="0.65" />
    <!-- Secondary Caustic Specular Glint in Lower Right Iris -->
    <ellipse cx="328" cy="164" rx="3.0" ry="3.5" fill="#FFE094" opacity="0.85" />
    <ellipse cx="328" cy="164" rx="1.5" ry="1.8" fill="#FFFFFF" opacity="0.90" />

    <!-- Porcelain Upper Eyelid Hood (Overhangs top of eyeball) -->
    <path d="M 287 143 C 288 118, 343 118, 344 145 C 330 148, 302 147, 287 143 Z" fill="url(#eyelidR)" />
    <!-- Soft porcelain brow crease above eyelid -->
    <path d="M 289 133 C 305 125, 328 126, 343 135" stroke="#9E816B" stroke-width="1.5" stroke-linecap="round" opacity="0.45" fill="none" />
  </g>

  <!-- 4. Seamless Rounded Porcelain Beak Cone -->
  <g id="beak">
    <!-- Cast shadow beneath beak tip onto breast -->
    <ellipse cx="255" cy="208" rx="15" ry="8" fill="url(#beakUnderShadow)" />
    
    <!-- Beak Body Cone (Flows from between the eyes at Y=145 down to rounded tip at Y=204) -->
    <path d="M 255 145 C 248 155, 240 175, 241 190 C 242 198, 247 205, 255 205 C 263 205, 268 198, 269 190 C 270 175, 262 155, 255 145 Z" fill="url(#beakGrad)" />
    
    <!-- Beak Left Illuminated Ridge (Top-left key light) -->
    <path d="M 252 147 C 247 160, 244 175, 245 192 C 246 199, 250 204, 255 204 C 253 202, 250 196, 249 188 C 247 175, 250 160, 252 147 Z" fill="#FFFFFF" opacity="0.35" />
    <path d="M 254 150 C 253 165, 252 185, 253 201" stroke="#FFFFFF" stroke-width="1.2" stroke-linecap="round" opacity="0.30" fill="none" />
  </g>
</svg>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    return path

if __name__ == "__main__":
    svg_path = build_owluko_svg()
    rendered_png = render_svg_chrome(svg_path, "scratch/temp_owluko_v25.png")
    metrics = evaluate(rendered_png)
    print(f"[V25] IoU: {metrics['iou']*100:.2f}%, SSIM: {metrics['ssim']*100:.2f}%, NCC: {metrics['ncc']*100:.2f}%, Delta E: {metrics['delta_e']:.2f}, MSE: {metrics['mse']:.1f}")
