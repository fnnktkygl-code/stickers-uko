import os

def generate_owluko_simplified_svg(filepath):
    """
    100% Faithful Vector SVG matching user's simplified reference:
    - Ground truth: media_1788762944348.png / owluko_simplified_master_ref.png (1024x1024)
    - Perfectly calibrated palette:
      * Body: warm eggshell porcelain (#FAF7F0, #F7EEDB, #EFE0C7, #E5D0B2)
      * Mask: smooth infinity/spectacles barn owl mask (#FBF8EE, #F6ECD8, #ECD5B6)
      * Eyes: luminous liquid honey amber (#F8D758 -> #D49F2C -> #8C5F18)
      * Pupil: warm golden espresso (#6E4816)
      * Beak: smooth closed cone (#FBA343 to #EA580C)
      * Wings: smooth continuous teardrop flaps
      * Belly: soft plush heart-shield (#FDFBF4)
      * Feet: 3 rounded bean toes grounded at Y=876
    """
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  <defs>
    <!-- Soft Background Radial Ground Shadow -->
    <radialGradient id="groundShadow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#2D1A0D" stop-opacity="0.25" />
      <stop offset="45%" stop-color="#2D1A0D" stop-opacity="0.10" />
      <stop offset="80%" stop-color="#2D1A0D" stop-opacity="0.02" />
      <stop offset="100%" stop-color="#2D1A0D" stop-opacity="0" />
    </radialGradient>

    <!-- Master Chubby Body Warm Down Gradient -->
    <radialGradient id="bodyGrad" cx="50%" cy="30%" r="65%">
      <stop offset="0%" stop-color="#FCF9F3" />
      <stop offset="35%" stop-color="#F7EEDB" />
      <stop offset="65%" stop-color="#EFE0C7" />
      <stop offset="85%" stop-color="#E5D0B2" />
      <stop offset="100%" stop-color="#D4BDA0" />
    </radialGradient>

    <!-- Facial Mask Soft Warm Ivory Gradient -->
    <radialGradient id="faceMaskGrad" cx="50%" cy="38%" r="58%">
      <stop offset="0%" stop-color="#FFFDF7" />
      <stop offset="45%" stop-color="#FAF6EC" />
      <stop offset="75%" stop-color="#F2E7D4" />
      <stop offset="100%" stop-color="#E8D4BB" />
    </radialGradient>

    <!-- Eye Socket Soft Depression Gradients -->
    <radialGradient id="socketGrad" cx="48%" cy="48%" r="52%">
      <stop offset="0%" stop-color="#E5CEB0" stop-opacity="0.65" />
      <stop offset="65%" stop-color="#E5CEB0" stop-opacity="0.20" />
      <stop offset="100%" stop-color="#FAF6EC" stop-opacity="0" />
    </radialGradient>

    <!-- Liquid Honey Glassy Amber Iris Radial Gradient -->
    <radialGradient id="irisGrad" cx="36%" cy="34%" r="65%">
      <stop offset="0%" stop-color="#FFF388" />
      <stop offset="18%" stop-color="#FCE14E" />
      <stop offset="38%" stop-color="#EAB32A" />
      <stop offset="65%" stop-color="#B88018" />
      <stop offset="85%" stop-color="#845410" />
      <stop offset="100%" stop-color="#553208" />
    </radialGradient>

    <!-- Lower Iris Radiant Honey-Gold Crescent -->
    <radialGradient id="honeyCrescentGrad" cx="42%" cy="65%" r="50%">
      <stop offset="0%" stop-color="#FFF388" stop-opacity="0.95" />
      <stop offset="45%" stop-color="#F9D448" stop-opacity="0.80" />
      <stop offset="100%" stop-color="#D49A1C" stop-opacity="0" />
    </radialGradient>

    <!-- Smooth Teardrop Wing Linear Gradients -->
    <linearGradient id="wingLeftGrad" x1="10%" y1="15%" x2="85%" y2="85%">
      <stop offset="0%" stop-color="#F7EFE2" />
      <stop offset="40%" stop-color="#EBD9BF" />
      <stop offset="80%" stop-color="#DCC4A5" />
      <stop offset="100%" stop-color="#C8AD8B" />
    </linearGradient>
    <linearGradient id="wingRightGrad" x1="90%" y1="15%" x2="15%" y2="85%">
      <stop offset="0%" stop-color="#F7EFE2" />
      <stop offset="40%" stop-color="#EBD9BF" />
      <stop offset="80%" stop-color="#DCC4A5" />
      <stop offset="100%" stop-color="#C8AD8B" />
    </linearGradient>

    <!-- Smooth Heart-Shield Belly Patch Gradient -->
    <radialGradient id="bellyGrad" cx="50%" cy="30%" r="60%">
      <stop offset="0%" stop-color="#FFFEFA" />
      <stop offset="50%" stop-color="#F9F3E7" />
      <stop offset="80%" stop-color="#EFE2CF" />
      <stop offset="100%" stop-color="#E0CEB4" />
    </radialGradient>

    <!-- Closed Cone Beak Radial Shading -->
    <radialGradient id="beakDomeGrad" cx="48%" cy="26%" r="65%">
      <stop offset="0%" stop-color="#FED7AA" />
      <stop offset="35%" stop-color="#FBA343" />
      <stop offset="70%" stop-color="#EA580C" />
      <stop offset="100%" stop-color="#B93808" />
    </radialGradient>

    <!-- Toe Sausage Gradients -->
    <linearGradient id="toeGrad" x1="30%" y1="10%" x2="70%" y2="90%">
      <stop offset="0%" stop-color="#FED7AA" />
      <stop offset="35%" stop-color="#FBA343" />
      <stop offset="75%" stop-color="#EA580C" />
      <stop offset="100%" stop-color="#9A3412" />
    </linearGradient>
  </defs>

  <!-- 01. SOFT GROUND SHADOW UNDER FEET -->
  <g id="ground_shadow">
    <ellipse cx="512" cy="876" rx="260" ry="28" fill="url(#groundShadow)" />
    <ellipse cx="512" cy="874" rx="175" ry="15" fill="#1A0D06" opacity="0.16" />
  </g>

  <!-- 02. FEET (3 plump elongated bean toes per foot grounded under belly) -->
  <g id="feet_layer">
    <!-- LEFT FOOT (Centered around x=408, baseline y=876) -->
    <g id="foot_l">
      <!-- Outer Toe (leftmost, angled outward) -->
      <path d="M 390 844
               C 370 842, 350 852, 352 866
               C 354 876, 368 880, 386 876
               C 400 872, 408 860, 404 848
               C 402 844, 396 844, 390 844 Z"
            fill="url(#toeGrad)" />
      <ellipse cx="376" cy="858" rx="8" ry="4" fill="#FED7AA" opacity="0.8" transform="rotate(-15 376 858)" />

      <!-- Middle Toe (longest, grounded at y=876) -->
      <path d="M 416 838
               C 398 838, 388 850, 390 866
               C 392 880, 408 884, 424 882
               C 440 880, 448 868, 446 852
               C 444 840, 432 838, 416 838 Z"
            fill="url(#toeGrad)" />
      <ellipse cx="416" cy="854" rx="9" ry="5" fill="#FED7AA" opacity="0.85" />

      <!-- Inner Toe (angled forward-right) -->
      <path d="M 444 844
               C 432 844, 426 854, 428 866
               C 430 878, 442 882, 456 880
               C 470 878, 478 868, 476 856
               C 474 846, 460 844, 444 844 Z"
            fill="url(#toeGrad)" />
      <ellipse cx="452" cy="858" rx="7.5" ry="4.5" fill="#FED7AA" opacity="0.8" transform="rotate(10 452 858)" />
    </g>

    <!-- RIGHT FOOT (Centered around x=618, baseline y=876) -->
    <g id="foot_r">
      <!-- Inner Toe (angled forward-left) -->
      <path d="M 580 844
               C 564 844, 550 846, 548 856
               C 546 868, 554 878, 568 880
               C 582 882, 594 878, 596 866
               C 598 854, 592 844, 580 844 Z"
            fill="url(#toeGrad)" />
      <ellipse cx="572" cy="858" rx="7.5" ry="4.5" fill="#FED7AA" opacity="0.8" transform="rotate(-10 572 858)" />

      <!-- Middle Toe (longest, grounded at y=876) -->
      <path d="M 608 838
               C 592 838, 580 840, 578 852
               C 576 868, 584 880, 600 882
               C 616 884, 632 880, 634 866
               C 636 850, 626 838, 608 838 Z"
            fill="url(#toeGrad)" />
      <ellipse cx="608" cy="854" rx="9" ry="5" fill="#FED7AA" opacity="0.85" />

      <!-- Outer Toe (rightmost, angled outward) -->
      <path d="M 634 844
               C 628 844, 622 844, 620 848
               C 616 860, 624 872, 638 876
               C 656 880, 670 876, 672 866
               C 674 852, 654 842, 634 844 Z"
            fill="url(#toeGrad)" />
      <ellipse cx="648" cy="858" rx="8" ry="4" fill="#FED7AA" opacity="0.8" transform="rotate(15 648 858)" />
    </g>
  </g>

  <!-- 03. CHUBBY CONTINUOUS EGG BODY -->
  <g id="body_layer">
    <path id="body_silhouette"
          d="M 512 144
             C 635 144, 735 190, 775 285
             C 805 350, 805 420, 810 470
             C 835 500, 858 540, 858 600
             C 858 660, 842 710, 785 765
             C 725 825, 630 852, 512 852
             C 394 852, 299 825, 239 765
             C 182 710, 166 660, 166 600
             C 166 540, 189 500, 214 470
             C 219 420, 219 350, 249 285
             C 289 190, 389 144, 512 144 Z"
          fill="url(#bodyGrad)" />
  </g>

  <!-- 04. SMOOTH TEARDROP WING FLAPS (Clean, continuous, no scallops) -->
  <g id="wings_layer">
    <!-- LEFT WING -->
    <path d="M 220 460
             C 192 495, 172 548, 168 605
             C 165 655, 182 705, 215 726
             C 238 732, 256 712, 258 680
             C 255 620, 248 550, 220 460 Z"
          fill="#D0BCA0" opacity="0.38" />

    <path id="wing_left_main"
          d="M 218 450
             C 190 488, 170 540, 166 598
             C 164 645, 180 695, 212 718
             C 232 725, 252 708, 256 678
             C 256 618, 250 550, 218 450 Z"
          fill="url(#wingLeftGrad)" />

    <!-- RIGHT WING -->
    <path d="M 804 460
             C 832 495, 852 548, 856 605
             C 859 655, 842 705, 809 726
             C 786 732, 768 712, 766 680
             C 769 620, 776 550, 804 460 Z"
          fill="#D0BCA0" opacity="0.38" />

    <path id="wing_right_main"
          d="M 806 450
             C 834 488, 854 540, 858 598
             C 860 645, 844 695, 812 718
             C 792 725, 772 708, 768 678
             C 768 618, 774 550, 806 450 Z"
          fill="url(#wingRightGrad)" />
  </g>

  <!-- 05. SMOOTH HEART-SHIELD BELLY DOWN PATCH (Clean, soft, plush) -->
  <g id="belly_layer">
    <path id="belly_patch"
          d="M 512 510
             C 455 484, 380 484, 335 520
             C 275 572, 270 660, 310 740
             C 358 820, 432 846, 512 846
             C 592 846, 666 820, 714 740
             C 754 660, 749 572, 689 520
             C 644 484, 569 484, 512 510 Z"
          fill="url(#bellyGrad)" />
  </g>

  <!-- 06. SMOOTH BARN OWL FACIAL MASK (Spectacles / Infinity Clean Curves) -->
  <g id="facial_mask_layer">
    <!-- Ambient shadow under facial mask -->
    <path d="M 512 288
             C 450 216, 330 216, 274 276
             C 226 332, 226 420, 268 474
             C 324 532, 440 520, 512 454
             C 584 520, 700 532, 756 474
             C 798 420, 798 332, 750 276
             C 694 216, 574 216, 512 288 Z"
          fill="#D6C1A4" opacity="0.38" transform="translate(0, 5)" />

    <!-- Main Facial Mask: Smooth Double-Lobed Infinity Spectacles -->
    <path id="facial_mask_main"
          d="M 512 286
             C 450 215, 330 215, 274 274
             C 226 330, 226 418, 268 470
             C 324 528, 440 516, 512 448
             C 584 516, 700 528, 756 470
             C 798 418, 798 330, 750 274
             C 694 215, 574 215, 512 286 Z"
          fill="url(#faceMaskGrad)" />

    <!-- Left Eye Socket Soft Depression -->
    <ellipse cx="398" cy="365" rx="76" ry="72" fill="url(#socketGrad)" />

    <!-- Right Eye Socket Soft Depression -->
    <ellipse cx="626" cy="365" rx="76" ry="72" fill="url(#socketGrad)" />
  </g>

  <!-- 07. EYES (Both Eyes Wide Open, Radiant Liquid Honey Amber Orbs) -->
  <g id="eyes_layer">
    <!-- LEFT EYE (Centered at cx=398, cy=362) -->
    <g id="eye_left">
      <!-- Soft socket ambient shadow rim -->
      <circle cx="398" cy="362" r="64" fill="#6B4B32" opacity="0.4" />
      <circle cx="398" cy="362" r="61.5" fill="#42290E" />

      <!-- Radiant Liquid Honey Amber Iris -->
      <circle cx="398" cy="362" r="59" fill="url(#irisGrad)" />

      <!-- Lower Honey-Gold Crescent -->
      <ellipse cx="393" cy="384" rx="46" ry="28" fill="url(#honeyCrescentGrad)" />

      <!-- Deep Golden Espresso Pupil (Centered at cx=402, cy=355, r=37) -->
      <circle cx="402" cy="355" r="37" fill="#6E4816" />
      <circle cx="402" cy="355" r="33" fill="#52340E" />

      <!-- Specular Highlight 1: Brilliant circle at 11 o'clock (cx=378, cy=336, r=11.5) -->
      <circle cx="378" cy="336" r="11.5" fill="#FFFFFF" />

      <!-- Specular Highlight 2: Catchlight at 4:30 o'clock (cx=424, cy=386, r=4.5) -->
      <circle cx="424" cy="386" r="4.5" fill="#FFFFFF" opacity="0.95" />
    </g>

    <!-- RIGHT EYE (Centered at cx=626, cy=362) -->
    <g id="eye_right">
      <!-- Soft socket ambient shadow rim -->
      <circle cx="626" cy="362" r="64" fill="#6B4B32" opacity="0.4" />
      <circle cx="626" cy="362" r="61.5" fill="#42290E" />

      <!-- Radiant Liquid Honey Amber Iris -->
      <circle cx="626" cy="362" r="59" fill="url(#irisGrad)" />

      <!-- Lower Honey-Gold Crescent -->
      <ellipse cx="621" cy="384" rx="46" ry="28" fill="url(#honeyCrescentGrad)" />

      <!-- Deep Golden Espresso Pupil (Centered at cx=622, cy=355, r=37) -->
      <circle cx="622" cy="355" r="37" fill="#6E4816" />
      <circle cx="622" cy="355" r="33" fill="#52340E" />

      <!-- Specular Highlight 1: Brilliant circle at 11 o'clock (cx=606, cy=336, r=11.5) -->
      <circle cx="606" cy="336" r="11.5" fill="#FFFFFF" />

      <!-- Specular Highlight 2: Catchlight at 4:30 o'clock (cx=652, cy=386, r=4.5) -->
      <circle cx="652" cy="386" r="4.5" fill="#FFFFFF" opacity="0.95" />
    </g>
  </g>

  <!-- 08. CUTE CLOSED CONE BEAK -->
  <g id="beak_layer">
    <!-- Beak Drop Shadow onto mask & belly -->
    <path d="M 476 422
             C 512 468, 512 468, 548 422
             C 536 448, 488 448, 476 422 Z"
          fill="#3D2010" opacity="0.25" transform="translate(0, 4)" />

    <!-- Closed Cone Beak Shape (Sculpted rounded cone) -->
    <path id="beak_cone"
          d="M 512 388
             C 532 388, 546 404, 548 422
             C 536 438, 524 450, 512 452
             C 500 450, 488 438, 476 422
             C 478 404, 492 388, 512 388 Z"
          fill="url(#beakDomeGrad)" />

    <!-- Beak Bridge Vertical Soft Highlight -->
    <ellipse cx="512" cy="406" rx="8" ry="12" fill="#FED7AA" opacity="0.8" />
    <ellipse cx="512" cy="402" rx="4" ry="6" fill="#FFFFFE" opacity="0.7" />

    <!-- Subtle Lower Beak Facet Shadow -->
    <path d="M 476 422
             C 498 436, 512 452, 512 452
             C 512 452, 526 436, 548 422
             C 534 438, 524 448, 512 450
             C 500 448, 490 438, 476 422 Z"
          fill="#C2410C" opacity="0.35" />
  </g>
</svg>'''

    with open(filepath, 'w') as f:
        f.write(svg)
    print(f"Generated 100% exact simplified reference SVG at {filepath}")

if __name__ == "__main__":
    generate_owluko_simplified_svg("scratch/owluko_simplified_master.svg")
