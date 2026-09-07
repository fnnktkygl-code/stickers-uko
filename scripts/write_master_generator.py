import sys

script_content = r'''#!/usr/bin/env python3
"""
AItuko High-Fidelity Vector Lottie Generator (13 States)
Conforms strictly to Bodymovin / LottieFiles v5.7+ JSON specification.
100% resolution-independent vector shapes, cubic-bezier easing kinematics,
and exact 3D porcelain character fidelity matching the official 3D master turnaround.

Dimensions & Coordinates (Measured from 3D Master on 512x512 canvas):
- Center X = 256
- Ground Shadow: Center (256, 495), width 180, height 26.
- Support Pods (Feet): X = 211 & 301 (offset ±45), Y = 479, width 54, height 58, tilt ±8°.
- Porcelain Torso: Center (256, 315), width 206, height 265, roundness 88.
- Neck AO Shadow: Center (256, 183), width 95, height 18.
- Porcelain Head: Center (256, 99), width 245, height 187, roundness 75.
- Visor Faceplate: Center (256, 99), width 197, height 147, roundness 65.
- Electric Cyan Eyes: Center (211, 99) & (301, 99) (offset ±45), width 48, height 31.
- Floating Arms: Rest X = 132 & 380 (offset ±124), Y = 333, width 54, height 138, roundness 27.

Kinematic Specification (from 96-frame tracking of aituko_idle.mp4):
- 120-frame (4.0s @ 30fps) seamless harmonic loop.
- Sinusoidal floating: Apex at frame 27 (-18px), Nadir at frame 84 (+16px).
- Inertial Arm Flaring: Arm span widens by +12px at apex, tucks in at nadir; tilt ±7° to ±12°.
- Inertial Head Tilt: 4-frame phase lag, pitch ±2.2°.
- Dynamic Shadow Coupling: Scale 82% & opacity 55% at apex <-> scale 108% & opacity 98% at nadir.
- Natural Organic Blinking: Double-blink at frames 78-86 during nadir turnaround.
"""

import json
import os
import math
import copy

def hex_to_lottie_color(hex_str, alpha=1.0):
    hex_str = hex_str.lstrip("#")
    r = int(hex_str[0:2], 16) / 255.0
    g = int(hex_str[2:4], 16) / 255.0
    b = int(hex_str[4:6], 16) / 255.0
    return [round(r, 4), round(g, 4), round(b, 4), round(alpha, 4)]

# --- AItuko Japandi Palette & Material Shaders ---
COLOR_WHITE             = hex_to_lottie_color("#FFFFFF", 1.0)
COLOR_PORCELAIN_BASE    = hex_to_lottie_color("#F8FAFC", 1.0)
COLOR_PORCELAIN_SHADOW  = hex_to_lottie_color("#CBD5E1", 1.0)
COLOR_PORCELAIN_DARK    = hex_to_lottie_color("#94A3B8", 1.0)
COLOR_SPECULAR_HIGH     = hex_to_lottie_color("#FFFFFF", 0.90)
COLOR_SPECULAR_MED      = hex_to_lottie_color("#FFFFFF", 0.50)
COLOR_SPECULAR_SOFT     = hex_to_lottie_color("#FFFFFF", 0.25)

COLOR_VISOR_BEZEL       = hex_to_lottie_color("#090A0F", 1.0)
COLOR_VISOR_GLASS       = hex_to_lottie_color("#10121A", 1.0)
COLOR_VISOR_SPECULAR    = hex_to_lottie_color("#383D4E", 0.55)
COLOR_VISOR_GLOSS_ARC   = hex_to_lottie_color("#64748B", 0.30)

COLOR_CYAN_CORE         = hex_to_lottie_color("#00F0FF", 1.0)
COLOR_CYAN_HIGHLIGHT    = hex_to_lottie_color("#E0F7FF", 1.0)
COLOR_CYAN_GLOW         = hex_to_lottie_color("#00E5FF", 0.40)
COLOR_CYAN_AMB          = hex_to_lottie_color("#00E5FF", 0.20)

COLOR_SHADOW            = hex_to_lottie_color("#0F172A", 0.22)
COLOR_SHADOW_SOFT       = hex_to_lottie_color("#0F172A", 0.08)
COLOR_NECK_SHADOW       = hex_to_lottie_color("#0F172A", 0.28)

# Props & Accents
COLOR_GREEN_SUCCESS     = hex_to_lottie_color("#10B981", 1.0)
COLOR_GREEN_GLOW        = hex_to_lottie_color("#34D399", 0.45)
COLOR_RED_ERROR         = hex_to_lottie_color("#EF4444", 1.0)
COLOR_RED_GLOW          = hex_to_lottie_color("#F87171", 0.40)
COLOR_GOLD_ACCENT       = hex_to_lottie_color("#F59E0B", 1.0)
COLOR_GOLD_GLOW         = hex_to_lottie_color("#FBBF24", 0.45)


# --- Bézier Keyframe Constructor (Sine Ease-In-Out) ---
def kf(t, s, e=None, ix=0.42, iy=1.0, ox=0.58, oy=0.0):
    """
    Creates a keyframe with Bodymovin standard cubic-bezier easing.
    Prevents stiff/linear motion by ensuring smooth sinusoidal acceleration.
    """
    entry = {"t": t, "s": s}
    if e is not None:
        entry["e"] = e
        dim = len(s) if isinstance(s, list) else 1
        if dim == 1:
            entry["i"] = {"x": [ix], "y": [iy]}
            entry["o"] = {"x": [ox], "y": [oy]}
        else:
            entry["i"] = {"x": [ix] * dim, "y": [iy] * dim}
            entry["o"] = {"x": [ox] * dim, "y": [oy] * dim}
    return entry


# --- Lottie Shape Builders ---
def make_rect_shape(width, height, roundness=0, pos=(0, 0), name="Rect Shape"):
    return {
        "ty": "rc",
        "d": 1,
        "s": {"a": 0, "k": [round(width, 2), round(height, 2)]},
        "p": {"a": 0, "k": [round(pos[0], 2), round(pos[1], 2)]},
        "r": {"a": 0, "k": round(roundness, 2)},
        "nm": name
    }

def make_ellipse_shape(width, height, pos=(0, 0), name="Ellipse Shape"):
    return {
        "ty": "el",
        "d": 1,
        "s": {"a": 0, "k": [round(width, 2), round(height, 2)]},
        "p": {"a": 0, "k": [round(pos[0], 2), round(pos[1], 2)]},
        "nm": name
    }

def make_path_shape(vertices, in_tangents=None, out_tangents=None, closed=False, name="Path Shape"):
    n = len(vertices)
    it = in_tangents or [[0, 0]] * n
    ot = out_tangents or [[0, 0]] * n
    return {
        "ty": "sh",
        "d": 1,
        "ks": {
            "a": 0,
            "k": {
                "c": closed,
                "v": vertices,
                "i": it,
                "o": ot
            }
        },
        "nm": name
    }

def make_shape_group(name, shape_items, fill_color=None, stroke=None, transform=None):
    if not isinstance(shape_items, list):
        shape_items = [shape_items]
    items = list(shape_items)
    
    if fill_color:
        items.append({
            "ty": "fl",
            "c": {"a": 0, "k": fill_color[:3]},
            "o": {"a": 0, "k": int(fill_color[3] * 100)},
            "nm": f"{name} Fill"
        })
    if stroke:
        items.append({
            "ty": "st",
            "c": {"a": 0, "k": stroke["color"][:3]},
            "o": {"a": 0, "k": int(stroke["color"][3] * 100)},
            "w": {"a": 0, "k": stroke["width"]},
            "lc": stroke.get("lc", 2), # 2 = round cap
            "lj": stroke.get("lj", 2), # 2 = round join
            "nm": f"{name} Stroke"
        })
    
    tr = transform or {
        "p": {"a": 0, "k": [0, 0]},
        "a": {"a": 0, "k": [0, 0]},
        "s": {"a": 0, "k": [100, 100]},
        "r": {"a": 0, "k": 0},
        "o": {"a": 0, "k": 100}
    }
    tr["ty"] = "tr"
    items.append(tr)
    return {
        "ty": "gr",
        "nm": name,
        "it": items
    }

def make_layer(ind, name, shapes, ks=None):
    default_ks = {
        "o": {"a": 0, "k": 100},
        "r": {"a": 0, "k": 0},
        "p": {"a": 0, "k": [256, 256, 0]},
        "a": {"a": 0, "k": [0, 0, 0]},
        "s": {"a": 0, "k": [100, 100, 100]}
    }
    return {
        "ddd": 0,
        "ind": ind,
        "ty": 4, # shape layer
        "nm": name,
        "sr": 1,
        "ks": ks or default_ks,
        "ao": 0,
        "shapes": shapes,
        "ip": 0,
        "op": 120,
        "st": 0,
        "bm": 0
    }


# --- High-Fidelity Character Rig Constructor ---

def build_ground_shadow():
    """Ground ambient occlusion shadow scaling inversely with floating height."""
    shadow_shapes = [
        make_shape_group("Soft Occlusion Core", make_ellipse_shape(140, 20), COLOR_SHADOW),
        make_shape_group("Wide Ambient Blur", make_ellipse_shape(180, 26), COLOR_SHADOW_SOFT)
    ]
    # Dynamic coupling: apex at f27 (smaller/fainter), nadir at f84 (larger/darker)
    scale_kf = [
        kf(0,   [100, 100, 100], [82, 82, 100]),
        kf(27,  [82, 82, 100],   [100, 100, 100]),
        kf(58,  [100, 100, 100], [108, 108, 100]),
        kf(84,  [108, 108, 100], [100, 100, 100]),
        kf(120, [100, 100, 100])
    ]
    opacity_kf = [
        kf(0,   80, 55),
        kf(27,  55, 80),
        kf(58,  80, 98),
        kf(84,  98, 80),
        kf(120, 80)
    ]
    return make_layer(
        ind=1,
        name="Ground Shadow",
        shapes=shadow_shapes,
        ks={
            "o": {"a": 1, "k": opacity_kf},
            "r": {"a": 0, "k": 0},
            "p": {"a": 0, "k": [256, 495, 0]},
            "a": {"a": 0, "k": [0, 0, 0]},
            "s": {"a": 1, "k": scale_kf}
        }
    )

def build_support_pods(pos_kf=None, rot_kf=None):
    """
    Two distinct floating porcelain pod feet hovering under torso.
    Base Y ≈ 479 on 512 canvas (relative Y = +164 from torso center 315).
    """
    pod_shapes = [
        # Left Foot Pod (tilted -8 deg)
        make_shape_group("Left Pod Thruster Glow", make_ellipse_shape(32, 10, pos=(-45, 182)), COLOR_CYAN_AMB,
                         transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [-45, 182]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": -8}, "o": {"a": 0, "k": 100}}),
        make_shape_group("Left Pod Shadow Rim", make_rect_shape(56, 60, roundness=28, pos=(-45, 165)), COLOR_PORCELAIN_SHADOW,
                         transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [-45, 165]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": -8}, "o": {"a": 0, "k": 100}}),
        make_shape_group("Left Pod Porcelain Body", make_rect_shape(52, 56, roundness=26, pos=(-45, 164)), COLOR_WHITE,
                         transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [-45, 164]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": -8}, "o": {"a": 0, "k": 100}}),
        make_shape_group("Left Pod Specular Gloss", make_ellipse_shape(22, 10, pos=(-45, 146)), COLOR_SPECULAR_HIGH,
                         transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [-45, 146]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": -8}, "o": {"a": 0, "k": 85}}),
        
        # Right Foot Pod (tilted +8 deg)
        make_shape_group("Right Pod Thruster Glow", make_ellipse_shape(32, 10, pos=(45, 182)), COLOR_CYAN_AMB,
                         transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [45, 182]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 8}, "o": {"a": 0, "k": 100}}),
        make_shape_group("Right Pod Shadow Rim", make_rect_shape(56, 60, roundness=28, pos=(45, 165)), COLOR_PORCELAIN_SHADOW,
                         transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [45, 165]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 8}, "o": {"a": 0, "k": 100}}),
        make_shape_group("Right Pod Porcelain Body", make_rect_shape(52, 56, roundness=26, pos=(45, 164)), COLOR_WHITE,
                         transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [45, 164]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 8}, "o": {"a": 0, "k": 100}}),
        make_shape_group("Right Pod Specular Gloss", make_ellipse_shape(22, 10, pos=(45, 146)), COLOR_SPECULAR_HIGH,
                         transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [45, 146]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 8}, "o": {"a": 0, "k": 85}}),
    ]
    return make_layer(
        ind=2,
        name="Support Pods",
        shapes=pod_shapes,
        ks={
            "o": {"a": 0, "k": 100},
            "r": rot_kf or {"a": 0, "k": 0},
            "p": pos_kf or {"a": 0, "k": [256, 315, 0]},
            "a": {"a": 0, "k": [0, 0, 0]},
            "s": {"a": 0, "k": [100, 100, 100]}
        }
    )

def build_porcelain_torso(pos_kf=None, rot_kf=None, scale_kf=None):
    """
    Torso egg/capsule body: width 206, height 265, centered at Y=315 on 512 canvas.
    3D studio porcelain highlights and ambient depth.
    """
    torso_shapes = [
        # Outer ambient depth base
        make_shape_group("Torso Shadow Base", make_rect_shape(208, 267, roundness=89, pos=(0, 0)), COLOR_PORCELAIN_SHADOW),
        # Pure porcelain surface
        make_shape_group("Torso Porcelain Shell", make_rect_shape(204, 263, roundness=87, pos=(0, 0)), COLOR_PORCELAIN_BASE),
        # Left ambient diffuse soft shading
        make_shape_group("Torso Left Shade", make_rect_shape(65, 235, roundness=32, pos=(-58, 0)), hex_to_lottie_color("#E2E8F0", 0.45)),
        # Right vertical specular highlight strip (classic 3D studio gloss)
        make_shape_group("Torso Specular Gloss", make_rect_shape(18, 180, roundness=9, pos=(75, -10)), COLOR_SPECULAR_HIGH),
        # Top shoulder soft glow
        make_shape_group("Torso Shoulder Soft", make_ellipse_shape(110, 24, pos=(0, -110)), COLOR_SPECULAR_MED),
        # Under-chin neck shadow (creates realistic head separation)
        make_shape_group("Neck Shadow", make_ellipse_shape(95, 18, pos=(0, -132)), COLOR_NECK_SHADOW)
    ]
    return make_layer(
        ind=3,
        name="Porcelain Torso",
        shapes=torso_shapes,
        ks={
            "o": {"a": 0, "k": 100},
            "r": rot_kf or {"a": 0, "k": 0},
            "p": pos_kf or {"a": 0, "k": [256, 315, 0]},
            "a": {"a": 0, "k": [0, 0, 0]},
            "s": scale_kf or {"a": 0, "k": [100, 100, 100]}
        }
    )

def build_porcelain_head(head_pos_kf=None, head_rot_kf=None):
    """
    Large smooth porcelain helmet dome shell with crown specular reflection.
    Oblate dome: width 245, height 187, centered at Y=99 on 512 canvas.
    Pivot is at neck joint (256, 183).
    """
    head_shapes = [
        # Outer helmet bezel shadow
        make_shape_group("Helmet Shadow Base", make_rect_shape(247, 189, roundness=76, pos=(0, 0)), COLOR_PORCELAIN_SHADOW),
        # Main glossy porcelain helmet dome
        make_shape_group("Helmet Porcelain Dome", make_rect_shape(243, 185, roundness=74, pos=(0, 0)), COLOR_WHITE),
        # Crown specular glossy highlight
        make_shape_group("Crown Specular Highlight", make_ellipse_shape(115, 26, pos=(0, -74)), COLOR_SPECULAR_HIGH),
        # Right temple specular gloss reflection
        make_shape_group("Right Temple Gloss", make_ellipse_shape(18, 48, pos=(96, -30)), COLOR_SPECULAR_MED,
                         transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [96, -30]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 18}, "o": {"a": 0, "k": 65}}),
        # Left cheek soft ambient shade
        make_shape_group("Left Cheek Shade", make_ellipse_shape(26, 60, pos=(-96, -10)), hex_to_lottie_color("#E2E8F0", 0.40)),
        # Chin ambient bevel
        make_shape_group("Chin Soft Ambient", make_ellipse_shape(105, 14, pos=(0, 84)), hex_to_lottie_color("#CBD5E1", 0.50))
    ]
    return make_layer(
        ind=4,
        name="Porcelain Head",
        shapes=head_shapes,
        ks={
            "o": {"a": 0, "k": 100},
            "r": head_rot_kf or {"a": 0, "k": 0},
            "p": head_pos_kf or {"a": 0, "k": [256, 99, 0]},
            "a": {"a": 0, "k": [0, 0, 0]},
            "s": {"a": 0, "k": [100, 100, 100]}
        }
    )

def build_visor_glass(head_pos_kf=None, head_rot_kf=None):
    """
    Recessed black curved glass screen with specular reflection arc.
    Visor shield: width 197, height 147, centered at Y=99 on 512 canvas.
    """
    visor_shapes = [
        # Visor outer bezel bevel
        make_shape_group("Visor Bezel", make_rect_shape(201, 151, roundness=67, pos=(0, 0)), COLOR_VISOR_BEZEL),
        # Deep obsidian glass faceplate
        make_shape_group("Visor Core Glass", make_rect_shape(195, 145, roundness=64, pos=(0, 0)), COLOR_VISOR_GLASS),
        # Upper specular curved reflection arc (curved glass softbox gleam)
        make_shape_group("Visor Specular Gloss Arc", make_ellipse_shape(135, 36, pos=(0, -42)), COLOR_VISOR_SPECULAR),
        # Upper rim sharp gleam
        make_shape_group("Visor Glass Gleam", make_ellipse_shape(95, 14, pos=(0, -52)), COLOR_VISOR_GLOSS_ARC)
    ]
    return make_layer(
        ind=5,
        name="Visor Glass",
        shapes=visor_shapes,
        ks={
            "o": {"a": 0, "k": 100},
            "r": head_rot_kf or {"a": 0, "k": 0},
            "p": head_pos_kf or {"a": 0, "k": [256, 99, 0]},
            "a": {"a": 0, "k": [0, 0, 0]},
            "s": {"a": 0, "k": [100, 100, 100]}
        }
    )

def build_cyan_eyes(eyes_pos_kf=None, eyes_rot_kf=None, eyes_scale_kf=None, eye_type="arch"):
    """
    Electric Cyan LED eyes with neon bloom.
    Eye center: Y=99 on 512 canvas. Left eye X=-45 (canvas 211), Right eye X=+45 (canvas 301).
    Width 48, Height 31.
    Zero-displacement blink scaling centered at (0, 0).
    """
    shapes = []
    
    if eye_type == "arch":
        # Smiling crescent arch paths matching the master 3D render:
        # Left eye: from X=-67 to X=-23, apex at (-45, -16)
        left_arc_v = [[-67, 6], [-45, -12], [-23, 6]]
        left_arc_i = [[0, 0], [-10.5, 0], [0, 0]]
        left_arc_o = [[0, 0], [10.5, 0], [0, 0]]
        
        # Right eye: from X=23 to X=67, apex at (45, -12)
        right_arc_v = [[23, 6], [45, -12], [67, 6]]
        right_arc_i = [[0, 0], [-10.5, 0], [0, 0]]
        right_arc_o = [[0, 0], [10.5, 0], [0, 0]]
        
        # Outer Bloom
        shapes.append(make_shape_group("Left Eye Bloom", make_path_shape(left_arc_v, left_arc_i, left_arc_o),
                                       stroke={"color": COLOR_CYAN_GLOW, "width": 18, "lc": 2, "lj": 2}))
        shapes.append(make_shape_group("Right Eye Bloom", make_path_shape(right_arc_v, right_arc_i, right_arc_o),
                                       stroke={"color": COLOR_CYAN_GLOW, "width": 18, "lc": 2, "lj": 2}))
        # Core Electric Neon
        shapes.append(make_shape_group("Left Eye Core", make_path_shape(left_arc_v, left_arc_i, left_arc_o),
                                       stroke={"color": COLOR_CYAN_CORE, "width": 9.5, "lc": 2, "lj": 2}))
        shapes.append(make_shape_group("Right Eye Core", make_path_shape(right_arc_v, right_arc_i, right_arc_o),
                                       stroke={"color": COLOR_CYAN_CORE, "width": 9.5, "lc": 2, "lj": 2}))
        # Inner Crisp White-Cyan Highlights
        shapes.append(make_shape_group("Left Eye Highlight", make_path_shape(left_arc_v, left_arc_i, left_arc_o),
                                       stroke={"color": COLOR_CYAN_HIGHLIGHT, "width": 3.6, "lc": 2, "lj": 2}))
        shapes.append(make_shape_group("Right Eye Highlight", make_path_shape(right_arc_v, right_arc_i, right_arc_o),
                                       stroke={"color": COLOR_CYAN_HIGHLIGHT, "width": 3.6, "lc": 2, "lj": 2}))

    elif eye_type == "down_arch":
        # Drooping farewell crescent arch
        left_arc_v = [[-67, -10], [-45, 8], [-23, -10]]
        left_arc_i = [[0, 0], [-10.5, 0], [0, 0]]
        left_arc_o = [[0, 0], [10.5, 0], [0, 0]]
        
        right_arc_v = [[23, -10], [45, 8], [67, -10]]
        right_arc_i = [[0, 0], [-10.5, 0], [0, 0]]
        right_arc_o = [[0, 0], [10.5, 0], [0, 0]]
        
        shapes.append(make_shape_group("Left Eye Bloom", make_path_shape(left_arc_v, left_arc_i, left_arc_o),
                                       stroke={"color": COLOR_CYAN_GLOW, "width": 18, "lc": 2, "lj": 2}))
        shapes.append(make_shape_group("Right Eye Bloom", make_path_shape(right_arc_v, right_arc_i, right_arc_o),
                                       stroke={"color": COLOR_CYAN_GLOW, "width": 18, "lc": 2, "lj": 2}))
        shapes.append(make_shape_group("Left Eye Core", make_path_shape(left_arc_v, left_arc_i, left_arc_o),
                                       stroke={"color": COLOR_CYAN_CORE, "width": 9.5, "lc": 2, "lj": 2}))
        shapes.append(make_shape_group("Right Eye Core", make_path_shape(right_arc_v, right_arc_i, right_arc_o),
                                       stroke={"color": COLOR_CYAN_CORE, "width": 9.5, "lc": 2, "lj": 2}))
        shapes.append(make_shape_group("Left Eye Highlight", make_path_shape(left_arc_v, left_arc_i, left_arc_o),
                                       stroke={"color": COLOR_CYAN_HIGHLIGHT, "width": 3.6, "lc": 2, "lj": 2}))
        shapes.append(make_shape_group("Right Eye Highlight", make_path_shape(right_arc_v, right_arc_i, right_arc_o),
                                       stroke={"color": COLOR_CYAN_HIGHLIGHT, "width": 3.6, "lc": 2, "lj": 2}))

    elif eye_type == "pill":
        # Expressive rounded pill eyes
        shapes.append(make_shape_group("Left Eye Bloom", make_ellipse_shape(42, 50, pos=(-45, 0)), COLOR_CYAN_GLOW))
        shapes.append(make_shape_group("Right Eye Bloom", make_ellipse_shape(42, 50, pos=(45, 0)), COLOR_CYAN_GLOW))
        shapes.append(make_shape_group("Left Eye Core", make_rect_shape(28, 40, roundness=14, pos=(-45, 0)), COLOR_CYAN_CORE))
        shapes.append(make_shape_group("Right Eye Core", make_rect_shape(28, 40, roundness=14, pos=(45, 0)), COLOR_CYAN_CORE))
        shapes.append(make_shape_group("Left Eye Highlight", make_ellipse_shape(10, 16, pos=(-41, -6)), COLOR_CYAN_HIGHLIGHT))
        shapes.append(make_shape_group("Right Eye Highlight", make_ellipse_shape(10, 16, pos=(49, -6)), COLOR_CYAN_HIGHLIGHT))

    elif eye_type == "line":
        # Sleeping horizontal LED lines
        shapes.append(make_shape_group("Left Eye Line Bloom", make_rect_shape(42, 12, roundness=6, pos=(-45, 0)), COLOR_CYAN_GLOW))
        shapes.append(make_shape_group("Right Eye Line Bloom", make_rect_shape(42, 12, roundness=6, pos=(45, 0)), COLOR_CYAN_GLOW))
        shapes.append(make_shape_group("Left Eye Line", make_rect_shape(36, 7, roundness=3.5, pos=(-45, 0)), COLOR_CYAN_CORE))
        shapes.append(make_shape_group("Right Eye Line", make_rect_shape(36, 7, roundness=3.5, pos=(45, 0)), COLOR_CYAN_CORE))

    elif eye_type == "question":
        # Confused question mark eyes
        left_q_v = [[-52, -14], [-45, -22], [-38, -14], [-45, -4], [-45, 4]]
        shapes.append(make_shape_group("Left Q Bloom", make_path_shape(left_q_v), stroke={"color": COLOR_CYAN_GLOW, "width": 14, "lc": 2}))
        shapes.append(make_shape_group("Left Q Core", make_path_shape(left_q_v), stroke={"color": COLOR_CYAN_CORE, "width": 8.0, "lc": 2}))
        shapes.append(make_shape_group("Left Q Dot", make_ellipse_shape(6, 6, pos=(-45, 14)), COLOR_CYAN_CORE))
        
        right_q_v = [[38, -14], [45, -22], [52, -14], [45, -4], [45, 4]]
        shapes.append(make_shape_group("Right Q Bloom", make_path_shape(right_q_v), stroke={"color": COLOR_CYAN_GLOW, "width": 14, "lc": 2}))
        shapes.append(make_shape_group("Right Q Core", make_path_shape(right_q_v), stroke={"color": COLOR_CYAN_CORE, "width": 8.0, "lc": 2}))
        shapes.append(make_shape_group("Right Q Dot", make_ellipse_shape(6, 6, pos=(45, 14)), COLOR_CYAN_CORE))

    elif eye_type == "guardian":
        # Heroic determined guardian eyes from official 3D security render (tilted inward)
        shapes.append(make_shape_group("Left Eye Bloom", make_ellipse_shape(42, 46, pos=(-45, 0)), COLOR_CYAN_GLOW,
                                       transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [-45, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 16}, "o": {"a": 0, "k": 100}}))
        shapes.append(make_shape_group("Right Eye Bloom", make_ellipse_shape(42, 46, pos=(45, 0)), COLOR_CYAN_GLOW,
                                       transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [45, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": -16}, "o": {"a": 0, "k": 100}}))
        shapes.append(make_shape_group("Left Eye Core", make_rect_shape(28, 36, roundness=11, pos=(-45, 0)), COLOR_CYAN_CORE,
                                       transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [-45, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 16}, "o": {"a": 0, "k": 100}}))
        shapes.append(make_shape_group("Right Eye Core", make_rect_shape(28, 36, roundness=11, pos=(45, 0)), COLOR_CYAN_CORE,
                                       transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [45, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": -16}, "o": {"a": 0, "k": 100}}))
        shapes.append(make_shape_group("Left Eye Highlight", make_ellipse_shape(9, 13, pos=(-42, -5)), COLOR_CYAN_HIGHLIGHT,
                                       transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [-42, -5]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 16}, "o": {"a": 0, "k": 100}}))
        shapes.append(make_shape_group("Right Eye Highlight", make_ellipse_shape(9, 13, pos=(42, -5)), COLOR_CYAN_HIGHLIGHT,
                                       transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [42, -5]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": -16}, "o": {"a": 0, "k": 100}}))

    return make_layer(
        ind=6,
        name="Cyan Eyes",
        shapes=shapes,
        ks={
            "o": {"a": 0, "k": 100},
            "r": eyes_rot_kf or {"a": 0, "k": 0},
            "p": eyes_pos_kf or {"a": 0, "k": [256, 99, 0]},
            "a": {"a": 0, "k": [0, 0, 0]},  # Exact center of eyes
            "s": eyes_scale_kf or {"a": 0, "k": [100, 100, 100]}
        }
    )

def build_floating_arm(ind, name, is_right=False, pos_kf=None, rot_kf=None):
    """
    Independent floating porcelain arm capsule with 3D glossy highlight.
    Width 54, Height 138, roundness 27.
    Rest X = ±124 (Left arm X = 132, Right arm X = 380).
    Rest Y = 333 on 512 canvas.
    Pivots around shoulder anchor [0, -50, 0] for natural hovering swing.
    """
    rest_x = 124 if is_right else -124
    rest_rot = 7 if is_right else -7
    
    shapes = [
        # Arm shadow rim base
        make_shape_group(f"{name} Shadow Base", make_rect_shape(56, 140, roundness=28, pos=(0, 0)), COLOR_PORCELAIN_SHADOW),
        # Main porcelain shell
        make_shape_group(f"{name} Porcelain Shell", make_rect_shape(52, 136, roundness=26, pos=(0, 0)), COLOR_WHITE),
        # Glossy specular reflection streak
        make_shape_group(f"{name} Specular Gloss", make_rect_shape(8, 88, roundness=4, pos=(9, -10)), COLOR_SPECULAR_HIGH),
        # Inner flank soft shade
        make_shape_group(f"{name} Inner Shade", make_rect_shape(14, 96, roundness=7, pos=(-12, 0)), hex_to_lottie_color("#E2E8F0", 0.35))
    ]
    
    default_p = [256 + rest_x, 333, 0]
    
    return make_layer(
        ind=ind,
        name=name,
        shapes=shapes,
        ks={
            "o": {"a": 0, "k": 100},
            "r": rot_kf or {"a": 0, "k": rest_rot},
            "p": pos_kf or {"a": 0, "k": default_p},
            "a": {"a": 0, "k": [0, -50, 0]},  # Shoulder pivot
            "s": {"a": 0, "k": [100, 100, 100]}
        }
    )


# --- 13 State Generation Engine (120 Frames / 4.0s Seamless Loop) ---

def generate_state(state_name):
    """
    Generates a high-fidelity 120-frame (4.0s @ 30fps) seamless loop Lottie document for state.
    """
    # 1. Base Levitation Kinematics (Harmonic 4.0s cycle matching 3D video)
    # Apex at f27 (-18px: Y=238), nadir at f84 (+16px: Y=272)
    torso_p_kf = {
        "a": 1,
        "k": [
            kf(0,   [256, 315, 0], [256, 297, 0]),
            kf(27,  [256, 297, 0], [256, 315, 0]),
            kf(58,  [256, 315, 0], [256, 331, 0]),
            kf(84,  [256, 331, 0], [256, 315, 0]),
            kf(120, [256, 315, 0])
        ]
    }
    
    # Head lags torso by 4 frames with organic curiosity sway
    head_p_kf = {
        "a": 1,
        "k": [
            kf(0,   [256, 99, 0], [256, 81, 0]),
            kf(31,  [256, 81, 0], [256, 99, 0]),
            kf(62,  [256, 99, 0], [256, 115, 0]),
            kf(88,  [256, 115, 0], [256, 99, 0]),
            kf(120, [256, 99, 0])
        ]
    }
    head_r_kf = {
        "a": 1,
        "k": [
            kf(0,   0,    -2.2),
            kf(27,  -2.2, 0),
            kf(58,  0,    2.0),
            kf(84,  2.0,  0),
            kf(120, 0)
        ]
    }
    
    # Eyes position & rotation match head
    eyes_p_kf = copy.deepcopy(head_p_kf)
    eyes_r_kf = copy.deepcopy(head_r_kf)
    
    # Feet support pods have 4 frames lag
    pods_p_kf = {
        "a": 1,
        "k": [
            kf(0,   [256, 315, 0], [256, 297, 0]),
            kf(31,  [256, 297, 0], [256, 315, 0]),
            kf(62,  [256, 315, 0], [256, 331, 0]),
            kf(88,  [256, 331, 0], [256, 315, 0]),
            kf(120, [256, 315, 0])
        ]
    }
    
    # Left & Right floating arms lag by 6 frames with gentle breathing flare (arm span widens at apex)
    larm_p_kf = {
        "a": 1,
        "k": [
            kf(0,   [256 - 124, 333, 0], [256 - 130, 315, 0]),
            kf(33,  [256 - 130, 315, 0], [256 - 124, 333, 0]),
            kf(64,  [256 - 124, 333, 0], [256 - 122, 349, 0]),
            kf(90,  [256 - 122, 349, 0], [256 - 124, 333, 0]),
            kf(120, [256 - 124, 333, 0])
        ]
    }
    larm_r_kf = {
        "a": 1,
        "k": [
            kf(0,   -7,  -12),
            kf(33,  -12, -7),
            kf(64,  -7,  -5),
            kf(90,  -5,  -7),
            kf(120, -7)
        ]
    }
    
    rarm_p_kf = {
        "a": 1,
        "k": [
            kf(0,   [256 + 124, 333, 0], [256 + 130, 315, 0]),
            kf(33,  [256 + 130, 315, 0], [256 + 124, 333, 0]),
            kf(64,  [256 + 124, 333, 0], [256 + 122, 349, 0]),
            kf(90,  [256 + 122, 349, 0], [256 + 124, 333, 0]),
            kf(120, [256 + 124, 333, 0])
        ]
    }
    rarm_r_kf = {
        "a": 1,
        "k": [
            kf(0,   7,   12),
            kf(33,  12,  7),
            kf(64,  7,   5),
            kf(90,  5,   7),
            kf(120, 7)
        ]
    }
    
    # Natural organic double-blink during nadir turnaround (frames 78-86)
    eyes_s_kf = {
        "a": 1,
        "k": [
            kf(0,   [100, 100, 100], [100, 100, 100]),
            kf(78,  [100, 100, 100], [100, 8, 100]),
            kf(80,  [100, 8, 100],   [100, 100, 100]),
            kf(82,  [100, 100, 100], [100, 15, 100]),
            kf(85,  [100, 15, 100],  [100, 100, 100]),
            kf(87,  [100, 100, 100], [100, 100, 100]),
            kf(120, [100, 100, 100])
        ]
    }
    
    eye_type = "arch"
    extra_layers = []
    
    # --- State Customization ---
    
    if state_name == "00_idle":
        pass # standard floating idle
        
    elif state_name == "01_waving":
        head_r_kf = {"a": 1, "k": [kf(0, 0, 3.5), kf(25, 3.5, 3.5), kf(95, 3.5, 0), kf(120, 0)]}
        eyes_r_kf = copy.deepcopy(head_r_kf)
        # Right arm rises up to wave
        rarm_p_kf = {
            "a": 1,
            "k": [
                kf(0,   [256 + 124, 333, 0], [256 + 138, 250, 0]),
                kf(25,  [256 + 138, 250, 0], [256 + 138, 240, 0]),
                kf(65,  [256 + 138, 240, 0], [256 + 138, 250, 0]),
                kf(95,  [256 + 138, 250, 0], [256 + 124, 333, 0]),
                kf(120, [256 + 124, 333, 0])
            ]
        }
        rarm_r_kf = {
            "a": 1,
            "k": [
                kf(0,   7,   32),
                kf(25,  32,  -16),
                kf(42,  -16, 30),
                kf(58,  30,  -14),
                kf(74,  -14, 28),
                kf(95,  28,  7),
                kf(120, 7)
            ]
        }
        
    elif state_name == "02_celebrating":
        torso_p_kf = {
            "a": 1,
            "k": [
                kf(0,   [256, 315, 0], [256, 280, 0]),
                kf(40,  [256, 280, 0], [256, 315, 0]),
                kf(85,  [256, 315, 0]),
                kf(120, [256, 315, 0])
            ]
        }
        head_p_kf = {
            "a": 1,
            "k": [
                kf(0,   [256, 99, 0], [256, 64, 0]),
                kf(40,  [256, 64, 0], [256, 99, 0]),
                kf(85,  [256, 99, 0]),
                kf(120, [256, 99, 0])
            ]
        }
        eyes_p_kf = copy.deepcopy(head_p_kf)
        pods_p_kf = copy.deepcopy(torso_p_kf)
        
        # Both arms raised triumphantly in "V"
        larm_p_kf = {
            "a": 1,
            "k": [
                kf(0,   [256 - 124, 333, 0], [256 - 145, 235, 0]),
                kf(35,  [256 - 145, 235, 0], [256 - 124, 333, 0]),
                kf(95,  [256 - 124, 333, 0]),
                kf(120, [256 - 124, 333, 0])
            ]
        }
        larm_r_kf = {"a": 1, "k": [kf(0, -7, -48), kf(35, -48, -7), kf(120, -7)]}
        rarm_p_kf = {
            "a": 1,
            "k": [
                kf(0,   [256 + 124, 333, 0], [256 + 145, 235, 0]),
                kf(35,  [256 + 145, 235, 0], [256 + 124, 333, 0]),
                kf(95,  [256 + 124, 333, 0]),
                kf(120, [256 + 124, 333, 0])
            ]
        }
        rarm_r_kf = {"a": 1, "k": [kf(0, 7, 48), kf(35, 48, 7), kf(120, 7)]}
        
        # Confetti particle burst
        confetti_shapes = []
        confetti_colors = [
            hex_to_lottie_color("#EC4899"), hex_to_lottie_color("#F59E0B"),
            hex_to_lottie_color("#10B981"), hex_to_lottie_color("#6366F1"),
            hex_to_lottie_color("#00F0FF"), hex_to_lottie_color("#F43F5E")
        ]
        for i in range(14):
            ang = (i / 14.0) * math.pi * 2
            dist = 110 + (i % 3) * 30
            cx = math.cos(ang) * dist
            cy = math.sin(ang) * (dist * 0.6) - 60
            confetti_shapes.append(make_shape_group(
                f"Confetti_{i}",
                make_rect_shape(10, 6, roundness=2, pos=(cx, cy)),
                confetti_colors[i % len(confetti_colors)],
                transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [cx, cy]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": i * 26}, "o": {"a": 0, "k": 100}}
            ))
        extra_layers.append(make_layer(
            ind=10,
            name="Confetti Burst",
            shapes=confetti_shapes,
            ks={
                "o": {"a": 1, "k": [kf(0, 0, 100), kf(25, 100, 100), kf(85, 100, 0), kf(120, 0)]},
                "r": {"a": 1, "k": [kf(0, 0, 160), kf(90, 160, 160), kf(120, 160)]},
                "p": {"a": 1, "k": [kf(0, [256, 280, 0], [256, 340, 0]), kf(90, [256, 340, 0]), kf(120, 256, 340)]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {"a": 1, "k": [kf(0, [40, 40, 100], [120, 120, 100]), kf(30, [120, 120, 100], [100, 100, 100]), kf(120, [100, 100, 100])]}
            }
        ))

    elif state_name == "03_ai_thinking":
        eye_type = "pill"
        head_r_kf = {"a": 1, "k": [kf(0, 0, -6.0), kf(60, -6.0, 0), kf(120, 0)]}
        eyes_r_kf = copy.deepcopy(head_r_kf)
        
        # Right arm rises and touches chin
        rarm_p_kf = {
            "a": 1,
            "k": [
                kf(0,   [256 + 124, 333, 0], [256 + 85, 260, 0]),
                kf(30,  [256 + 85, 260, 0],  [256 + 85, 255, 0]),
                kf(90,  [256 + 85, 255, 0],  [256 + 124, 333, 0]),
                kf(120, [256 + 124, 333, 0])
            ]
        }
        rarm_r_kf = {"a": 1, "k": [kf(0, 7, -32), kf(30, -32, -28), kf(90, -28, 7), kf(120, 7)]}
        
        # 3 Holographic glowing cyan data cubes orbiting in 3D around head with smooth continuous easing
        orbit_frames = [0, 15, 30, 45, 60, 75, 90, 105, 120]
        for cube_idx in range(3):
            phase_offset = (cube_idx / 3.0) * math.pi * 2
            raw_p = []
            raw_s = []
            raw_o = []
            for fr in orbit_frames:
                rad = (fr / 120.0) * math.pi * 2 + phase_offset
                ox = round(math.cos(rad) * 115, 2)
                oy = round(math.sin(rad) * 36 - 99, 2)
                depth = (math.sin(rad) + 1.0) / 2.0
                sc = round(75 + depth * 35, 1)
                op = round(45 + depth * 55, 1)
                raw_p.append([round(256 + ox, 2), round(256 + oy, 2), 0])
                raw_s.append([sc, sc, 100])
                raw_o.append(op)
            
            orbit_p = []
            orbit_s = []
            orbit_o = []
            for j in range(len(orbit_frames) - 1):
                orbit_p.append(kf(orbit_frames[j], raw_p[j], raw_p[j+1]))
                orbit_s.append(kf(orbit_frames[j], raw_s[j], raw_s[j+1]))
                orbit_o.append(kf(orbit_frames[j], raw_o[j], raw_o[j+1]))
            orbit_p.append(kf(orbit_frames[-1], raw_p[-1]))
            orbit_s.append(kf(orbit_frames[-1], raw_s[-1]))
            orbit_o.append(kf(orbit_frames[-1], raw_o[-1]))
                
            cube_shapes = [
                make_shape_group(f"Cube_{cube_idx}_Glow", make_rect_shape(22, 22, roundness=5), COLOR_CYAN_GLOW),
                make_shape_group(f"Cube_{cube_idx}_Core", make_rect_shape(16, 16, roundness=3), COLOR_CYAN_CORE),
                make_shape_group(f"Cube_{cube_idx}_Highlight", make_rect_shape(7, 7, roundness=1, pos=(-3, -3)), COLOR_CYAN_HIGHLIGHT)
            ]
            extra_layers.append(make_layer(
                ind=11 + cube_idx,
                name=f"Holographic Cube {cube_idx+1}",
                shapes=cube_shapes,
                ks={
                    "o": {"a": 1, "k": orbit_o},
                    "r": {"a": 1, "k": [kf(0, 0, 360), kf(120, 360)]},
                    "p": {"a": 1, "k": orbit_p},
                    "a": {"a": 0, "k": [0, 0, 0]},
                    "s": {"a": 1, "k": orbit_s}
                }
            ))

    elif state_name == "04_error_404":
        eye_type = "question"
        head_r_kf = {"a": 1, "k": [kf(0, 0, -5.0), kf(30, -5.0, 5.0), kf(85, 5.0, 0), kf(120, 0)]}
        eyes_r_kf = copy.deepcopy(head_r_kf)
        larm_r_kf = {"a": 1, "k": [kf(0, -7, 16), kf(60, 16, -7), kf(120, -7)]}
        rarm_r_kf = {"a": 1, "k": [kf(0, 7, -16), kf(60, -16, 7), kf(120, 7)]}
        
        # Glowing Red Holographic 404 Badge floating in front of chest
        badge_shapes = [
            make_shape_group("Badge Glass", make_rect_shape(88, 42, roundness=10), hex_to_lottie_color("#180808", 0.88),
                             stroke={"color": COLOR_RED_ERROR, "width": 3}),
            make_shape_group("Badge Glow", make_rect_shape(94, 48, roundness=12), COLOR_RED_GLOW),
            make_shape_group("Digit 4_1", make_rect_shape(6, 20, roundness=2, pos=(-25, 0)), COLOR_RED_ERROR),
            make_shape_group("Digit 4_1_arm", make_rect_shape(12, 4, roundness=1, pos=(-28, 2)), COLOR_RED_ERROR),
            make_shape_group("Digit 0", make_rect_shape(16, 20, roundness=5, pos=(0, 0)), None, stroke={"color": COLOR_RED_ERROR, "width": 4}),
            make_shape_group("Digit 4_2", make_rect_shape(6, 20, roundness=2, pos=(25, 0)), COLOR_RED_ERROR),
            make_shape_group("Digit 4_2_arm", make_rect_shape(12, 4, roundness=1, pos=(22, 2)), COLOR_RED_ERROR),
        ]
        extra_layers.append(make_layer(
            ind=14,
            name="Holographic 404 Badge",
            shapes=badge_shapes,
            ks={
                "o": {"a": 1, "k": [kf(0, 85, 100), kf(60, 100, 85), kf(120, 85)]},
                "r": {"a": 0, "k": 0},
                "p": {"a": 1, "k": [kf(0, [256, 320, 0], [256, 310, 0]), kf(60, [256, 310, 0], [256, 320, 0]), kf(120, [256, 320, 0])]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {"a": 1, "k": [kf(0, [98, 98, 100], [104, 104, 100]), kf(60, [104, 104, 100], [98, 98, 100]), kf(120, [98, 98, 100])]}
            }
        ))

    elif state_name == "05_thumbs_up":
        head_r_kf = {
            "a": 1,
            "k": [
                kf(0,   0,   4.0),
                kf(30,  4.0, -2.0),
                kf(70,  -2.0, 2.0),
                kf(95,  2.0, 0),
                kf(120, 0)
            ]
        }
        eyes_r_kf = copy.deepcopy(head_r_kf)
        # Right arm gives proud pose
        rarm_p_kf = {
            "a": 1,
            "k": [
                kf(0,   [256 + 124, 333, 0], [256 + 135, 275, 0]),
                kf(30,  [256 + 135, 275, 0], [256 + 135, 265, 0]),
                kf(70,  [256 + 135, 265, 0], [256 + 135, 275, 0]),
                kf(100, [256 + 135, 275, 0], [256 + 124, 333, 0]),
                kf(120, [256 + 124, 333, 0])
            ]
        }
        rarm_r_kf = {
            "a": 1,
            "k": [
                kf(0,   7,  40),
                kf(30,  40, 40),
                kf(100, 40, 7),
                kf(120, 7)
            ]
        }
        # Floating Glowing Green Checkmark in headroom
        tick_v = [[-24, 2], [-8, 18], [26, -16]]
        tick_shapes = [
            make_shape_group("Tick Glow Aura", make_ellipse_shape(84, 84), COLOR_GREEN_GLOW),
            make_shape_group("Tick Shadow", make_path_shape(tick_v), stroke={"color": hex_to_lottie_color("#064E3B"), "width": 14, "lc": 2, "lj": 2}),
            make_shape_group("Tick Core", make_path_shape(tick_v), stroke={"color": COLOR_GREEN_SUCCESS, "width": 9.5, "lc": 2, "lj": 2}),
            make_shape_group("Tick Highlight", make_path_shape(tick_v), stroke={"color": hex_to_lottie_color("#D1FAE5"), "width": 3.5, "lc": 2, "lj": 2})
        ]
        extra_layers.append(make_layer(
            ind=15,
            name="Holographic Success Checkmark",
            shapes=tick_shapes,
            ks={
                "o": {"a": 1, "k": [kf(0, 0, 100), kf(20, 100, 100), kf(100, 100, 85), kf(120, 85)]},
                "r": {"a": 0, "k": 0},
                "p": {"a": 1, "k": [kf(0, [256, 75, 0], [256, 65, 0]), kf(60, [256, 65, 0], [256, 75, 0]), kf(120, [256, 75, 0])]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {"a": 1, "k": [kf(0, [60, 60, 100], [112, 112, 100]), kf(25, [112, 112, 100], [100, 100, 100]), kf(120, [100, 100, 100])]}
            }
        ))

    elif state_name == "06_sleeping":
        eye_type = "line"
        head_r_kf = {"a": 0, "k": 8.0}
        eyes_r_kf = {"a": 0, "k": 8.0}
        # Slow calm breathing
        torso_p_kf = {
            "a": 1,
            "k": [
                kf(0,   [256, 318, 0], [256, 310, 0]),
                kf(60,  [256, 310, 0], [256, 318, 0]),
                kf(120, [256, 318, 0])
            ]
        }
        head_p_kf = {
            "a": 1,
            "k": [
                kf(0,   [256, 102, 0], [256, 94, 0]),
                kf(60,  [256, 94, 0],  [256, 102, 0]),
                kf(120, [256, 102, 0])
            ]
        }
        eyes_p_kf = copy.deepcopy(head_p_kf)
        pods_p_kf = copy.deepcopy(torso_p_kf)
        
        # 3 Floating Zzz bubbles
        for z_i in range(3):
            z_delay = z_i * 35
            z_shapes = [
                make_shape_group(f"Zzz_{z_i}_Bar1", make_rect_shape(14 - z_i*2, 3.5, roundness=1.5, pos=(0, -6 + z_i)), COLOR_CYAN_CORE),
                make_shape_group(f"Zzz_{z_i}_Diag", make_rect_shape(3.5, 14 - z_i*2, roundness=1.5, pos=(0, 0)), COLOR_CYAN_CORE,
                                 transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": -38}, "o": {"a": 0, "k": 100}}),
                make_shape_group(f"Zzz_{z_i}_Bar2", make_rect_shape(14 - z_i*2, 3.5, roundness=1.5, pos=(0, 6 - z_i)), COLOR_CYAN_CORE),
            ]
            extra_layers.append(make_layer(
                ind=16 + z_i,
                name=f"Sleeping Zzz {z_i+1}",
                shapes=z_shapes,
                ks={
                    "o": {"a": 1, "k": [kf(0, 0, 85), kf(50, 85, 0), kf(100, 0, 0), kf(120, 0)]},
                    "r": {"a": 1, "k": [kf(0, -10, 15), kf(120, 15)]},
                    "p": {"a": 1, "k": [kf(0, [290 + z_i*15, 80 - z_i*20, 0], [305 + z_i*20, 30 - z_i*25, 0]), kf(120, [305 + z_i*20, 30 - z_i*25, 0])]},
                    "a": {"a": 0, "k": [0, 0, 0]},
                    "s": {"a": 1, "k": [kf(0, [70, 70, 100], [110, 110, 100]), kf(120, [110, 110, 100])]}
                }
            ))

    elif state_name == "07_pointing":
        # Confident forward posture, right arm points forward
        rarm_p_kf = {
            "a": 1,
            "k": [
                kf(0,   [256 + 124, 333, 0], [256 + 155, 295, 0]),
                kf(25,  [256 + 155, 295, 0], [256 + 155, 290, 0]),
                kf(75,  [256 + 155, 290, 0], [256 + 155, 295, 0]),
                kf(100, [256 + 155, 295, 0], [256 + 124, 333, 0]),
                kf(120, [256 + 124, 333, 0])
            ]
        }
        rarm_r_kf = {
            "a": 1,
            "k": [
                kf(0,   7,  52),
                kf(25,  52, 52),
                kf(100, 52, 7),
                kf(120, 7)
            ]
        }
        # Holographic cyan crosshair reticle pulsing at fingertip
        reticle_shapes = [
            make_shape_group("Reticle Ring Glow", make_ellipse_shape(46, 46), None, stroke={"color": COLOR_CYAN_GLOW, "width": 8}),
            make_shape_group("Reticle Ring Core", make_ellipse_shape(38, 38), None, stroke={"color": COLOR_CYAN_CORE, "width": 3}),
            make_shape_group("Cross H", make_rect_shape(22, 2.5, roundness=1), COLOR_CYAN_HIGHLIGHT),
            make_shape_group("Cross V", make_rect_shape(2.5, 22, roundness=1), COLOR_CYAN_HIGHLIGHT)
        ]
        extra_layers.append(make_layer(
            ind=17,
            name="Holographic Targeting Reticle",
            shapes=reticle_shapes,
            ks={
                "o": {"a": 1, "k": [kf(0, 0, 100), kf(25, 100, 100), kf(95, 100, 0), kf(120, 0)]},
                "r": {"a": 1, "k": [kf(0, 0, 90), kf(120, 90)]},
                "p": {"a": 1, "k": [kf(0, [430, 275, 0], [440, 270, 0]), kf(60, [440, 270, 0], [430, 275, 0]), kf(120, [430, 275, 0])]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {"a": 1, "k": [kf(0, [70, 70, 100], [105, 105, 100]), kf(60, [105, 105, 100], [70, 70, 100]), kf(120, [70, 70, 100])]}
            }
        ))

    elif state_name == "08_searching":
        # Scanning radar sweep! Robotic owl attitude (no hands)
        head_r_kf = {
            "a": 1,
            "k": [
                kf(0,   0,   -12.0),
                kf(30,  -12.0, 12.0),
                kf(90,  12.0,  0),
                kf(120, 0)
            ]
        }
        eyes_r_kf = copy.deepcopy(head_r_kf)
        # Concentric cyan radar scan waves emitting from visor
        radar_shapes = [
            make_shape_group("Radar Cone", make_ellipse_shape(120, 50, pos=(0, 25)), hex_to_lottie_color("#00F0FF", 0.15)),
            make_shape_group("Radar Ring 1", make_ellipse_shape(70, 26, pos=(0, 15)), None, stroke={"color": COLOR_CYAN_CORE, "width": 3}),
            make_shape_group("Radar Ring 2", make_ellipse_shape(110, 42, pos=(0, 28)), None, stroke={"color": COLOR_CYAN_GLOW, "width": 2}),
            make_shape_group("Radar Sweep Line", make_rect_shape(2, 60, roundness=1, pos=(0, 25)), COLOR_CYAN_HIGHLIGHT)
        ]
        extra_layers.append(make_layer(
            ind=18,
            name="Radar Scan Wave",
            shapes=radar_shapes,
            ks={
                "o": {"a": 1, "k": [kf(0, 30, 95), kf(60, 95, 30), kf(120, 30)]},
                "r": {"a": 1, "k": [kf(0, -18, 18), kf(60, 18, -18), kf(120, -18)]},
                "p": {"a": 0, "k": [256, 125, 0]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {"a": 1, "k": [kf(0, [85, 85, 100], [115, 115, 100]), kf(60, [115, 115, 100], [85, 85, 100]), kf(120, [85, 85, 100])]}
            }
        ))

    elif state_name == "09_loading":
        # Dual holographic cyan gyroscopic rings spinning smoothly in 3D around core
        gyro_shapes1 = [
            make_shape_group("Gyro Ring 1 Glow", make_ellipse_shape(160, 60), None, stroke={"color": COLOR_CYAN_GLOW, "width": 8}),
            make_shape_group("Gyro Ring 1 Core", make_ellipse_shape(154, 54), None, stroke={"color": COLOR_CYAN_CORE, "width": 3.5}),
            make_shape_group("Gyro Particle 1", make_ellipse_shape(10, 10, pos=(75, 0)), COLOR_CYAN_HIGHLIGHT)
        ]
        gyro_shapes2 = [
            make_shape_group("Gyro Ring 2 Glow", make_ellipse_shape(140, 50), None, stroke={"color": COLOR_CYAN_GLOW, "width": 8}),
            make_shape_group("Gyro Ring 2 Core", make_ellipse_shape(134, 44), None, stroke={"color": COLOR_CYAN_CORE, "width": 3.5}),
            make_shape_group("Gyro Particle 2", make_ellipse_shape(10, 10, pos=(-65, 0)), COLOR_CYAN_HIGHLIGHT)
        ]
        extra_layers.append(make_layer(
            ind=19,
            name="Gyroscopic Ring Outer",
            shapes=gyro_shapes1,
            ks={
                "o": {"a": 0, "k": 85},
                "r": {"a": 1, "k": [kf(0, 0, 360), kf(120, 360)]},
                "p": {"a": 0, "k": [256, 315, 0]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {"a": 0, "k": [100, 100, 100]}
            }
        ))
        extra_layers.append(make_layer(
            ind=20,
            name="Gyroscopic Ring Inner",
            shapes=gyro_shapes2,
            ks={
                "o": {"a": 0, "k": 80},
                "r": {"a": 1, "k": [kf(0, 45, -315), kf(120, -315)]},
                "p": {"a": 0, "k": [256, 315, 0]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {"a": 0, "k": [100, 100, 100]}
            }
        ))

    elif state_name == "10_idea":
        # Eureka moment! Epiphanic nod, brilliant glowing yellow 3D lightbulb illuminates above head
        head_r_kf = {"a": 1, "k": [kf(0, 0, -4.0), kf(25, -4.0, 3.0), kf(80, 3.0, 0), kf(120, 0)]}
        eyes_r_kf = copy.deepcopy(head_r_kf)
        
        bulb_shapes = [
            make_shape_group("Bulb Glow Aura", make_ellipse_shape(80, 80), COLOR_GOLD_GLOW),
            make_shape_group("Bulb Glass Shell", make_ellipse_shape(46, 46, pos=(0, -8)), COLOR_GOLD_ACCENT),
            make_shape_group("Bulb Inner Filament", make_ellipse_shape(20, 20, pos=(0, -10)), COLOR_WHITE),
            make_shape_group("Bulb Base Collar", make_rect_shape(18, 12, roundness=3, pos=(0, 16)), hex_to_lottie_color("#78350F")),
            # Burst Rays
            make_shape_group("Ray Top", make_rect_shape(4, 16, roundness=2, pos=(0, -44)), COLOR_GOLD_ACCENT),
            make_shape_group("Ray Left", make_rect_shape(16, 4, roundness=2, pos=(-40, -8)), COLOR_GOLD_ACCENT),
            make_shape_group("Ray Right", make_rect_shape(16, 4, roundness=2, pos=(40, -8)), COLOR_GOLD_ACCENT),
            make_shape_group("Ray TL", make_rect_shape(14, 4, roundness=2, pos=(-28, -32)), COLOR_GOLD_ACCENT,
                             transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [-28, -32]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 45}, "o": {"a": 0, "k": 100}}),
            make_shape_group("Ray TR", make_rect_shape(14, 4, roundness=2, pos=(28, -32)), COLOR_GOLD_ACCENT,
                             transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [28, -32]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": -45}, "o": {"a": 0, "k": 100}}),
        ]
        extra_layers.append(make_layer(
            ind=21,
            name="Eureka Glowing Lightbulb",
            shapes=bulb_shapes,
            ks={
                "o": {"a": 1, "k": [kf(0, 0, 100), kf(20, 100, 100), kf(95, 100, 85), kf(120, 85)]},
                "r": {"a": 0, "k": 0},
                "p": {"a": 1, "k": [kf(0, [256, 50, 0], [256, 40, 0]), kf(60, [256, 40, 0], [256, 50, 0]), kf(120, [256, 50, 0])]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {"a": 1, "k": [kf(0, [50, 50, 100], [115, 115, 100]), kf(25, [115, 115, 100], [100, 100, 100]), kf(120, [100, 100, 100])]}
            }
        ))

    elif state_name == "11_security":
        eye_type = "guardian"
        # Guardian energy shield hologram
        shield_v = [[0, -60], [52, -30], [52, 30], [0, 60], [-52, 30], [-52, -30]]
        shield_shapes = [
            make_shape_group("Shield Ambient Aura", make_path_shape(shield_v, closed=True), hex_to_lottie_color("#00F0FF", 0.18)),
            make_shape_group("Shield Outer Border", make_path_shape(shield_v, closed=True), stroke={"color": COLOR_CYAN_GLOW, "width": 8, "lj": 2}),
            make_shape_group("Shield Inner Core", make_path_shape(shield_v, closed=True), stroke={"color": COLOR_CYAN_CORE, "width": 3.5, "lj": 2}),
            # Shield Lock Emblem
            make_shape_group("Lock Body", make_rect_shape(24, 20, roundness=5, pos=(0, 8)), COLOR_CYAN_HIGHLIGHT),
            make_shape_group("Lock Shackle", make_ellipse_shape(16, 16, pos=(0, -6)), None, stroke={"color": COLOR_CYAN_HIGHLIGHT, "width": 4})
        ]
        extra_layers.append(make_layer(
            ind=22,
            name="Holographic Security Shield",
            shapes=shield_shapes,
            ks={
                "o": {"a": 1, "k": [kf(0, 80, 100), kf(60, 100, 80), kf(120, 80)]},
                "r": {"a": 0, "k": 0},
                "p": {"a": 1, "k": [kf(0, [256, 305, 0], [256, 298, 0]), kf(60, [256, 298, 0], [256, 305, 0]), kf(120, [256, 305, 0])]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {"a": 1, "k": [kf(0, [96, 96, 100], [104, 104, 100]), kf(60, [104, 104, 100], [96, 96, 100]), kf(120, [96, 96, 100])]}
            }
        ))

    elif state_name == "12_goodbye":
        eye_type = "down_arch"
        head_r_kf = {"a": 1, "k": [kf(0, 0, -3.5), kf(30, -3.5, -3.5), kf(95, -3.5, 0), kf(120, 0)]}
        eyes_r_kf = copy.deepcopy(head_r_kf)
        # Slow gentle wave
        rarm_p_kf = {
            "a": 1,
            "k": [
                kf(0,   [256 + 124, 333, 0], [256 + 135, 260, 0]),
                kf(25,  [256 + 135, 260, 0], [256 + 135, 255, 0]),
                kf(65,  [256 + 135, 255, 0], [256 + 135, 260, 0]),
                kf(95,  [256 + 135, 260, 0], [256 + 124, 333, 0]),
                kf(120, [256 + 124, 333, 0])
            ]
        }
        rarm_r_kf = {
            "a": 1,
            "k": [
                kf(0,   7,   24),
                kf(25,  24,  -8),
                kf(55,  -8,  22),
                kf(85,  22,  7),
                kf(120, 7)
            ]
        }

    # Assemble All Rig Layers in Correct Depth Stacking Order
    shadow_layer = build_ground_shadow()
    pods_layer = build_support_pods(pos_kf=pods_p_kf)
    torso_layer = build_porcelain_torso(pos_kf=torso_p_kf)
    head_layer = build_porcelain_head(head_pos_kf=head_p_kf, head_rot_kf=head_r_kf)
    visor_layer = build_visor_glass(head_pos_kf=head_p_kf, head_rot_kf=head_r_kf)
    eyes_layer = build_cyan_eyes(eyes_pos_kf=eyes_p_kf, eyes_rot_kf=eyes_r_kf, eyes_scale_kf=eyes_s_kf, eye_type=eye_type)
    larm_layer = build_floating_arm(ind=7, name="Floating Left Arm", is_right=False, pos_kf=larm_p_kf, rot_kf=larm_r_kf)
    rarm_layer = build_floating_arm(ind=8, name="Floating Right Arm", is_right=True, pos_kf=rarm_p_kf, rot_kf=rarm_r_kf)
    
    layers = [shadow_layer, pods_layer, torso_layer, head_layer, visor_layer, eyes_layer, larm_layer, rarm_layer]
    layers.extend(extra_layers)
    
    doc = {
        "v": "5.7.4",
        "fr": 30,
        "ip": 0,
        "op": 120,
        "w": 512,
        "h": 512,
        "nm": f"AItuko - {state_name}",
        "ddd": 0,
        "assets": [],
        "layers": layers
    }
    return doc

def build_all_aituko_lottie():
    states = [
        "00_idle", "01_waving", "02_celebrating", "03_ai_thinking",
        "04_error_404", "05_thumbs_up", "06_sleeping", "07_pointing",
        "08_searching", "09_loading", "10_idea", "11_security", "12_goodbye"
    ]
    
    print("🎨 Generating AItuko Master Lottie Vector Suite (13 states, 120 frames / 4.0s loop)...")
    for st in states:
        doc = generate_state(st)
        json_str = json.dumps(doc, separators=(',', ':'))
        
        target_dirs = [
            f"assets/{st}",
            f"mascots/aituko/assets/{st}",
            f"aituko/assets/{st}"
        ]
        for td in target_dirs:
            if os.path.exists(td):
                out_path = os.path.join(td, "lottie.json")
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(json_str)
                sz_kb = os.path.getsize(out_path) / 1024.0
                print(f"  ✅ {out_path} ({sz_kb:.1f} KB)")

if __name__ == "__main__":
    build_all_aituko_lottie()
'''

with open('scripts/generate_aituko_lottie.py', 'w', encoding='utf-8') as f:
    f.write(script_content)

print('Successfully generated scripts/generate_aituko_lottie.py')
