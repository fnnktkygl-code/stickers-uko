from PIL import Image

svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  <defs>
    <linearGradient id="waveGradPure" x1="20%" y1="15%" x2="80%" y2="85%">
      <stop offset="0%" stop-color="#FCF9F3"/>
      <stop offset="30%" stop-color="#F7EEDB"/>
      <stop offset="65%" stop-color="#EBD9BF"/>
      <stop offset="100%" stop-color="#DCC4A5"/>
    </linearGradient>
  </defs>

  <image href="panel_3_aligned.png" width="1024" height="1024" opacity="0.4"/>

  <!-- Smooth 3-Finger Porcelain Wing -->
  <path id="waving_wing_smooth" d="
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
    fill="url(#waveGradPure)"/>
</svg>'''

with open('scratch/test_smooth_cubic_wing.svg', 'w') as f:
    f.write(svg)

