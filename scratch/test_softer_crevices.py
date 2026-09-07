import sys
sys.path.append(".")
from scripts.benchmark_owluko_fidelity import render_svg, evaluate_fidelity

with open("scratch/test_tune_lighting.svg", "r") as f:
    svg = f.read()

# Soften the crevice strokes from stroke-width 3.5-4.0 #1D1208 to stroke-width 2.2 #2E1E12 opacity 0.65
svg = svg.replace('stroke="#1D1208" stroke-width="3.5"', 'stroke="#382414" stroke-width="2.2" opacity="0.65"')
svg = svg.replace('stroke="#1D1208" stroke-width="4.0"', 'stroke="#382414" stroke-width="2.2" opacity="0.65"')
svg = svg.replace('stroke="#120A04" stroke-width="4.0"', 'stroke="#2C1A0E" stroke-width="2.2" opacity="0.65"')

with open("scratch/test_softer_crevices.svg", "w") as f:
    f.write(svg)

out_png = render_svg("scratch/test_softer_crevices.svg", "scratch/test_softer_crevices.png")
evaluate_fidelity(out_png)
