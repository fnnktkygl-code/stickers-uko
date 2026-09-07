import subprocess
import cv2
import numpy as np
import re

with open("scratch/test_rwing_fix.svg") as f:
    full_svg = f.read()

# Let's inspect the rendered PNG at 465, 255:
# Why would Chrome have [224, 211, 201, 255]?
# Notice 224, 211, 201 is the background color or body color?
# BodyGrad at (255, 465):
# x1="34%", y1="5%", x2="65%", y2="90%"
# at (255, 465), y is near 90%! The color at 90% is between #A59587 and #726052 (around 140, 120, 100).
# BUT [224, 211, 201] is #E0D3C9! That's CHEST color!
# How could chest color be at y=465?
# Let's check where [224, 211, 201] exists in the whole image!
vec = cv2.imread("scratch/temp_svg_rendered.png", cv2.IMREAD_UNCHANGED)
print("vec shape:", vec.shape)
print("Vec at (y=465, x=255) BGRA:", vec[465, 255])
# Let's find all pixels in vec that have color close to [224, 211, 201]
diff = np.linalg.norm(vec[:, :, :3].astype(float) - np.array([201, 211, 224]), axis=2)
print("Min diff across image:", diff.min())
ys, xs = np.where(diff < 5)
print(f"Number of pixels with diff < 5: {len(ys)}")
print(f"Y range: [{ys.min()}, {ys.max()}], X range: [{xs.min()}, {xs.max()}]")
