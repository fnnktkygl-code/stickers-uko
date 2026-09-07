#!/usr/bin/env python3
"""
Render high-fidelity PNG and animated GIF of the pure hands-free AItuko vector rig.
Uses 2x supersampling (1024x1024 downsampled to 512x512) for smooth antialiased curves.
Outputs:
- aituko_hands_free_master.png (512x512)
- aituko_hands_free_animated.gif (4.0s harmonic floating loop)
- aituko_hands_free_comparison.png (1024x512 comparison with 3D reference)
"""

import math
import os
import shutil
from PIL import Image, ImageDraw, ImageFilter

BRAIN_DIR = "/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68"
WORKSPACE_DIR = "/Users/richard/Developer/Stickers Uko"

def draw_rotated_rounded_rect(canvas, center, size, radius, angle_deg, fill_color, border_color=None, border_w=0):
    """Draws a rounded rect rotated around its center at 2x scale."""
    cx, cy = center
    w, h = size
    r = radius
    
    pad = int(max(w, h) * 1.6)
    patch = Image.new('RGBA', (pad, pad), (0, 0, 0, 0))
    pd = ImageDraw.Draw(patch)
    
    bx = (pad - w) // 2
    by = (pad - h) // 2
    pd.rounded_rectangle([bx, by, bx + w, by + h], radius=r, fill=fill_color, outline=border_color, width=border_w)
    
    rotated = patch.rotate(angle_deg, resample=Image.Resampling.BICUBIC, center=(pad // 2, pad // 2))
    
    px = int(cx - pad // 2)
    py = int(cy - pad // 2)
    canvas.alpha_composite(rotated, (px, py))

def render_aituko_frame(scale=2, y_float=0, head_pitch=0, lpod_offset=(0,0), lpod_rot=-9, 
                        rpod_offset=(0,0), rpod_rot=9, blink_factor=1.0, shadow_scale=1.0, shadow_opacity=0.75):
    """
    Renders one full frame of AItuko hands-free vector rig at 2x scale.
    """
    W = 512 * scale
    H = 512 * scale
    img = Image.new('RGBA', (W, H), (11, 15, 23, 255))

    # 1. Soft Ground Shadow
    sh_w = int(180 * scale * shadow_scale)
    sh_h = int(28 * scale * shadow_scale)
    sh_cx = int(256 * scale)
    sh_cy = int(468 * scale)
    
    sh_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(sh_layer)
    alpha = int(255 * 0.45 * shadow_opacity)
    sh_draw.ellipse([sh_cx - sh_w // 2, sh_cy - sh_h // 2, sh_cx + sh_w // 2, sh_cy + sh_h // 2], fill=(15, 23, 42, alpha))
    sh_layer = sh_layer.filter(ImageFilter.GaussianBlur(radius=8 * scale))
    img.alpha_composite(sh_layer)

    dy = int(y_float * scale)

    # 2. Foot Pods
    for is_right in [False, True]:
        fx = 284 if is_right else 228
        fy = 412
        f_rot = 10 if is_right else -10
        
        # Thruster glow
        tg_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        tg_draw = ImageDraw.Draw(tg_layer)
        tg_cx = int(fx * scale)
        tg_cy = int((fy + 20 + dy/scale) * scale)
        tg_draw.ellipse([tg_cx - int(14 * scale), tg_cy - int(5 * scale), tg_cx + int(14 * scale), tg_cy + int(5 * scale)], fill=(0, 240, 255, 140))
        tg_layer = tg_layer.filter(ImageFilter.GaussianBlur(radius=4 * scale))
        img.alpha_composite(tg_layer)
        
        # Foot body: base rim + porcelain
        draw_rotated_rounded_rect(img, (fx * scale, (fy + dy/scale) * scale), (38 * scale, 46 * scale), 19 * scale, f_rot, (203, 213, 225, 255))
        draw_rotated_rounded_rect(img, (fx * scale, (fy + dy/scale) * scale), (34 * scale, 44 * scale), 17 * scale, f_rot, (248, 250, 252, 255))
        # Specular gloss
        draw_rotated_rounded_rect(img, ((fx - 2) * scale, (fy - 10 + dy/scale) * scale), (18 * scale, 8 * scale), 4 * scale, f_rot, (255, 255, 255, 210))

    # 3. Slender Neck
    nx = 256 * scale
    ny = int((193 * scale) + dy)
    nw = 36 * scale
    nh = 22 * scale
    draw_rotated_rounded_rect(img, (nx, ny), (nw, nh), 10 * scale, 0, (203, 213, 225, 255))
    draw_rotated_rounded_rect(img, (nx, ny), (32 * scale, 20 * scale), 9 * scale, 0, (241, 245, 249, 255))
    n_draw = ImageDraw.Draw(img)
    n_draw.ellipse([nx - 16 * scale, ny - 10 * scale, nx + 16 * scale, ny - 4 * scale], fill=(15, 23, 42, 65))

    # 4. Torso Capsule
    tx = 256 * scale
    ty = int((298 * scale) + dy)
    tw = 124 * scale
    th = 176 * scale
    draw_rotated_rounded_rect(img, (tx, ty), (tw + 4 * scale, th + 4 * scale), 64 * scale, 0, (203, 213, 225, 255))
    draw_rotated_rounded_rect(img, (tx, ty), (tw, th), 62 * scale, 0, (248, 250, 252, 255))
    
    # Torso left diffuse shade
    draw_rotated_rounded_rect(img, (tx - 38 * scale, ty), (38 * scale, 152 * scale), 19 * scale, 0, (226, 232, 240, 120))
    # Torso right specular streak
    draw_rotated_rounded_rect(img, (tx + 44 * scale, ty), (12 * scale, 124 * scale), 6 * scale, 0, (255, 255, 255, 220))
    # Torso shoulder soft highlight
    t_draw = ImageDraw.Draw(img)
    t_draw.ellipse([tx - 36 * scale, ty - 76 * scale, tx + 36 * scale, ty - 60 * scale], fill=(255, 255, 255, 150))
    t_draw.ellipse([tx - 30 * scale, ty - 92 * scale, tx + 30 * scale, ty - 80 * scale], fill=(15, 23, 42, 60))

    # 5. Porcelain Head Dome
    hx = 256 * scale
    hy = int((126 * scale) + dy)
    hw = 236 * scale
    hh = 164 * scale
    
    head_patch = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    hp_draw = ImageDraw.Draw(head_patch)
    
    # Outer base rim
    hp_draw.rounded_rectangle([hx - hw//2 - 2*scale, hy - hh//2 - 2*scale, hx + hw//2 + 2*scale, hy + hh//2 + 2*scale], radius=74*scale, fill=(203, 213, 225, 255))
    # Main porcelain head
    hp_draw.rounded_rectangle([hx - hw//2, hy - hh//2, hx + hw//2, hy + hh//2], radius=72*scale, fill=(248, 250, 252, 255))
    # Crown specular reflection
    hp_draw.ellipse([hx - 70*scale, hy - 76*scale, hx + 40*scale, hy - 52*scale], fill=(255, 255, 255, 235))
    # Temple right gloss
    hp_draw.ellipse([hx + 82*scale, hy - 48*scale, hx + 98*scale, hy - 4*scale], fill=(255, 255, 255, 160))
    # Cheek left diffuse shade
    hp_draw.ellipse([hx - 106*scale, hy - 20*scale, hx - 82*scale, hy + 32*scale], fill=(226, 232, 240, 100))
    # Chin rim
    hp_draw.ellipse([hx - 46*scale, hy + 72*scale, hx + 46*scale, hy + 84*scale], fill=(203, 213, 225, 120))

    # Dark Visor Faceplate
    vw = 188 * scale
    vh = 126 * scale
    hp_draw.rounded_rectangle([hx - vw//2 - 2*scale, hy - vh//2 - 2*scale, hx + vw//2 + 2*scale, hy + vh//2 + 2*scale], radius=58*scale, fill=(9, 10, 15, 255))
    hp_draw.rounded_rectangle([hx - vw//2, hy - vh//2, hx + vw//2, hy + vh//2], radius=56*scale, fill=(16, 18, 26, 255), outline=(31, 36, 51, 255), width=int(1.5*scale))
    hp_draw.ellipse([hx - 66*scale, hy - 58*scale, hx + 66*scale, hy - 24*scale], fill=(100, 116, 139, 70))
    hp_draw.ellipse([hx - 42*scale, hy - 53*scale, hx + 42*scale, hy - 41*scale], fill=(255, 255, 255, 50))

    # Cyan Neon Arch Eyes (^ ^)
    eye_bloom_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    eb_draw = ImageDraw.Draw(eye_bloom_layer)
    eye_core_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ec_draw = ImageDraw.Draw(eye_core_layer)

    for is_right in [False, True]:
        ecx = (296 if is_right else 212) * scale
        ecy = hy + int(2 * scale)
        ew = int(18 * scale)
        eh = max(2, int(15 * scale * blink_factor))
        
        pts = []
        for deg in range(180, 361, 10):
            rad = math.radians(deg)
            px = ecx + ew * math.cos(rad)
            py = ecy + eh * math.sin(rad)
            pts.append((px, py))
        
        if blink_factor > 0.15:
            eb_draw.line(pts, fill=(0, 240, 255, 180), width=int(16 * scale), joint='curve')
            ec_draw.line(pts, fill=(0, 240, 255, 255), width=int(8.5 * scale), joint='curve')
            ec_draw.line(pts, fill=(224, 247, 255, 255), width=int(3.2 * scale), joint='curve')
        else:
            slit_pts = [(ecx - ew, ecy), (ecx + ew, ecy)]
            eb_draw.line(slit_pts, fill=(0, 240, 255, 180), width=int(8 * scale))
            ec_draw.line(slit_pts, fill=(224, 247, 255, 255), width=int(3.2 * scale))

    eye_bloom_layer = eye_bloom_layer.filter(ImageFilter.GaussianBlur(radius=6 * scale))
    head_patch.alpha_composite(eye_bloom_layer)
    head_patch.alpha_composite(eye_core_layer)

    if abs(head_pitch) > 0.05:
        head_patch = head_patch.rotate(head_pitch, resample=Image.Resampling.BICUBIC, center=(hx, hy))
    img.alpha_composite(head_patch)

    # 6. Lateral Pods (Winglets/Thrusters — STRICTLY NO HANDS)
    for is_right in [False, True]:
        lx = (374 if is_right else 138) + (rpod_offset[0] if is_right else lpod_offset[0])
        ly = 298 + (dy / scale) + (rpod_offset[1] if is_right else lpod_offset[1])
        l_rot = rpod_rot if is_right else lpod_rot
        
        # Thruster bottom glow
        lg_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        lg_draw = ImageDraw.Draw(lg_layer)
        rad = math.radians(l_rot)
        bot_dx = -math.sin(rad) * 56 * scale
        bot_dy = math.cos(rad) * 56 * scale
        bg_cx = int(lx * scale + bot_dx)
        bg_cy = int(ly * scale + bot_dy)
        lg_draw.ellipse([bg_cx - int(10 * scale), bg_cy - int(4 * scale), bg_cx + int(10 * scale), bg_cy + int(4 * scale)], fill=(0, 240, 255, 160))
        lg_layer = lg_layer.filter(ImageFilter.GaussianBlur(radius=5 * scale))
        img.alpha_composite(lg_layer)
        
        # Winglet pod body
        draw_rotated_rounded_rect(img, (lx * scale, ly * scale), (38 * scale, 112 * scale), 19 * scale, l_rot, (203, 213, 225, 255))
        draw_rotated_rounded_rect(img, (lx * scale, ly * scale), (34 * scale, 108 * scale), 17 * scale, l_rot, (248, 250, 252, 255))
        
        # Specular streak
        streak_offset_x = 8 if is_right else -8
        draw_rotated_rounded_rect(img, ((lx + streak_offset_x) * scale, ly * scale), (6 * scale, 74 * scale), 3 * scale, l_rot, (255, 255, 255, 210))
        
        # Inner flank shade
        shade_offset_x = -9 if is_right else 9
        draw_rotated_rounded_rect(img, ((lx + shade_offset_x) * scale, ly * scale), (9 * scale, 80 * scale), 4.5 * scale, l_rot, (203, 213, 225, 90))

    final_img = img.resize((512, 512), resample=Image.Resampling.LANCZOS)
    return final_img

def build_all_renders():
    print("🎨 Generating AItuko hands-free master visual renders...")
    
    # 1. Master High-Resolution Static Image
    master_img = render_aituko_frame(scale=2, y_float=0, head_pitch=0, lpod_rot=-9, rpod_rot=9, blink_factor=1.0)
    master_path = os.path.join(BRAIN_DIR, "aituko_hands_free_master.png")
    master_img.save(master_path, "PNG")
    print(f"  ✅ Saved {master_path} ({os.path.getsize(master_path)/1024:.1f} KB)")
    
    ws_master_path = os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_hands_free_master.png")
    master_img.save(ws_master_path, "PNG")

    # 2. Side-by-Side Comparison Image (1024x512)
    ref_3d_path = os.path.join(BRAIN_DIR, "aituko_3d_master_crop_512.png")
    if os.path.exists(ref_3d_path):
        ref_img = Image.open(ref_3d_path).convert("RGBA").resize((512, 512), resample=Image.Resampling.LANCZOS)
        sbs = Image.new("RGBA", (1024, 512), (11, 15, 23, 255))
        sbs.paste(ref_img, (0, 0))
        sbs.paste(master_img, (512, 0))
        
        sbs_draw = ImageDraw.Draw(sbs)
        sbs_draw.rectangle([16, 16, 320, 48], fill=(19, 26, 38, 220), outline=(34, 47, 68, 255))
        sbs_draw.text((28, 24), "MODÈLE 3D RÉFÉRENCE (STUDIO)", fill=(0, 240, 255, 255))
        
        sbs_draw.rectangle([528, 16, 880, 48], fill=(19, 26, 38, 220), outline=(16, 185, 129, 255))
        sbs_draw.text((540, 24), "RIG VECTORIEL PUR (100% SANS MAINS)", fill=(52, 211, 153, 255))
        
        sbs_draw.line([(512, 0), (512, 512)], fill=(34, 47, 68, 255), width=2)
        
        sbs_path = os.path.join(BRAIN_DIR, "aituko_hands_free_comparison.png")
        sbs.save(sbs_path, "PNG")
        print(f"  ✅ Saved {sbs_path} ({os.path.getsize(sbs_path)/1024:.1f} KB)")

    # 3. Animated GIF (24 frames, 4.0s seamless harmonic loop)
    print("🎬 Generating 24-frame seamless animated GIF (4.0s @ 6fps)...")
    frames = []
    num_frames = 24
    for i in range(num_frames):
        t = i / num_frames
        sin_t = math.sin(t * 2 * math.pi)
        
        y_float = -14 * sin_t
        head_pitch = 1.8 * math.sin((t - 0.08) * 2 * math.pi)
        pod_flare = 4 * sin_t
        pod_tilt = 3 * sin_t
        shadow_scale = 1.0 - 0.15 * sin_t
        shadow_opacity = 0.75 - 0.2 * sin_t
        
        blink = 1.0
        if i == 18:
            blink = 0.08
        elif i == 19:
            blink = 1.0
        elif i == 20:
            blink = 0.15
        elif i == 21:
            blink = 1.0
            
        fr = render_aituko_frame(
            scale=2,
            y_float=y_float,
            head_pitch=head_pitch,
            lpod_offset=(-pod_flare, 0),
            lpod_rot=-9 - pod_tilt,
            rpod_offset=(pod_flare, 0),
            rpod_rot=9 + pod_tilt,
            blink_factor=blink,
            shadow_scale=shadow_scale,
            shadow_opacity=shadow_opacity
        )
        frames.append(fr.convert("P", palette=Image.Palette.ADAPTIVE))

    gif_path = os.path.join(BRAIN_DIR, "aituko_hands_free_animated.gif")
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=166, # 166ms * 24 = ~4.0s
        loop=0,
        optimize=True
    )
    print(f"  ✅ Saved {gif_path} ({os.path.getsize(gif_path)/1024:.1f} KB)")
    
    ws_gif_path = os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_hands_free_animated.gif")
    shutil.copyfile(gif_path, ws_gif_path)

if __name__ == "__main__":
    build_all_renders()
