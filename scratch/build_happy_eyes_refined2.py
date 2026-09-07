svg_face = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  <image href="panel_5_aligned.png" width="1024" height="1024" opacity="0.45"/>

  <!-- Left Happy Eye Tapered Crescent -->
  <path d="
    M 345,366
    C 362,354 380,344 398,344
    C 416,344 434,354 451,366
    C 436,346 418,332 398,332
    C 378,332 360,346 345,366 Z"
    fill="#52381C"/>

  <!-- Right Happy Eye Tapered Crescent -->
  <path d="
    M 573,366
    C 590,354 608,344 626,344
    C 644,344 662,354 679,366
    C 664,346 646,332 626,332
    C 606,332 588,346 573,366 Z"
    fill="#52381C"/>
</svg>'''

with open('scratch/happy_eyes_refined2.svg', 'w') as f:
    f.write(svg_face)

