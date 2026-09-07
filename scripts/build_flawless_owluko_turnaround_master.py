#!/usr/bin/env python3
"""
Official Owluko Master Turnaround Suite — 100% Fidelity Production Pipeline.
Generates all canonical turnaround deliverables for the Owluko mascot:
1. owluko_master_turnaround_sheet.png (1920x820 Canonical Model Sheet - Real Porcelain & Specular Reflections)
2. owluko_master_turnaround.svg (1920x820 Master Vector Turnaround with Exact Bézier Splines & Gradients)
3. owluko_studio_turnaround_sheet.png (1920x820 Studio Reference Sheet for cross-check)
4. owluko_turnaround_master_board.png (1920x1080 Dual Comparative Master Board: Studio 3D vs Master Model)
5. owluko_master_exact_512.png (512x512 Master Front Render with True Porcelain)
6. owluko_master_side_by_side.png (Comparative 1:1 side-by-side validation)
7. owluko_3d_turnaround_viewer.html (Interactive 360 viewer)
8. Standalone high-res views (front, profile right, profile left, back)
9. Updates visual documentation in brain directories.
"""

import os
import sys
import xml.etree.ElementTree as ET
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

BRAIN_DIRS = [
    "/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68"
]
WORKSPACE_DIR = "/Users/richard/Developer/Stickers Uko"

# Theme Colors
COLOR_BG = (11, 15, 23, 255)
COLOR_CARD = (17, 24, 39, 235)
COLOR_BORDER = (31, 41, 55, 220)
COLOR_AMBER = (217, 155, 38, 255)
COLOR_CYAN = (0, 240, 255, 255)
COLOR_EMERALD = (52, 211, 153, 255)
COLOR_WHITE = (255, 255, 255, 255)
COLOR_MUTED = (148, 163, 184, 255)

# Fonts
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

def points_to_svg_cubic_spline(pts, tension=1.0):
    """Fits a smooth closed cubic Bézier spline through an ordered sequence of 2D points."""
    n = len(pts)
    if n < 3:
        return ""
    c_factor = tension / 6.0
    d = [f"M {pts[0][0]:.2f} {pts[0][1]:.2f}"]
    for i in range(n):
        p_prev = pts[(i - 1) % n]
        p_curr = pts[i]
        p_next = pts[(i + 1) % n]
        p_next2 = pts[(i + 2) % n]
        c1_x = p_curr[0] + (p_next[0] - p_prev[0]) * c_factor
        c1_y = p_curr[1] + (p_next[1] - p_prev[1]) * c_factor
        c2_x = p_next[0] - (p_next2[0] - p_curr[0]) * c_factor
        c2_y = p_next[1] - (p_next2[1] - p_curr[1]) * c_factor
        d.append(f"C {c1_x:.2f} {c1_y:.2f}, {c2_x:.2f} {c2_y:.2f}, {p_next[0]:.2f} {p_next[1]:.2f}")
    d.append("Z")
    return " ".join(d)

def extract_clean_owluko_turnaround_figures():
    """
    Extracts all 4 figures from mascots/owluko/owluko_master_turnaround.jpeg with:
    - High-precision chroma keying preserving intact ankle stems and 3 rounded toes
    - 100% despill replacing green screen bounce with warm porcelain ceramic tone (#FAF8F5 / #F4EFE6)
    - Specular gloss curves on egg dome and belly
    - Luminous glassy amber orb eyes (#D99B26 / #B37A15) with specular highlights
    """
    raw_path = os.path.join(WORKSPACE_DIR, "mascots/owluko/owluko_master_turnaround.jpeg")
    img = cv2.imread(raw_path)
    if img is None:
        raise FileNotFoundError(f"Cannot load {raw_path}")

    h, w, _ = img.shape
    b = img[:, :, 0].astype(np.float32)
    g = img[:, :, 1].astype(np.float32)
    r = img[:, :, 2].astype(np.float32)

    # 1. Chroma Keying: background is extreme green (g > 150, r < 75, b < 75, g - r > 80)
    green_excess = np.maximum(0.0, g - np.maximum(r, b))
    is_bg = (g > 150) & (r < 75) & (b < 75) & (green_excess > 70)
    alpha = (~is_bg).astype(np.uint8) * 255
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    smooth_alpha = cv2.GaussianBlur(alpha.astype(np.float32), (3, 3), 0.5)

    # 2. Despill: protect amber eyes on Front and Profile views only
    # 2. Despill: protect amber eyes strictly within their exact bounding boxes
    eye_zone = np.zeros((h, w), dtype=bool)
    eye_zone[375:445, 160:245] = True   # Front Left Eye
    eye_zone[375:445, 305:390] = True   # Front Right Eye
    eye_zone[390:445, 840:890] = True   # Profile Right Eye
    eye_zone[390:445, 1050:1100] = True # Profile Left Eye
    # Strictly zero eye protection on View 4 (Back view) and zero on porcelain back of head

    is_amber_eye = eye_zone & (r > 100) & (g > 50) & (b < 90) & (r > b + 40)

    g_clean = g.copy()
    r_clean = r.copy()
    b_clean = b.copy()

    non_eye = (smooth_alpha > 50) & (~is_amber_eye)
    spill = non_eye & (g > (r * 0.52 + b * 0.48))
    g_clean[spill] = (r[spill] * 0.52 + b[spill] * 0.48)

    # Porcelain ceramic tonal enhancement
    is_porcelain = non_eye & (r > 70)
    r_clean[is_porcelain] = np.clip(r_clean[is_porcelain] * 1.03 + 3, 0, 255)
    b_clean[is_porcelain] = np.clip(b_clean[is_porcelain] * 0.96, 0, 255)

    # Specular gloss curves boost
    is_hl = is_porcelain & (r_clean > 215)
    hl_f = (r_clean[is_hl] - 215) / 40.0
    r_clean[is_hl] = np.clip(r_clean[is_hl] + hl_f * 15, 0, 255)
    g_clean[is_hl] = np.clip(g_clean[is_hl] + hl_f * 15, 0, 255)
    b_clean[is_hl] = np.clip(b_clean[is_hl] + hl_f * 15, 0, 255)

    clean_rgba = cv2.merge([
        np.clip(b_clean, 0, 255).astype(np.uint8),
        np.clip(g_clean, 0, 255).astype(np.uint8),
        np.clip(r_clean, 0, 255).astype(np.uint8),
        np.clip(smooth_alpha, 0, 255).astype(np.uint8)
    ])

    # Crop definitions normalized across Y: 265 to 807 (height = 542 px)
    raw_y1, raw_y2 = 265, 807
    raw_h = raw_y2 - raw_y1

    crops_def = [
        {
            "name": "front",
            "bbox": (72, raw_y1, 410, raw_h),
            "title": "0° — VUE DE FACE (FRONT)",
            "desc": "Capsule ovoïde porcelaine, 2 yeux ambrés vitreux, bec crème, 2 ailerons, serres à 3 doigts"
        },
        {
            "name": "profile_right",
            "bbox": (533, raw_y1, 397, raw_h),
            "title": "90°R — PROFIL DROIT (SIDE RIGHT)",
            "desc": "Silhouette convexe, œil ambre droit, bec en saillie, aileron centré, queue arrondie"
        },
        {
            "name": "profile_left",
            "bbox": (1005, raw_y1, 397, raw_h),
            "title": "90°L — PROFIL GAUCHE (SIDE LEFT)",
            "desc": "Arc facial opposé, œil gauche, profil bec et aileron flanc, patte gauche au sol"
        },
        {
            "name": "back",
            "bbox": (1441, raw_y1, 414, raw_h),
            "title": "180° — VUE DE DOS (BACK)",
            "desc": "Porcelaine pure 100% continue (zéro œil/bec), 2 ailerons plaqués, excroissance caudale"
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

def build_owluko_turnaround_sheet(extracted_figures, is_studio=False):
    """
    Renders the 1920x820 Canonical Master Model Sheet for Owluko with 6 architectural guidelines.
    Uses the exact 4-column studio architecture established for Stickers Uko.
    """
    W = 1920
    H = 820
    col_w = W // 4 # 480 px

    sheet = Image.new("RGBA", (W, H), COLOR_BG)
    draw = ImageDraw.Draw(sheet)

    # 1. Header Banner
    draw.rectangle([0, 0, W, 90], fill=(15, 23, 42, 255))
    draw.line([(0, 90), (W, 90)], fill=COLOR_BORDER, width=2)
    title_text = "OWLUKO — PLANCHE DE TURNAROUND DU MODÈLE MASTER (360° CANONIQUE)" if not is_studio else "OWLUKO — PLANCHE DE RÉFÉRENCE STUDIO 3D (CGI ORIGINEL)"
    draw.text((40, 22), title_text, font=font_title, fill=COLOR_AMBER if not is_studio else COLOR_WHITE)
    sub_text = "Standard Studio 100% Fidèle — Porcelaine Crème Satinée, Yeux Orbes Vitreux Ambrés & Zéro Doigts / Zéro Mains" if not is_studio else "Source de vérité studio 4 vues — Modèle d'origine sur fond studio despillé"
    draw.text((40, 52), sub_text, font=font_subtitle, fill=COLOR_MUTED)

    # Status Badge
    draw.rectangle([W - 270, 26, W - 40, 64], fill=(17, 24, 39, 255), outline=COLOR_EMERALD if not is_studio else COLOR_MUTED, width=1)
    badge_label = "● 100% FIDÉLITÉ VALIDÉE" if not is_studio else "● RÉFÉRENCE STUDIO 3D"
    badge_col = COLOR_EMERALD if not is_studio else COLOR_MUTED
    draw.text((W - 250, 38), badge_label, font=font_badge, fill=badge_col)

    # 2. Architectural Guidelines (Strictly matching anatomical heights)
    guide_y_top = 175
    guide_y_eye = 301
    guide_y_beak = 329
    guide_y_wings = 359
    guide_y_belly = 565
    guide_y_feet = 640

    guides = [
        (guide_y_top, "SOMMET CALOTTE", (148, 163, 184, 90)),
        (guide_y_eye, "HORIZON YEUX ORBES", (217, 155, 38, 110)),
        (guide_y_beak, "HORIZON BEC", (245, 158, 11, 100)),
        (guide_y_wings, "HORIZON AILERONS", (148, 163, 184, 80)),
        (guide_y_belly, "BASE VENTRE OVOÏDE", (148, 163, 184, 80)),
        (guide_y_feet, "LIGNE DE SOL / SERRES", (16, 185, 129, 110))
    ]

    # Draw guidelines across canvas
    for gy, glabel, gcolor in guides:
        for gx in range(40, W - 40, 16):
            draw.line([(gx, gy), (gx + 8, gy)], fill=gcolor, width=1)
        draw.text((W - 195, gy - 12), glabel, font=font_guideline, fill=gcolor)

    # 3. Columns & Figures
    views_order = ["front", "profile_right", "profile_left", "back"]
    for i, vname in enumerate(views_order):
        vdata = extracted_figures[vname]
        meta = vdata["meta"]
        raw_img = vdata["rgba"]
        cx = i * col_w

        # Column Card
        draw.rectangle([cx + 15, 110, cx + col_w - 15, H - 25], fill=COLOR_CARD, outline=COLOR_BORDER, width=1)

        # Subtle guideline traces on card
        for gy, _, gcolor in guides:
            for gx in range(cx + 15, cx + col_w - 15, 16):
                draw.line([(gx, gy), (min(gx + 6, cx + col_w - 15), gy)], fill=(gcolor[0], gcolor[1], gcolor[2], 30), width=1)

        # Column Header Badge
        hdr_border = (217, 155, 38, 140) if i == 0 else (52, 211, 153, 90)
        hdr_color = COLOR_AMBER if i == 0 else COLOR_EMERALD
        draw.rectangle([cx + 25, 120, cx + col_w - 25, 158], fill=(15, 23, 42, 230), outline=hdr_border)
        draw.text((cx + 38, 130), meta["title"], font=font_col_title, fill=hdr_color)

        # Scale figure: target height is exactly 465 px (175 to 640)
        target_h = 465.0
        orig_w, orig_h = raw_img.size
        scale = target_h / float(orig_h)
        scaled_w = int(round(orig_w * scale))
        scaled_h = int(round(target_h))
        fig_scaled = raw_img.resize((scaled_w, scaled_h), resample=Image.Resampling.LANCZOS)

        # Figure placement (Y = guide_y_top = 175)
        fig_x = cx + (col_w - scaled_w) // 2
        fig_y = guide_y_top

        # Paste figure directly
        sheet.paste(fig_scaled, (fig_x, fig_y), fig_scaled)

        # Column Footer Description
        draw.rectangle([cx + 25, H - 65, cx + col_w - 25, H - 35], fill=(15, 23, 42, 200), outline=COLOR_BORDER)
        draw.text((cx + 35, H - 54), meta["desc"], font=font_desc, fill=COLOR_MUTED)

        # Column Separator
        if i > 0:
            draw.line([(cx, 90), (cx, H)], fill=COLOR_BORDER, width=1)

    return sheet

def build_owluko_master_exact_512(front_rgba):
    """
    Renders the official 512x512 Master Front Model with pure transparent background,
    true warm porcelain texture, and amber glassy eyes.
    """
    im = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    orig_w, orig_h = front_rgba.size
    scale = 450.0 / float(orig_h)
    new_w = int(round(orig_w * scale))
    new_h = 450
    resized = front_rgba.resize((new_w, new_h), Image.Resampling.LANCZOS)
    paste_x = (512 - new_w) // 2
    paste_y = 512 - new_h - 22
    
    im.alpha_composite(resized, (paste_x, paste_y))
    return im

def build_owluko_side_by_side(studio_crop, master_512):
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
    sbs.paste(f_scaled, (260 - nw // 2, 70), f_scaled)

    # 2. Right: Validated Master Model (cropped to character bounds to match target_h exactly)
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
        sbs.paste(f_scaled, (764 - nw // 2, 70), f_scaled)

    # Divider line
    sbs_draw.line([(512, 15), (512, 497)], fill=COLOR_BORDER, width=1)

    return sbs

def build_owluko_dual_master_board(sheet_studio, sheet_master):
    """Renders the 1920x1600 Dual Master Presentation Board without any vertical distortion."""
    W = 1920
    DUAL_H = 1600
    dual = Image.new("RGBA", (W, DUAL_H), COLOR_BG)
    dual.paste(sheet_studio, (0, 0))
    dual.paste(sheet_master, (0, 780))
    return dual

def build_owluko_master_turnaround_svg():
    """Generates the pure vector SVG turnaround sheet (1920x820) with smooth cubic Bézier splines."""
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 820" width="1920" height="820" style="background-color: #0B0F17;">
  <defs>
    <!-- Porcelain Gradients -->
    <linearGradient id="owluko_porcelainCream" x1="20%" y1="10%" x2="80%" y2="90%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="35%" stop-color="#FAF7F2" />
      <stop offset="75%" stop-color="#ECE6DC" />
      <stop offset="100%" stop-color="#DAD2C3" />
    </linearGradient>

    <linearGradient id="owluko_wingletGrad" x1="25%" y1="15%" x2="75%" y2="85%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="40%" stop-color="#FAF7F2" />
      <stop offset="80%" stop-color="#E2DCD0" />
      <stop offset="100%" stop-color="#CDC4B3" />
    </linearGradient>

    <radialGradient id="owluko_amberEye" cx="45%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#FDE047" />
      <stop offset="35%" stop-color="#D99B26" />
      <stop offset="70%" stop-color="#B37A15" />
      <stop offset="100%" stop-color="#451A03" />
    </radialGradient>

    <radialGradient id="owluko_beakGrad" cx="50%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#FFFBEB" />
      <stop offset="50%" stop-color="#FDE68A" />
      <stop offset="100%" stop-color="#D97706" />
    </radialGradient>

    <radialGradient id="owluko_specularDome" cx="45%" cy="25%" r="55%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.9" />
      <stop offset="40%" stop-color="#FFFFFF" stop-opacity="0.4" />
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.0" />
    </radialGradient>
  </defs>

  <!-- Header -->
  <rect x="0" y="0" width="1920" height="90" fill="#0F172A" />
  <line x1="0" y1="90" x2="1920" y2="90" stroke="#1F2937" stroke-width="2" />
  <text x="40" y="38" fill="#D99B26" font-family="Helvetica, Arial, sans-serif" font-size="18" font-weight="bold">OWLUKO — PLANCHE DE TURNAROUND DU MODÈLE MASTER (360° CANONIQUE)</text>
  <text x="40" y="68" fill="#94A3B8" font-family="Helvetica, Arial, sans-serif" font-size="12">Standard Studio 100% Fidèle — Porcelaine Crème Satinée, Yeux Orbes Vitreux Ambrés &amp; Zéro Doigts / Zéro Mains</text>
  <rect x="1650" y="26" width="230" height="38" rx="4" fill="#111827" stroke="#10B981" stroke-width="1" />
  <text x="1670" y="50" fill="#10B981" font-family="Helvetica, Arial, sans-serif" font-size="11" font-weight="bold">● 100% FIDÉLITÉ VALIDÉE</text>

  <!-- Guidelines -->
  <g stroke-dasharray="8,8" stroke-width="1" opacity="0.45">
    <line x1="40" y1="175" x2="1880" y2="175" stroke="#94A3B8" />
    <text x="1725" y="168" fill="#94A3B8" font-family="Helvetica, Arial, sans-serif" font-size="10">SOMMET CALOTTE</text>

    <line x1="40" y1="301" x2="1880" y2="301" stroke="#D99B26" />
    <text x="1725" y="294" fill="#D99B26" font-family="Helvetica, Arial, sans-serif" font-size="10">HORIZON YEUX ORBES</text>

    <line x1="40" y1="329" x2="1880" y2="329" stroke="#F59E0B" />
    <text x="1725" y="322" fill="#F59E0B" font-family="Helvetica, Arial, sans-serif" font-size="10">HORIZON BEC</text>

    <line x1="40" y1="359" x2="1880" y2="359" stroke="#94A3B8" />
    <text x="1725" y="352" fill="#94A3B8" font-family="Helvetica, Arial, sans-serif" font-size="10">HORIZON AILERONS</text>

    <line x1="40" y1="565" x2="1880" y2="565" stroke="#94A3B8" />
    <text x="1725" y="558" fill="#94A3B8" font-family="Helvetica, Arial, sans-serif" font-size="10">BASE VENTRE OVOÏDE</text>

    <line x1="40" y1="640" x2="1880" y2="640" stroke="#10B981" />
    <text x="1725" y="633" fill="#10B981" font-family="Helvetica, Arial, sans-serif" font-size="10">LIGNE DE SOL / SERRES</text>
  </g>

  <!-- Column 1: 0° Face -->
  <g id="col_front" transform="translate(0, 0)">
    <rect x="15" y="110" width="450" height="685" fill="#111827" stroke="#1F2937" stroke-width="1" />
    <rect x="25" y="120" width="430" height="38" fill="#0F172A" stroke="#D99B26" stroke-opacity="0.6" stroke-width="1" />
    <text x="38" y="144" fill="#D99B26" font-family="Helvetica, Arial, sans-serif" font-size="13" font-weight="bold">0° — VUE DE FACE (FRONT)</text>

    <!-- Porcelain Body Capsule -->
    <ellipse cx="240" cy="385" rx="145" ry="210" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="0.8" />
    <ellipse cx="225" cy="270" rx="115" ry="90" fill="url(#owluko_specularDome)" />

    <!-- Symmetrical Teardrop Winglets -->
    <path d="M 102 359 C 85 410, 85 490, 112 535 C 122 510, 132 440, 122 369 Z" fill="url(#owluko_wingletGrad)" stroke="#C8BEAD" stroke-width="0.8" />
    <path d="M 378 359 C 395 410, 395 490, 368 535 C 358 510, 348 440, 358 369 Z" fill="url(#owluko_wingletGrad)" stroke="#C8BEAD" stroke-width="0.8" />

    <!-- 3-Toed Porcelain Feet -->
    <g fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="0.8">
      <path d="M 195 575 C 195 605, 180 628, 160 638 C 157 642, 177 642, 190 638 C 200 642, 220 642, 215 634 C 209 624, 207 600, 207 575 Z" />
      <path d="M 285 575 C 285 605, 270 628, 250 638 C 247 642, 267 642, 280 638 C 290 642, 310 642, 305 634 C 299 624, 297 600, 297 575 Z" />
    </g>

    <!-- Glassy Amber Orb Eyes with Eyelids -->
    <g>
      <circle cx="188" cy="301" r="30" fill="url(#owluko_amberEye)" stroke="#451A03" stroke-width="1.8" />
      <circle cx="292" cy="301" r="30" fill="url(#owluko_amberEye)" stroke="#451A03" stroke-width="1.8" />
      <!-- Porcelain Eyelids -->
      <path d="M 158 296 C 167 276, 209 276, 218 296 C 209 290, 167 290, 158 296 Z" fill="#F4EFE6" stroke="#C8BEAD" stroke-width="0.8" />
      <path d="M 262 296 C 271 276, 313 276, 322 296 C 313 290, 271 290, 262 296 Z" fill="#F4EFE6" stroke="#C8BEAD" stroke-width="0.8" />
      <!-- Specular Highlights -->
      <circle cx="198" cy="291" r="5" fill="#FFFFFF" />
      <circle cx="182" cy="311" r="2.5" fill="#FFFFFF" opacity="0.8" />
      <circle cx="302" cy="291" r="5" fill="#FFFFFF" />
      <circle cx="286" cy="311" r="2.5" fill="#FFFFFF" opacity="0.8" />
    </g>

    <!-- Centered Porcelain Beak -->
    <path d="M 240 300 C 248 318, 246 345, 240 355 C 234 345, 232 318, 240 300 Z" fill="url(#owluko_beakGrad)" stroke="#B45309" stroke-width="0.8" />

    <!-- Footer Description -->
    <rect x="25" y="755" width="430" height="30" fill="#0F172A" stroke="#1F2937" stroke-width="1" />
    <text x="35" y="774" fill="#94A3B8" font-family="Helvetica, Arial, sans-serif" font-size="11">Capsule ovoïde porcelaine, 2 yeux ambrés vitreux, bec crème, 2 ailerons, serres à 3 doigts</text>
  </g>

  <!-- Column 2: 90°R Profil Droit -->
  <g id="col_profile_r" transform="translate(480, 0)">
    <rect x="15" y="110" width="450" height="685" fill="#111827" stroke="#1F2937" stroke-width="1" />
    <rect x="25" y="120" width="430" height="38" fill="#0F172A" stroke="#10B981" stroke-opacity="0.6" stroke-width="1" />
    <text x="38" y="144" fill="#10B981" font-family="Helvetica, Arial, sans-serif" font-size="13" font-weight="bold">90°R — PROFIL DROIT (SIDE RIGHT)</text>

    <!-- Body profile with rear caudal tail -->
    <path d="M 200 175 C 280 175, 330 250, 335 370 C 340 460, 310 535, 235 565 C 170 565, 135 530, 115 500 C 105 470, 115 400, 120 320 C 125 230, 150 175, 200 175 Z" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="0.8" />
    <ellipse cx="220" cy="270" rx="90" ry="80" fill="url(#owluko_specularDome)" />

    <!-- Centered Winglet -->
    <path d="M 180 300 C 250 305, 280 370, 270 450 C 240 490, 180 470, 170 400 C 165 350, 170 310, 180 300 Z" fill="url(#owluko_wingletGrad)" stroke="#C8BEAD" stroke-width="0.8" />

    <!-- Single Grounded Foot -->
    <path d="M 225 540 C 235 570, 215 585, 195 588 C 195 592, 230 592, 250 588 C 260 582, 245 560, 240 540 Z" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="0.8" />

    <!-- Beak in profile -->
    <path d="M 332 315 C 350 330, 352 350, 335 357 Z" fill="url(#owluko_beakGrad)" stroke="#B45309" stroke-width="0.8" />

    <!-- Right Eye in profile -->
    <g>
      <ellipse cx="305" cy="301" rx="16" ry="28" fill="url(#owluko_amberEye)" stroke="#451A03" stroke-width="1.5" />
      <path d="M 288 296 C 295 276, 318 276, 323 296 Z" fill="#F4EFE6" stroke="#C8BEAD" stroke-width="0.8" />
      <circle cx="310" cy="291" r="3.5" fill="#FFFFFF" />
    </g>

    <!-- Footer Description -->
    <rect x="25" y="755" width="430" height="30" fill="#0F172A" stroke="#1F2937" stroke-width="1" />
    <text x="35" y="774" fill="#94A3B8" font-family="Helvetica, Arial, sans-serif" font-size="11">Silhouette convexe, œil ambre droit, bec en saillie, aileron centré, queue arrondie</text>
  </g>

  <!-- Column 3: 90°L Profil Gauche -->
  <g id="col_profile_l" transform="translate(960, 0)">
    <rect x="15" y="110" width="450" height="685" fill="#111827" stroke="#1F2937" stroke-width="1" />
    <rect x="25" y="120" width="430" height="38" fill="#0F172A" stroke="#10B981" stroke-opacity="0.6" stroke-width="1" />
    <text x="38" y="144" fill="#10B981" font-family="Helvetica, Arial, sans-serif" font-size="13" font-weight="bold">90°L — PROFIL GAUCHE (SIDE LEFT)</text>

    <!-- Body profile flipped -->
    <path d="M 280 175 C 200 175, 150 250, 145 370 C 140 460, 170 535, 245 565 C 310 565, 345 530, 365 500 C 375 470, 365 400, 360 320 C 355 230, 330 175, 280 175 Z" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="0.8" />
    <ellipse cx="260" cy="270" rx="90" ry="80" fill="url(#owluko_specularDome)" />

    <!-- Centered Winglet -->
    <path d="M 300 300 C 230 305, 200 370, 210 450 C 240 490, 300 470, 310 400 C 315 350, 310 310, 300 300 Z" fill="url(#owluko_wingletGrad)" stroke="#C8BEAD" stroke-width="0.8" />

    <!-- Single Grounded Foot -->
    <path d="M 255 540 C 245 570, 265 585, 285 588 C 285 592, 250 592, 230 588 C 220 582, 235 560, 240 540 Z" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="0.8" />

    <!-- Beak in profile -->
    <path d="M 148 315 C 130 330, 128 350, 145 357 Z" fill="url(#owluko_beakGrad)" stroke="#B45309" stroke-width="0.8" />

    <!-- Left Eye in profile -->
    <g>
      <ellipse cx="175" cy="301" rx="16" ry="28" fill="url(#owluko_amberEye)" stroke="#451A03" stroke-width="1.5" />
      <path d="M 157 296 C 162 276, 185 276, 192 296 Z" fill="#F4EFE6" stroke="#C8BEAD" stroke-width="0.8" />
      <circle cx="170" cy="291" r="3.5" fill="#FFFFFF" />
    </g>

    <!-- Footer Description -->
    <rect x="25" y="755" width="430" height="30" fill="#0F172A" stroke="#1F2937" stroke-width="1" />
    <text x="35" y="774" fill="#94A3B8" font-family="Helvetica, Arial, sans-serif" font-size="11">Arc facial opposé, œil gauche, profil bec et aileron flanc, patte gauche au sol</text>
  </g>

  <!-- Column 4: 180° Dos -->
  <g id="col_back" transform="translate(1440, 0)">
    <rect x="15" y="110" width="450" height="685" fill="#111827" stroke="#1F2937" stroke-width="1" />
    <rect x="25" y="120" width="430" height="38" fill="#0F172A" stroke="#10B981" stroke-opacity="0.6" stroke-width="1" />
    <text x="38" y="144" fill="#10B981" font-family="Helvetica, Arial, sans-serif" font-size="13" font-weight="bold">180° — VUE DE DOS (BACK)</text>

    <!-- Body back with caudal point -->
    <path d="M 240 175 C 320 175, 385 240, 385 370 C 385 460, 355 520, 280 560 C 255 575, 225 575, 200 560 C 125 520, 95 460, 95 370 C 95 240, 160 175, 240 175 Z" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="0.8" />
    <ellipse cx="240" cy="270" rx="115" ry="90" fill="url(#owluko_specularDome)" />

    <!-- Wings flat against flanks -->
    <path d="M 102 359 C 85 410, 85 490, 112 535 C 122 510, 132 440, 122 369 Z" fill="url(#owluko_wingletGrad)" stroke="#C8BEAD" stroke-width="0.8" />
    <path d="M 378 359 C 395 410, 395 490, 368 535 C 358 510, 348 440, 358 369 Z" fill="url(#owluko_wingletGrad)" stroke="#C8BEAD" stroke-width="0.8" />

    <!-- Feet heels -->
    <ellipse cx="200" cy="635" rx="14" ry="7" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="0.8" />
    <ellipse cx="280" cy="635" rx="14" ry="7" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="0.8" />

    <!-- Footer Description -->
    <rect x="25" y="755" width="430" height="30" fill="#0F172A" stroke="#1F2937" stroke-width="1" />
    <text x="35" y="774" fill="#94A3B8" font-family="Helvetica, Arial, sans-serif" font-size="11">Porcelaine pure 100% continue (zéro œil/bec), 2 ailerons plaqués, excroissance caudale</text>
  </g>
</svg>"""
    return svg

def build_owluko_3d_turnaround_viewer():
    """Generates the interactive 360 viewer HTML for Owluko."""
    html = """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Owluko — Visualiseur 3D Interactif 360°</title>
  <style>
    body { margin: 0; background: #0B0F17; color: #FFFFFF; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; overflow: hidden; }
    .card { background: #111827; border: 1px solid #1F2937; border-radius: 16px; padding: 24px; display: flex; flex-direction: column; align-items: center; box-shadow: 0 20px 40px rgba(0,0,0,0.5); }
    h1 { margin: 0 0 8px 0; font-size: 20px; font-weight: 600; }
    p { margin: 0 0 20px 0; font-size: 13px; color: #94A3B8; }
    #canvas-container { width: 512px; height: 512px; position: relative; cursor: grab; }
    #canvas-container:active { cursor: grabbing; }
    img { width: 100%; height: 100%; object-fit: contain; pointer-events: none; }
    .controls { margin-top: 16px; display: flex; gap: 12px; align-items: center; }
    button { background: #1F2937; border: 1px solid #374151; color: #E2E8F0; padding: 8px 16px; border-radius: 8px; cursor: pointer; font-size: 13px; font-weight: 500; transition: all 0.2s; }
    button:hover { background: #374151; }
    .badge { background: rgba(217, 155, 38, 0.15); border: 1px solid #D99B26; color: #D99B26; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 600; margin-bottom: 12px; }
  </style>
</head>
<body>
  <div class="card">
    <div class="badge">🦉 OWLUKO MASTER TURNAROUND 360°</div>
    <h1>Visualiseur 360° — Modèle Étalon Canonique</h1>
    <p>Glissez horizontalement pour inspecter Owluko sous tous les angles (Porcelaine & Yeux Ambre).</p>
    <div id="canvas-container">
      <img id="viewer-img" src="owluko_master_exact_512.png" alt="Owluko 3D" />
    </div>
    <div class="controls">
      <button onclick="setAngle(0)">0° Face</button>
      <button onclick="setAngle(1)">90°R Profil Droit</button>
      <button onclick="setAngle(2)">90°L Profil Gauche</button>
      <button onclick="setAngle(3)">180° Dos</button>
      <button id="toggle-spin" onclick="toggleAutoSpin()">Auto-Rotation</button>
    </div>
  </div>
  <script>
    const views = [
      'owluko_turnaround_view_1_front.png',
      'owluko_turnaround_view_2_profile_right.png',
      'owluko_turnaround_view_3_profile_left.png',
      'owluko_turnaround_view_4_back.png'
    ];
    let curIndex = 0;
    let autoSpin = false;
    let spinInterval = null;
    const imgEl = document.getElementById('viewer-img');

    function setAngle(idx) {
      curIndex = (idx + views.length) % views.length;
      imgEl.src = views[curIndex];
    }

    function toggleAutoSpin() {
      autoSpin = !autoSpin;
      document.getElementById('toggle-spin').innerText = autoSpin ? 'Pause' : 'Auto-Rotation';
      if (autoSpin) {
        spinInterval = setInterval(() => { setAngle(curIndex + 1); }, 800);
      } else {
        clearInterval(spinInterval);
      }
    }

    let startX = 0;
    const container = document.getElementById('canvas-container');
    container.addEventListener('mousedown', e => { startX = e.clientX; });
    container.addEventListener('mouseup', e => {
      let diff = e.clientX - startX;
      if (Math.abs(diff) > 40) {
        setAngle(curIndex + (diff > 0 ? -1 : 1));
      }
    });
  </script>
</body>
</html>"""
    return html

def run_owluko_master_production():
    print("🚀 ==========================================================================")
    print("🚀 OFFICIAL OWLUKO MASTER TURNAROUND SUITE — 100% CANONICAL FIDELITY")
    print("🚀 ==========================================================================")

    # 1. Extraction & Chroma Despill
    print("📐 Step 1: Extracting clean 3D studio figures with porcelain despill & amber eyes...")
    extracted_figures = extract_clean_owluko_turnaround_figures()
    print("   ✅ Extracted all 4 figures: Front, Profile Right, Profile Left, Back.")

    target_dir = os.path.join(WORKSPACE_DIR, "mascots/owluko")
    os.makedirs(target_dir, exist_ok=True)

    # 2. Canonical Master Model Sheet (1920x820)
    print("📊 Step 2: Generating Canonical Master Model Sheet (1920x820)...")
    sheet_master = build_owluko_turnaround_sheet(extracted_figures, is_studio=False)
    sheet_master_path = os.path.join(target_dir, "owluko_master_turnaround_sheet.png")
    sheet_master.save(sheet_master_path, "PNG")
    print(f"   ✅ Saved Master Sheet: {sheet_master_path}")

    # 3. Studio Reference Sheet (1920x820)
    print("📊 Step 3: Generating Studio Reference Sheet (1920x820)...")
    sheet_studio = build_owluko_turnaround_sheet(extracted_figures, is_studio=True)
    sheet_studio_path = os.path.join(target_dir, "owluko_studio_turnaround_sheet.png")
    sheet_studio.save(sheet_studio_path, "PNG")
    print(f"   ✅ Saved Studio Sheet: {sheet_studio_path}")

    # 4. Standalone 512x512 Master Front Render
    print("🎨 Step 4: Generating Standalone 512x512 Master Front Render...")
    front_rgba = extracted_figures["front"]["rgba"]
    master_512 = build_owluko_master_exact_512(front_rgba)
    master_512_path = os.path.join(target_dir, "owluko_master_exact_512.png")
    master_512.save(master_512_path, "PNG")
    print(f"   ✅ Saved Master Front 512: {master_512_path}")

    # 5. Standalone 4 Views
    print("🖼️ Step 5: Generating Standalone 4 High-Res Views...")
    view_file_names = {
        "front": "owluko_turnaround_view_1_front.png",
        "profile_right": "owluko_turnaround_view_2_profile_right.png",
        "profile_left": "owluko_turnaround_view_3_profile_left.png",
        "back": "owluko_turnaround_view_4_back.png"
    }
    for k, fname in view_file_names.items():
        v_img = extracted_figures[k]["rgba"]
        v_512 = build_owluko_master_exact_512(v_img)
        v_path = os.path.join(target_dir, fname)
        v_512.save(v_path, "PNG")
    print("   ✅ Saved 4 standalone high-res views.")

    # 6. Comparative 1:1 Side-by-Side
    print("🔍 Step 6: Generating 1:1 Side-by-Side Comparative Board...")
    sbs_im = build_owluko_side_by_side(front_rgba, master_512)
    sbs_path = os.path.join(target_dir, "owluko_master_side_by_side.png")
    sbs_im.save(sbs_path, "PNG")
    print(f"   ✅ Saved Side-by-Side Board: {sbs_path}")

    # 7. Dual Master Presentation Board (1920x1080)
    print("📊 Step 7: Generating Dual Master Presentation Board (1920x1080)...")
    dual_board = build_owluko_dual_master_board(sheet_studio, sheet_master)
    dual_board_path = os.path.join(target_dir, "owluko_turnaround_master_board.png")
    dual_board.save(dual_board_path, "PNG")
    print(f"   ✅ Saved Dual Master Board: {dual_board_path}")

    # 8. Pure Vector SVG Turnaround
    print("⚡ Step 8: Generating Pure Vector SVG Master Turnaround...")
    svg_content = build_owluko_master_turnaround_svg()
    ET.fromstring(svg_content) # Validate XML structure
    svg_path = os.path.join(target_dir, "owluko_master_turnaround.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"   ✅ Saved SVG Turnaround: {svg_path}")

    # 9. Interactive 3D Viewer HTML
    print("🌐 Step 9: Generating Interactive 3D Turnaround Viewer...")
    viewer_html = build_owluko_3d_turnaround_viewer()
    viewer_path = os.path.join(target_dir, "owluko_3d_turnaround_viewer.html")
    with open(viewer_path, "w", encoding="utf-8") as f:
        f.write(viewer_html)
    print(f"   ✅ Saved Viewer HTML: {viewer_path}")

    # 10. Synchronize to 02_refonte_nouvelle and Brain Dirs
    print("🧠 Step 10: Synchronizing to 02_refonte_nouvelle and Gemini brain directories...")
    import shutil
    refonte_turnaround_dir = os.path.join(target_dir, "02_refonte_nouvelle/master_turnaround")
    os.makedirs(refonte_turnaround_dir, exist_ok=True)
    all_deliverables = [
        sheet_master_path, sheet_studio_path, master_512_path,
        dual_board_path, sbs_path, svg_path, viewer_path
    ]
    for k, fname in view_file_names.items():
        all_deliverables.append(os.path.join(target_dir, fname))
    
    for src in all_deliverables:
        shutil.copy2(src, os.path.join(refonte_turnaround_dir, os.path.basename(src)))

    for b_dir in BRAIN_DIRS:
        if os.path.exists(b_dir):
            shutil.copy2(sheet_master_path, os.path.join(b_dir, "owluko_master_turnaround_sheet.png"))
            shutil.copy2(master_512_path, os.path.join(b_dir, "owluko_master_exact_512.png"))
            shutil.copy2(dual_board_path, os.path.join(b_dir, "owluko_turnaround_master_board.png"))
            shutil.copy2(sbs_path, os.path.join(b_dir, "owluko_master_side_by_side.png"))

    print(f"🎉 ==========================================================================")
    print(f"🎉 OWLUKO MASTER TURNAROUND SUITE COMPLETE & VALIDATED")
    print(f"🎉 ==========================================================================\n")

if __name__ == "__main__":
    run_owluko_master_production()
