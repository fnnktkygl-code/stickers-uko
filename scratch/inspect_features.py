import cv2
import numpy as np
from PIL import Image

ref = np.array(Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA"))
vec = np.array(Image.open("scratch/temp_svg_rendered.png").convert("RGBA"))

def save_crop_comparison(name, y1, y2, x1, x2):
    r_crop = ref[y1:y2, x1:x2]
    v_crop = vec[y1:y2, x1:x2]
    diff = np.abs(r_crop[:, :, :3].astype(int) - v_crop[:, :, :3].astype(int)).astype(np.uint8)
    combined = np.hstack([r_crop[:, :, :3], v_crop[:, :, :3], diff])
    cv2.imwrite(f"scratch/inspect_{name}.png", cv2.cvtColor(combined, cv2.COLOR_RGB2BGR))
    print(f"Saved scratch/inspect_{name}.png (ref | vec | diff)")

save_crop_comparison("left_eye", 130, 190, 160, 235)
save_crop_comparison("right_eye", 130, 190, 280, 345)
save_crop_comparison("beak", 160, 230, 240, 272)
save_crop_comparison("left_foot", 445, 495, 150, 240)
save_crop_comparison("right_foot", 445, 495, 270, 360)
