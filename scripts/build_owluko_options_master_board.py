#!/usr/bin/env python3
"""
Generates the comprehensive visual comparison board:
`owluko_searching_options_master_board.png` (1920x1400 px)
Directly comparing:
- Tier 1: Modèle Étalon Validé (Proposition 02 Japandi - 4 vues canoniques)
- Tier 2: Option A — Test de Rotation 360° par Découpe 2.5D (Visualisation du problème de brisure)
- Tier 3: Option B — Recherche Naturelle Aviaire (Référence Officielle owluko_searching.mp4)
"""

import os
from PIL import Image, ImageDraw, ImageFont

WORKSPACE_DIR = "/Users/richard/Developer/Stickers Uko"
BRAIN_DIR = "/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68"

W, H = 1920, 1440
board = Image.new("RGBA", (W, H), (11, 15, 23, 255))
draw = ImageDraw.Draw(board)

# Fonts
FONT_HELVETICA = "/System/Library/Fonts/Helvetica.ttc"
try:
    font_title = ImageFont.truetype(FONT_HELVETICA, 20)
    font_sub = ImageFont.truetype(FONT_HELVETICA, 12)
    font_tier_title = ImageFont.truetype(FONT_HELVETICA, 14)
    font_col_title = ImageFont.truetype(FONT_HELVETICA, 12)
    font_desc = ImageFont.truetype(FONT_HELVETICA, 11)
    font_badge = ImageFont.truetype(FONT_HELVETICA, 11)
except Exception:
    font_title = font_sub = font_tier_title = font_col_title = font_desc = font_badge = ImageFont.load_default()

# 1. Main Header
draw.rectangle([0, 0, W, 70], fill=(15, 23, 42, 255))
draw.line([(0, 70), (W, 70)], fill=(217, 155, 38, 255), width=2)
draw.text((40, 14), "OWLUKO — ARBITRAGE VISUEL DE L'ANIMATION DE RECHERCHE (08_SEARCHING)", font=font_title, fill=(255, 255, 255, 255))
draw.text((40, 42), "Comparaison visuelle directe : Modèle étalon Proposition 02 vs Test Rotation 360° découpée vs Recherche Naturelle Aviaire", font=font_sub, fill=(148, 163, 184, 255))

draw.rectangle([W - 310, 18, W - 40, 52], fill=(17, 24, 39, 255), outline=(217, 155, 38, 255), width=1)
draw.text((W - 295, 28), "PLANCHE COMPARATIVE DE DÉCISION", font=font_badge, fill=(217, 155, 38, 255))

col_w = (W - 80) // 4

def draw_tier(y_start, h_tier, title, badge_text, badge_col, views_data, is_problem=False):
    draw.rectangle([40, y_start, W - 40, y_start + 40], fill=(17, 24, 39, 240), outline=(31, 41, 55, 255), width=1)
    draw.text((55, y_start + 12), title, font=font_tier_title, fill=(255, 255, 255, 255))
    
    bw = len(badge_text) * 7 + 30
    draw.rectangle([W - 55 - bw, y_start + 8, W - 55, y_start + 32], fill=(15, 23, 42, 255), outline=badge_col, width=1)
    draw.text((W - 55 - bw + 15, y_start + 14), badge_text, font=font_badge, fill=badge_col)

    card_y = y_start + 48
    card_h = h_tier - 56

    for i, (col_title, img_pil, desc, note_col) in enumerate(views_data):
        cx = 40 + i * col_w
        card_border = (239, 68, 68, 180) if is_problem and i in [1, 2, 3] else (31, 41, 55, 255)
        card_bg = (24, 16, 20, 240) if is_problem and i in [1, 2, 3] else (15, 23, 42, 220)
        draw.rectangle([cx + 5, card_y, cx + col_w - 5, card_y + card_h], fill=card_bg, outline=card_border, width=1)
        
        draw.rectangle([cx + 12, card_y + 8, cx + col_w - 12, card_y + 34], fill=(11, 15, 23, 255), outline=(51, 65, 85, 200))
        draw.text((cx + 20, card_y + 14), col_title, font=font_col_title, fill=(226, 232, 240, 255))

        target_img_h = card_h - 90
        iw, ih = img_pil.size
        s = target_img_h / float(ih)
        nw, nh = int(round(iw * s)), int(round(target_img_h))
        scaled = img_pil.resize((nw, nh), resample=Image.Resampling.LANCZOS)
        
        px = cx + 5 + (col_w - 10 - nw) // 2
        py = card_y + 40
        board.paste(scaled, (px, py), scaled)

        draw.rectangle([cx + 12, card_y + card_h - 42, cx + col_w - 12, card_y + card_h - 8], fill=(11, 15, 23, 255), outline=card_border)
        draw.text((cx + 18, card_y + card_h - 34), desc, font=font_desc, fill=note_col)

# -------------------------------------------------------------
# TIER 1: Modèle Étalon Validé (Proposition 02 Japandi)
# -------------------------------------------------------------
views_t1 = [
    ("0° — VUE DE FACE", Image.open("mascots/owluko/owluko_turnaround_view_1_front.png"), "Collerette porcelaine épurée, yeux ambre vitreux", (148, 163, 184, 255)),
    ("90°R — PROFIL DROIT", Image.open("mascots/owluko/owluko_turnaround_view_2_profile_right.png"), "Fraisette profilée, silhouette convexe continue", (148, 163, 184, 255)),
    ("180° — VUE DE DOS", Image.open("mascots/owluko/owluko_turnaround_view_4_back.png"), "Collerette nucale évasée, queue effilée", (148, 163, 184, 255)),
    ("90°L — PROFIL GAUCHE", Image.open("mascots/owluko/owluko_turnaround_view_3_profile_left.png"), "Arc facial gauche, bec doré saillant", (148, 163, 184, 255))
]
draw_tier(80, 420, "1. MODÈLE ÉTALON VALIDÉ PAR L'UTILISATEUR (PROPOSITION 02 JAPANDI)", "VALIDÉ (100% CONFORME)", (52, 211, 153, 255), views_t1)

# -------------------------------------------------------------
# TIER 2: Option A — Test de Rotation 360° par Découpe 2.5D
# -------------------------------------------------------------
views_t2 = [
    ("F00 — FACE NOMINALE", Image.open("scratch/pose_v2_00_front.png"), "0° Face : Corps et tête parfaitement raccords", (52, 211, 153, 255)),
    ("F24 — 90°R SUR CORPS FACE", Image.open("scratch/pose_v2_90_pr.png"), "DÉFAUT : Marches d'épaules découvertes & brisure", (239, 68, 68, 255)),
    ("F45 — 180° DOS SUR CORPS FACE", Image.open("scratch/pose_v2_180_back.png"), "DÉFAUT : Collerette trop haute, trou nucal visible", (239, 68, 68, 255)),
    ("F64 — 270°L SUR CORPS FACE", Image.open("scratch/pose_v2_270_pl.png"), "DÉFAUT : Retombée collerette coupée sur épaule", (239, 68, 68, 255))
]
draw_tier(520, 420, "2. OPTION A : TEST DE ROTATION 360° PAR DÉCOUPE 2.5D (DIAGNOSTIC TECHNIQUE)", "DÉFAUTS DE DÉCOUPE 2D", (239, 68, 68, 255), views_t2, is_problem=True)

# -------------------------------------------------------------
# TIER 3: Option B — Recherche Naturelle Aviaire (owluko_searching.mp4)
# -------------------------------------------------------------
views_t3 = [
    ("F00 — STANCE NOMINALE", Image.open("scratch/ref_search_clean_f0.png"), "Regard centré, posture équilibrée au sol", (52, 211, 153, 255)),
    ("F20 — TILT CURIEUX DROIT (+4.5°)", Image.open("scratch/ref_search_clean_f20.png"), "Inclinaison interrogatrice, regard ambré scrutateur", (52, 211, 153, 255)),
    ("F60 — TILT CURIEUX GAUCHE (-5.0°)", Image.open("scratch/ref_search_clean_f60.png"), "Balayage opposé curieux, 100% fluide et continu", (52, 211, 153, 255)),
    ("F80 — ATTENTION & RESPIRATION", Image.open("scratch/ref_search_clean_f80.png"), "Pause attentive, zéro coupure, silhouette pure", (52, 211, 153, 255))
]
draw_tier(960, 440, "3. OPTION B : RECHERCHE NATURELLE AVIAIRE (RÉFÉRENCE OFFICIELLE STUDIO owluko_searching.mp4)", "RECOMMANDÉ (HARMONIEUX & FLUIDE)", (217, 155, 38, 255), views_t3)

# Save board
out_path_workspace = os.path.join(WORKSPACE_DIR, "mascots/owluko/02_refonte_nouvelle/planches_comparatives/owluko_searching_options_master_board.png")
out_path_brain = os.path.join(BRAIN_DIR, "owluko_searching_options_master_board.png")
out_path_root = os.path.join(WORKSPACE_DIR, "mascots/owluko/owluko_searching_options_master_board.png")

board.save(out_path_workspace, "PNG")
board.save(out_path_brain, "PNG")
board.save(out_path_root, "PNG")

print("✅ Board updated cleanly without broken font characters!")
