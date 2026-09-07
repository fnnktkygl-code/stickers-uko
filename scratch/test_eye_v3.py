import re
import cv2
import numpy as np
import subprocess
import os

with open("scratch/test_calibrated_v2.svg") as f:
    svg = f.read()

# Define new Eye Gradients:
# Notice in linearGradient from Y=140 to Y=178 (y1="10%", y2="90%")
new_eye_grads = """    <!-- Left Eye Amber Gradient (Continuous Caustic Flow) -->
    <linearGradient id="amberEyeL" x1="20%" y1="10%" x2="40%" y2="95%">
      <stop offset="0%" stop-color="#3A1C04" />
      <stop offset="40%" stop-color="#552B05" />
      <stop offset="65%" stop-color="#9C5E16" />
      <stop offset="85%" stop-color="#DC9228" />
      <stop offset="100%" stop-color="#F2B852" />
    </linearGradient>

    <!-- Right Eye Amber Gradient (Continuous Caustic Flow) -->
    <linearGradient id="amberEyeR" x1="20%" y1="10%" x2="75%" y2="95%">
      <stop offset="0%" stop-color="#321804" />
      <stop offset="40%" stop-color="#462204" />
      <stop offset="65%" stop-color="#8E5210" />
      <stop offset="85%" stop-color="#D07C1C" />
      <stop offset="100%" stop-color="#EAA236" />
    </linearGradient>

    <!-- Soft Cornea Pupil Core -->
    <radialGradient id="pupilCoreL" cx="50%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#522A04" />
      <stop offset="70%" stop-color="#552B05" stop-opacity="0.9" />
      <stop offset="100%" stop-color="#552B05" stop-opacity="0" />
    </radialGradient>

    <radialGradient id="pupilCoreR" cx="50%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#381B02" />
      <stop offset="70%" stop-color="#3A1C04" stop-opacity="0.9" />
      <stop offset="100%" stop-color="#3A1C04" stop-opacity="0" />
    </radialGradient>"""

svg = re.sub(r'<!-- Left Eye Radial -->.*?<!-- Pupil Gradient -->\s*<radialGradient id="pupilGrad".*?</radialGradient>', new_eye_grads, svg, flags=re.DOTALL)

# Now update the eye elements:
new_eyes = """  <!-- 3. Eye Sockets & Amber Eyes (Smooth Continuous Porcelain Depression & Glowing Amber Crescent) -->
  <!-- Left Eye -->
  <g id="left_eye">
    <!-- Soft Socket Ambient Shadow -->
    <ellipse cx="196" cy="159" rx="27" ry="19.5" fill="#422510" opacity="0.35" />
    <!-- Iris Base -->
    <ellipse cx="196" cy="158" rx="24.5" ry="17.5" fill="url(#amberEyeL)" />
    <!-- Soft Pupil Core (Centered at 197, 149) -->
    <ellipse cx="197" cy="149" rx="14" ry="7.5" fill="url(#pupilCoreL)" />
  </g>

  <!-- Right Eye -->
  <g id="right_eye">
    <!-- Soft Socket Ambient Shadow -->
    <ellipse cx="308" cy="159" rx="27.5" ry="19.5" fill="#351B0A" opacity="0.40" />
    <!-- Iris Base -->
    <ellipse cx="308" cy="158" rx="25" ry="17.5" fill="url(#amberEyeR)" />
    <!-- Soft Pupil Core (Centered at 307, 149) -->
    <ellipse cx="307" cy="149" rx="14" ry="7.5" fill="url(#pupilCoreR)" />
    <!-- Right Eye Outer Amber Caustic Flare (x=330, y=166) -->
    <ellipse cx="329" cy="166" rx="8" ry="10" fill="#F8B84C" opacity="0.45" />
  </g>"""

svg = re.sub(r'<!-- 3\. Eye Sockets & Amber Eyes.*?<!-- Right Eye -->\s*<g id="right_eye">.*?</g>', new_eyes, svg, flags=re.DOTALL)

with open("scratch/test_eye_v3.svg", "w") as f:
    f.write(svg)

# Render and test
cmd = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "--headless", "--disable-gpu", "--screenshot=scratch/test_eye_v3.png",
    "--window-size=512,512", "--default-background-color=00000000",
    f"file://{os.path.abspath('scratch/test_eye_v3.svg')}"
]
subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

from scripts.benchmark_owluko_fidelity import evaluate_fidelity
res = evaluate_fidelity("scratch/test_eye_v3.png", title="AUDIT: test_eye_v3.svg")
