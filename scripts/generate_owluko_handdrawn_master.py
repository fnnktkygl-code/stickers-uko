import math

def generate_handdrawn_owluko_svg(filepath):
    """
    Generate an authentic, hand-drawn vector illustration of Owluko.
    - Continuous chubby downy pear body.
    - Integrated lateral flank wings (natural folds resting against belly, NOT pasted on!).
    - Heart-shaped barn owl facial disk.
    - Glassy amber orb eyes with depth, eyelids, and specular glints.
    - Cute rounded terracotta beak.
    - 3 chubby bean toes per foot emerging naturally from beneath the belly down.
    - Organic character linework (warm dark cocoa strokes, round caps/joins).
    - Soft volumetric warmth and cel-shaded folds.
    """
    
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <!-- Soft Ground Shadow Gradient -->
    <radialGradient id="groundShadow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#2D1A0E" stop-opacity="0.25" />
      <stop offset="50%" stop-color="#2D1A0E" stop-opacity="0.10" />
      <stop offset="100%" stop-color="#2D1A0E" stop-opacity="0" />
    </radialGradient>
    <radialGradient id="groundContactShadow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#1A0D06" stop-opacity="0.35" />
      <stop offset="70%" stop-color="#1A0D06" stop-opacity="0.10" />
      <stop offset="100%" stop-color="#1A0D06" stop-opacity="0" />
    </radialGradient>

    <!-- Main Body Warm Down Gradient -->
    <radialGradient id="bodyBaseGrad" cx="44%" cy="32%" r="65%">
      <stop offset="0%" stop-color="#FFFDF9" />
      <stop offset="45%" stop-color="#F7EFE2" />
      <stop offset="75%" stop-color="#EADBCC" />
      <stop offset="100%" stop-color="#D2BEA6" />
    </radialGradient>

    <!-- Belly Lighter Down Gradient -->
    <radialGradient id="bellyGrad" cx="50%" cy="40%" r="55%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="60%" stop-color="#FAF5EC" />
      <stop offset="85%" stop-color="#EFE5D6" />
      <stop offset="100%" stop-color="#DECDB7" />
    </radialGradient>

    <!-- Facial Disk Heart Gradient -->
    <radialGradient id="facialDiskGrad" cx="50%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="65%" stop-color="#FAF6EE" />
      <stop offset="85%" stop-color="#EFE6D7" />
      <stop offset="100%" stop-color="#DFCFB9" />
    </radialGradient>

    <!-- Wing Lateral Shading Gradients -->
    <linearGradient id="wingLeftGrad" x1="0%" y1="20%" x2="100%" y2="80%">
      <stop offset="0%" stop-color="#F5EDE0" />
      <stop offset="60%" stop-color="#E5D6C1" />
      <stop offset="100%" stop-color="#D0BC9F" />
    </linearGradient>
    <linearGradient id="wingRightGrad" x1="100%" y1="20%" x2="0%" y2="80%">
      <stop offset="0%" stop-color="#F5EDE0" />
      <stop offset="60%" stop-color="#E5D6C1" />
      <stop offset="100%" stop-color="#D0BC9F" />
    </linearGradient>

    <!-- Eye Amber Radial Gradients -->
    <radialGradient id="eyeAmberGradL" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#FDE047" />
      <stop offset="30%" stop-color="#F59E0B" />
      <stop offset="65%" stop-color="#D97706" />
      <stop offset="88%" stop-color="#92400E" />
      <stop offset="100%" stop-color="#451A03" />
    </radialGradient>
    <radialGradient id="eyeAmberGradR" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#FDE047" />
      <stop offset="30%" stop-color="#F59E0B" />
      <stop offset="65%" stop-color="#D97706" />
      <stop offset="88%" stop-color="#92400E" />
      <stop offset="100%" stop-color="#451A03" />
    </radialGradient>

    <!-- Beak Gradient -->
    <linearGradient id="beakGrad" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#FDBA74" />
      <stop offset="40%" stop-color="#F97316" />
      <stop offset="80%" stop-color="#EA580C" />
      <stop offset="100%" stop-color="#9A3412" />
    </linearGradient>

    <!-- Feet Toes Gradient -->
    <linearGradient id="toeGrad" x1="40%" y1="0%" x2="60%" y2="100%">
      <stop offset="0%" stop-color="#FDBA74" />
      <stop offset="40%" stop-color="#F97316" />
      <stop offset="80%" stop-color="#EA580C" />
      <stop offset="100%" stop-color="#9A3412" />
    </linearGradient>

    <!-- Soft Cheek Blush Radial -->
    <radialGradient id="blushGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#F87171" stop-opacity="0.25" />
      <stop offset="60%" stop-color="#F87171" stop-opacity="0.10" />
      <stop offset="100%" stop-color="#F87171" stop-opacity="0" />
    </radialGradient>
  </defs>

  <!-- 01. GROUND SHADOW -->
  <g id="ground_shadow_group">
    <ellipse cx="256" cy="470" rx="160" ry="22" fill="url(#groundShadow)" />
    <ellipse cx="256" cy="468" rx="110" ry="12" fill="url(#groundContactShadow)" />
  </g>

  <!-- 02. FEET (3 plump rounded bean toes per foot, resting on floor plane) -->
  <g id="feet_group">
    <!-- LEFT FOOT (Centered under left eye at x=190, y=462) -->
    <g id="foot_left">
      <!-- Toe 1 (Outer left) -->
      <path d="M 166 450 C 160 450, 154 456, 154 463 C 154 470, 161 475, 168 474 C 175 473, 178 467, 178 459 C 178 453, 173 450, 166 450 Z"
            fill="url(#toeGrad)" stroke="#6C2A0C" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />
      <!-- Toe 3 (Inner right) -->
      <path d="M 214 450 C 207 450, 202 453, 202 459 C 202 467, 205 473, 212 474 C 219 475, 226 470, 226 463 C 226 456, 220 450, 214 450 Z"
            fill="url(#toeGrad)" stroke="#6C2A0C" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />
      <!-- Toe 2 (Middle, slightly larger and proud) -->
      <path d="M 190 446 C 182 446, 176 452, 176 461 C 176 470, 183 476, 190 476 C 197 476, 204 470, 204 461 C 204 452, 198 446, 190 446 Z"
            fill="url(#toeGrad)" stroke="#6C2A0C" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />
      <!-- Toe highlights -->
      <ellipse cx="166" cy="457" rx="3.5" ry="2.2" fill="#FED7AA" opacity="0.7" />
      <ellipse cx="190" cy="453" rx="4.5" ry="2.5" fill="#FED7AA" opacity="0.8" />
      <ellipse cx="214" cy="457" rx="3.5" ry="2.2" fill="#FED7AA" opacity="0.7" />
    </g>

    <!-- RIGHT FOOT (Centered under right eye at x=322, y=462) -->
    <g id="foot_right">
      <!-- Toe 1 (Inner left) -->
      <path d="M 298 450 C 292 450, 286 456, 286 463 C 286 470, 293 475, 300 474 C 307 473, 310 467, 310 459 C 310 453, 305 450, 298 450 Z"
            fill="url(#toeGrad)" stroke="#6C2A0C" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />
      <!-- Toe 3 (Outer right) -->
      <path d="M 346 450 C 339 450, 334 453, 334 459 C 334 467, 337 473, 344 474 C 351 475, 358 470, 358 463 C 358 456, 352 450, 346 450 Z"
            fill="url(#toeGrad)" stroke="#6C2A0C" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />
      <!-- Toe 2 (Middle, slightly larger and proud) -->
      <path d="M 322 446 C 314 446, 308 452, 308 461 C 308 470, 315 476, 322 476 C 329 476, 336 470, 336 461 C 336 452, 330 446, 322 446 Z"
            fill="url(#toeGrad)" stroke="#6C2A0C" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />
      <!-- Toe highlights -->
      <ellipse cx="298" cy="457" rx="3.5" ry="2.2" fill="#FED7AA" opacity="0.7" />
      <ellipse cx="322" cy="453" rx="4.5" ry="2.5" fill="#FED7AA" opacity="0.8" />
      <ellipse cx="346" cy="457" rx="3.5" ry="2.2" fill="#FED7AA" opacity="0.7" />
    </g>
  </g>

  <!-- 03. MAIN BODY & INTEGRATED WINGS (Continuous Chubby Owl Silhouette) -->
  <!-- Hand-drawn smooth cubic silhouette: rounded crown, cheeks, flanks, and belly -->
  <g id="body_main_group">
    <!-- The outer contour of Owluko: includes the folded wings on the sides! -->
    <path id="body_outer_silhouette"
          d="M 256 56
             C 320 56, 386 86, 404 150
             C 416 192, 422 240, 424 290
             C 426 348, 412 400, 372 432
             C 340 458, 298 464, 256 464
             C 214 464, 172 458, 140 432
             C 100 400, 86 348, 88 290
             C 90 240, 96 192, 108 150
             C 126 86, 192 56, 256 56 Z"
          fill="url(#bodyBaseGrad)"
          stroke="#4A3425"
          stroke-width="3.5"
          stroke-linecap="round"
          stroke-linejoin="round" />

    <!-- INTEGRATED LEFT WING FOLD (Delineates the folded wing resting against the body) -->
    <!-- Soft shadow behind wing fold -->
    <path d="M 124 220
             C 106 260, 102 320, 114 374
             C 120 400, 134 420, 148 430
             C 142 422, 130 400, 126 370
             C 118 318, 122 262, 136 226 Z"
          fill="#C8B39B" opacity="0.6" />
    <!-- Wing fold character contour stroke -->
    <path id="wing_left_fold"
          d="M 128 215
             C 108 260, 104 324, 116 376
             C 122 404, 136 424, 150 432"
          fill="none"
          stroke="#5C4231"
          stroke-width="3.0"
          stroke-linecap="round"
          stroke-linejoin="round" />

    <!-- INTEGRATED RIGHT WING FOLD (Mirrored) -->
    <!-- Soft shadow behind wing fold -->
    <path d="M 388 220
             C 406 260, 410 320, 398 374
             C 392 400, 378 420, 364 430
             C 370 422, 382 400, 386 370
             C 394 318, 390 262, 376 226 Z"
          fill="#C8B39B" opacity="0.6" />
    <!-- Wing fold character contour stroke -->
    <path id="wing_right_fold"
          d="M 384 215
             C 404 260, 408 324, 396 376
             C 390 404, 376 424, 362 432"
          fill="none"
          stroke="#5C4231"
          stroke-width="3.0"
          stroke-linecap="round"
          stroke-linejoin="round" />

    <!-- CHUBBY BELLY DOWN PATCH (Soft, lighter creamy down nestled between wings) -->
    <path id="belly_down"
          d="M 172 260
             C 214 250, 298 250, 340 260
             C 372 300, 376 360, 356 405
             C 334 445, 298 456, 256 456
             C 214 456, 178 445, 156 405
             C 136 360, 140 300, 172 260 Z"
          fill="url(#bellyGrad)"
          stroke="#E5D6C1"
          stroke-width="1.5"
          opacity="0.95" />

    <!-- Subtle Down Feather Fluff Accents on Belly -->
    <path d="M 238 340 Q 256 348 274 340" fill="none" stroke="#D8C5AE" stroke-width="2.0" stroke-linecap="round" opacity="0.6" />
    <path d="M 226 372 Q 256 382 286 372" fill="none" stroke="#D8C5AE" stroke-width="2.0" stroke-linecap="round" opacity="0.6" />
    <path d="M 242 404 Q 256 412 270 404" fill="none" stroke="#D8C5AE" stroke-width="2.0" stroke-linecap="round" opacity="0.6" />
  </g>

  <!-- 04. FACIAL DISK (Heart-shaped Barn Owl Spectacles) -->
  <g id="facial_disk_group">
    <!-- Soft shadow cast beneath the facial disk -->
    <path d="M 256 142
             C 236 100, 174 94, 142 126
             C 112 156, 116 210, 138 252
             C 162 296, 218 316, 256 316
             C 294 316, 350 296, 374 252
             C 396 210, 400 156, 370 126
             C 338 94, 276 100, 256 142 Z"
          fill="#C4AE95" opacity="0.4" transform="translate(0, 4)" />

    <!-- Main Heart-Shaped Spectacles Mask -->
    <path id="facial_disk_main"
          d="M 256 140
             C 236 96, 174 90, 142 122
             C 112 152, 116 206, 138 248
             C 162 292, 218 312, 256 312
             C 294 312, 350 292, 374 248
             C 396 206, 400 152, 370 122
             C 338 90, 276 96, 256 140 Z"
          fill="url(#facialDiskGrad)"
          stroke="#4A3425"
          stroke-width="3.2"
          stroke-linecap="round"
          stroke-linejoin="round" />

    <!-- Inner Soft Feather Rim -->
    <path d="M 256 146
             C 238 106, 182 102, 152 130
             C 126 156, 128 202, 148 240
             C 170 280, 220 298, 256 298
             C 292 298, 342 280, 364 240
             C 384 202, 386 156, 360 130
             C 330 102, 274 106, 256 146 Z"
          fill="none"
          stroke="#F3E7D5"
          stroke-width="2.0" />

    <!-- Soft Cheek Blush (Adds endearing life & warmth) -->
    <ellipse cx="152" cy="226" rx="22" ry="14" fill="url(#blushGrad)" />
    <ellipse cx="360" cy="226" rx="22" ry="14" fill="url(#blushGrad)" />
  </g>

  <!-- 05. EYES (Glassy Amber Orbs with Eyelids and Specular Highlights) -->
  <g id="eyes_group">
    <!-- LEFT EYE (Centered at x=190, y=175) -->
    <g id="eye_left">
      <!-- Outer dark eyeliner socket -->
      <circle cx="190" cy="175" r="41" fill="#1C1008" stroke="#4A3425" stroke-width="2.5" />
      <!-- Radiant amber iris -->
      <circle cx="190" cy="175" r="39" fill="url(#eyeAmberGradL)" />
      <!-- Inner dark pupil -->
      <circle cx="190" cy="175" r="26" fill="#0D0603" />
      <!-- Bottom golden reflex crescent -->
      <path d="M 168 184 C 174 198, 206 198, 212 184 C 206 192, 174 192, 168 184 Z" fill="#FDE047" opacity="0.65" />
      <!-- Primary glassy specular glint (10 o'clock) -->
      <circle cx="178" cy="163" r="8.5" fill="#FFFFFF" />
      <!-- Secondary micro catchlight (4 o'clock) -->
      <circle cx="202" cy="186" r="3.2" fill="#FFFFFF" opacity="0.85" />
      <!-- Eyelid crease arc above eye -->
      <path d="M 156 154 C 172 136, 208 136, 224 154" fill="none" stroke="#3D2719" stroke-width="3.0" stroke-linecap="round" />
    </g>

    <!-- RIGHT EYE (Centered at x=322, y=175) -->
    <g id="eye_right">
      <!-- Outer dark eyeliner socket -->
      <circle cx="322" cy="175" r="41" fill="#1C1008" stroke="#4A3425" stroke-width="2.5" />
      <!-- Radiant amber iris -->
      <circle cx="322" cy="175" r="39" fill="url(#eyeAmberGradR)" />
      <!-- Inner dark pupil -->
      <circle cx="322" cy="175" r="26" fill="#0D0603" />
      <!-- Bottom golden reflex crescent -->
      <path d="M 300 184 C 306 198, 338 198, 344 184 C 338 192, 306 192, 300 184 Z" fill="#FDE047" opacity="0.65" />
      <!-- Primary glassy specular glint (10 o'clock) -->
      <circle cx="310" cy="163" r="8.5" fill="#FFFFFF" />
      <!-- Secondary micro catchlight (4 o'clock) -->
      <circle cx="334" cy="186" r="3.2" fill="#FFFFFF" opacity="0.85" />
      <!-- Eyelid crease arc above eye -->
      <path d="M 288 154 C 304 136, 340 136, 356 154" fill="none" stroke="#3D2719" stroke-width="3.0" stroke-linecap="round" />
    </g>
  </g>

  <!-- 06. BEAK (Cute Rounded Terracotta Heart Cone nestled between eyes) -->
  <g id="beak_group">
    <!-- Beak shadow cast on chin -->
    <path d="M 242 222 L 256 244 L 270 222 Z" fill="#4A3425" opacity="0.3" transform="translate(0, 3)" />
    <!-- Main beak cone -->
    <path id="beak_main"
          d="M 256 194
             C 264 194, 272 198, 272 208
             C 272 218, 262 232, 256 240
             C 250 232, 240 218, 240 208
             C 240 198, 248 194, 256 194 Z"
          fill="url(#beakGrad)"
          stroke="#6C2A0C"
          stroke-width="2.6"
          stroke-linecap="round"
          stroke-linejoin="round" />
    <!-- Beak top highlight -->
    <ellipse cx="256" cy="202" rx="6" ry="3.5" fill="#FED7AA" opacity="0.75" />
    <!-- Beak center ridge -->
    <path d="M 256 206 L 256 232" stroke="#FED7AA" stroke-width="1.5" stroke-linecap="round" opacity="0.5" />
  </g>
</svg>'''

    with open(filepath, 'w') as f:
        f.write(svg)
    print(f"Generated hand-drawn Owluko master SVG at {filepath}")

if __name__ == "__main__":
    generate_handdrawn_owluko_svg("scratch/owluko_handdrawn_master.svg")
