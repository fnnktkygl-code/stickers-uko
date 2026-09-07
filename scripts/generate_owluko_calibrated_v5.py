import math

def generate_owluko_calibrated_v5(filepath):
    """
    Generate calibrated v5 master vector illustration for Owluko:
    - 100% faithful to fluffy baby barn owl reference (owluko_fluffy_view_1.png).
    - Perfect chubby spherical ball silhouette with rounded bowl belly.
    - Pure circular, innocent, alert glassy amber eyes (pure black pupil + brilliant white catchlight).
    - Broad, gentle barn owl facial disk with subtle brow dip.
    - Organic folded flank wings that end at Y~340, letting the plump round belly curve out below them.
    - Plump 3-bean toes clustered snugly under the rounded belly.
    - Illustrated character styling matching high-end Rive mascots.
    """

    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <!-- Soft Ground Shadows -->
    <radialGradient id="groundShadowDiffuse" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#2D1B0F" stop-opacity="0.32" />
      <stop offset="60%" stop-color="#2D1B0F" stop-opacity="0.10" />
      <stop offset="100%" stop-color="#2D1B0F" stop-opacity="0" />
    </radialGradient>
    <radialGradient id="groundShadowContact" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#1A0D06" stop-opacity="0.55" />
      <stop offset="70%" stop-color="#1A0D06" stop-opacity="0.18" />
      <stop offset="100%" stop-color="#1A0D06" stop-opacity="0" />
    </radialGradient>

    <!-- Master Chubby Body Warm Down Gradient -->
    <radialGradient id="bodyFluffGrad" cx="46%" cy="32%" r="64%">
      <stop offset="0%" stop-color="#FFFDF8" />
      <stop offset="38%" stop-color="#F8EFE3" />
      <stop offset="68%" stop-color="#EBDCC9" />
      <stop offset="86%" stop-color="#DECBBA" />
      <stop offset="100%" stop-color="#CBB39D" />
    </radialGradient>

    <!-- Belly Plush Down Gradient -->
    <radialGradient id="bellyPlushGrad" cx="50%" cy="38%" r="55%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="56%" stop-color="#FAF5ED" />
      <stop offset="84%" stop-color="#EFE3D3" />
      <stop offset="100%" stop-color="#DFCCB5" />
    </radialGradient>

    <!-- Facial Disk Soft Heart Gradient -->
    <radialGradient id="facialDiskGrad" cx="50%" cy="44%" r="55%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="58%" stop-color="#FAF6EE" />
      <stop offset="84%" stop-color="#EFE6D7" />
      <stop offset="100%" stop-color="#DFCFB9" />
    </radialGradient>

    <!-- Glassy Amber Eye Radial Gradients (Rich, radiant, soulful) -->
    <radialGradient id="amberEyeL" cx="34%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#FEF08A" />
      <stop offset="16%" stop-color="#FBBF24" />
      <stop offset="38%" stop-color="#F59E0B" />
      <stop offset="68%" stop-color="#D97706" />
      <stop offset="86%" stop-color="#92400E" />
      <stop offset="100%" stop-color="#451A03" />
    </radialGradient>
    <radialGradient id="amberEyeR" cx="34%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#FEF08A" />
      <stop offset="16%" stop-color="#FBBF24" />
      <stop offset="38%" stop-color="#F59E0B" />
      <stop offset="68%" stop-color="#D97706" />
      <stop offset="86%" stop-color="#92400E" />
      <stop offset="100%" stop-color="#451A03" />
    </radialGradient>

    <!-- Beak Terracotta Gradient -->
    <linearGradient id="beakGrad" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#FDBA74" />
      <stop offset="32%" stop-color="#F97316" />
      <stop offset="72%" stop-color="#EA580C" />
      <stop offset="100%" stop-color="#9A3412" />
    </linearGradient>

    <!-- Bean Toes Warm Terracotta Gradient -->
    <linearGradient id="toeGrad" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#FDBA74" />
      <stop offset="32%" stop-color="#F97316" />
      <stop offset="72%" stop-color="#EA580C" />
      <stop offset="100%" stop-color="#9A3412" />
    </linearGradient>

    <!-- Soft Cheek Blush Radial -->
    <radialGradient id="blushGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#F87171" stop-opacity="0.22" />
      <stop offset="60%" stop-color="#F87171" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#F87171" stop-opacity="0" />
    </radialGradient>
  </defs>

  <!-- 01. GROUND SHADOW -->
  <g id="ground_shadow_layer">
    <ellipse cx="256" cy="472" rx="174" ry="24" fill="url(#groundShadowDiffuse)" />
    <ellipse cx="256" cy="470" rx="124" ry="13" fill="url(#groundShadowContact)" />
  </g>

  <!-- 02. PLUMP 3-BEAN TOES (Under the belly down, firmly grounded) -->
  <g id="feet_layer">
    <!-- LEFT FOOT (Centered at X=182, Y=464 under left eye) -->
    <g id="foot_l">
      <!-- Outer Toe 1 -->
      <path d="M 158 450 C 150 450, 142 457, 142 466 C 142 474, 150 480, 159 479 C 168 478, 171 471, 171 462 C 171 454, 166 450, 158 450 Z"
            fill="url(#toeGrad)" stroke="#5B2308" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />
      <ellipse cx="158" cy="459" rx="3.8" ry="2.2" fill="#FED7AA" opacity="0.85" />

      <!-- Inner Toe 3 -->
      <path d="M 206 450 C 198 450, 193 454, 193 462 C 193 471, 196 478, 205 479 C 214 480, 222 474, 222 466 C 222 457, 214 450, 206 450 Z"
            fill="url(#toeGrad)" stroke="#5B2308" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />
      <ellipse cx="206" cy="459" rx="3.8" ry="2.2" fill="#FED7AA" opacity="0.85" />

      <!-- Middle Toe 2 (Slightly larger, proud) -->
      <path d="M 182 446 C 171 446, 165 454, 165 464 C 165 475, 173 482, 182 482 C 191 482, 199 475, 199 464 C 199 454, 193 446, 182 446 Z"
            fill="url(#toeGrad)" stroke="#5B2308" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />
      <ellipse cx="182" cy="455" rx="4.8" ry="2.8" fill="#FED7AA" opacity="0.9" />
    </g>

    <!-- RIGHT FOOT (Centered at X=330, Y=464 under right eye) -->
    <g id="foot_r">
      <!-- Inner Toe 1 -->
      <path d="M 306 450 C 298 450, 290 457, 290 466 C 290 474, 298 480, 307 479 C 316 478, 319 471, 319 462 C 319 454, 314 450, 306 450 Z"
            fill="url(#toeGrad)" stroke="#5B2308" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />
      <ellipse cx="306" cy="459" rx="3.8" ry="2.2" fill="#FED7AA" opacity="0.85" />

      <!-- Outer Toe 3 -->
      <path d="M 354 450 C 346 450, 341 454, 341 462 C 341 471, 344 478, 353 479 C 362 480, 370 474, 370 466 C 370 457, 362 450, 354 450 Z"
            fill="url(#toeGrad)" stroke="#5B2308" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />
      <ellipse cx="354" cy="459" rx="3.8" ry="2.2" fill="#FED7AA" opacity="0.85" />

      <!-- Middle Toe 2 (Slightly larger, proud) -->
      <path d="M 330 446 C 319 446, 313 454, 313 464 C 313 475, 321 482, 330 482 C 339 482, 347 475, 347 464 C 347 454, 341 446, 330 446 Z"
            fill="url(#toeGrad)" stroke="#5B2308" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />
      <ellipse cx="330" cy="455" rx="4.8" ry="2.8" fill="#FED7AA" opacity="0.9" />
    </g>
  </g>

  <!-- 03. CHUBBY SPHERICAL BODY & INTEGRATED WINGS (PERFECT SPHERICAL CONVEX DOUGH BALL) -->
  <g id="body_layer">
    <!-- True chubby sphere:
         Crown at Y=46, Cheeks & Wings swelling out to X=42 and X=470 at Y=260..290,
         Lower belly swelling out smoothly below the wings,
         Rounding into a plush convex bowl down to Y=464, resting right above the toes!
    -->
    <path id="body_main_silhouette"
          d="M 256 46
             C 334 46, 404 76, 440 134
             C 466 178, 474 230, 470 286
             C 466 338, 446 388, 404 424
             C 362 458, 310 464, 256 464
             C 202 464, 150 458, 108 424
             C 66 388, 46 338, 42 286
             C 38 230, 46 178, 72 134
             C 108 76, 178 46, 256 46 Z"
          fill="url(#bodyFluffGrad)"
          stroke="#3D271A"
          stroke-width="3.5"
          stroke-linecap="round"
          stroke-linejoin="round" />

    <!-- INTEGRATED LEFT WING FOLD (Natural resting flank fold ending at Y~340) -->
    <!-- Ambient shadow under wing crease -->
    <path d="M 86 195
             C 68 228, 66 268, 74 300
             C 82 324, 98 338, 114 344
             C 106 336, 96 320, 92 298
             C 86 268, 88 232, 100 200 Z"
          fill="#C4AE96" opacity="0.48" />
    <!-- Wing fold character line -->
    <path id="wing_l_crease_line"
          d="M 90 190
             C 72 228, 70 270, 78 304
             C 84 328, 100 342, 116 346"
          fill="none"
          stroke="#4A3425"
          stroke-width="3.0"
          stroke-linecap="round"
          stroke-linejoin="round" />
    <!-- Soft feather texture tick on wing -->
    <path d="M 64 274 C 72 282, 82 286, 94 282" fill="none" stroke="#D2BEA6" stroke-width="2.0" stroke-linecap="round" />

    <!-- INTEGRATED RIGHT WING FOLD (Mirrored) -->
    <!-- Ambient shadow under wing crease -->
    <path d="M 426 195
             C 444 228, 446 268, 438 300
             C 430 324, 414 338, 398 344
             C 406 336, 416 320, 420 298
             C 426 268, 424 232, 412 200 Z"
          fill="#C4AE96" opacity="0.48" />
    <!-- Wing fold character line -->
    <path id="wing_r_crease_line"
          d="M 422 190
             C 440 228, 442 270, 434 304
             C 428 328, 412 342, 396 346"
          fill="none"
          stroke="#4A3425"
          stroke-width="3.0"
          stroke-linecap="round"
          stroke-linejoin="round" />
    <!-- Soft feather texture tick on wing -->
    <path d="M 448 274 C 440 282, 430 286, 418 282" fill="none" stroke="#D2BEA6" stroke-width="2.0" stroke-linecap="round" />

    <!-- PLUSH BELLY DOWN PATCH (Luminous, rounded warm cream/white down) -->
    <path id="belly_plush_patch"
          d="M 132 230
             C 178 218, 334 218, 380 230
             C 422 275, 424 350, 396 398
             C 366 446, 316 456, 256 456
             C 196 456, 146 446, 116 398
             C 88 350, 90 275, 132 230 Z"
          fill="url(#bellyPlushGrad)"
          stroke="#E5D7C4"
          stroke-width="1.8"
          opacity="0.96" />

    <!-- Soft Down Tuft Accents on Belly -->
    <path d="M 230 320 Q 256 332 282 320" fill="none" stroke="#D5C1A9" stroke-width="2.2" stroke-linecap="round" opacity="0.55" />
    <path d="M 214 358 Q 256 372 298 358" fill="none" stroke="#D5C1A9" stroke-width="2.2" stroke-linecap="round" opacity="0.55" />
    <path d="M 234 396 Q 256 408 278 396" fill="none" stroke="#D5C1A9" stroke-width="2.2" stroke-linecap="round" opacity="0.55" />
  </g>

  <!-- 04. FACIAL DISK (Broad, Gentle Heart Spectacles with subtle brow dip) -->
  <g id="facial_disk_layer">
    <!-- Ambient Occlusion Shadow under Facial Disk -->
    <path d="M 256 128
             C 236 92, 160 84, 122 116
             C 82 148, 80 206, 108 252
             C 140 298, 210 314, 256 314
             C 302 314, 372 298, 404 252
             C 432 206, 430 148, 392 116
             C 352 84, 276 92, 256 128 Z"
          fill="#C4AE96" opacity="0.38" transform="translate(0, 5)" />

    <!-- Main Heart-Shaped Barn Owl Facial Disk -->
    <path id="facial_disk_main"
          d="M 256 126
             C 236 88, 160 80, 122 112
             C 82 144, 80 202, 108 248
             C 140 294, 210 310, 256 310
             C 302 310, 372 294, 404 248
             C 432 202, 430 144, 392 112
             C 352 80, 276 88, 256 126 Z"
          fill="url(#facialDiskGrad)"
          stroke="#3D271A"
          stroke-width="3.2"
          stroke-linecap="round"
          stroke-linejoin="round" />

    <!-- Inner Soft Feather Rim -->
    <path d="M 256 132
             C 238 96, 168 90, 134 120
             C 98 148, 96 198, 122 238
             C 150 280, 214 294, 256 294
             C 298 294, 362 280, 390 238
             C 416 198, 414 148, 378 120
             C 344 90, 274 96, 256 132 Z"
          fill="none"
          stroke="#F4E8D7"
          stroke-width="2.2" />

    <!-- Sweet Cheek Blush -->
    <ellipse cx="136" cy="222" rx="26" ry="16" fill="url(#blushGrad)" />
    <ellipse cx="376" cy="222" rx="26" ry="16" fill="url(#blushGrad)" />
  </g>

  <!-- 05. EYES (HUGE, ALERT, ADORABLE GLASSY AMBER ORBS - PURE SOLID OBSIDIAN PUPIL) -->
  <g id="eyes_layer">
    <!-- LEFT EYE (Centered at X=182, Y=165, Radius=46px) -->
    <g id="eye_left_orb">
      <!-- Dark Eyeliner Socket -->
      <circle cx="182" cy="165" r="48" fill="#1A0D06" stroke="#3D271A" stroke-width="3.0" />
      <!-- Radiant Amber Iris -->
      <circle cx="182" cy="165" r="45" fill="url(#amberEyeL)" />
      <!-- Bottom Golden Iris Rim Glow (BEFORE pupil!) -->
      <path d="M 148 178 C 158 204, 206 204, 216 178 C 208 196, 156 196, 148 178 Z" fill="#FEF08A" opacity="0.6" />
      <!-- Deep Obsidian Pupil (PURE, ROUND, SOLID BLACK ON TOP OF IRIS!) -->
      <circle cx="182" cy="165" r="28" fill="#0A0502" />
      <!-- Primary Glassy Specular Catchlight (10:30 o'clock - Large, round, bright white) -->
      <circle cx="168" cy="151" r="10.5" fill="#FFFFFF" />
      <!-- Secondary Micro Catchlight (4:30 o'clock) -->
      <circle cx="197" cy="179" r="4.2" fill="#FFFFFF" opacity="0.9" />
      <!-- Delicate Brow Fold Arc (Above eye on brow) -->
      <path d="M 144 134 C 162 116, 202 116, 220 134" fill="none" stroke="#382214" stroke-width="3.0" stroke-linecap="round" />
    </g>

    <!-- RIGHT EYE (Centered at X=330, Y=165, Radius=46px) -->
    <g id="eye_right_orb">
      <!-- Dark Eyeliner Socket -->
      <circle cx="330" cy="165" r="48" fill="#1A0D06" stroke="#3D271A" stroke-width="3.0" />
      <!-- Radiant Amber Iris -->
      <circle cx="330" cy="165" r="45" fill="url(#amberEyeR)" />
      <!-- Bottom Golden Iris Rim Glow (BEFORE pupil!) -->
      <path d="M 296 178 C 306 204, 354 204, 364 178 C 356 196, 304 196, 296 178 Z" fill="#FEF08A" opacity="0.6" />
      <!-- Deep Obsidian Pupil (PURE, ROUND, SOLID BLACK ON TOP OF IRIS!) -->
      <circle cx="330" cy="165" r="28" fill="#0A0502" />
      <!-- Primary Glassy Specular Catchlight (10:30 o'clock - Large, round, bright white) -->
      <circle cx="316" cy="151" r="10.5" fill="#FFFFFF" />
      <!-- Secondary Micro Catchlight (4:30 o'clock) -->
      <circle cx="345" cy="179" r="4.2" fill="#FFFFFF" opacity="0.9" />
      <!-- Delicate Brow Fold Arc (Above eye on brow) -->
      <path d="M 292 134 C 310 116, 350 116, 368 134" fill="none" stroke="#382214" stroke-width="3.0" stroke-linecap="round" />
    </g>
  </g>

  <!-- 06. BEAK (Snug, Plump Terracotta Heart Cone nestled between eyes) -->
  <g id="beak_layer">
    <!-- Drop Shadow on chin -->
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
    print(f"Written calibrated master SVG v5 to {filepath}")

if __name__ == "__main__":
    generate_owluko_calibrated_v5("scratch/owluko_calibrated_v5.svg")
