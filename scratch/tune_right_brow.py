import sys
sys.path.append(".")
from scripts.benchmark_owluko_fidelity import render_svg, evaluate_fidelity

with open("scratch/test_chest_radiance.svg", "r") as f:
    svg = f.read()

# Add right temple/brow soft shading gradient
r_head_shadow_def = """
    <!-- Right Head / Brow Ambient Shadow -->
    <linearGradient id="rHeadShadow" x1="0%" y1="20%" x2="100%" y2="80%">
      <stop offset="0%" stop-color="#C5B8AC" stop-opacity="0" />
      <stop offset="50%" stop-color="#8E7E70" stop-opacity="0.30" />
      <stop offset="100%" stop-color="#554436" stop-opacity="0.55" />
    </linearGradient>
"""
svg = svg.replace("</defs>", f"{r_head_shadow_def}\n  </defs>")

# Add right brow shadow path
r_head_shadow_path = """
    <!-- Right Brow & Temple Shading -->
    <path d="M 265 75 C 330 80, 395 105, 405 180 C 375 180, 330 160, 290 140 C 270 120, 260 95, 265 75 Z" fill="url(#rHeadShadow)" />
"""
svg = svg.replace("<!-- Right Flank Ambient Occlusion -->", f"{r_head_shadow_path}\n    <!-- Right Flank Ambient Occlusion -->")

with open("scratch/test_right_brow.svg", "w") as f:
    f.write(svg)

out_png = render_svg("scratch/test_right_brow.svg", "scratch/test_right_brow.png")
evaluate_fidelity(out_png)
