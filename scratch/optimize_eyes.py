import sys, re
sys.path.append(".")
import numpy as np
import cv2
from PIL import Image
from scripts.benchmark_owluko_fidelity import compute_ssim_numpy, render_svg, evaluate_fidelity

ref_img = Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA")
ref = np.array(ref_img)

def test_eyes(lx, ly, lr, lpx, lpy, lpr, rx, ry, rr, rpx, rpy, rpr):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" style="background: transparent;">
  <defs>
    <!-- Left Eye Radial -->
    <radialGradient id="amberEyeL" cx="30%" cy="75%" r="70%">
      <stop offset="0%" stop-color="#FDE047" />
      <stop offset="25%" stop-color="#D99B26" />
      <stop offset="60%" stop-color="#8A4807" />
      <stop offset="88%" stop-color="#2D1302" />
      <stop offset="100%" stop-color="#150800" />
    </radialGradient>
    <!-- Right Eye Radial -->
    <radialGradient id="amberEyeR" cx="70%" cy="75%" r="70%">
      <stop offset="0%" stop-color="#FDE047" />
      <stop offset="25%" stop-color="#D99B26" />
      <stop offset="60%" stop-color="#8A4807" />
      <stop offset="88%" stop-color="#2D1302" />
      <stop offset="100%" stop-color="#150800" />
    </radialGradient>
    <!-- Pupil -->
    <radialGradient id="pupilGrad" cx="45%" cy="45%" r="50%">
      <stop offset="0%" stop-color="#080402" />
      <stop offset="80%" stop-color="#180A03" />
      <stop offset="100%" stop-color="#301505" />
    </radialGradient>
  </defs>

  <!-- Left Eye Socket -->
  <circle cx="{lx}" cy="{ly}" r="{lr+3.5}" fill="#3A281A" opacity="0.85" />
  <circle cx="{lx}" cy="{ly}" r="{lr+1.5}" fill="#1F0D02" />
  <circle cx="{lx}" cy="{ly}" r="{lr}" fill="url(#amberEyeL)" />
  <circle cx="{lpx}" cy="{lpy}" r="{lpr}" fill="url(#pupilGrad)" />
  <ellipse cx="{lx-5}" cy="{ly-6}" rx="3.5" ry="2.5" fill="#FFFFFF" opacity="0.9" />
  <circle cx="{lx+7}" cy="{ly+6}" r="1.5" fill="#FFFFFF" opacity="0.5" />

  <!-- Right Eye Socket -->
  <circle cx="{rx}" cy="{ry}" r="{rr+3.5}" fill="#3A281A" opacity="0.85" />
  <circle cx="{rx}" cy="{ry}" r="{rr+1.5}" fill="#1F0D02" />
  <circle cx="{rx}" cy="{ry}" r="{rr}" fill="url(#amberEyeR)" />
  <circle cx="{rpx}" cy="{rpy}" r="{rpr}" fill="url(#pupilGrad)" />
  <ellipse cx="{rx-6}" cy="{ry-6}" rx="3.5" ry="2.5" fill="#FFFFFF" opacity="0.9" />
  <circle cx="{rx+7}" cy="{ry+6}" r="1.5" fill="#FFFFFF" opacity="0.5" />
</svg>"""
    return svg

print("Optimization helper ready.")
