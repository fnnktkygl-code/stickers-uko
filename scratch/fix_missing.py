import re

with open("scripts/build_flawless_meoweko_idle.py", "r") as f:
    content = f.read()

missing_functions = """
import cv2
import numpy as np
import math
from PIL import Image, ImageDraw, ImageFont

def load_and_despill_reference_video():
    ref_path = "mascots/luneko/luneko_idle.mp4"
    cap = cv2.VideoCapture(ref_path)
    raw_frames = []
    while True:
        ret, frame = cap.read()
        if not ret: break
        raw_frames.append(frame)
    cap.release()
    
    clean_frames = []
    for frame in raw_frames:
        b, g, r = frame[:,:,0].astype(np.float32), frame[:,:,1].astype(np.float32), frame[:,:,2].astype(np.float32)
        green_excess = np.maximum(0.0, g - np.maximum(r, b))
        is_bg = (g > 150) & (r < 75) & (b < 75) & (green_excess > 70)
        alpha = (~is_bg).astype(np.uint8) * 255
        alpha = cv2.morphologyEx(alpha, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
        bgr_clean = frame.copy()
        rgba = cv2.cvtColor(bgr_clean, cv2.COLOR_BGR2RGBA)
        rgba[:,:,3] = alpha
        
        # Scale & center exactly as standard
        crop_y, crop_h = 271, 1019-271
        crop_x, crop_w = 55, 623-55
        if crop_y + crop_h > rgba.shape[0]: crop_h = rgba.shape[0] - crop_y
        if crop_x + crop_w > rgba.shape[1]: crop_w = rgba.shape[1] - crop_x
        
        crop = rgba[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
        TARGET_H = 450.0
        scale = TARGET_H / float(crop.shape[0])
        nw = int(round(crop.shape[1] * scale))
        nh = int(round(TARGET_H))
        scaled = cv2.resize(crop, (nw, nh), interpolation=cv2.INTER_LANCZOS4)
        
        canvas = np.zeros((512, 512, 4), dtype=np.uint8)
        px = (512 - nw) // 2
        py = 491 - nh
        canvas[py:py+nh, px:px+nw] = scaled
        canvas[492:, :, 3] = 0 # zero shadow
        
        clean_frames.append(Image.fromarray(canvas))
    return clean_frames

def resample_to_120_frames(frames_96):
    n_in = len(frames_96)
    n_out = 120
    resampled = []
    for i in range(n_out):
        t = (i / float(n_out)) * n_in
        idx0 = int(math.floor(t)) % n_in
        idx1 = (idx0 + 1) % n_in
        frac = t - math.floor(t)
        if frac < 0.05: resampled.append(frames_96[idx0])
        elif frac > 0.95: resampled.append(frames_96[idx1])
        else: resampled.append(Image.blend(frames_96[idx0], frames_96[idx1], frac))
    return resampled

def build_meoweko_2tier_master_board(frames_120):
    board = Image.new("RGBA", (1920, 1080), (11, 15, 23, 255))
    return board

def build_studio_trichroma_board(frame):
    board = Image.new("RGBA", (1536, 512), (11, 15, 23, 255))
    return board

"""

content = content.replace("def run_meoweko_idle_production():", missing_functions + "\\ndef run_meoweko_idle_production():")

with open("scripts/build_flawless_meoweko_idle.py", "w") as f:
    f.write(content)
