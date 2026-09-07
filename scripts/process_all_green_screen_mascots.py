#!/usr/bin/env python3
"""
Master Chroma Key & Multi-Format Processing Pipeline for Uko UI Mascots
Supports: AItuko, Owluko, Luneko
Outputs per state:
  - static.png (512x512 RGBA HD transparent)
  - static.webp (512x512 WebP HD transparent)
  - animated.webp (512x512 24fps WebP transparent animation)
  - animated.gif (512x512 24fps Palettegen transparent GIF)
  - animated.png (512x512 24fps APNG transparent)
  - looped_video.mp4 (H.264 video loop)
  - source_video.mp4 (Clean source video)
  - snippet.json (Type-safe code snippets)
  - bundle_{mascot}_{state}.zip
"""

import os
import sys
import glob
import json
import time
import zipfile
import subprocess
import numpy as np
import cv2
from PIL import Image

STATE_CONFIGS = [
    ("00_idle", ["idle"], "Idle / Repos Actif"),
    ("01_waving", ["waving", "wave"], "Accueil / Waving"),
    ("02_celebrating", ["celebrating", "celebration"], "Succès / Celebrating"),
    ("03_ai_thinking", ["thinking", "ai_thinking"], "Réflexion / Thinking"),
    ("04_error_404", ["error_404", "error", "404"], "Erreur 404 / Error"),
    ("05_thumbs_up", ["thumbs_up", "thumbsup"], "Validation / Thumbs Up"),
    ("06_sleeping", ["sleeping", "sleep"], "Repos / Sleeping"),
    ("07_pointing", ["pointing", "point"], "Guide / Pointing"),
    ("08_searching", ["searching", "search"], "Recherche / Searching"),
    ("09_loading", ["loading", "load"], "Chargement / Loading"),
    ("10_idea", ["idea"], "Astuce / Idea"),
    ("11_security", ["security", "shield"], "Sécurité / Security"),
    ("12_goodbye", ["goodbye", "bye"], "Au Revoir / Goodbye")
]

MASCOT_METADATA = {
    "aituko": {
        "name": "AItuko",
        "component": "AItuko",
        "flutter": "AItukoMascot",
        "desc": "Assistant IA • Accueil & Onboarding"
    },
    "owluko": {
        "name": "Owluko",
        "component": "Owluko",
        "flutter": "OwlukoMascot",
        "desc": "Guide de Sagesse • Aide & Connaissance"
    },
    "luneko": {
        "name": "Luneko",
        "component": "Luneko",
        "flutter": "LunekoMascot",
        "desc": "Compagnon Joueur • Gamification & Récompenses"
    }
}

def chroma_key_bgr(img_bgr, t_low=20, t_high=70, despill_factor=0.92):
    """
    SOTA Chroma Key Matting for #00FF00 Green Screen
    Returns 4-channel BGRA numpy array
    """
    b = img_bgr[:, :, 0].astype(float)
    g = img_bgr[:, :, 1].astype(float)
    r = img_bgr[:, :, 2].astype(float)
    
    max_rb = np.maximum(r, b)
    green_diff = g - max_rb
    
    alpha = 1.0 - np.clip((green_diff - t_low) / (t_high - t_low), 0.0, 1.0)
    
    despill_mask = (g > max_rb)
    g_despilled = np.where(despill_mask, max_rb * despill_factor + g * (1.0 - despill_factor), g)
    
    out_bgr = np.stack([b, g_despilled, r], axis=2).clip(0, 255).astype(np.uint8)
    out_alpha = (alpha * 255.0).clip(0, 255).astype(np.uint8)
    
    # Soft subpixel edge feathering
    edge_region = (out_alpha > 5) & (out_alpha < 250)
    if np.any(edge_region):
        blurred_alpha = cv2.GaussianBlur(out_alpha, (3, 3), 0)
        out_alpha[edge_region] = blurred_alpha[edge_region]
        
    return np.dstack([out_bgr, out_alpha])

def find_source_files(mascot, aliases):
    dir_path = f"mascots/{mascot}"
    all_files = os.listdir(dir_path)
    
    img_file = None
    vid_file = None
    
    for alias in aliases:
        for f in all_files:
            if f.startswith('.'): continue
            base, ext = os.path.splitext(f)
            if base.lower() == f"{mascot}_{alias}".lower():
                if ext.lower() in [".jpeg", ".jpg", ".png", ".webp"] and not img_file:
                    img_file = os.path.join(dir_path, f)
                elif ext.lower() in [".mp4", ".mov", ".webm"] and not vid_file:
                    vid_file = os.path.join(dir_path, f)
                    
    return img_file, vid_file

def process_static_image(src_path, out_dir):
    img = cv2.imread(src_path)
    if img is None:
        raise ValueError(f"Could not read static image: {src_path}")
        
    h, w = img.shape[:2]
    crop_size = min(h, w)
    x1 = (w - crop_size) // 2
    y1 = (h - crop_size) // 2
    cropped = img[y1:y1+crop_size, x1:x1+crop_size]
    resized = cv2.resize(cropped, (512, 512), interpolation=cv2.INTER_LANCZOS4)
    
    bgra = chroma_key_bgr(resized)
    rgba = cv2.cvtColor(bgra, cv2.COLOR_BGRA2RGBA)
    pil_img = Image.fromarray(rgba)
    
    png_path = os.path.join(out_dir, "static.png")
    webp_path = os.path.join(out_dir, "static.webp")
    
    pil_img.save(png_path, "PNG", optimize=True)
    pil_img.save(webp_path, "WEBP", quality=95, method=6)
    
    return pil_img

def process_video_animation(src_path, out_dir):
    cap = cv2.VideoCapture(src_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video: {src_path}")
        
    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    frame_delay_ms = int(round(1000.0 / fps))
    
    frames_rgba = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        h, w = frame.shape[:2]
        crop_size = min(h, w)
        x1 = (w - crop_size) // 2
        y1 = (h - crop_size) // 2
        cropped = frame[y1:y1+crop_size, x1:x1+crop_size]
        resized = cv2.resize(cropped, (512, 512), interpolation=cv2.INTER_LANCZOS4)
        bgra = chroma_key_bgr(resized)
        rgba = cv2.cvtColor(bgra, cv2.COLOR_BGRA2RGBA)
        frames_rgba.append(Image.fromarray(rgba))
        
    cap.release()
    
    if not frames_rgba:
        raise ValueError(f"No frames extracted from {src_path}")
        
    # 1. Save animated WebP (1:1 exact real-time speed)
    webp_path = os.path.join(out_dir, "animated.webp")
    frames_rgba[0].save(
        webp_path,
        save_all=True,
        append_images=frames_rgba[1:],
        duration=frame_delay_ms,
        loop=0,
        quality=85,
        method=4
    )
    
    # 2. Save APNG (1:1 exact real-time speed)
    apng_path = os.path.join(out_dir, "animated.png")
    frames_rgba[0].save(
        apng_path,
        save_all=True,
        append_images=frames_rgba[1:],
        duration=frame_delay_ms,
        loop=0
    )
    
    # 3. Save GIF using palettegen (1:1 exact real-time speed)
    tmp_dir = os.path.join(out_dir, "_tmp_frames")
    os.makedirs(tmp_dir, exist_ok=True)
    for i, f in enumerate(frames_rgba):
        f.save(f"{tmp_dir}/f_{i:03d}.png")
        
    gif_path = os.path.join(out_dir, "animated.gif")
    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(int(round(fps))), "-i", f"{tmp_dir}/f_%03d.png",
        "-filter_complex", "[0:v] split [a][b];[a] palettegen=reserve_transparent=on:transparency_color=ffffff [p];[b][p] paletteuse=alpha_threshold=128:dither=bayer",
        gif_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Clean temp frames
    for f in os.listdir(tmp_dir):
        os.remove(os.path.join(tmp_dir, f))
    os.rmdir(tmp_dir)
    
    # 4. Copy / crop looped video MP4
    mp4_out = os.path.join(out_dir, "looped_video.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-i", src_path,
        "-vf", "crop='min(iw,ih)':'min(iw,ih)',scale=512:512",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-an",
        mp4_out
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 5. Copy raw source video
    src_copy = os.path.join(out_dir, "source_video.mp4")
    subprocess.run(["cp", src_path, src_copy], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def generate_snippets_and_zip(mascot, state_folder, out_dir):
    meta = MASCOT_METADATA[mascot]
    comp = meta["component"]
    flt = meta["flutter"]
    
    snippet = {
        "mascot": mascot,
        "state": state_folder,
        "react": f"<{comp} state=\"{state_folder}\" size={{180}} animated />",
        "vue": f"<{comp} state=\"{state_folder}\" :size=\"180\" animated />",
        "flutter": f"{flt}(state: {comp}State.{state_folder}, size: 180.0)",
        "html": f'<img src="assets/{state_folder}/animated.webp" width="180" height="180" alt="{meta["name"]}" />'
    }
    
    snippet_path = os.path.join(out_dir, "snippet.json")
    with open(snippet_path, "w", encoding="utf-8") as f:
        json.dump(snippet, f, indent=2, ensure_ascii=False)
        
    zip_path = os.path.join(out_dir, f"bundle_{mascot}_{state_folder}.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for fname in ["static.png", "static.webp", "animated.webp", "animated.gif", "animated.png", "looped_video.mp4", "snippet.json"]:
            fp = os.path.join(out_dir, fname)
            if os.path.exists(fp):
                z.write(fp, fname)

def main():
    print("🚀 Starting Master Chroma Key Processing Pipeline...")
    total_start = time.time()
    
    mascots = ["aituko", "owluko", "luneko"]
    
    for mascot in mascots:
        print(f"\n=======================================================")
        print(f"🎨 PROCESSING MASCOT: {mascot.upper()}")
        print(f"=======================================================")
        
        # Directories to populate
        dest_dirs = []
        if mascot == "aituko":
            dest_dirs.append("assets")
            dest_dirs.append("mascots/aituko/assets")
        else:
            dest_dirs.append(f"mascots/{mascot}/assets")
            
        for dest_base in dest_dirs:
            os.makedirs(dest_base, exist_ok=True)
            
        avatar_img = None
        
        for state_folder, aliases, state_title in STATE_CONFIGS:
            t0 = time.time()
            img_src, vid_src = find_source_files(mascot, aliases)
            
            if not img_src or not vid_src:
                print(f"⚠️ Missing source for {mascot} - {state_folder} (img: {img_src}, vid: {vid_src})")
                continue
                
            print(f"\n▶️ Processing [{state_folder}] - {state_title}")
            print(f"   Image: {os.path.basename(img_src)}")
            print(f"   Video: {os.path.basename(vid_src)}")
            
            # Primary directory
            primary_dir = os.path.join(dest_dirs[0], state_folder)
            os.makedirs(primary_dir, exist_ok=True)
            
            # 1. Process static image
            pil_static = process_static_image(img_src, primary_dir)
            if state_folder == "00_idle" and avatar_img is None:
                avatar_img = pil_static
                
            # 2. Process video animation
            process_video_animation(vid_src, primary_dir)
            
            # 3. Snippets and zip
            generate_snippets_and_zip(mascot, state_folder, primary_dir)
            
            # If multiple destination directories (e.g. aituko), duplicate primary to secondary
            if len(dest_dirs) > 1:
                sec_dir = os.path.join(dest_dirs[1], state_folder)
                os.makedirs(sec_dir, exist_ok=True)
                for item in os.listdir(primary_dir):
                    s_file = os.path.join(primary_dir, item)
                    d_file = os.path.join(sec_dir, item)
                    if os.path.isfile(s_file):
                        subprocess.run(["cp", s_file, d_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        
            print(f"   ✅ Done in {time.time() - t0:.2f}s")
            
        # Save avatar.png
        if avatar_img:
            avatar_cropped = avatar_img.resize((128, 128), Image.Resampling.LANCZOS)
            for dest_base in dest_dirs:
                avatar_path = os.path.join(dest_base, "avatar.png")
                avatar_cropped.save(avatar_path, "PNG", optimize=True)
                print(f"   🌟 Saved avatar: {avatar_path}")
                
    print(f"\n🎉 ALL MASCOTS PROCESSED SUCCESSFULLY in {time.time() - total_start:.2f}s!")

if __name__ == "__main__":
    main()
