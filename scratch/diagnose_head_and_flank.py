import cv2
import numpy as np
from PIL import Image

ref_img = Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA")
vec_img = Image.open("scratch/test_eye_v3.png").convert("RGBA")

ref = np.array(ref_img)
vec = np.array(vec_img)

ref_alpha = ref[:, :, 3] > 20
vec_alpha = vec[:, :, 3] > 20
inter = ref_alpha & vec_alpha

ref_gray = cv2.cvtColor(ref[:, :, :3], cv2.COLOR_RGB2GRAY).astype(np.float64)
vec_gray = cv2.cvtColor(vec[:, :, :3], cv2.COLOR_RGB2GRAY).astype(np.float64)

# Mean luminance difference across whole foreground
diff_gray = vec_gray - ref_gray
print(f"Overall Foreground: Mean Gray Diff (vec - ref) = {diff_gray[inter].mean():.2f}")
print(f"Overall Foreground: Mean Abs Diff = {np.abs(diff_gray)[inter].mean():.2f}")

# Head Upper: Y in [40, 130], X in [150, 360]
hu_mask = inter[40:130, 150:360]
hu_diff = diff_gray[40:130, 150:360][hu_mask]
print(f"\nHead Upper (40-130, 150-360):")
print(f"  Mean Gray Diff (vec - ref) = {hu_diff.mean():.2f}")
print(f"  Ref Mean Gray = {ref_gray[40:130, 150:360][hu_mask].mean():.2f}, Vec Mean Gray = {vec_gray[40:130, 150:360][hu_mask].mean():.2f}")

# Left Flank: Y in [180, 440], X in [80, 180]
lf_mask = inter[180:440, 80:180]
lf_diff = diff_gray[180:440, 80:180][lf_mask]
print(f"\nLeft Flank (180-440, 80-180):")
print(f"  Mean Gray Diff (vec - ref) = {lf_diff.mean():.2f}")
print(f"  Ref Mean Gray = {ref_gray[180:440, 80:180][lf_mask].mean():.2f}, Vec Mean Gray = {vec_gray[180:440, 80:180][lf_mask].mean():.2f}")

# Right Flank: Y in [180, 440], X in [330, 430]
rf_mask = inter[180:440, 330:430]
rf_diff = diff_gray[180:440, 330:430][rf_mask]
print(f"\nRight Flank (180-440, 330-430):")
print(f"  Mean Gray Diff (vec - ref) = {rf_diff.mean():.2f}")
print(f"  Ref Mean Gray = {ref_gray[180:440, 330:430][rf_mask].mean():.2f}, Vec Mean Gray = {vec_gray[180:440, 330:430][rf_mask].mean():.2f}")
