import sys
sys.path.append(".")
import cv2, numpy as np
from PIL import Image

# Let us extract the exact contours of left foot and right foot from mask
ref = np.array(Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA"))
alpha = ref[:, :, 3]

# Left foot mask
l_mask = np.zeros_like(alpha)
l_mask[435:495, 150:240] = (alpha[435:495, 150:240] > 20).astype(np.uint8) * 255
cnts_l, _ = cv2.findContours(l_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
approx_l = cv2.approxPolyDP(cnts_l[0], 0.7, True)[:, 0, :]

# Right foot mask
r_mask = np.zeros_like(alpha)
r_mask[435:495, 270:360] = (alpha[435:495, 270:360] > 20).astype(np.uint8) * 255
cnts_r, _ = cv2.findContours(r_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
approx_r = cv2.approxPolyDP(cnts_r[0], 0.7, True)[:, 0, :]

def pts_to_d(pts):
    return "M " + " L ".join([f"{p[0]} {p[1]}" for p in pts]) + " Z"

print("Left foot path:", pts_to_d(approx_l))
print("Right foot path:", pts_to_d(approx_r))

with open("scratch/owluko_feet_paths.txt", "w") as f:
    f.write(f"LEFT: {pts_to_d(approx_l)}\nRIGHT: {pts_to_d(approx_r)}\n")
