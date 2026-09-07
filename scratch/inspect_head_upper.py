import cv2
import numpy as np

ref = cv2.imread("mascots/owluko/owluko_master_exact_512.png")
ref_gray = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)

print("Head Upper vertical luminance profile at center x=256:")
for y in range(45, 130, 10):
    print(f"y={y}: val={ref_gray[y, 256]}, RGB={ref[y, 256].tolist()}")

print("\nHead Upper horizontal luminance profile at y=85 (cranial dome):")
for x in range(160, 360, 15):
    print(f"x={x}: val={ref_gray[85, x]}, RGB={ref[85, x].tolist()}")
