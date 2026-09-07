#!/usr/bin/env python3
"""
Build Flawless 4-View Turnaround Model Sheet for AItuko.
Constructs both:
1. aituko_vector_turnaround_sheet.png (Our Vector Reconstructed Model across 4 angles)
2. aituko_studio_turnaround_sheet.png (Studio 3D Reference across 4 angles on dark backdrop)
3. aituko_vector_turnaround.svg (Standalone 4-view pure vector SVG)
"""

import os
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

BRAIN_DIR = "/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68"
WORKSPACE_DIR = "/Users/richard/Developer/Stickers Uko"

# Colors
COLOR_BG = (11, 15, 23, 255)
COLOR_CARD = (17, 24, 39, 230)
COLOR_CARD_BORDER = (31, 41, 55, 220)
COLOR_CYAN = (0, 240, 255, 255)
COLOR_EMERALD = (52, 211, 153, 255)
COLOR_WHITE = (255, 255, 255, 255)
COLOR_MUTED = (148, 163, 184, 255)
COLOR_LABEL = (203, 213, 225, 255)

PORCELAIN_FILL = (255, 255, 255, 255)
PORCELAIN_OUTLINE = (210, 218, 228, 255)
VISOR_GLASS = (12, 14, 20, 255)
VISOR_RIM = (28, 33, 46, 255)
NECK_SOCKET = (26, 32, 44, 255)

def render_vector_view(view_name, scale=4):
    """
    Renders our vector model for a specific view (front, three_quarter, profile, back)
    with 100% spotless uniform porcelain, crisp outlines, obsidian visor, and glowing cyan eyes.
    """
    img_path = f"scratch/turnaround_views/{view_name}_clean.png"
    rgba = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    if rgba is None:
        raise FileNotFoundError(f"Cannot load {img_path}")
        
    h, w, _ = rgba.shape
    alpha = rgba[:, :, 3]
    bgr = rgba[:, :, :3]
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    
    char_mask = (alpha > 80).astype(np.uint8) * 255
    
    # 1. Cyan Eyes
    cyan_mask = (hsv[:, :, 0] >= 75) & (hsv[:, :, 0] <= 115) & (hsv[:, :, 1] >= 60) & (hsv[:, :, 2] >= 75)
    ec, _ = cv2.findContours(cyan_mask.astype(np.uint8)*255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    eyes = sorted([c for c in ec if cv2.contourArea(c) > 15], key=lambda c: cv2.boundingRect(c)[0])
    
    # 2. Visor (if not back)
    visor = []
    if view_name != "back":
        head_crop = np.zeros_like(char_mask)
        head_crop[:175, :] = char_mask[:175, :]
        v_cand = (head_crop > 0) & (gray < 85)
        v_mask = cv2.morphologyEx(v_cand.astype(np.uint8)*255, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
        vc, _ = cv2.findContours(v_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        visor = [c for c in vc if cv2.contourArea(c) > 500]
        
    # 3. Head Dome (y < 196)
    head_mask = np.zeros_like(char_mask)
    head_mask[:196, :] = char_mask[:196, :]
    head_mask = cv2.morphologyEx(head_mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)))
    hc, _ = cv2.findContours(head_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    head = [c for c in hc if cv2.contourArea(c) > 3000]
    
    # 4. Neck Socket
    neck_mask = np.zeros_like(char_mask)
    neck_mask[188:206, :] = (char_mask[188:206, :] > 0) & (gray[188:206, :] < 140)
    neck_c, _ = cv2.findContours(neck_mask.astype(np.uint8)*255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    neck = [c for c in neck_c if cv2.contourArea(c) > 40]
    
    # 5. Feet (y > 415)
    feet_mask = np.zeros_like(char_mask)
    feet_mask[415:, :] = char_mask[415:, :]
    fc, _ = cv2.findContours(feet_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    feet = sorted([c for c in fc if cv2.contourArea(c) > 200], key=lambda c: cv2.boundingRect(c)[0])
    
    # 6. Body & Pods (y 196..415)
    body_mask = np.zeros_like(char_mask)
    body_mask[196:415, :] = char_mask[196:415, :]
    
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(body_mask)
    torso_cnts = []
    pods_cnts = []
    
    if num_labels > 2:
        comps = []
        for i in range(1, num_labels):
            if stats[i, cv2.CC_STAT_AREA] > 300:
                comps.append((stats[i, cv2.CC_STAT_AREA], i))
        comps.sort(reverse=True)
        if comps:
            torso_label = comps[0][1]
            t_mask = (labels == torso_label).astype(np.uint8)*255
            tc, _ = cv2.findContours(t_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            torso_cnts = [c for c in tc if cv2.contourArea(c) > 1000]
            for _, lab in comps[1:]:
                p_mask = (labels == lab).astype(np.uint8)*255
                pc, _ = cv2.findContours(p_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                pods_cnts.extend([c for c in pc if cv2.contourArea(c) > 300])
    else:
        tc, _ = cv2.findContours(body_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        torso_cnts = [c for c in tc if cv2.contourArea(c) > 1000]
        
    # Profile & 3/4 pod extraction if not separated by alpha
    if view_name == "profile" and len(pods_cnts) == 0:
        # Profile side pod is around x: 94..157, y: 250..378
        pod_mask = np.zeros_like(char_mask)
        pod_mask[250:378, 94:157] = 255
        pod_mask = (pod_mask > 0) & (char_mask > 0)
        pc, _ = cv2.findContours(pod_mask.astype(np.uint8)*255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        pods_cnts = [c for c in pc if cv2.contourArea(c) > 2000]
    elif view_name == "three_quarter" and len(pods_cnts) == 0:
        # Front pod around x: 10..60, y: 245..375
        pod_mask = np.zeros_like(char_mask)
        pod_mask[245:375, 10:60] = 255
        pod_mask = (pod_mask > 0) & (char_mask > 0)
        pc, _ = cv2.findContours(pod_mask.astype(np.uint8)*255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        pods_cnts = [c for c in pc if cv2.contourArea(c) > 1500]

    # --- Render to Canvas ---
    canv_w = w * scale
    canv_h = h * scale + 40 * scale
    out = Image.new("RGBA", (canv_w, canv_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(out)
    
    def T(cnt):
        approx = cv2.approxPolyDP(cnt, 0.7, True)
        return [(int(p[0][0] * scale), int(p[0][1] * scale)) for p in approx]

    # 1. Soft Ambient Ground Shadow
    sh_layer = Image.new("RGBA", (canv_w, canv_h), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(sh_layer)
    cx = canv_w // 2
    cy = int(482 * scale)
    rx = int(w * 0.35 * scale)
    ry = int(12 * scale)
    sh_draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(0, 0, 0, 150))
    sh_layer = sh_layer.filter(ImageFilter.GaussianBlur(radius=6 * scale))
    out.alpha_composite(sh_layer)
    
    # 2. Feet Landing Pods (Spotless White + Bottom Cyan Glow)
    for f in feet:
        pts = T(f)
        if len(pts) >= 3:
            fx = int(np.mean([p[0] for p in pts]))
            fy = int(np.max([p[1] for p in pts]))
            # Thruster glow
            fg = Image.new("RGBA", (canv_w, canv_h), (0, 0, 0, 0))
            ImageDraw.Draw(fg).ellipse([fx - int(14*scale), fy - int(3*scale), fx + int(14*scale), fy + int(6*scale)], fill=(0, 240, 255, 140))
            fg = fg.filter(ImageFilter.GaussianBlur(radius=4 * scale))
            out.alpha_composite(fg)
            # Porcelain shape
            draw.polygon(pts, fill=PORCELAIN_FILL, outline=PORCELAIN_OUTLINE, width=max(1, int(1.2 * scale)))
            
    # 3. Torso Capsule (Spotless Uniform White Porcelain - ZERO SMUDGES)
    for t in torso_cnts:
        pts = T(t)
        if len(pts) >= 3:
            draw.polygon(pts, fill=PORCELAIN_FILL, outline=PORCELAIN_OUTLINE, width=max(1, int(1.2 * scale)))
            
    # 4. Neck Socket
    for n in neck:
        pts = T(n)
        if len(pts) >= 3:
            draw.polygon(pts, fill=NECK_SOCKET, outline=NECK_SOCKET, width=1)
            
    # 5. Head Dome (Spotless Uniform White Porcelain)
    for hd in head:
        pts = T(hd)
        if len(pts) >= 3:
            draw.polygon(pts, fill=PORCELAIN_FILL, outline=PORCELAIN_OUTLINE, width=max(1, int(1.2 * scale)))
            
    # 6. Visor (Obsidian Glass + Horizon Specular Highlight)
    for v in visor:
        pts = T(v)
        if len(pts) >= 3:
            draw.polygon(pts, fill=VISOR_GLASS, outline=VISOR_RIM, width=max(1, int(1.5 * scale)))
            # Specular reflection arc on upper visor
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
            
            # Mask specular to visor
            vmask = Image.new("L", (canv_w, canv_h), 0)
            ImageDraw.Draw(vmask).polygon(pts, fill=255)
            vl.putalpha(ImageChops.multiply(vl.split()[-1], vmask))
            out.alpha_composite(vl)
            
    # 7. Cyan Eyes (Emissive Crescents + 2-Stage Bloom)
    if eyes:
        wb = Image.new("RGBA", (canv_w, canv_h), (0, 0, 0, 0))
        wbd = ImageDraw.Draw(wb)
        mb = Image.new("RGBA", (canv_w, canv_h), (0, 0, 0, 0))
        mbd = ImageDraw.Draw(mb)
        core = Image.new("RGBA", (canv_w, canv_h), (0, 0, 0, 0))
        cored = ImageDraw.Draw(core)
        
        for e in eyes:
            pts = T(e)
            if len(pts) >= 3:
                wbd.polygon(pts, fill=(0, 240, 255, 140))
                mbd.polygon(pts, fill=(0, 240, 255, 220))
                cored.polygon(pts, fill=(0, 245, 255, 255))
                
        wb = wb.filter(ImageFilter.GaussianBlur(radius=10 * scale))
        mb = mb.filter(ImageFilter.GaussianBlur(radius=4 * scale))
        out.alpha_composite(wb)
        out.alpha_composite(mb)
        out.alpha_composite(core)
        
    # 8. Floating Lateral Pods (Winglets - ZERO HANDS, Spotless Porcelain + Bottom Glow)
    for p in pods_cnts:
        pts = T(p)
        if len(pts) >= 3:
            px = int(np.mean([pt[0] for pt in pts]))
            py = int(np.max([pt[1] for pt in pts]))
            # Glow
            pg = Image.new("RGBA", (canv_w, canv_h), (0, 0, 0, 0))
            ImageDraw.Draw(pg).ellipse([px - int(10*scale), py - int(3*scale), px + int(10*scale), py + int(6*scale)], fill=(0, 240, 255, 130))
            pg = pg.filter(ImageFilter.GaussianBlur(radius=4 * scale))
            out.alpha_composite(pg)
            # Pod shape
            draw.polygon(pts, fill=PORCELAIN_FILL, outline=PORCELAIN_OUTLINE, width=max(1, int(1.2 * scale)))

    # Antialiased downsample
    final_w = canv_w // scale
    final_h = canv_h // scale
    return out.resize((final_w, final_h), resample=Image.Resampling.LANCZOS)

# Test rendering all 4
for v in ['front', 'three_quarter', 'profile', 'back']:
    res = render_vector_view(v, scale=3)
    res.save(f"scratch/turnaround_views/test_{v}_vector.png")
    print(f"Rendered test_{v}_vector.png: {res.size}")

