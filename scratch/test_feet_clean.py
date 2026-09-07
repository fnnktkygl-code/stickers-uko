import sys
sys.path.append(".")
from scripts.benchmark_owluko_fidelity import render_svg, evaluate_fidelity

with open("scratch/test_tune_lighting.svg", "r") as f:
    svg = f.read()

# Remove the base shadow rectangles
svg = svg.replace('<path d="M 156 460 C 156 448, 226 448, 226 460 L 235 491 L 156 491 Z" fill="#423022" />', '')
svg = svg.replace('<path d="M 276 460 C 276 448, 353 448, 353 460 L 353 491 L 276 491 Z" fill="#2E1E12" />', '')

with open("scratch/test_feet_clean.svg", "w") as f:
    f.write(svg)

out_png = render_svg("scratch/test_feet_clean.svg", "scratch/test_feet_clean.png")
evaluate_fidelity(out_png)
