#!/usr/bin/env python3
"""
Refined Master Vector AItuko Renderer with 100% Spotless Uniform Porcelain.
Removes ALL interior shadow smudges, streaks, and grey patches.
Pure clean uniform mascot matching user requirement.
"""

import math
import os
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.build_master_vector_aituko import extract_all_component_splines, SCALE_512, CENTER_X_GT, Y_MIN_GT, OFFSET_Y_512
from scripts.verify_aituko_component import ref_bgr, clean_char_mask

BRAIN_DIR = "/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68"
WORKSPACE_DIR = "/Users/richard/Developer/Stickers Uko"

# Spotless Uniform Porcelain Colors
PORCELAIN_FILL = (255, 255, 255, 255)
PORCELAIN_OUTLINE = (218, 224, 233, 255)
VISOR_GLASS = (12, 14, 20, 255)
VISOR_RIM = (28, 33, 46, 255)
CYAN_EMISSIVE = (0, 240, 255, 255)

def render_flawless_master(scale=4):
    W = 512 * scale
    H = 512 * scale
    
    # 1. Base Studio Dark Backdrop (#0B0F17)
    img = Image.new('RGBA', (W, H), (11, 15, 23, 255))
    
    # Extract calibrated points
    _, points_512 = extract_all_component_splines()
    
    def S(pts):
        return np.array([[int(round(x * scale)), int(round(y * scale))] for x, y in pts], dtype=np.int32)

    # 1. Ground Ambient Shadow
    sh_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(sh_layer)
    cx, cy = int(256 * scale), int(488 * scale)
    rx, ry = int(95 * scale), int(12 * scale)
    sh_draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(0, 0, 0, 140))
    sh_layer = sh_layer.filter(ImageFilter.GaussianBlur(radius=8 * scale))
    img.alpha_composite(sh_layer)

    # 2. Foot Landing Pods (Spotless Uniform White Porcelain)
    for foot_name in ["left_foot", "right_foot"]:
        foot_pts = S(points_512[foot_name])
        fcx = int(np.mean(foot_pts[:, 0]))
        fcy = int(np.max(foot_pts[:, 1]))
        
        # Cyan thruster glow underneath
        tg_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        tg_draw = ImageDraw.Draw(tg_layer)
        tg_draw.ellipse([fcx - int(16 * scale), fcy - int(3 * scale), fcx + int(16 * scale), fcy + int(8 * scale)], fill=(0, 240, 255, 140))
        tg_layer = tg_layer.filter(ImageFilter.GaussianBlur(radius=5 * scale))
        img.alpha_composite(tg_layer)
        
        # Pure spotless porcelain fill
        foot_patch = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        fp_draw = ImageDraw.Draw(foot_patch)
        fp_draw.polygon([tuple(p) for p in foot_pts], fill=PORCELAIN_FILL, outline=PORCELAIN_OUTLINE, width=max(1, int(1.2 * scale)))
        img.alpha_composite(foot_patch)

    # 3. Torso (Spotless Uniform Porcelain Capsule - NO GREY SHADOWS, NO STREAKS)
    torso_pts = S(points_512["torso"])
    torso_patch = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    tp_draw = ImageDraw.Draw(torso_patch)
    tp_draw.polygon([tuple(p) for p in torso_pts], fill=PORCELAIN_FILL, outline=PORCELAIN_OUTLINE, width=max(1, int(1.2 * scale)))
    img.alpha_composite(torso_patch)

    # 4. Head Dome & Visor (Spotless Uniform Porcelain Helmet)
    head_pts = S(points_512["head"])
    head_patch = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    hp_draw = ImageDraw.Draw(head_patch)
    # Pure spotless helmet dome
    hp_draw.polygon([tuple(p) for p in head_pts], fill=PORCELAIN_FILL, outline=PORCELAIN_OUTLINE, width=max(1, int(1.2 * scale)))
    
    # Visor (Deep Obsidian Glass Faceplate)
    visor_pts = S(points_512["visor"])
    hp_draw.polygon([tuple(p) for p in visor_pts], fill=VISOR_GLASS, outline=VISOR_RIM, width=max(1, int(1.5 * scale)))
    
    # Soft Horizon Reflection Arc on upper glass
    v_light = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    vl_draw = ImageDraw.Draw(v_light)
    vc_x = int(256 * scale)
    v_min_y = int(np.min(visor_pts[:, 1]))
    vl_draw.ellipse([vc_x - int(75 * scale), v_min_y + int(6 * scale), vc_x + int(75 * scale), v_min_y + int(48 * scale)], fill=(120, 140, 170, 45))
    vl_draw.ellipse([vc_x - int(50 * scale), v_min_y + int(8 * scale), vc_x + int(50 * scale), v_min_y + int(28 * scale)], fill=(255, 255, 255, 45))
    v_light = v_light.filter(ImageFilter.GaussianBlur(radius=5 * scale))
    v_mask = Image.new('L', (W, H), 0)
    ImageDraw.Draw(v_mask).polygon([tuple(p) for p in visor_pts], fill=255)
    v_light.putalpha(ImageChops.multiply(v_light.split()[-1], v_mask))
    head_patch.alpha_composite(v_light)
    
    # Luminous Cyan Eyes (^ ^ Pure Glowing Solid Crescents with Multi-Stage Bloom)
    wide_bloom = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    wb_draw = ImageDraw.Draw(wide_bloom)
    med_bloom = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    mb_draw = ImageDraw.Draw(med_bloom)
    core_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    cb_draw = ImageDraw.Draw(core_layer)
    
    for eye_name in ["left_eye", "right_eye"]:
        eye_pts = S(points_512[eye_name])
        wb_draw.polygon([tuple(p) for p in eye_pts], fill=(0, 240, 255, 140))
        mb_draw.polygon([tuple(p) for p in eye_pts], fill=(0, 240, 255, 220))
        cb_draw.polygon([tuple(p) for p in eye_pts], fill=(0, 245, 255, 255))
        
    wide_bloom = wide_bloom.filter(ImageFilter.GaussianBlur(radius=12 * scale))
    med_bloom = med_bloom.filter(ImageFilter.GaussianBlur(radius=5 * scale))
    
    head_patch.alpha_composite(wide_bloom)
    head_patch.alpha_composite(med_bloom)
    head_patch.alpha_composite(core_layer)
    img.alpha_composite(head_patch)

    # 5. Floating Lateral Pods (Winglets — STRICTLY ZERO HANDS, Spotless Uniform White)
    for pod_name in ["left_pod", "right_pod"]:
        pod_pts = S(points_512[pod_name])
        pcx = int(np.mean(pod_pts[:, 0]))
        pcy = int(np.max(pod_pts[:, 1]))
        
        # Thruster bottom glow
        lg_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        lg_draw = ImageDraw.Draw(lg_layer)
        lg_draw.ellipse([pcx - int(12 * scale), pcy - int(3 * scale), pcx + int(12 * scale), pcy + int(6 * scale)], fill=(0, 240, 255, 130))
        lg_layer = lg_layer.filter(ImageFilter.GaussianBlur(radius=4 * scale))
        img.alpha_composite(lg_layer)
        
        # Pure spotless porcelain fill - NO GREY LINES OR SMUDGES
        pod_patch = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        pp_draw = ImageDraw.Draw(pod_patch)
        pp_draw.polygon([tuple(p) for p in pod_pts], fill=PORCELAIN_FILL, outline=PORCELAIN_OUTLINE, width=max(1, int(1.2 * scale)))
        img.alpha_composite(pod_patch)

    # 6. Downsample with Lanczos filter for pristine antialiasing
    master_512 = img.resize((512, 512), resample=Image.Resampling.LANCZOS)
    return master_512

def prepare_calibrated_3d_reference():
    M = np.float32([
        [SCALE_512, 0, 256.0 - CENTER_X_GT * SCALE_512],
        [0, SCALE_512, OFFSET_Y_512 - Y_MIN_GT * SCALE_512]
    ])
    
    b, g, r = cv2.split(ref_bgr)
    spill = (g > r) & (g > b) & (clean_char_mask > 0)
    g_clean = g.copy()
    g_clean[spill] = np.maximum(r[spill], b[spill])
    
    alpha_clean = cv2.GaussianBlur(clean_char_mask, (3, 3), 0)
    ref_rgba = cv2.merge([b, g_clean, r, alpha_clean])
    
    ref_512 = cv2.warpAffine(ref_rgba, M, (512, 512), flags=cv2.INTER_LANCZOS4)
    ref_crop_path = os.path.join(BRAIN_DIR, "aituko_3d_master_crop_512.png")
    cv2.imwrite(ref_crop_path, ref_512)
    return Image.fromarray(cv2.cvtColor(ref_512, cv2.COLOR_BGRA2RGBA))

def run_production():
    print("🎨 Rendering 100% spotless uniform porcelain master vector AItuko at 4x...")
    master_512 = render_flawless_master(scale=4)
    
    master_path = os.path.join(BRAIN_DIR, "aituko_master_exact_512.png")
    master_512.save(master_path, "PNG")
    print(f"  ✅ Saved {master_path}")
    
    ws_master_path = os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_master_exact_512.png")
    master_512.save(ws_master_path, "PNG")
    
    ref_img_raw = prepare_calibrated_3d_reference()
    ref_studio = Image.new("RGBA", (512, 512), (11, 15, 23, 255))
    ref_studio.paste(ref_img_raw, (0, 0), ref_img_raw)
    
    sbs = Image.new("RGBA", (1024, 512), (11, 15, 23, 255))
    sbs.paste(ref_studio, (0, 0))
    sbs.paste(master_512, (512, 0))
    
    sbs_draw = ImageDraw.Draw(sbs)
    sbs_draw.rectangle([16, 16, 360, 50], fill=(19, 26, 38, 230), outline=(34, 47, 68, 255))
    sbs_draw.text((28, 26), "MODELE 3D DE REFERENCE (STUDIO)", fill=(0, 240, 255, 255))
    
    sbs_draw.rectangle([528, 16, 950, 50], fill=(19, 26, 38, 230), outline=(16, 185, 129, 255))
    sbs_draw.text((540, 26), "MASTER VECTORIEL (PORCELAINE PURE SANS OMBRE)", fill=(52, 211, 153, 255))
    
    sbs_draw.line([(512, 0), (512, 512)], fill=(34, 47, 68, 255), width=2)
    
    sbs_path = os.path.join(BRAIN_DIR, "aituko_master_side_by_side.png")
    sbs.save(sbs_path, "PNG")
    print(f"  ✅ Saved {sbs_path}")
    
    ws_sbs_path = os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_master_side_by_side.png")
    sbs.save(ws_sbs_path, "PNG")

    overlay = Image.blend(ref_studio, master_512, alpha=0.5)
    overlay_path = os.path.join(BRAIN_DIR, "aituko_master_overlay_match.png")
    overlay.save(overlay_path, "PNG")
    print(f"  ✅ Saved {overlay_path}")

if __name__ == "__main__":
    run_production()
