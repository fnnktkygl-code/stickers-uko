import math

def generate_owluko_calibrated_v3(filepath):
    """
    Generate master v3 vector illustration for Owluko:
    - 100% faithful to the baby barn owl reference (owluko_fluffy_view_1.png).
    - True chubby spherical body: unbroken, seamless convex curves (NO shoulder notch!).
    - HUGE, soulful, wide-open glassy amber orb eyes (radius 46px, alert & endearing).
    - Broad, soft barn owl heart facial disk framing the eyes.
    - Cute rounded pumpkin beak nestled snugly between the eyes.
    - Wings as an organic, integral part of the body (smooth lateral flanks with soft fold creases).
    - Plump 3-bean toes clustered snugly under the belly down.
    - Hand-drawn illustrated styling with warm character linework and soft volumetric cel-shading.
    """

    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <!-- Soft Ground Shadows -->
    <radialGradient id="groundShadowDiffuse" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#2D1B0F" stop-opacity="0.30" />
      <stop offset="55%" stop-color="#2D1B0F" stop-opacity="0.10" />
      <stop offset="100%" stop-color="#2D1B0F" stop-opacity="0" />
    </radialGradient>
    <radialGradient id="groundShadowContact" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#1A0D06" stop-opacity="0.50" />
      <stop offset="70%" stop-color="#1A0D06" stop-opacity="0.15" />
      <stop offset="100%" stop-color="#1A0D06" stop-opacity="0" />
    </radialGradient>

    <!-- Master Chubby Body Warm Down Gradient -->
    <radialGradient id="bodyFluffGrad" cx="46%" cy="34%" r="62%">
      <stop offset="0%" stop-color="#FFFDF8" />
      <stop offset="40%" stop-color="#F8EFE3" />
      <stop offset="70%" stop-color="#EBDBC8" />
      <stop offset="88%" stop-color="#DEC9B2" />
      <stop offset="100%" stop-color="#CBB199" />
    </radialGradient>

    <!-- Belly Plush Down Gradient -->
    <radialGradient id="bellyPlushGrad" cx="50%" cy="40%" r="55%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="58%" stop-color="#FAF5ED" />
      <stop offset="85%" stop-color="#EFE3D3" />
      <stop offset="100%" stop-color="#DFCCB5" />
    </radialGradient>

    <!-- Facial Disk Soft Heart Gradient -->
    <radialGradient id="facialDiskGrad" cx="50%" cy="46%" r="55%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="60%" stop-color="#FAF6EE" />
      <stop offset="85%" stop-color="#EFE6D7" />
      <stop offset="100%" stop-color="#DFCFB9" />
    </radialGradient>

    <!-- Glassy Amber Eye Radial Gradients (Rich, radiant, soulful) -->
    <radialGradient id="amberEyeL" cx="35%" cy="32%" r="68%">
      <stop offset="0%" stop-color="#FEF08A" />
      <stop offset="18%" stop-color="#FBBF24" />
      <stop offset="42%" stop-color="#F59E0B" />
      <stop offset="70%" stop-color="#D97706" />
      <stop offset="88%" stop-color="#92400E" />
      <stop offset="100%" stop-color="#451A03" />
    </radialGradient>
    <radialGradient id="amberEyeR" cx="35%" cy="32%" r="68%">
      <stop offset="0%" stop-color="#FEF08A" />
      <stop offset="18%" stop-color="#FBBF24" />
      <stop offset="42%" stop-color="#F59E0B" />
      <stop offset="70%" stop-color="#D97706" />
      <stop offset="88%" stop-color="#92400E" />
      <stop offset="100%" stop-color="#451A03" />
    </radialGradient>

    <!-- Beak Terracotta Gradient -->
    <linearGradient id="beakGrad" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#FDBA74" />
      <stop offset="35%" stop-color="#F97316" />
      <stop offset="75%" stop-color="#EA580C" />
      <stop offset="100%" stop-color="#9A3412" />
    </linearGradient>

    <!-- Bean Toes Warm Terracotta Gradient -->
    <linearGradient id="toeGrad" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#FDBA74" />
      <stop offset="35%" stop-color="#F97316" />
      <stop offset="75%" stop-color="#EA580C" />
      <stop offset="100%" stop-color="#9A3412" />
    </linearGradient>

    <!-- Soft Cheek Blush Radial -->
    <radialGradient id="blushGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#F87171" stop-opacity="0.24" />
      <stop offset="60%" stop-color="#F87171" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#F87171" stop-opacity="0" />
    </radialGradient>
  </defs>

  <!-- 01. GROUND SHADOW -->
  <g id="ground_shadow_layer">
    <ellipse cx="256" cy="470" rx="172" ry="24" fill="url(#groundShadowDiffuse)" />
    <ellipse cx="256" cy="468" rx="122" ry="13" fill="url(#groundShadowContact)" />
  </g>

  <!-- 02. PLUMP 3-BEAN TOES (Under the belly down, firmly grounded) -->
  <g id="feet_layer">
    <!-- LEFT FOOT (Centered at X=182, Y=462 under left eye) -->
    <g id="foot_l">
      <!-- Outer Toe 1 -->
      <path d="M 158 448 C 150 448, 142 455, 142 464 C 142 472, 150 478, 159 477 C 168 476, 171 469, 171 460 C 171 452, 166 448, 158 448 Z"
            fill="url(#toeGrad)" stroke="#5B2308" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />
      <ellipse cx="158" cy="457" rx="3.8" ry="2.2" fill="#FED7AA" opacity="0.8" />

      <!-- Inner Toe 3 -->
      <path d="M 206 448 C 198 448, 193 452, 193 460 C 193 469, 196 476, 205 477 C 214 478, 222 472, 222 464 C 222 455, 214 448, 206 448 Z"
            fill="url(#toeGrad)" stroke="#5B2308" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />
      <ellipse cx="206" cy="457" rx="3.8" ry="2.2" fill="#FED7AA" opacity="0.8" />

      <!-- Middle Toe 2 (Slightly larger, proud) -->
      <path d="M 182 444 C 171 444, 165 452, 165 462 C 165 473, 173 480, 182 480 C 191 480, 199 473, 199 462 C 199 452, 193 444, 182 444 Z"
            fill="url(#toeGrad)" stroke="#5B2308" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />
      <ellipse cx="182" cy="453" rx="4.8" ry="2.8" fill="#FED7AA" opacity="0.9" />
    </g>

    <!-- RIGHT FOOT (Centered at X=330, Y=462 under right eye) -->
    <g id="foot_r">
      <!-- Inner Toe 1 -->
      <path d="M 306 448 C 298 448, 290 455, 290 464 C 290 472, 298 478, 307 477 C 316 476, 319 469, 319 460 C 319 452, 314 448, 306 448 Z"
            fill="url(#toeGrad)" stroke="#5B2308" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />
      <ellipse cx="306" cy="457" rx="3.8" ry="2.2" fill="#FED7AA" opacity="0.8" />

      <!-- Outer Toe 3 -->
      <path d="M 354 448 C 346 448, 341 452, 341 460 C 341 469, 344 476, 353 477 C 362 478, 370 472, 370 464 C 370 455, 362 448, 354 448 Z"
            fill="url(#toeGrad)" stroke="#5B2308" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />
      <ellipse cx="354" cy="457" rx="3.8" ry="2.2" fill="#FED7AA" opacity="0.8" />

      <!-- Middle Toe 2 (Slightly larger, proud) -->
      <path d="M 330 444 C 319 444, 313 452, 313 462 C 313 473, 321 480, 330 480 C 339 480, 347 473, 347 462 C 347 452, 341 444, 330 444 Z"
            fill="url(#toeGrad)" stroke="#5B2308" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />
      <ellipse cx="330" cy="453" rx="4.8" ry="2.8" fill="#FED7AA" opacity="0.9" />
    </g>
  </g>

  <!-- 03. CHUBBY SPHERICAL BODY & INTEGRATED WINGS (UNBROKEN CONTINUOUS SILHOUETTE) -->
  <g id="body_layer">
    <!-- Continuous, plush baby owl sphere:
         Crown at Y=44, Cheek & Flank swell reaching X=40 and X=472 at Y=280..320,
         Belly curving down to Y=460 overhanging the feet.
         Unbroken, seamless, organic curves!
    -->
    <path id="body_main_silhouette"
          d="M 256 44
             C 320 44, 382 68, 424 122
             C 456 164, 468 220, 468 280
             C 468 340, 452 396, 408 432
             C 368 464, 314 460, 256 460
             C 198 460, 144 464, 104 432
             C 60 396, 44 340, 44 280
             C 44 220, 56 164, 88 122
             C 130 68, 192 44, 256 44 Z"
          fill="url(#bodyFluffGrad)"
          stroke="#422E20"
          stroke-width="3.5"
          stroke-linecap="round"
          stroke-linejoin="round" />

    <!-- INTEGRATED LEFT WING FOLD (Natural fold resting against flank, NOT an appendage!) -->
    <!-- Ambient occlusion behind wing crease -->
    <path d="M 86 215
             C 70 250, 68 295, 78 332
             C 88 362, 108 382, 126 390
             C 118 382, 104 362, 98 336
             C 90 298, 94 256, 106 220 Z"
          fill="#C4AE96" opacity="0.5" />
    <!-- Wing fold character line -->
    <path id="wing_l_crease_line"
          d="M 92 210
             C 76 250, 74 298, 82 336
             C 90 366, 110 386, 128 392"
          fill="none"
          stroke="#4D3525"
          stroke-width="3.0"
          stroke-linecap="round"
          stroke-linejoin="round" />
    <!-- Down feather tick -->
    <path d="M 68 305 C 76 314, 88 320, 102 316" fill="none" stroke="#D2BEA6" stroke-width="2.0" stroke-linecap="round" />

    <!-- INTEGRATED RIGHT WING FOLD (Mirrored) -->
    <!-- Ambient occlusion behind wing crease -->
    <path d="M 426 215
             C 442 250, 444 295, 434 332
             C 424 362, 404 382, 386 390
             C 394 382, 408 362, 414 336
             C 422 298, 418 256, 406 220 Z"
          fill="#C4AE96" opacity="0.5" />
    <!-- Wing fold character line -->
    <path id="wing_r_crease_line"
          d="M 420 210
             C 436 250, 438 298, 430 336
             C 422 366, 402 386, 384 392"
          fill="none"
          stroke="#4D3525"
          stroke-width="3.0"
          stroke-linecap="round"
          stroke-linejoin="round" />
    <!-- Down feather tick -->
    <path d="M 444 305 C 436 314, 424 320, 410 316" fill="none" stroke="#D2BEA6" stroke-width="2.0" stroke-linecap="round" />

    <!-- PLUSH BELLY DOWN PATCH (Luminous warm white/cream down nestled between wings) -->
    <path id="belly_plush_patch"
          d="M 136 240
             C 180 228, 332 228, 376 240
             C 414 282, 418 348, 394 396
             C 364 444, 314 455, 256 455
             C 198 455, 148 444, 118 396
             C 94 348, 98 282, 136 240 Z"
          fill="url(#bellyPlushGrad)"
          stroke="#E5D7C4"
          stroke-width="1.8"
          opacity="0.96" />

    <!-- Soft Down Tuft Accents on Belly -->
    <path d="M 230 320 Q 256 332 282 320" fill="none" stroke="#D5C1A9" stroke-width="2.2" stroke-linecap="round" opacity="0.55" />
    <path d="M 214 358 Q 256 372 298 358" fill="none" stroke="#D5C1A9" stroke-width="2.2" stroke-linecap="round" opacity="0.55" />
    <path d="M 234 396 Q 256 408 278 396" fill="none" stroke="#D5C1A9" stroke-width="2.2" stroke-linecap="round" opacity="0.55" />
  </g>

  <!-- 04. FACIAL DISK (Broad, Soft Barn Owl Heart Spectacles) -->
  <g id="facial_disk_layer">
    <!-- Ambient Occlusion Shadow under Facial Disk -->
    <path d="M 256 122
             C 234 76, 160 70, 122 104
             C 86 136, 84 196, 110 242
             C 142 292, 210 308, 256 308
             C 302 308, 370 292, 402 242
             C 428 196, 426 136, 390 104
             C 352 70, 278 76, 256 122 Z"
          fill="#C4AE96" opacity="0.38" transform="translate(0, 5)" />

    <!-- Main Heart-Shaped Barn Owl Facial Disk -->
    <path id="facial_disk_main"
          d="M 256 120
             C 234 72, 160 66, 122 100
             C 86 132, 84 192, 110 238
             C 142 288, 210 304, 256 304
             C 302 304, 370 288, 402 238
             C 428 192, 426 132, 390 100
             C 352 66, 278 72, 256 120 Z"
          fill="url(#facialDiskGrad)"
          stroke="#422E20"
          stroke-width="3.2"
          stroke-linecap="round"
          stroke-linejoin="round" />

    <!-- Inner Soft Feather Rim -->
    <path d="M 256 126
             C 236 82, 168 78, 134 108
             C 102 136, 100 186, 124 228
             C 152 272, 214 288, 256 288
             C 298 288, 360 272, 388 228
             C 412 186, 410 136, 378 108
             C 344 78, 276 82, 256 126 Z"
          fill="none"
          stroke="#F4E8D7"
          stroke-width="2.2" />

    <!-- Sweet Cheek Blush -->
    <ellipse cx="138" cy="218" rx="26" ry="16" fill="url(#blushGrad)" />
    <ellipse cx="374" cy="218" rx="26" ry="16" fill="url(#blushGrad)" />
  </g>

  <!-- 05. EYES (HUGE, GLORIOUS, ALERT GLASSY AMBER ORBS) -->
  <g id="eyes_layer">
    <!-- LEFT EYE (Centered at X=182, Y=165, Radius=46px) -->
    <g id="eye_left_orb">
      <!-- Dark Eyeliner Rim -->
      <circle cx="182" cy="165" r="48" fill="#1A0D06" stroke="#422E20" stroke-width="3.0" />
      <!-- Radiant Amber Iris -->
      <circle cx="182" cy="165" r="45" fill="url(#amberEyeL)" />
      <!-- Deep Obsidian Pupil (Large, round, innocent) -->
      <circle cx="182" cy="165" r="30" fill="#0A0502" />
      <!-- Bottom Amber-Gold Reflex Arc -->
      <path d="M 154 175 C 162 195, 202 195, 210 175 C 202 186, 162 186, 154 175 Z" fill="#FEF08A" opacity="0.65" />
      <!-- Primary Glassy Specular Catchlight (10:30 o'clock - Large & Brilliant) -->
      <circle cx="169" cy="151" r="10.5" fill="#FFFFFF" />
      <!-- Secondary Micro Catchlight (4:30 o'clock) -->
      <circle cx="197" cy="179" r="4.2" fill="#FFFFFF" opacity="0.9" />
      <!-- Subtle Eyelid Crease Arc (Above the eye) -->
      <path d="M 142 138 C 160 118, 204 118, 222 138" fill="none" stroke="#382214" stroke-width="3.2" stroke-linecap="round" />
    </g>

    <!-- RIGHT EYE (Centered at X=330, Y=165, Radius=46px) -->
    <g id="eye_right_orb">
      <!-- Dark Eyeliner Rim -->
      <circle cx="330" cy="165" r="48" fill="#1A0D06" stroke="#422E20" stroke-width="3.0" />
      <!-- Radiant Amber Iris -->
      <circle cx="330" cy="165" r="45" fill="url(#amberEyeR)" />
      <!-- Deep Obsidian Pupil (Large, round, innocent) -->
      <circle cx="330" cy="165" r="30" fill="#0A0502" />
      <!-- Bottom Amber-Gold Reflex Arc -->
      <path d="M 302 175 C 310 195, 350 195, 358 175 C 350 186, 310 186, 302 175 Z" fill="#FEF08A" opacity="0.65" />
      <!-- Primary Glassy Specular Catchlight (10:30 o'clock - Large & Brilliant) -->
      <circle cx="317" cy="151" r="10.5" fill="#FFFFFF" />
      <!-- Secondary Micro Catchlight (4:30 o'clock) -->
      <circle cx="345" cy="179" r="4.2" fill="#FFFFFF" opacity="0.9" />
      <!-- Subtle Eyelid Crease Arc (Above the eye) -->
      <path d="M 290 138 C 308 118, 352 118, 370 138" fill="none" stroke="#382214" stroke-width="3.2" stroke-linecap="round" />
    </g>
  </g>

  <!-- 06. BEAK (Snug Rounded Terracotta Heart Cone nestled between eyes) -->
  <g id="beak_layer">
    <!-- Drop Shadow -->
    <path d="M 242 210 L 256 238 L 270 210 Z" fill="#3D2719" opacity="0.32" transform="translate(0, 3)" />
    <!-- Beak Main Body -->
    <path id="beak_cone"
          d="M 256 188
             C 267 188, 275 193, 275 205
             C 275 217, 264 231, 256 239
             C 248 231, 237 217, 237 205
             C 237 193, 245 188, 256 188 Z"
          fill="url(#beakGrad)"
          stroke="#5B2308"
          stroke-width="2.6"
          stroke-linecap="round"
          stroke-linejoin="round" />
    <!-- Glossy Highlight -->
    <ellipse cx="256" cy="196" rx="7.0" ry="4.0" fill="#FED7AA" opacity="0.85" />
    <!-- Center Beak Seam -->
    <path d="M 256 200 L 256 230" stroke="#FED7AA" stroke-width="1.6" stroke-linecap="round" opacity="0.55" />
  </g>
</svg>'''

    with open(filepath, 'w') as f:
        f.write(svg)
    print(f"Written calibrated master SVG v3 to {filepath}")

if __name__ == "__main__":
    generate_owluko_calibrated_v3("scratch/owluko_calibrated_v3.svg")
