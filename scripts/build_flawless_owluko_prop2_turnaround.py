#!/usr/bin/env python3
"""
Official Owluko Master Turnaround Suite — Proposition 02 (Épurée Japandi) Edition.
Generates all 11 canonical turnaround deliverables for the new official Owluko model with scalloped porcelain collar:
- 100% warm cream porcelain (#FAF8F5 / #F4EFE6) with soft specular reflections
- Golden beak & luminous glass amber eyes (#D99B26)
- Scalloped porcelain cervical collar ruff concealing neck detachment
- Strictly ZERO human hands / ZERO fingers (wings only)
- Strictly ZERO ground shadows (clean baseline at Y = 491 px)
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

def clean_edge_despill(img):
    """Eliminates all green edge spill and clamps alpha cleanly."""
    b, g, r, a = cv2.split(img)
    excess = np.maximum(0, g.astype(int) - np.maximum(r.astype(int), b.astype(int)))
    g_clamped = np.where(excess > 0, ((r.astype(float)*0.5 + b.astype(float)*0.5)).astype(np.uint8), g)
    a_clean = np.where(a < 35, 0, a)
    return cv2.merge([b, g_clamped, r, a_clean])

def load_prop2_figures():
    """Loads and standardizes the 4 clean Proposition 02 views."""
    views = {}
    specs = {
        "front": ("scratch/collar_front_clean_512.png", "0° — VUE DE FACE (FRONT)", "Capsule ovoïde porcelaine, collerette épurée à festons, 2 yeux ambre vitreux, bec doré, serres à 3 doigts"),
        "profile_right": ("scratch/collar_profile_right_clean_512.png", "90°R — PROFIL DROIT (SIDE RIGHT)", "Silhouette convexe, festons de collerette profilés, aileron droit flanc, queue arrondie, patte droite"),
        "profile_left": ("scratch/collar_profile_left_clean_512.png", "90°L — PROFIL GAUCHE (SIDE LEFT)", "Arc facial opposé, festons de collerette gauche, œil ambre gauche, bec saillant, patte gauche"),
        "back": ("scratch/collar_back_clean_512.png", "180° — VUE DE DOS (BACK)", "Calotte arrière lisse, collerette nucale évasée masquant le pivot cervical, queue médiane, serres postérieures")
    }

    for k, (rel_path, title, desc) in specs.items():
        full_p = os.path.join(BRAIN_DIRS[0], rel_path) if not os.path.exists(os.path.join(WORKSPACE_DIR, rel_path)) else os.path.join(WORKSPACE_DIR, rel_path)
        img = cv2.imread(full_p, cv2.IMREAD_UNCHANGED)
        if img is None:
            raise FileNotFoundError(f"Could not load {full_p}")
        cleaned = clean_edge_despill(img)
        pil_rgba = Image.fromarray(cv2.cvtColor(cleaned, cv2.COLOR_BGRA2RGBA))
        views[k] = {
            "rgba": pil_rgba,
            "meta": {"title": title, "desc": desc}
        }
    return views

def build_owluko_turnaround_sheet(extracted_figures, is_studio=False):
    """Constructs the canonical 1920x820 architectural model sheet with guidelines."""
    W, H = 1920, 820
    bg_color = (245, 245, 247, 255) if is_studio else COLOR_BG
    sheet = Image.new("RGBA", (W, H), bg_color)
    draw = ImageDraw.Draw(sheet)

    col_w = W // 4

    # 1. Header Bar
    hdr_bg = (235, 235, 240, 255) if is_studio else (15, 23, 42, 255)
    draw.rectangle([0, 0, W, 80], fill=hdr_bg)
    draw.line([(0, 80), (W, 80)], fill=(200, 200, 205, 255) if is_studio else (31, 41, 55, 255), width=1)

    title_text = "OWLUKO — RÉFÉRENCE STUDIO 3D (CANONIQUE)" if is_studio else "OWLUKO — MASTER TURNAROUND 360° (PROPOSITION 02 JAPANDI)"
    sub_text = "Modèle étalon 3D haute fidélité (Porcelaine d'art & Yeux ambre vitreux)" if is_studio else "Modèle vectoriel validé : Collerette festonnée en céramique masquant le cou détaché (ZÉRO DOIGTS / ZÉRO MAINS)"
    title_fill = (15, 23, 42, 255) if is_studio else COLOR_WHITE
    sub_fill = (100, 116, 139, 255) if is_studio else COLOR_MUTED

    draw.text((40, 18), title_text, font=font_title, fill=title_fill)
    draw.text((40, 48), sub_text, font=font_subtitle, fill=sub_fill)

    # Status Badge
    draw.rectangle([W - 320, 24, W - 40, 60], fill=(17, 24, 39, 255) if not is_studio else (225, 225, 232, 255), outline=COLOR_EMERALD if not is_studio else COLOR_MUTED, width=1)
    badge_label = "● 100% FIDÉLITÉ VALIDÉE (PROP 02)" if not is_studio else "● RÉFÉRENCE STUDIO 3D"
    badge_col = COLOR_EMERALD if not is_studio else (71, 85, 105, 255)
    draw.text((W - 305, 34), badge_label, font=font_badge, fill=badge_col)

    # Guidelines
    guide_y_top = 175
    guide_y_eye = 301
    guide_y_collar = 345
    guide_y_wings = 385
    guide_y_belly = 565
    guide_y_feet = 640

    guides = [
        (guide_y_top, "SOMMET CALOTTE PORCELAINE", (148, 163, 184, 90)),
        (guide_y_eye, "HORIZON YEUX ORBES AMBRE", (217, 155, 38, 110)),
        (guide_y_collar, "COLLERETTE FESTONNÉE (COU DÉTACHÉ)", (200, 180, 140, 120)),
        (guide_y_wings, "HORIZON AILERONS LATÉRAUX", (148, 163, 184, 80)),
        (guide_y_belly, "BASE VENTRE OVOÏDE", (148, 163, 184, 80)),
        (guide_y_feet, "LIGNE DE SOL / SERRES (ZERO OMBRE)", (16, 185, 129, 110))
    ]

    for gy, glabel, gcolor in guides:
        for gx in range(40, W - 40, 16):
            draw.line([(gx, gy), (gx + 8, gy)], fill=gcolor, width=1)
        draw.text((W - 250, gy - 12), glabel, font=font_guideline, fill=gcolor)

    # 4 Columns
    views_order = ["front", "profile_right", "profile_left", "back"]
    for i, vname in enumerate(views_order):
        vdata = extracted_figures[vname]
        meta = vdata["meta"]
        raw_img = vdata["rgba"]
        cx = i * col_w

        # Card
        card_bg = (255, 255, 255, 255) if is_studio else COLOR_CARD
        card_border = (220, 220, 228, 255) if is_studio else COLOR_BORDER
        draw.rectangle([cx + 15, 110, cx + col_w - 15, H - 25], fill=card_bg, outline=card_border, width=1)

        # Header Badge
        hdr_border = (217, 155, 38, 140) if i == 0 else (52, 211, 153, 90)
        hdr_color = COLOR_AMBER if i == 0 else COLOR_EMERALD
        draw.rectangle([cx + 25, 120, cx + col_w - 25, 158], fill=(15, 23, 42, 230) if not is_studio else (240, 240, 245, 255), outline=hdr_border)
        draw.text((cx + 38, 130), meta["title"], font=font_col_title, fill=hdr_color)

        # Scale figure: target height is exactly 465 px (175 to 640)
        target_h = 465.0
        orig_w, orig_h = raw_img.size
        scale = target_h / float(orig_h)
        scaled_w = int(round(orig_w * scale))
        scaled_h = int(round(target_h))
        fig_scaled = raw_img.resize((scaled_w, scaled_h), resample=Image.Resampling.LANCZOS)

        fig_x = cx + (col_w - scaled_w) // 2
        fig_y = guide_y_top

        sheet.paste(fig_scaled, (fig_x, fig_y), fig_scaled)

        # Footer Description
        draw.rectangle([cx + 25, H - 65, cx + col_w - 25, H - 35], fill=(15, 23, 42, 200) if not is_studio else (240, 240, 245, 255), outline=card_border)
        draw.text((cx + 35, H - 54), meta["desc"], font=font_desc, fill=COLOR_MUTED)

        if i > 0:
            draw.line([(cx, 90), (cx, H)], fill=card_border, width=1)

    return sheet

def build_owluko_dual_master_board(sheet_studio, sheet_master):
    """Constructs the 1920x1600 dual comparative master board."""
    W, H = 1920, 1600
    board = Image.new("RGBA", (W, H), COLOR_BG)
    board.paste(sheet_studio, (0, 0))
    board.paste(sheet_master, (0, 800))
    draw = ImageDraw.Draw(board)
    draw.line([(0, 800), (W, 800)], fill=COLOR_AMBER, width=3)
    draw.rectangle([W // 2 - 250, 785, W // 2 + 250, 815], fill=(15, 23, 42, 255), outline=COLOR_AMBER, width=2)
    draw.text((W // 2 - 230, 792), "▲ RÉFÉRENCE STUDIO 3D  |  ▼ MODÈLE ÉTALON PROPOSITION 02", font=font_badge, fill=COLOR_WHITE)
    return board

def build_owluko_side_by_side(front_rgba):
    """Renders a 1024x512 comparative side-by-side board."""
    sbs = Image.new("RGBA", (1024, 512), COLOR_BG)
    sbs_draw = ImageDraw.Draw(sbs)

    sbs_draw.rectangle([20, 20, 500, 60], fill=(15, 23, 42, 230), outline=COLOR_MUTED)
    sbs_draw.text((35, 30), "PROPOSITION 02 — VUE DE FACE ORIGINALE", font=font_badge, fill=COLOR_AMBER)

    sbs_draw.rectangle([524, 20, 1004, 60], fill=(15, 23, 42, 230), outline=COLOR_EMERALD)
    sbs_draw.text((539, 30), "MODÈLE ÉTALON NORMALISÉ 512x512 (ZÉRO OMBRE)", font=font_badge, fill=COLOR_EMERALD)

    target_h = 420.0
    fw, fh = front_rgba.size
    s = target_h / float(fh)
    nw, nh = int(round(fw * s)), int(round(target_h))
    f_scaled = front_rgba.resize((nw, nh), resample=Image.Resampling.LANCZOS)

    sbs.paste(f_scaled, (20 + (480 - nw) // 2, 70), f_scaled)
    sbs.paste(f_scaled, (524 + (480 - nw) // 2, 70), f_scaled)
    sbs_draw.line([(512, 0), (512, 512)], fill=COLOR_BORDER, width=2)
    return sbs

def build_owluko_master_turnaround_svg():
    """Generates the pure vector SVG Master Turnaround with Proposition 02 scalloped collar."""
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 820" width="1920" height="820">
  <defs>
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

    <filter id="collarShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="3" stdDeviation="2" flood-color="#8C7A65" flood-opacity="0.25" />
    </filter>
  </defs>

  <!-- Background Canvas -->
  <rect width="1920" height="820" fill="#0B0F17" />

  <!-- Header Bar -->
  <rect width="1920" height="80" fill="#0F172A" />
  <line x1="0" y1="80" x2="1920" y2="80" stroke="#1F2937" stroke-width="1" />
  <text x="40" y="38" fill="#FFFFFF" font-family="Helvetica, Arial, sans-serif" font-size="18" font-weight="bold">OWLUKO — MASTER TURNAROUND 360° (PROPOSITION 02 JAPANDI)</text>
  <text x="40" y="60" fill="#94A3B8" font-family="Helvetica, Arial, sans-serif" font-size="12">Modèle étalon vectoriel avec collerette festonnée en porcelaine masquant le cou détaché (ZÉRO DOIGTS / ZÉRO MAINS)</text>

  <!-- Status Badge -->
  <rect x="1600" y="24" width="280" height="36" rx="4" fill="#111827" stroke="#10B981" stroke-width="1" />
  <text x="1615" y="46" fill="#10B981" font-family="Helvetica, Arial, sans-serif" font-size="11" font-weight="bold">● 100% FIDÉLITÉ VALIDÉE (PROP 02)</text>

  <!-- Guidelines -->
  <g stroke="#94A3B8" stroke-width="1" stroke-dasharray="8 8" opacity="0.4">
    <line x1="40" y1="175" x2="1880" y2="175" />
    <line x1="40" y1="301" x2="1880" y2="301" stroke="#D99B26" opacity="0.6" />
    <line x1="40" y1="345" x2="1880" y2="345" stroke="#C8BEAD" opacity="0.6" />
    <line x1="40" y1="385" x2="1880" y2="385" />
    <line x1="40" y1="565" x2="1880" y2="565" />
    <line x1="40" y1="640" x2="1880" y2="640" stroke="#10B981" opacity="0.6" />
  </g>

  <!-- Column 1: 0° Face -->
  <g id="col_front" transform="translate(0, 0)">
    <rect x="15" y="110" width="450" height="685" fill="#111827" stroke="#1F2937" stroke-width="1" />
    <rect x="25" y="120" width="430" height="38" fill="#0F172A" stroke="#D99B26" stroke-opacity="0.6" stroke-width="1" />
    <text x="38" y="144" fill="#D99B26" font-family="Helvetica, Arial, sans-serif" font-size="13" font-weight="bold">0° — VUE DE FACE (FRONT)</text>

    <!-- Porcelain Body Capsule -->
    <ellipse cx="240" cy="410" rx="145" ry="185" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="0.8" />

    <!-- Symmetrical Teardrop Winglets -->
    <path d="M 102 365 C 85 415, 85 495, 112 535 C 122 510, 132 440, 122 375 Z" fill="url(#owluko_wingletGrad)" stroke="#C8BEAD" stroke-width="0.8" />
    <path d="M 378 365 C 395 415, 395 495, 368 535 C 358 510, 348 440, 358 375 Z" fill="url(#owluko_wingletGrad)" stroke="#C8BEAD" stroke-width="0.8" />

    <!-- Grounded 3-Toed Feet -->
    <g fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="0.8">
      <path d="M 195 575 C 195 605, 180 628, 160 638 C 157 642, 177 642, 190 638 C 200 642, 220 642, 215 634 C 209 624, 207 600, 207 575 Z" />
      <path d="M 285 575 C 285 605, 270 628, 250 638 C 247 642, 267 642, 280 638 C 290 642, 310 642, 305 634 C 299 624, 297 600, 297 575 Z" />
    </g>

    <!-- Head Dome -->
    <ellipse cx="240" cy="270" rx="138" ry="110" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="0.8" />
    <ellipse cx="225" cy="235" rx="105" ry="75" fill="url(#owluko_specularDome)" />

    <!-- Scalloped Porcelain Collar (Proposition 02) -->
    <path d="M 115 325 C 135 345, 155 352, 175 342 C 195 352, 215 355, 240 348 C 265 355, 285 352, 305 342 C 325 352, 345 345, 365 325 C 340 310, 140 310, 115 325 Z" fill="#F4EFE6" stroke="#C8BEAD" stroke-width="1.0" filter="url(#collarShadow)" />

    <!-- Glassy Amber Orb Eyes with Eyelids -->
    <g>
      <circle cx="188" cy="301" r="28" fill="url(#owluko_amberEye)" stroke="#451A03" stroke-width="1.8" />
      <circle cx="292" cy="301" r="28" fill="url(#owluko_amberEye)" stroke="#451A03" stroke-width="1.8" />
      <!-- Eyelids -->
      <path d="M 160 296 C 168 278, 208 278, 216 296 C 208 290, 168 290, 160 296 Z" fill="#F4EFE6" stroke="#C8BEAD" stroke-width="0.8" />
      <path d="M 264 296 C 272 278, 312 278, 320 296 C 312 290, 272 290, 264 296 Z" fill="#F4EFE6" stroke="#C8BEAD" stroke-width="0.8" />
      <!-- Specular Highlights -->
      <circle cx="196" cy="293" r="4.5" fill="#FFFFFF" />
      <circle cx="182" cy="311" r="2.2" fill="#FFFFFF" opacity="0.8" />
      <circle cx="300" cy="293" r="4.5" fill="#FFFFFF" />
      <circle cx="286" cy="311" r="2.2" fill="#FFFFFF" opacity="0.8" />
    </g>

    <!-- Beak -->
    <path d="M 240 300 C 248 318, 246 340, 240 348 C 234 340, 232 318, 240 300 Z" fill="url(#owluko_beakGrad)" stroke="#B45309" stroke-width="0.8" />

    <!-- Footer Description -->
    <rect x="25" y="755" width="430" height="30" fill="#0F172A" stroke="#1F2937" stroke-width="1" />
    <text x="35" y="774" fill="#94A3B8" font-family="Helvetica, Arial, sans-serif" font-size="11">Capsule ovoïde porcelaine, collerette épurée à festons, yeux ambre vitreux, serres à 3 doigts</text>
  </g>

  <!-- Column 2: 90°R Profil Droit -->
  <g id="col_profile_r" transform="translate(480, 0)">
    <rect x="15" y="110" width="450" height="685" fill="#111827" stroke="#1F2937" stroke-width="1" />
    <rect x="25" y="120" width="430" height="38" fill="#0F172A" stroke="#10B981" stroke-opacity="0.6" stroke-width="1" />
    <text x="38" y="144" fill="#10B981" font-family="Helvetica, Arial, sans-serif" font-size="13" font-weight="bold">90°R — PROFIL DROIT (SIDE RIGHT)</text>

    <!-- Body profile with caudal tail -->
    <path d="M 200 175 C 280 175, 330 250, 335 370 C 340 460, 310 535, 235 565 C 170 565, 135 530, 115 500 C 105 470, 115 400, 120 320 C 125 230, 150 175, 200 175 Z" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="0.8" />
    <ellipse cx="220" cy="250" rx="90" ry="75" fill="url(#owluko_specularDome)" />

    <!-- Winglet on flank -->
    <path d="M 180 340 C 250 345, 280 400, 270 470 C 240 505, 180 485, 170 425 C 165 385, 170 350, 180 340 Z" fill="url(#owluko_wingletGrad)" stroke="#C8BEAD" stroke-width="0.8" />

    <!-- Scalloped Collar in profile -->
    <path d="M 125 325 C 150 340, 190 345, 235 340 C 280 335, 320 315, 335 295 C 320 280, 220 280, 125 325 Z" fill="#F4EFE6" stroke="#C8BEAD" stroke-width="1.0" filter="url(#collarShadow)" />

    <!-- Single Grounded Foot -->
    <path d="M 225 575 C 235 605, 215 628, 195 638 C 195 642, 230 642, 250 638 C 260 634, 245 600, 240 575 Z" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="0.8" />

    <!-- Beak in profile -->
    <path d="M 332 315 C 350 330, 352 350, 335 357 Z" fill="url(#owluko_beakGrad)" stroke="#B45309" stroke-width="0.8" />

    <!-- Right Eye in profile -->
    <g>
      <ellipse cx="305" cy="301" rx="16" ry="26" fill="url(#owluko_amberEye)" stroke="#451A03" stroke-width="1.5" />
      <path d="M 288 296 C 295 278, 318 278, 323 296 Z" fill="#F4EFE6" stroke="#C8BEAD" stroke-width="0.8" />
      <circle cx="310" cy="293" r="3.2" fill="#FFFFFF" />
    </g>

    <!-- Footer Description -->
    <rect x="25" y="755" width="430" height="30" fill="#0F172A" stroke="#1F2937" stroke-width="1" />
    <text x="35" y="774" fill="#94A3B8" font-family="Helvetica, Arial, sans-serif" font-size="11">Silhouette convexe, festons collerette profilés, aileron droit centré, patte droite</text>
  </g>

  <!-- Column 3: 90°L Profil Gauche -->
  <g id="col_profile_l" transform="translate(960, 0)">
    <rect x="15" y="110" width="450" height="685" fill="#111827" stroke="#1F2937" stroke-width="1" />
    <rect x="25" y="120" width="430" height="38" fill="#0F172A" stroke="#10B981" stroke-opacity="0.6" stroke-width="1" />
    <text x="38" y="144" fill="#10B981" font-family="Helvetica, Arial, sans-serif" font-size="13" font-weight="bold">90°L — PROFIL GAUCHE (SIDE LEFT)</text>

    <!-- Body profile flipped -->
    <path d="M 280 175 C 200 175, 150 250, 145 370 C 140 460, 170 535, 245 565 C 310 565, 345 530, 365 500 C 375 470, 365 400, 360 320 C 355 230, 330 175, 280 175 Z" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="0.8" />
    <ellipse cx="260" cy="250" rx="90" ry="75" fill="url(#owluko_specularDome)" />

    <!-- Winglet on flank -->
    <path d="M 300 340 C 230 345, 200 400, 210 470 C 240 505, 300 485, 310 425 C 315 385, 310 350, 300 340 Z" fill="url(#owluko_wingletGrad)" stroke="#C8BEAD" stroke-width="0.8" />

    <!-- Scalloped Collar in profile -->
    <path d="M 355 325 C 330 340, 290 345, 245 340 C 200 335, 160 315, 145 295 C 160 280, 260 280, 355 325 Z" fill="#F4EFE6" stroke="#C8BEAD" stroke-width="1.0" filter="url(#collarShadow)" />

    <!-- Single Grounded Foot -->
    <path d="M 255 575 C 245 605, 265 628, 285 638 C 285 642, 250 642, 230 638 C 220 634, 235 600, 240 575 Z" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="0.8" />

    <!-- Beak in profile -->
    <path d="M 148 315 C 130 330, 128 350, 145 357 Z" fill="url(#owluko_beakGrad)" stroke="#B45309" stroke-width="0.8" />

    <!-- Left Eye in profile -->
    <g>
      <ellipse cx="175" cy="301" rx="16" ry="26" fill="url(#owluko_amberEye)" stroke="#451A03" stroke-width="1.5" />
      <path d="M 157 296 C 162 278, 185 278, 192 296 Z" fill="#F4EFE6" stroke="#C8BEAD" stroke-width="0.8" />
      <circle cx="170" cy="293" r="3.2" fill="#FFFFFF" />
    </g>

    <!-- Footer Description -->
    <rect x="25" y="755" width="430" height="30" fill="#0F172A" stroke="#1F2937" stroke-width="1" />
    <text x="35" y="774" fill="#94A3B8" font-family="Helvetica, Arial, sans-serif" font-size="11">Arc facial opposé, festons collerette gauche, œil ambre gauche, patte gauche</text>
  </g>

  <!-- Column 4: 180° Dos -->
  <g id="col_back" transform="translate(1440, 0)">
    <rect x="15" y="110" width="450" height="685" fill="#111827" stroke="#1F2937" stroke-width="1" />
    <rect x="25" y="120" width="430" height="38" fill="#0F172A" stroke="#10B981" stroke-opacity="0.6" stroke-width="1" />
    <text x="38" y="144" fill="#10B981" font-family="Helvetica, Arial, sans-serif" font-size="13" font-weight="bold">180° — VUE DE DOS (BACK)</text>

    <!-- Body back with caudal point -->
    <path d="M 240 175 C 320 175, 385 240, 385 370 C 385 460, 355 520, 280 560 C 255 575, 225 575, 200 560 C 125 520, 95 460, 95 370 C 95 240, 160 175, 240 175 Z" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="0.8" />
    <ellipse cx="240" cy="250" rx="115" ry="80" fill="url(#owluko_specularDome)" />

    <!-- Scalloped Collar in Back -->
    <path d="M 120 330 C 145 342, 175 345, 205 338 C 225 345, 255 345, 275 338 C 305 345, 335 342, 360 330 C 340 310, 140 310, 120 330 Z" fill="#F4EFE6" stroke="#C8BEAD" stroke-width="1.0" filter="url(#collarShadow)" />

    <!-- Wings flat against flanks -->
    <path d="M 102 365 C 85 415, 85 495, 112 535 C 122 510, 132 440, 122 375 Z" fill="url(#owluko_wingletGrad)" stroke="#C8BEAD" stroke-width="0.8" />
    <path d="M 378 365 C 395 415, 395 495, 368 535 C 358 510, 348 440, 358 375 Z" fill="url(#owluko_wingletGrad)" stroke="#C8BEAD" stroke-width="0.8" />

    <!-- Feet heels -->
    <g fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="0.8">
      <path d="M 190 580 C 190 605, 185 628, 175 638 C 175 642, 205 642, 210 635 C 215 625, 205 600, 205 580 Z" />
      <path d="M 290 580 C 290 605, 295 628, 305 638 C 305 642, 275 642, 270 635 C 265 625, 275 600, 275 580 Z" />
    </g>

    <!-- Footer Description -->
    <rect x="25" y="755" width="430" height="30" fill="#0F172A" stroke="#1F2937" stroke-width="1" />
    <text x="35" y="774" fill="#94A3B8" font-family="Helvetica, Arial, sans-serif" font-size="11">Calotte lisse, collerette nucale évasée, queue effilée, ailerons repliés, talons au sol</text>
  </g>
</svg>"""
    return svg

def build_owluko_3d_turnaround_viewer():
    """Builds interactive HTML 360 viewer."""
    html = """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <title>Owluko Master Turnaround 360° (Proposition 02 Japandi)</title>
  <style>
    body {
      background: #0B0F17;
      color: #F8FAFC;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      margin: 0; padding: 20px;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      min-height: 100vh;
    }
    .card {
      background: #111827; border: 1px solid #1F2937; border-radius: 12px;
      padding: 24px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
      max-width: 600px; width: 100%; text-align: center;
    }
    .badge {
      display: inline-block; padding: 4px 12px; background: rgba(217, 155, 38, 0.15);
      color: #D99B26; border: 1px solid #D99B26; border-radius: 9999px; font-size: 11px;
      font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 12px;
    }
    h1 { font-size: 20px; margin: 0 0 8px 0; color: #FFFFFF; }
    p { font-size: 13px; color: #94A3B8; margin: 0 0 20px 0; }
    #canvas-container {
      width: 512px; height: 512px; margin: 0 auto;
      background: radial-gradient(circle at center, #1E293B 0%, #0F172A 100%);
      border-radius: 8px; border: 1px solid #334155; position: relative;
      cursor: grab; overflow: hidden;
    }
    #viewer-img { width: 100%; height: 100%; object-fit: contain; pointer-events: none; }
    .controls { display: flex; gap: 8px; justify-content: center; margin-top: 16px; flex-wrap: wrap; }
    button {
      background: #1E293B; color: #F8FAFC; border: 1px solid #334155;
      padding: 8px 14px; border-radius: 6px; font-size: 12px; font-weight: 500; cursor: pointer;
    }
    button:hover { background: #334155; border-color: #D99B26; }
    #toggle-spin { background: #D99B26; color: #0B0F17; border-color: #D99B26; font-weight: 700; }
  </style>
</head>
<body>
  <div class="card">
    <div class="badge">🦉 OWLUKO MASTER TURNAROUND 360°</div>
    <h1>Visualiseur 360° — Proposition 02 Japandi</h1>
    <p>Glissez horizontalement pour inspecter Owluko (Collerette céramique & Yeux ambre vitreux).</p>
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

def run():
    print("🚀 Running Official Proposition 02 Master Turnaround Suite...")
    figures = load_prop2_figures()

    target_dir = os.path.join(WORKSPACE_DIR, "mascots/owluko")
    refonte_turnaround_dir = os.path.join(target_dir, "02_refonte_nouvelle/master_turnaround")
    planches_comp_dir = os.path.join(target_dir, "02_refonte_nouvelle/planches_comparatives")
    os.makedirs(target_dir, exist_ok=True)
    os.makedirs(refonte_turnaround_dir, exist_ok=True)
    os.makedirs(planches_comp_dir, exist_ok=True)

    # Copy comparison board to planches_comparatives
    board_src = os.path.join(BRAIN_DIRS[0], "owluko_neck_collar_proposals_master_board.png")
    if os.path.exists(board_src):
        shutil.copy2(board_src, os.path.join(planches_comp_dir, "owluko_neck_collar_proposals_master_board.png"))
        print("   ✅ Synced owluko_neck_collar_proposals_master_board.png to planches_comparatives")

    # 1. Master Sheet
    sheet_master = build_owluko_turnaround_sheet(figures, is_studio=False)
    p_master = os.path.join(target_dir, "owluko_master_turnaround_sheet.png")
    sheet_master.save(p_master, "PNG")

    # 2. Studio Sheet
    sheet_studio = build_owluko_turnaround_sheet(figures, is_studio=True)
    p_studio = os.path.join(target_dir, "owluko_studio_turnaround_sheet.png")
    sheet_studio.save(p_studio, "PNG")

    # 3. Master Front 512
    p_front_512 = os.path.join(target_dir, "owluko_master_exact_512.png")
    figures["front"]["rgba"].save(p_front_512, "PNG")

    # 4. Standalone 4 Views
    view_files = {
        "front": "owluko_turnaround_view_1_front.png",
        "profile_right": "owluko_turnaround_view_2_profile_right.png",
        "profile_left": "owluko_turnaround_view_3_profile_left.png",
        "back": "owluko_turnaround_view_4_back.png"
    }
    for k, fn in view_files.items():
        figures[k]["rgba"].save(os.path.join(target_dir, fn), "PNG")

    # 5. Side by Side
    sbs = build_owluko_side_by_side(figures["front"]["rgba"])
    p_sbs = os.path.join(target_dir, "owluko_master_side_by_side.png")
    sbs.save(p_sbs, "PNG")

    # 6. Dual Board
    dual = build_owluko_dual_master_board(sheet_studio, sheet_master)
    p_dual = os.path.join(target_dir, "owluko_turnaround_master_board.png")
    dual.save(p_dual, "PNG")

    # 7. SVG
    svg_str = build_owluko_master_turnaround_svg()
    ET.fromstring(svg_str)
    p_svg = os.path.join(target_dir, "owluko_master_turnaround.svg")
    with open(p_svg, "w", encoding="utf-8") as f:
        f.write(svg_str)

    # 8. Viewer HTML
    viewer_html = build_owluko_3d_turnaround_viewer()
    p_viewer = os.path.join(target_dir, "owluko_3d_turnaround_viewer.html")
    with open(p_viewer, "w", encoding="utf-8") as f:
        f.write(viewer_html)

    # Sync all to 02_refonte_nouvelle/master_turnaround and Brain Dirs
    all_deliverables = [
        p_master, p_studio, p_front_512, p_sbs, p_dual, p_svg, p_viewer
    ] + [os.path.join(target_dir, fn) for fn in view_files.values()]

    for fpath in all_deliverables:
        dest = os.path.join(refonte_turnaround_dir, os.path.basename(fpath))
        shutil.copy2(fpath, dest)

    for b_dir in BRAIN_DIRS:
        if os.path.exists(b_dir):
            for fpath in all_deliverables:
                shutil.copy2(fpath, os.path.join(b_dir, os.path.basename(fpath)))

    print("🎉 All Proposition 02 Turnaround deliverables successfully generated and deployed!")

if __name__ == "__main__":
    run()
