import cv2
import numpy as np

ref = cv2.imread("mascots/owluko/owluko_master_exact_512.png")
ref_gray = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)

# In rows 200, 240, 280, 320, 360, 400:
# Print horizontal profile from x=85 to x=180
print("Left Flank horizontal luminance profiles in reference:")
for y in range(200, 410, 30):
    row_vals = [ref_gray[y, x] for x in range(95, 175, 4)]
    # find where the valley/ridge is
    min_x = 95 + 4 * np.argmin(row_vals)
    max_x = 95 + 4 * np.argmax(row_vals)
    print(f"y={y}: min at x={min_x} (val={min(row_vals)}), max at x={max_x} (val={max(row_vals)}), vals={[int(v) for v in row_vals]}")
