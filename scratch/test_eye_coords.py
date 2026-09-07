import sys
sys.path.append(".")
from scripts.benchmark_owluko_fidelity import render_svg, evaluate_fidelity

with open("scratch/test_rwing_fix.svg", "r") as f:
    svg = f.read()

# Update eye positions:
# Left eye: cx: 196 -> 191, cy: 159 -> 153
# Right eye: cx: 309 -> 312, cy: 159 -> 158
old_left = """  <!-- Left Eye -->
  <g id="left_eye">
    <!-- Brow Crevice / Socket Rim -->
    <ellipse cx="196" cy="159" rx="27" ry="19.5" fill="#3D2817" opacity="0.65" />
    <ellipse cx="196" cy="159" rx="25" ry="18" fill="#1C0C02" />
    <!-- Amber Iris -->
    <ellipse cx="196" cy="159" rx="24" ry="17" fill="url(#amberEyeL)" />
    <!-- Pupil -->
    <ellipse cx="197" cy="155" rx="14" ry="11.5" fill="url(#pupilGrad)" />
  </g>"""

new_left = """  <!-- Left Eye -->
  <g id="left_eye">
    <!-- Brow Crevice / Socket Rim -->
    <ellipse cx="191" cy="153" rx="26" ry="18.5" fill="#3D2817" opacity="0.65" />
    <ellipse cx="191" cy="153" rx="24" ry="17" fill="#1C0C02" />
    <!-- Amber Iris -->
    <ellipse cx="191" cy="153" rx="23" ry="16" fill="url(#amberEyeL)" />
    <!-- Pupil -->
    <ellipse cx="193" cy="149" rx="13.5" ry="10.5" fill="url(#pupilGrad)" />
  </g>"""

old_right = """  <!-- Right Eye -->
  <g id="right_eye">
    <!-- Brow Crevice / Socket Rim -->
    <ellipse cx="309" cy="159" rx="28.5" ry="19.5" fill="#301A0D" opacity="0.75" />
    <ellipse cx="309" cy="159" rx="26.5" ry="18" fill="#180A02" />
    <!-- Amber Iris -->
    <ellipse cx="309" cy="159" rx="25.5" ry="17" fill="url(#amberEyeR)" />
    <!-- Pupil -->
    <ellipse cx="307" cy="155" rx="14" ry="11.5" fill="url(#pupilGrad)" />
  </g>"""

new_right = """  <!-- Right Eye -->
  <g id="right_eye">
    <!-- Brow Crevice / Socket Rim -->
    <ellipse cx="312" cy="158" rx="27.5" ry="19" fill="#301A0D" opacity="0.75" />
    <ellipse cx="312" cy="158" rx="25.5" ry="17.5" fill="#180A02" />
    <!-- Amber Iris -->
    <ellipse cx="312" cy="158" rx="24.5" ry="16.5" fill="url(#amberEyeR)" />
    <!-- Pupil -->
    <ellipse cx="310" cy="154" rx="13.5" ry="10.5" fill="url(#pupilGrad)" />
  </g>"""

svg = svg.replace(old_left, new_left)
svg = svg.replace(old_right, new_right)

with open("scratch/test_eye_coords.svg", "w") as f:
    f.write(svg)

out_png = render_svg("scratch/test_eye_coords.svg", "scratch/test_eye_coords.png")
evaluate_fidelity(out_png)
