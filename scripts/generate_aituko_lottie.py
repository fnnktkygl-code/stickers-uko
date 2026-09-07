#!/usr/bin/env python3
"""
AItuko High-Fidelity Vector Lottie Generator (13 States)
Conforms strictly to Bodymovin / LottieFiles v5.7+ JSON specification.
100% pure vector mascot: NO hands, fingers, or thumbs!
Floating porcelain Japandi aesthetic matching exact user reference.

Dimensions & Coordinates (Measured on 512x512 canvas):
- Center X = 256
- Ground Shadow: Center (256, 468), width 180, height 28.
- Floating Foot Pods: X = 228 & 284 (offset ±28), Y = 412, width 34, height 44, tilt ±10°.
- Slender Neck: Center (256, 202), width 32, height 20, roundness 9.
- Porcelain Torso: Center (256, 298), width 124, height 176, roundness 62.
- Porcelain Head: Center (256, 126), width 236, height 164, roundness 72.
- Visor Faceplate: Center (256, 126), width 188, height 126, roundness 56.
- Electric Cyan Eyes: Center (214, 126) & (298, 126) (offset ±42), arc apex (-42, -10) & (42, -10).
- Floating Lateral Pods: Rest X = 138 & 374 (offset ±118), Y = 298, width 34, height 108, roundness 17, tilt ±9°.

Kinematic Specification:
- 120-frame (4.0s @ 30fps) seamless harmonic loop.
- Sinusoidal floating: Apex at frame 27 (-14px), Nadir at frame 84 (+14px).
- Inertial Lateral Pod Flaring: Pod span widens at apex, tucks in at nadir; tilt ±9° to ±13°.
- Inertial Head Tilt: 4-frame phase lag, pitch ±1.8°.
- Dynamic Shadow Coupling: Scale 84% & opacity 55% at apex <-> scale 108% & opacity 98% at nadir.
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
COLOR_SPECULAR_MED      = hex_to_lottie_color("#FFFFFF", 0.60)
COLOR_SPECULAR_SOFT     = hex_to_lottie_color("#FFFFFF", 0.25)

COLOR_VISOR_BEZEL       = hex_to_lottie_color("#090A0F", 1.0)
COLOR_VISOR_GLASS       = hex_to_lottie_color("#10121A", 1.0)
COLOR_VISOR_SPECULAR    = hex_to_lottie_color("#383D4E", 0.55)
COLOR_VISOR_GLOSS_ARC   = hex_to_lottie_color("#64748B", 0.30)

COLOR_CYAN_CORE         = hex_to_lottie_color("#00F0FF", 1.0)
COLOR_CYAN_HIGHLIGHT    = hex_to_lottie_color("#E0F7FF", 1.0)
COLOR_CYAN_GLOW         = hex_to_lottie_color("#00E5FF", 0.40)
COLOR_CYAN_AMB          = hex_to_lottie_color("#00F0FF", 0.30)

COLOR_SHADOW            = hex_to_lottie_color("#0F172A", 0.22)
COLOR_SHADOW_SOFT       = hex_to_lottie_color("#0F172A", 0.08)
COLOR_NECK_SHADOW       = hex_to_lottie_color("#0F172A", 0.25)

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
    Smooth sinusoidal acceleration.
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
            "lc": stroke.get("lc", 2),
            "lj": stroke.get("lj", 2),
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
        "ty": 4,
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


# --- High-Fidelity Character Rig Constructor (Hands-Free Pure Vector) ---

def build_ground_shadow():
    """Ground ambient occlusion shadow scaling inversely with floating height."""
    shadow_shapes = [
        make_shape_group("Soft Occlusion Core", make_ellipse_shape(140, 20), COLOR_SHADOW),
        make_shape_group("Wide Ambient Blur", make_ellipse_shape(180, 28), COLOR_SHADOW_SOFT)
    ]
    scale_kf = [
        kf(0,   [100, 100, 100], [84, 84, 100]),
        kf(27,  [84, 84, 100],   [100, 100, 100]),
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
            "p": {"a": 0, "k": [256, 468, 0]},
            "a": {"a": 0, "k": [0, 0, 0]},
            "s": {"a": 1, "k": scale_kf}
        }
    )

def build_support_pods(pos_kf=None, rot_kf=None):
    """
    Two distinct floating porcelain pod feet hovering under torso.
    Center (256, 412). Left foot pod at (-28, 0), Right foot pod at (+28, 0).
    """
    pod_shapes = [
        # Left Foot Pod (tilted -10 deg)
        make_shape_group("Left Foot Thruster Glow", make_ellipse_shape(28, 10, pos=(-28, 22)), COLOR_CYAN_AMB,
                         transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [-28, 22]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": -10}, "o": {"a": 0, "k": 100}}),
        make_shape_group("Left Foot Pod Shell", make_rect_shape(38, 46, roundness=19, pos=(-28, 0)), COLOR_PORCELAIN_SHADOW,
                         transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [-28, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": -10}, "o": {"a": 0, "k": 100}}),
        make_shape_group("Left Foot Porcelain Body", make_rect_shape(34, 44, roundness=17, pos=(-28, 0)), COLOR_WHITE,
                         transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [-28, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": -10}, "o": {"a": 0, "k": 100}}),
        make_shape_group("Left Foot Specular Gloss", make_ellipse_shape(18, 8, pos=(-28, -12)), COLOR_SPECULAR_HIGH,
                         transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [-28, -12]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": -10}, "o": {"a": 0, "k": 85}}),
        
        # Right Foot Pod (tilted +10 deg)
        make_shape_group("Right Foot Thruster Glow", make_ellipse_shape(28, 10, pos=(28, 22)), COLOR_CYAN_AMB,
                         transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [28, 22]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 10}, "o": {"a": 0, "k": 100}}),
        make_shape_group("Right Foot Pod Shell", make_rect_shape(38, 46, roundness=19, pos=(28, 0)), COLOR_PORCELAIN_SHADOW,
                         transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [28, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 10}, "o": {"a": 0, "k": 100}}),
        make_shape_group("Right Foot Porcelain Body", make_rect_shape(34, 44, roundness=17, pos=(28, 0)), COLOR_WHITE,
                         transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [28, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 10}, "o": {"a": 0, "k": 100}}),
        make_shape_group("Right Foot Specular Gloss", make_ellipse_shape(18, 8, pos=(28, -12)), COLOR_SPECULAR_HIGH,
                         transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [28, -12]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 10}, "o": {"a": 0, "k": 85}}),
    ]
    return make_layer(
        ind=2,
        name="Floating Foot Pods",
        shapes=pod_shapes,
        ks={
            "o": {"a": 0, "k": 100},
            "r": rot_kf or {"a": 0, "k": 0},
            "p": pos_kf or {"a": 0, "k": [256, 412, 0]},
            "a": {"a": 0, "k": [0, 0, 0]},
            "s": {"a": 0, "k": [100, 100, 100]}
        }
    )

def build_slender_neck(pos_kf=None, rot_kf=None):
    """
    Slender neck connecting head and torso.
    Visible cylinder: width 32, height 20, centered at Y=202 on 512 canvas.
    """
    neck_shapes = [
        make_shape_group("Neck Shadow Rim", make_rect_shape(36, 22, roundness=10, pos=(0, 0)), COLOR_PORCELAIN_SHADOW),
        make_shape_group("Neck Porcelain Cylinder", make_rect_shape(32, 20, roundness=9, pos=(0, 0)), COLOR_PORCELAIN_BASE),
        make_shape_group("Neck Under-Chin Shadow", make_ellipse_shape(32, 6, pos=(0, -8)), COLOR_NECK_SHADOW)
    ]
    return make_layer(
        ind=3,
        name="Slender Neck",
        shapes=neck_shapes,
        ks={
            "o": {"a": 0, "k": 100},
            "r": rot_kf or {"a": 0, "k": 0},
            "p": pos_kf or {"a": 0, "k": [256, 202, 0]},
            "a": {"a": 0, "k": [0, 0, 0]},
            "s": {"a": 0, "k": [100, 100, 100]}
        }
    )

def build_porcelain_torso(pos_kf=None, rot_kf=None, scale_kf=None):
    """
    Torso capsule body: width 124, height 176, roundness 62, centered at Y=298 on 512 canvas.
    Chibi ratio (head 236 wide : torso 124 wide = ~1.9:1).
    """
    torso_shapes = [
        make_shape_group("Torso Shadow Base", make_rect_shape(128, 180, roundness=64, pos=(0, 0)), COLOR_PORCELAIN_SHADOW),
        make_shape_group("Torso Porcelain Shell", make_rect_shape(124, 176, roundness=62, pos=(0, 0)), COLOR_PORCELAIN_BASE),
        make_shape_group("Torso Left Shade", make_rect_shape(38, 152, roundness=19, pos=(-38, 0)), hex_to_lottie_color("#E2E8F0", 0.45)),
        make_shape_group("Torso Specular Gloss", make_rect_shape(12, 124, roundness=6, pos=(44, 0)), COLOR_SPECULAR_HIGH),
        make_shape_group("Torso Shoulder Soft", make_ellipse_shape(72, 16, pos=(0, -72)), COLOR_SPECULAR_MED),
        make_shape_group("Torso Neck AO Shadow", make_ellipse_shape(60, 12, pos=(0, -88)), COLOR_NECK_SHADOW)
    ]
    return make_layer(
        ind=4,
        name="Porcelain Torso",
        shapes=torso_shapes,
        ks={
            "o": {"a": 0, "k": 100},
            "r": rot_kf or {"a": 0, "k": 0},
            "p": pos_kf or {"a": 0, "k": [256, 298, 0]},
            "a": {"a": 0, "k": [0, 0, 0]},
            "s": scale_kf or {"a": 0, "k": [100, 100, 100]}
        }
    )

def build_porcelain_head(head_pos_kf=None, head_rot_kf=None):
    """
    Oblate porcelain helmet dome: width 236, height 164, roundness 72, centered at Y=126 on 512 canvas.
    """
    head_shapes = [
        make_shape_group("Helmet Shadow Base", make_rect_shape(240, 168, roundness=74, pos=(0, 0)), COLOR_PORCELAIN_SHADOW),
        make_shape_group("Helmet Porcelain Dome", make_rect_shape(236, 164, roundness=72, pos=(0, 0)), COLOR_WHITE),
        make_shape_group("Crown Specular Highlight", make_ellipse_shape(110, 24, pos=(-14, -66)), COLOR_SPECULAR_HIGH),
        make_shape_group("Right Temple Gloss", make_ellipse_shape(16, 44, pos=(90, -26)), COLOR_SPECULAR_MED,
                         transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [90, -26]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 16}, "o": {"a": 0, "k": 65}}),
        make_shape_group("Left Cheek Shade", make_ellipse_shape(24, 52, pos=(-94, -8)), hex_to_lottie_color("#E2E8F0", 0.40)),
        make_shape_group("Chin Soft Ambient", make_ellipse_shape(92, 12, pos=(0, 78)), hex_to_lottie_color("#CBD5E1", 0.50))
    ]
    return make_layer(
        ind=5,
        name="Porcelain Head",
        shapes=head_shapes,
        ks={
            "o": {"a": 0, "k": 100},
            "r": head_rot_kf or {"a": 0, "k": 0},
            "p": head_pos_kf or {"a": 0, "k": [256, 126, 0]},
            "a": {"a": 0, "k": [0, 0, 0]},
            "s": {"a": 0, "k": [100, 100, 100]}
        }
    )

def build_visor_glass(head_pos_kf=None, head_rot_kf=None):
    """
    Recessed black curved glass screen: width 188, height 126, roundness 56, centered at Y=126 on 512 canvas.
    """
    visor_shapes = [
        make_shape_group("Visor Bezel", make_rect_shape(192, 130, roundness=58, pos=(0, 0)), COLOR_VISOR_BEZEL),
        make_shape_group("Visor Core Glass", make_rect_shape(188, 126, roundness=56, pos=(0, 0)), COLOR_VISOR_GLASS),
        make_shape_group("Visor Specular Gloss Arc", make_ellipse_shape(132, 34, pos=(0, -34)), COLOR_VISOR_SPECULAR),
        make_shape_group("Visor Glass Gleam", make_ellipse_shape(84, 12, pos=(0, -47)), COLOR_VISOR_GLOSS_ARC)
    ]
    return make_layer(
        ind=6,
        name="Visor Glass",
        shapes=visor_shapes,
        ks={
            "o": {"a": 0, "k": 100},
            "r": head_rot_kf or {"a": 0, "k": 0},
            "p": head_pos_kf or {"a": 0, "k": [256, 126, 0]},
            "a": {"a": 0, "k": [0, 0, 0]},
            "s": {"a": 0, "k": [100, 100, 100]}
        }
    )

def build_cyan_eyes(eyes_pos_kf=None, eyes_rot_kf=None, eyes_scale_kf=None, eye_type="arch"):
    """
    Electric Cyan LED eyes with neon bloom.
    Eye center: Y=126 on 512 canvas. Left eye X=-42 (canvas 214), Right eye X=+42 (canvas 298).
    Zero-displacement blink scaling centered at (0, 0).
    """
    shapes = []
    
    if eye_type == "arch":
        # Smiling crescent arch paths matching the master 3D render:
        # Left eye: from X=-62 to X=-26, apex at (-42, -10)
        left_arc_v = [[-62, 5], [-42, -10], [-26, 5]]
        left_arc_i = [[0, 0], [-9, 0], [0, 0]]
        left_arc_o = [[0, 0], [9, 0], [0, 0]]
        
        # Right eye: from X=22 to X=58, apex at (42, -10)
        right_arc_v = [[22, 5], [42, -10], [58, 5]]
        right_arc_i = [[0, 0], [-9, 0], [0, 0]]
        right_arc_o = [[0, 0], [9, 0], [0, 0]]
        
        shapes.append(make_shape_group("Left Eye Bloom", make_path_shape(left_arc_v, left_arc_i, left_arc_o),
                                       stroke={"color": COLOR_CYAN_GLOW, "width": 16, "lc": 2, "lj": 2}))
        shapes.append(make_shape_group("Right Eye Bloom", make_path_shape(right_arc_v, right_arc_i, right_arc_o),
                                       stroke={"color": COLOR_CYAN_GLOW, "width": 16, "lc": 2, "lj": 2}))
        shapes.append(make_shape_group("Left Eye Core", make_path_shape(left_arc_v, left_arc_i, left_arc_o),
                                       stroke={"color": COLOR_CYAN_CORE, "width": 8.5, "lc": 2, "lj": 2}))
        shapes.append(make_shape_group("Right Eye Core", make_path_shape(right_arc_v, right_arc_i, right_arc_o),
                                       stroke={"color": COLOR_CYAN_CORE, "width": 8.5, "lc": 2, "lj": 2}))
        shapes.append(make_shape_group("Left Eye Highlight", make_path_shape(left_arc_v, left_arc_i, left_arc_o),
                                       stroke={"color": COLOR_CYAN_HIGHLIGHT, "width": 3.2, "lc": 2, "lj": 2}))
        shapes.append(make_shape_group("Right Eye Highlight", make_path_shape(right_arc_v, right_arc_i, right_arc_o),
                                       stroke={"color": COLOR_CYAN_HIGHLIGHT, "width": 3.2, "lc": 2, "lj": 2}))

    elif eye_type == "down_arch":
        left_arc_v = [[-62, -8], [-42, 7], [-26, -8]]
        left_arc_i = [[0, 0], [-9, 0], [0, 0]]
        left_arc_o = [[0, 0], [9, 0], [0, 0]]
        
        right_arc_v = [[22, -8], [42, 7], [58, -8]]
        right_arc_i = [[0, 0], [-9, 0], [0, 0]]
        right_arc_o = [[0, 0], [9, 0], [0, 0]]
        
        shapes.append(make_shape_group("Left Eye Bloom", make_path_shape(left_arc_v, left_arc_i, left_arc_o),
                                       stroke={"color": COLOR_CYAN_GLOW, "width": 16, "lc": 2, "lj": 2}))
        shapes.append(make_shape_group("Right Eye Bloom", make_path_shape(right_arc_v, right_arc_i, right_arc_o),
                                       stroke={"color": COLOR_CYAN_GLOW, "width": 16, "lc": 2, "lj": 2}))
        shapes.append(make_shape_group("Left Eye Core", make_path_shape(left_arc_v, left_arc_i, left_arc_o),
                                       stroke={"color": COLOR_CYAN_CORE, "width": 8.5, "lc": 2, "lj": 2}))
        shapes.append(make_shape_group("Right Eye Core", make_path_shape(right_arc_v, right_arc_i, right_arc_o),
                                       stroke={"color": COLOR_CYAN_CORE, "width": 8.5, "lc": 2, "lj": 2}))
        shapes.append(make_shape_group("Left Eye Highlight", make_path_shape(left_arc_v, left_arc_i, left_arc_o),
                                       stroke={"color": COLOR_CYAN_HIGHLIGHT, "width": 3.2, "lc": 2, "lj": 2}))
        shapes.append(make_shape_group("Right Eye Highlight", make_path_shape(right_arc_v, right_arc_i, right_arc_o),
                                       stroke={"color": COLOR_CYAN_HIGHLIGHT, "width": 3.2, "lc": 2, "lj": 2}))

    elif eye_type == "pill":
        shapes.append(make_shape_group("Left Eye Bloom", make_ellipse_shape(38, 44, pos=(-42, 0)), COLOR_CYAN_GLOW))
        shapes.append(make_shape_group("Right Eye Bloom", make_ellipse_shape(38, 44, pos=(42, 0)), COLOR_CYAN_GLOW))
        shapes.append(make_shape_group("Left Eye Core", make_rect_shape(24, 34, roundness=12, pos=(-42, 0)), COLOR_CYAN_CORE))
        shapes.append(make_shape_group("Right Eye Core", make_rect_shape(24, 34, roundness=12, pos=(42, 0)), COLOR_CYAN_CORE))
        shapes.append(make_shape_group("Left Eye Highlight", make_ellipse_shape(9, 14, pos=(-38, -5)), COLOR_CYAN_HIGHLIGHT))
        shapes.append(make_shape_group("Right Eye Highlight", make_ellipse_shape(9, 14, pos=(46, -5)), COLOR_CYAN_HIGHLIGHT))

    elif eye_type == "line":
        shapes.append(make_shape_group("Left Eye Line Bloom", make_rect_shape(38, 10, roundness=5, pos=(-42, 0)), COLOR_CYAN_GLOW))
        shapes.append(make_shape_group("Right Eye Line Bloom", make_rect_shape(38, 10, roundness=5, pos=(42, 0)), COLOR_CYAN_GLOW))
        shapes.append(make_shape_group("Left Eye Line", make_rect_shape(32, 6, roundness=3, pos=(-42, 0)), COLOR_CYAN_CORE))
        shapes.append(make_shape_group("Right Eye Line", make_rect_shape(32, 6, roundness=3, pos=(42, 0)), COLOR_CYAN_CORE))

    elif eye_type == "question":
        left_q_v = [[-48, -12], [-42, -19], [-36, -12], [-42, -3], [-42, 4]]
        shapes.append(make_shape_group("Left Q Bloom", make_path_shape(left_q_v), stroke={"color": COLOR_CYAN_GLOW, "width": 12, "lc": 2}))
        shapes.append(make_shape_group("Left Q Core", make_path_shape(left_q_v), stroke={"color": COLOR_CYAN_CORE, "width": 7.0, "lc": 2}))
        shapes.append(make_shape_group("Left Q Dot", make_ellipse_shape(5, 5, pos=(-42, 12)), COLOR_CYAN_CORE))
        
        right_q_v = [[36, -12], [42, -19], [48, -12], [42, -3], [42, 4]]
        shapes.append(make_shape_group("Right Q Bloom", make_path_shape(right_q_v), stroke={"color": COLOR_CYAN_GLOW, "width": 12, "lc": 2}))
        shapes.append(make_shape_group("Right Q Core", make_path_shape(right_q_v), stroke={"color": COLOR_CYAN_CORE, "width": 7.0, "lc": 2}))
        shapes.append(make_shape_group("Right Q Dot", make_ellipse_shape(5, 5, pos=(42, 12)), COLOR_CYAN_CORE))

    elif eye_type == "guardian":
        shapes.append(make_shape_group("Left Eye Bloom", make_ellipse_shape(38, 40, pos=(-42, 0)), COLOR_CYAN_GLOW,
                                       transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [-42, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 16}, "o": {"a": 0, "k": 100}}))
        shapes.append(make_shape_group("Right Eye Bloom", make_ellipse_shape(38, 40, pos=(42, 0)), COLOR_CYAN_GLOW,
                                       transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [42, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": -16}, "o": {"a": 0, "k": 100}}))
        shapes.append(make_shape_group("Left Eye Core", make_rect_shape(24, 30, roundness=10, pos=(-42, 0)), COLOR_CYAN_CORE,
                                       transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [-42, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 16}, "o": {"a": 0, "k": 100}}))
        shapes.append(make_shape_group("Right Eye Core", make_rect_shape(24, 30, roundness=10, pos=(42, 0)), COLOR_CYAN_CORE,
                                       transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [42, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": -16}, "o": {"a": 0, "k": 100}}))
        shapes.append(make_shape_group("Left Eye Highlight", make_ellipse_shape(8, 11, pos=(-39, -4)), COLOR_CYAN_HIGHLIGHT,
                                       transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [-39, -4]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 16}, "o": {"a": 0, "k": 100}}))
        shapes.append(make_shape_group("Right Eye Highlight", make_ellipse_shape(8, 11, pos=(39, -4)), COLOR_CYAN_HIGHLIGHT,
                                       transform={"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [39, -4]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": -16}, "o": {"a": 0, "k": 100}}))

    return make_layer(
        ind=7,
        name="Cyan Eyes",
        shapes=shapes,
        ks={
            "o": {"a": 0, "k": 100},
            "r": eyes_rot_kf or {"a": 0, "k": 0},
            "p": eyes_pos_kf or {"a": 0, "k": [256, 126, 0]},
            "a": {"a": 0, "k": [0, 0, 0]},
            "s": eyes_scale_kf or {"a": 0, "k": [100, 100, 100]}
        }
    )

def build_floating_lateral_pod(ind, name, is_right=False, pos_kf=None, rot_kf=None):
    """
    Independent floating porcelain lateral pod (winglet / thruster) on robot flank.
    CRITICAL: NO hands, fingers, or thumbs! Smooth streamlined aerodynamic pod.
    Width 34, Height 108, roundness 17.
    Rest X = 138 (left) or 374 (right). Rest Y = 298. Tilt = ±9°.
    Pivots around anchor [0, -50, 0].
    """
    rest_x = 118 if is_right else -118
    rest_rot = 9 if is_right else -9
    streak_x = 8 if is_right else -8
    shade_x = -9 if is_right else 9
    
    shapes = [
        # Pod bottom thruster glow
        make_shape_group(f"{name} Thruster Glow", make_ellipse_shape(20, 8, pos=(0, 56)), COLOR_CYAN_AMB),
        # Shadow rim base
        make_shape_group(f"{name} Shadow Rim", make_rect_shape(38, 112, roundness=19, pos=(0, 0)), COLOR_PORCELAIN_SHADOW),
        # Main porcelain shell
        make_shape_group(f"{name} Porcelain Body", make_rect_shape(34, 108, roundness=17, pos=(0, 0)), COLOR_WHITE),
        # Glossy specular reflection streak
        make_shape_group(f"{name} Specular Streak", make_rect_shape(6, 74, roundness=3, pos=(streak_x, -4)), COLOR_SPECULAR_HIGH),
        # Inner flank soft shade
        make_shape_group(f"{name} Inner Flank Shade", make_rect_shape(9, 80, roundness=4.5, pos=(shade_x, 2)), hex_to_lottie_color("#E2E8F0", 0.35))
    ]
    
    default_p = [256 + rest_x, 298, 0]
    
    return make_layer(
        ind=ind,
        name=name,
        shapes=shapes,
        ks={
            "o": {"a": 0, "k": 100},
            "r": rot_kf or {"a": 0, "k": rest_rot},
            "p": pos_kf or {"a": 0, "k": default_p},
            "a": {"a": 0, "k": [0, -50, 0]},  # Flank pivot anchor
            "s": {"a": 0, "k": [100, 100, 100]}
        }
    )


# --- 13 State Generation Engine (120 Frames / 4.0s Seamless Loop) ---

def generate_state(state_name):
    """
    Generates a high-fidelity 120-frame (4.0s @ 30fps) seamless loop Lottie document for state.
    """
    # 1. Base Levitation Kinematics (Harmonic 4.0s cycle matching 3D video)
    # Apex at f27 (-14px: Y=284), nadir at f84 (+14px: Y=312)
    torso_p_kf = {
        "a": 1,
        "k": [
            kf(0,   [256, 298, 0], [256, 284, 0]),
            kf(27,  [256, 284, 0], [256, 298, 0]),
            kf(58,  [256, 298, 0], [256, 312, 0]),
            kf(84,  [256, 312, 0], [256, 298, 0]),
            kf(120, [256, 298, 0])
        ]
    }
    
    # Slender neck tracks torso
    neck_p_kf = {
        "a": 1,
        "k": [
            kf(0,   [256, 202, 0], [256, 188, 0]),
            kf(27,  [256, 188, 0], [256, 202, 0]),
            kf(58,  [256, 202, 0], [256, 216, 0]),
            kf(84,  [256, 216, 0], [256, 202, 0]),
            kf(120, [256, 202, 0])
        ]
    }
    
    # Head lags torso by 4 frames with organic curiosity sway
    head_p_kf = {
        "a": 1,
        "k": [
            kf(0,   [256, 126, 0], [256, 111, 0]),
            kf(31,  [256, 111, 0], [256, 126, 0]),
            kf(62,  [256, 126, 0], [256, 140, 0]),
            kf(88,  [256, 140, 0], [256, 126, 0]),
            kf(120, [256, 126, 0])
        ]
    }
    head_r_kf = {
        "a": 1,
        "k": [
            kf(0,   0,    -1.8),
            kf(27,  -1.8, 0),
            kf(58,  0,    1.8),
            kf(84,  1.8,  0),
            kf(120, 0)
        ]
    }
    
    # Eyes position & rotation match head
    eyes_p_kf = copy.deepcopy(head_p_kf)
    eyes_r_kf = copy.deepcopy(head_r_kf)
    
    # Feet support pods have 3 frames lag
    pods_p_kf = {
        "a": 1,
        "k": [
            kf(0,   [256, 412, 0], [256, 399, 0]),
            kf(30,  [256, 399, 0], [256, 412, 0]),
            kf(61,  [256, 412, 0], [256, 425, 0]),
            kf(87,  [256, 425, 0], [256, 412, 0]),
            kf(120, [256, 412, 0])
        ]
    }
    
    # Left & Right floating lateral pods lag by 6 frames with gentle breathing flare
    lpod_p_kf = {
        "a": 1,
        "k": [
            kf(0,   [138, 298, 0], [134, 283, 0]),
            kf(33,  [134, 283, 0], [138, 298, 0]),
            kf(64,  [138, 298, 0], [140, 312, 0]),
            kf(90,  [140, 312, 0], [138, 298, 0]),
            kf(120, [138, 298, 0])
        ]
    }
    lpod_r_kf = {
        "a": 1,
        "k": [
            kf(0,   -9,  -13),
            kf(33,  -13, -9),
            kf(64,  -9,  -6),
            kf(90,  -6,  -9),
            kf(120, -9)
        ]
    }
    
    rpod_p_kf = {
        "a": 1,
        "k": [
            kf(0,   [374, 298, 0], [378, 283, 0]),
            kf(33,  [378, 283, 0], [374, 298, 0]),
            kf(64,  [374, 298, 0], [372, 312, 0]),
            kf(90,  [372, 312, 0], [374, 298, 0]),
            kf(120, [374, 298, 0])
        ]
    }
    rpod_r_kf = {
        "a": 1,
        "k": [
            kf(0,   9,   13),
            kf(33,  13,  9),
            kf(64,  9,   6),
            kf(90,  6,   9),
            kf(120, 9)
        ]
    }
    
    # Natural organic double-blink during nadir turnaround (frames 78-87)
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
        pass
        
    elif state_name == "01_waving":
        head_r_kf = {"a": 1, "k": [kf(0, 0, 3.5), kf(25, 3.5, 3.5), kf(95, 3.5, 0), kf(120, 0)]}
        eyes_r_kf = copy.deepcopy(head_r_kf)
        # Right lateral pod rises up and flutters in greeting
        rpod_p_kf = {
            "a": 1,
            "k": [
                kf(0,   [374, 298, 0], [382, 235, 0]),
                kf(25,  [382, 235, 0], [382, 225, 0]),
                kf(65,  [382, 225, 0], [382, 235, 0]),
                kf(95,  [382, 235, 0], [374, 298, 0]),
                kf(120, [374, 298, 0])
            ]
        }
        rpod_r_kf = {
            "a": 1,
            "k": [
                kf(0,   9,   28),
                kf(25,  28,  -14),
                kf(42,  -14, 26),
                kf(58,  26,  -12),
                kf(74,  -12, 24),
                kf(95,  24,  9),
                kf(120, 9)
            ]
        }
        
    elif state_name == "02_celebrating":
        torso_p_kf = {
            "a": 1,
            "k": [
                kf(0,   [256, 298, 0], [256, 265, 0]),
                kf(40,  [256, 265, 0], [256, 298, 0]),
                kf(85,  [256, 298, 0]),
                kf(120, [256, 298, 0])
            ]
        }
        neck_p_kf = copy.deepcopy(torso_p_kf)
        head_p_kf = {
            "a": 1,
            "k": [
                kf(0,   [256, 126, 0], [256, 95, 0]),
                kf(40,  [256, 95, 0], [256, 126, 0]),
                kf(85,  [256, 126, 0]),
                kf(120, [256, 126, 0])
            ]
        }
        eyes_p_kf = copy.deepcopy(head_p_kf)
        pods_p_kf = copy.deepcopy(torso_p_kf)
        
        # Both lateral pods flare upward in celebratory winglet lift
        lpod_p_kf = {
            "a": 1,
            "k": [
                kf(0,   [138, 298, 0], [122, 220, 0]),
                kf(35,  [122, 220, 0], [138, 298, 0]),
                kf(95,  [138, 298, 0]),
                kf(120, [138, 298, 0])
            ]
        }
        lpod_r_kf = {"a": 1, "k": [kf(0, -9, -42), kf(35, -42, -9), kf(120, -9)]}
        rpod_p_kf = {
            "a": 1,
            "k": [
                kf(0,   [374, 298, 0], [390, 220, 0]),
                kf(35,  [390, 220, 0], [374, 298, 0]),
                kf(95,  [374, 298, 0]),
                kf(120, [374, 298, 0])
            ]
        }
        rpod_r_kf = {"a": 1, "k": [kf(0, 9, 42), kf(35, 42, 9), kf(120, 9)]}
        
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
                "p": {"a": 1, "k": [kf(0, [256, 260, 0], [256, 320, 0]), kf(90, [256, 320, 0]), kf(120, [256, 320, 0])]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {"a": 1, "k": [kf(0, [40, 40, 100], [120, 120, 100]), kf(30, [120, 120, 100], [100, 100, 100]), kf(120, [100, 100, 100])]}
            }
        ))

    elif state_name == "03_ai_thinking":
        eye_type = "pill"
        head_r_kf = {"a": 1, "k": [kf(0, 0, -5.0), kf(60, -5.0, 0), kf(120, 0)]}
        eyes_r_kf = copy.deepcopy(head_r_kf)
        
        # Right lateral pod tucks inward toward chin/visor level
        rpod_p_kf = {
            "a": 1,
            "k": [
                kf(0,   [374, 298, 0], [340, 245, 0]),
                kf(30,  [340, 245, 0], [340, 240, 0]),
                kf(90,  [340, 240, 0], [374, 298, 0]),
                kf(120, [374, 298, 0])
            ]
        }
        rpod_r_kf = {"a": 1, "k": [kf(0, 9, -24), kf(30, -24, -20), kf(90, -20, 9), kf(120, 9)]}
        
        # 3 Holographic glowing cyan data cubes orbiting in 3D around head
        orbit_frames = [0, 15, 30, 45, 60, 75, 90, 105, 120]
        for cube_idx in range(3):
            phase_offset = (cube_idx / 3.0) * math.pi * 2
            raw_p = []
            raw_s = []
            raw_o = []
            for fr in orbit_frames:
                rad = (fr / 120.0) * math.pi * 2 + phase_offset
                ox = round(math.cos(rad) * 115, 2)
                oy = round(math.sin(rad) * 36 - 126, 2)
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
        head_r_kf = {"a": 1, "k": [kf(0, 0, -4.5), kf(30, -4.5, 4.5), kf(85, 4.5, 0), kf(120, 0)]}
        eyes_r_kf = copy.deepcopy(head_r_kf)
        lpod_r_kf = {"a": 1, "k": [kf(0, -9, 14), kf(60, 14, -9), kf(120, -9)]}
        rpod_r_kf = {"a": 1, "k": [kf(0, 9, -14), kf(60, -14, 9), kf(120, 9)]}
        
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
                "p": {"a": 1, "k": [kf(0, [256, 305, 0], [256, 295, 0]), kf(60, [256, 295, 0], [256, 305, 0]), kf(120, [256, 305, 0])]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {"a": 1, "k": [kf(0, [98, 98, 100], [104, 104, 100]), kf(60, [104, 104, 100], [98, 98, 100]), kf(120, [98, 98, 100])]}
            }
        ))

    elif state_name == "05_thumbs_up":
        # AItuko has NO hands! Proud Winglet Affirmation / Success Salute
        head_r_kf = {
            "a": 1,
            "k": [
                kf(0,   0,   3.5),
                kf(30,  3.5, -2.0),
                kf(70,  -2.0, 2.0),
                kf(95,  2.0, 0),
                kf(120, 0)
            ]
        }
        eyes_r_kf = copy.deepcopy(head_r_kf)
        # Right lateral pod tilts up proudly in success affirmation
        rpod_p_kf = {
            "a": 1,
            "k": [
                kf(0,   [374, 298, 0], [382, 250, 0]),
                kf(30,  [382, 250, 0], [382, 240, 0]),
                kf(70,  [382, 240, 0], [382, 250, 0]),
                kf(100, [382, 250, 0], [374, 298, 0]),
                kf(120, [374, 298, 0])
            ]
        }
        rpod_r_kf = {
            "a": 1,
            "k": [
                kf(0,   9,  34),
                kf(30,  34, 34),
                kf(100, 34, 9),
                kf(120, 9)
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
                "p": {"a": 1, "k": [kf(0, [256, 65, 0], [256, 55, 0]), kf(60, [256, 55, 0], [256, 65, 0]), kf(120, [256, 65, 0])]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {"a": 1, "k": [kf(0, [60, 60, 100], [112, 112, 100]), kf(25, [112, 112, 100], [100, 100, 100]), kf(120, [100, 100, 100])]}
            }
        ))

    elif state_name == "06_sleeping":
        eye_type = "line"
        head_r_kf = {"a": 0, "k": 7.0}
        eyes_r_kf = {"a": 0, "k": 7.0}
        torso_p_kf = {
            "a": 1,
            "k": [
                kf(0,   [256, 302, 0], [256, 294, 0]),
                kf(60,  [256, 294, 0], [256, 302, 0]),
                kf(120, [256, 302, 0])
            ]
        }
        neck_p_kf = copy.deepcopy(torso_p_kf)
        head_p_kf = {
            "a": 1,
            "k": [
                kf(0,   [256, 128, 0], [256, 120, 0]),
                kf(60,  [256, 120, 0], [256, 128, 0]),
                kf(120, [256, 128, 0])
            ]
        }
        eyes_p_kf = copy.deepcopy(head_p_kf)
        pods_p_kf = copy.deepcopy(torso_p_kf)
        
        # 3 Floating Zzz bubbles
        for z_i in range(3):
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
        # Robotic directional indication: right lateral pod aims outward toward targeting reticle
        rpod_p_kf = {
            "a": 1,
            "k": [
                kf(0,   [374, 298, 0], [398, 275, 0]),
                kf(25,  [398, 275, 0], [398, 270, 0]),
                kf(75,  [398, 270, 0], [398, 275, 0]),
                kf(100, [398, 275, 0], [374, 298, 0]),
                kf(120, [374, 298, 0])
            ]
        }
        rpod_r_kf = {
            "a": 1,
            "k": [
                kf(0,   9,  42),
                kf(25,  42, 42),
                kf(100, 42, 9),
                kf(120, 9)
            ]
        }
        # Holographic cyan crosshair reticle pulsing
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
                "p": {"a": 1, "k": [kf(0, [430, 255, 0], [440, 250, 0]), kf(60, [440, 250, 0], [430, 255, 0]), kf(120, [430, 255, 0])]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {"a": 1, "k": [kf(0, [70, 70, 100], [105, 105, 100]), kf(60, [105, 105, 100], [70, 70, 100]), kf(120, [70, 70, 100])]}
            }
        ))

    elif state_name == "08_searching":
        # Scanning radar sweep with robotic head pan
        head_r_kf = {
            "a": 1,
            "k": [
                kf(0,   0,   -10.0),
                kf(30,  -10.0, 10.0),
                kf(90,  10.0,  0),
                kf(120, 0)
            ]
        }
        eyes_r_kf = copy.deepcopy(head_r_kf)
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
                "p": {"a": 0, "k": [256, 145, 0]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {"a": 1, "k": [kf(0, [85, 85, 100], [115, 115, 100]), kf(60, [115, 115, 100], [85, 85, 100]), kf(120, [85, 85, 100])]}
            }
        ))

    elif state_name == "09_loading":
        # Dual holographic cyan gyroscopic rings spinning in 3D around core
        gyro_shapes1 = [
            make_shape_group("Gyro Ring 1 Glow", make_ellipse_shape(150, 56), None, stroke={"color": COLOR_CYAN_GLOW, "width": 8}),
            make_shape_group("Gyro Ring 1 Core", make_ellipse_shape(144, 50), None, stroke={"color": COLOR_CYAN_CORE, "width": 3.5}),
            make_shape_group("Gyro Particle 1", make_ellipse_shape(10, 10, pos=(70, 0)), COLOR_CYAN_HIGHLIGHT)
        ]
        gyro_shapes2 = [
            make_shape_group("Gyro Ring 2 Glow", make_ellipse_shape(130, 46), None, stroke={"color": COLOR_CYAN_GLOW, "width": 8}),
            make_shape_group("Gyro Ring 2 Core", make_ellipse_shape(124, 40), None, stroke={"color": COLOR_CYAN_CORE, "width": 3.5}),
            make_shape_group("Gyro Particle 2", make_ellipse_shape(10, 10, pos=(-60, 0)), COLOR_CYAN_HIGHLIGHT)
        ]
        extra_layers.append(make_layer(
            ind=19,
            name="Gyroscopic Ring Outer",
            shapes=gyro_shapes1,
            ks={
                "o": {"a": 0, "k": 85},
                "r": {"a": 1, "k": [kf(0, 0, 360), kf(120, 360)]},
                "p": {"a": 0, "k": [256, 298, 0]},
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
                "p": {"a": 0, "k": [256, 298, 0]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {"a": 0, "k": [100, 100, 100]}
            }
        ))

    elif state_name == "10_idea":
        head_r_kf = {"a": 1, "k": [kf(0, 0, -3.5), kf(25, -3.5, 2.5), kf(80, 2.5, 0), kf(120, 0)]}
        eyes_r_kf = copy.deepcopy(head_r_kf)
        
        bulb_shapes = [
            make_shape_group("Bulb Glow Aura", make_ellipse_shape(80, 80), COLOR_GOLD_GLOW),
            make_shape_group("Bulb Glass Shell", make_ellipse_shape(46, 46, pos=(0, -8)), COLOR_GOLD_ACCENT),
            make_shape_group("Bulb Inner Filament", make_ellipse_shape(20, 20, pos=(0, -10)), COLOR_WHITE),
            make_shape_group("Bulb Base Collar", make_rect_shape(18, 12, roundness=3, pos=(0, 16)), hex_to_lottie_color("#78350F")),
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
                "p": {"a": 1, "k": [kf(0, [256, 45, 0], [256, 35, 0]), kf(60, [256, 35, 0], [256, 45, 0]), kf(120, [256, 45, 0])]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {"a": 1, "k": [kf(0, [50, 50, 100], [115, 115, 100]), kf(25, [115, 115, 100], [100, 100, 100]), kf(120, [100, 100, 100])]}
            }
        ))

    elif state_name == "11_security":
        eye_type = "guardian"
        shield_v = [[0, -60], [52, -30], [52, 30], [0, 60], [-52, 30], [-52, -30]]
        shield_shapes = [
            make_shape_group("Shield Ambient Aura", make_path_shape(shield_v, closed=True), hex_to_lottie_color("#00F0FF", 0.18)),
            make_shape_group("Shield Outer Border", make_path_shape(shield_v, closed=True), stroke={"color": COLOR_CYAN_GLOW, "width": 8, "lj": 2}),
            make_shape_group("Shield Inner Core", make_path_shape(shield_v, closed=True), stroke={"color": COLOR_CYAN_CORE, "width": 3.5, "lj": 2}),
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
                "p": {"a": 1, "k": [kf(0, [256, 290, 0], [256, 284, 0]), kf(60, [256, 284, 0], [256, 290, 0]), kf(120, [256, 290, 0])]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {"a": 1, "k": [kf(0, [96, 96, 100], [104, 104, 100]), kf(60, [104, 104, 100], [96, 96, 100]), kf(120, [96, 96, 100])]}
            }
        ))

    elif state_name == "12_goodbye":
        eye_type = "down_arch"
        head_r_kf = {"a": 1, "k": [kf(0, 0, -3.0), kf(30, -3.0, -3.0), kf(95, -3.0, 0), kf(120, 0)]}
        eyes_r_kf = copy.deepcopy(head_r_kf)
        rpod_p_kf = {
            "a": 1,
            "k": [
                kf(0,   [374, 298, 0], [380, 245, 0]),
                kf(25,  [380, 245, 0], [380, 240, 0]),
                kf(65,  [380, 240, 0], [380, 245, 0]),
                kf(95,  [380, 245, 0], [374, 298, 0]),
                kf(120, [374, 298, 0])
            ]
        }
        rpod_r_kf = {
            "a": 1,
            "k": [
                kf(0,   9,   22),
                kf(25,  22,  -6),
                kf(55,  -6,  20),
                kf(85,  20,  9),
                kf(120, 9)
            ]
        }

    # Assemble All Rig Layers in Correct Depth Stacking Order (Pure Vector Rig, strictly NO hands)
    shadow_layer = build_ground_shadow()
    pods_layer   = build_support_pods(pos_kf=pods_p_kf)
    neck_layer   = build_slender_neck(pos_kf=neck_p_kf)
    torso_layer  = build_porcelain_torso(pos_kf=torso_p_kf)
    head_layer   = build_porcelain_head(head_pos_kf=head_p_kf, head_rot_kf=head_r_kf)
    visor_layer  = build_visor_glass(head_pos_kf=head_p_kf, head_rot_kf=head_r_kf)
    eyes_layer   = build_cyan_eyes(eyes_pos_kf=eyes_p_kf, eyes_rot_kf=eyes_r_kf, eyes_scale_kf=eyes_s_kf, eye_type=eye_type)
    lpod_layer   = build_floating_lateral_pod(ind=8, name="Floating Left Lateral Pod", is_right=False, pos_kf=lpod_p_kf, rot_kf=lpod_r_kf)
    rpod_layer   = build_floating_lateral_pod(ind=9, name="Floating Right Lateral Pod", is_right=True, pos_kf=rpod_p_kf, rot_kf=rpod_r_kf)
    
    layers = [shadow_layer, pods_layer, neck_layer, torso_layer, head_layer, visor_layer, eyes_layer, lpod_layer, rpod_layer]
    layers.extend(extra_layers)
    
    doc = {
        "v": "5.7.4",
        "fr": 30,
        "ip": 0,
        "op": 120,
        "w": 512,
        "h": 512,
        "nm": f"AItuko - {state_name} (Hands-Free Vector Rig)",
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
    
    print("🎨 Generating AItuko Master Lottie Vector Suite (13 states, 120 frames / 4.0s loop, hands-free)...")
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
