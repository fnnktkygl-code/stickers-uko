import os
import sys
import subprocess
import re
import cv2
import numpy as np
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

def render_svg_chrome(svg_path, out_png="scratch/temp_owluko_test.png"):
    abs_svg = os.path.abspath(svg_path)
    abs_out = os.path.abspath(out_png)
    html_wrap = "scratch/temp_test_wrap.html"
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
    union = ref_mask | vec_mask
    iou = inter.sum() / (union.sum() + 1e-6)

    ref_gray = cv2.cvtColor(ref[:, :, :3], cv2.COLOR_RGB2GRAY)
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

    print(f"IoU: {iou*100:.2f}% | SSIM: {ssim_val*100:.2f}% | NCC: {ncc*100:.2f}% | Delta E: {delta_e:.2f} | MSE: {mse:.1f} | PSNR: {psnr:.2f} dB")
    return {"iou": iou, "ssim": ssim_val, "ncc": ncc, "delta_e": delta_e, "mse": mse}

def generate_svg(out_path="scratch/test_owluko_v18.svg"):
    # Master Silhouette path
    sil_d = "M 272 40 L 237 40 L 216 44 L 207 48 L 201 49 L 185 57 L 168 69 L 155 82 L 147 94 L 145 95 L 132 119 L 126 134 L 124 145 L 120 155 L 120 162 L 116 174 L 115 183 L 103 194 L 95 213 L 92 231 L 90 235 L 90 246 L 88 255 L 87 271 L 90 314 L 96 339 L 105 359 L 109 363 L 110 366 L 119 374 L 127 377 L 132 382 L 144 400 L 151 407 L 168 421 L 186 430 L 192 437 L 188 451 L 183 459 L 178 462 L 164 465 L 158 470 L 155 479 L 157 485 L 160 488 L 169 489 L 176 485 L 180 485 L 186 489 L 198 489 L 206 485 L 214 485 L 220 489 L 224 489 L 231 486 L 233 482 L 231 469 L 221 461 L 217 451 L 218 445 L 224 441 L 242 443 L 293 441 L 297 446 L 297 455 L 293 461 L 283 470 L 280 476 L 280 484 L 283 488 L 293 489 L 300 485 L 308 485 L 314 489 L 324 489 L 329 485 L 337 485 L 340 487 L 349 488 L 352 487 L 356 483 L 356 474 L 351 466 L 338 462 L 329 456 L 323 442 L 323 434 L 327 429 L 334 427 L 337 424 L 344 421 L 356 411 L 372 395 L 380 382 L 385 377 L 391 376 L 397 373 L 404 366 L 407 358 L 411 353 L 411 350 L 416 339 L 416 334 L 421 317 L 424 290 L 424 260 L 420 228 L 416 217 L 416 213 L 409 197 L 409 194 L 396 183 L 392 166 L 391 155 L 389 152 L 385 135 L 382 130 L 379 120 L 364 93 L 347 73 L 331 60 L 311 50 L 305 49 L 293 44 L 277 42 Z"

    svg_str = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" style="background: transparent;">
  <defs>
    <!-- Master Body Silhouette Clip -->
    <clipPath id="bodyClip">
      <path d="{sil_d}" />
    </clipPath>

    <!-- Master Porcelain Body Gradient -->
    <linearGradient id="bodyGrad" x1="26%" y1="5%" x2="74%" y2="95%">
      <stop offset="0%" stop-color="#FDF5EC" />
      <stop offset="15%" stop-color="#F6EAE0" />
      <stop offset="35%" stop-color="#E8D7C8" />
      <stop offset="60%" stop-color="#D4C1B0" />
      <stop offset="82%" stop-color="#A5907E" />
      <stop offset="100%" stop-color="#6B5747" />
    </linearGradient>

    <!-- Cranial Keylight Specular Dome -->
    <radialGradient id="cranialHl" cx="42%" cy="17%" r="35%">
      <stop offset="0%" stop-color="#FFFDF9" stop-opacity="0.35" />
      <stop offset="50%" stop-color="#F7EEE4" stop-opacity="0.14" />
      <stop offset="100%" stop-color="#ECE0D4" stop-opacity="0" />
    </radialGradient>

    <!-- Head Right Ambient Falloff -->
    <radialGradient id="headRightShadow" cx="72%" cy="18%" r="42%">
      <stop offset="0%" stop-color="#7A6250" stop-opacity="0.30" />
      <stop offset="60%" stop-color="#7A6250" stop-opacity="0.12" />
      <stop offset="100%" stop-color="#7A6250" stop-opacity="0" />
    </radialGradient>

    <!-- Breast / Torso Soft Illumination -->
    <radialGradient id="chestHl" cx="45%" cy="48%" r="42%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.22" />
      <stop offset="55%" stop-color="#F8EFE7" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#E2D4C6" stop-opacity="0" />
    </radialGradient>

    <!-- Left Wing Lateral Soft Highlight -->
    <linearGradient id="lWingGrad" x1="0%" y1="20%" x2="100%" y2="80%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.28" />
      <stop offset="40%" stop-color="#F8EFE5" stop-opacity="0.10" />
      <stop offset="100%" stop-color="#DECFC0" stop-opacity="0" />
    </linearGradient>

    <!-- Right Flank Ambient Occlusion -->
    <linearGradient id="rWingShadow" x1="0%" y1="20%" x2="100%" y2="80%">
      <stop offset="0%" stop-color="#D4C2B0" stop-opacity="0.0" />
      <stop offset="45%" stop-color="#A8927E" stop-opacity="0.30" />
      <stop offset="100%" stop-color="#6B5442" stop-opacity="0.65" />
    </linearGradient>

    <!-- Orbital Cavity Gradients (Soft 3D Eye Sockets) -->
    <radialGradient id="lOrbitGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#8E7562" stop-opacity="0.22" />
      <stop offset="70%" stop-color="#8E7562" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#8E7562" stop-opacity="0.0" />
    </radialGradient>
    <radialGradient id="rOrbitGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#785F4D" stop-opacity="0.34" />
      <stop offset="75%" stop-color="#785F4D" stop-opacity="0.14" />
      <stop offset="100%" stop-color="#785F4D" stop-opacity="0.0" />
    </radialGradient>

    <!-- Left Amber Iris (Rich Translucent Glowing Amber) -->
    <radialGradient id="lIrisGrad" cx="48%" cy="75%" r="65%">
      <stop offset="0%" stop-color="#E8A642" />
      <stop offset="35%" stop-color="#CA842C" />
      <stop offset="70%" stop-color="#764014" />
      <stop offset="100%" stop-color="#3D1D06" />
    </radialGradient>

    <!-- Right Amber Iris (Shadow Side Translucent Amber) -->
    <radialGradient id="rIrisGrad" cx="48%" cy="75%" r="65%">
      <stop offset="0%" stop-color="#D29035" />
      <stop offset="35%" stop-color="#B26E22" />
      <stop offset="70%" stop-color="#66350E" />
      <stop offset="100%" stop-color="#301504" />
    </radialGradient>

    <!-- Left Eyelid 3D Porcelain Hood Gradient -->
    <linearGradient id="lLidGrad" x1="45%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#F2E3D4" />
      <stop offset="40%" stop-color="#FFF8F0" />
      <stop offset="75%" stop-color="#EAD8C7" />
      <stop offset="92%" stop-color="#C2A690" />
      <stop offset="100%" stop-color="#7D573B" />
    </linearGradient>

    <!-- Right Eyelid 3D Porcelain Hood Gradient -->
    <linearGradient id="rLidGrad" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#DFCFBF" />
      <stop offset="40%" stop-color="#EDE0D2" />
      <stop offset="75%" stop-color="#D4BEAA" />
      <stop offset="92%" stop-color="#A88B74" />
      <stop offset="100%" stop-color="#6B4527" />
    </linearGradient>

    <!-- Eyelid Margin Cast Shadow on Eyeball -->
    <linearGradient id="lEyeShadow" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#241004" stop-opacity="0.88" />
      <stop offset="45%" stop-color="#462208" stop-opacity="0.55" />
      <stop offset="100%" stop-color="#7C3B07" stop-opacity="0.0" />
    </linearGradient>
    <linearGradient id="rEyeShadow" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#1B0A02" stop-opacity="0.90" />
      <stop offset="45%" stop-color="#3B1B06" stop-opacity="0.58" />
      <stop offset="100%" stop-color="#682F05" stop-opacity="0.0" />
    </linearGradient>

    <!-- Beak 3D Porcelain Gradient -->
    <linearGradient id="beakGrad" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#F0E2D4" />
      <stop offset="35%" stop-color="#D8C2B2" />
      <stop offset="70%" stop-color="#AA907A" />
      <stop offset="100%" stop-color="#78604C" />
    </linearGradient>

    <!-- Soft Under-Beak Cast Shadow -->
    <radialGradient id="beakTipShadow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#6B503D" stop-opacity="0.45" />
      <stop offset="60%" stop-color="#6B503D" stop-opacity="0.18" />
      <stop offset="100%" stop-color="#6B503D" stop-opacity="0" />
    </radialGradient>

    <!-- Left Foot Overall Volumetric Gradient -->
    <linearGradient id="lFootGrad" x1="40%" y1="0%" x2="60%" y2="100%">
      <stop offset="0%" stop-color="#806954" />
      <stop offset="25%" stop-color="#A58E78" />
      <stop offset="60%" stop-color="#CEB9A4" />
      <stop offset="85%" stop-color="#B29A84" />
      <stop offset="100%" stop-color="#78604C" />
    </linearGradient>

    <!-- Right Foot Overall Volumetric Gradient -->
    <linearGradient id="rFootGrad" x1="40%" y1="0%" x2="60%" y2="100%">
      <stop offset="0%" stop-color="#6B5542" />
      <stop offset="25%" stop-color="#8A735E" />
      <stop offset="60%" stop-color="#B59F8B" />
      <stop offset="85%" stop-color="#9C8470" />
      <stop offset="100%" stop-color="#604C3B" />
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

    <!-- Lower Belly Shading Gradient -->
    <ellipse cx="254" cy="405" rx="85" ry="30" fill="#755F4E" opacity="0.25" />
    <ellipse cx="256" cy="442" rx="65" ry="18" fill="#523D2C" opacity="0.35" />

    <!-- Feet 3D Modeling (Seamless Organic Avian Feet) -->
    <!-- Left Leg Stub and Paws -->
    <g id="left_foot">
      <path d="M 183 438 C 182 446, 178 456, 166 464 C 158 470, 155 479, 157 485 C 160 488, 169 489, 176 485 C 180 485, 186 489, 198 489 C 206 485, 214 485, 220 489 C 224 489, 231 486, 233 482 C 231 469, 221 461, 217 451 C 218 445, 224 441, 235 442 L 183 438 Z" fill="url(#lFootGrad)" />
      <!-- Knuckle Domes (Soft diffuse illumination on 3 toes) -->
      <ellipse cx="166" cy="474" rx="8" ry="6" fill="#F0DFD0" opacity="0.40" />
      <ellipse cx="192" cy="470" rx="9" ry="7" fill="#F5E8DC" opacity="0.45" />
      <ellipse cx="221" cy="474" rx="8" ry="6" fill="#EBD9C9" opacity="0.38" />
      <!-- Knuckle Specular Peaks -->
      <ellipse cx="165" cy="472" rx="4" ry="2.5" fill="#FFFFFF" opacity="0.35" />
      <ellipse cx="191" cy="468" rx="4.5" ry="3" fill="#FFFFFF" opacity="0.40" />
      <ellipse cx="221" cy="472" rx="4" ry="2.5" fill="#FFFFFF" opacity="0.32" />
      <!-- Soft Inter-toe Crevices (Organic ambient occlusion) -->
      <path d="M 178 466 C 179 473, 179 480, 179 485" stroke="#3D291B" stroke-width="3" stroke-linecap="round" opacity="0.35" fill="none" />
      <path d="M 207 465 C 207 472, 206 479, 206 485" stroke="#3D291B" stroke-width="3" stroke-linecap="round" opacity="0.35" fill="none" />
    </g>

    <!-- Right Leg Stub and Paws -->
    <g id="right_foot">
      <path d="M 285 440 C 295 445, 297 455, 293 461 C 283 470, 280 476, 280 484 C 283 488, 293 489, 300 485 C 308 485, 314 489, 324 489 C 329 485, 337 485, 340 487 C 349 488, 352 487, 356 483 C 356 474, 351 466, 338 462 C 329 456, 323 442, 323 434 L 285 440 Z" fill="url(#rFootGrad)" />
      <!-- Knuckle Domes -->
      <ellipse cx="291" cy="474" rx="8" ry="6" fill="#DECABB" opacity="0.35" />
      <ellipse cx="318" cy="470" rx="9" ry="7" fill="#E6D3C4" opacity="0.40" />
      <ellipse cx="346" cy="474" rx="8" ry="6" fill="#D8C3B4" opacity="0.32" />
      <!-- Knuckle Specular Peaks -->
      <ellipse cx="291" cy="472" rx="4" ry="2.5" fill="#FFFFFF" opacity="0.28" />
      <ellipse cx="318" cy="468" rx="4.5" ry="3" fill="#FFFFFF" opacity="0.32" />
      <ellipse cx="346" cy="472" rx="4" ry="2.5" fill="#FFFFFF" opacity="0.25" />
      <!-- Soft Inter-toe Crevices -->
      <path d="M 305 466 C 305 472, 304 479, 304 485" stroke="#2D1D12" stroke-width="3" stroke-linecap="round" opacity="0.38" fill="none" />
      <path d="M 333 466 C 332 472, 331 479, 331 485" stroke="#2D1D12" stroke-width="3" stroke-linecap="round" opacity="0.38" fill="none" />
    </g>
  </g>

  <!-- 3. Facial Depressions & Eye Orbits (Heart-Shaped Owl Facial Mask) -->
  <!-- Left Eye Orbit Cavity -->
  <ellipse cx="195" cy="150" rx="44" ry="38" fill="url(#lOrbitGrad)" />
  <!-- Right Eye Orbit Cavity -->
  <ellipse cx="310" cy="150" rx="44" ry="38" fill="url(#rOrbitGrad)" />
  <!-- Brow bridge subtle indentation -->
  <ellipse cx="254" cy="138" rx="18" ry="14" fill="#886E5A" opacity="0.12" />

  <!-- 4. Sleepy Hooded Glassy Amber Eyes -->
  <!-- LEFT EYE -->
  <g id="left_eye">
    <!-- Amber Iris Sphere (Organic Aperture) -->
    <path d="M 168 143 C 180 140, 210 140, 224 148 C 224 162, 215 174, 203 178 C 193 180, 180 177, 172 168 C 167 160, 166 150, 168 143 Z" fill="url(#lIrisGrad)" />
    
    <!-- Pupil / Deep Obsidian Core -->
    <ellipse cx="196" cy="156" rx="9" ry="11" fill="#200B02" opacity="0.85" />
    
    <!-- Lower Iris Glowing Honey Crescent -->
    <path d="M 174 162 C 182 173, 204 175, 218 165 C 213 173, 198 178, 185 177 C 178 175, 174 168, 174 162 Z" fill="#FFB74D" opacity="0.65" />

    <!-- Eyelid Cast Shadow onto Eyeball -->
    <path d="M 168 143 C 180 140, 210 140, 224 148 C 222 156, 208 155, 195 153 C 182 151, 170 152, 168 143 Z" fill="url(#lEyeShadow)" />

    <!-- Specular Reflection Glint (Calibrated to 3D Ref: Top-Left under eyelid X=180, Y=145) -->
    <ellipse cx="180" cy="145" rx="3.2" ry="2.4" fill="#FFFFFF" opacity="0.95" />
    <ellipse cx="180" cy="145" rx="5.0" ry="3.5" fill="#FFEBB0" opacity="0.40" />

    <!-- Secondary Soft Reflection on Lower Rim -->
    <ellipse cx="212" cy="171" rx="2.5" ry="3.0" fill="#FFF0D0" opacity="0.45" />

    <!-- Porcelain Upper Eyelid Hood (Bulging 3D Fold) -->
    <path d="M 165 132 C 172 115, 216 116, 225 134 C 225 140, 224 148, 224 148 C 210 140, 180 140, 168 143 C 166 140, 165 134, 165 132 Z" fill="url(#lLidGrad)" />
    <!-- Eyelid Crease Soft Accent -->
    <path d="M 168 130 C 178 118, 212 118, 223 131" stroke="#B09682" stroke-width="1.8" stroke-linecap="round" opacity="0.35" fill="none" />
    <!-- Eyelid Hood Specular Highlight Peak -->
    <ellipse cx="195" cy="126" rx="14" ry="6" fill="#FFFFFF" opacity="0.25" />
  </g>

  <!-- RIGHT EYE -->
  <g id="right_eye">
    <!-- Amber Iris Sphere -->
    <path d="M 282 148 C 296 140, 326 140, 338 144 C 340 152, 338 162, 332 170 C 324 178, 310 180, 301 178 C 290 173, 282 161, 282 148 Z" fill="url(#rIrisGrad)" />
    
    <!-- Pupil / Deep Obsidian Core -->
    <ellipse cx="309" cy="156" rx="9" ry="11" fill="#180701" opacity="0.85" />
    
    <!-- Lower Iris Glowing Honey Crescent -->
    <path d="M 288 165 C 300 175, 320 174, 330 162 C 328 170, 316 177, 304 177 C 295 175, 290 170, 288 165 Z" fill="#F5A836" opacity="0.55" />

    <!-- Eyelid Cast Shadow -->
    <path d="M 282 148 C 296 140, 326 140, 338 144 C 336 153, 324 152, 310 153 C 298 154, 285 156, 282 148 Z" fill="url(#rEyeShadow)" />

    <!-- Specular Reflection Glint (Calibrated to 3D Ref: X=326, Y=165) -->
    <ellipse cx="326" cy="165" rx="2.8" ry="3.6" fill="#FFFFFF" opacity="0.92" />
    <ellipse cx="326" cy="165" rx="4.5" ry="5.0" fill="#FFDF9E" opacity="0.45" />

    <!-- Porcelain Upper Eyelid Hood (Bulging 3D Fold) -->
    <path d="M 283 134 C 292 116, 332 116, 340 133 C 340 138, 338 144, 338 144 C 326 140, 296 140, 282 148 C 282 143, 283 136, 283 134 Z" fill="url(#rLidGrad)" />
    <!-- Eyelid Crease Soft Accent -->
    <path d="M 285 132 C 296 119, 328 119, 337 131" stroke="#967E6C" stroke-width="1.8" stroke-linecap="round" opacity="0.40" fill="none" />
    <!-- Eyelid Hood Specular Highlight Peak -->
    <ellipse cx="310" cy="127" rx="13" ry="5" fill="#FFFFFF" opacity="0.18" />
  </g>

  <!-- 5. Seamless Rounded Porcelain Beak Cone (Y: 148 to 207) -->
  <g id="beak">
    <!-- Cast Shadow beneath beak tip onto breast -->
    <ellipse cx="254" cy="210" rx="13" ry="6" fill="url(#beakTipShadow)" />
    <!-- Beak Body Teardrop/Cone -->
    <path d="M 254 148 C 246 158, 241 174, 242 192 C 243 200, 247 207, 254 207 C 261 207, 265 200, 266 192 C 267 174, 262 158, 254 148 Z" fill="url(#beakGrad)" />
    <!-- Beak Longitudinal Highlight Ridge -->
    <path d="M 253 150 C 253 165, 253 190, 253 204" stroke="#FFFFFF" stroke-width="1.3" stroke-linecap="round" opacity="0.32" fill="none" />
    <!-- Right Beak Flank Ambient Occlusion -->
    <path d="M 254 150 C 260 162, 265 178, 265 195 C 265 202, 261 206, 257 207 C 263 204, 266 196, 266 190 C 266 174, 261 158, 254 150 Z" fill="#664D3B" opacity="0.30" />
  </g>
</svg>"""

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_str)
    return out_path

if __name__ == "__main__":
    svg_file = generate_svg()
    print("Generated:", svg_file)
    rendered = render_svg_chrome(svg_file)
    evaluate(rendered)
