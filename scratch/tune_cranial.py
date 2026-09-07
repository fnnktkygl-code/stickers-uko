import sys
sys.path.append(".")
from scripts.benchmark_owluko_fidelity import render_svg, evaluate_fidelity

with open("scratch/test_feet_clean.svg", "r") as f:
    svg = f.read()

# Update cranial highlight:
# cx="225" cy="85" rx="100" ry="55"
# color: #FFF2E6
svg = svg.replace(
    '<radialGradient id="cranialHl" cx="42%" cy="20%" r="48%">\n      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.45" />\n      <stop offset="45%" stop-color="#F5EFEA" stop-opacity="0.16" />\n      <stop offset="100%" stop-color="#DED6CE" stop-opacity="0" />\n    </radialGradient>',
    '<radialGradient id="cranialHl" cx="38%" cy="16%" r="35%">\n      <stop offset="0%" stop-color="#FFF2E6" stop-opacity="0.50" />\n      <stop offset="50%" stop-color="#F5EFEA" stop-opacity="0.18" />\n      <stop offset="100%" stop-color="#DED6CE" stop-opacity="0" />\n    </radialGradient>'
)
svg = svg.replace(
    '<ellipse cx="248" cy="112" rx="142" ry="88" fill="url(#cranialHl)" />',
    '<ellipse cx="225" cy="85" rx="105" ry="55" fill="url(#cranialHl)" />'
)

with open("scratch/test_tune_cranial.svg", "w") as f:
    f.write(svg)

out_png = render_svg("scratch/test_tune_cranial.svg", "scratch/test_tune_cranial.png")
evaluate_fidelity(out_png)
