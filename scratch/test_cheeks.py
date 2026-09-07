import sys
sys.path.append(".")
from scripts.benchmark_owluko_fidelity import render_svg, evaluate_fidelity

with open("scratch/test_pupil_calib.svg", "r") as f:
    svg = f.read()

# Add cheek gradients to defs
cheek_defs = """
    <!-- Cheek Radial Highlights -->
    <radialGradient id="leftCheekGlow" cx="45%" cy="45%" r="50%">
      <stop offset="0%" stop-color="#FFF4E8" stop-opacity="0.55" />
      <stop offset="60%" stop-color="#F5E8DC" stop-opacity="0.25" />
      <stop offset="100%" stop-color="#E8DDD5" stop-opacity="0" />
    </radialGradient>

    <radialGradient id="rightCheekGlow" cx="50%" cy="45%" r="50%">
      <stop offset="0%" stop-color="#FFE8D2" stop-opacity="0.30" />
      <stop offset="60%" stop-color="#F0DDD0" stop-opacity="0.10" />
      <stop offset="100%" stop-color="#E8DDD5" stop-opacity="0" />
    </radialGradient>
"""

svg = svg.replace("</defs>", f"{cheek_defs}\n  </defs>")

# Add cheek ellipses inside clipPath
cheek_elements = """
    <!-- Facial Cheek Volumes -->
    <ellipse cx="135" cy="160" rx="30" ry="34" fill="url(#leftCheekGlow)" />
    <ellipse cx="378" cy="158" rx="30" ry="34" fill="url(#rightCheekGlow)" />
"""

svg = svg.replace("<!-- Beak Cast Shadow -->", f"{cheek_elements}\n    <!-- Beak Cast Shadow -->")

with open("scratch/test_cheeks.svg", "w") as f:
    f.write(svg)

out_png = render_svg("scratch/test_cheeks.svg", "scratch/test_cheeks.png")
evaluate_fidelity(out_png)
