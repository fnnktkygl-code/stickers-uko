#!/usr/bin/env python3
"""
Official AItuko Master Error 404 Animation Engine — 100% Studio Fidelity Suite.
Generates fluid, endearing, seamless looping Error 404 animation strictly matching
canonical specifications and ground truth:
- Phase 1 (f=0..20): Sustentation nominale (peaceful floating levitation, smiling cyan arch eyes ^ ^)
- Phase 2 (f=21..28): Alert / Shock stutter (thrusters cut, cyan eyes OFF, red glowing exclamation marks '!   !')
- Phase 3 (f=29..34): Touchdown & seated transition (torso touches ground, canonical feet swing forward in front of torso)
- Phase 4 (f=35..74): Complete Grounded Seated Posture ("totalement assise"):
  * Porcelain torso collapses squarely onto the ground plane (dy_root = 44px, scale_x=1.04, scale_y=0.95)
  * Canonical landing feet pods seated flat IN FRONT OF torso, spread & resting on the floor:
    (dy_feet = +20px, dx_l=-12, dx_r=+12, rot_l=-16°, rot_r=+16°, scale_feet_x=1.15, scale_feet_y=0.85)
  * Decoupled lateral winglet pods drop down to the floor beside flanks (rot_l=+13.5°, rot_r=-13.5°, dy=52px)
  * Head bows forward with chin resting low over chest, discreetly concealing neck collar (dy_head=54px, rot_head=3.6°)
  * Visor displays 100% RED glowing digital 7-segment 'ERR' (cyber LED red #FF3B30, stroke width ~4, subtle bloom & highlight)
  * Cyan eyes are completely OFF (zero cyan on body or visor during error)
  * Ground contact shadow expands to full contact occlusion (shadow_s=1.35, shadow_a=235)
  * Strictly ZERO floating 404 card / screen (all telemetry inside the robot's visor screen)
- Phase 5 (f=75..84): System reboot & thruster reignition (red telemetry extinguishes, smiling cyan eyes ^ ^ reignite at f=81, upward thrust ascent)
- Phase 6 (f=85..119): Damped settling & seamless loop bouclage (smooth return to rest with conscious settle blink at f=103..107)

Strict Architectural & Anatomical Standards:
- Strictly ZERO human hands, ZERO fingers (aerodynamic porcelain pods only)
- Strictly ZERO foreign foot assets / ZERO foot swapping (uses ONLY master components lfoot & rfoot)
- Strictly ZERO floating card / screen
- Visor error telemetry: 100% RED — ZERO CYAN DURING ERROR
- Lustrous warm cream porcelain ceramic shading (#FAF8F5 / #F2EDE4), zero flat white paint, zero cyan on body
- Pure Vector Lottie JSON strictly < 50 KB with Bodymovin markers
- Multi-backdrop video and animated GIF/WebP deliverables across White, Dark, and Chroma Green
"""

import os
import sys
import math
import json
import shutil
import zipfile
import subprocess
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.build_master_vector_aituko import points_to_svg_cubic_spline
from scripts.build_flawless_aituko_idle import get_calibrated_master_splines, load_master_components, transform_rgba

WORKSPACE_DIR = "/Users/richard/Developer/Stickers Uko"
BRAIN_DIRS = [
    "/Users/richard/.gemini/antigravity/brain/0cd2247b-1c47-4dda-b692-574d0d799d98",
    "/Users/richard/.gemini/antigravity/brain/12dc3f80-67c3-41f2-9a22-76081a969c18",
    "/Users/richard/.gemini/antigravity/brain/ac37e720-db25-4d7f-a157-af9bd837d9c2",
    "/Users/richard/.gemini/antigravity/brain/fa7d6dc6-aed9-45de-bcb0-97eddb955525",
    "/Users/richard/.gemini/antigravity/brain/5c5bb48f-4d2c-498b-8689-41146af7df47",
    "/Users/richard/.gemini/antigravity/brain/467a784a-d1d2-4cca-89a3-7ecb1a862229",
    "/Users/richard/.gemini/antigravity/brain/cce42c8b-58a8-409f-aa1a-dd25d8b19f78",
    "/Users/richard/.gemini/antigravity/brain/83516754-5ac9-40c7-8491-3c074efdcaba",
    "/Users/richard/.gemini/antigravity/brain/fad00c0e-7c48-455a-89b5-6f8a6ea65af2",
    "/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68",
    "/Users/richard/.gemini/antigravity/brain/88d80b78-1cdb-447f-9df1-9299172c040b",
    "/Users/richard/.gemini/antigravity/brain/8378667c-4a1e-43c3-9957-f1104b73750f"
]

def get_all_brain_dirs():
    base_b = "/Users/richard/.gemini/antigravity/brain"
    d_set = set(BRAIN_DIRS)
    if os.path.exists(base_b):
        for entry in os.listdir(base_b):
            fp = os.path.join(base_b, entry)
            if os.path.isdir(fp) and not entry.startswith('.'):
                d_set.add(fp)
    return sorted(list(d_set))

TOTAL_FRAMES = 120
FPS = 30.0
LOOP_DURATION = 4.0  # seconds

COLOR_BG_DARK = (11, 15, 23, 255)
COLOR_BG_GREEN = (0, 255, 0, 255)
COLOR_BG_WHITE = (255, 255, 255, 255)
COLOR_RED_CORAL = (255, 59, 48, 255)
COLOR_CYAN = (0, 240, 255, 255)


def get_error_404_kinematics(f, total_frames=120):
    """
    Computes authentic cinematic kinematics for Error 404 (Canonical Grounded Posture):
    - f=0..20: Nominal floating levitation, smiling cyan arch eyes (^ ^)
    - f=21..28: Phase 2 Alert/Shock: Thrusters cut, cyan eyes shut off, red glowing exclamation marks '!   !'
    - f=26..35: Phase 3 Touchdown & seated transition: Canonical feet swing forward into Option Idéale (+12° / -12°)
    - f=35..74: Phase 4 Complete Grounded Seated Posture ("le tronc du corps aussi est au sol"):
        * Porcelain torso firmly grounded on floor plane (dy_root = 72.0px, scale_x=1.06, scale_y=0.93)
        * Option Idéale feet seated flat IN FRONT OF torso, resting on the floor plane y = 488:
          (dy_feet = +22.0px, dx_l=-8.0, dx_r=+8.0, rot_l=+12.0°, rot_r=-12.0°, scale_feet_x=1.12, scale_feet_y=0.88)
        * Decoupled lateral winglet pods drop down touching floor beside flanks (rot_l=+14.0°, rot_r=-14.0°, dy_pods=70.0px, dx_l=-4.0, dx_r=+4.0)
        * Head bows forward with chin resting low over chest, concealing neck collar (dy_head=78.0px, rot_head=3.6°)
        * Visor screen displays glowing red digital 7-segment 'ERR' (cyber LED red #FF3B30, stroke width ~4)
        * Cyan eyes completely OFF (zero cyan on entire mascot)
        * Ground contact shadow expands to full contact occlusion (shadow_s=1.35, shadow_a=235)
    - f=75..84: Phase 5 System reboot & thruster ascent (red telemetry extinguishes, smiling cyan eyes ^ ^ reignite at f=81, upward thrust liftoff)
    - f=85..119: Phase 6 Damped settling & seamless loop bouclage (smooth return to rest with conscious settle blink at f=103..107)
    """
    f = float(f)
    if f <= 20.0:
        # Phase 1: Nominal levitation
        u_nom = f / 20.0
        dy_root = 2.0 * math.sin(2.0 * math.pi * u_nom)
        dy_head = dy_root * 1.1
        dy_pods = dy_root * 0.95
        dy_feet = dy_root * 0.9
        dx_lfoot = 0.0
        dx_rfoot = 0.0
        rot_lfoot = 0.0
        rot_rfoot = 0.0
        scale_feet_x = 1.0
        scale_feet_y = 1.0
        rot_head = 0.0
        rot_lpod = 0.0
        rot_rpod = 0.0
        dx_lpod = 0.0
        dx_rpod = 0.0
        scale_x = 1.0
        scale_y = 1.0
        shadow_s = 1.0 - 0.03 * (dy_root / 2.0)
        shadow_a = int(round(135 - 15 * (dy_root / 2.0)))
        eye_opacity = 1.0
        scale_eye_y = 1.0
        eyes_shut = False
        excl_opacity = 0.0
        err_opacity = 0.0
        err_404_opacity = 0.0
        p_seated = 0.0
    elif f <= 26.0:
        # Phase 2: Alert/Shock drop onset, red glowing exclamation marks '!   !', cyan eyes completely OFF
        u = (f - 20.0) / 6.0
        p_drop = u**1.6
        dy_root = 18.0 * p_drop
        dy_head = 19.0 * p_drop
        dy_pods = 16.0 * p_drop
        dy_feet = 16.0 * p_drop
        dx_lfoot = 0.0
        dx_rfoot = 0.0
        rot_lfoot = 0.0
        rot_rfoot = 0.0
        scale_feet_x = 1.0
        scale_feet_y = 1.0
        rot_head = 1.5 * u
        rot_lpod = 2.0 * u
        rot_rpod = -2.0 * u
        dx_lpod = 0.0
        dx_rpod = 0.0
        scale_x = 1.0
        scale_y = 1.0
        shadow_s = 1.0 + 0.05 * u
        shadow_a = int(round(135 + 15 * u))
        eye_opacity = 0.0
        scale_eye_y = 1.0
        eyes_shut = False
        excl_opacity = 1.0
        err_opacity = 0.0
        err_404_opacity = 0.0
        p_seated = 0.0
    elif f <= 34.0:
        # Phase 3: Touchdown impact & smooth seated transition into Option Idéale feet and grounded torso (f=26..35)
        u = (f - 26.0) / 9.0
        s_u = u * u * (3.0 - 2.0 * u)
        dy_root = 18.0 + (72.0 - 18.0) * s_u
        dy_head = 19.0 + (78.0 - 19.0) * s_u
        dy_pods = 16.0 + (70.0 - 16.0) * s_u
        rot_head = 1.5 + (3.6 - 1.5) * s_u
        rot_lpod = 2.0 + (14.0 - 2.0) * s_u
        rot_rpod = -2.0 + (-14.0 - -2.0) * s_u
        dx_lpod = -4.0 * s_u
        dx_rpod = 4.0 * s_u
        dy_feet = 16.0 + (22.0 - 16.0) * s_u
        dx_lfoot = -8.0 * s_u
        dx_rfoot = 8.0 * s_u
        rot_lfoot = 12.0 * s_u
        rot_rfoot = -12.0 * s_u
        scale_feet_x = 1.0 + 0.12 * s_u
        scale_feet_y = 1.0 - 0.12 * s_u
        scale_x = 1.0 + 0.06 * s_u
        scale_y = 1.0 - 0.07 * s_u
        shadow_s = 1.05 + 0.30 * s_u
        shadow_a = int(round(150 + 85 * s_u))
        eye_opacity = 0.0
        scale_eye_y = 1.0
        eyes_shut = False
        excl_opacity = 1.0 if f <= 28.0 else 0.0
        err_opacity = 1.0 if f > 28.0 else 0.0
        err_404_opacity = err_opacity
        p_seated = s_u
    elif f <= 74.0:
        # Phase 4: Grounded complete seated posture ("le tronc du corps aussi est au sol")
        u_slump = (f - 35.0) / 39.0
        breath = 0.5 * math.sin(2.0 * math.pi * u_slump * 2.0)
        pulse = 0.94 + 0.06 * math.sin(2.0 * math.pi * u_slump * 4.0)
        dy_root = 72.0 + breath
        dy_head = 78.0 + breath
        dy_pods = 70.0
        rot_head = 3.6
        rot_lpod = 14.0
        rot_rpod = -14.0
        dx_lpod = -4.0
        dx_rpod = 4.0
        dy_feet = 22.0
        dx_lfoot = -8.0
        dx_rfoot = 8.0
        rot_lfoot = 12.0
        rot_rfoot = -12.0
        scale_feet_x = 1.12
        scale_feet_y = 0.88
        scale_x = 1.06
        scale_y = 0.93
        shadow_s = 1.35
        shadow_a = 235
        eye_opacity = 0.0
        scale_eye_y = 1.0
        eyes_shut = False
        excl_opacity = 0.0
        err_opacity = pulse
        err_404_opacity = pulse
        p_seated = 1.0
    elif f <= 84.0:
        # Phase 5: System reboot & thruster ascent (f=75..84 reboot interpolation, cyan eyes reignite at f=81)
        u = (f - 75.0) / 9.0
        s_u = 1.0 - (u * u * (3.0 - 2.0 * u))
        dy_root = 72.0 * s_u
        dy_head = 78.0 * s_u
        dy_pods = 70.0 * s_u
        rot_head = 3.6 * s_u
        rot_lpod = 14.0 * s_u
        rot_rpod = -14.0 * s_u
        dx_lpod = -4.0 * s_u
        dx_rpod = 4.0 * s_u
        dy_feet = 22.0 * s_u
        dx_lfoot = -8.0 * s_u
        dx_rfoot = 8.0 * s_u
        rot_lfoot = 12.0 * s_u
        rot_rfoot = -12.0 * s_u
        scale_feet_x = 1.0 + 0.12 * s_u
        scale_feet_y = 1.0 - 0.12 * s_u
        scale_x = 1.0 + 0.06 * s_u
        scale_y = 1.0 - 0.07 * s_u
        shadow_s = 1.0 + 0.35 * s_u
        shadow_a = int(round(135 + 100 * s_u))
        # Eyes reignite at f >= 81.0
        eye_opacity = 1.0 if f >= 81.0 else 0.0
        scale_eye_y = 1.0
        eyes_shut = False
        excl_opacity = 0.0
        err_opacity = 0.0
        err_404_opacity = 0.0
        p_seated = s_u
    else:
        # Phase 6: Damped settling & seamless loop bouclage (f=85..119)
        u_ret = (f - 85.0) / 34.0
        env = math.exp(-3.0 * u_ret)
        dy_root = -5.0 * env * math.sin(2.0 * math.pi * u_ret * 2.0)
        dy_head = dy_root * 1.1
        dy_pods = dy_root * 0.95
        dy_feet = dy_root * 0.9
        dx_lfoot = 0.0
        dx_rfoot = 0.0
        rot_lfoot = 0.0
        rot_rfoot = 0.0
        scale_feet_x = 1.0
        scale_feet_y = 1.0
        rot_head = 0.0
        rot_lpod = 0.0
        rot_rpod = 0.0
        dx_lpod = 0.0
        dx_rpod = 0.0
        scale_x = 1.0
        scale_y = 1.0
        shadow_s = 1.0
        shadow_a = 135
        
        # Conscious settle blink at f=103..107
        blink_sc = 1.0
        if 103 <= f <= 107:
            if f == 103: blink_sc = 0.5
            elif f in [104, 105]: blink_sc = 0.08
            elif f == 106: blink_sc = 0.5
            elif f == 107: blink_sc = 1.0
            
        eye_opacity = 1.0
        scale_eye_y = blink_sc
        eyes_shut = False
        excl_opacity = 0.0
        err_opacity = 0.0
        err_404_opacity = 0.0
        p_seated = 0.0

    return {
        'dy_root': round(dy_root, 2),
        'dy_head': round(dy_head, 2),
        'dy_pods': round(dy_pods, 2),
        'rot_head': round(rot_head, 2),
        'dy_feet': round(dy_feet, 2),
        'dx_lfoot': round(dx_lfoot, 2),
        'dx_rfoot': round(dx_rfoot, 2),
        'rot_lfoot': round(rot_lfoot, 2),
        'rot_rfoot': round(rot_rfoot, 2),
        'scale_feet_x': round(scale_feet_x, 3),
        'scale_feet_y': round(scale_feet_y, 3),
        'scale_torso_x': round(scale_x, 3),
        'scale_torso_y': round(scale_y, 3),
        'rot_lpod': round(rot_lpod, 2),
        'rot_rpod': round(rot_rpod, 2),
        'dx_lpod': round(dx_lpod, 2),
        'dx_rpod': round(dx_rpod, 2),
        'shadow_s': round(shadow_s, 3),
        'shadow_a': shadow_a,
        'eye_opacity': round(eye_opacity, 3),
        'scale_eye_y': round(scale_eye_y, 3),
        'eyes_shut': eyes_shut,
        'excl_opacity': round(excl_opacity, 3),
        'err_opacity': round(err_opacity, 3),
        'err_404_opacity': round(err_404_opacity, 3),
        'p_seated': round(p_seated, 3)
    }



def make_lottie_kf(t, s, e=None):
    kf = {
        't': t, 's': s if isinstance(s, list) else [s],
        'i': {'x': [0.4], 'y': [1.0]},
        'o': {'x': [0.4], 'y': [0.0]}
    }
    if e is not None:
        kf['e'] = e if isinstance(e, list) else [e]
    return kf


def points_to_lottie_shape(pts, anchor_x=0.0, anchor_y=0.0):
    rel_pts = [[p[0] - anchor_x, p[1] - anchor_y] for p in pts]
    return {
        'ty': 'sh', 'nm': 'Spline Path',
        'ks': {
            'a': 0,
            'k': {
                'c': True,
                'v': [[round(p[0], 2), round(p[1], 2)] for p in rel_pts],
                'i': [[0, 0] for _ in rel_pts],
                'o': [[0, 0] for _ in rel_pts]
            }
        }
    }


def make_stroke_shape(pts, closed=False, name='Stroke Path'):
    return {
        'ty': 'sh',
        'ks': {
            'a': 0,
            'k': {
                'c': closed,
                'v': [[round(p[0], 2), round(p[1], 2)] for p in pts],
                'i': [[0, 0] for _ in pts],
                'o': [[0, 0] for _ in pts]
            }
        },
        'nm': name
    }


def make_poly_shape(pts, anchor_x=0.0, anchor_y=0.0, name='Segment'):
    """Constructs a closed polygon path shape for Lottie with 1-decimal precision."""
    rel_pts = [[round(p[0] - anchor_x, 1), round(p[1] - anchor_y, 1)] for p in pts]
    return {
        'ty': 'sh', 'nm': name,
        'ks': {
            'a': 0,
            'k': {
                'c': True,
                'v': rel_pts,
                'i': [[0, 0] for _ in rel_pts],
                'o': [[0, 0] for _ in rel_pts]
            }
        }
    }


def get_7seg_polygons(ox, oy, w=20, h=32, sw=3.8, g=1.0, italic=0.0):
    """
    Computes vertices of authentic digital 7-segment display with 45° chamfered / mitred ends:
    a (top), b (top-right), c (bottom-right), d (bottom), e (bottom-left), f (top-left), g (middle).
    """
    mid_y = oy + h / 2.0
    pts_a = [(ox + sw/2.0 + g, oy), (ox + w - sw/2.0 - g, oy), (ox + w - sw - g, oy + sw), (ox + sw + g, oy + sw)]
    pts_d = [(ox + sw + g, oy + h - sw), (ox + w - sw - g, oy + h - sw), (ox + w - sw/2.0 - g, oy + h), (ox + sw/2.0 + g, oy + h)]
    pts_g = [(ox + sw/2.0 + g, mid_y), (ox + sw + g, mid_y - sw/2.0), (ox + w - sw - g, mid_y - sw/2.0),
             (ox + w - sw/2.0 - g, mid_y), (ox + w - sw - g, mid_y + sw/2.0), (ox + sw + g, mid_y + sw/2.0)]
    pts_f = [(ox, oy + sw/2.0 + g), (ox + sw, oy + sw + g), (ox + sw, mid_y - sw/2.0 - g), (ox, mid_y - g)]
    pts_b = [(ox + w - sw, oy + sw + g), (ox + w, oy + sw/2.0 + g), (ox + w, mid_y - g), (ox + w - sw, mid_y - sw/2.0 - g)]
    pts_e = [(ox, mid_y + g), (ox + sw, mid_y + sw/2.0 + g), (ox + sw, oy + h - sw - g), (ox, oy + h - sw/2.0 - g)]
    pts_c = [(ox + w - sw, mid_y + sw/2.0 + g), (ox + w, mid_y + g), (ox + w, oy + h - sw/2.0 - g), (ox + w - sw, oy + h - sw - g)]
    all_segs = {'a': pts_a, 'b': pts_b, 'c': pts_c, 'd': pts_d, 'e': pts_e, 'f': pts_f, 'g': pts_g}
    if italic != 0.0:
        rad = math.radians(italic)
        tan_v = math.tan(rad)
        sheared = {}
        for k, pts in all_segs.items():
            sheared[k] = [(px + (oy + h - py) * tan_v, py) for px, py in pts]
        return sheared
    return all_segs


def draw_7seg_glyph(draw, segs, ox, oy, w=20, h=32, sw=3.8, g=1.0, italic=0.0,
                    col_on=(255, 59, 48, 255), col_off=(45, 14, 16, 90), col_hl=(255, 208, 208, 240)):
    """Draws an authentic 7-segment digit with 45° chamfered / mitred polygonal segments."""
    all_segs = get_7seg_polygons(ox, oy, w=w, h=h, sw=sw, g=g, italic=italic)
    mid_y = oy + h / 2.0
    for k, pts in all_segs.items():
        is_on = segs.get(k, False)
        draw.polygon(pts, fill=col_on if is_on else col_off)
        if is_on:
            # inner highlight core line
            if len(pts) == 4:
                if k in ['b', 'c', 'e', 'f']:
                    # Vertical segments: top-center to bottom-center
                    mx1, my1 = (pts[0][0] + pts[1][0]) / 2.0, (pts[0][1] + pts[1][1]) / 2.0
                    mx2, my2 = (pts[2][0] + pts[3][0]) / 2.0, (pts[2][1] + pts[3][1]) / 2.0
                else:
                    # Horizontal segments: left-center to right-center
                    mx1, my1 = (pts[0][0] + pts[3][0]) / 2.0, (pts[0][1] + pts[3][1]) / 2.0
                    mx2, my2 = (pts[1][0] + pts[2][0]) / 2.0, (pts[1][1] + pts[2][1]) / 2.0
                draw.line([(mx1, my1), (mx2, my2)], fill=col_hl, width=max(1, int(round(sw * 0.25))))
            elif len(pts) == 6:
                draw.line([(pts[0][0] + sw/2.0, mid_y), (pts[3][0] - sw/2.0, mid_y)], fill=col_hl, width=max(1, int(round(sw * 0.25))))


def build_pure_vector_lottie(points_512):
    """
    Constructs the pure vector Lottie JSON (< 50KB) for Error 404 strictly per user directives:
    - Layer 10: Ground Contact Breathing Shadow
    - Layer 9: Porcelain Torso Capsule (slumped ground seating)
    - Layer 8: Right Pod Winglet (resting at floor beside body)
    - Layer 7: Left Pod Winglet (resting at floor beside body)
    - Layer 6: Right Foot Pod (Canonical seated flare in front of torso)
    - Layer 5: Left Foot Pod (Canonical seated flare in front of torso)
    - Layer 4: Mechanical Collar Socket
    - Layer 3: Porcelain Head Dome (empathetic bow)
    - Layer 2: Obsidian Visor Faceplate
    - Layer 1: Electric Cyan Eyes (^ ^ with conscious settle blink, off during error)
    - Layer 0: Red Visor Telemetry (! ! and 7-segment ERR)
    - Strictly ZERO external raster textures, ZERO floating 404 card.
    """
    C_CYAN = [0.0, 0.941, 1.0]
    C_RED_CORAL = [1.0, 0.231, 0.188]
    C_RED_HIGHLIGHT = [1.0, 0.745, 0.725]
    C_NECK = [0.094, 0.106, 0.149]
    C_NECK_BORDER = [0.18, 0.20, 0.26]
    C_STROKE = [0.78, 0.745, 0.69]

    # Polygon optimization for strict < 50 KB Lottie payload
    sim_points = {}
    for k, pts in points_512.items():
        arr = np.array(pts, dtype=np.float32).reshape(-1, 1, 2)
        eps = 0.45 if k in ['head', 'visor', 'torso'] else 0.40
        simplified = cv2.approxPolyDP(arr, eps, True)
        sim_points[k] = [[float(round(p[0][0], 1)), float(round(p[0][1], 1))] for p in simplified]

    body_times = [0, 20, 26, 35, 74, 84, 120]

    # 1. Shadow Layer
    sh_scale_kf = []
    sh_op_kf = []
    for idx, t in enumerate(body_times):
        k_curr = get_error_404_kinematics(t)
        sc = [round(k_curr['shadow_s'] * 100, 1), round(k_curr['shadow_s'] * 100, 1), 100.0]
        op = round((k_curr['shadow_a'] / 255.0) * 100.0, 1)
        if idx < len(body_times) - 1:
            next_t = body_times[idx + 1]
            k_next = get_error_404_kinematics(next_t)
            next_sc = [round(k_next['shadow_s'] * 100, 1), round(k_next['shadow_s'] * 100, 1), 100.0]
            next_op = round((k_next['shadow_a'] / 255.0) * 100.0, 1)
            sh_scale_kf.append(make_lottie_kf(t, sc, next_sc))
            sh_op_kf.append(make_lottie_kf(t, op, next_op))
        else:
            sh_scale_kf.append(make_lottie_kf(t, sc))
            sh_op_kf.append(make_lottie_kf(t, op))

    shadow_layer = {
        'ddd': 0, 'ind': 10, 'ty': 4, 'nm': 'Ground Contact Shadow', 'sr': 1,
        'ks': {
            'o': {'a': 1, 'k': sh_op_kf}, 'r': {'a': 0, 'k': 0},
            'p': {'a': 0, 'k': [256, 488, 0]}, 'a': {'a': 0, 'k': [0, 0, 0]},
            's': {'a': 1, 'k': sh_scale_kf}
        },
        'ao': 0,
        'shapes': [{
            'ty': 'gr', 'nm': 'Shadow Group',
            'it': [
                {'ty': 'el', 'd': 1, 's': {'a': 0, 'k': [190, 24]}, 'p': {'a': 0, 'k': [0, 0]}, 'nm': 'Shadow Ellipse'},
                {'ty': 'gf', 'nm': 'Shadow Grad', 'o': {'a': 0, 'k': 100}, 't': 2, 's': {'a': 0, 'k': [0, 0]}, 'e': {'a': 0, 'k': [95, 12]}, 'g': {'p': 2, 'k': {'a': 0, 'k': [0.0, 0, 0, 0, 1.0, 0, 0, 0, 0.0, 0.92, 0.6, 0.5, 1.0, 0.0]}}},
                {'p': {'a': 0, 'k': [0, 0]}, 'a': {'a': 0, 'k': [0, 0]}, 's': {'a': 0, 'k': [100, 100]}, 'r': {'a': 0, 'k': 0}, 'o': {'a': 0, 'k': 100}, 'ty': 'tr'}
            ]
        }],
        'ip': 0, 'op': 120, 'st': 0, 'bm': 0
    }

    # 2. Torso Layer (Seated Ground Slump)
    torso_pos_kf = []
    torso_sc_kf = []
    for idx, t in enumerate(body_times):
        k_curr = get_error_404_kinematics(t)
        pos = [256.0, round(312.0 + k_curr['dy_root'], 1), 0.0]
        sc = [round(k_curr['scale_torso_x'] * 100, 1), round(k_curr['scale_torso_y'] * 100, 1), 100.0]
        if idx < len(body_times) - 1:
            next_t = body_times[idx + 1]
            k_next = get_error_404_kinematics(next_t)
            next_pos = [256.0, round(312.0 + k_next['dy_root'], 1), 0.0]
            next_sc = [round(k_next['scale_torso_x'] * 100, 1), round(k_next['scale_torso_y'] * 100, 1), 100.0]
            torso_pos_kf.append(make_lottie_kf(t, pos, next_pos))
            torso_sc_kf.append(make_lottie_kf(t, sc, next_sc))
        else:
            torso_pos_kf.append(make_lottie_kf(t, pos))
            torso_sc_kf.append(make_lottie_kf(t, sc))

    torso_layer = {
        'ddd': 0, 'ind': 9, 'ty': 4, 'nm': 'Porcelain Torso Capsule', 'sr': 1,
        'ks': {
            'o': {'a': 0, 'k': 100}, 'r': {'a': 0, 'k': 0}, 'p': {'a': 1, 'k': torso_pos_kf},
            'a': {'a': 0, 'k': [256.0, 312.0, 0]}, 's': {'a': 1, 'k': torso_sc_kf}
        },
        'ao': 0,
        'shapes': [{
            'ty': 'gr', 'nm': 'Torso Geometry',
            'it': [
                points_to_lottie_shape(sim_points['torso'], 256.0, 312.0),
                {'ty': 'gf', 'nm': 'Porcelain Gradient', 'o': {'a': 0, 'k': 100}, 't': 1, 's': {'a': 0, 'k': [-45, -70]}, 'e': {'a': 0, 'k': [55, 80]}, 'g': {'p': 4, 'k': {'a': 0, 'k': [0.0, 1, 1, 1, 0.35, 0.98, 0.97, 0.95, 0.75, 0.91, 0.89, 0.84, 1.0, 0.82, 0.78, 0.72]}}},
                {'ty': 'st', 'c': {'a': 0, 'k': C_STROKE}, 'o': {'a': 0, 'k': 100}, 'w': {'a': 0, 'k': 0.8}, 'lc': 2, 'lj': 2, 'nm': 'St'},
                {'p': {'a': 0, 'k': [0, 0]}, 'a': {'a': 0, 'k': [0, 0]}, 's': {'a': 0, 'k': [100, 100]}, 'r': {'a': 0, 'k': 0}, 'o': {'a': 0, 'k': 100}, 'ty': 'tr'}
            ]
        }],
        'ip': 0, 'op': 120, 'st': 0, 'bm': 0
    }

    # 3. Lateral Pods (resting down beside body on floor)
    lpod_pos_kf = []
    lpod_rot_kf = []
    rpod_pos_kf = []
    rpod_rot_kf = []
    for idx, t in enumerate(body_times):
        k_curr = get_error_404_kinematics(t)
        pos_l = [round(158.0 + k_curr['dx_lpod'], 1), round(268.0 + k_curr['dy_pods'], 1), 0.0]
        pos_r = [round(354.0 + k_curr['dx_rpod'], 1), round(268.0 + k_curr['dy_pods'], 1), 0.0]
        rot_l = round(k_curr['rot_lpod'], 1)
        rot_r = round(k_curr['rot_rpod'], 1)
        if idx < len(body_times) - 1:
            next_t = body_times[idx + 1]
            k_next = get_error_404_kinematics(next_t)
            next_pos_l = [round(158.0 + k_next['dx_lpod'], 1), round(268.0 + k_next['dy_pods'], 1), 0.0]
            next_pos_r = [round(354.0 + k_next['dx_rpod'], 1), round(268.0 + k_next['dy_pods'], 1), 0.0]
            next_rot_l = round(k_next['rot_lpod'], 1)
            next_rot_r = round(k_next['rot_rpod'], 1)
            lpod_pos_kf.append(make_lottie_kf(t, pos_l, next_pos_l))
            lpod_rot_kf.append(make_lottie_kf(t, rot_l, next_rot_l))
            rpod_pos_kf.append(make_lottie_kf(t, pos_r, next_pos_r))
            rpod_rot_kf.append(make_lottie_kf(t, rot_r, next_rot_r))
        else:
            lpod_pos_kf.append(make_lottie_kf(t, pos_l))
            lpod_rot_kf.append(make_lottie_kf(t, rot_l))
            rpod_pos_kf.append(make_lottie_kf(t, pos_r))
            rpod_rot_kf.append(make_lottie_kf(t, rot_r))

    left_pod_layer = {
        'ddd': 0, 'ind': 7, 'ty': 4, 'nm': 'Left Pod Winglet (Floor Rest)', 'sr': 1,
        'ks': {
            'o': {'a': 0, 'k': 100}, 'r': {'a': 1, 'k': lpod_rot_kf}, 'p': {'a': 1, 'k': lpod_pos_kf},
            'a': {'a': 0, 'k': [158.0, 268.0, 0]}, 's': {'a': 0, 'k': [100, 100, 100]}
        },
        'ao': 0,
        'shapes': [{
            'ty': 'gr', 'nm': 'Left Winglet',
            'it': [
                points_to_lottie_shape(sim_points['left_pod'], 158.0, 268.0),
                {'ty': 'gf', 'nm': 'Left Winglet Shading', 'o': {'a': 0, 'k': 100}, 't': 1, 's': {'a': 0, 'k': [-30, -50]}, 'e': {'a': 0, 'k': [30, 50]}, 'g': {'p': 4, 'k': {'a': 0, 'k': [0.0, 1, 1, 1, 0.4, 0.98, 0.97, 0.95, 0.85, 0.87, 0.84, 0.78, 1.0, 0.78, 0.75, 0.68]}}},
                {'ty': 'st', 'c': {'a': 0, 'k': C_STROKE}, 'o': {'a': 0, 'k': 100}, 'w': {'a': 0, 'k': 0.8}, 'lc': 2, 'lj': 2, 'nm': 'St'},
                {'p': {'a': 0, 'k': [0, 0]}, 'a': {'a': 0, 'k': [0, 0]}, 's': {'a': 0, 'k': [100, 100]}, 'r': {'a': 0, 'k': 0}, 'o': {'a': 0, 'k': 100}, 'ty': 'tr'}
            ]
        }],
        'ip': 0, 'op': 120, 'st': 0, 'bm': 0
    }

    right_pod_layer = {
        'ddd': 0, 'ind': 8, 'ty': 4, 'nm': 'Right Pod Winglet (Floor Rest)', 'sr': 1,
        'ks': {
            'o': {'a': 0, 'k': 100}, 'r': {'a': 1, 'k': rpod_rot_kf}, 'p': {'a': 1, 'k': rpod_pos_kf},
            'a': {'a': 0, 'k': [354.0, 268.0, 0]}, 's': {'a': 0, 'k': [100, 100, 100]}
        },
        'ao': 0,
        'shapes': [{
            'ty': 'gr', 'nm': 'Right Winglet',
            'it': [
                points_to_lottie_shape(sim_points['right_pod'], 354.0, 268.0),
                {'ty': 'gf', 'nm': 'Right Winglet Shading', 'o': {'a': 0, 'k': 100}, 't': 1, 's': {'a': 0, 'k': [30, -50]}, 'e': {'a': 0, 'k': [-30, 50]}, 'g': {'p': 4, 'k': {'a': 0, 'k': [0.0, 1, 1, 1, 0.4, 0.98, 0.97, 0.95, 0.85, 0.87, 0.84, 0.78, 1.0, 0.78, 0.75, 0.68]}}},
                {'ty': 'st', 'c': {'a': 0, 'k': C_STROKE}, 'o': {'a': 0, 'k': 100}, 'w': {'a': 0, 'k': 0.8}, 'lc': 2, 'lj': 2, 'nm': 'St'},
                {'p': {'a': 0, 'k': [0, 0]}, 'a': {'a': 0, 'k': [0, 0]}, 's': {'a': 0, 'k': [100, 100]}, 'r': {'a': 0, 'k': 0}, 'o': {'a': 0, 'k': 100}, 'ty': 'tr'}
            ]
        }],
        'ip': 0, 'op': 120, 'st': 0, 'bm': 0
    }

    # 4. Canonical Landing Feet Pods (Rendered IN FRONT OF Torso per Directive 1!)
    lfoot_pos_kf = []
    lfoot_rot_kf = []
    lfoot_sc_kf = []
    rfoot_pos_kf = []
    rfoot_rot_kf = []
    rfoot_sc_kf = []
    for idx, t in enumerate(body_times):
        k_curr = get_error_404_kinematics(t)
        pos_l = [round(214.0 + k_curr['dx_lfoot'], 1), round(448.0 + k_curr['dy_feet'], 1), 0.0]
        pos_r = [round(298.0 + k_curr['dx_rfoot'], 1), round(448.0 + k_curr['dy_feet'], 1), 0.0]
        rot_l = round(k_curr['rot_lfoot'], 1)
        rot_r = round(k_curr['rot_rfoot'], 1)
        sc_l = [round(k_curr['scale_feet_x'] * 100, 1), round(k_curr['scale_feet_y'] * 100, 1), 100.0]
        sc_r = [round(k_curr['scale_feet_x'] * 100, 1), round(k_curr['scale_feet_y'] * 100, 1), 100.0]
        if idx < len(body_times) - 1:
            next_t = body_times[idx + 1]
            k_next = get_error_404_kinematics(next_t)
            next_pos_l = [round(214.0 + k_next['dx_lfoot'], 1), round(448.0 + k_next['dy_feet'], 1), 0.0]
            next_pos_r = [round(298.0 + k_next['dx_rfoot'], 1), round(448.0 + k_next['dy_feet'], 1), 0.0]
            next_rot_l = round(k_next['rot_lfoot'], 1)
            next_rot_r = round(k_next['rot_rfoot'], 1)
            next_sc_l = [round(k_next['scale_feet_x'] * 100, 1), round(k_next['scale_feet_y'] * 100, 1), 100.0]
            next_sc_r = [round(k_next['scale_feet_x'] * 100, 1), round(k_next['scale_feet_y'] * 100, 1), 100.0]
            lfoot_pos_kf.append(make_lottie_kf(t, pos_l, next_pos_l))
            lfoot_rot_kf.append(make_lottie_kf(t, rot_l, next_rot_l))
            lfoot_sc_kf.append(make_lottie_kf(t, sc_l, next_sc_l))
            rfoot_pos_kf.append(make_lottie_kf(t, pos_r, next_pos_r))
            rfoot_rot_kf.append(make_lottie_kf(t, rot_r, next_rot_r))
            rfoot_sc_kf.append(make_lottie_kf(t, sc_r, next_sc_r))
        else:
            lfoot_pos_kf.append(make_lottie_kf(t, pos_l))
            lfoot_rot_kf.append(make_lottie_kf(t, rot_l))
            lfoot_sc_kf.append(make_lottie_kf(t, sc_l))
            rfoot_pos_kf.append(make_lottie_kf(t, pos_r))
            rfoot_rot_kf.append(make_lottie_kf(t, rot_r))
            rfoot_sc_kf.append(make_lottie_kf(t, sc_r))

    left_foot_layer = {
        'ddd': 0, 'ind': 5, 'ty': 4, 'nm': 'Left Foot Pod (Seated Flare)', 'sr': 1,
        'ks': {
            'o': {'a': 0, 'k': 100}, 'r': {'a': 1, 'k': lfoot_rot_kf}, 'p': {'a': 1, 'k': lfoot_pos_kf},
            'a': {'a': 0, 'k': [214.0, 448.0, 0]}, 's': {'a': 1, 'k': lfoot_sc_kf}
        },
        'ao': 0,
        'shapes': [{
            'ty': 'gr', 'nm': 'Left Foot Shape',
            'it': [
                points_to_lottie_shape(sim_points['left_foot'], 214.0, 448.0),
                {'ty': 'gf', 'nm': 'Foot Grad', 'o': {'a': 0, 'k': 100}, 't': 1, 's': {'a': 0, 'k': [-25, -10]}, 'e': {'a': 0, 'k': [25, 20]}, 'g': {'p': 4, 'k': {'a': 0, 'k': [0.0, 1, 1, 1, 0.35, 0.98, 0.97, 0.95, 0.75, 0.92, 0.90, 0.85, 1.0, 0.85, 0.82, 0.77]}}},
                {'ty': 'st', 'c': {'a': 0, 'k': C_STROKE}, 'o': {'a': 0, 'k': 100}, 'w': {'a': 0, 'k': 0.8}, 'lc': 2, 'lj': 2, 'nm': 'St'},
                {'p': {'a': 0, 'k': [0, 0]}, 'a': {'a': 0, 'k': [0, 0]}, 's': {'a': 0, 'k': [100, 100]}, 'r': {'a': 0, 'k': 0}, 'o': {'a': 0, 'k': 100}, 'ty': 'tr'}
            ]
        }],
        'ip': 0, 'op': 120, 'st': 0, 'bm': 0
    }

    right_foot_layer = {
        'ddd': 0, 'ind': 6, 'ty': 4, 'nm': 'Right Foot Pod (Seated Flare)', 'sr': 1,
        'ks': {
            'o': {'a': 0, 'k': 100}, 'r': {'a': 1, 'k': rfoot_rot_kf}, 'p': {'a': 1, 'k': rfoot_pos_kf},
            'a': {'a': 0, 'k': [298.0, 448.0, 0]}, 's': {'a': 1, 'k': rfoot_sc_kf}
        },
        'ao': 0,
        'shapes': [{
            'ty': 'gr', 'nm': 'Right Foot Shape',
            'it': [
                points_to_lottie_shape(sim_points['right_foot'], 298.0, 448.0),
                {'ty': 'gf', 'nm': 'Foot Grad', 'o': {'a': 0, 'k': 100}, 't': 1, 's': {'a': 0, 'k': [-25, -10]}, 'e': {'a': 0, 'k': [25, 20]}, 'g': {'p': 4, 'k': {'a': 0, 'k': [0.0, 1, 1, 1, 0.35, 0.98, 0.97, 0.95, 0.75, 0.92, 0.90, 0.85, 1.0, 0.85, 0.82, 0.77]}}},
                {'ty': 'st', 'c': {'a': 0, 'k': C_STROKE}, 'o': {'a': 0, 'k': 100}, 'w': {'a': 0, 'k': 0.8}, 'lc': 2, 'lj': 2, 'nm': 'St'},
                {'p': {'a': 0, 'k': [0, 0]}, 'a': {'a': 0, 'k': [0, 0]}, 's': {'a': 0, 'k': [100, 100]}, 'r': {'a': 0, 'k': 0}, 'o': {'a': 0, 'k': 100}, 'ty': 'tr'}
            ]
        }],
        'ip': 0, 'op': 120, 'st': 0, 'bm': 0
    }

    # 5. Head & Neck Kinematics
    head_pos_kf = []
    head_rot_kf = []
    for idx, t in enumerate(body_times):
        k_curr = get_error_404_kinematics(t)
        pos = [256.0, round(204.0 + k_curr['dy_head'], 1), 0.0]
        rot = round(k_curr['rot_head'], 1)
        if idx < len(body_times) - 1:
            next_t = body_times[idx + 1]
            k_next = get_error_404_kinematics(next_t)
            next_pos = [256.0, round(204.0 + k_next['dy_head'], 1), 0.0]
            next_rot = round(k_next['rot_head'], 1)
            head_pos_kf.append(make_lottie_kf(t, pos, next_pos))
            head_rot_kf.append(make_lottie_kf(t, rot, next_rot))
        else:
            head_pos_kf.append(make_lottie_kf(t, pos))
            head_rot_kf.append(make_lottie_kf(t, rot))

    neck_layer = {
        'ddd': 0, 'ind': 4, 'ty': 4, 'nm': 'Mechanical Collar Socket', 'sr': 1,
        'ks': {
            'o': {'a': 0, 'k': 100}, 'r': {'a': 0, 'k': 0}, 'p': {'a': 1, 'k': head_pos_kf},
            'a': {'a': 0, 'k': [0, 0, 0]}, 's': {'a': 0, 'k': [100, 100, 100]}
        },
        'ao': 0,
        'shapes': [{
            'ty': 'gr', 'nm': 'Collar Ring',
            'it': [
                {'ty': 'el', 'd': 1, 's': {'a': 0, 'k': [30, 14]}, 'p': {'a': 0, 'k': [0, 0]}, 'nm': 'El'},
                {'ty': 'fl', 'c': {'a': 0, 'k': C_NECK}, 'o': {'a': 0, 'k': 100}, 'nm': 'Fl'},
                {'ty': 'st', 'c': {'a': 0, 'k': C_NECK_BORDER}, 'o': {'a': 0, 'k': 100}, 'w': {'a': 0, 'k': 0.8}, 'lc': 2, 'lj': 2, 'nm': 'St'},
                {'p': {'a': 0, 'k': [0, 0]}, 'a': {'a': 0, 'k': [0, 0]}, 's': {'a': 0, 'k': [100, 100]}, 'r': {'a': 0, 'k': 0}, 'o': {'a': 0, 'k': 100}, 'ty': 'tr'}
            ]
        }],
        'ip': 0, 'op': 120, 'st': 0, 'bm': 0
    }

    head_layer = {
        'ddd': 0, 'ind': 3, 'ty': 4, 'nm': 'Porcelain Head Dome', 'sr': 1,
        'ks': {
            'o': {'a': 0, 'k': 100}, 'r': {'a': 1, 'k': head_rot_kf}, 'p': {'a': 1, 'k': head_pos_kf},
            'a': {'a': 0, 'k': [256.0, 204.0, 0]}, 's': {'a': 0, 'k': [100, 100, 100]}
        },
        'ao': 0,
        'shapes': [{
            'ty': 'gr', 'nm': 'Head Porcelain',
            'it': [
                points_to_lottie_shape(sim_points['head'], 256.0, 204.0),
                {'ty': 'gf', 'nm': 'Porcelain Cranial Grad', 'o': {'a': 0, 'k': 100}, 't': 1, 's': {'a': 0, 'k': [-60, -70]}, 'e': {'a': 0, 'k': [60, 60]}, 'g': {'p': 4, 'k': {'a': 0, 'k': [0.0, 1, 1, 1, 0.35, 0.98, 0.97, 0.95, 0.75, 0.92, 0.90, 0.85, 1.0, 0.85, 0.82, 0.77]}}},
                {'ty': 'st', 'c': {'a': 0, 'k': C_STROKE}, 'o': {'a': 0, 'k': 100}, 'w': {'a': 0, 'k': 0.8}, 'lc': 2, 'lj': 2, 'nm': 'St'},
                {'p': {'a': 0, 'k': [0, 0]}, 'a': {'a': 0, 'k': [0, 0]}, 's': {'a': 0, 'k': [100, 100]}, 'r': {'a': 0, 'k': 0}, 'o': {'a': 0, 'k': 100}, 'ty': 'tr'}
            ]
        }],
        'ip': 0, 'op': 120, 'st': 0, 'bm': 0
    }

    visor_layer = {
        'ddd': 0, 'ind': 2, 'ty': 4, 'nm': 'Obsidian Visor Faceplate', 'sr': 1,
        'ks': {
            'o': {'a': 0, 'k': 100}, 'r': {'a': 1, 'k': head_rot_kf}, 'p': {'a': 1, 'k': head_pos_kf},
            'a': {'a': 0, 'k': [256.0, 204.0, 0]}, 's': {'a': 0, 'k': [100, 100, 100]}
        },
        'ao': 0,
        'shapes': [{
            'ty': 'gr', 'nm': 'Visor Shape',
            'it': [
                points_to_lottie_shape(sim_points['visor'], 256.0, 204.0),
                {'ty': 'gf', 'nm': 'Visor Obsidian Radial', 'o': {'a': 0, 'k': 100}, 't': 2, 's': {'a': 0, 'k': [0, -10]}, 'e': {'a': 0, 'k': [0, 50]}, 'g': {'p': 3, 'k': {'a': 0, 'k': [0.0, 0.094, 0.106, 0.149, 0.6, 0.063, 0.075, 0.11, 1.0, 0.027, 0.031, 0.051]}}},
                {'ty': 'st', 'c': {'a': 0, 'k': [0.1, 0.12, 0.17]}, 'o': {'a': 0, 'k': 100}, 'w': {'a': 0, 'k': 1.2}, 'lc': 2, 'lj': 2, 'nm': 'St'},
                {'p': {'a': 0, 'k': [0, 0]}, 'a': {'a': 0, 'k': [0, 0]}, 's': {'a': 0, 'k': [100, 100]}, 'r': {'a': 0, 'k': 0}, 'o': {'a': 0, 'k': 100}, 'ty': 'tr'}
            ]
        }],
        'ip': 0, 'op': 120, 'st': 0, 'bm': 0
    }

    # 6. Electric Cyan Eyes (^ ^ with Conscious Blinking, strictly OFF during error)
    eye_times = [0, 20, 21, 80, 81, 103, 105, 107, 120]
    eye_op_kf = []
    eye_sc_kf = []
    for idx, t in enumerate(eye_times):
        k_curr = get_error_404_kinematics(t)
        op = round(k_curr['eye_opacity'] * 100.0, 1)
        sc = [100.0, round(k_curr['scale_eye_y'] * 100.0, 1), 100.0]
        if idx < len(eye_times) - 1:
            next_t = eye_times[idx + 1]
            k_next = get_error_404_kinematics(next_t)
            next_op = round(k_next['eye_opacity'] * 100.0, 1)
            next_sc = [100.0, round(k_next['scale_eye_y'] * 100.0, 1), 100.0]
            eye_op_kf.append(make_lottie_kf(t, op, next_op))
            eye_sc_kf.append(make_lottie_kf(t, sc, next_sc))
        else:
            eye_op_kf.append(make_lottie_kf(t, op))
            eye_sc_kf.append(make_lottie_kf(t, sc))

    eye_layer = {
        'ddd': 0, 'ind': 1, 'ty': 4, 'nm': 'Electric Cyan Eyes', 'sr': 1,
        'ks': {
            'o': {'a': 1, 'k': eye_op_kf}, 'r': {'a': 1, 'k': head_rot_kf}, 'p': {'a': 1, 'k': head_pos_kf},
            'a': {'a': 0, 'k': [256.0, 204.0, 0]}, 's': {'a': 1, 'k': eye_sc_kf}
        },
        'ao': 0,
        'shapes': [
            {'ty': 'gr', 'nm': 'Left Eye', 'it': [
                points_to_lottie_shape(sim_points['left_eye'], 256.0, 204.0),
                {'ty': 'fl', 'c': {'a': 0, 'k': C_CYAN}, 'o': {'a': 0, 'k': 100}, 'nm': 'Fl'},
                {'p': {'a': 0, 'k': [0, 0]}, 'a': {'a': 0, 'k': [0, 0]}, 's': {'a': 0, 'k': [100, 100]}, 'r': {'a': 0, 'k': 0}, 'o': {'a': 0, 'k': 100}, 'ty': 'tr'}
            ]},
            {'ty': 'gr', 'nm': 'Right Eye', 'it': [
                points_to_lottie_shape(sim_points['right_eye'], 256.0, 204.0),
                {'ty': 'fl', 'c': {'a': 0, 'k': C_CYAN}, 'o': {'a': 0, 'k': 100}, 'nm': 'Fl'},
                {'p': {'a': 0, 'k': [0, 0]}, 'a': {'a': 0, 'k': [0, 0]}, 's': {'a': 0, 'k': [100, 100]}, 'r': {'a': 0, 'k': 0}, 'o': {'a': 0, 'k': 100}, 'ty': 'tr'}
            ]}
        ],
        'ip': 0, 'op': 120, 'st': 0, 'bm': 0
    }

    # 7. Red Visor Telemetry (Phase 2 '! !' and Phase 4 digital 7-segment 'ERR')
    # Directive 3: 100% RED, ZERO CYAN DURING ERROR
    excl_times = [0, 20, 21, 28, 29, 120]
    excl_op_kf = []
    for idx, t in enumerate(excl_times):
        k = get_error_404_kinematics(t)
        op = round(k['excl_opacity'] * 100.0, 1)
        if idx < len(excl_times) - 1:
            next_t = excl_times[idx + 1]
            k_next = get_error_404_kinematics(next_t)
            next_op = round(k_next['excl_opacity'] * 100.0, 1)
            excl_op_kf.append(make_lottie_kf(t, op, next_op))
        else:
            excl_op_kf.append(make_lottie_kf(t, op))

    err_times = [0, 28, 29, 74, 75, 120]
    err_op_kf = []
    for idx, t in enumerate(err_times):
        k = get_error_404_kinematics(t)
        op = round(k['err_opacity'] * 100.0, 1)
        if idx < len(err_times) - 1:
            next_t = err_times[idx + 1]
            k_next = get_error_404_kinematics(next_t)
            next_op = round(k_next['err_opacity'] * 100.0, 1)
            err_op_kf.append(make_lottie_kf(t, op, next_op))
        else:
            err_op_kf.append(make_lottie_kf(t, op))

    # Vector stroke paths for '!   !' (Phase 2)
    # Head anchor is (256, 204). Eye level is 120 (rel_y = -84). Left is 221 (rel_x = -35), Right is 291 (rel_x = +35)
    s_excl_l_stem = make_stroke_shape([(-35, -99), (-35, -84)], False)
    s_excl_l_dot = {'ty': 'el', 'd': 1, 's': {'a': 0, 'k': [5, 5]}, 'p': {'a': 0, 'k': [-35, -77]}, 'nm': 'DotExclL'}
    s_excl_r_stem = make_stroke_shape([(35, -99), (35, -84)], False)
    s_excl_r_dot = {'ty': 'el', 'd': 1, 's': {'a': 0, 'k': [5, 5]}, 'p': {'a': 0, 'k': [35, -77]}, 'nm': 'DotExclR'}

    # Option 01 : 7-Segments Classique Industriel ('E r r')
    # Authentic 7-segment LED display geometry:
    # Character 1: 'E' (a, f, g, e, d lit)
    # Character 2: 'r' (e, g lit: bottom-left vertical + middle horizontal bar)
    # Character 3: 'r' (e, g lit: bottom-left vertical + middle horizontal bar)
    # Centered on visor at y in [105, 137], anchor (256, 204)
    lottie_glyphs = [
        (214, {'a': True, 'f': True, 'g': True, 'e': True, 'd': True}, 'E'),
        (244, {'e': True, 'g': True}, 'r1'),
        (274, {'e': True, 'g': True}, 'r2'),
    ]
    lottie_ghost_shapes = []
    lottie_active_shapes = []
    lottie_hl_shapes = []

    for ox, active_dict, gname in lottie_glyphs:
        polys = get_7seg_polygons(ox, 105, w=20, h=32, sw=3.8, g=1.0)
        for seg_key, pts in polys.items():
            if active_dict.get(seg_key, False):
                lottie_active_shapes.append(make_poly_shape(pts, anchor_x=256.0, anchor_y=204.0, name=f'{gname}_{seg_key}'))
                mid_y = 105.0 + 16.0
                if len(pts) == 4:
                    if seg_key in ['b', 'c', 'e', 'f']:
                        mx1 = (pts[0][0] + pts[1][0]) / 2.0 - 256.0
                        my1 = (pts[0][1] + pts[1][1]) / 2.0 - 204.0
                        mx2 = (pts[2][0] + pts[3][0]) / 2.0 - 256.0
                        my2 = (pts[2][1] + pts[3][1]) / 2.0 - 204.0
                    else:
                        mx1 = (pts[0][0] + pts[3][0]) / 2.0 - 256.0
                        my1 = (pts[0][1] + pts[3][1]) / 2.0 - 204.0
                        mx2 = (pts[1][0] + pts[2][0]) / 2.0 - 256.0
                        my2 = (pts[1][1] + pts[2][1]) / 2.0 - 204.0
                    lottie_hl_shapes.append(make_stroke_shape([(mx1, my1), (mx2, my2)], name=f'{gname}_{seg_key}_hl'))
                elif len(pts) == 6:
                    x1 = pts[0][0] + 3.8 / 2.0 - 256.0
                    x2 = pts[3][0] - 3.8 / 2.0 - 256.0
                    y = mid_y - 204.0
                    lottie_hl_shapes.append(make_stroke_shape([(x1, y), (x2, y)], name=f'{gname}_{seg_key}_hl'))
            else:
                lottie_ghost_shapes.append(make_poly_shape(pts, anchor_x=256.0, anchor_y=204.0, name=f'{gname}_{seg_key}_ghost'))

    visor_telemetry_layer = {
        'ddd': 0, 'ind': 0, 'ty': 4, 'nm': "Red Visor Telemetry (! ! and ERR)", 'sr': 1,
        'ks': {
            'o': {'a': 0, 'k': 100}, 'r': {'a': 1, 'k': head_rot_kf}, 'p': {'a': 1, 'k': head_pos_kf},
            'a': {'a': 0, 'k': [256.0, 204.0, 0]}, 's': {'a': 0, 'k': [100, 100, 100]}
        },
        'ao': 0,
        'shapes': [
            {
                'ty': 'gr', 'nm': 'Alert Exclamations (! !)',
                'it': [
                    {
                        'ty': 'gr', 'nm': 'Stems',
                        'it': [
                            s_excl_l_stem, s_excl_r_stem,
                            {'ty': 'st', 'c': {'a': 0, 'k': C_RED_CORAL}, 'o': {'a': 100}, 'w': {'a': 0, 'k': 4.0}, 'lc': 2, 'lj': 2, 'nm': 'StExclStem'},
                            {'p': {'a': 0, 'k': [0, 0]}, 'a': {'a': 0, 'k': [0, 0]}, 's': {'a': 0, 'k': [100, 100]}, 'r': {'a': 0, 'k': 0}, 'o': {'a': 0, 'k': 100}, 'ty': 'tr'}
                        ]
                    },
                    {
                        'ty': 'gr', 'nm': 'Dots',
                        'it': [
                            s_excl_l_dot, s_excl_r_dot,
                            {'ty': 'fl', 'c': {'a': 0, 'k': C_RED_CORAL}, 'o': {'a': 100}, 'nm': 'FlExclDot'},
                            {'p': {'a': 0, 'k': [0, 0]}, 'a': {'a': 0, 'k': [0, 0]}, 's': {'a': 0, 'k': [100, 100]}, 'r': {'a': 0, 'k': 0}, 'o': {'a': 0, 'k': 100}, 'ty': 'tr'}
                        ]
                    },
                    {'p': {'a': 0, 'k': [0, 0]}, 'a': {'a': 0, 'k': [0, 0]}, 's': {'a': 0, 'k': [100, 100]}, 'r': {'a': 0, 'k': 0}, 'o': {'a': 1, 'k': excl_op_kf}, 'ty': 'tr'}
                ]
            },
            {
                'ty': 'gr', 'nm': 'Digital 7-Segment ERR',
                'it': [
                    {
                        'ty': 'gr', 'nm': 'Ghost Segments (#2D0E10)',
                        'it': lottie_ghost_shapes + [
                            {'ty': 'fl', 'c': {'a': 0, 'k': [45/255.0, 14/255.0, 16/255.0]}, 'o': {'a': 0, 'k': 35.0}, 'nm': 'FlGhost'},
                            {'p': {'a': 0, 'k': [0, 0]}, 'a': {'a': 0, 'k': [0, 0]}, 's': {'a': 0, 'k': [100, 100]}, 'r': {'a': 0, 'k': 0}, 'o': {'a': 0, 'k': 100}, 'ty': 'tr'}
                        ]
                    },
                    {
                        'ty': 'gr', 'nm': 'Active Red Segments (#FF3B30)',
                        'it': lottie_active_shapes + [
                            {'ty': 'fl', 'c': {'a': 0, 'k': C_RED_CORAL}, 'o': {'a': 0, 'k': 100.0}, 'nm': 'FlActive'},
                            {'p': {'a': 0, 'k': [0, 0]}, 'a': {'a': 0, 'k': [0, 0]}, 's': {'a': 0, 'k': [100, 100]}, 'r': {'a': 0, 'k': 0}, 'o': {'a': 0, 'k': 100}, 'ty': 'tr'}
                        ]
                    },
                    {
                        'ty': 'gr', 'nm': 'Inner Highlights (#FFD0D0)',
                        'it': lottie_hl_shapes + [
                            {'ty': 'st', 'c': {'a': 0, 'k': [1.0, 0.816, 0.816]}, 'o': {'a': 0, 'k': 95.0}, 'w': {'a': 0, 'k': 1.0}, 'lc': 2, 'lj': 2, 'nm': 'StHL'},
                            {'p': {'a': 0, 'k': [0, 0]}, 'a': {'a': 0, 'k': [0, 0]}, 's': {'a': 0, 'k': [100, 100]}, 'r': {'a': 0, 'k': 0}, 'o': {'a': 0, 'k': 100}, 'ty': 'tr'}
                        ]
                    },
                    {'p': {'a': 0, 'k': [0, 0]}, 'a': {'a': 0, 'k': [0, 0]}, 's': {'a': 0, 'k': [100, 100]}, 'r': {'a': 0, 'k': 0}, 'o': {'a': 1, 'k': err_op_kf}, 'ty': 'tr'}
                ]
            }
        ],
        'ip': 0, 'op': 120, 'st': 0, 'bm': 0
    }

    markers = [
        {'tm': 0, 'cm': 'error_intro', 'dr': 35},
        {'tm': 35, 'cm': 'error_slump_loop', 'dr': 40},
        {'tm': 75, 'cm': 'error_reboot', 'dr': 45}
    ]

    lottie_dict = {
        'v': '5.7.4', 'fr': 30, 'ip': 0, 'op': 120, 'w': 512, 'h': 512,
        'nm': 'AItuko Error 404 — 100% Fidelity Cyber Porcelain Master Suite',
        'ddd': 0, 'assets': [], 'markers': markers,
        'layers': [
            visor_telemetry_layer,
            eye_layer,
            visor_layer,
            head_layer,
            neck_layer,
            left_foot_layer,
            right_foot_layer,
            left_pod_layer,
            right_pod_layer,
            torso_layer,
            shadow_layer
        ]
    }
    return lottie_dict


def build_animated_svg(points_512):
    """
    Generates standalone pure vector animated SVG with CSS @keyframes:
    - Canonical feet animated and rendered IN FRONT of torso
    - Strictly ZERO floating card
    - Phase 2: Red exclamation marks '!   !'
    - Phase 4: Red digital 7-segment 'ERR'
    - Cyan eyes strictly OFF during error
    """
    svg_pts = {k: points_to_svg_cubic_spline(pts) for k, pts in points_512.items()}
    
    # Option 01: 7-Segments Classique Industriel ('E r r') SVG paths
    glyphs_svg = [
        (214, {'a': True, 'f': True, 'g': True, 'e': True, 'd': True}),
        (244, {'e': True, 'g': True}),
        (274, {'e': True, 'g': True}),
    ]
    ghost_svg_paths = []
    active_svg_paths = []
    hl_svg_paths = []
    for ox, active_dict in glyphs_svg:
        polys = get_7seg_polygons(ox, 105, w=20, h=32, sw=3.8, g=1.0)
        for seg_key, pts in polys.items():
            d_str = "M " + " L ".join(f"{round(x, 1)} {round(y, 1)}" for x, y in pts) + " Z"
            if active_dict.get(seg_key, False):
                active_svg_paths.append(d_str)
                mid_y = 105.0 + 16.0
                if len(pts) == 4:
                    if seg_key in ['b', 'c', 'e', 'f']:
                        mx1, my1 = (pts[0][0] + pts[1][0]) / 2.0, (pts[0][1] + pts[1][1]) / 2.0
                        mx2, my2 = (pts[2][0] + pts[3][0]) / 2.0, (pts[2][1] + pts[3][1]) / 2.0
                    else:
                        mx1, my1 = (pts[0][0] + pts[3][0]) / 2.0, (pts[0][1] + pts[3][1]) / 2.0
                        mx2, my2 = (pts[1][0] + pts[2][0]) / 2.0, (pts[1][1] + pts[2][1]) / 2.0
                    hl_svg_paths.append(f"M {round(mx1, 1)} {round(my1, 1)} L {round(mx2, 1)} {round(my2, 1)}")
                elif len(pts) == 6:
                    x1 = pts[0][0] + 3.8 / 2.0
                    x2 = pts[3][0] - 3.8 / 2.0
                    hl_svg_paths.append(f"M {round(x1, 1)} {round(mid_y, 1)} L {round(x2, 1)} {round(mid_y, 1)}")
            else:
                ghost_svg_paths.append(d_str)

    svg_ghost_d = " ".join(ghost_svg_paths)
    svg_active_d = " ".join(active_svg_paths)
    svg_hl_d = " ".join(hl_svg_paths)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <radialGradient id="shadowGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#000" stop-opacity="0.92"/>
      <stop offset="60%" stop-color="#000" stop-opacity="0.50"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="porcelainGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="35%" stop-color="#FAF8F5"/>
      <stop offset="75%" stop-color="#F2EDE4"/>
      <stop offset="100%" stop-color="#E2DCD2"/>
    </linearGradient>
    <radialGradient id="visorGrad" cx="50%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#181D26"/>
      <stop offset="65%" stop-color="#0E1117"/>
      <stop offset="100%" stop-color="#07090D"/>
    </radialGradient>
    <filter id="cyanGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="coralGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <style>
    @keyframes rootMotion {{
      0%, 16.7% {{ transform: translateY(0px) scale(1, 1); }}
      21.7% {{ transform: translateY(18px) scale(1, 1); }}
      29.2% {{ transform: translateY(72px) scale(1.06, 0.93); }}
      61.7% {{ transform: translateY(72px) scale(1.06, 0.93); }}
      70.0% {{ transform: translateY(0px) scale(1, 1); }}
      100% {{ transform: translateY(0px) scale(1, 1); }}
    }}
    @keyframes headMotion {{
      0%, 16.7% {{ transform: translateY(0px) rotate(0deg); }}
      21.7% {{ transform: translateY(19px) rotate(1.5deg); }}
      29.2% {{ transform: translateY(78px) rotate(3.6deg); }}
      61.7% {{ transform: translateY(78px) rotate(3.6deg); }}
      70.0% {{ transform: translateY(0px) rotate(0deg); }}
      100% {{ transform: translateY(0px) rotate(0deg); }}
    }}
    @keyframes leftPodMotion {{
      0%, 16.7% {{ transform: translate(0px, 0px) rotate(0deg); }}
      21.7% {{ transform: translate(0px, 16px) rotate(2deg); }}
      29.2% {{ transform: translate(-4px, 70px) rotate(14deg); }}
      61.7% {{ transform: translate(-4px, 70px) rotate(14deg); }}
      70.0% {{ transform: translate(0px, 0px) rotate(0deg); }}
      100% {{ transform: translate(0px, 0px) rotate(0deg); }}
    }}
    @keyframes rightPodMotion {{
      0%, 16.7% {{ transform: translate(0px, 0px) rotate(0deg); }}
      21.7% {{ transform: translate(0px, 16px) rotate(-2deg); }}
      29.2% {{ transform: translate(4px, 70px) rotate(-14deg); }}
      61.7% {{ transform: translate(4px, 70px) rotate(-14deg); }}
      70.0% {{ transform: translate(0px, 0px) rotate(0deg); }}
      100% {{ transform: translate(0px, 0px) rotate(0deg); }}
    }}
    @keyframes leftFootMotion {{
      0%, 16.7% {{ transform: translate(0px, 0px) rotate(0deg) scale(1, 1); }}
      21.7% {{ transform: translate(0px, 16px) rotate(0deg) scale(1, 1); }}
      29.2% {{ transform: translate(-8px, 22px) rotate(12deg) scale(1.12, 0.88); }}
      61.7% {{ transform: translate(-8px, 22px) rotate(12deg) scale(1.12, 0.88); }}
      70.0% {{ transform: translate(0px, 0px) rotate(0deg) scale(1, 1); }}
      100% {{ transform: translate(0px, 0px) rotate(0deg) scale(1, 1); }}
    }}
    @keyframes rightFootMotion {{
      0%, 16.7% {{ transform: translate(0px, 0px) rotate(0deg) scale(1, 1); }}
      21.7% {{ transform: translate(0px, 16px) rotate(0deg) scale(1, 1); }}
      29.2% {{ transform: translate(8px, 22px) rotate(-12deg) scale(1.12, 0.88); }}
      61.7% {{ transform: translate(8px, 22px) rotate(-12deg) scale(1.12, 0.88); }}
      70.0% {{ transform: translate(0px, 0px) rotate(0deg) scale(1, 1); }}
      100% {{ transform: translate(0px, 0px) rotate(0deg) scale(1, 1); }}
    }}
    @keyframes shadowMotion {{
      0%, 16.7% {{ transform: scale(1); opacity: 0.53; }}
      21.7% {{ transform: scale(1.05); opacity: 0.59; }}
      29.2% {{ transform: scale(1.35); opacity: 0.92; }}
      61.7% {{ transform: scale(1.35); opacity: 0.92; }}
      70.0% {{ transform: scale(1); opacity: 0.53; }}
      100% {{ transform: scale(1); opacity: 0.53; }}
    }}

    @keyframes eyesOpacity {{
      0%, 16.7% {{ opacity: 1; }}
      17.5% {{ opacity: 0; }}
      66.7% {{ opacity: 0; }}
      67.5% {{ opacity: 1; }}
      85.8% {{ opacity: 1; }}
      87.5% {{ opacity: 0.08; }}
      89.2% {{ opacity: 1; }}
      100% {{ opacity: 1; }}
    }}
    @keyframes exclOpacity {{
      0%, 16.7% {{ opacity: 0; }}
      17.5% {{ opacity: 1; }}
      23.3% {{ opacity: 1; }}
      24.2% {{ opacity: 0; }}
      100% {{ opacity: 0; }}
    }}
    @keyframes errOpacity {{
      0%, 23.3% {{ opacity: 0; }}
      24.2% {{ opacity: 1; }}
      61.7% {{ opacity: 1; }}
      62.5% {{ opacity: 0; }}
      100% {{ opacity: 0; }}
    }}
    .anim-root {{ animation: rootMotion 4s ease-in-out infinite; transform-origin: 256px 312px; }}
    .anim-head {{ animation: headMotion 4s ease-in-out infinite; transform-origin: 256px 204px; }}
    .anim-lpod {{ animation: leftPodMotion 4s ease-in-out infinite; transform-origin: 158px 268px; }}
    .anim-rpod {{ animation: rightPodMotion 4s ease-in-out infinite; transform-origin: 354px 268px; }}
    .anim-lfoot {{ animation: leftFootMotion 4s ease-in-out infinite; transform-origin: 214px 448px; }}
    .anim-rfoot {{ animation: rightFootMotion 4s ease-in-out infinite; transform-origin: 298px 448px; }}
    .anim-shadow {{ animation: shadowMotion 4s ease-in-out infinite; transform-origin: 256px 488px; }}
    .anim-eyes {{ animation: eyesOpacity 4s ease-in-out infinite; }}
    .anim-excl {{ animation: exclOpacity 4s ease-in-out infinite; }}
    .anim-err {{ animation: errOpacity 4s ease-in-out infinite; }}
  </style>

  <!-- Ground Contact Shadow -->
  <g class="anim-shadow">
    <ellipse cx="256" cy="488" rx="95" ry="12" fill="url(#shadowGrad)"/>
  </g>

  <!-- Torso Capsule (Seated Ground Compression) -->
  <g class="anim-root">
    <path d="{svg_pts['torso']}" fill="url(#porcelainGrad)" stroke="#C8C0B2" stroke-width="0.8"/>
  </g>

  <!-- Pod Winglets (Floor Rest beside Body) -->
  <g class="anim-lpod">
    <path d="{svg_pts['left_pod']}" fill="url(#porcelainGrad)" stroke="#C8C0B2" stroke-width="0.8"/>
  </g>
  <g class="anim-rpod">
    <path d="{svg_pts['right_pod']}" fill="url(#porcelainGrad)" stroke="#C8C0B2" stroke-width="0.8"/>
  </g>

  <!-- Canonical Landing Feet Pods (Rendered IN FRONT of Torso per Directive 1!) -->
  <g class="anim-lfoot">
    <path d="{svg_pts['left_foot']}" fill="url(#porcelainGrad)" stroke="#C8C0B2" stroke-width="0.8"/>
  </g>
  <g class="anim-rfoot">
    <path d="{svg_pts['right_foot']}" fill="url(#porcelainGrad)" stroke="#C8C0B2" stroke-width="0.8"/>
  </g>

  <!-- Head & Visor Group -->
  <g class="anim-head">
    <!-- Collar -->
    <ellipse cx="256" cy="204" rx="15" ry="7" fill="#181B26" stroke="#2E3442" stroke-width="0.8"/>
    <!-- Head Dome -->
    <path d="{svg_pts['head']}" fill="url(#porcelainGrad)" stroke="#C8C0B2" stroke-width="0.8"/>
    <!-- Visor Faceplate -->
    <path d="{svg_pts['visor']}" fill="url(#visorGrad)" stroke="#1A1F2B" stroke-width="1.2"/>
    <!-- Electric Cyan Eyes (Active f=0..20, extinguished during error, reignites at f=81) -->
    <g class="anim-eyes" filter="url(#cyanGlow)">
      <path d="{svg_pts['left_eye']}" fill="#00F0FF"/>
      <path d="{svg_pts['right_eye']}" fill="#00F0FF"/>
    </g>
    <!-- Phase 2: Red glowing exclamation marks '!   !' on visor (f=21..28) -->
    <g class="anim-excl" filter="url(#coralGlow)">
      <line x1="221" y1="105" x2="221" y2="120" stroke="#FF3B30" stroke-width="4" stroke-linecap="round"/>
      <circle cx="221" cy="127" r="2.5" fill="#FF3B30"/>
      <line x1="291" y1="105" x2="291" y2="120" stroke="#FF3B30" stroke-width="4" stroke-linecap="round"/>
      <circle cx="291" cy="127" r="2.5" fill="#FF3B30"/>
      <line x1="221" y1="106" x2="221" y2="119" stroke="#FFA099" stroke-width="1.2" stroke-linecap="round"/>
      <line x1="291" y1="106" x2="291" y2="119" stroke="#FFA099" stroke-width="1.2" stroke-linecap="round"/>
    </g>
    <!-- Phase 4: Option 01: 7-Segments Classique Industriel 'E r r' on visor (f=29..74) -->
    <g class="anim-err" filter="url(#coralGlow)">
      <!-- Unlit Ghost Segments (#2D0E10, opacity ~0.35) -->
      <path d="{svg_ghost_d}" fill="#2D0E10" opacity="0.35"/>
      <!-- Active Glowing Red Segments (#FF3B30) -->
      <path d="{svg_active_d}" fill="#FF3B30"/>
      <!-- Bright Coral-White Inner Core Highlights (#FFD0D0) -->
      <path d="{svg_hl_d}" fill="none" stroke="#FFD0D0" stroke-width="1.0" stroke-linecap="round"/>
    </g>
  </g>
</svg>"""
    return svg


def clean_head_component(raw_head):
    """
    Cleans residual turnaround cyan halo from visor faceplate so visor is pure obsidian when eyes are off.
    Directive 3: 'tout doit être en rouge, pas en couleur cyan. C'est une erreur.'
    """
    head = raw_head.copy()
    hsv = cv2.cvtColor(head[:, :, :3], cv2.COLOR_RGB2HSV)
    cyan_mask = (hsv[:, :, 0] >= 75) & (hsv[:, :, 0] <= 110) & (hsv[:, :, 1] >= 40) & (hsv[:, :, 2] >= 30)
    mask_u8 = cv2.dilate(cyan_mask.astype(np.uint8) * 255, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    bgr = cv2.cvtColor(head[:, :, :3], cv2.COLOR_RGB2BGR)
    clean_bgr = cv2.inpaint(bgr, mask_u8, 5, cv2.INPAINT_TELEA)
    hsv_c = cv2.cvtColor(clean_bgr, cv2.COLOR_BGR2HSV)
    box_cyan = (hsv_c[:, :, 0] >= 70) & (hsv_c[:, :, 0] <= 115) & (hsv_c[:, :, 1] >= 25) & (hsv_c[:, :, 2] >= 25)
    clean_bgr[box_cyan] = [26, 18, 14]  # BGR for (14, 18, 26) RGB dark obsidian visor color
    head[:, :, :3] = cv2.cvtColor(clean_bgr, cv2.COLOR_BGR2RGB)
    return head


def render_error_404_frame(f, master_components, backdrop=None):
    """
    Renders high-definition, pixel-perfect 512x512 RGBA frame for frame f strictly adhering to directives:
    - Zero external foot cut textures (uses canonical master_components['lfoot'] and ['rfoot'] only)
    - Feet rendered IN FRONT OF slumped torso on the floor plane
    - Visor telemetry: 100% RED — ZERO CYAN during error
    - Phase 2: Red glowing exclamation marks '!   !'
    - Phase 4: Red digital 7-segment 'ERR' with subtle bloom and inner highlight
    - Strictly ZERO floating card
    """
    k = get_error_404_kinematics(f)
    canvas = Image.new('RGBA', (512, 512), backdrop if backdrop is not None else (0, 0, 0, 0))
    p = k['p_seated']

    # 1. Soft Studio Ambient Occlusion Ground Shadow (canonical floor plane y = 488)
    sh_layer = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(sh_layer)
    cy_floor = 488
    rx_main = int(120 * k['shadow_s'])
    ry_main = int(14 * k['shadow_s'])
    sh_draw.ellipse([256 - rx_main, cy_floor - ry_main, 256 + rx_main, cy_floor + ry_main], fill=(0, 0, 0, int(k['shadow_a'] * 0.5)))
    if p > 0.05:
        # Seated ground contact occlusion:
        # Directive 2: dense contact occlusion ellipse right under the rounded base of the torso (x in [200, 312], y in [482, 494]) and under the feet.
        cy_torso_occ = int(488 * p + cy_floor * (1.0 - p))
        # Torso contact occlusion (x in [200, 312], y in [482, 494])
        sh_draw.ellipse([256 - int(56 * p), cy_torso_occ - int(6 * p), 256 + int(56 * p), cy_torso_occ + int(6 * p)], fill=(0, 0, 0, int(160 * p)))
        # Option Idéale feet contact occlusion (left foot x=206, right foot x=306)
        sh_draw.ellipse([206 - int(28 * p), cy_floor - int(7 * p), 206 + int(28 * p), cy_floor + int(7 * p)], fill=(0, 0, 0, int(150 * p)))
        sh_draw.ellipse([306 - int(28 * p), cy_floor - int(7 * p), 306 + int(28 * p), cy_floor + int(7 * p)], fill=(0, 0, 0, int(150 * p)))
        # Lateral pods contact occlusion (left pod x=154, right pod x=358)
        cy_pod_occ = int(472 * p + cy_floor * (1.0 - p))
        sh_draw.ellipse([154 - int(18 * p), cy_pod_occ - int(5 * p), 154 + int(18 * p), cy_pod_occ + int(5 * p)], fill=(0, 0, 0, int(90 * p)))
        sh_draw.ellipse([358 - int(18 * p), cy_pod_occ - int(5 * p), 358 + int(18 * p), cy_pod_occ + int(5 * p)], fill=(0, 0, 0, int(90 * p)))
    sh_blur = int(round(5.0 + 2.0 * p))
    sh_layer = sh_layer.filter(ImageFilter.GaussianBlur(radius=sh_blur))
    canvas.alpha_composite(sh_layer)

    torso_comp = master_components["torso"]
    if not hasattr(render_error_404_frame, "_cleaned_head"):
        render_error_404_frame._cleaned_head = clean_head_component(master_components["head"])
    head_comp = render_error_404_frame._cleaned_head
    lpod_comp = master_components["lpod"]
    rpod_comp = master_components["rpod"]
    lfoot_comp = master_components["lfoot"]
    rfoot_comp = master_components["rfoot"]

    # 2. Porcelain Torso Capsule (Firmly Grounded on Floor Plane)
    torso_pivot = (256.0, 314.0)
    w_torso = transform_rgba(torso_comp, torso_pivot, angle_deg=0.0,
                             scale=(k['scale_torso_x'], k['scale_torso_y']), translate=(0.0, k['dy_root']))
    canvas.alpha_composite(Image.fromarray(w_torso))

    # 3. Lateral Pods (resting down beside body on floor when seated)
    w_lpod = transform_rgba(lpod_comp, (146.0, 321.0), angle_deg=k['rot_lpod'],
                            scale=(1.0 - 0.05 * p, 1.0 - 0.05 * p),
                            translate=(k['dx_lpod'], k['dy_pods']))
    canvas.alpha_composite(Image.fromarray(w_lpod))

    w_rpod = transform_rgba(rpod_comp, (365.0, 320.0), angle_deg=k['rot_rpod'],
                            scale=(1.0 - 0.05 * p, 1.0 - 0.05 * p),
                            translate=(k['dx_rpod'], k['dy_pods']))
    canvas.alpha_composite(Image.fromarray(w_rpod))

    # 4. Canonical Feet (Option Idéale: Rendered IN FRONT of the slumped torso per Directive 1!)
    feet_pivot_l = (214.0, 448.0)
    feet_pivot_r = (298.0, 448.0)
    w_lfoot = transform_rgba(lfoot_comp, feet_pivot_l, angle_deg=k['rot_lfoot'],
                             scale=(k['scale_feet_x'], k['scale_feet_y']),
                             translate=(k['dx_lfoot'], k['dy_feet']))
    w_rfoot = transform_rgba(rfoot_comp, feet_pivot_r, angle_deg=k['rot_rfoot'],
                             scale=(k['scale_feet_x'], k['scale_feet_y']),
                             translate=(k['dx_rfoot'], k['dy_feet']))
    canvas.alpha_composite(Image.fromarray(w_lfoot))
    canvas.alpha_composite(Image.fromarray(w_rfoot))

    # 5. Mechanical Neck Collar Socket (visible when floating, hidden by chin when seated)
    if p < 0.8:
        neck_layer = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
        neck_cy = int(204.0 + k['dy_head'])
        ImageDraw.Draw(neck_layer).ellipse([256 - 15, neck_cy - 7, 256 + 15, neck_cy + 7], fill=(24, 27, 38, int(255 * (1.0 - p))))
        canvas.alpha_composite(neck_layer)

    # 6. Porcelain Head Dome & Obsidian Visor (Empathetic forward bow, chin covers neck ring)
    head_pivot = (256.0, 124.0)
    w_head = transform_rgba(head_comp, head_pivot, angle_deg=k['rot_head'],
                            scale=(1.0 + 0.04 * p, 1.0 + 0.04 * p), translate=(0.0, k['dy_head'] + 4.0 * p))
    canvas.alpha_composite(Image.fromarray(w_head))

    # 7. Visor Displays (Cyan Eyes, Red '! !' alert, Red 7-segment 'ERR')
    # Directive 3: 100% RED — ZERO CYAN DURING ERROR
    layer_visor = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
    dv = ImageDraw.Draw(layer_visor)

    # A. Smiling Cyan Eyes (^ ^) / Settle blink (ONLY active when eye_opacity > 0)
    if k['eye_opacity'] > 0.05:
        if k['scale_eye_y'] <= 0.2:
            dv.line([(204, 120), (238, 120)], fill=(0, 240, 255, int(255 * k['eye_opacity'])), width=3)
            dv.line([(274, 120), (308, 120)], fill=(0, 240, 255, int(255 * k['eye_opacity'])), width=3)
        else:
            w_eyes = transform_rgba(master_components["eyes"], (256.0, 120.34), angle_deg=0.0,
                                    scale=(1.0, k['scale_eye_y']), translate=(0.0, 0.0))
            w_eyes = w_eyes.copy()
            w_eyes[:, :, 3] = (w_eyes[:, :, 3].astype(float) * k['eye_opacity']).astype(np.uint8)
            e_im = Image.fromarray(w_eyes)
            layer_visor.paste(e_im, (0, 0), e_im)

    # B. Phase 2 (f=21..28): Red glowing exclamation marks '!   !'
    if k['excl_opacity'] > 0.05:
        ex_op = k['excl_opacity']
        c_red = (255, 59, 48, int(255 * ex_op))
        c_hl = (255, 190, 185, int(230 * ex_op))
        # Left !
        dv.line([(221, 105), (221, 120)], fill=c_red, width=4)
        dv.ellipse([221 - 2.5, 127 - 2.5, 221 + 2.5, 127 + 2.5], fill=c_red)
        # Right !
        dv.line([(291, 105), (291, 120)], fill=c_red, width=4)
        dv.ellipse([291 - 2.5, 127 - 2.5, 291 + 2.5, 127 + 2.5], fill=c_red)
        # Inner highlights
        dv.line([(221, 106), (221, 119)], fill=c_hl, width=1)
        dv.line([(291, 106), (291, 119)], fill=c_hl, width=1)

    # C. Phase 4 (f=29..74): Option 01: 7-Segments Classique Industriel ('E r r')
    if k['err_opacity'] > 0.05:
        e_op = k['err_opacity']
        c_on = (255, 59, 48, int(round(255 * e_op)))
        c_off = (45, 14, 16, int(round(90 * e_op)))  # #2D0E10 with opacity ~0.35
        c_hl = (255, 208, 208, int(round(240 * e_op)))  # #FFD0D0 inner core highlight

        e_segs = {'a': True, 'f': True, 'g': True, 'e': True, 'd': True}
        r_segs = {'e': True, 'g': True}

        # Authentic 7-segment chamfered glyphs centered on visor at y in [105, 137]
        draw_7seg_glyph(dv, e_segs, 214, 105, w=20, h=32, sw=3.8, g=1.0, col_on=c_on, col_off=c_off, col_hl=c_hl)
        draw_7seg_glyph(dv, r_segs, 244, 105, w=20, h=32, sw=3.8, g=1.0, col_on=c_on, col_off=c_off, col_hl=c_hl)
        draw_7seg_glyph(dv, r_segs, 274, 105, w=20, h=32, sw=3.8, g=1.0, col_on=c_on, col_off=c_off, col_hl=c_hl)

    w_visor = transform_rgba(np.array(layer_visor), head_pivot, angle_deg=k['rot_head'],
                             scale=(1.0 + 0.04 * p, 1.0 + 0.04 * p), translate=(0.0, k['dy_head'] + 4.0 * p))
    im_v = Image.fromarray(w_visor)
    canvas.alpha_composite(im_v.filter(ImageFilter.GaussianBlur(2)))
    canvas.alpha_composite(im_v)

    # Directive 3: Infill any residual cyan pixels during error with obsidian dark visor color (14, 18, 26)
    if k['eye_opacity'] < 0.05:
        c_arr = np.array(canvas)
        hsv_check = cv2.cvtColor(c_arr[:, :, :3], cv2.COLOR_RGB2HSV)
        cyan_mask = (hsv_check[:, :, 0] >= 75) & (hsv_check[:, :, 0] <= 110) & (hsv_check[:, :, 1] >= 40) & (hsv_check[:, :, 2] >= 40) & (c_arr[:, :, 3] > 30)
        if np.any(cyan_mask):
            c_arr[cyan_mask, 0] = 14
            c_arr[cyan_mask, 1] = 18
            c_arr[cyan_mask, 2] = 26
            canvas = Image.fromarray(c_arr)

    return canvas



def generate_all_error_404_deliverables():
    print("================================================================")
    print("🚀 PRODUCING MASTER DELIVERABLES: AItuko Error 404 (04_error_404)")
    print("================================================================")
    
    output_dir = os.path.join(WORKSPACE_DIR, "assets/04_error_404")
    mascots_dir = os.path.join(WORKSPACE_DIR, "mascots/aituko")
    aituko_dir = os.path.join(WORKSPACE_DIR, "aituko/assets/04_error_404")
    mascots_assets_dir = os.path.join(WORKSPACE_DIR, "mascots/aituko/assets/04_error_404")
    downloads_dir = os.path.join(WORKSPACE_DIR, "downloads")
    
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(mascots_dir, exist_ok=True)
    os.makedirs(aituko_dir, exist_ok=True)
    os.makedirs(mascots_assets_dir, exist_ok=True)
    os.makedirs(downloads_dir, exist_ok=True)
    
    _, points_512 = get_calibrated_master_splines()
    master_comps = load_master_components()

    # 1. Pure Vector Lottie JSON
    print("📦 [1/8] Generating Pure Vector Lottie JSON (< 50 KB)...")
    lottie_dict = build_pure_vector_lottie(points_512)
    lottie_path = os.path.join(output_dir, "lottie.json")
    with open(lottie_path, "w", encoding="utf-8") as f:
        json.dump(lottie_dict, f, separators=(',', ':'))
    size_kb = os.path.getsize(lottie_path) / 1024.0
    print(f"  ✅ Lottie JSON: {size_kb:.2f} KB (Strict limit: < 50.0 KB)")
    assert size_kb < 50.0, f"Lottie file size {size_kb:.2f} KB exceeds 50.0 KB limit!"
    shutil.copy2(lottie_path, os.path.join(mascots_dir, "aituko_error_404_vector.json"))

    # 2. Animated SVG
    print("🎨 [2/8] Generating CSS-Keyframe Animated SVG...")
    svg_str = build_animated_svg(points_512)
    svg_path = os.path.join(output_dir, "animated.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_str)
    shutil.copy2(svg_path, os.path.join(mascots_dir, "aituko_error_404_animated.svg"))
    print(f"  ✅ Animated SVG saved ({os.path.getsize(svg_path)/1024.0:.1f} KB)")

    # 3. Render 120 Frames
    print("🎬 [3/8] Rendering 120 Ultra-Crisp Frames (30 FPS, 4.0s loop)...")
    frames_rgba = []
    frames_dark = []
    frames_green = []
    
    for f_idx in range(TOTAL_FRAMES):
        fr_rgba = render_error_404_frame(f_idx, master_comps, backdrop=None)
        frames_rgba.append(fr_rgba)
        
        fr_dark = render_error_404_frame(f_idx, master_comps, backdrop=COLOR_BG_DARK)
        frames_dark.append(fr_dark)
        
        fr_green = render_error_404_frame(f_idx, master_comps, backdrop=COLOR_BG_GREEN)
        frames_green.append(fr_green)
        
        if f_idx % 30 == 0:
            print(f"  ... frame {f_idx}/{TOTAL_FRAMES} rendered")
            
    print("  ✅ All 120 frames rendered successfully across 3 color profiles")

    # 4. Animated WebP (Transparent)
    print("🌐 [4/8] Assembling High-Fidelity Animated WebP...")
    webp_path = os.path.join(output_dir, "animated.webp")
    frames_rgba[0].save(
        webp_path,
        save_all=True,
        append_images=frames_rgba[1:],
        duration=int(1000 / FPS),
        loop=0,
        quality=95,
        method=4
    )
    shutil.copy2(webp_path, os.path.join(mascots_dir, "aituko_error_404.webp"))
    print(f"  ✅ Animated WebP: {os.path.getsize(webp_path)/1024.0:.1f} KB")

    # 5. Animated GIFs (Transparent, Dark, Chroma Green)
    print("🎞️ [5/8] Assembling Multi-Backdrop Animated GIFs...")
    gif_path = os.path.join(output_dir, "animated.gif")
    frames_rgba[0].save(
        gif_path,
        save_all=True,
        append_images=frames_rgba[1:],
        duration=int(1000 / FPS),
        loop=0,
        disposal=2
    )
    gif_dark_path = os.path.join(output_dir, "animated_dark.gif")
    frames_dark[0].save(
        gif_dark_path,
        save_all=True,
        append_images=frames_dark[1:],
        duration=int(1000 / FPS),
        loop=0
    )
    gif_green_path = os.path.join(output_dir, "animated_green.gif")
    frames_green[0].save(
        gif_green_path,
        save_all=True,
        append_images=frames_green[1:],
        duration=int(1000 / FPS),
        loop=0
    )
    print("  ✅ GIFs generated: transparent, dark studio, chroma green")

    # 6. Looped MP4 Video
    print("🎥 [6/8] Encoding H.264 MP4 Video...")
    mp4_path = os.path.join(output_dir, "looped_video.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    vw = cv2.VideoWriter(mp4_path, fourcc, FPS, (512, 512))
    for fr in frames_dark:
        vw.write(cv2.cvtColor(np.array(fr), cv2.COLOR_RGBA2BGR))
    vw.release()
    shutil.copy2(mp4_path, os.path.join(mascots_dir, "aituko_error_404.mp4"))
    shutil.copy2(mp4_path, os.path.join(mascots_dir, "looped_video.mp4"))
    shutil.copy2(mp4_path, os.path.join(WORKSPACE_DIR, "aituko/aituko_error_404.mp4"))
    shutil.copy2(webp_path, os.path.join(WORKSPACE_DIR, "aituko/aituko_error_404.webp"))
    print(f"  ✅ Looped MP4: {os.path.getsize(mp4_path)/1024.0:.1f} KB")

    # 6b. Static Hero Poster & Animated PNG (APNG)
    print("🖼️ [6b/8] Generating Static Hero Frame & Animated PNG...")
    static_png_path = os.path.join(output_dir, "static.png")
    frames_rgba[55].save(static_png_path, "PNG", optimize=True)
    static_webp_path = os.path.join(output_dir, "static.webp")
    frames_rgba[55].save(static_webp_path, "WEBP", quality=95)
    shutil.copy2(static_png_path, os.path.join(mascots_dir, "aituko_error_404_static.png"))
    shutil.copy2(static_png_path, os.path.join(mascots_dir, "static.png"))
    shutil.copy2(static_webp_path, os.path.join(mascots_dir, "aituko_error_404_static.webp"))
    shutil.copy2(static_webp_path, os.path.join(mascots_dir, "static.webp"))

    apng_path = os.path.join(output_dir, "animated.png")
    frames_rgba[0].save(
        apng_path,
        save_all=True,
        append_images=frames_rgba[1:],
        duration=int(1000 / FPS),
        loop=0
    )
    print(f"  ✅ Static hero poster (f=55) and APNG generated ({os.path.getsize(apng_path)/1024.0:.1f} KB)")

    # 7. Presentation Master Boards
    print("🖼️ [7/8] Generating Presentation Master Boards...")
    kf_names = [
        ("01_nominal_levitation", "01 — Sustentation Nominale (t = 0.0s)", 0),
        ("02_shock_stutter", "02 — Alerte Immédiate '! !' (t = 0.83s)", 25),
        ("03_grounded_slump_err", "03 — Posture Assise & Télémétrie 'ERR' (t = 1.83s)", 55),
        ("04_reboot_ascent", "04 — Reboot Système & Redécollage (t = 2.73s)", 82)
    ]
    
    for fname, title, idx in kf_names:
        img_dark = frames_dark[idx]
        p_img = os.path.join(output_dir, f"keyframe_{fname}.png")
        img_dark.save(p_img)
        shutil.copy2(p_img, os.path.join(mascots_dir, f"aituko_error_404_{fname}.png"))
        if "grounded_slump" in fname:
            p_404 = os.path.join(output_dir, "keyframe_03_grounded_slump_404.png")
            img_dark.save(p_404)
            shutil.copy2(p_404, os.path.join(mascots_dir, "aituko_error_404_03_grounded_slump_404.png"))

    # Master Presentation Board (1920x1080)
    master_board = Image.new('RGBA', (1920, 1080), (11, 15, 23, 255))
    b_draw = ImageDraw.Draw(master_board)

    font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
    if not os.path.exists(font_path):
        font_path = "/System/Library/Fonts/Helvetica.ttc"
    
    font_header = ImageFont.truetype(font_path, 28)
    font_sub = ImageFont.truetype(font_path, 18)
    font_card_title = ImageFont.truetype(font_path, 17)
    font_card_desc = ImageFont.truetype(font_path, 14)
    font_specs_head = ImageFont.truetype(font_path, 18)
    font_specs_body = ImageFont.truetype(font_path, 15)

    b_draw.text((80, 45), "AITUKO STATE 04 — ERROR 404 MASTER SUITE (100% STUDIO FIDELITY)", font=font_header, fill=(255, 255, 255, 255))
    b_draw.text((80, 85), "Architecture 100% Conforme : Mascotte Fermement au Sol (Option Idéale) + Télémétrie Visière 100% Rouge ('! !' & 'ERR')", font=font_sub, fill=(0, 240, 255, 255))
    
    card_w, card_h = 420, 420
    start_x = 75
    gap_x = 45
    card_y = 145
    
    for i, (fname, title, idx) in enumerate(kf_names):
        x = start_x + i * (card_w + gap_x)
        b_draw.rounded_rectangle([x, card_y, x + card_w, card_y + card_h + 120], radius=16, fill=(18, 24, 38, 255), outline=(35, 45, 68, 255), width=2)
        kf_crop = frames_dark[idx].resize((card_w - 20, card_h - 20), Image.Resampling.LANCZOS)
        master_board.paste(kf_crop, (x + 10, card_y + 10))
        b_draw.text((x + 18, card_y + card_h + 20), title, font=font_card_title, fill=(240, 245, 255, 255))
        if i == 0:
            desc = "Lévitation équilibrée, yeux cyan souriants (^ ^)."
        elif i == 1:
            desc = "Propulseurs coupés, yeux d'alerte '! !' rouge-corail, amorce chute."
        elif i == 2:
            desc = "Tronc au sol (dy=72px), pieds Option Idéale (+12°/-12°), télémétrie 7-segments 'E r r'."
        else:
            desc = "Reboot système, yeux cyan (^ ^) ré-allumés, redécollage ascendant."
        b_draw.text((x + 18, card_y + card_h + 52), desc, font=font_card_desc, fill=(148, 163, 184, 255))

    specs_y = 795
    b_draw.rounded_rectangle([75, specs_y, 1845, 1020], radius=16, fill=(15, 20, 32, 255), outline=(30, 40, 60, 255), width=1)
    b_draw.text((105, specs_y + 22), "SPÉCIFICATIONS TECHNIQUES DE VALIDATION (100% FIDÉLITÉ STUDIO)", font=font_specs_head, fill=(0, 240, 255, 255))
    
    specs = [
        "• Posture Assise 100% Fidèle : Tronc au sol (dy=72px, base à y=485..487px), pieds Option Idéale (+12° / -12°) en avant du torse, ailerons au sol.",
        "• Télémétrie Visière 100% Rouge : Points d'exclamation '! !' (f=21..28), puis Option 01 7-segments 'E r r' avec segments biseautés et fantômes (f=29..74).",
        "• Zéro Asset Externe / Zéro Carte Flottante : Composants canoniques stricts, affichage 100% diégétique dans l'écran de la visière.",
        f"• Format Lottie Vectoriel : {size_kb:.2f} Ko (strictement < 50 Ko), 120 frames @ 30 FPS, continuité C1 parfaite avec markers Bodymovin.",
        "• Shading Porcelaine Authentique : Céramique crème (#FAF8F5 / #F2EDE4) avec reflets spéculaires zénithaux, zéro cyan corporel."
    ]

    for s_idx, sp in enumerate(specs):
        b_draw.text((105, specs_y + 58 + s_idx * 28), sp, font=font_specs_body, fill=(203, 213, 225, 255))
        
    master_board_path = os.path.join(output_dir, "aituko_error_404_master_board.png")
    master_board.save(master_board_path)
    shutil.copy2(master_board_path, os.path.join(mascots_dir, "aituko_error_404_master_board.png"))
    print(f"  ✅ Master Board saved: {master_board_path}")

    # Trichrome Inspection Board (1536x512)
    tri_board = Image.new('RGBA', (1536, 512), (11, 15, 23, 255))
    f55_white = render_error_404_frame(55, master_comps, backdrop=COLOR_BG_WHITE)
    f55_dark = frames_dark[55]
    f55_green = frames_green[55]
    tri_board.paste(f55_white, (0, 0))
    tri_board.paste(f55_dark, (512, 0))
    tri_board.paste(f55_green, (1024, 0))
    
    font_tri = ImageFont.truetype(font_path, 20)
    tri_draw = ImageDraw.Draw(tri_board)
    tri_draw.text((30, 30), "STUDIO WHITE", font=font_tri, fill=(15, 20, 28, 255))
    tri_draw.text((512 + 30, 30), "STUDIO DARK", font=font_tri, fill=(255, 255, 255, 255))
    tri_draw.text((1024 + 30, 30), "CHROMA GREEN", font=font_tri, fill=(0, 0, 0, 255))
    
    tri_path = os.path.join(output_dir, "aituko_error_404_studio_trichroma_board.png")
    tri_board.save(tri_path)
    shutil.copy2(tri_path, os.path.join(mascots_dir, "aituko_error_404_studio_trichroma_board.png"))
    print(f"  ✅ Trichrome Board saved: {tri_path}")

    # Side-by-Side Comparison Board (Reference f=48 vs Render f=55)
    ref_path = os.path.join(WORKSPACE_DIR, "scratch/true_studio_error_frames/f_048.png")
    if os.path.exists(ref_path):
        ref_img = cv2.imread(ref_path)
        h_ref, w_ref = ref_img.shape[:2]
        ref_crop = ref_img[int(h_ref*0.08):int(h_ref*0.92), int(w_ref*0.35):int(w_ref*0.65)]
        ref_512 = cv2.resize(ref_crop, (512, 512))
        rnd_arr = np.array(f55_white)[:, :, :3]
        rnd_bgr = cv2.cvtColor(rnd_arr, cv2.COLOR_RGB2BGR)
        side_by_side = np.hstack([ref_512, rnd_bgr])
        cv2.putText(side_by_side, "3D STUDIO REFERENCE", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        cv2.putText(side_by_side, "AITUKO MASTER RENDER (100% FIDELE)", (532, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 180, 0), 2)
        
        comp_path = os.path.join(output_dir, "seated_f55_comparison.png")
        cv2.imwrite(comp_path, side_by_side)
        shutil.copy2(comp_path, os.path.join(mascots_dir, "seated_f55_comparison.png"))
        
        for b_dir in BRAIN_DIRS:
            if os.path.exists(b_dir):
                cv2.imwrite(os.path.join(b_dir, "seated_f55_comparison.png"), side_by_side)
        print("  ✅ Side-by-side comparison board generated & synchronized")

    # 8. Zip Deliverables Bundle & Brain Sync
    print("📦 [8/8] Packaging Deliverables ZIP & Synchronizing Brain...")
    zip_path = os.path.join(output_dir, "aituko_error_404_bundle.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(output_dir):
            for file in files:
                if file.endswith('.zip'): continue
                full_p = os.path.join(root, file)
                rel_p = os.path.relpath(full_p, output_dir)
                zipf.write(full_p, rel_p)
    shutil.copy2(zip_path, os.path.join(downloads_dir, "aituko_error_404_bundle.zip"))
    shutil.copy2(zip_path, os.path.join(downloads_dir, "bundle_aituko_04_error_404.zip"))
    shutil.copy2(zip_path, os.path.join(output_dir, "bundle_aituko_04_error_404.zip"))
    shutil.copy2(zip_path, os.path.join(aituko_dir, "bundle_aituko_04_error_404.zip"))

    # Sync complete suite to aituko_dir
    shutil.copy2(lottie_path, os.path.join(aituko_dir, "lottie.json"))
    shutil.copy2(svg_path, os.path.join(aituko_dir, "animated.svg"))
    shutil.copy2(webp_path, os.path.join(aituko_dir, "animated.webp"))
    shutil.copy2(gif_path, os.path.join(aituko_dir, "animated.gif"))
    shutil.copy2(apng_path, os.path.join(aituko_dir, "animated.png"))
    shutil.copy2(mp4_path, os.path.join(aituko_dir, "looped_video.mp4"))
    shutil.copy2(static_png_path, os.path.join(aituko_dir, "static.png"))
    shutil.copy2(static_webp_path, os.path.join(aituko_dir, "static.webp"))

    # Sync mascots_dir standard names
    shutil.copy2(lottie_path, os.path.join(mascots_dir, "lottie.json"))
    shutil.copy2(gif_path, os.path.join(mascots_dir, "animated.gif"))
    shutil.copy2(gif_dark_path, os.path.join(mascots_dir, "animated_dark.gif"))
    shutil.copy2(gif_green_path, os.path.join(mascots_dir, "animated_green.gif"))
    shutil.copy2(apng_path, os.path.join(mascots_dir, "animated.png"))

    # Sync complete suite to mascots/aituko/assets/04_error_404
    shutil.copy2(lottie_path, os.path.join(mascots_assets_dir, "lottie.json"))
    shutil.copy2(svg_path, os.path.join(mascots_assets_dir, "animated.svg"))
    shutil.copy2(webp_path, os.path.join(mascots_assets_dir, "animated.webp"))
    shutil.copy2(gif_path, os.path.join(mascots_assets_dir, "animated.gif"))
    shutil.copy2(apng_path, os.path.join(mascots_assets_dir, "animated.png"))
    shutil.copy2(mp4_path, os.path.join(mascots_assets_dir, "looped_video.mp4"))
    shutil.copy2(mp4_path, os.path.join(mascots_assets_dir, "source_video.mp4"))
    shutil.copy2(static_png_path, os.path.join(mascots_assets_dir, "static.png"))
    shutil.copy2(static_webp_path, os.path.join(mascots_assets_dir, "static.webp"))
    shutil.copy2(zip_path, os.path.join(mascots_assets_dir, "bundle_aituko_04_error_404.zip"))
    shutil.copy2(master_board_path, os.path.join(mascots_assets_dir, "aituko_error_404_master_board.png"))
    shutil.copy2(tri_path, os.path.join(mascots_assets_dir, "aituko_error_404_studio_trichroma_board.png"))
    comp_src = os.path.join(output_dir, "seated_f55_comparison.png")
    if os.path.exists(comp_src):
        shutil.copy2(comp_src, os.path.join(mascots_assets_dir, "seated_f55_comparison.png"))

    # Prepare updated walkthrough.md and aituko_visual_render.md
    wt_path = os.path.join(output_dir, "walkthrough.md")
    vr_path = os.path.join(output_dir, "aituko_visual_render.md")
    
    import re
    wt_content = ""
    if os.path.exists(wt_path):
        with open(wt_path, "r", encoding="utf-8") as f:
            wt_content = f.read()
        wt_content = re.sub(r'(\*\*)\d+\.\d+\s*K[oB](\*\*\s*\([^\)]*<\s*50)', rf'\g<1>{size_kb:.2f} Ko\g<2>', wt_content)
        with open(wt_path, "w", encoding="utf-8") as f:
            f.write(wt_content)

    vr_content = ""
    if os.path.exists(vr_path):
        with open(vr_path, "r", encoding="utf-8") as f:
            vr_content = f.read()
        vr_content = re.sub(r'(\*\*)\d+\.\d+\s*K[oB](\*\*\s*\([^\)]*<\s*50)', rf'\g<1>{size_kb:.2f} Ko\g<2>', vr_content)
        with open(vr_path, "w", encoding="utf-8") as f:
            f.write(vr_content)

    all_target_brain_dirs = get_all_brain_dirs()
    for b_dir in all_target_brain_dirs:
        os.makedirs(b_dir, exist_ok=True)
        shutil.copy2(lottie_path, os.path.join(b_dir, "aituko_error_404_vector.json"))
        shutil.copy2(lottie_path, os.path.join(b_dir, "lottie.json"))
        shutil.copy2(svg_path, os.path.join(b_dir, "aituko_error_404_animated.svg"))
        shutil.copy2(svg_path, os.path.join(b_dir, "animated.svg"))
        shutil.copy2(webp_path, os.path.join(b_dir, "aituko_error_404.webp"))
        shutil.copy2(webp_path, os.path.join(b_dir, "animated.webp"))
        shutil.copy2(gif_path, os.path.join(b_dir, "aituko_error_404_animated.gif"))
        shutil.copy2(gif_path, os.path.join(b_dir, "animated.gif"))
        shutil.copy2(gif_dark_path, os.path.join(b_dir, "aituko_error_404_animated_dark.gif"))
        shutil.copy2(gif_dark_path, os.path.join(b_dir, "animated_dark.gif"))
        shutil.copy2(gif_green_path, os.path.join(b_dir, "aituko_error_404_animated_green.gif"))
        shutil.copy2(gif_green_path, os.path.join(b_dir, "animated_green.gif"))
        shutil.copy2(mp4_path, os.path.join(b_dir, "aituko_error_404.mp4"))
        shutil.copy2(mp4_path, os.path.join(b_dir, "looped_video.mp4"))
        shutil.copy2(static_png_path, os.path.join(b_dir, "static.png"))
        shutil.copy2(static_png_path, os.path.join(b_dir, "aituko_error_404_static.png"))
        shutil.copy2(static_webp_path, os.path.join(b_dir, "static.webp"))
        shutil.copy2(static_webp_path, os.path.join(b_dir, "aituko_error_404_static.webp"))
        shutil.copy2(master_board_path, os.path.join(b_dir, "aituko_error_404_master_board.png"))
        shutil.copy2(tri_path, os.path.join(b_dir, "aituko_error_404_studio_trichroma_board.png"))
        if os.path.exists(comp_src):
            shutil.copy2(comp_src, os.path.join(b_dir, "seated_f55_comparison.png"))
        if wt_content:
            with open(os.path.join(b_dir, "walkthrough.md"), "w", encoding="utf-8") as f:
                f.write(wt_content)
        if vr_content:
            with open(os.path.join(b_dir, "aituko_visual_render.md"), "w", encoding="utf-8") as f:
                f.write(vr_content)
        for fname, _, _ in kf_names:
            p_src = os.path.join(output_dir, f"keyframe_{fname}.png")
            if os.path.exists(p_src):
                shutil.copy2(p_src, os.path.join(b_dir, f"aituko_error_404_{fname}.png"))
        # Legacy alias
        p_404 = os.path.join(output_dir, "keyframe_03_grounded_slump_404.png")
        if os.path.exists(p_404):
            shutil.copy2(p_404, os.path.join(b_dir, "aituko_error_404_03_grounded_slump_404.png"))

    # Rebuild global download zip packages
    try:
        from scripts.rebuild_all_zip_packages import build_all
        build_all()
    except Exception as e:
        print(f"  ⚠️ Warning rebuilding zip packages: {e}")

    shutil.copy2(zip_path, os.path.join(downloads_dir, "aituko_error_404_bundle.zip"))
    shutil.copy2(zip_path, os.path.join(downloads_dir, "bundle_aituko_04_error_404.zip"))

    print("================================================================")
    print("🎉 PRODUCTION COMPLETE: AItuko Error 404 Successfully Generated!")
    print(f"  • Lottie Vector JSON : {lottie_path} ({size_kb:.2f} KB)")
    print(f"  • Animated SVG       : {svg_path}")
    print(f"  • Animated WebP      : {webp_path}")
    print(f"  • Master Board       : {master_board_path}")
    print(f"  • Deliverables ZIP   : {zip_path}")
    print("================================================================")


if __name__ == "__main__":
    generate_all_error_404_deliverables()
