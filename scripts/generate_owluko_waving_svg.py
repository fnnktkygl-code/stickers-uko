import os

def generate_owluko_waving_svg(filepath):
    """
    100% Faithful Vector SVG matching user's simplified model & waving storyboard:
    - Master Model: media_1788763397755.png / media_1788762944348.png
    - Waving Storyboard: media_1788763379758.png (6 panels)
    - 3-Finger Smooth Porcelain Waving Wing (pure organic curves, zero stroke creases)
    - Joyful Smiling Eyes (espresso crescent arcs on top of cream porcelain eyelids)
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

    <!-- Smooth 3-Finger Waving Wing Porcelain Gradient -->
    <linearGradient id="wingWavePureGrad" x1="20%" y1="15%" x2="80%" y2="85%">
      <stop offset="0%" stop-color="#FCF9F3"/>
      <stop offset="30%" stop-color="#F7EEDB"/>
      <stop offset="65%" stop-color="#EBD9BF"/>
      <stop offset="100%" stop-color="#DCC4A5"/>
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
      <stop offset="40%" stop-color="#FB923C" />
      <stop offset="75%" stop-color="#EA580C" />
      <stop offset="100%" stop-color="#C2410C" />
    </linearGradient>
  </defs>

  <!-- ========================================== -->
  <!-- LAYER 1: GROUND CONTACT SHADOW             -->
  <!-- ========================================== -->
  <g id="ground_shadow_group">
    <ellipse id="ground_shadow_outer" cx="512" cy="876" rx="275" ry="34" fill="url(#groundShadow)" />
    <ellipse id="ground_shadow_dense" cx="512" cy="876" rx="205" ry="22" fill="#2D1A0D" opacity="0.18" />
  </g>

  <!-- ========================================== -->
  <!-- LAYER 2: 3-BEAN ROUNDED FEET               -->
  <!-- ========================================== -->
  <g id="feet_group">
    <!-- Left Foot (Toes 1, 2, 3) -->
    <g id="foot_left">
      <ellipse id="toe_l1" cx="372" cy="870" rx="19" ry="13" transform="rotate(-18 372 870)" fill="url(#toeGrad)" />
      <ellipse id="toe_l2" cx="400" cy="872" rx="22" ry="14" fill="url(#toeGrad)" />
      <ellipse id="toe_l3" cx="428" cy="870" rx="19" ry="13" transform="rotate(16 428 870)" fill="url(#toeGrad)" />
      <ellipse id="toe_l1_hi" cx="370" cy="867" rx="8" ry="4" transform="rotate(-18 370 867)" fill="#FED7AA" opacity="0.65" />
      <ellipse id="toe_l2_hi" cx="400" cy="868" rx="10" ry="4" fill="#FED7AA" opacity="0.75" />
      <ellipse id="toe_l3_hi" cx="430" cy="867" rx="8" ry="4" transform="rotate(16 430 867)" fill="#FED7AA" opacity="0.65" />
    </g>
    <!-- Right Foot (Toes 1, 2, 3) -->
    <g id="foot_right">
      <ellipse id="toe_r1" cx="596" cy="870" rx="19" ry="13" transform="rotate(-16 596 870)" fill="url(#toeGrad)" />
      <ellipse id="toe_r2" cx="624" cy="872" rx="22" ry="14" fill="url(#toeGrad)" />
      <ellipse id="toe_r3" cx="652" cy="870" rx="19" ry="13" transform="rotate(18 652 870)" fill="url(#toeGrad)" />
      <ellipse id="toe_r1_hi" cx="594" cy="867" rx="8" ry="4" transform="rotate(-16 594 867)" fill="#FED7AA" opacity="0.65" />
      <ellipse id="toe_r2_hi" cx="624" cy="868" rx="10" ry="4" fill="#FED7AA" opacity="0.75" />
      <ellipse id="toe_r3_hi" cx="654" cy="867" rx="8" ry="4" transform="rotate(18 654 867)" fill="#FED7AA" opacity="0.65" />
    </g>
  </g>

  <!-- ========================================== -->
  <!-- LAYER 3: MAIN CHUBBY BODY CAPSULE          -->
  <!-- ========================================== -->
  <g id="body_main_group">
    <path id="body_silhouette" d="
      M 512, 144
      C 628, 144  756, 218  782, 372
      C 804, 502  806, 672  726, 796
      C 666, 888  358, 888  298, 796
      C 218, 672  220, 502  242, 372
      C 268, 218  396, 144  512, 144 Z"
      fill="url(#bodyGrad)" />
  </g>

  <!-- ========================================== -->
  <!-- LAYER 4: WINGS                             -->
  <!-- ========================================== -->
  <g id="wings_group">
    <!-- Left Wing (Viewer Left) -->
    <g id="wing_left">
      <path id="wing_left_shadow" d="
        M 248, 442
        C 220, 482  196, 560  204, 642
        C 212, 722  244, 762  262, 750
        C 272, 744  272, 700  266, 638
        C 260, 576  256, 498  248, 442 Z"
        fill="#B89B7D" opacity="0.22" />
      <path id="wing_left_main" d="
        M 252, 456
        C 218, 488  190, 568  198, 648
        C 206, 728  238, 764  256, 748
        C 268, 738  274, 690  270, 630
        C 266, 570  262, 498  252, 456 Z"
        fill="url(#wingLeftGrad)" />
    </g>

    <!-- Right Wing (Resting Folded Pose) -->
    <g id="wing_right_rest">
      <path id="wing_right_shadow" d="
        M 776, 442
        C 804, 482  828, 560  820, 642
        C 812, 722  780, 762  762, 750
        C 752, 744  752, 700  758, 638
        C 764, 576  768, 498  776, 442 Z"
        fill="#B89B7D" opacity="0.22" />
      <path id="wing_right_main" d="
        M 772, 456
        C 806, 488  834, 568  826, 648
        C 818, 728  786, 764  768, 748
        C 756, 738  750, 690  754, 630
        C 758, 570  762, 498  772, 456 Z"
        fill="url(#wingRightGrad)" />
    </g>

    <!-- Right Wing (Smooth 3-Finger Waving Pose) -->
    <g id="wing_right_wave">
      <!-- Soft ambient shadow behind wing -->
      <path id="wing_wave_shadow" d="
        M 750, 520
        C 765, 570  775, 630  760, 690
        C 750, 705  770, 710  780, 690
        C 800, 630  790, 560  765, 515 Z"
        fill="#B89B7D" opacity="0.25"/>

      <!-- Smooth Continuous 3-Lobe Porcelain Waving Wing -->
      <path id="wing_wave_smooth_main" d="
        M 780, 360
        C 796, 310  836, 230  874, 184
        C 886, 170  902, 178  905, 196
        C 908, 214  906, 240  914, 252
        C 920, 260  934, 246  944, 240
        C 958, 232  968, 242  966, 260
        C 964, 278  952, 298  960, 312
        C 966, 322  982, 312  990, 324
        C 1000, 340  996, 372  984, 402
        C 966, 448  926, 520  868, 574
        C 824, 614  792, 646  778, 670
        C 772, 630  768, 540  768, 460
        C 768, 410  774, 380  780, 360 Z"
        fill="url(#wingWavePureGrad)" />
    </g>
  </g>

  <!-- ========================================== -->
  <!-- LAYER 5: SMOOTH HEART-SHIELD BELLY PATCH   -->
  <!-- ========================================== -->
  <g id="belly_group">
    <path id="belly_patch" d="
      M 512, 546
      C 560, 524  670, 532  702, 638
      C 724, 712  698, 804  644, 856
      C 592, 904  432, 904  380, 856
      C 326, 804  300, 712  322, 638
      C 354, 532  464, 524  512, 546 Z"
      fill="url(#bellyGrad)" />
  </g>

  <!-- ========================================== -->
  <!-- LAYER 6: HEAD & FACIAL MASK                -->
  <!-- ========================================== -->
  <g id="head_mask_group">
    <path id="facial_mask_shadow" d="
      M 512, 336
      C 468, 214  310, 218  276, 362
      C 252, 464  332, 544  434, 522
      C 472, 514  496, 484  512, 458
      C 528, 484  552, 514  590, 522
      C 692, 544  772, 464  748, 362
      C 714, 218  556, 214  512, 336 Z"
      fill="#D4BDA0" opacity="0.25" />
    <path id="facial_mask_main" d="
      M 512, 330
      C 470, 222  318, 226  284, 364
      C 260, 460  338, 536  436, 516
      C 472, 508  496, 478  512, 452
      C 528, 478  552, 508  588, 516
      C 686, 536  764, 460  740, 364
      C 706, 226  554, 222  512, 330 Z"
      fill="url(#faceMaskGrad)" />
    <ellipse id="socket_left" cx="398" cy="362" rx="72" ry="72" fill="url(#socketGrad)" />
    <ellipse id="socket_right" cx="626" cy="362" rx="72" ry="72" fill="url(#socketGrad)" />
  </g>

  <!-- ========================================== -->
  <!-- LAYER 7: EYES (OPEN STATE & HAPPY SMILE)   -->
  <!-- ========================================== -->
  <g id="eyes_group">
    <!-- LEFT EYE (Viewer Left) -->
    <g id="eye_left">
      <!-- Open Eye Elements -->
      <circle id="eye_l_outer_rim" cx="398" cy="362" r="64" fill="#3D2406" />
      <circle id="eye_l_iris" cx="398" cy="362" r="62" fill="url(#irisGrad)" />
      <path id="eye_l_crescent" d="
        M 346, 364
        C 350, 404  394, 422  438, 404
        C 448, 396  454, 384  458, 372
        C 446, 408  402, 420  362, 402
        C 350, 392  346, 378  346, 364 Z"
        fill="url(#honeyCrescentGrad)" />
      <circle id="eye_l_pupil" cx="402" cy="355" r="37" fill="#6E4816" />
      <ellipse id="eye_l_pupil_inner" cx="402" cy="355" r="34" fill="#52340E" />
      <ellipse id="eye_l_glint_major" cx="376" cy="334" rx="16" ry="17" transform="rotate(-18 376 334)" fill="#FFFFFF" opacity="0.96" />
      <ellipse id="eye_l_glint_minor" cx="426" cy="378" rx="7" ry="7" fill="#FFFFFF" opacity="0.88" />

      <!-- Happy Smile Eye Crescent (Panel 5 Joyful Expression) -->
      <path id="happy_eye_l" d="
        M 345,374
        C 362,362 380,352 398,352
        C 416,352 434,362 451,374
        C 436,354 418,340 398,340
        C 378,340 360,354 345,374 Z"
        fill="#52381C" opacity="0" />
    </g>

    <!-- RIGHT EYE (Viewer Right) -->
    <g id="eye_right">
      <!-- Open Eye Elements -->
      <circle id="eye_r_outer_rim" cx="626" cy="362" r="64" fill="#3D2406" />
      <circle id="eye_r_iris" cx="626" cy="362" r="62" fill="url(#irisGrad)" />
      <path id="eye_r_crescent" d="
        M 574, 364
        C 578, 404  622, 422  666, 404
        C 676, 396  682, 384  686, 372
        C 674, 408  630, 420  590, 402
        C 578, 392  574, 378  574, 364 Z"
        fill="url(#honeyCrescentGrad)" />
      <circle id="eye_r_pupil" cx="622" cy="355" r="37" fill="#6E4816" />
      <ellipse id="eye_r_pupil_inner" cx="622" cy="355" r="34" fill="#52340E" />
      <ellipse id="eye_r_glint_major" cx="598" cy="334" rx="16" ry="17" transform="rotate(-18 598 334)" fill="#FFFFFF" opacity="0.96" />
      <ellipse id="eye_r_glint_minor" cx="648" cy="378" rx="7" ry="7" fill="#FFFFFF" opacity="0.88" />

      <!-- Happy Smile Eye Crescent (Panel 5 Joyful Expression) -->
      <path id="happy_eye_r" d="
        M 573,374
        C 590,362 608,352 626,352
        C 644,352 662,362 679,374
        C 664,354 646,340 626,340
        C 606,340 588,354 573,374 Z"
        fill="#52381C" opacity="0" />
    </g>
  </g>

  <!-- ========================================== -->
  <!-- LAYER 8: CUTE CLOSED CONE BEAK             -->
  <!-- ========================================== -->
  <g id="beak_group">
    <path id="beak_shadow" d="
      M 482, 408
      C 474, 402  550, 402  542, 408
      C 536, 442  518, 464  512, 464
      C 506, 464  488, 442  482, 408 Z"
      fill="#8C2E06" opacity="0.30" />
    <path id="beak_cone" d="
      M 482, 404
      C 476, 396  548, 396  542, 404
      C 536, 438  518, 460  512, 460
      C 506, 460  488, 438  482, 404 Z"
      fill="url(#beakDomeGrad)" />
    <ellipse id="beak_highlight" cx="508" cy="409" rx="14" ry="7" transform="rotate(-6 508 409)" fill="#FEEBC8" opacity="0.75" />
    <ellipse id="beak_tip_point" cx="512" cy="454" rx="5" ry="3" fill="#FED7AA" opacity="0.60" />
  </g>
</svg>'''

    with open(filepath, 'w') as f:
        f.write(svg)
    print(f"Generated clean waving master SVG at: {filepath}")

if __name__ == '__main__':
    out_svg = os.path.abspath('scratch/owluko_waving_master.svg')
    generate_owluko_waving_svg(out_svg)
