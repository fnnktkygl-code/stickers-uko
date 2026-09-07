#!/usr/bin/env python3
"""
Test script to generate and visually verify a flawless frame of AItuko:
- Zero oblique lines on winglets (pure curvature shading, no <rect> streaks)
- Zero horizontal neck cut/gap (subtle mechanical neck collar joint)
- Zero fake cyan glow on feet and winglets (only eyes glow cyan)
- Natural 3D porcelain ceramic lighting with high contrast on white, dark, and green backgrounds.
"""

import math
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.build_master_vector_aituko import extract_all_component_splines, points_to_svg_cubic_spline

splines, points_512 = extract_all_component_splines()

def render_ceramic_component(W, H, pts_scaled, light_pos=(0.35, 0.25), is_winglet=False):
    """
    Renders realistic 3D volumetric ceramic porcelain:
    - Pure smooth 3D spherical/cylindrical falloff
    - Warm porcelain base: #FFFDF8 highlight, #F7F3EB midtone, #D6CEBE shadow rim
    - Crisp subtle outline in #B8AE9C to guarantee clear separation on white background
    - Smooth elongated specular highlight aligned with curvature, NOT a hard rectangle
    """
    pts_arr = np.array(pts_scaled)
    min_x, max_x = np.min(pts_arr[:, 0]), np.max(pts_arr[:, 0])
    min_y, max_y = np.min(pts_arr[:, 1]), np.max(pts_arr[:, 1])
    pw = max(1, max_x - min_x)
    ph = max(1, max_y - min_y)
    
    y_idx, x_idx = np.mgrid[min_y:max_y+1, min_x:max_x+1]
    nx = (x_idx - min_x) / pw
    ny = (y_idx - min_y) / ph
    
    lx, ly = light_pos
    dist_light = np.sqrt(((nx - lx) * 1.2)**2 + ((ny - ly) * 0.8)**2)
    dist_light = np.clip(dist_light, 0.0, 1.4)
    t = np.clip(dist_light * 0.75, 0.0, 1.0)
    
    # Clean warm porcelain tones:
    # Highlight: (255, 255, 255)
    # Midtone:   (246, 244, 240)
    # Shading:   (210, 204, 194) -> Gives crisp contrast against #FFFFFF!
    r_map = 255 - (t * 45).astype(np.uint8)
    g_map = 253 - (t * 49).astype(np.uint8)
    b_map = 249 - (t * 55).astype(np.uint8)
    a_map = np.full_like(r_map, 255)
    
    grad_arr = np.dstack([r_map, g_map, b_map, a_map])
    full_patch = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    full_patch.paste(Image.fromarray(grad_arr), (min_x, min_y))
    
    # Soft curvature specular sheen (elliptical, naturally blurred, NO HARD RECTANGLES)
    spec_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sp_cx = int(min_x + lx * pw)
    sp_cy = int(min_y + (ly + 0.1) * ph)
    if is_winglet:
        sp_rx = int(pw * 0.22)
        sp_ry = int(ph * 0.35)
    else:
        sp_rx = int(pw * 0.22)
        sp_ry = int(ph * 0.30)
    ImageDraw.Draw(spec_layer).ellipse([sp_cx - sp_rx, sp_cy - sp_ry, sp_cx + sp_rx, sp_cy + sp_ry], fill=(255, 255, 255, 120))
    spec_layer = spec_layer.filter(ImageFilter.GaussianBlur(radius=max(2, int(pw * 0.12))))
    full_patch = Image.alpha_composite(full_patch, spec_layer)
    
    # Mask to component boundary
    mask = Image.new('L', (W, H), 0)
    ImageDraw.Draw(mask).polygon(pts_scaled, fill=255)
    full_patch.putalpha(ImageChops.multiply(full_patch.split()[-1], mask))
    
    # Anti-aliased outer boundary rim for contrast against pure white backgrounds
    outline_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(outline_layer).polygon(pts_scaled, fill=None, outline=(185, 178, 168, 200), width=max(1, int(W / 512 * 0.9)))
    full_patch = Image.alpha_composite(full_patch, outline_layer)
    
    return full_patch

def render_flawless_frame(scale=4, bg_color=(11, 15, 23, 255), tilt_head=True):
    W = 512 * scale
    H = 512 * scale
    canvas = Image.new('RGBA', (W, H), bg_color)
    
    def S(pts):
        return [(int(round(x * scale)), int(round(y * scale))) for x, y in pts]

    # 1. Soft Ground Contact Shadow
    sh_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh_layer).ellipse([int(161 * scale), int(476 * scale), int(351 * scale), int(500 * scale)], fill=(0, 0, 0, 160))
    sh_layer = sh_layer.filter(ImageFilter.GaussianBlur(radius=int(8 * scale)))
    canvas.alpha_composite(sh_layer)
    
    # 2. Landing Feet Pods (NO CYAN GLOW!)
    for foot_name in ["left_foot", "right_foot"]:
        lx = 0.40 if foot_name == "left_foot" else 0.60
        foot_patch = render_ceramic_component(W, H, S(points_512[foot_name]), light_pos=(lx, 0.25))
        canvas.alpha_composite(foot_patch)
        
    # 3. Torso Capsule
    torso_patch = render_ceramic_component(W, H, S(points_512["torso"]), light_pos=(0.36, 0.28))
    canvas.alpha_composite(torso_patch)
    
    # 4. Mechanical Neck Collar Socket (Dark socket connecting torso and head - ZERO horizontal cut line!)
    neck_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(neck_layer).ellipse([int(242 * scale), int(196 * scale), int(270 * scale), int(210 * scale)], fill=(20, 24, 34, 255))
    canvas.alpha_composite(neck_layer)
    
    # 5. Porcelain Head Dome & Obsidian Visor
    # Simulate head tilt of -1.2 deg and -1.5px translation to test neck joint stability
    head_pivot = (256.0, 204.0)
    rad_h = math.radians(-1.2 if tilt_head else 0.0)
    cos_h = math.cos(rad_h)
    sin_h = math.sin(rad_h)
    dy_h = -1.5 if tilt_head else 0.0
    
    def transform_pt(x, y):
        dx = x - head_pivot[0]
        dy = y - head_pivot[1]
        rx = dx * cos_h - dy * sin_h + head_pivot[0]
        ry = dx * sin_h + dy * cos_h + head_pivot[1] + dy_h
        return (rx, ry)
        
    head_pts = [transform_pt(x, y) for x, y in points_512["head"]]
    head_patch = render_ceramic_component(W, H, S(head_pts), light_pos=(0.42, 0.20))
    
    # Obsidian Visor
    visor_pts = [transform_pt(x, y) for x, y in points_512["visor"]]
    visor_pts_s = S(visor_pts)
    hp_draw = ImageDraw.Draw(head_patch)
    hp_draw.polygon(visor_pts_s, fill=(12, 14, 22, 255), outline=(26, 32, 44, 255), width=max(1, int(1.0 * scale)))
    
    # Visor Horizon Softbox Arc Reflection
    v_mask = Image.new('L', (W, H), 0)
    ImageDraw.Draw(v_mask).polygon(visor_pts_s, fill=255)
    v_refl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    vr_draw = ImageDraw.Draw(v_refl)
    vx_c = int(256.0 * scale)
    vy_c = int((76.0 + dy_h) * scale)
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
        e_pts = [transform_pt(x, y) for x, y in points_512[eye_name]]
        eye_pts_s = S(e_pts)
        wb_draw.polygon(eye_pts_s, fill=(0, 240, 255, 140))
        mb_draw.polygon(eye_pts_s, fill=(0, 240, 255, 220))
        cb_draw.polygon(eye_pts_s, fill=(0, 245, 255, 255))
        
    wb_layer = wb_layer.filter(ImageFilter.GaussianBlur(radius=int(12 * scale)))
    mb_layer = mb_layer.filter(ImageFilter.GaussianBlur(radius=int(4.5 * scale)))
    
    head_patch.alpha_composite(wb_layer)
    head_patch.alpha_composite(mb_layer)
    head_patch.alpha_composite(core_layer)
    canvas.alpha_composite(head_patch)
    
    # 6. Floating Lateral Winglets (NO BARS, NO RECTANGLES, NO CYAN GLOW!)
    for pod_name, lx in [("left_pod", 0.38), ("right_pod", 0.62)]:
        pod_pts_s = S(points_512[pod_name])
        pod_patch = render_ceramic_component(W, H, pod_pts_s, light_pos=(lx, 0.28), is_winglet=True)
        canvas.alpha_composite(pod_patch)
        
    out = canvas.resize((512, 512), resample=Image.Resampling.LANCZOS)
    return out

def generate_clean_animated_svg(points_512):
    """
    Constructs 100% clean vector animated SVG:
    - Zero rectangular streaks
    - Dark neck collar socket
    - Zero fake cyan glow on pods and feet
    - High-contrast ceramic porcelain gradients
    """
    spline_head = points_to_svg_cubic_spline(points_512["head"])
    spline_visor = points_to_svg_cubic_spline(points_512["visor"])
    spline_left_eye = points_to_svg_cubic_spline(points_512["left_eye"])
    spline_right_eye = points_to_svg_cubic_spline(points_512["right_eye"])
    spline_torso = points_to_svg_cubic_spline(points_512["torso"])
    spline_left_pod = points_to_svg_cubic_spline(points_512["left_pod"])
    spline_right_pod = points_to_svg_cubic_spline(points_512["right_pod"])
    spline_left_foot = points_to_svg_cubic_spline(points_512["left_foot"])
    spline_right_foot = points_to_svg_cubic_spline(points_512["right_foot"])

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" style="background-color: #0B0F17; overflow: visible;">
  <defs>
    <!-- High-Contrast Authentic Porcelain Ceramic Gradient -->
    <linearGradient id="master_porcelainCream" x1="20%" y1="10%" x2="80%" y2="90%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="30%" stop-color="#F7F4EC" />
      <stop offset="70%" stop-color="#EAE3D5" />
      <stop offset="100%" stop-color="#D4CCC0" />
    </linearGradient>

    <!-- Torso Curvature Gradient -->
    <linearGradient id="master_torsoShading" x1="15%" y1="15%" x2="85%" y2="85%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="35%" stop-color="#F8F5EE" />
      <stop offset="75%" stop-color="#E8E1D2" />
      <stop offset="100%" stop-color="#CFC5B5" />
    </linearGradient>

    <!-- Winglet Curvature Gradients -->
    <linearGradient id="master_wingletLeft" x1="25%" y1="10%" x2="75%" y2="90%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="40%" stop-color="#F7F4EC" />
      <stop offset="85%" stop-color="#DCD4C5" />
      <stop offset="100%" stop-color="#C8BEAD" />
    </linearGradient>

    <linearGradient id="master_wingletRight" x1="75%" y1="10%" x2="25%" y2="90%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="40%" stop-color="#F7F4EC" />
      <stop offset="85%" stop-color="#DCD4C5" />
      <stop offset="100%" stop-color="#C8BEAD" />
    </linearGradient>

    <!-- Cranial Dome Specular Highlight (Curved radial ellipse) -->
    <radialGradient id="master_specularDome" cx="45%" cy="30%" r="55%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.95" />
      <stop offset="45%" stop-color="#FFFFFF" stop-opacity="0.45" />
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.0" />
    </radialGradient>

    <!-- Obsidian Glass Visor Faceplate -->
    <radialGradient id="master_visorGlass" cx="50%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#181B26" />
      <stop offset="60%" stop-color="#10131C" />
      <stop offset="100%" stop-color="#07080D" />
    </radialGradient>

    <!-- Visor Horizon Softbox Arc Reflection -->
    <linearGradient id="master_visorArcReflection" x1="20%" y1="0%" x2="80%" y2="100%">
      <stop offset="0%" stop-color="#94A3B8" stop-opacity="0.40" />
      <stop offset="40%" stop-color="#64748B" stop-opacity="0.20" />
      <stop offset="100%" stop-color="#334155" stop-opacity="0.0" />
    </linearGradient>

    <!-- Ground Contact Shadow Radial Gradient -->
    <radialGradient id="master_groundShadow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.65" />
      <stop offset="60%" stop-color="#000000" stop-opacity="0.25" />
      <stop offset="100%" stop-color="#000000" stop-opacity="0.0" />
    </radialGradient>

    <!-- Radiant Cyan Neon Bloom Filter -->
    <filter id="master_cyanGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur1" />
      <feGaussianBlur in="SourceGraphic" stdDeviation="9" result="blur2" />
      <feMerge>
        <feMergeNode in="blur2" />
        <feMergeNode in="blur1" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <style>
      @keyframes idleRootFloat {{
        0%, 100% {{ transform: translateY(0px); }}
        25% {{ transform: translateY(-12px); }}
        50% {{ transform: translateY(0px); }}
        75% {{ transform: translateY(12px); }}
      }}

      @keyframes idleTorsoBreathe {{
        0%, 50%, 100% {{ transform: scale(1.0, 1.0); }}
        25% {{ transform: scale(0.985, 1.015); }}
        75% {{ transform: scale(1.015, 0.985); }}
      }}

      @keyframes idleHeadTilt {{
        0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
        28% {{ transform: translateY(-1.5px) rotate(-1.2deg); }}
        53% {{ transform: translateY(0px) rotate(0deg); }}
        78% {{ transform: translateY(1.5px) rotate(1.2deg); }}
      }}

      @keyframes idleEyeBlink {{
        0%, 64% {{ transform: scaleY(1); }}
        65% {{ transform: scaleY(0.08); }}
        66.5% {{ transform: scaleY(1); }}
        67.5% {{ transform: scaleY(0.12); }}
        69%, 100% {{ transform: scaleY(1); }}
      }}

      @keyframes idleWingletLeft {{
        0%, 100% {{ transform: translate(0px, 0px) rotate(-9deg); }}
        28% {{ transform: translate(2.5px, -3px) rotate(-12deg); }}
        54% {{ transform: translate(0px, 0px) rotate(-9deg); }}
        78% {{ transform: translate(-3.5px, 3px) rotate(-6deg); }}
      }}

      @keyframes idleWingletRight {{
        0%, 100% {{ transform: translate(0px, 0px) rotate(9deg); }}
        28% {{ transform: translate(-2.5px, -3px) rotate(12deg); }}
        54% {{ transform: translate(0px, 0px) rotate(9deg); }}
        78% {{ transform: translate(3.5px, 3px) rotate(6deg); }}
      }}

      @keyframes idleFeetMotion {{
        0%, 100% {{ transform: translateY(0px); }}
        27% {{ transform: translateY(-1.5px); }}
        52% {{ transform: translateY(0px); }}
        77% {{ transform: translateY(1.5px); }}
      }}

      @keyframes idleShadowBreathe {{
        0%, 50%, 100% {{ transform: scale(1.0, 1.0); opacity: 0.60; }}
        25% {{ transform: scale(0.88, 0.88); opacity: 0.38; }}
        75% {{ transform: scale(1.12, 1.12); opacity: 0.82; }}
      }}

      .anim-shadow {{
        transform-box: view-box;
        transform-origin: 256px 488px;
        animation: idleShadowBreathe 4s cubic-bezier(0.45, 0.05, 0.55, 0.95) infinite;
      }}
      .anim-root {{
        animation: idleRootFloat 4s cubic-bezier(0.45, 0.05, 0.55, 0.95) infinite;
      }}
      .anim-torso {{
        transform-box: view-box;
        transform-origin: 256px 312px;
        animation: idleTorsoBreathe 4s ease-in-out infinite;
      }}
      .anim-head {{
        transform-box: view-box;
        transform-origin: 256px 204px;
        animation: idleHeadTilt 4s ease-in-out infinite;
      }}
      .anim-eyes {{
        transform-box: view-box;
        transform-origin: 256px 120px;
        animation: idleEyeBlink 4s ease-in-out infinite;
      }}
      .anim-winglet-l {{
        transform-box: view-box;
        transform-origin: 147px 321px;
        animation: idleWingletLeft 4s cubic-bezier(0.45, 0.05, 0.55, 0.95) infinite;
      }}
      .anim-winglet-r {{
        transform-box: view-box;
        transform-origin: 364px 321px;
        animation: idleWingletRight 4s cubic-bezier(0.45, 0.05, 0.55, 0.95) infinite;
      }}
      .anim-feet {{
        transform-box: view-box;
        transform-origin: 256px 448px;
        animation: idleFeetMotion 4s ease-in-out infinite;
      }}
    </style>
  </defs>

  <!-- 1. Soft Ground Contact Shadow -->
  <g class="anim-shadow">
    <ellipse cx="256" cy="488" rx="95" ry="12" fill="url(#master_groundShadow)" />
  </g>

  <!-- 2. Root Floating Group -->
  <g class="anim-root">

    <!-- 2a. Floating Landing Feet Pods (Strictly zero fake cyan glow) -->
    <g class="anim-feet">
      <path d="{spline_left_foot}" fill="url(#master_porcelainCream)" stroke="#C8BEAD" stroke-width="0.9" />
      <path d="{spline_right_foot}" fill="url(#master_porcelainCream)" stroke="#C8BEAD" stroke-width="0.9" />
    </g>

    <!-- 2b. Porcelain Torso Capsule -->
    <g class="anim-torso">
      <path d="{spline_torso}" fill="url(#master_torsoShading)" stroke="#C8BEAD" stroke-width="0.9" />
    </g>

    <!-- 2c. Mechanical Neck Collar Socket (Prevents ANY gap or cut line) -->
    <ellipse cx="256" cy="204" rx="14" ry="7" fill="#181B26" stroke="#0F1118" stroke-width="0.8" />

    <!-- 2d. Porcelain Head Dome & Obsidian Visor -->
    <g class="anim-head">
      <path d="{spline_head}" fill="url(#master_porcelainCream)" stroke="#C8BEAD" stroke-width="0.9" />
      <ellipse cx="248" cy="54" rx="55" ry="12" fill="url(#master_specularDome)" />

      <!-- Obsidian Visor Faceplate -->
      <g id="masterVisorGroup">
        <path d="{spline_visor}" fill="url(#master_visorGlass)" stroke="#1A202C" stroke-width="1.2" />
        <path d="M 180 94 C 205 72 250 68 296 74 C 274 78 222 84 196 104 Z" fill="url(#master_visorArcReflection)" />
        <ellipse cx="256" cy="74" rx="44" ry="5.5" fill="#FFFFFF" opacity="0.18" />

        <!-- Electric Cyan Neon Eyes (^ ^) -->
        <g class="anim-eyes" filter="url(#master_cyanGlow)">
          <path d="{spline_left_eye}" fill="#00F0FF" />
          <path d="{spline_right_eye}" fill="#00F0FF" />
        </g>
      </g>
    </g>

    <!-- 2e. Decoupled Floating Lateral Winglets (NO BARS, NO RECTANGLES, NO CYAN GLOW!) -->
    <g class="anim-winglet-l">
      <path d="{spline_left_pod}" fill="url(#master_wingletLeft)" stroke="#C8BEAD" stroke-width="0.9" />
    </g>

    <g class="anim-winglet-r">
      <path d="{spline_right_pod}" fill="url(#master_wingletRight)" stroke="#C8BEAD" stroke-width="0.9" />
    </g>

  </g>
</svg>"""
    return svg

if __name__ == "__main__":
    # Render on Dark
    im_dark = render_flawless_frame(scale=4, bg_color=(11, 15, 23, 255))
    im_dark.save("/tmp/test_flawless_dark.png")
    
    # Render on White
    im_white = render_flawless_frame(scale=4, bg_color=(255, 255, 255, 255))
    im_white.save("/tmp/test_flawless_white.png")
    
    # Render on Studio Green
    im_green = render_flawless_frame(scale=4, bg_color=(0, 255, 0, 255))
    im_green.save("/tmp/test_flawless_green.png")
    
    # Create 3-panel comparison board
    board = Image.new('RGB', (1536, 512), (0, 0, 0))
    board.paste(im_white.convert('RGB'), (0, 0))
    board.paste(im_dark.convert('RGB'), (512, 0))
    board.paste(im_green.convert('RGB'), (1024, 0))
    board.save("/tmp/test_flawless_board.png")
    print("✅ Saved /tmp/test_flawless_board.png")
    
    # Generate SVG
    svg_content = generate_clean_animated_svg(points_512)
    with open("/tmp/test_flawless.svg", "w") as f:
        f.write(svg_content)
    print("✅ Saved /tmp/test_flawless.svg")
