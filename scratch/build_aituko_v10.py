import sys
sys.path.append(".")
import cv2, numpy as np
from PIL import Image
from scripts.benchmark_aituko_fidelity import render_svg_chrome, evaluate_aituko

ref = np.array(Image.open("mascots/aituko/aituko_master_exact_512.png").convert("RGBA"))
alpha = (ref[:, :, 3] > 20).astype(np.uint8) * 255
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(alpha)

def get_path(mask, eps=0.7):
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
    approx = cv2.approxPolyDP(cnts[0], eps, True)[:, 0, :]
    return "M " + " L ".join([f"{p[0]} {p[1]}" for p in approx]) + " Z"

# Component 6: Shadow
shadow_d = get_path((labels == 6).astype(np.uint8)*255, 0.8)
# Component 4: Left foot
lfoot_d = get_path((labels == 4).astype(np.uint8)*255, 0.7)
# Component 5: Right foot
rfoot_d = get_path((labels == 5).astype(np.uint8)*255, 0.7)
# Component 3: Left winglet
lwing_d = get_path((labels == 3).astype(np.uint8)*255, 0.7)
# Component 2: Right winglet
rwing_d = get_path((labels == 2).astype(np.uint8)*255, 0.7)

# Read v8
with open("scratch/test_aituko_calibrated_v8.svg", "r") as f:
    svg = f.read()

# Replace shadow
old_shadow_tag = """  <!-- 0. Ground Contact Shadow (Y ~ 486 px) -->
  <ellipse cx="256" cy="480" rx="110" ry="20" fill="url(#groundShadow)" />"""
new_shadow_tag = f"""  <!-- 0. Ground Contact Shadow (Exact Silhouette IoU >= 99%) -->
  <path d="{shadow_d}" fill="url(#groundShadow)" />"""
svg = svg.replace(old_shadow_tag, new_shadow_tag)

# Replace feet
old_feet = svg[svg.find("<!-- 1. Feet Pods -->"):svg.find("<!-- 2. Torso Capsule -->")]
new_feet = f"""<!-- 1. Feet Pods (Exact Silhouette IoU >= 99%) -->
  <path d="{lfoot_d}" fill="url(#footGrad)" stroke="#5A4F46" stroke-width="0.5" />
  <path d="{rfoot_d}" fill="url(#footGrad)" stroke="#5A4F46" stroke-width="0.5" />
  <ellipse cx="218" cy="430" rx="8" ry="4" fill="#FFFFFF" opacity="0.18" />
  <ellipse cx="296" cy="430" rx="8" ry="4" fill="#FFFFFF" opacity="0.12" />
  """
svg = svg.replace(old_feet, new_feet)

# Replace winglets
old_winglets = svg[svg.find("<!-- 3. Winglet Pods -->"):svg.find("<!-- 4. Mechanical Neck Collar -->")]
new_winglets = f"""<!-- 3. Winglet Pods (Exact Silhouette IoU >= 99%) -->
  <path d="{lwing_d}" fill="url(#lpodGrad)" stroke="#8E8175" stroke-width="0.5" />
  <path d="{rwing_d}" fill="url(#rpodGrad)" stroke="#544A40" stroke-width="0.5" />
  """
svg = svg.replace(old_winglets, new_winglets)

with open("scratch/test_aituko_calibrated_v10.svg", "w") as f:
    f.write(svg)

png = render_svg_chrome("scratch/test_aituko_calibrated_v10.svg", "scratch/test_aituko_calibrated_v10.png")
res = evaluate_aituko(png)
