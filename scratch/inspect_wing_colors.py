import cv2
import numpy as np

p4 = cv2.imread('scratch/panel_4_aligned.png')
# Extract pixels of the waving wing: x in [730, 1024], y in [150, 750]
crop = p4[150:750, 730:1024]
# Find colors:
# Non-white pixels
mask = np.mean(crop, axis=2) < 250
colors = crop[mask]
print("Wing BGR min:", colors.min(axis=0), "max:", colors.max(axis=0), "mean:", colors.mean(axis=0))
# Colors in RGB:
rgb = colors[:, ::-1]
print("Wing RGB mean:", rgb.mean(axis=0))
# Base shading: darkest non-background pixels:
darkest = rgb[np.argmin(np.mean(rgb, axis=1))]
lightest = rgb[np.argmax(np.mean(rgb, axis=1))]
print("Wing darkest RGB:", darkest, "lightest RGB:", lightest)
