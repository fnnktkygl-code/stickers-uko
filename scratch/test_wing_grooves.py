import re
import cv2
import numpy as np
import subprocess
import os

with open("scratch/test_eye_v3.svg") as f:
    svg = f.read()

# 1. Shift cranial highlight center to 205, 78
svg = re.sub(r'<ellipse cx="225" cy="85" rx="105" ry="55" fill="url\(#cranialHl\)" />',
             '<ellipse cx="205" cy="78" rx="95" ry="48" fill="url(#cranialHl)" />', svg)

# 2. Add wing seam grooves in clipped overlays
wing_grooves = """    <!-- Subtle Wing Seams (Flush Against Porcelain Flanks) -->
    <path d="M 110 220 C 114 270, 116 320, 126 370" stroke="#8A7664" stroke-width="3.5" opacity="0.25" fill="none" stroke-linecap="round" />
    <path d="M 390 220 C 396 270, 396 320, 386 370" stroke="#584232" stroke-width="3.5" opacity="0.30" fill="none" stroke-linecap="round" />"""

# Insert before Facial Cheek Volumes
svg = re.sub(r'<!-- Facial Cheek Volumes -->', wing_grooves + "\n\n    <!-- Facial Cheek Volumes -->", svg)

with open("scratch/test_wings.svg", "w") as f:
    f.write(svg)

cmd = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "--headless", "--disable-gpu", "--screenshot=scratch/test_wings.png",
    "--window-size=512,512", "--default-background-color=00000000",
    f"file://{os.path.abspath('scratch/test_wings.svg')}"
]
subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

from scripts.benchmark_owluko_fidelity import evaluate_fidelity
res = evaluate_fidelity("scratch/test_wings.png", title="AUDIT: test_wings.svg")
