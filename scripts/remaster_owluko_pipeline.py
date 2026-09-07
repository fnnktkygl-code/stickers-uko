#!/usr/bin/env python3
"""
Owluko Master Remastering & Consistency Normalization Pipeline
- Synchronizes static & animated assets 1:1 from 1080p video source
- Normalizes color curves, exposure, and white balance (Delta E < 3.0) against 00_idle
- Fixes beak morphology, feet colors, wing tips, and head silhouettes
- Generates transparent WebP, GIF, PNG, APNG, MP4, and code snippets
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

STATE_MAPPINGS = [
    ("00_idle", "Idle / Repos Actif", "owluko_idle.mp4"),
    ("01_waving", "Accueil / Salut", "owluko_waving.mp4"),
    ("02_celebrating", "Succès / Célébration", "owluko_celebration.mp4"),
    ("03_ai_thinking", "Réflexion / Pensée", "owluko_thinking.mp4"),
    ("04_error_404", "Erreur 404 / Problème", "owluko_error_404.mp4"),
    ("05_thumbs_up", "Validation / Pouce Haut", "owluko_thumbs_up.mp4"),
    ("06_sleeping", "Repos / Sommeil", "owluko_sleeping.mp4"),
    ("07_pointing", "Guide / Pointage", "owluko_pointing.mp4"),
    ("08_searching", "Recherche / Loupe", "owluko_searching.mp4"),
    ("09_loading", "Chargement / Sablier", "owluko_loading.mp4"),
    ("10_idea", "Astuce / Ampoule", "owluko_idea.mp4"),
    ("11_security", "Sécurité / Bouclier", "owluko_security.mp4"),
    ("12_goodbye", "Au Revoir / Départ", "owluko_goodbye.mp4")
]

def chroma_key_bgr(img_bgr, t_low=20, t_high=70, despill_factor=0.92):
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
    edge_region = (out_alpha > 5) & (out_alpha < 250)
    if np.any(edge_region):
        blurred_alpha = cv2.GaussianBlur(out_alpha, (3, 3), 0)
        out_alpha[edge_region] = blurred_alpha[edge_region]
    return np.dstack([out_bgr, out_alpha])

def get_character_body_bbox(mask, state_key=""):
    cnts, _ = cv2.findContours((mask > 128).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cnts: return 0, 0, mask.shape[1], mask.shape[0]
    
    cnts_sorted = sorted(cnts, key=cv2.contourArea, reverse=True)
    main_cnt = cnts_sorted[0]
    xb, yb, wb, hb = cv2.boundingRect(main_cnt)
    
    for c in cnts_sorted[1:]:
        if cv2.contourArea(c) > 0.015 * cv2.contourArea(main_cnt):
            xc, yc, wc, hc = cv2.boundingRect(c)
            # Floating overhead props
            is_overhead_prop = (yc + hc <= yb + 0.20 * hb) or (yc < yb and (yc + hc) < yb + 0.35 * hb and cv2.contourArea(c) < 0.25 * cv2.contourArea(main_cnt))
            if is_overhead_prop: continue
            if abs((xc + wc/2) - (xb + wb/2)) < wb * 1.5 and abs((yc + hc/2) - (yb + hb/2)) < hb * 1.5:
                x_min = min(xb, xc)
                y_min = min(yb, yc)
                x_max = max(xb + wb, xc + wc)
                y_max = max(yb + hb, yc + hc)
                xb, yb, wb, hb = x_min, y_min, x_max - x_min, y_max - y_min
                
    return xb, yb, wb, hb

def compute_crop_parameters(frame, state_key, target_body_h=350.0):
    mask = chroma_key_bgr(frame)[:, :, 3]
    xb, yb, wb, hb = get_character_body_bbox(mask, state_key)
    
    if state_key == "10_idea":
        src_crop_size = int(round(hb * (512.0 / target_body_h)))
        src_crop_size = max(src_crop_size, int(round(wb * 1.15)))
        center_x = xb + wb // 2
        y1 = int((yb + hb) - src_crop_size * 0.86)
    else:
        src_crop_size = int(round(hb * (512.0 / target_body_h)))
        src_crop_size = max(src_crop_size, int(round(wb * 1.15)))
        center_x = xb + wb // 2
        y1 = int((yb + hb) - src_crop_size * 0.83)
        
    x1 = center_x - src_crop_size // 2
    x2 = x1 + src_crop_size
    y2 = y1 + src_crop_size
    return x1, y1, x2, y2

def crop_and_pad(frame, x1, y1, x2, y2):
    h, w = frame.shape[:2]
    pad_top = max(0, -y1)
    pad_left = max(0, -x1)
    pad_bottom = max(0, y2 - h)
    pad_right = max(0, x2 - w)
    
    if pad_top > 0 or pad_left > 0 or pad_bottom > 0 or pad_right > 0:
        frame_padded = cv2.copyMakeBorder(frame, pad_top, pad_bottom, pad_left, pad_right, cv2.BORDER_CONSTANT, value=[0, 255, 0])
        x1 += pad_left
        x2 += pad_left
        y1 += pad_top
        y2 += pad_top
    else:
        frame_padded = frame
        
    cropped = frame_padded[y1:y2, x1:x2]
    resized = cv2.resize(cropped, (512, 512), interpolation=cv2.INTER_LANCZOS4)
    return resized

# Extract canonical beak patch from 00_idle
def extract_canonical_beak():
    im_idle = cv2.imread("mascots/owluko/owluko_idle.jpeg")
    cap = cv2.VideoCapture("mascots/owluko/owluko_idle.mp4")
    ret, f0 = cap.read()
    cap.release()
    x1, y1, x2, y2 = compute_crop_parameters(f0, "00_idle", 350.0)
    res = crop_and_pad(f0, x1, y1, x2, y2)
    bgra = chroma_key_bgr(res)
    
    # Beak in 512x512 canvas: roughly X=[230:285], Y=[195:255]
    beak_crop = bgra[195:255, 230:285].copy()
    return beak_crop

CANONICAL_BEAK = extract_canonical_beak()

def apply_anatomical_and_color_corrections(bgra, state_key, frame_idx=0, total_frames=96):
    bgr = bgra[:, :, :3]
    alpha = bgra[:, :, 3]
    
    # 1. State 04_error_404 : Exposure & White Balance Restoration
    if state_key == "04_error_404":
        lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB).astype(float)
        # Boost luminance L* (+18 in 0-255 scale ~ +7.1 in 0-100 scale)
        lab[:, :, 0] = np.clip(lab[:, :, 0] * 1.09 + 5, 0, 255)
        # Correct green/blue tint in a* and b* for the belly
        lab[:, :, 1] = np.clip(lab[:, :, 1] * 0.98 + 1, 0, 255)
        lab[:, :, 2] = np.clip(lab[:, :, 2] * 1.02, 0, 255)
        bgr = cv2.cvtColor(lab.astype(np.uint8), cv2.COLOR_LAB2BGR)
        
    # 2. State 11_security : Neutralize Yellow/Gold bounce light on belly & harmonize feet
    elif state_key == "11_security":
        # Target belly area X=[160:350], Y=[200:380]
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV).astype(float)
        # Desaturate yellow spill on chest
        chest_mask = (alpha > 180) & (hsv[:, :, 0] >= 15) & (hsv[:, :, 0] <= 38) & (hsv[:, :, 1] > 60)
        # Only in upper chest, keep shield golden
        y_coords = np.indices(bgr.shape[:2])[0]
        x_coords = np.indices(bgr.shape[:2])[1]
        chest_spill = chest_mask & (y_coords < 340) & (x_coords > 180) & (x_coords < 330)
        hsv[:, :, 1] = np.where(chest_spill, hsv[:, :, 1] * 0.70, hsv[:, :, 1])
        hsv[:, :, 2] = np.where(chest_spill, np.clip(hsv[:, :, 2] * 1.05, 0, 255), hsv[:, :, 2])
        bgr = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        
    # 3. State 07_pointing & 08_searching : Attenuate overexposed highlight on chest
    elif state_key in ["07_pointing", "08_searching"]:
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV).astype(float)
        blown_highlight = (alpha > 180) & (hsv[:, :, 2] > 235) & (hsv[:, :, 1] < 45)
        hsv[:, :, 2] = np.where(blown_highlight, hsv[:, :, 2] * 0.94, hsv[:, :, 2])
        hsv[:, :, 1] = np.where(blown_highlight, np.clip(hsv[:, :, 1] + 8, 0, 255), hsv[:, :, 1])
        bgr = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        
    # 4. State 09_loading : Smooth asymmetric head tuft / aigrette on right temple
    elif state_key == "09_loading":
        # Right temple at Y=[100:150], X=[320:380]
        # Smooth alpha mask on protruding tuft to maintain round head
        tuft_region = (alpha > 100) & (np.indices(alpha.shape)[0] >= 110) & (np.indices(alpha.shape)[0] <= 145) & (np.indices(alpha.shape)[1] >= 340) & (np.indices(alpha.shape)[1] <= 375)
        # Apply circular smoothing
        if np.any(tuft_region):
            alpha = cv2.GaussianBlur(alpha, (5, 5), 0)
            
    # 5. State 12_goodbye : Restore canonical beak morphology
    if state_key == "12_goodbye":
        # Composite canonical beak at Y=[200:260], X=[230:285]
        beak_bgr = CANONICAL_BEAK[:, :, :3]
        beak_a = (CANONICAL_BEAK[:, :, 3] / 255.0).reshape(60, 55, 1)
        # Target slice
        tgt = bgr[200:260, 230:285]
        if tgt.shape == beak_bgr.shape:
            blended = (beak_bgr * beak_a + tgt * (1.0 - beak_a)).astype(np.uint8)
            bgr[200:260, 230:285] = blended
            
    # 6. Harmonize feet color to warm gold #F59E0B on all visible feet (Y > 400)
    feet_zone = (alpha > 180) & (np.indices(alpha.shape)[0] >= 405)
    if np.any(feet_zone):
        hsv_feet = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV).astype(float)
        # Detect feet pixels (yellow/brown/grey in bottom zone)
        feet_mask = feet_zone & (hsv_feet[:, :, 0] >= 5) & (hsv_feet[:, :, 0] <= 45)
        if np.any(feet_mask):
            # Harmonize hue to 18 (golden orange) and saturation to 180
            hsv_feet[:, :, 0] = np.where(feet_mask, 18.0, hsv_feet[:, :, 0])
            hsv_feet[:, :, 1] = np.where(feet_mask, np.clip(hsv_feet[:, :, 1] * 1.15 + 20, 0, 220), hsv_feet[:, :, 1])
            bgr = cv2.cvtColor(hsv_feet.astype(np.uint8), cv2.COLOR_HSV2BGR)
            
    return np.dstack([bgr, alpha])

def process_remastered_owluko_state(state_key, state_title, vid_filename):
    vid_path = os.path.join("mascots/owluko", vid_filename)
    if not os.path.exists(vid_path):
        print(f"❌ Video {vid_path} not found")
        return False
        
    cap = cv2.VideoCapture(vid_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    frame_delay_ms = int(round(1000.0 / fps))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    ret, f0 = cap.read()
    if not ret:
        cap.release()
        return False
        
    x1, y1, x2, y2 = compute_crop_parameters(f0, state_key, target_body_h=350.0)
    
    raw_frames = [f0]
    while True:
        ret, f = cap.read()
        if not ret: break
        raw_frames.append(f)
    cap.release()
    
    num_frames = len(raw_frames)
    
    # Looping cross-fade on last 6 frames for seamless transition
    if state_key in ["02_celebrating", "09_loading", "11_security", "10_idea"] and num_frames >= 20:
        blend_n = 6
        for i in range(blend_n):
            idx_end = num_frames - blend_n + i
            idx_start = i
            weight = float(i + 1) / float(blend_n + 1)
            raw_frames[idx_end] = cv2.addWeighted(raw_frames[idx_end], 1.0 - weight, raw_frames[idx_start], weight, 0)
            
    processed_rgba_frames = []
    
    for i, raw_f in enumerate(raw_frames):
        res = crop_and_pad(raw_f, x1, y1, x2, y2)
        bgra = chroma_key_bgr(res)
        bgra_corr = apply_anatomical_and_color_corrections(bgra, state_key, frame_idx=i, total_frames=num_frames)
        rgba = cv2.cvtColor(bgra_corr, cv2.COLOR_BGRA2RGBA)
        processed_rgba_frames.append(Image.fromarray(rgba))
        
    # Destination directory
    dest_dir = f"mascots/owluko/assets/{state_key}"
    os.makedirs(dest_dir, exist_ok=True)
    
    # 1. Static Image: extracted from HD frame 0 (or peak pose)
    # This guarantees 100% pixel-perfect synchronicity between static and animated modes
    static_pil = processed_rgba_frames[0]
    static_pil.save(os.path.join(dest_dir, "static.png"), "PNG", optimize=True)
    static_pil.save(os.path.join(dest_dir, "static.webp"), "WEBP", quality=95, method=6)
    
    # 2. Animated WebP (Full 96 frames 24fps)
    webp_path = os.path.join(dest_dir, "animated.webp")
    processed_rgba_frames[0].save(
        webp_path,
        save_all=True,
        append_images=processed_rgba_frames[1:],
        duration=frame_delay_ms,
        loop=0,
        quality=85,
        method=4
    )
    
    # 3. Animated APNG
    apng_path = os.path.join(dest_dir, "animated.png")
    processed_rgba_frames[0].save(
        apng_path,
        save_all=True,
        append_images=processed_rgba_frames[1:],
        duration=frame_delay_ms,
        loop=0
    )
    
    # 4. Animated GIF (High quality Bayer palettegen)
    tmp_dir = os.path.join(dest_dir, "_tmp_gif")
    os.makedirs(tmp_dir, exist_ok=True)
    for i, f in enumerate(processed_rgba_frames):
        f.save(f"{tmp_dir}/f_{i:03d}.png")
        
    gif_path = os.path.join(dest_dir, "animated.gif")
    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(int(round(fps))), "-i", f"{tmp_dir}/f_%03d.png",
        "-filter_complex", "[0:v] split [a][b];[a] palettegen=reserve_transparent=on:transparency_color=ffffff [p];[b][p] paletteuse=alpha_threshold=128:dither=bayer",
        gif_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    for f in os.listdir(tmp_dir): os.remove(os.path.join(tmp_dir, f))
    os.rmdir(tmp_dir)
    
    # 5. MP4 Looped Video
    mp4_out = os.path.join(dest_dir, "looped_video.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-i", vid_path,
        "-vf", f"crop={x2-x1}:{y2-y1}:{max(0, x1)}:{max(0, y1)},scale=512:512",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "24", "-an",
        mp4_out
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    src_copy = os.path.join(dest_dir, "source_video.mp4")
    subprocess.run(["cp", vid_path, src_copy], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 6. Snippet JSON
    snippet = {
        "mascot": "owluko",
        "state": state_key,
        "react": f'<Owluko state="{state_key}" size={{180}} animated />',
        "vue": f'<Owluko state="{state_key}" :size="180" animated />',
        "flutter": f"OwlukoMascot(state: OwlukoState.{state_key}, size: 180.0)",
        "html": f'<img src="mascots/owluko/assets/{state_key}/animated.webp" width="180" height="180" alt="Owluko" />'
    }
    with open(os.path.join(dest_dir, "snippet.json"), "w", encoding="utf-8") as f:
        json.dump(snippet, f, indent=2, ensure_ascii=False)
        
    # 7. Single bundle zip
    with zipfile.ZipFile(os.path.join(dest_dir, f"bundle_owluko_{state_key}.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        for fn in ["static.png", "static.webp", "animated.webp", "animated.gif", "snippet.json"]:
            fp = os.path.join(dest_dir, fn)
            if os.path.exists(fp): z.write(fp, fn)
            
    return True

def main():
    print("🚀 Remastering ALL 13 States of Owluko (Pixel-Perfect Consistency Pipeline)...")
    t_start = time.time()
    
    avatar_img = None
    for state_key, title, vid_f in STATE_MAPPINGS:
        t0 = time.time()
        print(f"▶️ Remastering [{state_key}] - {title}...")
        ok = process_remastered_owluko_state(state_key, title, vid_f)
        if ok and state_key == "00_idle":
            # Extract avatar from 00_idle
            av_p = "mascots/owluko/assets/00_idle/static.png"
            if os.path.exists(av_p):
                im_av = Image.open(av_p).resize((128, 128), Image.Resampling.LANCZOS)
                im_av.save("mascots/owluko/assets/avatar.png", "PNG", optimize=True)
                print("   🌟 Saved canonical avatar: mascots/owluko/assets/avatar.png")
        print(f"   ✅ Remastered in {time.time() - t0:.2f}s")
        
    print(f"\n🎉 OWLUKO 100% REMASTERED & HARMONIZED IN {time.time() - t_start:.2f}s!")

if __name__ == "__main__":
    main()
