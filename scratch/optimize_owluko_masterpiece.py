import os, sys, subprocess, re, cv2, numpy as np
from PIL import Image

def build_svg(
    le_bowl="M 168 141 C 165 152, 169 167, 180 175 C 185 178.5, 190 180, 195 180 C 200 180, 206 178.5, 211 175 C 221 167, 226 152, 223 142 C 212 140, 180 139.5, 168 141 Z",
    re_bowl="M 283 142 C 280 152, 284 167, 294 175 C 299 178.5, 305 180, 311 180 C 317 180, 323 178.5, 328 175 C 338 167, 343 152, 340 141 C 329 139.5, 295 140, 283 142 Z",
    le_hood="M 167 140 C 173 119, 217 119, 223 142 C 212 140, 179 139.5, 167 140 Z",
    re_hood="M 283 142 C 289 119, 334 119, 340 140 C 329 139.5, 295 140, 283 142 Z",
    le_rim="M 167.5 140.8 C 180 139.6, 210 140.2, 222.5 142.2",
    re_rim="M 283.5 142.2 C 295 140.2, 325 139.6, 339.5 140.8",
    le_shadow="M 168 141 C 180 139.5, 212 140, 223 142 L 223 148 C 212 146, 180 145.5, 168 147 Z",
    re_shadow="M 283 142 C 295 140, 329 139.5, 340 141 L 340 147 C 329 145.5, 295 146, 283 148 Z",
    beak_path="M 252 150 C 248 165, 243.5 178, 243.5 188 C 243.5 197, 248 204.5, 254.5 204.5 C 261 204.5, 265.5 197, 265.5 188 C 265.5 178, 261 165, 257 150 C 255 149, 254 149, 252 150 Z",
    beak_hl="M 251 156 C 248.5 169, 247.5 182, 249.5 196",
    beak_shadow_y=206.5,
    beak_shadow_rx=12,
    beak_shadow_ry=5,
    beak_grad_stop3="#BEA692",
    beak_grad_stop4="#8A715C"
):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" style="background: transparent;">
  <defs>
    <!-- Master Body Silhouette Clip -->
    <clipPath id="bodyClip">
      <path d="M 272 40 L 237 40 L 216 44 L 207 48 L 201 49 L 185 57 L 168 69 L 155 82 L 147 94 L 145 95 L 132 119 L 126 134 L 124 145 L 120 155 L 120 162 L 116 174 L 115 183 L 103 194 L 95 213 L 92 231 L 90 235 L 90 246 L 88 255 L 87 271 L 90 314 L 96 339 L 105 359 L 109 363 L 110 366 L 119 374 L 127 377 L 132 382 L 144 400 L 151 407 L 168 421 L 186 430 L 192 437 L 188 451 L 183 459 L 178 462 L 164 465 L 158 470 L 155 479 L 157 485 L 160 488 L 169 489 L 176 485 L 180 485 L 186 489 L 198 489 L 206 485 L 214 485 L 220 489 L 224 489 L 231 486 L 233 482 L 231 469 L 221 461 L 217 451 L 218 445 L 224 441 L 242 443 L 293 441 L 297 446 L 297 455 L 293 461 L 283 470 L 280 476 L 280 484 L 283 488 L 293 489 L 300 485 L 308 485 L 314 489 L 324 489 L 329 485 L 337 485 L 340 487 L 349 488 L 352 487 L 356 483 L 356 474 L 351 466 L 338 462 L 329 456 L 323 442 L 323 434 L 327 429 L 334 427 L 337 424 L 344 421 L 356 411 L 372 395 L 380 382 L 385 377 L 391 376 L 397 373 L 404 366 L 407 358 L 411 353 L 411 350 L 416 339 L 416 334 L 421 317 L 424 290 L 424 260 L 420 228 L 416 217 L 416 213 L 409 197 L 409 194 L 396 183 L 392 166 L 391 155 L 389 152 L 385 135 L 382 130 L 379 120 L 364 93 L 347 73 L 331 60 L 311 50 L 305 49 L 293 44 L 277 42 Z" />
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
    <linearGradient id="amberEyeL" x1="30%" y1="10%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#462006" />
      <stop offset="38%" stop-color="#6E3A10" />
      <stop offset="68%" stop-color="#BA7D28" />
      <stop offset="88%" stop-color="#EAA646" />
      <stop offset="100%" stop-color="#D28C2E" />
    </linearGradient>

    <!-- Right Amber Iris -->
    <linearGradient id="amberEyeR" x1="15%" y1="15%" x2="85%" y2="85%">
      <stop offset="0%" stop-color="#3A1804" />
      <stop offset="30%" stop-color="#552B0C" />
      <stop offset="58%" stop-color="#8F561A" />
      <stop offset="82%" stop-color="#CE8828" />
      <stop offset="100%" stop-color="#EAA236" />
    </linearGradient>

    <!-- Translucent Warm Espresso Pupils -->
    <radialGradient id="pupilGradL" cx="50%" cy="45%" r="50%">
      <stop offset="0%" stop-color="#2D1102" />
      <stop offset="70%" stop-color="#482006" />
      <stop offset="100%" stop-color="#6B300C" stop-opacity="0" />
    </radialGradient>
    <radialGradient id="pupilGradR" cx="45%" cy="45%" r="50%">
      <stop offset="0%" stop-color="#260C01" />
      <stop offset="70%" stop-color="#3F1703" />
      <stop offset="100%" stop-color="#5A2406" stop-opacity="0" />
    </radialGradient>

    <!-- Left Porcelain Eyelid Hood -->
    <linearGradient id="eyelidHoodL" x1="35%" y1="0%" x2="65%" y2="100%">
      <stop offset="0%" stop-color="#FFFDF9" />
      <stop offset="45%" stop-color="#F6EDE3" />
      <stop offset="78%" stop-color="#DEBEA6" />
      <stop offset="100%" stop-color="#C2A088" />
    </linearGradient>

    <!-- Right Porcelain Eyelid Hood -->
    <linearGradient id="eyelidHoodR" x1="20%" y1="0%" x2="80%" y2="100%">
      <stop offset="0%" stop-color="#EFE2D4" />
      <stop offset="45%" stop-color="#DAC0AB" />
      <stop offset="78%" stop-color="#BDA088" />
      <stop offset="100%" stop-color="#A4846E" />
    </linearGradient>

    <!-- Eyelid Cast Shadow on Eyeball -->
    <linearGradient id="eyeShadow" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#140602" stop-opacity="0.75" />
      <stop offset="60%" stop-color="#3D1804" stop-opacity="0.32" />
      <stop offset="100%" stop-color="#723306" stop-opacity="0" />
    </linearGradient>

    <!-- Seamless Volumetric Porcelain Beak Gradient -->
    <linearGradient id="beakGrad" x1="22%" y1="10%" x2="78%" y2="90%">
      <stop offset="0%" stop-color="#FFF8F0" />
      <stop offset="28%" stop-color="#E8D5C6" />
      <stop offset="65%" stop-color="{beak_grad_stop3}" />
      <stop offset="100%" stop-color="{beak_grad_stop4}" />
    </linearGradient>

    <!-- Soft Under-Beak Ambient Shadow -->
    <radialGradient id="beakTipShadow" cx="50%" cy="45%" r="50%">
      <stop offset="0%" stop-color="#543A26" stop-opacity="0.50" />
      <stop offset="65%" stop-color="#543A26" stop-opacity="0.18" />
      <stop offset="100%" stop-color="#543A26" stop-opacity="0" />
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
  <path d="M 272 40 L 237 40 L 216 44 L 207 48 L 201 49 L 185 57 L 168 69 L 155 82 L 147 94 L 145 95 L 132 119 L 126 134 L 124 145 L 120 155 L 120 162 L 116 174 L 115 183 L 103 194 L 95 213 L 92 231 L 90 235 L 90 246 L 88 255 L 87 271 L 90 314 L 96 339 L 105 359 L 109 363 L 110 366 L 119 374 L 127 377 L 132 382 L 144 400 L 151 407 L 168 421 L 186 430 L 192 437 L 188 451 L 183 459 L 178 462 L 164 465 L 158 470 L 155 479 L 157 485 L 160 488 L 169 489 L 176 485 L 180 485 L 186 489 L 198 489 L 206 485 L 214 485 L 220 489 L 224 489 L 231 486 L 233 482 L 231 469 L 221 461 L 217 451 L 218 445 L 224 441 L 242 443 L 293 441 L 297 446 L 297 455 L 293 461 L 283 470 L 280 476 L 280 484 L 283 488 L 293 489 L 300 485 L 308 485 L 314 489 L 324 489 L 329 485 L 337 485 L 340 487 L 349 488 L 352 487 L 356 483 L 356 474 L 351 466 L 338 462 L 329 456 L 323 442 L 323 434 L 327 429 L 334 427 L 337 424 L 344 421 L 356 411 L 372 395 L 380 382 L 385 377 L 391 376 L 397 373 L 404 366 L 407 358 L 411 353 L 411 350 L 416 339 L 416 334 L 421 317 L 424 290 L 424 260 L 420 228 L 416 217 L 416 213 L 409 197 L 409 194 L 396 183 L 392 166 L 391 155 L 389 152 L 385 135 L 382 130 L 379 120 L 364 93 L 347 73 L 331 60 L 311 50 L 305 49 L 293 44 L 277 42 Z" fill="url(#bodyGrad)" />

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

  <!-- 3. Sleepy Hooded Glassy Amber Eyes (Relaxed Symmetrical Hoods & Caustics) -->
  <!-- Left Eye -->
  <g id="left_eye">
    <!-- Amber Iris (Relaxed, smooth spherical bowl) -->
    <path d="{le_bowl}" fill="url(#amberEyeL)" />
    <!-- Pupil -->
    <ellipse cx="195.5" cy="154" rx="14" ry="12" fill="url(#pupilGradL)" />
    <!-- Lower Golden Luminous Rim -->
    <path d="M 174 167 C 181 176, 193 178.5, 206 177.5 C 214 176, 220 170, 222 165 C 218 171, 208 175.5, 196 175.5 C 185 175.5, 178 170.5, 174 167 Z" fill="#FFE08E" opacity="0.72" />
    <!-- Eyelid Cast Shadow on eyeball -->
    <path d="{le_shadow}" fill="url(#eyeShadow)" />
    
    <!-- Specular Reflection Glint (Calibrated to Ref X=185.5, Y=142.5) -->
    <ellipse cx="185.5" cy="142.5" rx="2.5" ry="2.0" fill="#FFFFFF" opacity="0.95" />
    <ellipse cx="185.5" cy="142.5" rx="4.2" ry="3.2" fill="#FFF8E0" opacity="0.40" />

    <!-- Porcelain Upper Eyelid Hood (Gentle Arched Crease) -->
    <path d="{le_hood}" fill="url(#eyelidHoodL)" />
    <!-- Eyelid Lower Porcelain Edge Highlight -->
    <path d="{le_rim}" stroke="#FFFDF8" stroke-width="1.1" stroke-linecap="round" opacity="0.60" fill="none" />
  </g>

  <!-- Right Eye -->
  <g id="right_eye">
    <!-- Amber Iris (Relaxed, smooth spherical bowl) -->
    <path d="{re_bowl}" fill="url(#amberEyeR)" />
    <!-- Pupil -->
    <ellipse cx="310.5" cy="153" rx="13.5" ry="11.5" fill="url(#pupilGradR)" />
    <!-- Lower Golden Luminous Rim -->
    <path d="M 300 172.5 C 309 177.5, 321 177.5, 331 172.5 C 336 168, 338 162, 339 157 C 336 163, 328 169, 319 171 C 311 171, 305 171, 300 172.5 Z" fill="#E8A23C" opacity="0.62" />
    <!-- Caustic Pool on right side -->
    <ellipse cx="327" cy="164" rx="3.8" ry="4.2" fill="#FFB428" opacity="0.85" />
    <ellipse cx="327" cy="164" rx="2.2" ry="2.4" fill="#FFDC78" opacity="0.92" />

    <!-- Eyelid Cast Shadow -->
    <path d="{re_shadow}" fill="url(#eyeShadow)" />

    <!-- Specular Highlight Glint (Top rim) -->
    <ellipse cx="304" cy="141.5" rx="2.2" ry="1.8" fill="#FFE8C2" opacity="0.72" />

    <!-- Porcelain Upper Eyelid Hood -->
    <path d="{re_hood}" fill="url(#eyelidHoodR)" />
    <!-- Eyelid Lower Porcelain Edge Highlight -->
    <path d="{re_rim}" stroke="#F6ECE0" stroke-width="1.1" stroke-linecap="round" opacity="0.52" fill="none" />
  </g>

  <!-- 4. Plump Rounded 3D Porcelain Beak Cone (Width=22px, Height=37px) -->
  <g id="beak">
    <!-- Cast Shadow beneath beak tip onto breast -->
    <ellipse cx="254.5" cy="{beak_shadow_y}" rx="{beak_shadow_rx}" ry="{beak_shadow_ry}" fill="url(#beakTipShadow)" />
    <!-- Plump Volumetric Pear/Cone Beak Body (starts at Y=150 at bridge, swells smoothly into pear cone at Y=180..194, rounds to Y=204.5, width=22px) -->
    <path d="{beak_path}" fill="url(#beakGrad)" />
    <!-- Longitudinal Soft Volumetric Highlight Ridge -->
    <path d="{beak_hl}" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" opacity="0.28" fill="none" />
    <!-- Soft Apex Volume Highlight -->
    <ellipse cx="251" cy="184" rx="3.2" ry="6.5" fill="#FFFFFF" opacity="0.18" />
  </g>
</svg>
"""
    return svg

def evaluate(svg_str, tag='opt'):
    tmp_svg = f'scratch/{tag}.svg'
    tmp_png = f'scratch/{tag}.png'
    with open(tmp_svg, 'w') as f:
        f.write(svg_str)
        
    cmd = [
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        '--headless',
        '--disable-gpu',
        '--run-all-compositor-stages-before-draw',
        f'--screenshot={os.path.abspath(tmp_png)}',
        '--window-size=512,512',
        '--default-background-color=00000000',
        f'file://{os.path.abspath(tmp_svg)}'
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    ref = np.array(Image.open('mascots/owluko/owluko_master_exact_512.png').convert('RGBA'))
    vec = np.array(Image.open(tmp_png).convert('RGBA'))
    
    ref_lab = cv2.cvtColor(ref[:,:,:3], cv2.COLOR_RGB2LAB).astype(np.float32)
    vec_lab = cv2.cvtColor(vec[:,:,:3], cv2.COLOR_RGB2LAB).astype(np.float32)
    de = np.sqrt(np.sum((ref_lab - vec_lab)**2, axis=2))
    
    face_mask = np.zeros((512,512), dtype=bool)
    face_mask[100:220, 150:360] = True
    
    le_mask = np.zeros((512,512), dtype=bool)
    le_mask[135:185, 165:228] = True
    
    re_mask = np.zeros((512,512), dtype=bool)
    re_mask[135:185, 275:345] = True
    
    beak_mask = np.zeros((512,512), dtype=bool)
    beak_mask[145:212, 235:275] = True
    
    fh_mask = np.zeros((512,512), dtype=bool)
    fh_mask[95:135, 180:330] = True
    
    ref_mask = ref[:,:,3] > 20
    vec_mask_alpha = vec[:,:,3] > 20
    inter = ref_mask & vec_mask_alpha
    
    ref_gray = cv2.cvtColor(ref[:,:,:3], cv2.COLOR_RGB2GRAY)
    vec_gray = cv2.cvtColor(vec[:,:,:3], cv2.COLOR_RGB2GRAY)
    
    C1, C2 = (0.01*255)**2, (0.03*255)**2
    kernel = cv2.getGaussianKernel(11, 1.5)
    window = np.outer(kernel, kernel.transpose())
    mu1 = cv2.filter2D(ref_gray.astype(float), -1, window)
    mu2 = cv2.filter2D(vec_gray.astype(float), -1, window)
    ssim = ((2*mu1*mu2 + C1)*(2*cv2.filter2D((ref_gray*vec_gray).astype(float), -1, window) - 2*mu1*mu2 + C2)) / ((mu1**2 + mu2**2 + C1)*(cv2.filter2D((ref_gray**2).astype(float), -1, window) - mu1**2 + cv2.filter2D((vec_gray**2).astype(float), -1, window) - mu2**2 + C2))
    
    # Save visual comparison
    face_ref = ref[100:220, 150:360, :3]
    face_vec = vec[100:220, 150:360, :3]
    de_face = de[100:220, 150:360]
    de_vis = np.clip(de_face * 3.5, 0, 255).astype(np.uint8)
    de_color = cv2.cvtColor(cv2.applyColorMap(de_vis, cv2.COLORMAP_JET), cv2.COLOR_BGR2RGB)
    def z(img): return cv2.resize(img, (img.shape[1]*3, img.shape[0]*3), interpolation=cv2.INTER_NEAREST)
    comp = np.hstack([z(face_ref), z(face_vec), z(de_color)])
    Image.fromarray(comp).save(f'scratch/{tag}_comp.png')
    
    print(f'[{tag}] Face DE: {de[face_mask].mean():.2f} | LE DE: {de[le_mask].mean():.2f} | RE DE: {de[re_mask].mean():.2f} | Beak DE: {de[beak_mask].mean():.2f} | Forehead DE: {de[fh_mask].mean():.2f} | Global DE: {de[inter].mean():.2f} | SSIM: {ssim[inter].mean()*100:.2f}%')
    return {
        'face_de': de[face_mask].mean(),
        'le_de': de[le_mask].mean(),
        're_de': de[re_mask].mean(),
        'beak_de': de[beak_mask].mean(),
        'fh_de': de[fh_mask].mean(),
        'global_de': de[inter].mean(),
        'ssim': ssim[inter].mean()*100
    }

s = build_svg()
evaluate(s, 'masterpiece_v1')
