import os, sys, subprocess, re, cv2, numpy as np
from PIL import Image

def run_test():
    with open('mascots/owluko/owluko_master_exact_512.svg', 'r') as f:
        orig = f.read()

    # Build the updated SVG
    # 1. Defs updates:
    # Replace amberEyeL, amberEyeR, pupilGradL, pupilGradR, eyelidHoodL, eyelidHoodR, eyeShadow, beakGrad, beakTipShadow
    new_defs = """
    <!-- Left Amber Iris (Glassy spherical bowl) -->
    <linearGradient id="amberEyeL" x1="25%" y1="10%" x2="75%" y2="100%">
      <stop offset="0%" stop-color="#421C04" />
      <stop offset="35%" stop-color="#66330C" />
      <stop offset="65%" stop-color="#B27522" />
      <stop offset="85%" stop-color="#EAA640" />
      <stop offset="100%" stop-color="#D08826" />
    </linearGradient>

    <!-- Right Amber Iris (Directional caustic towards right) -->
    <linearGradient id="amberEyeR" x1="15%" y1="15%" x2="85%" y2="85%">
      <stop offset="0%" stop-color="#381602" />
      <stop offset="30%" stop-color="#55280A" />
      <stop offset="60%" stop-color="#965C18" />
      <stop offset="82%" stop-color="#DB922C" />
      <stop offset="100%" stop-color="#EDA840" />
    </linearGradient>

    <!-- Translucent Warm Espresso Pupils -->
    <radialGradient id="pupilGradL" cx="50%" cy="45%" r="50%">
      <stop offset="0%" stop-color="#280C01" />
      <stop offset="65%" stop-color="#4A1E05" />
      <stop offset="100%" stop-color="#6B300C" stop-opacity="0" />
    </radialGradient>
    <radialGradient id="pupilGradR" cx="45%" cy="45%" r="50%">
      <stop offset="0%" stop-color="#220A01" />
      <stop offset="65%" stop-color="#3E1703" />
      <stop offset="100%" stop-color="#5A2406" stop-opacity="0" />
    </radialGradient>

    <!-- Left Porcelain Eyelid Hood (Spherical Dome) -->
    <linearGradient id="eyelidHoodL" x1="35%" y1="0%" x2="65%" y2="100%">
      <stop offset="0%" stop-color="#FFFDF9" />
      <stop offset="45%" stop-color="#F7EEE3" />
      <stop offset="78%" stop-color="#E0C6B0" />
      <stop offset="100%" stop-color="#C5A58D" />
    </linearGradient>

    <!-- Right Porcelain Eyelid Hood -->
    <linearGradient id="eyelidHoodR" x1="25%" y1="0%" x2="75%" y2="100%">
      <stop offset="0%" stop-color="#EFE1D2" />
      <stop offset="45%" stop-color="#DAC0A9" />
      <stop offset="78%" stop-color="#BD9C84" />
      <stop offset="100%" stop-color="#A2826A" />
    </linearGradient>

    <!-- Eyelid Cast Shadow on Eyeball -->
    <linearGradient id="eyeShadow" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#120501" stop-opacity="0.82" />
      <stop offset="55%" stop-color="#381504" stop-opacity="0.35" />
      <stop offset="100%" stop-color="#662C05" stop-opacity="0" />
    </linearGradient>

    <!-- Seamless Volumetric Porcelain Beak Gradient -->
    <linearGradient id="beakGrad" x1="22%" y1="10%" x2="78%" y2="90%">
      <stop offset="0%" stop-color="#FFF6EC" />
      <stop offset="25%" stop-color="#ECDC handle" stop-color="#EDDEC $\rightarrow$ #EDDECE" />
    </linearGradient>
"""
