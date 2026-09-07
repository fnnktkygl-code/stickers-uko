#!/usr/bin/env python3
"""
AItuko Official Vector Turnaround Model Sheet Generator.
Constructs the full 360° 4-view model sheet of the vector mascot:
1. 0° Face (Front View)
2. 45° Trois-Quarts (3/4 View)
3. 90° Profil (Side View)
4. 180° Dos (Back View)

Uses pure spotless uniform porcelain white (zero grey smudges/dirty shadows)
and strictly zero hands/fingers across all 4 angles.
"""

import os
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.render_exact_spline_master import render_flawless_master

BRAIN_DIR = "/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68"
WORKSPACE_DIR = "/Users/richard/Developer/Stickers Uko"
TURNAROUND_SRC = "mascots/aituko/aituko_master_turnaround.jpeg"

# Studio Colors
COLOR_BG = (11, 15, 23, 255)
COLOR_CARD = (17, 24, 39, 255)
COLOR_BORDER = (31, 41, 55, 255)
COLOR_CYAN = (0, 240, 255, 255)
COLOR_EMERALD = (52, 211, 153, 255)
COLOR_WHITE = (255, 255, 255, 255)
COLOR_MUTED = (148, 163, 184, 255)

PORCELAIN_FILL = (255, 255, 255, 255)
PORCELAIN_OUTLINE = (210, 220, 232, 255)
VISOR_GLASS = (12, 14, 20, 255)
VISOR_RIM = (28, 33, 46, 255)

def extract_view_contours(view_img_path, is_back=False):
    """Extracts clean contours for head, visor, eyes, torso, pods, feet."""
    rgba = cv2.imread(view_img_path, cv2.IMREAD_UNCHANGED)
    h, w, _ = rgba.shape
    alpha = rgba[:, :, 3]
    bgr = rgba[:, :, :3]
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    
    char_mask = (alpha > 80).astype(np.uint8) * 255
    char_mask = cv2.morphologyEx(char_mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    
    # 1. Total character contour(s)
    total_cnts, _ = cv2.findContours(char_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    total_cnts = [c for c in total_cnts if cv2.contourArea(c) > 200]
    
    # 2. Visor (if not back view)
    visor_cnts = []
    if not is_back:
        v_cand = (char_mask > 0) & (gray < 135)
        v_cand[int(h * 0.44):, :] = False  # only upper head
        v_mask = v_cand.astype(np.uint8) * 255
        v_mask = cv2.morphologyEx(v_mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
        vc, _ = cv2.findContours(v_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        visor_cnts = [c for c in vc if cv2.contourArea(c) > 600]
        
    # 3. Cyan Eyes (if not back view)
    eyes_cnts = []
    if not is_back:
        cyan_mask = (hsv[:, :, 0] >= 75) & (hsv[:, :, 0] <= 115) & (hsv[:, :, 1] >= 60) & (hsv[:, :, 2] >= 75)
        cyan_mask = cv2.morphologyEx(cyan_mask.astype(np.uint8) * 255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
        ec, _ = cv2.findContours(cyan_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        eyes_cnts = sorted([c for c in ec if cv2.contourArea(c) > 15], key=lambda c: cv2.boundingRect(c)[0])
        
    return {
        "h": h,
        "w": w,
        "total_cnts": total_cnts,
        "visor_cnts": visor_cnts,
        "eyes_cnts": eyes_cnts
    }

def render_vector_view(view_data, target_h=460, scale=3):
    """
    Renders a clean vector mascot view with pure spotless porcelain,
    crisp outlines, and glowing cyan eyes.
    """
    orig_h = view_data["h"]
    orig_w = view_data["w"]
    
    # Scale to target height
    s_factor = (target_h / float(orig_h)) * scale
    canvas_w = int(orig_w * s_factor) + 40 * scale
    canvas_h = int(target_h * scale) + 60 * scale
    
    img = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    offset_x = 20 * scale
    offset_y = 15 * scale
    
    def transform_pt(pt):
        x, y = pt
        return (int(round(x * s_factor + offset_x)), int(round(y * s_factor + offset_y)))
    
    # 1. Ground Shadow
    sh_layer = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(sh_layer)
    scx = canvas_w // 2
    scy = int(target_h * scale + 15 * scale)
    sh_draw.ellipse([scx - int(45 * scale), scy - int(6 * scale), scx + int(45 * scale), scy + int(6 * scale)], fill=(0, 0, 0, 140))
    sh_layer = sh_layer.filter(ImageFilter.GaussianBlur(radius=6 * scale))
    img.alpha_composite(sh_layer)
    
    # 2. Total Porcelain Silhouette (Pure Spotless Uniform White)
    for c in view_data["total_cnts"]:
        approx = cv2.approxPolyDP(c, 0.8, True)
        pts = [transform_pt(p[0]) for p in approx]
        if len(pts) >= 3:
            draw.polygon(pts, fill=PORCELAIN_FILL, outline=PORCELAIN_OUTLINE, width=max(1, int(1.2 * scale)))
            
    # 3. Visor Faceplate (if any)
    for vc in view_data["visor_cnts"]:
        approx = cv2.approxPolyDP(vc, 0.8, True)
        pts = [transform_pt(p[0]) for p in approx]
        if len(pts) >= 3:
            draw.polygon(pts, fill=VISOR_GLASS, outline=VISOR_RIM, width=max(1, int(1.5 * scale)))
            
    # 4. Cyan Eyes with Multi-Stage Bloom (if any)
    if view_data["eyes_cnts"]:
        wb_layer = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
        wb_draw = ImageDraw.Draw(wb_layer)
        mb_layer = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
        mb_draw = ImageDraw.Draw(mb_layer)
        core_layer = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
        core_draw = ImageDraw.Draw(core_layer)
        
        for ec in view_data["eyes_cnts"]:
            approx = cv2.approxPolyDP(ec, 0.6, True)
            pts = [transform_pt(p[0]) for p in approx]
            if len(pts) >= 3:
                wb_draw.polygon(pts, fill=(0, 240, 255, 140))
                mb_draw.polygon(pts, fill=(0, 240, 255, 220))
                core_draw.polygon(pts, fill=(0, 245, 255, 255))
                
        wb_layer = wb_layer.filter(ImageFilter.GaussianBlur(radius=8 * scale))
        mb_layer = mb_layer.filter(ImageFilter.GaussianBlur(radius=4 * scale))
        img.alpha_composite(wb_layer)
        img.alpha_composite(mb_layer)
        img.alpha_composite(core_layer)
        
    # Downsample with Lanczos for antialiasing
    final_w = canvas_w // scale
    final_h = canvas_h // scale
    return img.resize((final_w, final_h), resample=Image.Resampling.LANCZOS)

def build_official_turnaround_sheet():
    print("📐 Generating official 4-view turnaround model sheet...")
    
    # 1. Generate the 4 views
    # View 1: 0° Face (from our verified 100% fidelity master model)
    view_front = render_flawless_master(scale=4)
    # Crop to content box
    v1_img = view_front.crop((100, 25, 412, 500))  # ~312x475
    
    # Views 2, 3, 4: from turnaround source
    data_3q = extract_view_contours("scratch/turnaround_views/three_quarter_clean.png", is_back=False)
    v2_img = render_vector_view(data_3q, target_h=440, scale=3)
    
    data_prof = extract_view_contours("scratch/turnaround_views/profile_clean.png", is_back=False)
    v3_img = render_vector_view(data_prof, target_h=440, scale=3)
    
    data_back = extract_view_contours("scratch/turnaround_views/back_clean.png", is_back=True)
    v4_img = render_vector_view(data_back, target_h=440, scale=3)
    
    # 2. Compose the Studio Turnaround Board (1920 x 820)
    SHEET_W = 1920
    SHEET_H = 820
    sheet = Image.new("RGBA", (SHEET_W, SHEET_H), COLOR_BG)
    draw = ImageDraw.Draw(sheet)
    
    # Header Banner
    draw.rectangle([0, 0, SHEET_W, 90], fill=(15, 23, 42, 255))
    draw.line([(0, 90), (SHEET_W, 90)], fill=COLOR_BORDER, width=2)
    
    draw.text((40, 22), "AITUKO — PLANCHE DE TURNAROUND DU MODELE VECTORIEL (360° MASTER)", fill=COLOR_CYAN)
    draw.text((40, 52), "Modele de Reference Geometrique Officiel — 4 Vues Orthographiques Calibrees — Porcelaine Blanche Pure & Zero Mains", fill=COLOR_MUTED)
    
    # Column Parameters
    cols = [
        {"angle": "0°", "name": "VUE DE FACE (FRONT)", "desc": "Visor 2 yeux cyan, 2 pods lateraux, 2 pieds V", "img": v1_img},
        {"angle": "45°", "name": "TROIS-QUARTS (3/4)", "desc": "Visor galbe oblique, perspective yeux & pods", "img": v2_img},
        {"angle": "90°", "name": "PROFIL (SIDE)", "desc": "Arc facial convexe, 1 oeil profil, pod centre", "img": v3_img},
        {"angle": "180°", "name": "VUE DE DOS (BACK)", "desc": "Porcelaine pure complete (zero ecran/yeux)", "img": v4_img}
    ]
    
    col_w = SHEET_W // 4
    guide_y_top = 180
    guide_y_eye = 265
    guide_y_neck = 360
    guide_y_torso = 550
    guide_y_feet = 645
    
    # Draw horizontal alignment guide lines across the entire board
    guides = [
        (guide_y_top, "SOMMET CASQUE", (52, 211, 153, 90)),
        (guide_y_eye, "HORIZON YEUX", (0, 240, 255, 90)),
        (guide_y_neck, "EMBOITEMENT COU", (148, 163, 184, 80)),
        (guide_y_torso, "BASE TORSE", (148, 163, 184, 80)),
        (guide_y_feet, "SUSTENTATION SOL", (0, 240, 255, 110))
    ]
    
    for gy, glabel, gcolor in guides:
        # Dashed guide line
        for gx in range(40, SHEET_W - 40, 16):
            draw.line([(gx, gy), (gx + 8, gy)], fill=gcolor, width=1)
        draw.text((SHEET_W - 170, gy - 12), glabel, fill=gcolor)
        
    # Place the 4 Figures in their columns
    for i, col in enumerate(cols):
        cx = i * col_w
        # Card Background
        card_rect = [cx + 15, 110, cx + col_w - 15, SHEET_H - 25]
        draw.rectangle(card_rect, fill=(17, 24, 39, 140), outline=(31, 41, 55, 200), width=1)
        
        # Column Title Banner
        draw.rectangle([cx + 25, 120, cx + col_w - 25, 158], fill=(15, 23, 42, 230), outline=(0, 240, 255, 120) if i==0 else (52, 211, 153, 80))
        draw.text((cx + 38, 130), f"{col['angle']} — {col['name']}", fill=COLOR_CYAN if i==0 else COLOR_EMERALD)
        
        # Paste mascot image centered vertically to align with guides
        fig = col["img"]
        fw, fh = fig.size
        px = cx + (col_w - fw) // 2
        py = guide_y_top - 20
        sheet.paste(fig, (px, py), fig)
        
        # Bottom Description Tag
        draw.rectangle([cx + 25, SHEET_H - 65, cx + col_w - 25, SHEET_H - 35], fill=(15, 23, 42, 200), outline=(31, 41, 55, 255))
        draw.text((cx + 35, SHEET_H - 55), col["desc"], fill=COLOR_MUTED)
        
        # Column Separator Line
        if i > 0:
            draw.line([(cx, 90), (cx, SHEET_H)], fill=(31, 41, 55, 180), width=1)
            
    # Save Master Turnaround Sheet
    out_png_brain = os.path.join(BRAIN_DIR, "aituko_vector_turnaround_sheet.png")
    sheet.save(out_png_brain, "PNG")
    print(f"✅ Saved official turnaround sheet to {out_png_brain}")
    
    out_png_ws = os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_vector_turnaround_sheet.png")
    sheet.save(out_png_ws, "PNG")
    print(f"✅ Saved official turnaround sheet to {out_png_ws}")
    
    return out_png_brain

if __name__ == "__main__":
    build_official_turnaround_sheet()
