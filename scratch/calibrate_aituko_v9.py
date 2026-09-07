import sys
sys.path.append(".")
import cv2, numpy as np
from PIL import Image
from scripts.benchmark_aituko_fidelity import render_svg_chrome, evaluate_aituko

with open("scratch/test_aituko_calibrated_v8.svg", "r") as f:
    svg = f.read()

# Fix ground shadow: center at 256, 480, rx=105, ry=20 with slightly higher opacity at edge
old_shadow = """    <!-- Ground Contact Shadow -->
    <radialGradient id="groundShadow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.62" />
      <stop offset="60%" stop-color="#000000" stop-opacity="0.45" />
      <stop offset="90%" stop-color="#000000" stop-opacity="0.16" />
      <stop offset="100%" stop-color="#000000" stop-opacity="0.0" />
    </radialGradient>"""

new_shadow = """    <!-- Ground Contact Shadow (Calibrated to 461-499, 152-360) -->
    <radialGradient id="groundShadow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.62" />
      <stop offset="55%" stop-color="#000000" stop-opacity="0.45" />
      <stop offset="85%" stop-color="#000000" stop-opacity="0.22" />
      <stop offset="96%" stop-color="#000000" stop-opacity="0.10" />
      <stop offset="100%" stop-color="#000000" stop-opacity="0.0" />
    </radialGradient>"""

svg = svg.replace(old_shadow, new_shadow)
svg = svg.replace("""<ellipse cx="256" cy="480" rx="110" ry="20" fill="url(#groundShadow)" />""", """<ellipse cx="256" cy="480" rx="104" ry="20" fill="url(#groundShadow)" />""")

with open("scratch/test_aituko_calibrated_v9.svg", "w") as f:
    f.write(svg)

png = render_svg_chrome("scratch/test_aituko_calibrated_v9.svg", "scratch/test_aituko_calibrated_v9.png")
res = evaluate_aituko(png)
