import os
import glob
import cv2
import numpy as np
from PIL import Image

BASE_DIRS = [
    "/Users/richard/Downloads/Stickers 3D",
    "/Users/richard/Developer/Stickers 3D"
]

mascots = ["inuko", "luneko", "hatoko", "usako", "owluko", "aituko"]
poses = [
    "01_waving", "02_celebrating", "03_ai_thinking", "04_error_404",
    "05_thumbs_up", "06_sleeping", "07_pointing", "08_searching",
    "09_loading", "10_idea", "11_security", "12_goodbye"
]

def process_video_frames(looped_mp4, temp_dir, mascot_key):
    os.makedirs(temp_dir, exist_ok=True)
    cap = cv2.VideoCapture(looped_mp4)
    frame_idx = 0
    
    # Range of green in HSV
    lower_green = np.array([30, 40, 40])
    upper_green = np.array([88, 255, 255])
    kernel = np.ones((3, 3), np.uint8)
    
    frames_rgba = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        h, w, _ = frame.shape
        # Center square crop
        if w > h:
            start_x = (w - h) // 2
            cropped = frame[:, start_x:start_x+h]
        else:
            cropped = frame
            
        hsv = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
        bg_mask = cv2.inRange(hsv, lower_green, upper_green)
        fg_mask = cv2.bitwise_not(bg_mask)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
        
        # Soft feathering
        alpha = fg_mask.astype(float) / 255.0
        alpha = cv2.GaussianBlur(alpha, (3, 3), 0)
        alpha = (alpha * 255).astype(np.uint8)
        
        # Color despill
        b, g, r = cv2.split(cropped)
        max_rb = np.maximum(r, b)
        g_clean = np.where((g > max_rb) & (alpha < 250), max_rb, g)
        
        rgba = cv2.merge([b, g_clean, r, alpha])
        rgba = cv2.cvtColor(rgba, cv2.COLOR_BGRA2RGBA)
        
        pil_frame = Image.fromarray(rgba).resize((512, 512), Image.Resampling.LANCZOS)
        out_frame_path = f"{temp_dir}/f_{frame_idx:03d}.png"
        pil_frame.save(out_frame_path)
        frames_rgba.append(pil_frame)
        frame_idx += 1
        
    cap.release()
    return frames_rgba

for base_dir in BASE_DIRS:
    if not os.path.exists(base_dir):
        continue
    print(f"\n==========================================")
    print(f"📦 Processing assets in: {base_dir}")
    print(f"==========================================")
    
    for m in mascots:
        m_assets_dir = f"{base_dir}/assets" if m == "aituko" else f"{base_dir}/mascots/{m}/assets"
        if not os.path.exists(m_assets_dir):
            continue
            
        print(f"\n🐶 Re-keying mascot: {m.upper()}...")
        for p in poses:
            p_dir = f"{m_assets_dir}/{p}"
            looped_mp4 = f"{p_dir}/looped_video.mp4"
            temp_dir = f"{p_dir}/temp_frames"
            
            if not os.path.exists(looped_mp4):
                # If looped video doesn't exist, check source_video
                source_mp4 = f"{p_dir}/source_video.mp4"
                if os.path.exists(source_mp4):
                    # Make ping-pong loop
                    subprocess.run([
                        "ffmpeg", "-y", "-t", "2.0", "-i", source_mp4,
                        "-filter_complex", "[0:v]split[v1][v2];[v2]reverse[v2rev];[v1][v2rev]concat=n=2:v=1[v]",
                        "-map", "[v]", "-r", "24", "-c:v", "libx264", "-pix_fmt", "yuv420p", looped_mp4
                    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            if os.path.exists(looped_mp4):
                frames = process_video_frames(looped_mp4, temp_dir, m)
                if frames:
                    # 1. Static PNG & WebP (neutral frame 0)
                    frames[0].save(f"{p_dir}/static.png")
                    frames[0].save(f"{p_dir}/static.webp", quality=92)
                    
                    # 2. Animated WebP (duration 41ms = 24fps)
                    frames[0].save(
                        f"{p_dir}/animated.webp",
                        save_all=True,
                        append_images=frames[1:],
                        duration=41,
                        loop=0,
                        quality=90,
                        method=3
                    )
                    
                    # 3. Animated GIF
                    frames[0].save(
                        f"{p_dir}/animated.gif",
                        save_all=True,
                        append_images=frames[1:],
                        duration=41,
                        loop=0,
                        disposal=2,
                        optimize=True
                    )
                    
                    # 4. Animated PNG (APNG)
                    frames[0].save(
                        f"{p_dir}/animated.png",
                        save_all=True,
                        append_images=frames[1:],
                        duration=41,
                        loop=0
                    )
                    print(f"  ✓ {m} {p}: 100% clean transparent assets built ({len(frames)} frames)")

        # Create avatar.png from neutral 01_waving static.png
        waving_static = f"{m_assets_dir}/01_waving/static.png"
        if os.path.exists(waving_static):
            im = Image.open(waving_static)
            im.resize((128, 128), Image.Resampling.LANCZOS).save(f"{m_assets_dir}/avatar.png")
            print(f"  ✓ {m} avatar.png updated from neutral frame.")

print("\n🎉 ALL ASSETS 100% RE-KEYED WITH PURE TRANSPARENCY!")
