#!/usr/bin/env python3
"""
Generates 10 distinct, authentic digital typographies for 'ERR' (or 'Err' / 'E R R')
matching the cyber LED digital display standard from aituko_error_404.jpeg.
Builds a master presentation board comparing all 10 options in macro view and in situ on the visor.
"""

import os
import math
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scripts.build_flawless_aituko_idle import load_master_components, transform_rgba

WORKSPACE_DIR = "/Users/richard/Developer/Stickers Uko"
OUTPUT_PATH = os.path.join(WORKSPACE_DIR, "assets/04_error_404/aituko_err_typography_proposals_board.png")
BRAIN_PATH = "/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68/aituko_err_typography_proposals_board.png"

COL_RED = (255, 59, 48, 255)
COL_HL = (255, 205, 200, 255)
COL_OFF = (45, 14, 16, 70)
COL_VISOR_BG = (12, 16, 24, 255)

# --- 1. SEGMENT GEOMETRY HELPERS ---

def draw_7seg_glyph(draw, segs, ox, oy, w=28, h=48, sw=5.5, g=1.2, italic=0.0):
    """Draws a 7-segment digit with 45° chamfered polygons."""
    mid_y = oy + h / 2
    
    # Vertices
    pts_a = [(ox + sw/2 + g, oy), (ox + w - sw/2 - g, oy), (ox + w - sw - g, oy + sw), (ox + sw + g, oy + sw)]
    pts_d = [(ox + sw + g, oy + h - sw), (ox + w - sw - g, oy + h - sw), (ox + w - sw/2 - g, oy + h), (ox + sw/2 + g, oy + h)]
    pts_g = [(ox + sw/2 + g, mid_y), (ox + sw + g, mid_y - sw/2), (ox + w - sw - g, mid_y - sw/2),
             (ox + w - sw/2 - g, mid_y), (ox + w - sw - g, mid_y + sw/2), (ox + sw + g, mid_y + sw/2)]
    pts_f = [(ox, oy + sw/2 + g), (ox + sw, oy + sw + g), (ox + sw, mid_y - sw/2 - g), (ox, mid_y - g)]
    pts_b = [(ox + w - sw, oy + sw + g), (ox + w, oy + sw/2 + g), (ox + w, mid_y - g), (ox + w - sw, mid_y - sw/2 - g)]
    pts_e = [(ox, mid_y + g), (ox + sw, mid_y + sw/2 + g), (ox + sw, oy + h - sw - g), (ox, oy + h - sw/2 - g)]
    pts_c = [(ox + w - sw, mid_y + sw/2 + g), (ox + w, mid_y + g), (ox + w, oy + h - sw/2 - g), (ox + w - sw, oy + h - sw - g)]
    
    all_segs = {'a': pts_a, 'b': pts_b, 'c': pts_c, 'd': pts_d, 'e': pts_e, 'f': pts_f, 'g': pts_g}
    
    for k, pts in all_segs.items():
        if italic != 0.0:
            shear_pts = []
            for px, py in pts:
                sx = px + (oy + h - py) * math.tan(math.radians(italic))
                shear_pts.append((sx, py))
            pts = shear_pts
            
        is_on = segs.get(k, False)
        draw.polygon(pts, fill=COL_RED if is_on else COL_OFF)
        if is_on:
            # inner highlight line
            if len(pts) == 4:
                if k in ['b', 'c', 'e', 'f']:
                    mx1, my1 = (pts[0][0] + pts[1][0])/2, (pts[0][1] + pts[1][1])/2
                    mx2, my2 = (pts[2][0] + pts[3][0])/2, (pts[2][1] + pts[3][1])/2
                else:
                    mx1, my1 = (pts[0][0] + pts[3][0])/2, (pts[0][1] + pts[3][1])/2
                    mx2, my2 = (pts[1][0] + pts[2][0])/2, (pts[1][1] + pts[2][1])/2
                draw.line([(mx1, my1), (mx2, my2)], fill=COL_HL, width=max(1, int(sw*0.25)))
            elif len(pts) == 6:
                draw.line([(pts[0][0]+sw/2, mid_y), (pts[3][0]-sw/2, mid_y)], fill=COL_HL, width=max(1, int(sw*0.25)))

def draw_14seg_glyph(draw, segs, ox, oy, w=28, h=48, sw=5.0, g=1.2):
    """Draws a 14-segment alphanumeric display glyph."""
    mid_y = oy + h / 2
    mid_x = ox + w / 2
    
    # 14 segments definitions
    pts = {
        'a1': [(ox + sw/2 + g, oy), (mid_x - g/2, oy), (mid_x - sw/2 - g/2, oy + sw), (ox + sw + g, oy + sw)],
        'a2': [(mid_x + g/2, oy), (ox + w - sw/2 - g, oy), (ox + w - sw - g, oy + sw), (mid_x + sw/2 + g/2, oy + sw)],
        'd1': [(ox + sw + g, oy + h - sw), (mid_x - sw/2 - g/2, oy + h - sw), (mid_x - g/2, oy + h), (ox + sw/2 + g, oy + h)],
        'd2': [(mid_x + sw/2 + g/2, oy + h - sw), (ox + w - sw - g, oy + h - sw), (ox + w - sw/2 - g, oy + h), (mid_x + g/2, oy + h)],
        'g1': [(ox + sw/2 + g, mid_y), (ox + sw + g, mid_y - sw/2), (mid_x - g/2, mid_y - sw/2), (mid_x - g/2, mid_y + sw/2), (ox + sw + g, mid_y + sw/2)],
        'g2': [(mid_x + g/2, mid_y - sw/2), (ox + w - sw - g, mid_y - sw/2), (ox + w - sw/2 - g, mid_y), (ox + w - sw - g, mid_y + sw/2), (mid_x + g/2, mid_y + sw/2)],
        'f':  [(ox, oy + sw/2 + g), (ox + sw, oy + sw + g), (ox + sw, mid_y - sw/2 - g), (ox, mid_y - g)],
        'b':  [(ox + w - sw, oy + sw + g), (ox + w, oy + sw/2 + g), (ox + w, mid_y - g), (ox + w - sw, mid_y - sw/2 - g)],
        'e':  [(ox, mid_y + g), (ox + sw, mid_y + sw/2 + g), (ox + sw, oy + h - sw - g), (ox, oy + h - sw/2 - g)],
        'c':  [(ox + w - sw, mid_y + sw/2 + g), (ox + w, mid_y + g), (ox + w, oy + h - sw/2 - g), (ox + w - sw, oy + h - sw - g)],
        'i':  [(mid_x - sw/2, oy + sw + g), (mid_x + sw/2, oy + sw + g), (mid_x + sw/2, mid_y - g), (mid_x - sw/2, mid_y - g)],
        'l':  [(mid_x - sw/2, mid_y + g), (mid_x + sw/2, mid_y + g), (mid_x + sw/2, oy + h - sw - g), (mid_x - sw/2, oy + h - sw - g)],
        'h':  [(ox + sw + g, oy + sw + g), (mid_x - g, mid_y - sw/2 - g), (mid_x - sw - g, mid_y - sw/2 - g)],
        'j':  [(ox + w - sw - g, oy + sw + g), (mid_x + g, mid_y - sw/2 - g), (mid_x + sw + g, mid_y - sw/2 - g)],
        'k':  [(ox + sw + g, oy + h - sw - g), (mid_x - g, mid_y + sw/2 + g), (mid_x - sw - g, mid_y + sw/2 + g)],
        'm':  [(ox + w - sw - g, oy + h - sw - g), (ox + w - 2*sw - g, oy + h - sw - g), (mid_x + g, mid_y + sw/2 + g), (mid_x + sw + g, mid_y + sw/2 + g)]
    }
    
    for k, poly in pts.items():
        is_on = segs.get(k, False)
        draw.polygon(poly, fill=COL_RED if is_on else COL_OFF)
        if is_on:
            draw.polygon(poly, outline=COL_HL, width=1)

# --- 2. GENERATE 10 TYPOGRAPHIES (Banner 260 x 80) ---

def generate_typo_banner(idx):
    im = Image.new('RGBA', (280, 90), (10, 14, 22, 255))
    draw = ImageDraw.Draw(im)
    
    # Outer bezel border
    draw.rounded_rectangle([(4, 4), (275, 85)], radius=8, fill=(14, 18, 28), outline=(40, 48, 64), width=1)
    # Inner display glass
    draw.rounded_rectangle([(10, 10), (269, 79)], radius=5, fill=(8, 11, 16))
    
    if idx == 1:
        # OPTION 1: 7-Segments Classique Industriel (E r r) - Chamfered Bevel
        e_segs = {'a': True, 'f': True, 'g': True, 'e': True, 'd': True}
        r_segs = {'e': True, 'g': True}
        draw_7seg_glyph(draw, e_segs, 45, 20, w=32, h=50, sw=6.0, g=1.5)
        draw_7seg_glyph(draw, r_segs, 115, 20, w=32, h=50, sw=6.0, g=1.5)
        draw_7seg_glyph(draw, r_segs, 185, 20, w=32, h=50, sw=6.0, g=1.5)
        
    elif idx == 2:
        # OPTION 2: 14-Segments Alphanumérique LED (E R R Majuscules)
        e_segs = {'a1': True, 'a2': True, 'f': True, 'e': True, 'd1': True, 'd2': True, 'g1': True, 'g2': True}
        r_segs = {'a1': True, 'a2': True, 'f': True, 'e': True, 'b': True, 'g1': True, 'g2': True, 'm': True}
        draw_14seg_glyph(draw, e_segs, 45, 20, w=32, h=50, sw=5.0, g=1.2)
        draw_14seg_glyph(draw, r_segs, 115, 20, w=32, h=50, sw=5.0, g=1.2)
        draw_14seg_glyph(draw, r_segs, 185, 20, w=32, h=50, sw=5.0, g=1.2)
        
    elif idx == 3:
        # OPTION 3: 16-Segments Haute Définition (E R R Majuscules avec boucle douce)
        # Similar to 14-seg but with narrower stroke, dual diagonal leg
        e_segs = {'a1': True, 'a2': True, 'f': True, 'e': True, 'd1': True, 'd2': True, 'g1': True}
        r_segs = {'a1': True, 'a2': True, 'f': True, 'e': True, 'b': True, 'g1': True, 'g2': True, 'm': True}
        draw_14seg_glyph(draw, e_segs, 45, 20, w=34, h=50, sw=4.2, g=1.0)
        draw_14seg_glyph(draw, r_segs, 115, 20, w=34, h=50, sw=4.2, g=1.0)
        draw_14seg_glyph(draw, r_segs, 185, 20, w=34, h=50, sw=4.2, g=1.0)
        
    elif idx == 4:
        # OPTION 4: 7-Segments Italique Sportif 12° (E r r Incliné)
        e_segs = {'a': True, 'f': True, 'g': True, 'e': True, 'd': True}
        r_segs = {'e': True, 'g': True}
        draw_7seg_glyph(draw, e_segs, 50, 20, w=30, h=50, sw=6.0, g=1.5, italic=12.0)
        draw_7seg_glyph(draw, r_segs, 120, 20, w=30, h=50, sw=6.0, g=1.5, italic=12.0)
        draw_7seg_glyph(draw, r_segs, 190, 20, w=30, h=50, sw=6.0, g=1.5, italic=12.0)
        
    elif idx == 5:
        # OPTION 5: 7-Segments Majuscule Hybride (E R R - R avec boucle haute et pied droit)
        e_segs = {'a': True, 'f': True, 'g': True, 'e': True, 'd': True}
        # Hybride R en 7-seg: boucle haute (a, b, f, g) + pied inférieur droit (c)
        r_hybrid = {'a': True, 'b': True, 'f': True, 'g': True, 'c': True}
        draw_7seg_glyph(draw, e_segs, 45, 20, w=32, h=50, sw=6.0, g=1.5)
        draw_7seg_glyph(draw, r_hybrid, 115, 20, w=32, h=50, sw=6.0, g=1.5)
        draw_7seg_glyph(draw, r_hybrid, 185, 20, w=32, h=50, sw=6.0, g=1.5)
        
    elif idx == 6:
        # OPTION 6: Dot-Matrix LED 5x7 (E R R Pastilles Circulaires)
        # 5 cols x 7 rows
        matrix_E = [
            [1,1,1,1,1],
            [1,0,0,0,0],
            [1,0,0,0,0],
            [1,1,1,1,0],
            [1,0,0,0,0],
            [1,0,0,0,0],
            [1,1,1,1,1]
        ]
        matrix_R = [
            [1,1,1,1,0],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,1,1,1,0],
            [1,0,1,0,0],
            [1,0,0,1,0],
            [1,0,0,0,1]
        ]
        
        def draw_matrix(mat, ox, oy, pr=2.6, gap=6.5):
            for r in range(7):
                for c in range(5):
                    cx = ox + c * gap
                    cy = oy + r * gap
                    on = mat[r][c] == 1
                    draw.ellipse([cx - pr, cy - pr, cx + pr, cy + pr], fill=COL_RED if on else COL_OFF)
                    if on:
                        draw.ellipse([cx - pr*0.5, cy - pr*0.5, cx + pr*0.5, cy + pr*0.5], fill=COL_HL)
                        
        draw_matrix(matrix_E, 45, 22)
        draw_matrix(matrix_R, 120, 22)
        draw_matrix(matrix_R, 195, 22)
        
    elif idx == 7:
        # OPTION 7: Digital LCD Monospace à Fentes Technologiques (Cyber Segment)
        def draw_stencil_char(char, ox, oy, w=32, h=50, sw=5.5):
            # Outline-based tech stencil
            if char == 'E':
                draw.rectangle([(ox, oy), (ox + sw, oy + h)], fill=COL_RED)
                draw.rectangle([(ox + sw + 2, oy), (ox + w, oy + sw)], fill=COL_RED)
                draw.rectangle([(ox + sw + 2, oy + h/2 - sw/2), (ox + w - 4, oy + h/2 + sw/2)], fill=COL_RED)
                draw.rectangle([(ox + sw + 2, oy + h - sw), (ox + w, oy + h)], fill=COL_RED)
                draw.line([(ox+sw/2, oy+2), (ox+sw/2, oy+h-2)], fill=COL_HL, width=1)
            elif char == 'R':
                draw.rectangle([(ox, oy), (ox + sw, oy + h)], fill=COL_RED)
                draw.rectangle([(ox + sw + 2, oy), (ox + w - sw, oy + sw)], fill=COL_RED)
                draw.rectangle([(ox + w - sw, oy), (ox + w, oy + h/2)], fill=COL_RED)
                draw.rectangle([(ox + sw + 2, oy + h/2 - sw), (ox + w - sw, oy + h/2)], fill=COL_RED)
                # Diagonal leg
                draw.polygon([(ox + sw + 2, oy + h/2), (ox + sw*2 + 2, oy + h/2), (ox + w, oy + h), (ox + w - sw, oy + h)], fill=COL_RED)
                draw.line([(ox+sw/2, oy+2), (ox+sw/2, oy+h-2)], fill=COL_HL, width=1)
                
        draw_stencil_char('E', 45, 20)
        draw_stencil_char('R', 115, 20)
        draw_stencil_char('R', 185, 20)
        
    elif idx == 8:
        # OPTION 8: 7-Segments Épais Bezel Intégré (Style Fente Basse Visière Référence)
        # Lower visor slot with intense neon glow
        draw.rounded_rectangle([(30, 16), (250, 74)], radius=8, fill=(6, 8, 12), outline=(180, 30, 30), width=1)
        e_segs = {'a': True, 'f': True, 'g': True, 'e': True, 'd': True}
        r_segs = {'e': True, 'g': True}
        draw_7seg_glyph(draw, e_segs, 55, 23, w=30, h=44, sw=7.0, g=1.5)
        draw_7seg_glyph(draw, r_segs, 120, 23, w=30, h=44, sw=7.0, g=1.5)
        draw_7seg_glyph(draw, r_segs, 185, 23, w=30, h=44, sw=7.0, g=1.5)
        
    elif idx == 9:
        # OPTION 9: Micro-LED Grille Carrée 8-Bit (Pixel Digital Matrix)
        matrix_E = [
            [1,1,1,1],
            [1,0,0,0],
            [1,1,1,0],
            [1,0,0,0],
            [1,1,1,1]
        ]
        matrix_R = [
            [1,1,1,0],
            [1,0,0,1],
            [1,1,1,0],
            [1,0,1,0],
            [1,0,0,1]
        ]
        def draw_pixel_grid(mat, ox, oy, ps=8, g=1.5):
            for r in range(5):
                for c in range(4):
                    x = ox + c * (ps + g)
                    y = oy + r * (ps + g)
                    on = mat[r][c] == 1
                    draw.rectangle([(x, y), (x + ps, y + ps)], fill=COL_RED if on else COL_OFF)
                    if on:
                        draw.rectangle([(x+1, y+1), (x + ps - 1, y + ps - 1)], outline=COL_HL, width=1)
                        
        draw_pixel_grid(matrix_E, 45, 22)
        draw_pixel_grid(matrix_R, 120, 22)
        draw_pixel_grid(matrix_R, 195, 22)
        
    elif idx == 10:
        # OPTION 10: 7-Segments Arrondi Moderne (Rounded Capsule Segments)
        def draw_rounded_7seg(segs, ox, oy, w=30, h=50, sw=6.5):
            mid_y = oy + h / 2
            # Horizontal capsules
            if segs.get('a', False): draw.rounded_rectangle([(ox+sw/2, oy), (ox+w-sw/2, oy+sw)], radius=sw/2, fill=COL_RED)
            if segs.get('g', False): draw.rounded_rectangle([(ox+sw/2, mid_y-sw/2), (ox+w-sw/2, mid_y+sw/2)], radius=sw/2, fill=COL_RED)
            if segs.get('d', False): draw.rounded_rectangle([(ox+sw/2, oy+h-sw), (ox+w-sw/2, oy+h)], radius=sw/2, fill=COL_RED)
            # Vertical capsules
            if segs.get('f', False): draw.rounded_rectangle([(ox, oy+sw/2), (ox+sw, mid_y-sw/2)], radius=sw/2, fill=COL_RED)
            if segs.get('b', False): draw.rounded_rectangle([(ox+w-sw, oy+sw/2), (ox+w, mid_y-sw/2)], radius=sw/2, fill=COL_RED)
            if segs.get('e', False): draw.rounded_rectangle([(ox, mid_y+sw/2), (ox+sw, oy+h-sw/2)], radius=sw/2, fill=COL_RED)
            if segs.get('c', False): draw.rounded_rectangle([(ox+w-sw, mid_y+sw/2), (ox+w, oy+h-sw/2)], radius=sw/2, fill=COL_RED)
            
        e_segs = {'a': True, 'f': True, 'g': True, 'e': True, 'd': True}
        r_segs = {'e': True, 'g': True}
        draw_rounded_7seg(e_segs, 45, 20)
        draw_rounded_7seg(r_segs, 115, 20)
        draw_rounded_7seg(r_segs, 185, 20)
        
    # Apply subtle realistic neon bloom
    bloom = im.filter(ImageFilter.GaussianBlur(1.5))
    result = Image.alpha_composite(bloom, im)
    return result

# --- 3. IN SITU RENDER ON ROBOT VISOR (512 x 512 cropped to 300 x 300) ---

def generate_in_situ_visor(idx, master_comps):
    head_comp = master_comps['head'].copy()
    # Infill cyan halo pixels with obsidian black
    is_cyan = (head_comp[:, :, 0] < 120) & (head_comp[:, :, 1] > 140) & (head_comp[:, :, 2] > 160) & (head_comp[:, :, 3] > 80)
    head_comp[is_cyan, :3] = [14, 18, 26]
    
    canvas = Image.new('RGBA', (512, 512), (11, 15, 23, 255))
    
    # Slumped head at dy = 78, rot = 3.6°
    head_pivot = (256.0, 124.0)
    w_head = transform_rgba(head_comp, head_pivot, angle_deg=3.6, scale=(1.04, 1.04), translate=(0.0, 78.0))
    canvas.alpha_composite(Image.fromarray(w_head))
    
    # Layer for visor typography
    layer_v = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
    draw_v = ImageDraw.Draw(layer_v)
    
    # Draw scaled typography at center of visor: cx = 256, cy = 120
    # In situ size is scaled to fit visor (~100px wide, ~30px high)
    if idx == 1:
        # 7-seg E r r
        e_segs = {'a': True, 'f': True, 'g': True, 'e': True, 'd': True}
        r_segs = {'e': True, 'g': True}
        draw_7seg_glyph(draw_v, e_segs, 214, 105, w=20, h=32, sw=3.8, g=1.0)
        draw_7seg_glyph(draw_v, r_segs, 244, 105, w=20, h=32, sw=3.8, g=1.0)
        draw_7seg_glyph(draw_v, r_segs, 274, 105, w=20, h=32, sw=3.8, g=1.0)
    elif idx == 2:
        # 14-seg E R R
        e_segs = {'a1': True, 'a2': True, 'f': True, 'e': True, 'd1': True, 'd2': True, 'g1': True, 'g2': True}
        r_segs = {'a1': True, 'a2': True, 'f': True, 'e': True, 'b': True, 'g1': True, 'g2': True, 'm': True}
        draw_14seg_glyph(draw_v, e_segs, 214, 105, w=20, h=32, sw=3.2, g=0.8)
        draw_14seg_glyph(draw_v, r_segs, 244, 105, w=20, h=32, sw=3.2, g=0.8)
        draw_14seg_glyph(draw_v, r_segs, 274, 105, w=20, h=32, sw=3.2, g=0.8)
    elif idx == 3:
        # 16-seg E R R
        e_segs = {'a1': True, 'a2': True, 'f': True, 'e': True, 'd1': True, 'd2': True, 'g1': True}
        r_segs = {'a1': True, 'a2': True, 'f': True, 'e': True, 'b': True, 'g1': True, 'g2': True, 'm': True}
        draw_14seg_glyph(draw_v, e_segs, 214, 105, w=20, h=32, sw=2.8, g=0.7)
        draw_14seg_glyph(draw_v, r_segs, 244, 105, w=20, h=32, sw=2.8, g=0.7)
        draw_14seg_glyph(draw_v, r_segs, 274, 105, w=20, h=32, sw=2.8, g=0.7)
    elif idx == 4:
        # 7-seg italic 12°
        e_segs = {'a': True, 'f': True, 'g': True, 'e': True, 'd': True}
        r_segs = {'e': True, 'g': True}
        draw_7seg_glyph(draw_v, e_segs, 216, 105, w=18, h=32, sw=3.8, g=1.0, italic=12.0)
        draw_7seg_glyph(draw_v, r_segs, 246, 105, w=18, h=32, sw=3.8, g=1.0, italic=12.0)
        draw_7seg_glyph(draw_v, r_segs, 276, 105, w=18, h=32, sw=3.8, g=1.0, italic=12.0)
    elif idx == 5:
        # 7-seg hybride E R R
        e_segs = {'a': True, 'f': True, 'g': True, 'e': True, 'd': True}
        r_hybrid = {'a': True, 'b': True, 'f': True, 'g': True, 'c': True}
        draw_7seg_glyph(draw_v, e_segs, 214, 105, w=20, h=32, sw=3.8, g=1.0)
        draw_7seg_glyph(draw_v, r_hybrid, 244, 105, w=20, h=32, sw=3.8, g=1.0)
        draw_7seg_glyph(draw_v, r_hybrid, 274, 105, w=20, h=32, sw=3.8, g=1.0)
    elif idx == 6:
        # Dot-Matrix 5x7
        matrix_E = [[1,1,1,1,1],[1,0,0,0,0],[1,0,0,0,0],[1,1,1,1,0],[1,0,0,0,0],[1,0,0,0,0],[1,1,1,1,1]]
        matrix_R = [[1,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,0],[1,0,1,0,0],[1,0,0,1,0],[1,0,0,0,1]]
        def draw_m(mat, ox, oy, pr=1.5, gap=4.2):
            for r in range(7):
                for c in range(5):
                    cx = ox + c * gap
                    cy = oy + r * gap
                    if mat[r][c] == 1:
                        draw_v.ellipse([cx - pr, cy - pr, cx + pr, cy + pr], fill=COL_RED)
                        draw_v.ellipse([cx - pr*0.5, cy - pr*0.5, cx + pr*0.5, cy + pr*0.5], fill=COL_HL)
        draw_m(matrix_E, 214, 107)
        draw_m(matrix_R, 244, 107)
        draw_m(matrix_R, 274, 107)
    elif idx == 7:
        # LCD Stencil
        def draw_st(char, ox, oy, w=20, h=32, sw=3.6):
            if char == 'E':
                draw_v.rectangle([(ox, oy), (ox + sw, oy + h)], fill=COL_RED)
                draw_v.rectangle([(ox + sw + 1, oy), (ox + w, oy + sw)], fill=COL_RED)
                draw_v.rectangle([(ox + sw + 1, oy + h/2 - sw/2), (ox + w - 3, oy + h/2 + sw/2)], fill=COL_RED)
                draw_v.rectangle([(ox + sw + 1, oy + h - sw), (ox + w, oy + h)], fill=COL_RED)
            elif char == 'R':
                draw_v.rectangle([(ox, oy), (ox + sw, oy + h)], fill=COL_RED)
                draw_v.rectangle([(ox + sw + 1, oy), (ox + w - sw, oy + sw)], fill=COL_RED)
                draw_v.rectangle([(ox + w - sw, oy), (ox + w, oy + h/2)], fill=COL_RED)
                draw_v.rectangle([(ox + sw + 1, oy + h/2 - sw), (ox + w - sw, oy + h/2)], fill=COL_RED)
                draw_v.polygon([(ox + sw + 1, oy + h/2), (ox + sw*2 + 1, oy + h/2), (ox + w, oy + h), (ox + w - sw, oy + h)], fill=COL_RED)
        draw_st('E', 214, 105)
        draw_st('R', 244, 105)
        draw_st('R', 274, 105)
    elif idx == 8:
        # Lower Visor Bezel Slot (like reference 404!)
        draw_v.chord([256 - 40, 146 - 12, 256 + 40, 146 + 12], start=0, end=180, fill=(12, 5, 7, 220), outline=(80, 14, 18), width=1)
        e_segs = {'a': True, 'f': True, 'g': True, 'e': True, 'd': True}
        r_segs = {'e': True, 'g': True}
        draw_7seg_glyph(draw_v, e_segs, 222, 138, w=18, h=22, sw=3.0, g=0.8)
        draw_7seg_glyph(draw_v, r_segs, 246, 138, w=18, h=22, sw=3.0, g=0.8)
        draw_7seg_glyph(draw_v, r_segs, 270, 138, w=18, h=22, sw=3.0, g=0.8)
    elif idx == 9:
        # Micro-LED 8-bit
        matrix_E = [[1,1,1,1],[1,0,0,0],[1,1,1,0],[1,0,0,0],[1,1,1,1]]
        matrix_R = [[1,1,1,0],[1,0,0,1],[1,1,1,0],[1,0,1,0],[1,0,0,1]]
        def draw_px(mat, ox, oy, ps=4.5, g=1.0):
            for r in range(5):
                for c in range(4):
                    if mat[r][c] == 1:
                        x = ox + c * (ps + g)
                        y = oy + r * (ps + g)
                        draw_v.rectangle([(x, y), (x + ps, y + ps)], fill=COL_RED)
                        draw_v.rectangle([(x+0.5, y+0.5), (x + ps - 0.5, y + ps - 0.5)], outline=COL_HL, width=1)
        draw_px(matrix_E, 215, 108)
        draw_px(matrix_R, 245, 108)
        draw_px(matrix_R, 275, 108)
    elif idx == 10:
        # Rounded 7-seg
        def draw_r7(segs, ox, oy, w=20, h=32, sw=4.0):
            mid_y = oy + h / 2
            if segs.get('a', False): draw_v.rounded_rectangle([(ox+sw/2, oy), (ox+w-sw/2, oy+sw)], radius=sw/2, fill=COL_RED)
            if segs.get('g', False): draw_v.rounded_rectangle([(ox+sw/2, mid_y-sw/2), (ox+w-sw/2, mid_y+sw/2)], radius=sw/2, fill=COL_RED)
            if segs.get('d', False): draw_v.rounded_rectangle([(ox+sw/2, oy+h-sw), (ox+w-sw/2, oy+h)], radius=sw/2, fill=COL_RED)
            if segs.get('f', False): draw_v.rounded_rectangle([(ox, oy+sw/2), (ox+sw, mid_y-sw/2)], radius=sw/2, fill=COL_RED)
            if segs.get('b', False): draw_v.rounded_rectangle([(ox+w-sw, oy+sw/2), (ox+w, mid_y-sw/2)], radius=sw/2, fill=COL_RED)
            if segs.get('e', False): draw_v.rounded_rectangle([(ox, mid_y+sw/2), (ox+sw, oy+h-sw/2)], radius=sw/2, fill=COL_RED)
            if segs.get('c', False): draw_v.rounded_rectangle([(ox+w-sw, mid_y+sw/2), (ox+w, oy+h-sw/2)], radius=sw/2, fill=COL_RED)
        e_segs = {'a': True, 'f': True, 'g': True, 'e': True, 'd': True}
        r_segs = {'e': True, 'g': True}
        draw_r7(e_segs, 214, 105)
        draw_r7(r_segs, 244, 105)
        draw_r7(r_segs, 274, 105)
        
    # Transform visor layer with head tilt
    w_visor = transform_rgba(np.array(layer_v), head_pivot, angle_deg=3.6, scale=(1.04, 1.04), translate=(0.0, 78.0))
    im_v = Image.fromarray(w_visor)
    canvas.alpha_composite(im_v.filter(ImageFilter.GaussianBlur(1.8)))
    canvas.alpha_composite(im_v)
    
    # Crop head area (x in [130, 382], y in [130, 330])
    crop_head = canvas.crop((150, 140, 362, 310))
    return crop_head

# --- 4. BUILD MASTER PRESENTATION BOARD ---

def build_master_proposals_board():
    print("🎨 Building Master 10 Typography Proposals Board...")
    master_comps = load_master_components()
    
    font_title = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 26)
    font_sub = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 15)
    font_card_num = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 16)
    font_card_title = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 14)
    font_body = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 12)
    font_badge = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 11)
    
    board_w = 2300
    board_h = 1620
    board = Image.new('RGB', (board_w, board_h), (11, 15, 23))
    draw = ImageDraw.Draw(board)
    
    # Header Banner
    draw.rectangle([(0, 0), (board_w, 100)], fill=(16, 22, 34))
    draw.text((50, 20), "10 PROPOSITIONS DE TYPOGRAPHIES DIGITALES 'E R R' (STANDARD CYBER LED DU 404)", font=font_title, fill=(0, 240, 255))
    draw.text((50, 60), "Conception géométrique vectorielle stricte : segments biseautés à 45°, cœurs néon et bloom, affichages 7-seg / 14-seg / matrice LED.", font=font_sub, fill=(200, 215, 235))
    
    # Reference comparison card on the right of header
    ref_crop = Image.open('scratch/ref_404_typography_crop.png').resize((200, 75))
    board.paste(ref_crop, (board_w - 260, 12))
    draw.rectangle([(board_w - 262, 10), (board_w - 58, 89)], outline=(255, 60, 60), width=1)
    draw.text((board_w - 255, 14), "RÉFÉRENCE 404 (CIBLE)", font=font_badge, fill=(255, 255, 255))
    
    # Metadata for the 10 options
    options_meta = [
        (1, "Option 01 : 7-Segments Classique Industriel", "Format 'E r r' standard (ISO 7-seg).",
         "Segments biseautés 45°, segments fantômes éteints visibles en arrière-plan.\nIdentique à la technologie d'affichage du 404 de référence.\nClair, universel et immédiatement lisible.",
         (0, 240, 255), "RECOMMANDÉ — FIDÉLITÉ 404"),
        (2, "Option 02 : 14-Segments Alphanumérique LED", "Format 'E R R' Majuscules Complètes.",
         "Standard avionique et médical. Les 'R' possèdent leur boucle et leur jambe diagonale.\nPermet d'écrire 'E R R' en toutes majuscules sur matrice segmentée.\nLook instrument de bord très professionnel.",
         (100, 255, 140), "MAJUSCULES STRICTES"),
        (3, "Option 03 : 16-Segments Haute Définition", "Format 'E R R' Alphanumérique Fin.",
         "16 segments fins par caractère, barre médiane centrée.\nPermet des arrondis optiques et une silhouette technologique élancée.\nStyle matériel audio de précision / rack de laboratoire.",
         (255, 215, 0), "HAUTE PRÉCISION"),
        (4, "Option 04 : 7-Segments Italique Sportif 12°", "Format 'E r r' Dynamique Incliné.",
         "Inclinaison dynamique de 12° vers la droite, segments biseautés.\nÉvoque les chronomètres de sport, compteurs de vitesse et horloges Casio.\nApporte du dynamisme et de la tension à l'état d'erreur.",
         (255, 140, 50), "DYNAMIQUE & SPORT"),
        (5, "Option 05 : 7-Segments Majuscule Hybride", "Format 'E R R' Majuscules Stylisées.",
         "Boucle haute (a,b,f,g) + jambe droite (c). Écrit un 'R' majuscule reconnaissable\nsans recourir à un afficheur 14-segments.\nLook vintage des synthétiseurs et amplis des années 80.",
         (200, 150, 255), "VINTAGE CYBER 80s"),
        (6, "Option 06 : Matrice de Points LED 5x7", "Format 'E R R' Dot Matrix Display.",
         "Matrice de pastilles LED rondes (5 colonnes x 7 rangées).\nTypographie majuscule classique des panneaux d'urgence réseau et serveurs.\nEffet de lueur sphérique individuelle sur chaque LED.",
         (255, 100, 180), "DOT MATRIX LED"),
        (7, "Option 07 : Digital LCD Stencil à Fentes", "Format 'E R R' Monospace Technologique.",
         "Lignes épaisses numériques avec micro-fentes horizontales et verticales.\nInspiration cockpit de science-fiction et interfaces HUD de mecha.\nTrès fort impact visuel, géométrie compacte et solide.",
         (80, 220, 255), "HUD SCI-FI MONOSPACE"),
        (8, "Option 08 : 7-Segments Épais dans Fente Bezel", "Format 'E r r' Bas de Visière (Fidèle Référence).",
         "Réplique la fente basse intégrée au bas de la visière dans le rendu 3D.\nSegments très épais logés dans un cartouche biseauté en verre teinté.\nLaisse le haut de la visière libre pour les expressions.",
         (255, 80, 80), "RÉPLIQUE EMPLACEMENT 3D"),
        (9, "Option 09 : Micro-LED Grille Carrée 8-Bit", "Format 'E R R' Pixel Grid OLED.",
         "Grille de micro-pixels carrés réguliers avec trame de masque sous-jacente.\nLook terminal digital rétro-futuriste / écran OLED monochrome.\nContraste saisissant et netteté géométrique parfaite.",
         (140, 255, 200), "PIXEL OLED 8-BIT"),
        (10, "Option 10 : 7-Segments Arrondi Moderne", "Format 'E r r' Capsule Soft Rounded.",
         "Segments 7-seg aux extrémités adoucies en capsule sans angles vifs.\nInspiration montres connectées modernes et appareils domotiques épurés.\nÉquilibre entre rigueur numérique et rondeur conviviale.",
         (255, 220, 120), "MODERNE ÉPURÉ")
    ]
    
    # 2 rows of 5 cards
    card_w = 425
    card_h = 690
    
    for opt_idx in range(1, 11):
        num, title, subtitle, desc, accent_col, tag = options_meta[opt_idx - 1]
        
        row = 0 if opt_idx <= 5 else 1
        col = (opt_idx - 1) % 5
        
        bx = 40 + col * (card_w + 20)
        by = 130 + row * (card_h + 30)
        
        # Card Background
        draw.rounded_rectangle([(bx, by), (bx + card_w, by + card_h)], radius=12, fill=(18, 24, 38), outline=accent_col, width=2 if opt_idx == 1 else 1)
        
        # Header inside card
        draw.rounded_rectangle([(bx, by), (bx + card_w, by + 50)], radius=10, fill=(24, 32, 50))
        draw.text((bx + 15, by + 14), title, font=font_card_title, fill=accent_col)
        
        # Tag Badge
        draw.rounded_rectangle([(bx + 15, by + 60), (bx + card_w - 15, by + 82)], radius=4, fill=(30, 42, 64))
        draw.text((bx + 25, by + 65), tag, font=font_badge, fill=accent_col)
        
        # Section A: Macro Typography Banner
        draw.text((bx + 15, by + 95), "1. Vue Rapprochée / Segments LED :", font=font_badge, fill=(180, 195, 215))
        banner = generate_typo_banner(opt_idx).resize((card_w - 30, 95))
        board.paste(banner, (bx + 15, by + 115))
        
        # Section B: In Situ Visor View
        draw.text((bx + 15, by + 225), "2. Intégration Réelle sur Visière AItuko :", font=font_badge, fill=(180, 195, 215))
        in_situ = generate_in_situ_visor(opt_idx, master_comps).resize((card_w - 30, 240))
        board.paste(in_situ, (bx + 15, by + 245))
        
        # Section C: Description & Spec
        draw.rounded_rectangle([(bx + 15, by + 500), (bx + card_w - 15, by + card_h - 20)], radius=6, fill=(14, 18, 28), outline=(35, 45, 65), width=1)
        draw.text((bx + 25, by + 510), subtitle, font=font_card_title, fill=(240, 240, 240))
        lines = desc.split('\n')
        for l_idx, line in enumerate(lines):
            draw.text((bx + 25, by + 538 + l_idx * 20), line, font=font_body, fill=(190, 205, 220))
            
    board.save(OUTPUT_PATH)
    board.save(BRAIN_PATH)
    print(f"✅ Successfully saved Master Proposals Board to {OUTPUT_PATH}")
    print(f"✅ Successfully copied to brain directory {BRAIN_PATH}")

if __name__ == "__main__":
    build_master_proposals_board()
