#!/usr/bin/env python3
import math
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.build_master_vector_aituko import extract_all_component_splines

def render_pure_porcelain_patch(W, H, pts_scaled, scale, outline_color=(232, 228, 222, 255), outline_w=1):
    """
    Renders an authentic, lustrous warm cream porcelain patch.
    Subtle ceramic shading: pure white #FFFFFF to light warm cream #F2EDE4.
    """
    pts_arr = np.array(pts_scaled)
    min_x, max_x = np.min(pts_arr[:, 0]), np.max(pts_arr[:, 0])
    min_y, max_y = np.min(pts_arr[:, 1]), np.max(pts_arr[:, 1])
    pw = max(1, max_x - min_x)
    ph = max(1, max_y - min_y)
    
    # 2D grid
    y_idx, x_idx = np.mgrid[min_y:max_y+1, min_x:max_x+1]
    
    # Light comes from top-left (approx 35 degrees)
    t_map = ((x_idx - min_x) / pw * 0.40 + (y_idx - min_y) / ph * 0.60).astype(np.float32)
    t_map = np.clip(t_map, 0.0, 1.0)
    
    # Smooth warm porcelain: from #FFFFFF (255, 255, 255) to warm ivory #FAF8F6 to soft cream #ECE7DE
    sub_r = 255 - (t_map * 13).astype(np.uint8)
    sub_g = 255 - (t_map * 16).astype(np.uint8)
    sub_b = 255 - (t_map * 22).astype(np.uint8)
    sub_a = np.full_like(sub_r, 255)
    
    sub_grad = np.dstack([sub_r, sub_g, sub_b, sub_a])
    full_grad = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    full_grad.paste(Image.fromarray(sub_grad), (min_x, min_y))
    
    mask = Image.new('L', (W, H), 0)
    ImageDraw.Draw(mask).polygon(pts_scaled, fill=255)
    full_grad.putalpha(ImageChops.multiply(full_grad.split()[-1], mask))
    
    # Delicate boundary outline
    if outline_w > 0:
        p_draw = ImageDraw.Draw(full_grad)
        p_draw.polygon(pts_scaled, fill=None, outline=outline_color, width=outline_w)
    
    return full_grad

def render_test_frame(scale=4, dark_bg=True):
    W = 512 * scale
    H = 512 * scale
    splines, points_512 = extract_all_component_splines()
    
    def S(pts):
        return [(int(round(x * scale)), int(round(y * scale))) for x, y in pts]
    
    bg = (11, 15, 23, 255) if dark_bg else (0, 0, 0, 0)
    canvas = Image.new('RGBA', (W, H), bg)
    
    # 1. Ground Contact Shadow
    sh_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(sh_layer)
    cx, cy = int(256 * scale), int(488 * scale)
    rx, ry = int(95 * scale), int(12 * scale)
    sh_draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(0, 0, 0, 140))
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
        
        # Porcelain Pod Body
        foot_patch = render_pure_porcelain_patch(W, H, f_pts_s, scale, outline_color=(230, 226, 220, 255), outline_w=max(1, int(0.8 * scale)))
        canvas.alpha_composite(foot_patch)
        
    # 3. Torso Capsule
    torso_pts_s = S(points_512["torso"])
    torso_patch = render_pure_porcelain_patch(W, H, torso_pts_s, scale, outline_color=(230, 226, 220, 255), outline_w=max(1, int(0.8 * scale)))
    
    # Soft vertical specular highlight streak down the front-right
    t_mask = Image.new('L', (W, H), 0)
    ImageDraw.Draw(t_mask).polygon(torso_pts_s, fill=255)
    
    t_spec = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    st_x = int(274.0 * scale)
    st_y = int(230.0 * scale)
    st_w = int(20.0 * scale)
    st_h = int(140.0 * scale)
    ImageDraw.Draw(t_spec).rounded_rectangle([st_x, st_y, st_x + st_w, st_y + st_h], radius=int(10 * scale), fill=(255, 255, 255, 100))
    t_spec = t_spec.filter(ImageFilter.GaussianBlur(radius=int(7 * scale)))
    t_spec.putalpha(ImageChops.multiply(t_spec.split()[-1], t_mask))
    torso_patch.alpha_composite(t_spec)
    
    canvas.alpha_composite(torso_patch)
    
    # 4. Small Neck Joint Collar
    neck_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(neck_layer).ellipse([int(246 * scale), int(196 * scale), int(266 * scale), int(206 * scale)], fill=(40, 48, 64, 255))
    canvas.alpha_composite(neck_layer)
    
    # 5. Porcelain Head Dome & Obsidian Visor
    head_pts_s = S(points_512["head"])
    head_patch = render_pure_porcelain_patch(W, H, head_pts_s, scale, outline_color=(230, 226, 220, 255), outline_w=max(1, int(0.8 * scale)))
    
    # Soft cranial dome highlight (curved specular reflection)
    h_mask = Image.new('L', (W, H), 0)
    ImageDraw.Draw(h_mask).polygon(head_pts_s, fill=255)
    
    h_spec = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    dom_x = int(248.0 * scale)
    dom_y = int(54.0 * scale)
    ImageDraw.Draw(h_spec).ellipse([dom_x - int(55 * scale), dom_y - int(12 * scale),
                                    dom_x + int(55 * scale), dom_y + int(12 * scale)], fill=(255, 255, 255, 180))
    h_spec = h_spec.filter(ImageFilter.GaussianBlur(radius=int(6 * scale)))
    h_spec.putalpha(ImageChops.multiply(h_spec.split()[-1], h_mask))
    head_patch.alpha_composite(h_spec)
    
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
                     vx_c + int(70 * scale), vy_c + int(32 * scale)], fill=(130, 150, 175, 45))
    vr_draw.ellipse([vx_c - int(48 * scale), vy_c - int(8 * scale),
                     vx_c + int(48 * scale), vy_c + int(14 * scale)], fill=(255, 255, 255, 65))
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
    
    # 6. Floating Lateral Winglets
    pod_configs = [
        ("left_pod", 146.0, 382.0, 126.0, -6.0),
        ("right_pod", 366.0, 382.0, 382.0, 6.0)
    ]
    for pod_name, pc_x, pc_y, sx_base, st_rot in pod_configs:
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
        
        # Porcelain Pod Body
        pod_patch = render_pure_porcelain_patch(W, H, pod_pts_s, scale, outline_color=(230, 226, 220, 255), outline_w=max(1, int(0.8 * scale)))
        
        # Soft specular highlight on pod
        p_mask = Image.new('L', (W, H), 0)
        ImageDraw.Draw(p_mask).polygon(pod_pts_s, fill=255)
        st_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        st_draw = ImageDraw.Draw(st_layer)
        sx_c = int(sx_base * scale)
        sy_c = int(278.0 * scale)
        st_draw.rounded_rectangle([sx_c, sy_c, sx_c + int(6 * scale), sy_c + int(70 * scale)], radius=int(3 * scale), fill=(255, 255, 255, 110))
        st_layer = st_layer.rotate(-st_rot, center=(sx_c, sy_c), resample=Image.Resampling.BILINEAR)
        st_layer = st_layer.filter(ImageFilter.GaussianBlur(radius=int(3 * scale)))
        st_layer.putalpha(ImageChops.multiply(st_layer.split()[-1], p_mask))
        pod_patch.alpha_composite(st_layer)
        
        canvas.alpha_composite(pod_patch)
        
    out = canvas.resize((512, 512), resample=Image.Resampling.LANCZOS)
    return out

if __name__ == "__main__":
    frame = render_test_frame(scale=4, dark_bg=True)
    frame.save("/tmp/clean_porcelain_v2.png")
    print("Saved /tmp/clean_porcelain_v2.png")
