import cv2
import numpy as np
from PIL import Image

# Load panel 4 aligned and master clean
p4 = Image.open('scratch/panel_4_aligned.png').convert('RGBA')
master = Image.open('mascots/owluko/owluko_master_ref_clean.png').convert('RGBA')

# Let's inspect the exact SVG representation of the waving wing
# We can create an SVG test file:
svg_test = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  <defs>
    <!-- Shading Gradients for Waving Wing -->
    <linearGradient id="wave_wing_grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFDF9"/>
      <stop offset="35%" stop-color="#F8F3EA"/>
      <stop offset="70%" stop-color="#EEDFC8"/>
      <stop offset="100%" stop-color="#D4BEA2"/>
    </linearGradient>
    <linearGradient id="wave_wing_crease" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#C5AC91" stop-opacity="0.0"/>
      <stop offset="50%" stop-color="#B89B7D" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#A88768" stop-opacity="0.5"/>
    </linearGradient>
    <radialGradient id="shoulder_shadow" cx="30%" cy="80%" r="70%">
      <stop offset="0%" stop-color="#BA9A78" stop-opacity="0.4"/>
      <stop offset="70%" stop-color="#E0CEB4" stop-opacity="0.1"/>
      <stop offset="100%" stop-color="#FAF6EE" stop-opacity="0.0"/>
    </radialGradient>
  </defs>

  <!-- Base Reference Underlay -->
  <image href="panel_4_aligned.png" width="1024" height="1024" opacity="0.3"/>

  <!-- Waving Wing Group centered near shoulder pivot (770, 560) -->
  <g id="waving_wing_test" transform="rotate(0, 770, 560)">
    <!-- 1. Ambient Occlusion Under Wing -->
    <path d="M 750,530 C 765,580 775,640 760,700 C 750,715 770,720 780,700 C 800,640 790,570 765,525 Z" fill="url(#shoulder_shadow)"/>

    <!-- 2. Main 3-Lobe Waving Wing Silhouette -->
    <!--
      Starts at inner shoulder (748, 380)
      Curves up along inner edge to primary feather tip (868, 175)
      Rounds tip of primary feather (868, 175 -> 885, 185)
      Drops into first notch (895, 252)
      Rises to second feather tip (942, 238)
      Rounds tip of second feather (942, 238 -> 956, 260)
      Drops into second notch (948, 322)
      Rises to third feather tip (974, 345)
      Rounds tip of third feather (974, 345 -> 970, 385)
      Curves down along outer lower flank (950, 460 -> 890, 560 -> 820, 645 -> 765, 715)
      Closes along shoulder seam (765, 715 -> 748, 380)
    -->
    <path id="wing_wave_main" d="
      M 748,390
      C 760,330 805,240 858,175
      C 872,158 892,168 894,192
      C 896,215 888,245 892,260
      C 896,275 918,255 936,242
      C 952,230 968,242 966,265
      C 964,288 948,318 952,335
      C 956,350 976,345 982,360
      C 990,380 985,410 968,438
      C 942,482 905,548 852,612
      C 810,662 776,698 758,715
      C 745,695 735,620 735,550
      C 735,480 742,420 748,390 Z"
      fill="url(#wave_wing_grad)"
      stroke="#D8C5AE" stroke-width="1.5" stroke-opacity="0.5"/>

    <!-- Subtle Feather Creases / Shading between Lobes -->
    <!-- Crease 1: between primary and middle feather -->
    <path d="M 892,260 C 885,285 870,335 850,380 C 835,415 820,445 805,470"
      fill="none" stroke="#D0BA9E" stroke-width="3.2" stroke-linecap="round" stroke-opacity="0.6"/>

    <!-- Crease 2: between middle and lower feather -->
    <path d="M 952,335 C 938,365 915,415 890,460 C 870,495 850,525 830,550"
      fill="none" stroke="#D0BA9E" stroke-width="3.2" stroke-linecap="round" stroke-opacity="0.6"/>

    <!-- Top Feather Highlight Curve -->
    <path d="M 770,320 C 805,240 850,185 868,175 C 878,170 885,178 888,195"
      fill="none" stroke="#FFFFFF" stroke-width="3.0" stroke-linecap="round" stroke-opacity="0.8"/>
  </g>
</svg>'''

with open('scratch/waving_wing_test.svg', 'w') as f:
    f.write(svg_test)

print("Saved scratch/waving_wing_test.svg")
