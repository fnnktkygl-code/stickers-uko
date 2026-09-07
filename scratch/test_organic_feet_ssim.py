import sys
sys.path.append(".")
import cv2, numpy as np
from PIL import Image
from scripts.benchmark_owluko_fidelity import compute_ssim_numpy, render_svg

ref_full = np.array(Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA"))
ref_feet = ref_full[435:495, 150:360]
r_gray = cv2.cvtColor(ref_feet[:, :, :3], cv2.COLOR_RGB2GRAY)
inter = (ref_feet[:, :, 3] > 20)

def test_feet_config(
    l_grad_stops=[("#D4C0AF", 0), ("#A89381", 45), ("#6B5442", 85), ("#483526", 100)],
    r_grad_stops=[("#BAA594", 0), ("#8D7866", 45), ("#584434", 85), ("#38271A", 100)],
    crevice_op=0.45,
    hl_op=0.28
):
    l_stops_svg = "".join([f'<stop offset="{s[1]}%" stop-color="{s[0]}" />' for s in l_grad_stops])
    r_stops_svg = "".join([f'<stop offset="{s[1]}%" stop-color="{s[0]}" />' for s in r_grad_stops])
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="150 435 210 60" width="210" height="60" style="background: transparent;">
  <defs>
    <linearGradient id="lFoot" x1="30%" y1="0%" x2="70%" y2="100%">
      {l_stops_svg}
    </linearGradient>
    <linearGradient id="rFoot" x1="30%" y1="0%" x2="70%" y2="100%">
      {r_stops_svg}
    </linearGradient>
    <!-- Soft crevice shadow gradient -->
    <radialGradient id="creviceGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#2D1B0E" stop-opacity="{crevice_op}" />
      <stop offset="60%" stop-color="#2D1B0E" stop-opacity="{crevice_op * 0.4}" />
      <stop offset="100%" stop-color="#2D1B0E" stop-opacity="0" />
    </radialGradient>
    <!-- Soft toe knuckle highlight -->
    <radialGradient id="toeHl" cx="45%" cy="40%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="{hl_op}" />
      <stop offset="50%" stop-color="#FFFFFF" stop-opacity="{hl_op * 0.35}" />
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0" />
    </radialGradient>
  </defs>

  <!-- Left Foot Whole Organic Mesh -->
  <path d="M 155 479 L 157 485 L 160 488 L 169 489 L 176 485 L 180 485 L 186 489 L 198 489 L 206 485 L 214 485 L 220 489 L 228 488 L 231 486 L 233 482 L 231 469 L 227 465 L 225 465 L 219 458 L 217 451 L 217 447 L 221 442 L 224 441 L 239 442 L 239 435 L 191 435 L 192 439 L 190 442 L 190 445 L 185 457 L 178 462 L 174 462 L 171 464 L 167 464 L 162 466 L 158 470 Z" fill="url(#lFoot)" />

  <!-- Left Foot Knuckle Highlights -->
  <ellipse cx="168" cy="477" rx="8" ry="5" fill="url(#toeHl)" />
  <ellipse cx="196" cy="470" rx="9" ry="6" fill="url(#toeHl)" />
  <ellipse cx="221" cy="477" rx="8" ry="5" fill="url(#toeHl)" />

  <!-- Left Foot Soft Crevices (NO hard strokes) -->
  <ellipse cx="179" cy="475" rx="3.5" ry="12" fill="url(#creviceGrad)" />
  <ellipse cx="208" cy="473" rx="3.5" ry="12" fill="url(#creviceGrad)" />

  <!-- Right Foot Whole Organic Mesh -->
  <path d="M 270 435 L 270 442 L 293 441 L 297 446 L 297 455 L 293 461 L 283 470 L 280 476 L 280 484 L 283 488 L 293 489 L 300 485 L 308 485 L 314 489 L 324 489 L 329 485 L 337 485 L 340 487 L 349 488 L 352 487 L 356 483 L 356 474 L 353 468 L 351 466 L 338 462 L 332 459 L 329 456 L 323 442 L 323 435 Z" fill="url(#rFoot)" />

  <!-- Right Foot Knuckle Highlights -->
  <ellipse cx="292" cy="477" rx="8" ry="5" fill="url(#toeHl)" opacity="0.65" />
  <ellipse cx="316" cy="470" rx="9" ry="6" fill="url(#toeHl)" opacity="0.75" />
  <ellipse cx="342" cy="477" rx="8" ry="5" fill="url(#toeHl)" opacity="0.55" />

  <!-- Right Foot Soft Crevices -->
  <ellipse cx="303" cy="473" rx="3.5" ry="12" fill="url(#creviceGrad)" />
  <ellipse cx="330" cy="475" rx="3.5" ry="12" fill="url(#creviceGrad)" />
</svg>"""
    with open("scratch/temp_feet_test.svg", "w") as f:
        f.write(svg)
    png = render_svg("scratch/temp_feet_test.svg", "scratch/temp_feet_test.png")
    vec_feet = np.array(Image.open(png).convert("RGBA"))
    v_gray = cv2.cvtColor(vec_feet[:, :, :3], cv2.COLOR_RGB2GRAY)
    
    ssim = compute_ssim_numpy(r_gray, v_gray).mean()
    
    r_flat = r_gray[inter].astype(float)
    v_flat = v_gray[inter].astype(float)
    ncc = np.corrcoef(r_flat, v_flat)[0, 1]
    
    print(f"Isolated Feet SSIM: {ssim*100:.2f}%, NCC: {ncc*100:.2f}%")
    return ssim, ncc

test_feet_config()
