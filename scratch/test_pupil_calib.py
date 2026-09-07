import sys
sys.path.append(".")
from scripts.benchmark_owluko_fidelity import render_svg, evaluate_fidelity

with open("scratch/test_softer_crevices.svg", "r") as f:
    svg = f.read()

# Update pupil gradient from #080402 -> #180A03 -> #2C1204 to #221208 -> #321C0E -> #422818
svg = svg.replace(
    '<radialGradient id="pupilGrad" cx="45%" cy="40%" r="55%">\n      <stop offset="0%" stop-color="#080402" />\n      <stop offset="70%" stop-color="#180A03" />\n      <stop offset="100%" stop-color="#2C1204" />\n    </radialGradient>',
    '<radialGradient id="pupilGrad" cx="45%" cy="40%" r="55%">\n      <stop offset="0%" stop-color="#24140A" />\n      <stop offset="70%" stop-color="#352014" />\n      <stop offset="100%" stop-color="#462C1C" />\n    </radialGradient>'
)

# Remove beak dark outline stroke
svg = svg.replace(
    'stroke="#4A3220" stroke-width="1.2"',
    'stroke="none"'
)

with open("scratch/test_pupil_calib.svg", "w") as f:
    f.write(svg)

out_png = render_svg("scratch/test_pupil_calib.svg", "scratch/test_pupil_calib.png")
evaluate_fidelity(out_png)
