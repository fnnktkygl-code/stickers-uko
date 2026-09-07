import math

def generate_owluko_calibrated_v4(filepath):
    """
    Generate master v4 vector illustration for Owluko:
    - 100% faithful to fluffy baby barn owl reference (owluko_fluffy_view_1.png).
    - Chubby spherical body with puffy lower belly swelling under the folded flank wings.
    - Pure circular, wide-open, alert glassy amber eyes (NO cutting lines inside pupil!).
    - Soft, wide barn owl heart spectacles facial disk.
    - Plump, rounded 3-bean toes clustered under the belly down.
    - Hand-drawn illustrated styling matching the high-end Rive cloud mascot reference.
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

    <!-- Glassy Amber Eye Radial Gradients (Soulful, wide open, radiant depth) -->
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

  <!-- 03. CHUBBY SPHERICAL BODY & INTEGRATED WINGS (UNBROKEN CONTINUOUS SILHOUETTE) -->
  <g id="body_layer">
    <!-- Unbroken, wide, plush baby owl sphere:
         Crown at Y=46, Cheeks & Wings swelling out to X=42 and X=470 at Y=260..300,
         Lower belly swelling out below wings at Y=360..420,
         Rounding down to Y=462 gently resting right above the toes!
    -->
    <path id="body_main_silhouette"
          d="M 256 46
             C 328 46, 396 74, 434 130
             C 462 172, 472 226, 470 286
             C 468 344, 452 398, 410 435
             C 370 468, 314 464, 256 464
             C 198 464, 142 468, 102 435
             C 60 398, 44 344, 42 286
             C 40 226, 50 172, 78 130
             C 116 74, 184 46, 256 46 Z"
          fill="url(#bodyFluffGrad)"
          stroke="#3D271A"
          stroke-width="3.5"
          stroke-linecap="round"
          stroke-linejoin="round" />

    <!-- INTEGRATED LEFT WING FOLD (Natural resting flank fold) -->
    <!-- Soft ambient shadow along the wing fold -->
    <path d="M 82 205
             C 66 238, 64 278, 72 312
             C 80 340, 98 358, 116 364
             C 108 356, 96 338, 92 314
             C 86 280, 90 244, 100 210 Z"
          fill="#C4AE96" opacity="0.48" />
    <!-- Wing fold character line -->
    <path id="wing_l_crease_line"
          d="M 88 200
             C 72 238, 70 282, 78 316
             C 84 342, 102 360, 118 366"
          fill="none"
          stroke="#4A3425"
          stroke-width="3.0"
          stroke-linecap="round"
          stroke-linejoin="round" />
    <!-- Soft feather texture tick on wing -->
    <path d="M 64 286 C 72 294, 82 298, 94 294" fill="none" stroke="#D2BEA6" stroke-width="2.0" stroke-linecap="round" />

    <!-- INTEGRATED RIGHT WING FOLD (Mirrored) -->
    <!-- Soft ambient shadow along the wing fold -->
    <path d="M 430 205
             C 446 238, 448 278, 440 312
             C 432 340, 414 358, 396 364
             C 404 356, 416 338, 420 314
             C 426 280, 422 244, 412 210 Z"
          fill="#C4AE96" opacity="0.48" />
    <!-- Wing fold character line -->
    <path id="wing_r_crease_line"
          d="M 424 200
             C 440 238, 442 282, 434 316
             C 428 342, 410 360, 394 366"
          fill="none"
          stroke="#4A3425"
          stroke-width="3.0"
          stroke-linecap="round"
          stroke-linejoin="round" />
    <!-- Soft feather texture tick on wing -->
    <path d="M 448 286 C 440 294, 430 298, 418 294" fill="none" stroke="#D2BEA6" stroke-width="2.0" stroke-linecap="round" />

    <!-- PLUSH BELLY DOWN PATCH (Luminous, rounded warm cream/white down) -->
    <path id="belly_plush_patch"
          d="M 132 235
             C 178 222, 334 222, 380 235
             C 420 280, 424 352, 398 402
             C 368 450, 316 460, 256 460
             C 196 460, 144 450, 114 402
             C 88 352, 92 280, 132 235 Z"
          fill="url(#bellyPlushGrad)"
          stroke="#E5D7C4"
          stroke-width="1.8"
          opacity="0.96" />

    <!-- Soft Down Tuft Accents on Belly -->
    <path d="M 230 326 Q 256 338 282 326" fill="none" stroke="#D5C1A9" stroke-width="2.2" stroke-linecap="round" opacity="0.55" />
    <path d="M 214 364 Q 256 378 298 364" fill="none" stroke="#D5C1A9" stroke-width="2.2" stroke-linecap="round" opacity="0.55" />
    <path d="M 234 402 Q 256 414 278 402" fill="none" stroke="#D5C1A9" stroke-width="2.2" stroke-linecap="round" opacity="0.55" />
  </g>

  <!-- 04. FACIAL DISK (Broad, Gentle Heart Spectacles) -->
  <g id="facial_disk_layer">
    <!-- Ambient Occlusion Shadow under Facial Disk -->
    <path d="M 256 126
             C 234 82, 158 76, 120 110
             C 82 142, 80 204, 108 250
             C 140 298, 210 314, 256 314
             C 302 314, 372 298, 404 250
             C 432 204, 430 142, 392 110
             C 354 76, 278 82, 256 126 Z"
          fill="#C4AE96" opacity="0.38" transform="translate(0, 5)" />

    <!-- Main Heart-Shaped Barn Owl Facial Disk -->
    <path id="facial_disk_main"
          d="M 256 124
             C 234 78, 158 72, 120 106
             C 82 138, 80 200, 108 246
             C 140 294, 210 310, 256 310
             C 302 310, 372 294, 404 246
             C 432 200, 430 138, 392 106
             C 354 72, 278 78, 256 124 Z"
          fill="url(#facialDiskGrad)"
          stroke="#3D271A"
          stroke-width="3.2"
          stroke-linecap="round"
          stroke-linejoin="round" />

    <!-- Inner Soft Feather Rim -->
    <path d="M 256 130
             C 236 88, 166 84, 132 114
             C 98 142, 96 194, 122 236
             C 150 280, 214 294, 256 294
             C 298 294, 362 280, 390 236
             C 416 194, 414 142, 380 114
             C 346 84, 276 88, 256 130 Z"
          fill="none"
          stroke="#F4E8D7"
          stroke-width="2.2" />

    <!-- Sweet Cheek Blush -->
    <ellipse cx="136" cy="222" rx="26" ry="16" fill="url(#blushGrad)" />
    <ellipse cx="376" cy="222" rx="26" ry="16" fill="url(#blushGrad)" />
  </g>

  <!-- 05. EYES (HUGE, ALERT, ADORABLE GLASSY AMBER ORBS - NO Sleepy Creases!) -->
  <g id="eyes_layer">
    <!-- LEFT EYE (Centered at X=182, Y=165, Radius=46px) -->
    <g id="eye_left_orb">
      <!-- Dark Eyeliner Socket -->
      <circle cx="182" cy="165" r="48" fill="#1A0D06" stroke="#3D271A" stroke-width="3.0" />
      <!-- Radiant Amber Iris -->
      <circle cx="182" cy="165" r="45" fill="url(#amberEyeL)" />
      <!-- Deep Obsidian Pupil (Circular, centered, innocent) -->
      <circle cx="182" cy="165" r="30" fill="#0A0502" />
      <!-- Bottom Amber-Gold Reflex Arc (Hugging the bottom iris rim, UNDER pupil) -->
      <path d="M 152 174 C 160 198, 204 198, 212 174 C 200 186, 164 186, 152 174 Z" fill="#FEF08A" opacity="0.65" />
      <!-- Primary Glassy Specular Catchlight (10:30 o'clock - Large, round, bright white) -->
      <circle cx="168" cy="151" r="10.5" fill="#FFFFFF" />
      <!-- Secondary Micro Catchlight (4:30 o'clock) -->
      <circle cx="197" cy="180" r="4.2" fill="#FFFFFF" opacity="0.9" />
      <!-- Delicate Brow Fold Arc (Above eye on brow, not on pupil) -->
      <path d="M 142 136 C 160 116, 204 116, 222 136" fill="none" stroke="#382214" stroke-width="3.0" stroke-linecap="round" />
    </g>

    <!-- RIGHT EYE (Centered at X=330, Y=165, Radius=46px) -->
    <g id="eye_right_orb">
      <!-- Dark Eyeliner Socket -->
      <circle cx="330" cy="165" r="48" fill="#1A0D06" stroke="#3D271A" stroke-width="3.0" />
      <!-- Radiant Amber Iris -->
      <circle cx="330" cy="165" r="45" fill="url(#amberEyeR)" />
      <!-- Deep Obsidian Pupil (Circular, centered, innocent) -->
      <circle cx="330" cy="165" r="30" fill="#0A0502" />
      <!-- Bottom Amber-Gold Reflex Arc (Hugging the bottom iris rim, UNDER pupil) -->
      <path d="M 300 174 C 308 198, 352 198, 360 174 C 348 186, 312 186, 300 174 Z" fill="#FEF08A" opacity="0.65" />
      <!-- Primary Glassy Specular Catchlight (10:30 o'clock - Large, round, bright white) -->
      <circle cx="316" cy="151" r="10.5" fill="#FFFFFF" />
      <!-- Secondary Micro Catchlight (4:30 o'clock) -->
      <circle cx="345" cy="180" r="4.2" fill="#FFFFFF" opacity="0.9" />
      <!-- Delicate Brow Fold Arc (Above eye on brow, not on pupil) -->
      <path d="M 290 136 C 308 116, 352 116, 370 136" fill="none" stroke="#382214" stroke-width="3.0" stroke-linecap="round" />
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
    print(f"Written calibrated master SVG v4 to {filepath}")

if __name__ == "__main__":
    generate_owluko_calibrated_v4("scratch/owluko_calibrated_v4.svg")
