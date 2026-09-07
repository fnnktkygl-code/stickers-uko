import sys
sys.path.append(".")
from scripts.benchmark_owluko_fidelity import render_svg, evaluate_fidelity

with open("scratch/test_pod_feet.svg", "r") as f:
    svg = f.read()

# Replace full socket ellipse with upper brow shadow arch
old_left_eye = """  <!-- Left Eye -->
  <g id="left_eye">
    <!-- Brow Crevice / Socket Rim -->
    <ellipse cx="196" cy="159" rx="27" ry="19.5" fill="#3D2817" opacity="0.65" />
    <ellipse cx="196" cy="159" rx="25" ry="18" fill="#1C0C02" />
    <!-- Amber Iris -->
    <ellipse cx="196" cy="159" rx="24" ry="17" fill="url(#amberEyeL)" />
    <!-- Pupil -->
    <ellipse cx="197" cy="155" rx="14" ry="11.5" fill="url(#pupilGrad)" />
  </g>"""

new_left_eye = """  <!-- Left Eye -->
  <g id="left_eye">
    <!-- Amber Iris (Full lower ellipse) -->
    <ellipse cx="196" cy="160" rx="25" ry="18" fill="url(#amberEyeL)" />
    <!-- Obsidian Pupil (Upper Center) -->
    <ellipse cx="197" cy="152" rx="15" ry="11" fill="url(#pupilGrad)" />
    <!-- Upper Brow Socket Shadow Arc (ONLY at top brow) -->
    <path d="M 171 158 C 173 140, 220 140, 221 158 C 218 143, 175 143, 171 158 Z" fill="#201004" opacity="0.85" />
    <path d="M 168 158 C 172 138, 222 138, 224 158" stroke="#3D2817" stroke-width="2.5" fill="none" opacity="0.45" />
  </g>"""

old_right_eye = """  <!-- Right Eye -->
  <g id="right_eye">
    <!-- Brow Crevice / Socket Rim -->
    <ellipse cx="309" cy="159" rx="28.5" ry="19.5" fill="#301A0D" opacity="0.75" />
    <ellipse cx="309" cy="159" rx="26.5" ry="18" fill="#180A02" />
    <!-- Amber Iris -->
    <ellipse cx="309" cy="159" rx="25.5" ry="17" fill="url(#amberEyeR)" />
    <!-- Pupil -->
    <ellipse cx="307" cy="155" rx="14" ry="11.5" fill="url(#pupilGrad)" />
  </g>"""

new_right_eye = """  <!-- Right Eye -->
  <g id="right_eye">
    <!-- Amber Iris (Full lower ellipse) -->
    <ellipse cx="309" cy="160" rx="26.5" ry="18" fill="url(#amberEyeR)" />
    <!-- Obsidian Pupil (Upper Center) -->
    <ellipse cx="306" cy="152" rx="15" ry="11" fill="url(#pupilGrad)" />
    <!-- Upper Brow Socket Shadow Arc (ONLY at top brow) -->
    <path d="M 283 158 C 285 140, 334 140, 335 158 C 332 143, 287 143, 283 158 Z" fill="#180A02" opacity="0.85" />
    <path d="M 280 158 C 284 138, 337 138, 338 158" stroke="#301A0D" stroke-width="2.5" fill="none" opacity="0.45" />
  </g>"""

svg = svg.replace(old_left_eye, new_left_eye)
svg = svg.replace(old_right_eye, new_right_eye)

with open("scratch/test_eye_rim_fix.svg", "w") as f:
    f.write(svg)

out_png = render_svg("scratch/test_eye_rim_fix.svg", "scratch/test_eye_rim_fix.png")
evaluate_fidelity(out_png)
