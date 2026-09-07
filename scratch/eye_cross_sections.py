import cv2
import numpy as np

ref = cv2.imread("mascots/owluko/owluko_master_exact_512.png")
# Convert to RGB
ref = cv2.cvtColor(ref, cv2.COLOR_BGR2RGB)

# Left eye center: (196, 158)
# Let's inspect along a vertical line through left eye: x = 196, y in [135, 185]
print("Left Eye vertical line x=196:")
for y in range(138, 182, 2):
    print(f"y={y}: RGB={ref[y, 196].tolist()}")

# Left eye horizontal line y=158, x in [165, 228]
print("\nLeft Eye horizontal line y=158:")
for x in range(168, 226, 3):
    print(f"x={x}: RGB={ref[158, x].tolist()}")

# Right Eye vertical line x=308, y in [138, 182]
print("\nRight Eye vertical line x=308:")
for y in range(138, 182, 2):
    print(f"y={y}: RGB={ref[y, 308].tolist()}")

# Right eye horizontal line y=158, x in [278, 338]
print("\nRight Eye horizontal line y=158:")
for x in range(280, 338, 3):
    print(f"x={x}: RGB={ref[158, x].tolist()}")
