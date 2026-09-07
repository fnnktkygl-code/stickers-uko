import bpy
import json
import numpy as np
import cv2

# Load contours
with open("scratch/owluko_contours.json", "r") as f:
    data = json.load(f)

# The total height of the mascot in 3D:
# Top pole is data['top_pole_z'] = (450 - 40) / 200 = 2.05
# Feet bottom is Z = (450 - 489) / 200 = -0.195
# Total 3D height = 2.05 - (-0.195) = 2.245 units.
# In 512x512 canvas:
# 2.245 units must occupy exactly 450 - 40 = 449 pixels = (449 / 512) of the camera frame.
# Therefore, ortho_scale = 2.245 / (449.0 / 512.0) = 2.560 units!
# And the vertical center of the mascot in 3D:
# Z_mid = (2.05 + (-0.195)) / 2.0 = 0.9275 units!
# But in canvas, mascot center is Y = (40 + 489) / 2.0 = 264.5 pixels (which is 8.5 pixels below canvas center 256.0).
# In ortho camera, shifting camera Z by delta_z shifts the image.
# Let's compute exact Z_cam:
# Canvas Y=256 corresponds to Z_cam.
# Mascot top at Y=40 is 216 pixels above canvas center.
# Mascot bottom at Y=489 is 233 pixels below canvas center.
# In 3D: Z_top = 2.05, Z_bot = -0.195.
# If ortho_scale = 2.560:
# 1 pixel = 2.560 / 512.0 = 0.005 units in 3D.
# Top at Y=40: Z_cam + (256 - 40) * 0.005 = Z_cam + 216 * 0.005 = Z_cam + 1.08 = 2.05 -> Z_cam = 0.970!
# Bottom at Y=489: Z_cam - (489 - 256) * 0.005 = Z_cam - 233 * 0.005 = Z_cam - 1.165 = 0.970 - 1.165 = -0.195! EXACT MATCH!

print("Calculated Ortho Camera Parameters:")
print("ortho_scale =", 2.560)
print("Z_cam =", 0.970)
