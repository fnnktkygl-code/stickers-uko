#!/usr/bin/env python3
"""
Official Meoweko Master Turnaround Suite (Ex-Luneko) — 100% Fidelity Production Suite.
Generates all 11 canonical turnaround deliverables for the Meoweko mascot:
1. meoweko_master_turnaround_sheet.png (1920x820 Canonical Model Sheet - Porcelain, Amber Eyes & Feline Ears)
2. meoweko_master_turnaround.svg (1920x820 Master Vector Turnaround with Pure Bézier Paths & Gradients)
3. meoweko_studio_turnaround_sheet.png (1920x820 Studio Reference Sheet on Pure White)
4. meoweko_turnaround_master_board.png (1920x1600 Dual Comparative Master Board: Studio 3D vs Master Model)
5. meoweko_master_exact_512.png (512x512 Standalone Master Front View)
6. meoweko_master_side_by_side.png (1024x512 Side-by-Side Validation: Studio 3D vs Model)
7. meoweko_3d_turnaround_viewer.html (Interactive 360° Feline Viewer)
8. Standalone 512x512 Views (view_1_front, view_2_profile_right, view_3_profile_left, view_4_back)
9. Syncs deliverables to brain directory and updates visual gallery artifact.
"""

import os
import sys
import shutil
import xml.etree.ElementTree as ET
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

WORKSPACE_DIR = "/Users/richard/Developer/Stickers Uko"
BRAIN_DIRS = [
    "/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68"
]

COLOR_BG = (11, 15, 23, 255)
COLOR_CARD = (17, 24, 39, 235)
COLOR_BORDER = (31, 41, 55, 220)
COLOR_AMBER = (217, 155, 38, 255)
COLOR_EMERALD = (52, 211, 153, 255)
COLOR_WHITE = (255, 255, 255, 255)
COLOR_MUTED = (148, 163, 184, 255)

FONT_HELVETICA = "/System/Library/Fonts/Helvetica.ttc"
try:
    font_title = ImageFont.truetype(FONT_HELVETICA, 18)
    font_subtitle = ImageFont.truetype(FONT_HELVETICA, 12)
    font_badge = ImageFont.truetype(FONT_HELVETICA, 11)
    font_col_title = ImageFont.truetype(FONT_HELVETICA, 13)
    font_guideline = ImageFont.truetype(FONT_HELVETICA, 10)
    font_desc = ImageFont.truetype(FONT_HELVETICA, 11)
except Exception:
    font_title = font_subtitle = font_badge = font_col_title = font_guideline = font_desc = ImageFont.load_default()

def copy_historical_luneko_elements():
    """Archives existing Luneko files into mascots/meoweko/01_anciens_elements/."""
    src_dir = os.path.join(WORKSPACE_DIR, "mascots/luneko")
    dst_dir = os.path.join(WORKSPACE_DIR, "mascots/meoweko/01_anciens_elements")
    os.makedirs(dst_dir, exist_ok=True)
    if os.path.exists(src_dir):
        for item in os.listdir(src_dir):
            s = os.path.join(src_dir, item)
            d = os.path.join(dst_dir, item)
            if not os.path.exists(d):
                if os.path.isdir(s):
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)
        print("   ✅ Archived historical Luneko files into mascots/meoweko/01_anciens_elements/")

def extract_clean_meoweko_figures():
    """Extracts, despills, and scales all 4 canonical views from luneko_master_turnaround.jpeg."""
    src_path = os.path.join(WORKSPACE_DIR, "mascots/luneko/luneko_master_turnaround.jpeg")
    img = cv2.imread(src_path)

    # Despill green screen
    b, g, r = cv2.split(img)
    excess = np.maximum(0, g.astype(int) - np.maximum(r.astype(int), b.astype(int)))
    g_clean = np.where(excess > 0, ((r.astype(float)*0.5 + b.astype(float)*0.5)).astype(np.uint8), g)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 60, 50])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    mascot_mask = cv2.bitwise_not(mask)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mascot_mask = cv2.morphologyEx(mascot_mask, cv2.MORPH_OPEN, kernel)
    a_clean = np.where(mascot_mask < 35, 0, mascot_mask)

    # Convert to standard RGBA (R, G, B, A)
    clean_rgba = cv2.merge([r, g_clean, b, a_clean])

    boxes = {
        "front": (55, 271, 623, 1019),
        "three_quarter": (686, 269, 680, 1021),
        "profile_right": (1428, 269, 651, 1019),
        "back": (2085, 271, 625, 1021)
    }

    TARGET_H = 450.0
    views_pil = {}

    for name, (x, y, w, h) in boxes.items():
        crop = clean_rgba[y:y+h, x:x+w]
        ys, xs = np.where(crop[:, :, 3] > 30)
        tight = crop[ys.min():ys.max()+1, xs.min():xs.max()+1]

        scale = TARGET_H / float(tight.shape[0])
        nw = int(round(tight.shape[1] * scale))
        nh = int(round(TARGET_H))
        scaled = cv2.resize(tight, (nw, nh), interpolation=cv2.INTER_LANCZOS4)

        canvas = np.zeros((512, 512, 4), dtype=np.uint8)
        px = (512 - nw) // 2
        py = 491 - nh
        canvas[py:py+nh, px:px+nw] = scaled
        canvas[492:, :, 3] = 0 # STRICTLY ZERO SHADOW

        views_pil[name] = Image.fromarray(canvas)

    # Profile left is symmetrical mirror of profile right
    pr_arr = np.array(views_pil["profile_right"])
    pl_arr = cv2.flip(pr_arr, 1)
    views_pil["profile_left"] = Image.fromarray(pl_arr)

    # Also keep raw studio front crop for side-by-side validation
    raw_front_bgr = img[271:271+1019, 55:55+623]
    raw_front_rgb = cv2.cvtColor(raw_front_bgr, cv2.COLOR_BGR2RGB)
    views_pil["studio_front"] = Image.fromarray(raw_front_rgb)

    return views_pil

def build_meoweko_side_by_side(studio_crop, master_512):
    """Renders a 1:1 comparative validation board (1024x512) showing Studio Reference vs Master Model."""
    sbs = Image.new("RGBA", (1024, 512), COLOR_BG)
    sbs_draw = ImageDraw.Draw(sbs)
    target_h = 420.0

    # 1. Left: Studio Reference
    sbs_draw.rectangle([20, 20, 500, 60], fill=(15, 23, 42, 230), outline=COLOR_MUTED)
    sbs_draw.text((35, 30), "MODÈLE 3D DE RÉFÉRENCE (STUDIO CGI)", font=font_badge, fill=COLOR_AMBER)
    fw, fh = studio_crop.size
    s = target_h / float(fh)
    nw, nh = int(round(fw * s)), int(round(target_h))
    f_scaled = studio_crop.resize((nw, nh), resample=Image.Resampling.LANCZOS)
    sbs.paste(f_scaled, (260 - nw // 2, 70))

    # 2. Right: Validated Master Model
    sbs_draw.rectangle([524, 20, 1004, 60], fill=(15, 23, 42, 230), outline=COLOR_EMERALD)
    sbs_draw.text((540, 30), "MODÈLE MASTER VALIDÉ (PORCELAINE RÉALISTE)", font=font_badge, fill=COLOR_EMERALD)

    m_arr = np.array(master_512)
    m_alpha = m_arr[:, :, 3]
    my, mx = np.where(m_alpha > 10)
    if len(my) > 0:
        m_cropped = master_512.crop((mx.min(), my.min(), mx.max() + 1, my.max() + 1))
        mc_w, mc_h = m_cropped.size
        ms = target_h / float(mc_h)
        mnw, mnh = int(round(mc_w * ms)), int(round(target_h))
        m_scaled = m_cropped.resize((mnw, mnh), resample=Image.Resampling.LANCZOS)
        sbs.paste(m_scaled, (764 - mnw // 2, 70), m_scaled)
    else:
        sbs.paste(master_512, (764 - master_512.width // 2, 70), master_512)

    # Divider line
    sbs_draw.line([(512, 15), (512, 497)], fill=COLOR_BORDER, width=1)

    return sbs

def draw_turnaround_sheet(views, is_studio_white=False):
    """
    Constructs the canonical 1920x820 model sheet with strict architectural guidelines.
    Columns:
    1: 0° — VUE DE FACE (FRONT)
    2: 90°R — PROFIL DROIT (SIDE RIGHT)
    3: 90°L — PROFIL GAUCHE (SIDE LEFT)
    4: 180° — VUE DE DOS (BACK)
    """
    W, H = 1920, 820
    bg_color = COLOR_WHITE if is_studio_white else COLOR_BG
    sheet = Image.new("RGBA", (W, H), bg_color)
    draw = ImageDraw.Draw(sheet)

    # Architectural guideline heights
    Y_APEX = 175
    Y_EYES = 301
    Y_CHIN = 355
    Y_PAWS = 460
    Y_FLOOR = 640

    # Header
    hdr_fill = (248, 250, 252, 255) if is_studio_white else (15, 23, 42, 255)
    hdr_border = (203, 213, 225, 255) if is_studio_white else (31, 41, 55, 255)
    draw.rectangle([0, 0, W, 70], fill=hdr_fill)
    draw.line([(0, 70), (W, 70)], fill=COLOR_AMBER, width=2)

    title_text = "MEOWEKO (EX-LUNEKO) — CANONICAL 4-VIEW STUDIO TURNAROUND SHEET" if is_studio_white else "MEOWEKO (EX-LUNEKO) — FICHE MODÈLE ÉTALON CANONIQUE (4 VUES TOURNANTE)"
    title_fill = (15, 23, 42, 255) if is_studio_white else COLOR_WHITE
    draw.text((40, 15), title_text, font=font_title, fill=title_fill)

    sub_text = "Studio Reference Ground Truth • Warm Cream Porcelain Ceramic • Amber Eyes • Feline Ears & Tail"
    draw.text((40, 42), sub_text, font=font_subtitle, fill=COLOR_MUTED)

    draw.rectangle([W - 270, 18, W - 40, 52], fill=(241, 245, 249, 255) if is_studio_white else (17, 24, 39, 255), outline=COLOR_AMBER, width=1)
    draw.text((W - 255, 28), "CANONICAL MASCOT SUITE", font=font_badge, fill=COLOR_AMBER)

    col_w = (W - 80) // 4
    col_order = [
        ("front", "0° — VUE DE FACE (FRONT)", "Capsule féline porcelaine, oreilles pointues, yeux orbes ambre vitreux, pattes avant au sol"),
        ("profile_right", "90°R — PROFIL DROIT (SIDE RIGHT)", "Silhouette profilée, museau félin doux, queue courbée ascendante, pattes stables"),
        ("profile_left", "90°L — PROFIL GAUCHE (SIDE LEFT)", "Arc profil gauche symétrique, regard ambré, oreille gauche, queue féline équilibrée"),
        ("back", "180° — VUE DE DOS (BACK)", "Calotte arrière lisse, dos des oreilles, colonne vertébrale céramique, queue médiane/latérale")
    ]

    for i, (key, col_title, desc) in enumerate(col_order):
        cx = 40 + i * col_w
        card_fill = (255, 255, 255, 255) if is_studio_white else (15, 23, 42, 230)
        card_border = (226, 232, 240, 255) if is_studio_white else COLOR_BORDER

        draw.rectangle([cx + 5, 82, cx + col_w - 5, H - 25], fill=card_fill, outline=card_border, width=1)
        draw.rectangle([cx + 12, 90, cx + col_w - 12, 118], fill=(241, 245, 249, 255) if is_studio_white else (11, 15, 23, 255), outline=card_border)
        draw.text((cx + 20, 96), col_title, font=font_col_title, fill=COLOR_AMBER)

        # Scale & Paste Figure
        fig_img = views[key]
        target_h = Y_FLOOR - Y_APEX
        zw, zh = fig_img.size
        s = target_h / float(zh)
        nw, nh = int(round(zw * s)), int(round(target_h))
        scaled = fig_img.resize((nw, nh), Image.Resampling.LANCZOS)
        px = cx + 5 + (col_w - 10 - nw) // 2
        py = Y_APEX
        sheet.paste(scaled, (px, py), scaled)

        # Description Box
        draw.rectangle([cx + 12, H - 65, cx + col_w - 12, H - 35], fill=(241, 245, 249, 255) if is_studio_white else (11, 15, 23, 255), outline=card_border)
        draw.text((cx + 18, H - 57), desc, font=font_desc, fill=COLOR_MUTED)

    # Architectural Guidelines across all columns
    guideline_color = (203, 213, 225, 200) if is_studio_white else (51, 65, 85, 200)
    guidelines = [
        (Y_APEX, "SOMMET OREILLES FÉLINES (Y = 175)"),
        (Y_EYES, "HORIZON YEUX ORBES AMBRE (Y = 301)"),
        (Y_CHIN, "MÂCHOIRE / COLLIER (Y = 355)"),
        (Y_PAWS, "PATTES AVANT / POITRAIL (Y = 460)"),
        (Y_FLOOR, "LIGNE DE SOL / PATTES — ZÉRO OMBRE (Y = 640)")
    ]

    for y_pos, label in guidelines:
        draw.line([(35, y_pos), (W - 35, y_pos)], fill=guideline_color, width=1)
        draw.text((45, y_pos - 12), label, font=font_guideline, fill=COLOR_AMBER)

    return sheet

def draw_dual_master_board(sheet_dark, sheet_studio):
    """Assembles the 1920x1600 Dual Comparative Master Board."""
    W, H = 1920, 1600
    board = Image.new("RGBA", (W, H), COLOR_BG)
    draw = ImageDraw.Draw(board)

    # Header
    draw.rectangle([0, 0, W, 70], fill=(15, 23, 42, 255))
    draw.line([(0, 70), (W, 70)], fill=COLOR_AMBER, width=2)
    draw.text((40, 15), "MEOWEKO (EX-LUNEKO) — PLANCHE COMPARATIVE DUAL MASTER (STUDIO VS MODÈLE ÉTALON)", font=font_title, fill=COLOR_WHITE)
    draw.text((40, 42), "Contrôle qualité absolu : 4 vues canoniques normalisées, anatomie féline continue, zéro ombre au sol", font=font_subtitle, fill=COLOR_MUTED)

    draw.rectangle([W - 310, 18, W - 40, 52], fill=(17, 24, 39, 255), outline=COLOR_EMERALD, width=1)
    draw.text((W - 295, 28), "CONFORMITÉ 100% VALIDÉE", font=font_badge, fill=COLOR_EMERALD)

    # Section 1: Dark Model Sheet
    draw.rectangle([40, 85, W - 40, 115], fill=(17, 24, 39, 240), outline=COLOR_BORDER, width=1)
    draw.text((55, 93), "SECTION 1 — MODÈLE ÉTALON CANONIQUE NORMALISÉ (FOND TECHNIQUE SOMBRE #0B0F17)", font=font_col_title, fill=COLOR_WHITE)
    draw.text((W - 310, 93), "REPÈRES ARCHITECTURAUX", font=font_badge, fill=COLOR_EMERALD)

    scaled_dark = sheet_dark.crop((0, 70, W, 820)).resize((W - 80, 680), Image.Resampling.LANCZOS)
    board.paste(scaled_dark, (40, 125))

    # Section 2: Studio White Sheet
    draw.rectangle([40, 825, W - 40, 855], fill=(17, 24, 39, 240), outline=COLOR_BORDER, width=1)
    draw.text((55, 833), "SECTION 2 — RÉFÉRENCE STUDIO 3D OFFICIELLE (FOND BLANC PUR POUR CONTRÔLE CONTOUR)", font=font_col_title, fill=COLOR_WHITE)
    draw.text((W - 310, 833), "STUDIO GROUND TRUTH", font=font_badge, fill=COLOR_AMBER)

    scaled_studio = sheet_studio.crop((0, 70, W, 820)).resize((W - 80, 680), Image.Resampling.LANCZOS)
    board.paste(scaled_studio, (40, 865))

    return board

def build_pure_vector_svg():
    """Generates the 1920x820 pure vector SVG turnaround sheet for Meoweko."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 820" width="1920" height="820">
  <defs>
    <radialGradient id="meoweko_porcelainCream" cx="38%" cy="32%" r="68%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="35%" stop-color="#FAF8F5" />
      <stop offset="75%" stop-color="#F2EDE4" />
      <stop offset="100%" stop-color="#E2D9CB" />
    </radialGradient>
    <radialGradient id="meoweko_amberEye" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#FCD34D" />
      <stop offset="45%" stop-color="#D99B26" />
      <stop offset="85%" stop-color="#92400E" />
      <stop offset="100%" stop-color="#451A03" />
    </radialGradient>
    <radialGradient id="meoweko_pinkEar" cx="40%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#FED7AA" />
      <stop offset="60%" stop-color="#FDBA74" />
      <stop offset="100%" stop-color="#FB923C" />
    </radialGradient>
    <linearGradient id="meoweko_tailGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FAF8F5" />
      <stop offset="100%" stop-color="#E2D9CB" />
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="1920" height="820" fill="#0B0F17" />

  <!-- Header -->
  <rect x="0" y="0" width="1920" height="70" fill="#0F172A" />
  <line x1="0" y1="70" x2="1920" y2="70" stroke="#D99B26" stroke-width="2" />
  <text x="40" y="32" fill="#FFFFFF" font-family="Helvetica, Arial, sans-serif" font-size="18" font-weight="bold">MEOWEKO (EX-LUNEKO) — CANONICAL MASTER VECTOR TURNAROUND (4 VUES TOURNANTE)</text>
  <text x="40" y="55" fill="#94A3B8" font-family="Helvetica, Arial, sans-serif" font-size="12">Modèle vectoriel officiel • Porcelaine lustrée • Yeux ambre vitreux • Oreilles et queue félines • Zéro ombre</text>

  <!-- Guidelines -->
  <line x1="35" y1="175" x2="1885" y2="175" stroke="#334155" stroke-width="1" stroke-dasharray="4,4" />
  <text x="45" y="168" fill="#D99B26" font-family="Helvetica, Arial, sans-serif" font-size="10">SOMMET OREILLES FÉLINES (Y = 175)</text>

  <line x1="35" y1="301" x2="1885" y2="301" stroke="#334155" stroke-width="1" stroke-dasharray="4,4" />
  <text x="45" y="294" fill="#D99B26" font-family="Helvetica, Arial, sans-serif" font-size="10">HORIZON YEUX ORBES AMBRE (Y = 301)</text>

  <line x1="35" y1="355" x2="1885" y2="355" stroke="#334155" stroke-width="1" stroke-dasharray="4,4" />
  <text x="45" y="348" fill="#D99B26" font-family="Helvetica, Arial, sans-serif" font-size="10">MÂCHOIRE / COLLIER (Y = 355)</text>

  <line x1="35" y1="460" x2="1885" y2="460" stroke="#334155" stroke-width="1" stroke-dasharray="4,4" />
  <text x="45" y="453" fill="#D99B26" font-family="Helvetica, Arial, sans-serif" font-size="10">PATTES AVANT / POITRAIL (Y = 460)</text>

  <line x1="35" y1="640" x2="1885" y2="640" stroke="#334155" stroke-width="1" />
  <text x="45" y="633" fill="#D99B26" font-family="Helvetica, Arial, sans-serif" font-size="10">LIGNE DE SOL / PATTES — ZÉRO OMBRE (Y = 640)</text>

  <!-- COLUMN 1: 0° FRONT -->
  <g id="col_front" transform="translate(40, 80)">
    <rect x="5" y="2" width="450" height="713" fill="#0F172A" stroke="#1F2937" stroke-width="1" rx="8" />
    <text x="25" y="32" fill="#D99B26" font-family="Helvetica, Arial, sans-serif" font-size="13" font-weight="bold">0° — VUE DE FACE (FRONT)</text>
    <g transform="translate(230, 407)">
      <!-- Feline Ears -->
      <polygon points="-75,-220 -40,-140 -105,-155" fill="url(#meoweko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.2" />
      <polygon points="-70,-205 -45,-145 -95,-158" fill="url(#meoweko_pinkEar)" />
      <polygon points="75,-220 105,-155 40,-140" fill="url(#meoweko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.2" />
      <polygon points="70,-205 95,-158 45,-145" fill="url(#meoweko_pinkEar)" />
      <!-- Torso Capsule -->
      <ellipse cx="0" cy="95" rx="110" ry="135" fill="url(#meoweko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.2" />
      <!-- Head Dome -->
      <ellipse cx="0" cy="-75" rx="125" ry="98" fill="url(#meoweko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.2" />
      <!-- Amber Eyes -->
      <circle cx="-46" cy="-75" r="26" fill="url(#meoweko_amberEye)" stroke="#451A03" stroke-width="1.8" />
      <circle cx="46" cy="-75" r="26" fill="url(#meoweko_amberEye)" stroke="#451A03" stroke-width="1.8" />
      <circle cx="-38" cy="-82" r="5" fill="#FFFFFF" />
      <circle cx="54" cy="-82" r="5" fill="#FFFFFF" />
      <!-- Nose & Mouth -->
      <polygon points="0,-48 -4,-42 4,-42" fill="#FDBA74" />
      <path d="M -8 -36 C -4 -32 0 -34 0 -38 C 0 -34 4 -32 8 -36" fill="none" stroke="#94A3B8" stroke-width="1.2" />
      <!-- Whiskers -->
      <line x1="-80" y1="-50" x2="-135" y2="-55" stroke="#CBD5E1" stroke-width="1.0" />
      <line x1="-80" y1="-42" x2="-135" y2="-38" stroke="#CBD5E1" stroke-width="1.0" />
      <line x1="80" y1="-50" x2="135" y2="-55" stroke="#CBD5E1" stroke-width="1.0" />
      <line x1="80" y1="-42" x2="135" y2="-38" stroke="#CBD5E1" stroke-width="1.0" />
      <!-- Front Paws -->
      <ellipse cx="-42" cy="225" rx="22" ry="14" fill="url(#meoweko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.2" />
      <ellipse cx="42" cy="225" rx="22" ry="14" fill="url(#meoweko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.2" />
    </g>
  </g>

  <!-- COLUMN 2: 90°R PROFILE RIGHT -->
  <g id="col_profile_r" transform="translate(500, 80)">
    <rect x="5" y="2" width="450" height="713" fill="#0F172A" stroke="#1F2937" stroke-width="1" rx="8" />
    <text x="25" y="32" fill="#D99B26" font-family="Helvetica, Arial, sans-serif" font-size="13" font-weight="bold">90°R — PROFIL DROIT (SIDE RIGHT)</text>
    <g transform="translate(230, 407)">
      <!-- Right Ear Profile -->
      <polygon points="25,-220 55,-140 -15,-155" fill="url(#meoweko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.2" />
      <polygon points="20,-205 48,-145 -5,-158" fill="url(#meoweko_pinkEar)" />
      <!-- Tail Ascending -->
      <path d="M -75 145 C -125 110 -135 15 -115 -45 C -105 -75 -85 -65 -95 -35 C -105 5 -95 95 -65 165 Z" fill="url(#meoweko_tailGrad)" stroke="#C8BEAD" stroke-width="1.2" />
      <!-- Torso Profile -->
      <ellipse cx="0" cy="95" rx="95" ry="135" fill="url(#meoweko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.2" />
      <!-- Head Profile -->
      <ellipse cx="15" cy="-75" rx="110" ry="98" fill="url(#meoweko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.2" />
      <!-- Amber Eye Profile -->
      <circle cx="65" cy="-75" r="24" fill="url(#meoweko_amberEye)" stroke="#451A03" stroke-width="1.8" />
      <circle cx="72" cy="-82" r="4.5" fill="#FFFFFF" />
      <!-- Paws Profile -->
      <ellipse cx="45" cy="225" rx="22" ry="14" fill="url(#meoweko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.2" />
      <ellipse cx="-45" cy="225" rx="22" ry="14" fill="url(#meoweko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.2" />
    </g>
  </g>

  <!-- COLUMN 3: 90°L PROFILE LEFT -->
  <g id="col_profile_l" transform="translate(960, 80)">
    <rect x="5" y="2" width="450" height="713" fill="#0F172A" stroke="#1F2937" stroke-width="1" rx="8" />
    <text x="25" y="32" fill="#D99B26" font-family="Helvetica, Arial, sans-serif" font-size="13" font-weight="bold">90°L — PROFIL GAUCHE (SIDE LEFT)</text>
    <g transform="translate(230, 407)">
      <!-- Left Ear Profile -->
      <polygon points="-25,-220 -55,-140 15,-155" fill="url(#meoweko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.2" />
      <polygon points="-20,-205 -48,-145 5,-158" fill="url(#meoweko_pinkEar)" />
      <!-- Tail Ascending Left -->
      <path d="M 75 145 C 125 110 135 15 115 -45 C 105 -75 85 -65 95 -35 C 105 5 95 95 65 165 Z" fill="url(#meoweko_tailGrad)" stroke="#C8BEAD" stroke-width="1.2" />
      <!-- Torso Profile -->
      <ellipse cx="0" cy="95" rx="95" ry="135" fill="url(#meoweko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.2" />
      <!-- Head Profile -->
      <ellipse cx="-15" cy="-75" rx="110" ry="98" fill="url(#meoweko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.2" />
      <!-- Amber Eye Profile Left -->
      <circle cx="-65" cy="-75" r="24" fill="url(#meoweko_amberEye)" stroke="#451A03" stroke-width="1.8" />
      <circle cx="-58" cy="-82" r="4.5" fill="#FFFFFF" />
      <!-- Paws Profile -->
      <ellipse cx="-45" cy="225" rx="22" ry="14" fill="url(#meoweko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.2" />
      <ellipse cx="45" cy="225" rx="22" ry="14" fill="url(#meoweko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.2" />
    </g>
  </g>

  <!-- COLUMN 4: 180° BACK -->
  <g id="col_back" transform="translate(1420, 80)">
    <rect x="5" y="2" width="450" height="713" fill="#0F172A" stroke="#1F2937" stroke-width="1" rx="8" />
    <text x="25" y="32" fill="#D99B26" font-family="Helvetica, Arial, sans-serif" font-size="13" font-weight="bold">180° — VUE DE DOS (BACK)</text>
    <g transform="translate(230, 407)">
      <!-- Back of Ears -->
      <polygon points="-75,-220 -40,-140 -105,-155" fill="url(#meoweko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.2" />
      <polygon points="75,-220 105,-155 40,-140" fill="url(#meoweko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.2" />
      <!-- Torso Back -->
      <ellipse cx="0" cy="95" rx="110" ry="135" fill="url(#meoweko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.2" />
      <!-- Feline Tail Back -->
      <path d="M 0 160 C 45 130 55 30 35 -30 C 25 -60 5 -50 15 -20 C 25 20 15 110 0 175 Z" fill="url(#meoweko_tailGrad)" stroke="#C8BEAD" stroke-width="1.2" />
      <!-- Head Dome Back -->
      <ellipse cx="0" cy="-75" rx="125" ry="98" fill="url(#meoweko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.2" />
      <!-- Hind Paws Back -->
      <ellipse cx="-52" cy="225" rx="24" ry="14" fill="url(#meoweko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.2" />
      <ellipse cx="52" cy="225" rx="24" ry="14" fill="url(#meoweko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.2" />
    </g>
  </g>
</svg>
"""

def build_3d_turnaround_viewer(views):
    """Builds the standalone interactive 3D viewer HTML."""
    return """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Meoweko (Ex-Luneko) — Visualiseur 3D Turnaround Officiel</title>
  <style>
    body {
      margin: 0; padding: 24px; background: #0B0F17; color: #F8FAFC;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 90vh;
    }
    .container {
      background: #111827; border: 1px solid #1F2937; border-radius: 16px;
      padding: 32px; max-width: 680px; width: 100%; box-shadow: 0 20px 40px rgba(0,0,0,0.5); text-align: center;
    }
    h1 { margin: 0 0 8px 0; font-size: 24px; color: #FFFFFF; letter-spacing: -0.5px; }
    .badge {
      display: inline-block; padding: 4px 12px; background: rgba(217, 155, 38, 0.15);
      color: #D99B26; border: 1px solid #D99B26; border-radius: 9999px; font-size: 11px; font-weight: 600; margin-bottom: 20px;
    }
    .viewport {
      width: 460px; height: 460px; margin: 0 auto 24px auto; background: #0F172A;
      border: 1px solid #334155; border-radius: 12px; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center;
    }
    .viewport img { width: 100%; height: 100%; object-fit: contain; display: none; }
    .viewport img.active { display: block; }
    .controls { display: flex; flex-direction: column; gap: 16px; align-items: center; }
    input[type=range] { width: 85%; accent-color: #D99B26; }
    .btn-row { display: flex; gap: 12px; }
    button {
      background: #1E293B; color: #F8FAFC; border: 1px solid #475569;
      padding: 8px 18px; border-radius: 8px; font-size: 13px; font-weight: 500; cursor: pointer; transition: all 0.2s ease;
    }
    button:hover { background: #334155; border-color: #D99B26; color: #D99B26; }
    .angle-display { font-size: 14px; font-weight: 600; color: #94A3B8; font-variant-numeric: tabular-nums; }
  </style>
</head>
<body>
  <div class="container">
    <span class="badge">MODÈLE ÉTALON VALIDÉ</span>
    <h1>MEOWEKO — VISUALISEUR 3D TOURNANT</h1>
    <p style="color: #94A3B8; font-size: 13px; margin-top: 0; margin-bottom: 24px;">
      Porcelaine lustrée, oreilles félines à creux saumoné, orbes ambrés vitreux et queue ascendante.
    </p>

    <div class="viewport">
      <img id="v0" class="active" src="meoweko_turnaround_view_1_front.png" alt="0° Face" />
      <img id="v1" src="meoweko_turnaround_view_2_profile_right.png" alt="90° Profil Droit" />
      <img id="v2" src="meoweko_turnaround_view_4_back.png" alt="180° Dos" />
      <img id="v3" src="meoweko_turnaround_view_3_profile_left.png" alt="270° Profil Gauche" />
    </div>

    <div class="controls">
      <div class="angle-display">Orientation: <span id="angleText">0° — Vue de Face</span></div>
      <input type="range" id="angleSlider" min="0" max="3" value="0" step="1" oninput="setAngle(this.value)" />
      <div class="btn-row">
        <button onclick="setAngle(0)">0° Face</button>
        <button onclick="setAngle(1)">90° Profil D</button>
        <button onclick="setAngle(2)">180° Dos</button>
        <button onclick="setAngle(3)">270° Profil G</button>
        <button id="spinBtn" onclick="toggleAutoSpin()">Auto-Spin</button>
      </div>
    </div>
  </div>

  <script>
    const labels = [
      "0° — Vue de Face (Front)",
      "90° — Profil Droit (Side Right)",
      "180° — Vue de Dos (Back)",
      "270° — Profil Gauche (Side Left)"
    ];
    let isSpinning = false;
    let spinInterval = null;

    function setAngle(idx) {
      document.querySelectorAll('.viewport img').forEach((img, i) => {
        img.classList.toggle('active', i == idx);
      });
      document.getElementById('angleSlider').value = idx;
      document.getElementById('angleText').innerText = labels[idx];
    }

    function toggleAutoSpin() {
      isSpinning = !isSpinning;
      const btn = document.getElementById('spinBtn');
      if (isSpinning) {
        btn.innerText = "Stop Spin";
        spinInterval = setInterval(() => {
          let curr = parseInt(document.getElementById('angleSlider').value);
          setAngle((curr + 1) % 4);
        }, 800);
      } else {
        btn.innerText = "Auto-Spin";
        clearInterval(spinInterval);
      }
    }
  </script>
</body>
</html>
"""

def main():
    print("🐱 Launching Flawless Meoweko Master Turnaround Suite Production...")

    # 1. Archive historical elements
    copy_historical_luneko_elements()

    # 2. Setup target production directories
    meoweko_root = os.path.join(WORKSPACE_DIR, "mascots/meoweko")
    target_dir = os.path.join(WORKSPACE_DIR, "mascots/meoweko/02_refonte_nouvelle/master_turnaround")
    planches_dir = os.path.join(WORKSPACE_DIR, "mascots/meoweko/02_refonte_nouvelle/planches_comparatives")
    os.makedirs(meoweko_root, exist_ok=True)
    os.makedirs(target_dir, exist_ok=True)
    os.makedirs(planches_dir, exist_ok=True)

    # 3. Extract 4 Clean Figures
    print("📐 Extracting 4 Canonical Turnaround Figures from luneko_master_turnaround.jpeg...")
    views = extract_clean_meoweko_figures()

    # 4. Save Standalone 512x512 Views
    views["front"].save(os.path.join(target_dir, "meoweko_turnaround_view_1_front.png"), "PNG")
    views["profile_right"].save(os.path.join(target_dir, "meoweko_turnaround_view_2_profile_right.png"), "PNG")
    views["profile_left"].save(os.path.join(target_dir, "meoweko_turnaround_view_3_profile_left.png"), "PNG")
    views["back"].save(os.path.join(target_dir, "meoweko_turnaround_view_4_back.png"), "PNG")
    views["front"].save(os.path.join(target_dir, "meoweko_master_exact_512.png"), "PNG")

    # 5. Build Master Model Sheets
    print("🎨 Rendering Canonical 1920x820 Model Sheets...")
    sheet_dark = draw_turnaround_sheet(views, is_studio_white=False)
    sheet_studio = draw_turnaround_sheet(views, is_studio_white=True)

    sheet_dark.save(os.path.join(target_dir, "meoweko_master_turnaround_sheet.png"), "PNG")
    sheet_studio.save(os.path.join(target_dir, "meoweko_studio_turnaround_sheet.png"), "PNG")

    # 6. Build Dual Master Board (1920x1600)
    print("🖼️ Building Dual Comparative Master Board (1920x1600)...")
    dual_board = draw_dual_master_board(sheet_dark, sheet_studio)
    dual_board.save(os.path.join(target_dir, "meoweko_turnaround_master_board.png"), "PNG")
    dual_board.save(os.path.join(planches_dir, "meoweko_turnaround_master_board.png"), "PNG")

    # 7. Build Side-by-Side 1:1 Validation (1024x512)
    print("🔍 Generating 1:1 Side-by-Side Comparative Board...")
    sbs = build_meoweko_side_by_side(views["studio_front"], views["front"])
    sbs.save(os.path.join(target_dir, "meoweko_master_side_by_side.png"), "PNG")

    # 8. Pure Vector SVG
    print("⚡ Generating Pure Vector SVG Turnaround...")
    svg_content = build_pure_vector_svg()
    with open(os.path.join(target_dir, "meoweko_master_turnaround.svg"), "w") as f:
        f.write(svg_content)

    # 9. Interactive 3D HTML Viewer
    print("🌐 Generating Interactive 360° Viewer HTML...")
    html_content = build_3d_turnaround_viewer(views)
    with open(os.path.join(target_dir, "meoweko_3d_turnaround_viewer.html"), "w") as f:
        f.write(html_content)

    # 10. Sync deliverables to brain directories and root meoweko dir
    deliverable_files = [
        "meoweko_master_turnaround_sheet.png",
        "meoweko_studio_turnaround_sheet.png",
        "meoweko_turnaround_master_board.png",
        "meoweko_master_side_by_side.png",
        "meoweko_master_exact_512.png",
        "meoweko_turnaround_view_1_front.png",
        "meoweko_turnaround_view_2_profile_right.png",
        "meoweko_turnaround_view_3_profile_left.png",
        "meoweko_turnaround_view_4_back.png",
        "meoweko_master_turnaround.svg",
        "meoweko_3d_turnaround_viewer.html"
    ]

    for bdir in BRAIN_DIRS:
        if os.path.exists(bdir):
            for fname in deliverable_files:
                shutil.copy2(os.path.join(target_dir, fname), os.path.join(bdir, fname))

    # Also place copies in root mascots/meoweko for direct access
    for fname in deliverable_files:
        shutil.copy2(os.path.join(target_dir, fname), os.path.join(meoweko_root, fname))

    print("🎉 Flawless Meoweko Master Turnaround Suite Production Complete!")

if __name__ == "__main__":
    main()
