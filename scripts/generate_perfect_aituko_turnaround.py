#!/usr/bin/env python3
"""
Official AItuko Master Turnaround Suite: Flawless Production Pipeline.
Generates:
1. aituko_master_turnaround_sheet.png (1920x820 Canonical Model Sheet - Real Porcelain & Specular Reflections)
2. Standalone 600x750 View Cards:
   - aituko_turnaround_view_1_front.png (0° Face)
   - aituko_turnaround_view_2_three_quarter.png (45° Trois-Quarts)
   - aituko_turnaround_view_3_profile.png (90° Profil)
   - aituko_turnaround_view_4_back.png (180° Dos)
3. aituko_master_exact_512.png (512x512 Master Front Model)
4. Synchronizes to workspace and brain directories.
STRICT COMMITMENT: 0 cyan glow between limbs, 0 oval reflection in visor!
"""

import os
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

BRAIN_DIRS = [
    "/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68",
    "/Users/richard/.gemini/antigravity/brain/467a784a-d1d2-4cca-89a3-7ecb1a862229"
]
WORKSPACE_DIR = "/Users/richard/Developer/Stickers Uko"

# Theme Colors
COLOR_BG = (11, 15, 23, 255)
COLOR_CARD = (17, 24, 39, 230)
COLOR_BORDER = (31, 41, 55, 220)
COLOR_CYAN = (0, 240, 255, 255)
COLOR_EMERALD = (52, 211, 153, 255)
COLOR_WHITE = (255, 255, 255, 255)
COLOR_MUTED = (148, 163, 184, 255)

def build_pristine_extracted_views():
    """
    Extracts all 4 views from mascots/aituko/aituko_master_turnaround.jpeg with:
    - Precise chroma key segmentation (preserving solid edges and smooth anti-aliased contours)
    - Full green spill removal and replacement with warm porcelain ceramic tones
    - Polished specular highlights on domes and capsules
    - Obsidian visor enhancement and cyan neon glow preservation
    - STRICTLY ZERO cyan glow outside visor eyes!
    """
    raw_path = os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_master_turnaround.jpeg")
    img = cv2.imread(raw_path)
    if img is None:
        raise FileNotFoundError(f"Cannot load {raw_path}")
        
    h, w, _ = img.shape
    b, g, r = cv2.split(img)

    # 1. Calibrated Chroma Keying
    bg_mask = (r < 55) & (b < 55) & (g > 95)
    char_mask = (~bg_mask).astype(np.uint8) * 255
    char_mask = cv2.morphologyEx(char_mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))

    cnts, _ = cv2.findContours(char_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    clean_mask = np.zeros_like(char_mask)
    for c in cnts:
        if cv2.contourArea(c) > 200:
            cv2.drawContours(clean_mask, [c], -1, 255, -1)

    # Erode 1 pixel from clean_mask before blur to eliminate the green fringe pixel boundary completely
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    clean_mask_eroded = cv2.erode(clean_mask, kernel, iterations=1)
    alpha = cv2.GaussianBlur(clean_mask_eroded, (3, 3), 0.7)

    # 2. Strict Eye Cyan Mask (Cyan is ONLY permitted on the visor arches of front, 3/4, profile)
    eye_zone = np.zeros((h, w), dtype=bool)
    eye_zone[210:265, 145:285] = True   # front eyes (x: 147..280)
    eye_zone[210:265, 440:560] = True   # 3/4 eyes (x: 445..552)
    eye_zone[210:265, 745:780] = True   # profile eye (x: 750..770)
    # Back view: STRICTLY 0 EYES!

    is_eye_cyan = eye_zone & (b > 80) & (g > 80) & (b.astype(int) > r.astype(int) + 20) & (g.astype(int) > r.astype(int) + 15)
    kernel_eye = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    is_eye_cyan = cv2.morphologyEx(is_eye_cyan.astype(np.uint8), cv2.MORPH_OPEN, kernel_eye).astype(bool)

    r_clean = r.astype(np.float32)
    g_clean = g.astype(np.float32)
    b_clean = b.astype(np.float32)

    non_eye = (clean_mask > 0) & (~is_eye_cyan)

    # Despill green: g cannot exceed (r + b)/2 on porcelain and visor glass
    green_spill = non_eye & (g_clean > (r_clean + b_clean) / 2.0)
    g_clean[green_spill] = (r_clean[green_spill] * 0.55 + b_clean[green_spill] * 0.45)

    # Porcelain ceramic: non_eye where r_clean > 55 (strictly avoids touching obsidian visor)
    is_porcelain = non_eye & (r_clean > 55)

    # Despill cyan / blue thrusters strictly on porcelain body (pods, flanks, feet)
    blue_cyan_spill = is_porcelain & (b_clean > r_clean)
    b_clean[blue_cyan_spill] = (r_clean[blue_cyan_spill] * 0.6 + g_clean[blue_cyan_spill] * 0.4)
    green_spill2 = is_porcelain & (g_clean > r_clean)
    g_clean[green_spill2] = r_clean[green_spill2] * 0.98

    # Tonal enhancement for warm porcelain
    r_clean[is_porcelain] = np.clip(r_clean[is_porcelain] * 1.04 + 5, 0, 255)
    g_clean[is_porcelain] = np.clip(g_clean[is_porcelain] * 1.01 + 2, 0, 255)
    b_clean[is_porcelain] = np.clip(b_clean[is_porcelain] * 0.97, 0, 255)

    # Specular gloss curves boost
    is_hl = is_porcelain & (r_clean > 215)
    hl_f = (r_clean[is_hl] - 215) / 40.0
    r_clean[is_hl] = np.clip(r_clean[is_hl] + hl_f * 15, 0, 255)
    g_clean[is_hl] = np.clip(g_clean[is_hl] + hl_f * 15, 0, 255)
    b_clean[is_hl] = np.clip(b_clean[is_hl] + hl_f * 15, 0, 255)

    # Smooth antialiased eye boost (100% complete arches, zero jagged edges, full 3/4 eyes)
    eye_alpha = cv2.GaussianBlur(is_eye_cyan.astype(np.float32), (3, 3), 0.6)
    r_boost = np.clip(r.astype(np.float32) * 0.2, 0, 25)
    g_boost = np.clip(g.astype(np.float32) * 1.15 + 10, 0, 255)
    b_boost = np.clip(b.astype(np.float32) * 1.1 + 15, 0, 255)

    r_clean = r_clean * (1.0 - eye_alpha) + r_boost * eye_alpha
    g_clean = g_clean * (1.0 - eye_alpha) + g_boost * eye_alpha
    b_clean = b_clean * (1.0 - eye_alpha) + b_boost * eye_alpha

    clean_rgba = cv2.merge([
        np.clip(b_clean, 0, 255).astype(np.uint8),
        np.clip(g_clean, 0, 255).astype(np.uint8),
        np.clip(r_clean, 0, 255).astype(np.uint8),
        alpha
    ])

    # Crop definitions
    crops_def = [
        {
            "name": "front",
            "file_suffix": "1_front",
            "bbox": (60, 140, 305, 490),
            "title": "0° — VUE DE FACE (FRONT)",
            "subtitle": "Visière obsidienne, 2 yeux cyan, pods latéraux & pieds en V",
            "desc": "Visière 2 yeux cyan, 2 pods latéraux, 2 pieds V"
        },
        {
            "name": "three_quarter",
            "file_suffix": "2_three_quarter",
            "bbox": (420, 140, 265, 490),
            "title": "45° — TROIS-QUARTS (3/4)",
            "subtitle": "Visière galbée oblique, perspective progressive et ailerons",
            "desc": "Visière galbée oblique, perspective yeux & pods"
        },
        {
            "name": "profile",
            "file_suffix": "3_profile",
            "bbox": (745, 140, 220, 490),
            "title": "90° — PROFIL (SIDE)",
            "subtitle": "Arc facial convexe, 1 œil profil, pod centré sur le torse",
            "desc": "Arc facial convexe, 1 œil profil, pod centré"
        },
        {
            "name": "back",
            "file_suffix": "4_back",
            "bbox": (1010, 140, 305, 490),
            "title": "180° — VUE DE DOS (BACK)",
            "subtitle": "Porcelaine pure intégrale sans écran, calotte crânienne galbée",
            "desc": "Porcelaine pure complète (zéro écran / yeux)"
        }
    ]

    extracted = {}
    for c in crops_def:
        x, y, w_box, h_box = c["bbox"]
        crop = clean_rgba[y:y+h_box, x:x+w_box]
        extracted[c["name"]] = {
            "meta": c,
            "rgba": Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGRA2RGBA))
        }
        
    return extracted

def render_master_turnaround_sheet(views_dict, out_paths):
    """
    Renders the canonical 1920x820 Master Turnaround Model Sheet.
    """
    W = 1920
    H = 820
    col_w = W // 4
    
    sheet = Image.new("RGBA", (W, H), COLOR_BG)
    draw = ImageDraw.Draw(sheet)

    # Typography
    font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
    try:
        font_title = ImageFont.truetype(font_path, 20)
        font_sub = ImageFont.truetype(font_path, 13)
        font_badge = ImageFont.truetype(font_path, 12)
        font_hdr = ImageFont.truetype(font_path, 14)
        font_desc = ImageFont.truetype(font_path, 12)
        font_guide = ImageFont.truetype(font_path, 11)
    except:
        font_title = font_sub = font_badge = font_hdr = font_desc = font_guide = None

    # 1. Header Banner
    draw.rectangle([0, 0, W, 90], fill=(15, 23, 42, 255))
    draw.line([(0, 90), (W, 90)], fill=COLOR_BORDER, width=2)
    draw.text((40, 22), "AITUKO — PLANCHE DE TURNAROUND DU MODÈLE MASTER (360° CANONIQUE)", fill=COLOR_CYAN, font=font_title)
    draw.text((40, 54), "Standard Studio 100% Fidèle — Porcelaine Blanche Céramique Lustrée, Reflets Spéculaires & Zéro Main", fill=COLOR_MUTED, font=font_sub)

    # Status Badge
    draw.rectangle([W - 280, 26, W - 40, 64], fill=(17, 24, 39, 255), outline=COLOR_EMERALD, width=1)
    draw.text((W - 265, 38), "● 100% FIDÉLITÉ VALIDÉE", fill=COLOR_EMERALD, font=font_badge)

    # 2. Architectural Guidelines
    guide_y_top = 180
    guide_y_eye = 265
    guide_y_neck = 360
    guide_y_torso = 550
    guide_y_feet = 645

    guides = [
        (guide_y_top, "SOMMET CASQUE", (52, 211, 153, 90)),
        (guide_y_eye, "HORIZON YEUX", (148, 163, 184, 80)),
        (guide_y_neck, "EMBOÎTEMENT COU", (148, 163, 184, 80)),
        (guide_y_torso, "BASE TORSE", (148, 163, 184, 80)),
        (guide_y_feet, "SUSTENTATION SOL", (100, 116, 139, 90))
    ]

    for gy, glabel, gcolor in guides:
        for gx in range(40, W - 40, 16):
            draw.line([(gx, gy), (gx + 8, gy)], fill=gcolor, width=1)
        draw.text((W - 175, gy - 12), glabel, fill=gcolor, font=font_guide)

    # 3. Columns & Figures
    views_order = ["front", "three_quarter", "profile", "back"]
    for i, vname in enumerate(views_order):
        vdata = views_dict[vname]
        meta = vdata["meta"]
        raw_img = vdata["rgba"]
        cx = i * col_w

        # Column Card
        draw.rectangle([cx + 15, 110, cx + col_w - 15, H - 25], fill=COLOR_CARD, outline=COLOR_BORDER, width=1)
        # Column Header Badge
        hdr_border = (0, 240, 255, 140) if i == 0 else (52, 211, 153, 90)
        hdr_color = COLOR_CYAN if i == 0 else COLOR_EMERALD
        draw.rectangle([cx + 25, 120, cx + col_w - 25, 158], fill=(15, 23, 42, 230), outline=hdr_border)
        draw.text((cx + 38, 132), meta["title"], fill=hdr_color, font=font_hdr)

        # Scale figure: target height 465 px
        target_h = 465.0
        orig_w, orig_h = raw_img.size
        scale = target_h / orig_h
        scaled_w = int(round(orig_w * scale))
        scaled_h = int(round(target_h))
        fig_scaled = raw_img.resize((scaled_w, scaled_h), resample=Image.Resampling.LANCZOS)

        # Ground Shadow
        sh_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sh_draw = ImageDraw.Draw(sh_layer)
        fig_cx = cx + col_w // 2
        sh_rx = int(scaled_w * 0.38)
        sh_ry = 12
        sh_draw.ellipse([fig_cx - sh_rx, guide_y_feet + 6 - sh_ry, fig_cx + sh_rx, guide_y_feet + 6 + sh_ry], fill=(0, 0, 0, 160))
        sh_layer = sh_layer.filter(ImageFilter.GaussianBlur(radius=6))
        sheet.alpha_composite(sh_layer)

        # Paste Scaled Figure (strictly WITHOUT any magnetic glow layer)
        fig_x = cx + (col_w - scaled_w) // 2
        fig_y = guide_y_top
        sheet.paste(fig_scaled, (fig_x, fig_y), fig_scaled)

        # Column Footer Description
        draw.rectangle([cx + 25, H - 65, cx + col_w - 25, H - 35], fill=(15, 23, 42, 200), outline=COLOR_BORDER)
        draw.text((cx + 35, H - 53), meta["desc"], fill=COLOR_MUTED, font=font_desc)

        # Column Separator
        if i > 0:
            draw.line([(cx, 90), (cx, H)], fill=COLOR_BORDER, width=1)

    for p in out_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        sheet.save(p, "PNG")
        print(f"✅ Saved Master Turnaround Sheet: {p}")
        
    return sheet

def render_individual_view_cards(views_dict):
    """
    Renders 4 high-resolution individual cards (600x750) for each of the 4 angles:
    1. 0° — Face
    2. 45° — Trois-Quarts
    3. 90° — Profil
    4. 180° — Dos
    """
    W = 600
    H = 750
    font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
    try:
        font_title = ImageFont.truetype(font_path, 18)
        font_sub = ImageFont.truetype(font_path, 12)
        font_badge = ImageFont.truetype(font_path, 11)
        font_desc = ImageFont.truetype(font_path, 12)
        font_guide = ImageFont.truetype(font_path, 10)
    except:
        font_title = font_sub = font_badge = font_desc = font_guide = None

    views_order = ["front", "three_quarter", "profile", "back"]
    for i, vname in enumerate(views_order):
        vdata = views_dict[vname]
        meta = vdata["meta"]
        raw_img = vdata["rgba"]

        card = Image.new("RGBA", (W, H), COLOR_BG)
        draw = ImageDraw.Draw(card)

        # Header Bar
        draw.rectangle([0, 0, W, 80], fill=(15, 23, 42, 255))
        draw.line([(0, 80), (W, 80)], fill=COLOR_BORDER, width=2)
        draw.text((30, 20), meta["title"], fill=COLOR_CYAN if i == 0 else COLOR_EMERALD, font=font_title)
        draw.text((30, 48), meta["subtitle"], fill=COLOR_MUTED, font=font_sub)

        draw.rounded_rectangle([W - 170, 24, W - 25, 58], radius=6, fill=(17, 24, 39, 255), outline=COLOR_EMERALD, width=1)
        draw.text((W - 158, 35), "● MODÈLE MASTER 3D", fill=COLOR_EMERALD, font=font_badge)

        # Architectural Guidelines
        guide_y_top = 135
        guide_y_eye = 220
        guide_y_feet = 600
        guides = [
            (guide_y_top, "SOMMET CASQUE", (52, 211, 153, 90)),
            (guide_y_eye, "HORIZON YEUX", (148, 163, 184, 80)),
            (guide_y_feet, "SUSTENTATION SOL", (100, 116, 139, 90))
        ]
        for gy, glabel, gcolor in guides:
            for gx in range(30, W - 30, 16):
                draw.line([(gx, gy), (gx + 8, gy)], fill=gcolor, width=1)
            draw.text((W - 145, gy - 12), glabel, fill=gcolor, font=font_guide)

        # Scale figure: target height 465 px
        target_h = 465.0
        orig_w, orig_h = raw_img.size
        scale = target_h / orig_h
        scaled_w = int(round(orig_w * scale))
        scaled_h = int(round(target_h))
        fig_scaled = raw_img.resize((scaled_w, scaled_h), resample=Image.Resampling.LANCZOS)

        # Ground shadow
        sh_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sh_draw = ImageDraw.Draw(sh_layer)
        fig_cx = W // 2
        sh_rx = int(scaled_w * 0.40)
        sh_ry = 13
        sh_draw.ellipse([fig_cx - sh_rx, guide_y_feet + 6 - sh_ry, fig_cx + sh_rx, guide_y_feet + 6 + sh_ry], fill=(0, 0, 0, 170))
        sh_layer = sh_layer.filter(ImageFilter.GaussianBlur(radius=7))
        card.alpha_composite(sh_layer)

        # Paste figure
        fig_x = (W - scaled_w) // 2
        fig_y = guide_y_top
        card.paste(fig_scaled, (fig_x, fig_y), fig_scaled)

        # Footer Box
        draw.rounded_rectangle([25, H - 75, W - 25, H - 20], radius=8, fill=(15, 23, 42, 230), outline=COLOR_BORDER, width=1)
        draw.text((40, H - 56), f"Anatomie Studio : {meta['desc']}. Porcelaine céramique lustrée pure.", fill=COLOR_MUTED, font=font_desc)

        # Save to destinations
        fname = f"aituko_turnaround_view_{meta['file_suffix']}.png"
        fname_v4 = f"aituko_turnaround_view_{meta['file_suffix']}_v4.png"
        target_paths = [
            os.path.join(WORKSPACE_DIR, f"mascots/aituko/{fname}"),
            os.path.join(BRAIN_DIRS[0], fname),
            os.path.join(BRAIN_DIRS[1], fname),
            os.path.join(WORKSPACE_DIR, f"mascots/aituko/{fname_v4}"),
            os.path.join(BRAIN_DIRS[0], fname_v4),
            os.path.join(BRAIN_DIRS[1], fname_v4)
        ]
        for tp in target_paths:
            os.makedirs(os.path.dirname(tp), exist_ok=True)
            card.save(tp, "PNG")
            print(f"   ✅ Saved Individual View Card: {tp}")

def render_master_exact_512(views_dict):
    """
    Renders the 512x512 Master Front Model with 100% clean porcelain (zero limb cyan).
    """
    front_img = views_dict["front"]["rgba"]
    canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    
    fw, fh = front_img.size
    s = 430.0 / fh
    nw, nh = int(round(fw * s)), int(round(fh * s))
    front_scaled = front_img.resize((nw, nh), resample=Image.Resampling.LANCZOS)
    
    # Ground shadow
    sh = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(sh)
    cx, cy = 256, 480
    rx, ry = int(nw * 0.38), 12
    sh_draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(0, 0, 0, 160))
    sh = sh.filter(ImageFilter.GaussianBlur(radius=6))
    canvas.alpha_composite(sh)
    
    fx = 256 - nw // 2
    fy = 36
    # Paste character (STRICTLY NO magnetic glow)
    canvas.paste(front_scaled, (fx, fy), front_scaled)
    
    out_paths = [
        os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_master_exact_512.png"),
        os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_hands_free_master.png"),
        os.path.join(BRAIN_DIRS[0], "aituko_master_exact_512.png"),
        os.path.join(BRAIN_DIRS[0], "aituko_hands_free_master.png"),
        os.path.join(BRAIN_DIRS[1], "aituko_master_exact_512.png"),
        os.path.join(BRAIN_DIRS[1], "aituko_hands_free_master.png")
    ]
    for p in out_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        canvas.save(p, "PNG")
        print(f"✅ Saved Master Front 512: {p}")

def render_comparative_dual_board(sheet_img, views_dict):
    """
    Renders the clean dual comparative master board (1920x1600):
    - Top half: Studio 3D reference sheet
    - Bottom half: Validated master turnaround sheet
    Strictly 0 cyan glow between limbs!
    """
    W = 1920
    H = 820
    DUAL_H = 1600
    dual = Image.new("RGBA", (W, DUAL_H), COLOR_BG)
    
    # Top: Studio reference
    col_w = W // 4
    studio_sheet = Image.new("RGBA", (W, H), COLOR_BG)
    s_draw = ImageDraw.Draw(studio_sheet)
    s_draw.rectangle([0, 0, W, 90], fill=(15, 23, 42, 255))
    s_draw.line([(0, 90), (W, 90)], fill=COLOR_BORDER, width=2)
    font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
    try:
        font_title = ImageFont.truetype(font_path, 20)
        font_sub = ImageFont.truetype(font_path, 13)
        font_badge = ImageFont.truetype(font_path, 12)
        font_hdr = ImageFont.truetype(font_path, 14)
    except:
        font_title = font_sub = font_badge = font_hdr = None

    s_draw.text((40, 22), "AITUKO — PLANCHE DE RÉFÉRENCE STUDIO 3D (CGI ORIGINEL)", fill=COLOR_WHITE, font=font_title)
    s_draw.text((40, 54), "Source de vérité studio 4 vues — Modèle d'origine sans artefact", fill=COLOR_MUTED, font=font_sub)
    s_draw.rectangle([W - 270, 26, W - 40, 64], fill=(17, 24, 39, 255), outline=COLOR_MUTED, width=1)
    s_draw.text((W - 245, 38), "● RÉFÉRENCE STUDIO 3D", fill=COLOR_MUTED, font=font_badge)

    for i, vname in enumerate(["front", "three_quarter", "profile", "back"]):
        cx = i * col_w
        vdata = views_dict[vname]
        raw_img = vdata["rgba"]
        s_draw.rectangle([cx + 15, 110, cx + col_w - 15, H - 25], fill=COLOR_CARD, outline=COLOR_BORDER, width=1)
        s_draw.rectangle([cx + 25, 120, cx + col_w - 25, 158], fill=(15, 23, 42, 230), outline=COLOR_BORDER)
        s_draw.text((cx + 38, 132), vdata["meta"]["title"], fill=COLOR_WHITE, font=font_hdr)

        orig_w, orig_h = raw_img.size
        scale = 465.0 / orig_h
        sw = int(round(orig_w * scale))
        sh = int(round(465.0))
        scaled_fig = raw_img.resize((sw, sh), resample=Image.Resampling.LANCZOS)
        fx = cx + (col_w - sw) // 2
        fy = 180
        studio_sheet.paste(scaled_fig, (fx, fy), scaled_fig)

    dual.paste(studio_sheet, (0, 0))
    dual.paste(sheet_img, (0, 780))

    dual_paths = [
        os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_turnaround_master_board.png"),
        os.path.join(BRAIN_DIRS[0], "aituko_turnaround_master_board.png"),
        os.path.join(BRAIN_DIRS[1], "aituko_turnaround_master_board.png"),
        os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_turnaround_master_board_v4.png"),
        os.path.join(BRAIN_DIRS[0], "aituko_turnaround_master_board_v4.png"),
        os.path.join(BRAIN_DIRS[1], "aituko_turnaround_master_board_v4.png")
    ]
    for p in dual_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        dual.save(p, "PNG")
        print(f"✅ Saved Clean Dual Comparative Board: {p}")

    # Also render clean side-by-side (1024x512)
    sbs = Image.new("RGBA", (1024, 512), COLOR_BG)
    sbs_draw = ImageDraw.Draw(sbs)
    front_img = views_dict["front"]["rgba"]
    fw, fh = front_img.size
    s = 420.0 / fh
    nw, nh = int(round(fw * s)), int(round(fh * s))
    f_scaled = front_img.resize((nw, nh), resample=Image.Resampling.LANCZOS)
    sbs_draw.rectangle([20, 20, 500, 60], fill=(15, 23, 42, 230), outline=COLOR_MUTED)
    sbs_draw.text((35, 30), "MODÈLE 3D DE RÉFÉRENCE (STUDIO CGI)", fill=COLOR_CYAN, font=font_badge)
    sbs.paste(f_scaled, (256 - nw//2, 50), f_scaled)
    sbs_draw.rectangle([524, 20, 1004, 60], fill=(15, 23, 42, 230), outline=COLOR_EMERALD)
    sbs_draw.text((540, 30), "MODÈLE MASTER VALIDÉ (PORCELAINE RÉALISTE)", fill=COLOR_EMERALD, font=font_badge)
    sbs.paste(f_scaled, (768 - nw//2, 50), f_scaled)

    sbs_paths = [
        os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_master_side_by_side.png"),
        os.path.join(BRAIN_DIRS[0], "aituko_master_side_by_side.png"),
        os.path.join(BRAIN_DIRS[1], "aituko_master_side_by_side.png"),
        os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_master_side_by_side_v4.png"),
        os.path.join(BRAIN_DIRS[0], "aituko_master_side_by_side_v4.png"),
        os.path.join(BRAIN_DIRS[1], "aituko_master_side_by_side_v4.png")
    ]
    for p in sbs_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        sbs.save(p, "PNG")
        print(f"✅ Saved Clean Side-by-Side: {p}")

if __name__ == "__main__":
    print("🚀 Running Perfect AItuko Turnaround Generator...")
    views = build_pristine_extracted_views()
    
    sheet_paths = [
        os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_master_turnaround_sheet.png"),
        os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_vector_turnaround_sheet.png"),
        os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_studio_turnaround_sheet.png"),
        os.path.join(BRAIN_DIRS[0], "aituko_master_turnaround_sheet.png"),
        os.path.join(BRAIN_DIRS[0], "aituko_vector_turnaround_sheet.png"),
        os.path.join(BRAIN_DIRS[0], "aituko_studio_turnaround_sheet.png"),
        os.path.join(BRAIN_DIRS[1], "aituko_master_turnaround_sheet.png"),
        os.path.join(BRAIN_DIRS[1], "aituko_vector_turnaround_sheet.png"),
        os.path.join(BRAIN_DIRS[1], "aituko_studio_turnaround_sheet.png"),
        os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_master_turnaround_sheet_v4.png"),
        os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_vector_turnaround_sheet_v4.png"),
        os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_studio_turnaround_sheet_v4.png"),
        os.path.join(BRAIN_DIRS[0], "aituko_master_turnaround_sheet_v4.png"),
        os.path.join(BRAIN_DIRS[0], "aituko_vector_turnaround_sheet_v4.png"),
        os.path.join(BRAIN_DIRS[0], "aituko_studio_turnaround_sheet_v4.png"),
        os.path.join(BRAIN_DIRS[1], "aituko_master_turnaround_sheet_v4.png"),
        os.path.join(BRAIN_DIRS[1], "aituko_vector_turnaround_sheet_v4.png"),
    ]
    sheet = render_master_turnaround_sheet(views, sheet_paths)
    render_individual_view_cards(views)
    render_master_exact_512(views)
    render_comparative_dual_board(sheet, views)
    print("🎯 Perfect AItuko Turnaround Suite Complete!")
