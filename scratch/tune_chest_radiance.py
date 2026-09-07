import sys
sys.path.append(".")
from scripts.benchmark_owluko_fidelity import render_svg, evaluate_fidelity

with open("scratch/test_pod_feet.svg", "r") as f:
    svg = f.read()

# Update bodyGrad to true bright porcelain
svg = svg.replace(
    '<stop offset="38%" stop-color="#D4C9BD" />\n      <stop offset="60%" stop-color="#BAABA0" />\n      <stop offset="82%" stop-color="#9E8C7F" />\n      <stop offset="100%" stop-color="#685648" />',
    '<stop offset="38%" stop-color="#DFD5CB" />\n      <stop offset="60%" stop-color="#C8BCB1" />\n      <stop offset="82%" stop-color="#A59587" />\n      <stop offset="100%" stop-color="#726052" />'
)

# Strengthen chest soft illumination
svg = svg.replace(
    '<radialGradient id="chestHl" cx="44%" cy="48%" r="44%">\n      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.18" />\n      <stop offset="50%" stop-color="#ECE5DC" stop-opacity="0.06" />\n      <stop offset="100%" stop-color="#DED6CE" stop-opacity="0" />\n    </radialGradient>',
    '<radialGradient id="chestHl" cx="42%" cy="45%" r="48%">\n      <stop offset="0%" stop-color="#FFF5EC" stop-opacity="0.38" />\n      <stop offset="55%" stop-color="#F2E6DC" stop-opacity="0.15" />\n      <stop offset="100%" stop-color="#DED6CE" stop-opacity="0" />\n    </radialGradient>'
)
svg = svg.replace(
    '<ellipse cx="242" cy="280" rx="108" ry="82" fill="url(#chestHl)" />',
    '<ellipse cx="236" cy="255" rx="125" ry="95" fill="url(#chestHl)" />'
)

with open("scratch/test_chest_radiance.svg", "w") as f:
    f.write(svg)

out_png = render_svg("scratch/test_chest_radiance.svg", "scratch/test_chest_radiance.png")
evaluate_fidelity(out_png)
