import sys
sys.path.append(".")
from scripts.benchmark_owluko_fidelity import render_svg, evaluate_fidelity

with open("scratch/temp_quick.svg", "r") as f:
    svg = f.read()

# Soften rWingShadow lower opacity
svg = svg.replace(
    '<linearGradient id="rWingShadow" x1="10%" y1="20%" x2="90%" y2="80%">\n      <stop offset="0%" stop-color="#C5B8AC" stop-opacity="0.15" />\n      <stop offset="45%" stop-color="#8E7E70" stop-opacity="0.42" />\n      <stop offset="100%" stop-color="#554436" stop-opacity="0.65" />\n    </linearGradient>',
    '<linearGradient id="rWingShadow" x1="10%" y1="20%" x2="90%" y2="80%">\n      <stop offset="0%" stop-color="#C5B8AC" stop-opacity="0.10" />\n      <stop offset="45%" stop-color="#9E8E80" stop-opacity="0.30" />\n      <stop offset="100%" stop-color="#706050" stop-opacity="0.35" />\n    </linearGradient>'
)

with open("scratch/test_rwing_fix.svg", "w") as f:
    f.write(svg)

out_png = render_svg("scratch/test_rwing_fix.svg", "scratch/test_rwing_fix.png")
evaluate_fidelity(out_png)
