#!/usr/bin/env python3
"""
Industrial Standard Volumetric Porcelain Shader Test.
Replaces artificial 'cylindrical bars' and 'rectangles' with true 3D spherical/capsular
light diffusion gradients.
Samples exact ceramic tones from reference:
- Key Light Highlight: #FFFDF8 / #FAF5EB
- Main Ceramic Body: #E5DFC4 / #D8D0BE (warm robotic porcelain with solid contrast on white!)
- Curvature Ambient Shadow: #C0B7A4 / #B0A792
- Visor: #0B0E14
- Eyes: #00F0FF with multi-stage glow
Tests rendering on 3 backgrounds:
1. White background (#FFFFFF) - to verify crisp contrast!
2. Dark studio background (#0B0F17) - to verify gloss and bloom!
3. Studio chroma green background (#00FF00) - to verify edge cleanliness and zero artifacts!
"""

import math
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.build_master_vector_aituko import extract_all_component_splines

def render_volumetric_ceramic_patch(W, H, pts_scaled, light_pos=(0.35, 0.25), contrast_boost=1.0):
    """
    Renders realistic 3D volumetric ceramic porcelain using continuous radial-cylindrical diffusion.
    Light is incident from light_pos (normalized 0..1 inside the bounding box).
    Produces smooth organic falloff without ANY artificial bars or hard rectangles.
    """
    pts_arr = np.array(pts_scaled)
    min_x, max_x = np.min(pts_arr[:, 0]), np.max(pts_arr[:, 0])
    min_y, max_y = np.min(pts_arr[:, 1]), np.max(pts_arr[:, 1])
    pw = max(1, max_x - min_x)
    ph = max(1, max_y - min_y)
    
    y_idx, x_idx = np.mgrid[min_y:max_y+1, min_x:max_x+1]
    
    # Normalized coords inside component
    nx = (x_idx - min_x) / pw
    ny = (y_idx - min_y) / ph
    
    # 3D spherical / cylindrical surface normal estimation
    lx, ly = light_pos
    # Distance from light center
    dist_light = np.sqrt(((nx - lx) * 1.1)**2 + ((ny - ly) * 0.9)**2)
    dist_light = np.clip(dist_light, 0.0, 1.4)
    
    # Volumetric illumination term: smooth cosine falloff
    # 0.0 is specular highlight, 1.0 is deep curvature shadow
    t = np.clip(dist_light * 0.85, 0.0, 1.0)
    
    # Authentic Warm Ceramic Porcelain Palette:
    # Highlight: #FFFDF8 (255, 253, 248)
    # Midtone 1: #FAF5EB (250, 245, 235)
    # Midtone 2: #E8E0D0 (232, 224, 208) - Warm ceramic
    # Shadow:    #C2B8A4 (194, 184, 164) - Gives clear contrast against white background!
    r_map = 252 - (t * 58).astype(np.uint8)
    g_map = 248 - (t * 64).astype(np.uint8)
    b_map = 242 - (t * 78).astype(np.uint8)
    a_map = np.full_like(r_map, 255)
    
    grad_arr = np.dstack([r_map, g_map, b_map, a_map])
    full_patch = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    full_patch.paste(Image.fromarray(grad_arr), (min_x, min_y))
    
    # Add subtle soft specular hotspot at the light incidence point
    spec_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sp_cx = int((min_x + lx * pw))
    sp_cy = int((min_y + ly * ph))
    sp_rx = int(pw * 0.18)
    sp_ry = int(ph * 0.14)
    ImageDraw.Draw(spec_layer).ellipse([sp_cx - sp_rx, sp_cy - sp_ry, sp_cx + sp_rx, sp_cy + sp_ry], fill=(255, 255, 255, 140))
    spec_layer = spec_layer.filter(ImageFilter.GaussianBlur(radius=max(2, int(pw * 0.08))))
    full_patch = Image.alpha_composite(full_patch, spec_layer)
    
    # Mask to component boundary
    mask = Image.new('L', (W, H), 0)
    ImageDraw.Draw(mask).polygon(pts_scaled, fill=255)
    full_patch.putalpha(ImageChops.multiply(full_patch.split()[-1], mask))
    
    # Subtle anti-aliased edge outline in warm shadow tone (#B8AE9E)
    outline_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(outline_layer).polygon(pts_scaled, fill=None, outline=(190, 180, 165, 255), width=max(1, int(W / 512 * 0.8)))
    full_patch = Image.alpha_composite(full_patch, outline_layer)
    
    return full_patch

def render_master_scene(bg_color=(11, 15, 23, 255), scale=4):
    W = 512 * scale
    H = 512 * scale
    splines, points_512 = extract_all_component_splines()
    
    def S(pts):
        return [(int(round(x * scale)), int(round(y * scale))) for x, y in pts]
    
    canvas = Image.new('RGBA', (W, H), bg_color)
    
    # 1. Ground Shadow
    sh_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(sh_layer)
    cx, cy = int(256 * scale), int(488 * scale)
    rx, ry = int(95 * scale), int(12 * scale)
    sh_draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(0, 0, 0, 160))
    sh_layer = sh_layer.filter(ImageFilter.GaussianBlur(radius=int(8 * scale)))
    canvas.alpha_composite(sh_layer)
    
    # 2. Landing Feet Pods
    for foot_name, fc_x in [("left_foot", 215.0), ("right_foot", 297.0)]:
        f_pts_s = S(points_512[foot_name])
        fc_scaled_x = int(fc_x * scale)
        fc_scaled_y = int(476.0 * scale)
        
        # Cyan Thruster Cushion
        tg_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        tg_draw = ImageDraw.Draw(tg_layer)
        tg_draw.ellipse([fc_scaled_x - int(16 * scale), fc_scaled_y - int(3 * scale),
                         fc_scaled_x + int(16 * scale), fc_scaled_y + int(8 * scale)],
                        fill=(0, 240, 255, 140))
        tg_layer = tg_layer.filter(ImageFilter.GaussianBlur(radius=int(5 * scale)))
        canvas.alpha_composite(tg_layer)
        
        # Volumetric porcelain foot
        lx = 0.40 if foot_name == "left_foot" else 0.60
        foot_patch = render_volumetric_ceramic_patch(W, H, f_pts_s, light_pos=(lx, 0.25))
        canvas.alpha_composite(foot_patch)
        
    # 3. Torso Capsule - Volumetric 3D Shading (NO BARS, NO CYLINDRICAL RECTANGLES)
    torso_pts_s = S(points_512["torso"])
    # Key light from top-left: lx=0.38, ly=0.30
    torso_patch = render_volumetric_ceramic_patch(W, H, torso_pts_s, light_pos=(0.38, 0.28))
    canvas.alpha_composite(torso_patch)
    
    # 4. Mechanical Neck Socket (Seamless dark collar, prevents ANY horizontal cut under chin)
    neck_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(neck_layer).ellipse([int(244 * scale), int(196 * scale), int(268 * scale), int(208 * scale)], fill=(24, 28, 38, 255))
    canvas.alpha_composite(neck_layer)
    
    # 5. Porcelain Head Dome & Obsidian Visor
    head_pts_s = S(points_512["head"])
    head_patch = render_volumetric_ceramic_patch(W, H, head_pts_s, light_pos=(0.42, 0.20))
    
    # Obsidian Visor Faceplate
    visor_pts_s = S(points_512["visor"])
    hp_draw = ImageDraw.Draw(head_patch)
    hp_draw.polygon(visor_pts_s, fill=(12, 14, 22, 255), outline=(26, 32, 44, 255), width=max(1, int(1.0 * scale)))
    
    # Visor Horizon Softbox Arc Reflection
    v_mask = Image.new('L', (W, H), 0)
    ImageDraw.Draw(v_mask).polygon(visor_pts_s, fill=255)
    
    v_refl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    vr_draw = ImageDraw.Draw(v_refl)
    vx_c = int(256.0 * scale)
    vy_c = int(76.0 * scale)
    vr_draw.ellipse([vx_c - int(70 * scale), vy_c - int(14 * scale),
                     vx_c + int(70 * scale), vy_c + int(32 * scale)], fill=(130, 150, 175, 55))
    vr_draw.ellipse([vx_c - int(48 * scale), vy_c - int(8 * scale),
                     vx_c + int(48 * scale), vy_c + int(14 * scale)], fill=(255, 255, 255, 75))
    v_refl = v_refl.filter(ImageFilter.GaussianBlur(radius=int(4 * scale)))
    v_refl.putalpha(ImageChops.multiply(v_refl.split()[-1], v_mask))
    head_patch.alpha_composite(v_refl)
    
    # Glowing Neon Cyan Eyes (^ ^)
    wb_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    mb_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    core_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    wb_draw = ImageDraw.Draw(wb_layer)
    mb_draw = ImageDraw.Draw(mb_layer)
    cb_draw = ImageDraw.Draw(core_layer)
    
    for eye_name in ["left_eye", "right_eye"]:
        eye_pts_s = S(points_512[eye_name])
        wb_draw.polygon(eye_pts_s, fill=(0, 240, 255, 140))
        mb_draw.polygon(eye_pts_s, fill=(0, 240, 255, 220))
        cb_draw.polygon(eye_pts_s, fill=(0, 245, 255, 255))
        
    wb_layer = wb_layer.filter(ImageFilter.GaussianBlur(radius=int(12 * scale)))
    mb_layer = mb_layer.filter(ImageFilter.GaussianBlur(radius=int(4.5 * scale)))
    
    head_patch.alpha_composite(wb_layer)
    head_patch.alpha_composite(mb_layer)
    head_patch.alpha_composite(core_layer)
    canvas.alpha_composite(head_patch)
    
    # 6. Floating Lateral Winglets (NO BARS, NO OBLIQUE STICKS!)
    pod_configs = [
        ("left_pod", 146.0, 382.0, 0.40),
        ("right_pod", 366.0, 382.0, 0.60)
    ]
    for pod_name, pc_x, pc_y, lx in pod_configs:
        pod_pts_s = S(points_512[pod_name])
        
        # Cyan thruster glow
        pt_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        pt_draw = ImageDraw.Draw(pt_layer)
        pc_scaled_x = int(pc_x * scale)
        pc_scaled_y = int(pc_y * scale)
        pt_draw.ellipse([pc_scaled_x - int(12 * scale), pc_scaled_y - int(3 * scale),
                         pc_scaled_x + int(12 * scale), pc_scaled_y + int(6 * scale)],
                        fill=(0, 240, 255, 140))
        pt_layer = pt_layer.filter(ImageFilter.GaussianBlur(radius=int(4 * scale)))
        canvas.alpha_composite(pt_layer)
        
        # Pure volumetric porcelain pod (smooth 3D falloff, ZERO STICKS)
        pod_patch = render_volumetric_ceramic_patch(W, H, pod_pts_s, light_pos=(lx, 0.30))
        canvas.alpha_composite(pod_patch)
        
    out = canvas.resize((512, 512), resample=Image.Resampling.LANCZOS)
    return out

if __name__ == "__main__":
    # Render on Dark Background
    im_dark = render_master_scene(bg_color=(11, 15, 23, 255))
    im_dark.save("/tmp/test_volumetric_dark.png")
    
    # Render on Pure White Background (#FFFFFF)
    im_white = render_master_scene(bg_color=(255, 255, 255, 255))
    im_white.save("/tmp/test_volumetric_white.png")
    
    # Render on Chroma Green (#00FF00)
    im_green = render_master_scene(bg_color=(0, 255, 0, 255))
    im_green.save("/tmp/test_volumetric_green.png")
    
    # Create 3-panel comparison test board (White, Dark, Green)
    board = Image.new('RGB', (1536, 512), (0, 0, 0))
    board.paste(im_white.convert('RGB'), (0, 0))
    board.paste(im_dark.convert('RGB'), (512, 0))
    board.paste(im_green.convert('RGB'), (1024, 0))
    board.save("/tmp/test_volumetric_board.png")
    print("Saved /tmp/test_volumetric_board.png")
