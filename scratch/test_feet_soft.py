import re
import cv2
import numpy as np
import subprocess
import os

with open("scratch/test_eye_v3.svg") as f:
    svg = f.read()

# Let's test feet without the harsh stroked lines
# In 3D CGI: the feet are smooth porcelain pods
# Let's see what happens if we remove the crevice strokes and ground contact strokes,
# and use soft toe gradients
feet_soft = """    <!-- Grounded Feet with 3 Anatomical Rounded Toes (Smooth Seamless Shading) -->
    <g id="feet">
      <!-- Left Foot Base Shadow -->
      <ellipse cx="195" cy="472" rx="36" ry="16" fill="#8A6E58" opacity="0.30" />

      <!-- Left Foot 3 Rounded Toe Specular Highlights -->
      <ellipse cx="168" cy="474" rx="10" ry="10" fill="#E8DDD1" opacity="0.50" />
      <ellipse cx="194" cy="467" rx="12" ry="12" fill="#FFF2E6" opacity="0.60" />
      <ellipse cx="220" cy="474" rx="10" ry="10" fill="#DFD2C4" opacity="0.50" />

      <!-- Soft Crevice Depth -->
      <ellipse cx="180" cy="478" rx="2.5" ry="8" fill="#4A3018" opacity="0.30" />
      <ellipse cx="206" cy="478" rx="2.5" ry="8" fill="#4A3018" opacity="0.30" />

      <!-- Right Foot Base Shadow -->
      <ellipse cx="316" cy="472" rx="36" ry="16" fill="#5E4330" opacity="0.35" />

      <!-- Right Foot 3 Rounded Toe Specular Highlights -->
      <ellipse cx="290" cy="474" rx="9" ry="9" fill="#C4B09C" opacity="0.40" />
      <ellipse cx="317" cy="467" rx="11" ry="11" fill="#D9C6B4" opacity="0.50" />
      <ellipse cx="341" cy="474" rx="9" ry="9" fill="#C8B5A2" opacity="0.40" />

      <!-- Soft Crevice Depth -->
      <ellipse cx="304" cy="478" rx="2.5" ry="8" fill="#382010" opacity="0.35" />
      <ellipse cx="330" cy="478" rx="2.5" ry="8" fill="#382010" opacity="0.35" />
    </g>"""

svg_soft = re.sub(r'<g id="feet">.*?</g>', feet_soft, svg, flags=re.DOTALL)

with open("scratch/test_feet_soft.svg", "w") as f:
    f.write(svg_soft)

cmd = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "--headless", "--disable-gpu", "--screenshot=scratch/test_feet_soft.png",
    "--window-size=512,512", "--default-background-color=00000000",
    f"file://{os.path.abspath('scratch/test_feet_soft.svg')}"
]
subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

from scripts.benchmark_owluko_fidelity import evaluate_fidelity
res = evaluate_fidelity("scratch/test_feet_soft.png", title="AUDIT: test_feet_soft.svg")
