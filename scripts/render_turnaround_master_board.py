#!/usr/bin/env python3
"""
Official AItuko Master Turnaround Model Sheet Generator.
Generates:
1. aituko_master_turnaround_sheet.png (Our Master Model across 4 angles: 0° Face, 45° 3/4, 90° Profil, 180° Dos)
2. aituko_studio_turnaround_sheet.png (Cleaned Studio 3D reference across 4 angles on dark studio backdrop)
3. aituko_turnaround_master_board.png (Side-by-side dual board: Studio Reference vs Our Master Model)
4. aituko_master_turnaround.svg (Standalone 4-view pure vector SVG)
"""

import os
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

BRAIN_DIR = "/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68"
WORKSPACE_DIR = "/Users/richard/Developer/Stickers Uko"

# Studio Theme
COLOR_BG = (11, 15, 23, 255)
COLOR_CARD = (17, 24, 39, 230)
COLOR_BORDER = (31, 41, 55, 220)
COLOR_CYAN = (0, 240, 255, 255)
COLOR_EMERALD = (52, 211, 153, 255)
COLOR_WHITE = (255, 255, 255, 255)
COLOR_MUTED = (148, 163, 184, 255)

PORCELAIN_FILL = (255, 255, 255, 255)
PORCELAIN_OUTLINE = (210, 218, 228, 255)
VISOR_GLASS = (12, 14, 20, 255)
VISOR_RIM = (28, 33, 46, 255)
NECK_SOCKET = (26, 32, 44, 255)

def get_smooth_contour(mask, eps=1.0):
    blur = cv2.GaussianBlur(mask, (5, 5), 1.0)
    _, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
    cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not cnts:
        return []
    cnt = max(cnts, key=cv2.contourArea)
    approx = cv2.approxPolyDP(cnt, eps, True)
    return approx.reshape(-1, 2)

def extract_view_geometry(view_name):
    rgba = cv2.imread(f"scratch/turnaround_views/{view_name}_clean.png", cv2.IMREAD_UNCHANGED)
    h, w, _ = rgba.shape
    alpha = rgba[:, :, 3]
    gray = cv2.cvtColor(rgba[:, :, :3], cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(rgba[:, :, :3], cv2.COLOR_BGR2HSV)
    
    char_mask = (alpha > 80).astype(np.uint8) * 255
    
    # 1. Cyan Eyes
    cyan_mask = (hsv[:, :, 0] >= 75) & (hsv[:, :, 0] <= 115) & (hsv[:, :, 1] >= 60) & (hsv[:, :, 2] >= 75)
    ec, _ = cv2.findContours(cyan_mask.astype(np.uint8)*255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    eyes_pts = []
    for c in ec:
        if cv2.contourArea(c) > 15:
            approx = cv2.approxPolyDP(c, 0.6, True).reshape(-1, 2)
            eyes_pts.append(approx)
    eyes_pts.sort(key=lambda pts: np.min(pts[:, 0]))
    
    # 2. Visor (if not back)
    visor_pts = []
    if view_name != "back":
        head_crop = np.zeros_like(char_mask)
        head_crop[:175, :] = char_mask[:175, :]
        v_cand = (head_crop > 0) & (gray < 85)
        v_mask = cv2.morphologyEx(v_cand.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
        vc, _ = cv2.findContours(v_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in vc:
            if cv2.contourArea(c) > 500:
                approx = cv2.approxPolyDP(c, 0.8, True).reshape(-1, 2)
                visor_pts.append(approx)
                
    # 3. Head Dome (y < 196)
    head_mask = np.zeros_like(char_mask)
    head_mask[:196, :] = char_mask[:196, :]
    head_mask = cv2.morphologyEx(head_mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)))
    head_pts = get_smooth_contour(head_mask, eps=1.0)
    
    # 4. Neck Socket
    neck_mask = np.zeros_like(char_mask)
    neck_mask[190:205, :] = (char_mask[190:205, :] > 0) & (gray[190:205, :] < 140)
    nc, _ = cv2.findContours(neck_mask.astype(np.uint8)*255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    neck_pts = []
    for c in nc:
        if cv2.contourArea(c) > 40:
            neck_pts.append(cv2.approxPolyDP(c, 0.8, True).reshape(-1, 2))
            
    # 5. Feet (y > 415)
    feet_mask = np.zeros_like(char_mask)
    feet_mask[415:, :] = char_mask[415:, :]
    fc, _ = cv2.findContours(feet_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    feet_pts = []
    for c in fc:
        if cv2.contourArea(c) > 200:
            feet_pts.append(cv2.approxPolyDP(c, 0.8, True).reshape(-1, 2))
    feet_pts.sort(key=lambda pts: np.min(pts[:, 0]))
    
    # 6. Torso & Pods
    body_mask = np.zeros_like(char_mask)
    body_mask[196:418, :] = char_mask[196:418, :]
    
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(body_mask)
    torso_pts = []
    pods_pts = []
    
    if num_labels > 2:
        comps = []
        for i in range(1, num_labels):
            if stats[i, cv2.CC_STAT_AREA] > 300:
                comps.append((stats[i, cv2.CC_STAT_AREA], i))
        comps.sort(reverse=True)
        if comps:
            torso_label = comps[0][1]
            t_mask = (labels == torso_label).astype(np.uint8)*255
            torso_pts.append(get_smooth_contour(t_mask, eps=1.0))
            for _, lab in comps[1:]:
                p_mask = (labels == lab).astype(np.uint8)*255
                pods_pts.append(get_smooth_contour(p_mask, eps=1.0))
    else:
        torso_pts.append(get_smooth_contour(body_mask, eps=1.0))
        
    return {
        "view": view_name,
        "w": w, "h": h,
        "head": head_pts,
        "visor": visor_pts,
        "eyes": eyes_pts,
        "neck": neck_pts,
        "torso": torso_pts,
        "pods": pods_pts,
        "feet": feet_pts
    }

def render_master_figure(data, target_h=460, scale=4):
    orig_h = data["h"]
    orig_w = data["w"]
    s = (target_h / float(orig_h)) * scale
    
    canv_w = int(orig_w * s) + 40 * scale
    canv_h = int(target_h * scale) + 60 * scale
    off_x = 20 * scale
    off_y = 15 * scale
    
    img = Image.new("RGBA", (canv_w, canv_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    def S(pts):
        return [(int(round(pt[0] * s + off_x)), int(round(pt[1] * s + off_y))) for pt in pts]
    
    # 1. Soft Ambient Ground Shadow
    sh_layer = Image.new("RGBA", (canv_w, canv_h), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(sh_layer)
    cx = canv_w // 2
    cy = int(target_h * scale + 24 * scale)
    rx = int(orig_w * 0.36 * s)
    ry = int(11 * scale)
    sh_draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(0, 0, 0, 150))
    sh_layer = sh_layer.filter(ImageFilter.GaussianBlur(radius=6 * scale))
    img.alpha_composite(sh_layer)
    
    # 2. Feet Landing Pods (Spotless White + Bottom Cyan Glow)
    for f in data["feet"]:
        pts = S(f)
        if len(pts) >= 3:
            fx = int(np.mean([p[0] for p in pts]))
            fy = int(np.max([p[1] for p in pts]))
            fg = Image.new("RGBA", (canv_w, canv_h), (0, 0, 0, 0))
            ImageDraw.Draw(fg).ellipse([fx - int(12*scale), fy - int(3*scale), fx + int(12*scale), fy + int(6*scale)], fill=(0, 240, 255, 140))
            fg = fg.filter(ImageFilter.GaussianBlur(radius=4 * scale))
            img.alpha_composite(fg)
            draw.polygon(pts, fill=PORCELAIN_FILL, outline=PORCELAIN_OUTLINE, width=max(1, int(1.2 * scale)))
            
    # 3. Torso Capsule (Spotless Uniform White Porcelain - ZERO SMUDGES)
    for t in data["torso"]:
        pts = S(t)
        if len(pts) >= 3:
            draw.polygon(pts, fill=PORCELAIN_FILL, outline=PORCELAIN_OUTLINE, width=max(1, int(1.2 * scale)))
            
    # 4. In Profile or 3/4: Render the floating winglet pod with smooth capsule
    if data["view"] == "profile":
        # Centered winglet capsule: x: 96..154, y: 252..388
        p_box = [int(96 * s + off_x), int(252 * s + off_y), int(154 * s + off_x), int(388 * s + off_y)]
        rad = int(28 * s)
        # Thruster glow
        pcx = (p_box[0] + p_box[2]) // 2
        pcy = p_box[3]
        pg = Image.new("RGBA", (canv_w, canv_h), (0, 0, 0, 0))
        ImageDraw.Draw(pg).ellipse([pcx - int(10*scale), pcy - int(3*scale), pcx + int(10*scale), pcy + int(6*scale)], fill=(0, 240, 255, 130))
        pg = pg.filter(ImageFilter.GaussianBlur(radius=4 * scale))
        img.alpha_composite(pg)
        draw.rounded_rectangle(p_box, radius=rad, fill=PORCELAIN_FILL, outline=PORCELAIN_OUTLINE, width=max(1, int(1.2 * scale)))
    elif data["view"] == "three_quarter":
        # Front winglet pod on left: x: 12..58, y: 252..385
        fp_box = [int(12 * s + off_x), int(252 * s + off_y), int(58 * s + off_x), int(385 * s + off_y)]
        frad = int(22 * s)
        # Rear winglet pod on right: x: 212..258, y: 252..385
        rp_box = [int(212 * s + off_x), int(252 * s + off_y), int(258 * s + off_x), int(385 * s + off_y)]
        rrad = int(22 * s)
        
        for pbox, prad in [(rp_box, rrad), (fp_box, frad)]:
            pcx = (pbox[0] + pbox[2]) // 2
            pcy = pbox[3]
            pg = Image.new("RGBA", (canv_w, canv_h), (0, 0, 0, 0))
            ImageDraw.Draw(pg).ellipse([pcx - int(8*scale), pcy - int(3*scale), pcx + int(8*scale), pcy + int(6*scale)], fill=(0, 240, 255, 130))
            pg = pg.filter(ImageFilter.GaussianBlur(radius=4 * scale))
            img.alpha_composite(pg)
            draw.rounded_rectangle(pbox, radius=prad, fill=PORCELAIN_FILL, outline=PORCELAIN_OUTLINE, width=max(1, int(1.2 * scale)))
            
    # 5. Neck Socket (clean dark joint)
    for n in data["neck"]:
        pts = S(n)
        if len(pts) >= 3:
            draw.polygon(pts, fill=NECK_SOCKET, outline=NECK_SOCKET, width=1)
            
    # 6. Head Dome (Spotless Uniform White Porcelain)
    if len(data["head"]) >= 3:
        pts = S(data["head"])
        draw.polygon(pts, fill=PORCELAIN_FILL, outline=PORCELAIN_OUTLINE, width=max(1, int(1.2 * scale)))
        
    # 7. Visor (Obsidian Glass + Horizon Specular Highlight)
    for v in data["visor"]:
        pts = S(v)
        if len(pts) >= 3:
            draw.polygon(pts, fill=VISOR_GLASS, outline=VISOR_RIM, width=max(1, int(1.5 * scale)))
            vx_min = min(p[0] for p in pts)
            vx_max = max(p[0] for p in pts)
            vy_min = min(p[1] for p in pts)
            vw = vx_max - vx_min
            vh = max(p[1] for p in pts) - vy_min
            
            vl = Image.new("RGBA", (canv_w, canv_h), (0, 0, 0, 0))
            vld = ImageDraw.Draw(vl)
            vcx = (vx_min + vx_max) // 2
            vld.ellipse([vcx - int(vw * 0.45), vy_min + int(vh * 0.05), vcx + int(vw * 0.45), vy_min + int(vh * 0.40)], fill=(120, 140, 170, 45))
            vld.ellipse([vcx - int(vw * 0.30), vy_min + int(vh * 0.08), vcx + int(vw * 0.30), vy_min + int(vh * 0.25)], fill=(255, 255, 255, 45))
            vl = vl.filter(ImageFilter.GaussianBlur(radius=4 * scale))
            
            vmask = Image.new("L", (canv_w, canv_h), 0)
            ImageDraw.Draw(vmask).polygon(pts, fill=255)
            vl.putalpha(ImageChops.multiply(vl.split()[-1], vmask))
            img.alpha_composite(vl)
            
    # 8. Cyan Eyes (Emissive Crescents + 2-Stage Bloom)
    if data["eyes"]:
        wb = Image.new("RGBA", (canv_w, canv_h), (0, 0, 0, 0))
        mb = Image.new("RGBA", (canv_w, canv_h), (0, 0, 0, 0))
        core = Image.new("RGBA", (canv_w, canv_h), (0, 0, 0, 0))
        
        for e in data["eyes"]:
            pts = S(e)
            if len(pts) >= 3:
                ImageDraw.Draw(wb).polygon(pts, fill=(0, 240, 255, 140))
                ImageDraw.Draw(mb).polygon(pts, fill=(0, 240, 255, 220))
                ImageDraw.Draw(core).polygon(pts, fill=(0, 245, 255, 255))
                
        wb = wb.filter(ImageFilter.GaussianBlur(radius=8 * scale))
        mb = mb.filter(ImageFilter.GaussianBlur(radius=4 * scale))
        img.alpha_composite(wb)
        img.alpha_composite(mb)
        img.alpha_composite(core)
        
    # 9. Pods (For Front and Back where they are segmented)
    for p in data["pods"]:
        pts = S(p)
        if len(pts) >= 3:
            px = int(np.mean([pt[0] for pt in pts]))
            py = int(np.max([pt[1] for pt in pts]))
            pg = Image.new("RGBA", (canv_w, canv_h), (0, 0, 0, 0))
            ImageDraw.Draw(pg).ellipse([px - int(10*scale), py - int(3*scale), px + int(10*scale), py + int(6*scale)], fill=(0, 240, 255, 130))
            pg = pg.filter(ImageFilter.GaussianBlur(radius=4 * scale))
            img.alpha_composite(pg)
            draw.polygon(pts, fill=PORCELAIN_FILL, outline=PORCELAIN_OUTLINE, width=max(1, int(1.2 * scale)))

    # Antialiased Lanczos Downsample
    final_w = canv_w // scale
    final_h = canv_h // scale
    return img.resize((final_w, final_h), resample=Image.Resampling.LANCZOS)

def generate_all():
    print("🚀 Generating Complete Turnaround Suite...")
    
    # 1. Render the 4 Master Vector Figures
    views = ["front", "three_quarter", "profile", "back"]
    figs = {}
    for v in views:
        data = extract_view_geometry(v)
        figs[v] = render_master_figure(data, target_h=460, scale=4)
        print(f"  ✅ Rendered master {v}: size {figs[v].size}")
        
    SHEET_W = 1920
    SHEET_H = 820
    col_w = SHEET_W // 4
    guide_y_top = 180
    guide_y_eye = 265
    guide_y_neck = 360
    guide_y_torso = 550
    guide_y_feet = 645
    
    guides = [
        (guide_y_top, "SOMMET CASQUE", (52, 211, 153, 90)),
        (guide_y_eye, "HORIZON YEUX", (0, 240, 255, 90)),
        (guide_y_neck, "EMBOITEMENT COU", (148, 163, 184, 80)),
        (guide_y_torso, "BASE TORSE", (148, 163, 184, 80)),
        (guide_y_feet, "SUSTENTATION SOL", (0, 240, 255, 110))
    ]
    
    cols = [
        {"key": "front", "angle": "0 DEG", "name": "VUE DE FACE (FRONT)", "desc": "Visor 2 yeux cyan, 2 pods lateraux, 2 pieds V"},
        {"key": "three_quarter", "angle": "45 DEG", "name": "TROIS-QUARTS (3/4)", "desc": "Visor galbe oblique, perspective yeux et pods"},
        {"key": "profile", "angle": "90 DEG", "name": "PROFIL (SIDE)", "desc": "Arc facial convexe, 1 oeil profil, pod centre"},
        {"key": "back", "angle": "180 DEG", "name": "VUE DE DOS (BACK)", "desc": "Porcelaine pure complete (zero ecran/yeux)"}
    ]
    
    # --- A. MASTER VECTOR TURNAROUND SHEET ---
    sheet_vec = Image.new("RGBA", (SHEET_W, SHEET_H), COLOR_BG)
    draw_v = ImageDraw.Draw(sheet_vec)
    
    draw_v.rectangle([0, 0, SHEET_W, 90], fill=(15, 23, 42, 255))
    draw_v.line([(0, 90), (SHEET_W, 90)], fill=COLOR_BORDER, width=2)
    draw_v.text((40, 22), "AITUKO - PLANCHE DE TURNAROUND DU MODELE MASTER VECTORIEL (360 DEGRES)", fill=COLOR_CYAN)
    draw_v.text((40, 52), "Planche Officielle Reconstruite - 4 Vues Orthographiques Calibrees - Porcelaine Blanche Pure Sans Ombre et Zero Mains", fill=COLOR_MUTED)
    
    for gy, glabel, gcolor in guides:
        for gx in range(40, SHEET_W - 40, 16):
            draw_v.line([(gx, gy), (gx + 8, gy)], fill=gcolor, width=1)
        draw_v.text((SHEET_W - 170, gy - 12), glabel, fill=gcolor)
        
    for i, col in enumerate(cols):
        cx = i * col_w
        draw_v.rectangle([cx + 15, 110, cx + col_w - 15, SHEET_H - 25], fill=COLOR_CARD, outline=COLOR_BORDER, width=1)
        draw_v.rectangle([cx + 25, 120, cx + col_w - 25, 158], fill=(15, 23, 42, 230), outline=(0, 240, 255, 120) if i==0 else (52, 211, 153, 80))
        draw_v.text((cx + 38, 130), f"{col['angle']} - {col['name']}", fill=COLOR_CYAN if i==0 else COLOR_EMERALD)
        
        fig = figs[col["key"]]
        fw, fh = fig.size
        px = cx + (col_w - fw) // 2
        py = guide_y_top - 15
        sheet_vec.paste(fig, (px, py), fig)
        
        draw_v.rectangle([cx + 25, SHEET_H - 65, cx + col_w - 25, SHEET_H - 35], fill=(15, 23, 42, 200), outline=COLOR_BORDER)
        draw_v.text((cx + 35, SHEET_H - 55), col["desc"], fill=COLOR_MUTED)
        if i > 0:
            draw_v.line([(cx, 90), (cx, SHEET_H)], fill=COLOR_BORDER, width=1)
            
    out_vec_brain = os.path.join(BRAIN_DIR, "aituko_master_turnaround_sheet.png")
    sheet_vec.save(out_vec_brain, "PNG")
    sheet_vec.save(os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_master_turnaround_sheet.png"), "PNG")
    print(f"✅ Saved Master Vector Turnaround Sheet: {out_vec_brain}")
    
    # Also save to aituko_vector_turnaround_sheet.png to maintain existing links
    sheet_vec.save(os.path.join(BRAIN_DIR, "aituko_vector_turnaround_sheet.png"), "PNG")
    sheet_vec.save(os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_vector_turnaround_sheet.png"), "PNG")

    # --- B. STUDIO 3D REFERENCE TURNAROUND SHEET ---
    sheet_studio = Image.new("RGBA", (SHEET_W, SHEET_H), COLOR_BG)
    draw_s = ImageDraw.Draw(sheet_studio)
    
    draw_s.rectangle([0, 0, SHEET_W, 90], fill=(15, 23, 42, 255))
    draw_s.line([(0, 90), (SHEET_W, 90)], fill=COLOR_BORDER, width=2)
    draw_s.text((40, 22), "AITUKO - PLANCHE DE TURNAROUND DU MODELE STUDIO 3D DE REFERENCE (DETOURE)", fill=COLOR_EMERALD)
    draw_s.text((40, 52), "Rendu Studio CGI Officiel sans Fond Vert - Calibre a l'Echelle 1:1 pour Validation Geometrique", fill=COLOR_MUTED)
    
    for gy, glabel, gcolor in guides:
        for gx in range(40, SHEET_W - 40, 16):
            draw_s.line([(gx, gy), (gx + 8, gy)], fill=gcolor, width=1)
        draw_s.text((SHEET_W - 170, gy - 12), glabel, fill=gcolor)
        
    for i, col in enumerate(cols):
        cx = i * col_w
        draw_s.rectangle([cx + 15, 110, cx + col_w - 15, SHEET_H - 25], fill=COLOR_CARD, outline=COLOR_BORDER, width=1)
        draw_s.rectangle([cx + 25, 120, cx + col_w - 25, 158], fill=(15, 23, 42, 230), outline=(52, 211, 153, 100))
        draw_s.text((cx + 38, 130), f"{col['angle']} - {col['name']}", fill=COLOR_EMERALD)
        
        raw_fig = Image.open(f"scratch/turnaround_views/{col['key']}_clean.png").convert("RGBA")
        rfw, rfh = raw_fig.size
        sc = 460.0 / rfh
        target_w = int(rfw * sc)
        fig_scaled = raw_fig.resize((target_w, 460), resample=Image.Resampling.LANCZOS)
        
        sh = Image.new("RGBA", (target_w + 60, 500), (0, 0, 0, 0))
        sh_draw = ImageDraw.Draw(sh)
        sh_cx = (target_w + 60) // 2
        sh_draw.ellipse([sh_cx - 50, 475, sh_cx + 50, 495], fill=(0, 0, 0, 140))
        sh = sh.filter(ImageFilter.GaussianBlur(radius=6))
        sh.paste(fig_scaled, (30, 20), fig_scaled)
        
        px = cx + (col_w - sh.size[0]) // 2
        py = guide_y_top - 15
        sheet_studio.paste(sh, (px, py), sh)
        
        draw_s.rectangle([cx + 25, SHEET_H - 65, cx + col_w - 25, SHEET_H - 35], fill=(15, 23, 42, 200), outline=COLOR_BORDER)
        draw_s.text((cx + 35, SHEET_H - 55), col["desc"], fill=COLOR_MUTED)
        if i > 0:
            draw_s.line([(cx, 90), (cx, SHEET_H)], fill=COLOR_BORDER, width=1)
            
    out_studio_brain = os.path.join(BRAIN_DIR, "aituko_studio_turnaround_sheet.png")
    sheet_studio.save(out_studio_brain, "PNG")
    sheet_studio.save(os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_studio_turnaround_sheet.png"), "PNG")
    print(f"✅ Saved Studio 3D Reference Turnaround Sheet: {out_studio_brain}")
    
    # --- C. DUAL COMPARATIVE MASTER BOARD ---
    DUAL_H = 1600
    dual = Image.new("RGBA", (SHEET_W, DUAL_H), COLOR_BG)
    dual.paste(sheet_studio, (0, 0))
    dual.paste(sheet_vec, (0, 780))
    out_dual_brain = os.path.join(BRAIN_DIR, "aituko_turnaround_master_board.png")
    dual.save(out_dual_brain, "PNG")
    dual.save(os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_turnaround_master_board.png"), "PNG")
    print(f"✅ Saved Dual Comparative Master Board: {out_dual_brain}")

if __name__ == "__main__":
    generate_all()
