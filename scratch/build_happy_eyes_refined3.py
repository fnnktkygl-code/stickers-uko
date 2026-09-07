svg_face = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  <image href="panel_5_aligned.png" width="1024" height="1024" opacity="0.5"/>

  <!-- Left Happy Eye Tapered Crescent -->
  <path d="
    M 345,374
    C 362,362 380,352 398,352
    C 416,352 434,362 451,374
    C 436,354 418,340 398,340
    C 378,340 360,354 345,374 Z"
    fill="#52381C"/>

  <!-- Right Happy Eye Tapered Crescent -->
  <path d="
    M 573,374
    C 590,362 608,352 626,352
    C 644,352 662,362 679,374
    C 664,354 646,340 626,340
    C 606,340 588,354 573,374 Z"
    fill="#52381C"/>
</svg>'''

with open('scratch/happy_eyes_refined3.svg', 'w') as f:
    f.write(svg_face)

