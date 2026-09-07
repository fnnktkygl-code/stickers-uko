import cv2
import numpy as np

ref = cv2.imread("mascots/owluko/owluko_master_exact_512.png")
ref_gray = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)

print("Right Flank horizontal luminance profiles in reference:")
for y in range(200, 410, 30):
    row_vals = [ref_gray[y, x] for x in range(330, 425, 4)]
    print(f"y={y}: vals={[int(v) for v in row_vals]}")
