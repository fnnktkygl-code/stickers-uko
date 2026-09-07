import os, sys, subprocess, re, cv2, numpy as np
from PIL import Image

def generate_svg(
    # Left eye params
    le_bowl_d="M 168 140 C 168 162, 178 179, 195 179 C 212 179, 222 162, 222 145 C 212 142, 185 139, 168 140 Z",
    le_hood_d="M 168 140 C 172 118, 218 118, 222 145 C 212 142, 185 139, 168 140 Z",
    le_rim_d="M 168 140.5 C 185 139.5, 212 142.5, 222 145.5",
    le_shadow_d="M 168 140 C 185 139, 212 142, 222 145 L 222 150 C 212 148, 185 146, 168 147 Z",
    
    # Right eye params
    re_bowl_d="M 283 145 C 283 162, 293 179, 310 179 C 327 179, 337 162, 337 140 C 320 139, 293 142, 283 145 Z",
    re_hood_d="M 283 145 C 288 118, 332 118, 337 140 C 320 139, 293 142, 283 145 Z",
    re_rim_d="M 283 145.5 C 293 142.5, 320 139.5, 337 140.5",
    re_shadow_d="M 283 145 C 293 142, 320 139, 337 140 L 337 147 C 320 146, 293 148, 283 150 Z",
    
    # Beak params
    beak_d="M 250 160 C 248 168, 244 178, 244 187 C 244 196, 248 204, 255 204 C 262 204, 266 196, 266 187 C 266 178, 262 168, 260 160 C 257 159, 253 159, 250 160 Z",
    beak_hl_d="M 251 163 C 249 172, 247 182, 249 196",
    beak_shadow_cx=255, beak_shadow_cy=206, beak_shadow_rx=11, beak_shadow_ry=4.5
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
      <stop offset="0%" stop-color="#7A6250" stop-opacity="0.25" />
      <stop offset="60%" stop-color="#7A6250" stop-opacity="0.08" />
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

    <!-- Soft Facial Orbital Depressions (Barn Owl facial disc concavity) -->
    <radialGradient id="orbitDiscL" cx="45%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.12" />
      <stop offset="70%" stop-color="#D8C4B2" stop-opacity="0.10" />
      <stop offset="100%" stop-color="#BCA592" stop-opacity="0" />
    </radialGradient>
    <radialGradient id="orbitDiscR" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#9A8270" stop-opacity="0.15" />
      <stop offset="70%" stop-color="#8C7462" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#8C7462" stop-opacity="0" />
    </radialGradient>

    <!-- Left Amber Iris -->
    <linearGradient id="amberEyeL" x1="30%" y1="10%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#3D1A04" />
      <stop offset="35%" stop-color="#5E2C0A" />
      <stop offset="65%" stop-color="#A86B20" />
      <stop offset="85%" stop-color="#E29A38" />
      <stop offset="100%" stop-color="#C57E24" />
    </linearGradient>

    <!-- Right Amber Iris -->
    <linearGradient id="amberEyeR" x1="20%" y1="15%" x2="80%" y2="85%">
      <stop offset="0%" stop-color="#361502" />
      <stop offset="30%" stop-color="#4F2408" />
      <stop offset="60%" stop-color="#8C5216" />
      <stop offset="82%" stop-color="#D08828" />
      <stop offset="100%" stop-color="#EAA63C" />
    </linearGradient>

    <!-- Translucent Warm Espresso Pupils -->
    <radialGradient id="pupilGradL" cx="50%" cy="45%" r="50%">
      <stop offset="0%" stop-color="#2D1002" />
      <stop offset="65%" stop-color="#481F06" />
      <stop offset="100%" stop-color="#6B300C" stop-opacity="0" />
    </radialGradient>
    <radialGradient id="pupilGradR" cx="45%" cy="45%" r="50%">
      <stop offset="0%" stop-color="#250C01" />
      <stop offset="65%" stop-color="#3D1603" />
      <stop offset="100%" stop-color="#5A2406" stop-opacity="0" />
    </radialGradient>

    <!-- Left Porcelain Eyelid Hood -->
    <linearGradient id="eyelidHoodL" x1="35%" y1="0%" x2="65%" y2="100%">
      <stop offset="0%" stop-color="#FFFDF9" />
      <stop offset="45%" stop-color="#F7EEE4" />
      <stop offset="75%" stop-color="#E2CCA8" />
      <stop offset="100%" stop-color="#CBB198" />
    </linearGradient>

    <!-- Right Porcelain Eyelid Hood -->
    <linearGradient id="eyelidHoodR" x1="25%" y1="0%" x2="75%" y2="100%">
      <stop offset="0%" stop-color="#F2E4D6" />
      <stop offset="45%" stop-color="#DFC4AD" />
      <stop offset="75%" stop-color="#C2A28A" />
      <stop offset="100%" stop-color="#A88870" />
    </linearGradient>

    <!-- Eyelid Cast Shadow on Eyeball -->
    <linearGradient id="eyeShadow" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#140601" stop-opacity="0.80" />
      <stop offset="60%" stop-color="#3A1604" stop-opacity="0.35" />
      <stop offset="100%" stop-color="#662C05" stop-opacity="0" />
    </linearGradient>

    <!-- Seamless Volumetric Porcelain Beak Gradient -->
    <linearGradient id="beakGrad" x1="20%" y1="10%" x2="80%" y2="90%">
      <stop offset="0%" stop-color="#FFF8F0" />
      <stop offset="25%" stop-color="#EEDECD" />
      <stop offset="55%" stop-color="#D2BCAB" />
      <stop offset="80%" stop-color="#B19682" />
      <stop offset="100%" stop-color="#8C7462" />
    </linearGradient>

    <!-- Soft Under-Beak Ambient Shadow -->
    <radialGradient id="beakTipShadow" cx="50%" cy="40%" r="50%">
      <stop offset="0%" stop-color="#4A3424" stop-opacity="0.52" />
      <stop offset="65%" stop-color="#4A3424" stop-opacity="0.18" />
      <stop offset="100%" stop-color="#4A3424" stop-opacity="0" />
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

    <!-- Upper Right Head Shadow (Continuous spherical cranial falloff) -->
    <ellipse cx="340" cy="95" rx="90" ry="70" fill="url(#headRightShadow)" />

    <!-- Soft Concave Orbital Discs -->
    <ellipse cx="195" cy="154" rx="42" ry="38" fill="url(#orbitDiscL)" />
    <ellipse cx="310" cy="154" rx="42" ry="38" fill="url(#orbitDiscR)" />

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
    <!-- Amber Iris Spherical Bowl -->
    <path d="{le_bowl_d}" fill="url(#amberEyeL)" />
    <!-- Orbit Cavity Ambient Occlusion Rim -->
    <path d="{le_bowl_d}" stroke="#5C3B24" stroke-width="1.2" fill="none" opacity="0.28" />
    <!-- Pupil (Centered Espresso Translucent Disk) -->
    <ellipse cx="195" cy="153" rx="13.5" ry="12" fill="url(#pupilGradL)" />
    <!-- Golden Luminous Caustic Rim -->
    <path d="M 174 165 C 180 174, 192 178, 206 177 C 215 175.5, 221 169, 222 163 C 218 171, 208 175.5, 196 175.5 C 185 175.5, 178 170, 174 165 Z" fill="#FFE08A" opacity="0.75" />
    <!-- Concentrated Caustic Pool at lower right -->
    <ellipse cx="205" cy="172" rx="6.5" ry="3.8" fill="#FFF0B0" opacity="0.65" />
    <!-- Eyelid Cast Shadow on eyeball -->
    <path d="{le_shadow_d}" fill="url(#eyeShadow)" />
    
    <!-- Specular Reflection Glint (Calibrated to Ref X=185.5, Y=142.5) -->
    <ellipse cx="185.5" cy="142.5" rx="2.2" ry="1.8" fill="#FFFFFF" opacity="0.95" />
    <ellipse cx="185.5" cy="142.5" rx="4.0" ry="3.0" fill="#FFF8E0" opacity="0.40" />

    <!-- Porcelain Upper Eyelid Hood (Gentle Arched Crease) -->
    <path d="{le_hood_d}" fill="url(#eyelidHoodL)" />
    <!-- Eyelid Lower Porcelain Edge Highlight -->
    <path d="{le_rim_d}" stroke="#FFFDF8" stroke-width="1.2" stroke-linecap="round" opacity="0.65" fill="none" />
    <!-- Soft Eyelid Crease Shadow -->
    <path d="M 168 140 C 172 118, 218 118, 222 145" stroke="#9E826C" stroke-width="1.0" stroke-linecap="round" opacity="0.20" fill="none" />
  </g>

  <!-- Right Eye -->
  <g id="right_eye">
    <!-- Amber Iris Spherical Bowl -->
    <path d="{re_bowl_d}" fill="url(#amberEyeR)" />
    <!-- Orbit Cavity Ambient Occlusion Rim -->
    <path d="{re_bowl_d}" stroke="#4E311B" stroke-width="1.2" fill="none" opacity="0.28" />
    <!-- Pupil (Centered Espresso Translucent Disk) -->
    <ellipse cx="310" cy="153" rx="13.5" ry="12" fill="url(#pupilGradR)" />
    <!-- Golden Luminous Caustic Rim -->
    <path d="M 298 171 C 306 177, 318 177.5, 328 173 C 334 169, 337 163, 337 157 C 335 164, 327 170, 318 171.5 C 309 171.5, 303 170, 298 171 Z" fill="#E8A440" opacity="0.65" />
    <!-- Concentrated Caustic Pool on right side -->
    <ellipse cx="325" cy="168" rx="5.5" ry="4.2" fill="#FFC960" opacity="0.85" />
    <ellipse cx="325" cy="168" rx="3.0" ry="2.2" fill="#FFE890" opacity="0.90" />

    <!-- Eyelid Cast Shadow on eyeball -->
    <path d="{re_shadow_d}" fill="url(#eyeShadow)" />

    <!-- Specular Highlight Glint (Top rim) -->
    <ellipse cx="332" cy="141.0" rx="2.0" ry="1.6" fill="#FFEEC8" opacity="0.75" />

    <!-- Porcelain Upper Eyelid Hood -->
    <path d="{re_hood_d}" fill="url(#eyelidHoodR)" />
    <!-- Eyelid Lower Porcelain Edge Highlight -->
    <path d="{re_rim_d}" stroke="#F6ECE0" stroke-width="1.2" stroke-linecap="round" opacity="0.55" fill="none" />
    <!-- Soft Eyelid Crease Shadow -->
    <path d="M 283 145 C 288 118, 332 118, 337 140" stroke="#7A604D" stroke-width="1.0" stroke-linecap="round" opacity="0.25" fill="none" />
  </g>

  <!-- 4. Plump Rounded 3D Porcelain Beak Cone (Nested between eyes, width=22px) -->
  <g id="beak">
    <!-- Cast Shadow beneath beak tip onto breast -->
    <ellipse cx="{beak_shadow_cx}" cy="{beak_shadow_cy}" rx="{beak_shadow_rx}" ry="{beak_shadow_ry}" fill="url(#beakTipShadow)" />
    <!-- Plump Volumetric Pear/Cone Beak Body (starts at Y=160 at bridge, swells smoothly into pear cone at Y=184..188, rounds to Y=204, width=22px) -->
    <path d="{beak_d}" fill="url(#beakGrad)" />
    <!-- Longitudinal Soft Volumetric Highlight Ridge -->
    <path d="{beak_hl_d}" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" opacity="0.32" fill="none" />
    <!-- Soft Apex Volume Highlight -->
    <ellipse cx="251" cy="184" rx="3.5" ry="7.0" fill="#FFFFFF" opacity="0.20" />
  </g>
</svg>
"""
    return svg

svg_content = generate_svg()
with open('scratch/test_owluko_v28.svg', 'w') as f:
    f.write(svg_content)

print("Generated scratch/test_owluko_v28.svg")
