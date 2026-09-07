import os
import glob
import cv2
import numpy as np
from PIL import Image

poses = [
    "01_waving", "02_celebrating", "03_ai_thinking", "04_error_404",
    "05_thumbs_up", "06_sleeping", "07_pointing", "08_searching",
    "09_loading", "10_idea", "11_security", "12_goodbye"
]

def clean_and_build(m_dir):
    print(f"Starting clean build for Inuko in {m_dir}...")
    for p in poses:
        p_dir = f"{m_dir}/{p}"
        vid = f"{p_dir}/looped_video.mp4"
        if not os.path.exists(vid):
            print(f"Skipping {p}, no video")
            continue
            
        temp_dir = f"{p_dir}/temp_frames"
        os.makedirs(temp_dir, exist_ok=True)
        
        cap = cv2.VideoCapture(vid)
        frames_rgba = []
        frame_idx = 0
        
        lower_green = np.array([30, 40, 40])
        upper_green = np.array([88, 255, 255])
        kernel = np.ones((3, 3), np.uint8)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            h, w, _ = frame.shape
            cropped = frame[:, 280:1000] if w == 1280 else frame
            
            hsv = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
            bg_mask = cv2.inRange(hsv, lower_green, upper_green)
            fg_mask = cv2.bitwise_not(bg_mask)
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
            
            alpha = fg_mask.astype(float) / 255.0
            alpha = cv2.GaussianBlur(alpha, (3, 3), 0)
            alpha = (alpha * 255).astype(np.uint8)
            
            b, g, r = cv2.split(cropped)
            max_rb = np.maximum(r, b)
            g_clean = np.where((g > max_rb) & (alpha < 250), max_rb, g)
            
            rgba = cv2.merge([b, g_clean, r, alpha])
            rgba = cv2.cvtColor(rgba, cv2.COLOR_BGRA2RGBA)
            
            pil_frame = Image.fromarray(rgba).resize((512, 512), Image.Resampling.LANCZOS)
            pil_frame.save(f"{temp_dir}/f_{frame_idx:03d}.png")
            frames_rgba.append(pil_frame)
            frame_idx += 1
            
        cap.release()
        
        if frames_rgba:
            # 1. Static PNG & WebP
            frames_rgba[0].save(f"{p_dir}/static.png")
            frames_rgba[0].save(f"{p_dir}/static.webp", quality=92)
            
            # 2. Animated WebP (duration 41ms = 24fps)
            frames_rgba[0].save(
                f"{p_dir}/animated.webp",
                save_all=True,
                append_images=frames_rgba[1:],
                duration=41,
                loop=0,
                quality=90,
                method=3
            )
            
            # 3. Animated GIF
            frames_rgba[0].save(
                f"{p_dir}/animated.gif",
                save_all=True,
                append_images=frames_rgba[1:],
                duration=41,
                loop=0,
                disposal=2,
                optimize=True
            )
            
            # 4. Animated PNG (APNG)
            frames_rgba[0].save(
                f"{p_dir}/animated.png",
                save_all=True,
                append_images=frames_rgba[1:],
                duration=41,
                loop=0
            )
            print(f"  ✓ inuko {p}: 100% clean transparent ({len(frames_rgba)} frames)")

    # Update avatar.png
    static_01 = f"{m_dir}/01_waving/static.png"
    if os.path.exists(static_01):
        Image.open(static_01).resize((128, 128), Image.Resampling.LANCZOS).save(f"{m_dir}/avatar.png")
        print("  ✓ inuko avatar.png updated.")

clean_and_build("/Users/richard/Downloads/Stickers 3D/mascots/inuko/assets")
print("Done Inuko processing.")
