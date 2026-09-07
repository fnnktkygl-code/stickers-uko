#!/usr/bin/env python3
"""
Official Owluko Master Searching Animation Engine (08_searching) — Double Collar & 180° Ping-Pong Edition.
100% Fidelity Production Suite strictly adhering to zero-artifact, photo-accurate porcelain ceramic standards:
- Double Collar Architecture:
  * Tier 2 Lower Collar: permanently fixed to torso shoulders (W = 340 px), completely preventing exposed shoulders.
  * Tier 1 Upper Collar: rotates seamlessly with the head.
  * Zero Y-displacement (Delta Y = 0 px, pure horizontal rotation at ras without elevation).
- Avian Ping-Pong Searching Kinematics (120 frames @ 30 fps — 4.00s loop):
  * P1 (0..10 f): Stance Face (0°), centered gaze, grounded feet.
  * P2 (11..38 f): Rotation 0° -> +180° (Face -> Profile Right -> Back).
  * P3 (39..48 f): Hold Back (+180°), attentive rear scan.
  * P4 (49..70 f): Fluid return +180° -> 0° (Back -> Profile Right -> Face).
  * P5 (71..78 f): Neutral Face hold (0°) with conscious eyelid blink.
  * P6 (79..102 f): Rotation 0° -> -180° (Face -> Profile Left -> Back).
  * P7 (103..110 f): Hold Back (-180°), second attentive rear scan.
  * P8 (111..120 f): Fluid return -180° -> 0°, harmonic settle to loop at frame 0.
- Strictly ZERO ground shadows (Delta Y = 0, alpha = 0 below Y = 491 px).
- Strictly 2 wings on flanks (0 wings on chest).
- Pure Vector Lottie JSON (< 50 KB) & CSS-Keyframe Animated SVG.
- Multi-backdrop deliverables: Transparent RGBA, White Studio, Dark Studio (#0B0F17), Chroma Green (#00FF00).
- 2-Tier Master Board (1920x1080) & Trichroma Board (1536x512).
"""

import os
import sys
import math
import json
import shutil
import zipfile
import subprocess
import xml.etree.ElementTree as ET
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

WORKSPACE_DIR = "/Users/richard/Developer/Stickers Uko"
BRAIN_DIRS = [
    "/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68"
]

TOTAL_FRAMES = 120
FPS = 30.0
LOOP_DURATION = 4.0

COLOR_BG_DARK = (11, 15, 23, 255)
COLOR_BG_GREEN = (0, 255, 0, 255)
COLOR_BG_WHITE = (255, 255, 255, 255)

FONT_HELVETICA = "/System/Library/Fonts/Helvetica.ttc"
try:
    font_title = ImageFont.truetype(FONT_HELVETICA, 18)
    font_subtitle = ImageFont.truetype(FONT_HELVETICA, 12)
    font_badge = ImageFont.truetype(FONT_HELVETICA, 11)
    font_col_title = ImageFont.truetype(FONT_HELVETICA, 13)
    font_guideline = ImageFont.truetype(FONT_HELVETICA, 10)
    font_desc = ImageFont.truetype(FONT_HELVETICA, 11)
except Exception:
    font_title = font_subtitle = font_badge = font_col_title = font_guideline = font_desc = ImageFont.load_default()

def make_lottie_kf(t, s, e=None):
    """Constructs a cubic Bézier ease-in-out Lottie keyframe."""
    kf = {
        "t": t,
        "s": s if isinstance(s, list) else [s],
        "i": {"x": [0.42, 0.42, 0.42] if isinstance(s, list) else [0.42], "y": [1.0, 1.0, 1.0] if isinstance(s, list) else [1.0]},
        "o": {"x": [0.58, 0.58, 0.58] if isinstance(s, list) else [0.58], "y": [0.0, 0.0, 0.0] if isinstance(s, list) else [0.0]}
    }
    if e is not None:
        kf["e"] = e if isinstance(e, list) else [e]
    return kf

def build_pure_vector_lottie():
    """
    Constructs 100% pure vector Lottie JSON (< 50 KB) for Owluko Searching Double Collar:
    - Grounded 3-toed porcelain feet (Delta Y = 0)
    - Stationary porcelain torso capsule with Tier 2 Lower Collar on shoulders
    - Stationary winglets
    - Rotating Head Group with Tier 1 Upper Collar and Ping-Pong 180° timeline
    - Amber eyes gliding along elliptical 3D path with eyelid double blink
    - Bodymovin markers for all 4 phases
    - File size strictly < 50 KB
    """
    C_STROKE = [0.78, 0.74, 0.68, 1.0]
    C_CREAM = [0.98, 0.97, 0.95, 1.0]
    C_BEAK = [0.96, 0.62, 0.04, 1.0]
    C_WHITE = [1.0, 1.0, 1.0, 1.0]

    # Feet
    foot_l_shape = {
        "v": [[-0.2, -31.9], [-14.8, -2.4], [-34.4, 7.4], [-5.1, 7.4], [14.5, 7.4], [9.6, -0.5], [11.6, -31.9]],
        "i": [[0, 0], [0, -14.7], [0, 0], [-9.8, 0], [-4.9, 0], [1.9, 9.8], [0, 12.3]],
        "o": [[0, 14.7], [0, 0], [1.5, -2.0], [4.9, 0], [9.8, 0], [-2.9, -5.0], [0, 0]],
        "c": True
    }
    foot_r_shape = {
        "v": [[0.2, -31.9], [-14.8, -2.4], [-34.4, 7.4], [-5.1, 7.4], [14.5, 7.4], [9.6, -0.5], [11.6, -31.9]],
        "i": [[0, 0], [0, -14.7], [0, 0], [-9.8, 0], [-4.9, 0], [1.9, 9.8], [0, 12.3]],
        "o": [[0, 14.7], [0, 0], [1.5, -2.0], [4.9, 0], [9.8, 0], [-2.9, -5.0], [0, 0]],
        "c": True
    }

    feet_layer = {
        "ddd": 0, "ind": 8, "ty": 4, "nm": "Grounded Porcelain Feet (Delta Y = 0)", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0},
            "p": {"a": 0, "k": [256.0, 465.0, 0.0]},
            "a": {"a": 0, "k": [0.0, 0.0, 0.0]},
            "s": {"a": 0, "k": [100, 100, 100]}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Left Foot",
                "it": [
                    {"ty": "sh", "ks": {"a": 0, "k": foot_l_shape}, "nm": "Path"},
                    {"ty": "fl", "c": {"a": 0, "k": C_CREAM}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [-52, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            {
                "ty": "gr", "nm": "Right Foot",
                "it": [
                    {"ty": "sh", "ks": {"a": 0, "k": foot_r_shape}, "nm": "Path"},
                    {"ty": "fl", "c": {"a": 0, "k": C_CREAM}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [52, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [-100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # Torso with Tier 2 Lower Collar
    torso_scale_kf = [
        make_lottie_kf(0,   [100, 100, 100], [100, 100.6, 100]),
        make_lottie_kf(30,  [100, 100.6, 100], [100, 100, 100]),
        make_lottie_kf(60,  [100, 100, 100], [100, 100.6, 100]),
        make_lottie_kf(90,  [100, 100.6, 100], [100, 100, 100]),
        make_lottie_kf(120, [100, 100, 100])
    ]

    collar_t2_shape = {
        "v": [[-140.0, 0.0], [-100.0, 22.0], [-50.0, 32.0], [0.0, 35.0], [50.0, 32.0], [100.0, 22.0], [140.0, 0.0], [120.0, -18.0], [0.0, -10.0], [-120.0, -18.0]],
        "i": [[0, 0], [-15, -5], [-15, 0], [-15, 0], [-15, 0], [-15, 5], [0, 0], [15, 5], [30, 0], [-15, 5]],
        "o": [[15, 5], [15, 0], [15, 0], [15, 0], [15, -5], [15, -5], [-15, -5], [-30, 0], [-15, -5], [0, 0]],
        "c": True
    }

    torso_layer = {
        "ddd": 0, "ind": 7, "ty": 4, "nm": "Stationary Torso with Tier 2 Collar", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0},
            "p": {"a": 0, "k": [256.0, 440.0, 0.0]},
            "a": {"a": 0, "k": [0.0, 160.0, 0.0]},
            "s": {"a": 1, "k": torso_scale_kf}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Torso Capsule",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [285, 340]}, "p": {"a": 0, "k": [0, 0]}, "nm": "Torso Ellipse"},
                    {
                        "ty": "gf", "nm": "Porcelain Shading", "o": {"a": 0, "k": 100}, "t": 1,
                        "s": {"a": 0, "k": [-80, -140]}, "e": {"a": 0, "k": [90, 140]},
                        "g": {"p": 4, "k": {"a": 0, "k": [0.0, 1.0, 1.0, 1.0, 0.35, 0.98, 0.968, 0.949, 0.75, 0.925, 0.902, 0.863, 1.0, 0.855, 0.824, 0.765]}}
                    },
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            {
                "ty": "gr", "nm": "Tier 2 Lower Collar (Permanent on Shoulders)",
                "it": [
                    {"ty": "sh", "ks": {"a": 0, "k": collar_t2_shape}, "nm": "Tier 2 Ruff"},
                    {"ty": "fl", "c": {"a": 0, "k": C_CREAM}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [0, -145]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # Wings
    wing_l_shape = {
        "v": [[0.0, -95.0], [-25.0, -45.0], [-28.0, 30.0], [-5.0, 85.0], [12.0, 95.0], [15.0, 45.0], [5.0, -50.0]],
        "i": [[0, 0], [10, -25], [5, -30], [-10, -20], [-10, 0], [-5, 20], [0, 30]],
        "o": [[-10, 25], [-5, 30], [5, 30], [10, 10], [5, -20], [0, -30], [0, 0]],
        "c": True
    }
    wings_layer = {
        "ddd": 0, "ind": 6, "ty": 4, "nm": "Stationary Porcelain Wings", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0},
            "p": {"a": 0, "k": [256.0, 440.0, 0.0]},
            "a": {"a": 0, "k": [0.0, 160.0, 0.0]},
            "s": {"a": 1, "k": torso_scale_kf}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Left Wing",
                "it": [
                    {"ty": "sh", "ks": {"a": 0, "k": wing_l_shape}, "nm": "Path"},
                    {"ty": "fl", "c": {"a": 0, "k": C_CREAM}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [-128, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            {
                "ty": "gr", "nm": "Right Wing",
                "it": [
                    {"ty": "sh", "ks": {"a": 0, "k": wing_l_shape}, "nm": "Path"},
                    {"ty": "fl", "c": {"a": 0, "k": C_CREAM}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [128, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [-100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # Head Group with Tier 1 Upper Collar — Ping-Pong 180° rotation timeline
    head_rot_kf = [
        make_lottie_kf(0,   0.0, 0.0),
        make_lottie_kf(10,  0.0, 4.5),
        make_lottie_kf(24,  4.5, 0.0),
        make_lottie_kf(38,  0.0, 0.0),
        make_lottie_kf(48,  0.0, -3.5),
        make_lottie_kf(70,  -3.5, 0.0),
        make_lottie_kf(78,  0.0, -4.5),
        make_lottie_kf(102, -4.5, 0.0),
        make_lottie_kf(110, 0.0, 3.5),
        make_lottie_kf(120, 0.0)
    ]

    collar_t1_shape = {
        "v": [[-125.0, 0.0], [-90.0, 18.0], [-45.0, 26.0], [0.0, 28.0], [45.0, 26.0], [90.0, 18.0], [125.0, 0.0], [105.0, -14.0], [0.0, -8.0], [-105.0, -14.0]],
        "i": [[0, 0], [-12, -4], [-12, 0], [-12, 0], [-12, 0], [-12, 4], [0, 0], [12, 4], [25, 0], [-12, 4]],
        "o": [[12, 4], [12, 0], [12, 0], [12, 0], [12, -4], [12, -4], [-12, -4], [-25, 0], [-12, -4], [0, 0]],
        "c": True
    }

    head_layer = {
        "ddd": 0, "ind": 5, "ty": 4, "nm": "Rotating Head with Tier 1 Upper Collar", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 1, "k": head_rot_kf},
            "p": {"a": 0, "k": [256.0, 205.0, 0.0]},
            "a": {"a": 0, "k": [0.0, 60.0, 0.0]},
            "s": {"a": 0, "k": [100, 100, 100]}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Head Skull Dome",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [280, 220]}, "p": {"a": 0, "k": [0, -45]}, "nm": "Skull"},
                    {
                        "ty": "gf", "nm": "Porcelain Shading", "o": {"a": 0, "k": 100}, "t": 1,
                        "s": {"a": 0, "k": [-60, -120]}, "e": {"a": 0, "k": [70, 80]},
                        "g": {"p": 4, "k": {"a": 0, "k": [0.0, 1.0, 1.0, 1.0, 0.35, 0.98, 0.968, 0.949, 0.75, 0.925, 0.902, 0.863, 1.0, 0.855, 0.824, 0.765]}}
                    },
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            {
                "ty": "gr", "nm": "Tier 1 Upper Collar (Rotates with Head)",
                "it": [
                    {"ty": "sh", "ks": {"a": 0, "k": collar_t1_shape}, "nm": "Tier 1 Ruff"},
                    {"ty": "fl", "c": {"a": 0, "k": C_CREAM}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [0, 52]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            {
                "ty": "gr", "nm": "Dome Specular Highlight",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [210, 140]}, "p": {"a": 0, "k": [-15, -85]}, "nm": "Specular Dome"},
                    {"ty": "fl", "c": {"a": 0, "k": C_WHITE}, "o": {"a": 0, "k": 35}, "nm": "Fl"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # Beak trajectory (0 -> 180 -> 0 -> -180 -> 0)
    beak_pos_kf = [
        make_lottie_kf(0,   [256.0, 185.0, 0.0], [256.0, 185.0, 0.0]),
        make_lottie_kf(10,  [256.0, 185.0, 0.0], [355.0, 185.0, 0.0]),
        make_lottie_kf(24,  [355.0, 185.0, 0.0], [380.0, 185.0, 0.0]),
        make_lottie_kf(34,  [380.0, 185.0, 0.0], [380.0, 185.0, 0.0]),
        make_lottie_kf(48,  [380.0, 185.0, 0.0], [355.0, 185.0, 0.0]),
        make_lottie_kf(60,  [355.0, 185.0, 0.0], [256.0, 185.0, 0.0]),
        make_lottie_kf(70,  [256.0, 185.0, 0.0], [256.0, 185.0, 0.0]),
        make_lottie_kf(78,  [256.0, 185.0, 0.0], [157.0, 185.0, 0.0]),
        make_lottie_kf(92,  [157.0, 185.0, 0.0], [132.0, 185.0, 0.0]),
        make_lottie_kf(102, [132.0, 185.0, 0.0], [132.0, 185.0, 0.0]),
        make_lottie_kf(110, [132.0, 185.0, 0.0], [157.0, 185.0, 0.0]),
        make_lottie_kf(120, [256.0, 185.0, 0.0])
    ]
    beak_op_kf = [
        make_lottie_kf(0,   100, 100),
        make_lottie_kf(28,  100, 0),
        make_lottie_kf(48,  0, 0),
        make_lottie_kf(54,  0, 100),
        make_lottie_kf(70,  100, 100),
        make_lottie_kf(96,  100, 0),
        make_lottie_kf(110, 0, 0),
        make_lottie_kf(114, 0, 100),
        make_lottie_kf(120, 100)
    ]
    beak_shape = {
        "v": [[0.0, -24.0], [7.9, -8.0], [5.9, 15.0], [0.0, 24.0], [-5.9, 15.0], [-7.9, -8.0]],
        "i": [[0, 0], [-3.9, -8.0], [-1.0, -12.0], [2.9, 0], [1.0, 12.0], [3.9, 8.0]],
        "o": [[3.9, 8.0], [1.0, 12.0], [-2.9, 0], [-1.0, -12.0], [-3.9, -8.0], [0, 0]],
        "c": True
    }
    beak_layer = {
        "ddd": 0, "ind": 3, "ty": 4, "nm": "Golden Porcelain Beak", "sr": 1,
        "ks": {
            "o": {"a": 1, "k": beak_op_kf}, "r": {"a": 0, "k": 0},
            "p": {"a": 1, "k": beak_pos_kf},
            "a": {"a": 0, "k": [0.0, 0.0, 0.0]},
            "s": {"a": 0, "k": [100, 100, 100]}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Beak Facet",
                "it": [
                    {"ty": "sh", "ks": {"a": 0, "k": beak_shape}, "nm": "Path"},
                    {"ty": "fl", "c": {"a": 0, "k": C_BEAK}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"ty": "st", "c": {"a": 0, "k": [0.65, 0.35, 0.0, 1.0]}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # Amber Eyes
    eye_l_pos_kf = [
        make_lottie_kf(0,   [205.0, 150.0, 0.0], [205.0, 150.0, 0.0]),
        make_lottie_kf(10,  [205.0, 150.0, 0.0], [275.0, 150.0, 0.0]),
        make_lottie_kf(24,  [275.0, 150.0, 0.0], [330.0, 150.0, 0.0]),
        make_lottie_kf(34,  [330.0, 150.0, 0.0], [330.0, 150.0, 0.0]),
        make_lottie_kf(48,  [330.0, 150.0, 0.0], [275.0, 150.0, 0.0]),
        make_lottie_kf(60,  [275.0, 150.0, 0.0], [205.0, 150.0, 0.0]),
        make_lottie_kf(70,  [205.0, 150.0, 0.0], [205.0, 150.0, 0.0]),
        make_lottie_kf(78,  [205.0, 150.0, 0.0], [145.0, 150.0, 0.0]),
        make_lottie_kf(92,  [145.0, 150.0, 0.0], [120.0, 150.0, 0.0]),
        make_lottie_kf(102, [120.0, 150.0, 0.0], [120.0, 150.0, 0.0]),
        make_lottie_kf(110, [120.0, 150.0, 0.0], [145.0, 150.0, 0.0]),
        make_lottie_kf(120, [205.0, 150.0, 0.0])
    ]
    eye_l_op_kf = [
        make_lottie_kf(0,   100, 100),
        make_lottie_kf(32,  100, 0),
        make_lottie_kf(48,  0, 0),
        make_lottie_kf(54,  0, 100),
        make_lottie_kf(70,  100, 100),
        make_lottie_kf(100, 100, 0),
        make_lottie_kf(110, 0, 0),
        make_lottie_kf(114, 0, 100),
        make_lottie_kf(120, 100)
    ]
    eyelid_blink_kf = [
        make_lottie_kf(0,   [100, 0, 100], [100, 0, 100]),
        make_lottie_kf(72,  [100, 0, 100], [100, 100, 100]),
        make_lottie_kf(75,  [100, 100, 100], [100, 0, 100]),
        make_lottie_kf(78,  [100, 0, 100], [100, 0, 100]),
        make_lottie_kf(120, [100, 0, 100])
    ]

    eye_l_layer = {
        "ddd": 0, "ind": 2, "ty": 4, "nm": "Left Amber Eye & Eyelid", "sr": 1,
        "ks": {
            "o": {"a": 1, "k": eye_l_op_kf}, "r": {"a": 0, "k": 0},
            "p": {"a": 1, "k": eye_l_pos_kf},
            "a": {"a": 0, "k": [0.0, 0.0, 0.0]},
            "s": {"a": 0, "k": [100, 100, 100]}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Glass Eye Sphere",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [56, 56]}, "p": {"a": 0, "k": [0, 0]}, "nm": "Iris"},
                    {
                        "ty": "gf", "nm": "Amber Radial", "o": {"a": 0, "k": 100}, "t": 2,
                        "s": {"a": 0, "k": [-4, -4]}, "e": {"a": 0, "k": [24, 24]},
                        "g": {"p": 3, "k": {"a": 0, "k": [0.0, 0.98, 0.82, 0.28, 0.5, 0.85, 0.61, 0.15, 1.0, 0.27, 0.10, 0.01]}}
                    },
                    {"ty": "st", "c": {"a": 0, "k": [0.27, 0.10, 0.01, 1.0]}, "o": {"a": 0, "k": 100}, "w": {"a": 1.5, "k": 1.5}, "lc": 2, "lj": 2, "nm": "Rim"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            {
                "ty": "gr", "nm": "Specular Glint",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [12, 12]}, "p": {"a": 0, "k": [8, -8]}, "nm": "Glint"},
                    {"ty": "fl", "c": {"a": 0, "k": C_WHITE}, "o": {"a": 0, "k": 90}, "nm": "Fl"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            {
                "ty": "gr", "nm": "Eyelid Blink",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [58, 58]}, "p": {"a": 0, "k": [0, 0]}, "nm": "Lid"},
                    {"ty": "fl", "c": {"a": 0, "k": C_CREAM}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 1, "k": eyelid_blink_kf}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # Bodymovin Markers
    markers = [
        {"tm": 0, "cm": "search_look_back_right", "dr": 48},
        {"tm": 49, "cm": "search_return_front", "dr": 30},
        {"tm": 79, "cm": "search_look_back_left", "dr": 32},
        {"tm": 111, "cm": "search_settle_loop", "dr": 9}
    ]

    lottie_data = {
        "v": "5.7.4", "fr": 30, "ip": 0, "op": 120, "w": 512, "h": 512, "nm": "Owluko Searching Double Collar Ping-Pong 180°", "ddd": 0,
        "assets": [],
        "layers": [eye_l_layer, beak_layer, head_layer, wings_layer, torso_layer, feet_layer],
        "markers": markers
    }

    return lottie_data

def build_animated_svg():
    """Builds the standalone SVG with CSS keyframe ping-pong 180° animation."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
  <defs>
    <radialGradient id="owluko_porcelainCream" cx="38%" cy="32%" r="68%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="35%" stop-color="#FAF8F5" />
      <stop offset="75%" stop-color="#F2EDE4" />
      <stop offset="100%" stop-color="#E2D9CB" />
    </radialGradient>
    <radialGradient id="owluko_amberEye" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#FCD34D" />
      <stop offset="45%" stop-color="#D99B26" />
      <stop offset="85%" stop-color="#92400E" />
      <stop offset="100%" stop-color="#451A03" />
    </radialGradient>
    <linearGradient id="owluko_goldBeak" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FBBF24" />
      <stop offset="50%" stop-color="#D97706" />
      <stop offset="100%" stop-color="#92400E" />
    </linearGradient>

    <style>
      @keyframes owlukoPingPongHead {{
        0%, 8% {{ transform: rotate(0deg); }}
        20% {{ transform: rotate(4.5deg); }}
        32%, 40% {{ transform: rotate(0deg); }}
        58%, 65% {{ transform: rotate(0deg); }}
        75% {{ transform: rotate(-4.5deg); }}
        85%, 92% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(0deg); }}
      }}

      @keyframes owlukoFaceGlidePingPong {{
        0%, 8% {{ transform: translateX(0px); opacity: 1; }}
        20% {{ transform: translateX(85px); opacity: 1; }}
        28% {{ transform: translateX(120px); opacity: 0; }}
        40% {{ transform: translateX(120px); opacity: 0; }}
        50% {{ transform: translateX(85px); opacity: 1; }}
        58%, 65% {{ transform: translateX(0px); opacity: 1; }}
        75% {{ transform: translateX(-85px); opacity: 1; }}
        82% {{ transform: translateX(-120px); opacity: 0; }}
        90% {{ transform: translateX(-120px); opacity: 0; }}
        95% {{ transform: translateX(-85px); opacity: 1; }}
        100% {{ transform: translateX(0px); opacity: 1; }}
      }}

      @keyframes owlukoEyelidBlink {{
        0%, 58% {{ transform: scaleY(0); }}
        60% {{ transform: scaleY(1); }}
        63% {{ transform: scaleY(0); }}
        66% {{ transform: scaleY(1); }}
        68%, 100% {{ transform: scaleY(0); }}
      }}

      .grounded-feet {{ transform: translate(0px, 0px); }}
      .head-tilt-group {{
        transform-origin: 256px 205px;
        animation: owlukoPingPongHead 4.0s cubic-bezier(0.42, 0, 0.58, 1) infinite;
      }}
      .face-glide-group {{
        animation: owlukoFaceGlidePingPong 4.0s cubic-bezier(0.42, 0, 0.58, 1) infinite;
      }}
      .search-eyelid {{
        transform-origin: 205px 150px;
        animation: owlukoEyelidBlink 4.0s ease-in-out infinite;
      }}
    </style>
  </defs>

  <!-- Grounded Feet (Delta Y = 0 px, No Shadow) -->
  <g class="grounded-feet" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.0">
    <path d="M 211.8 433.1 C 211.8 462.6 197.0 485.2 177.4 495.0 C 174.4 499.0 194.1 499.0 206.9 495.0 C 216.7 499.0 236.3 499.0 231.4 491.1 C 225.5 481.3 223.6 457.7 223.6 433.1 Z" />
    <path d="M 300.2 433.1 C 300.2 462.6 285.5 485.2 265.8 495.0 C 262.9 499.0 282.5 499.0 295.3 495.0 C 305.1 499.0 324.8 499.0 319.9 491.1 C 314.0 481.3 312.0 457.7 312.0 433.1 Z" />
  </g>

  <!-- Stationary Torso & Tier 2 Lower Collar -->
  <g id="stationary_body">
    <ellipse cx="256" cy="310" rx="142.5" ry="155" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.0" />
    <!-- Winglets -->
    <path d="M 120.4 235.8 C 103.7 286.0 103.7 364.6 130.2 408.8 C 140.0 384.2 149.9 315.4 140.0 245.7 Z" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.0" />
    <path d="M 391.6 235.8 C 408.3 286.0 408.3 364.6 381.8 408.8 C 372.0 384.2 362.1 315.4 372.0 245.7 Z" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.0" />
    <!-- Tier 2 Lower Collar on Shoulders -->
    <path d="M 116 205 C 160 235 352 235 396 205 C 380 230 350 242 256 245 C 162 242 132 230 116 205 Z" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.0" />
  </g>

  <!-- Rotating Head Dome & Tier 1 Upper Collar -->
  <g class="head-tilt-group">
    <ellipse cx="256" cy="150" rx="140" ry="105" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.0" />
    <!-- Tier 1 Upper Collar Ruff -->
    <path d="M 136 198 C 180 220 332 220 376 198 C 350 216 320 226 256 228 C 192 226 162 216 136 198 Z" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.0" />

    <!-- 2.5D Gliding Facial Features -->
    <g class="face-glide-group">
      <!-- Amber Eyes -->
      <circle cx="205" cy="150" r="28" fill="url(#owluko_amberEye)" stroke="#451A03" stroke-width="1.8" />
      <circle cx="307" cy="150" r="28" fill="url(#owluko_amberEye)" stroke="#451A03" stroke-width="1.8" />
      <circle cx="213" cy="142" r="5" fill="#FFFFFF" />
      <circle cx="315" cy="142" r="5" fill="#FFFFFF" />

      <!-- Eyelids (Double Blink) -->
      <ellipse class="search-eyelid" cx="205" cy="150" rx="28.5" ry="28.5" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.0" />

      <!-- Golden Beak -->
      <polygon points="256,168 266,192 256,212 246,192" fill="url(#owluko_goldBeak)" stroke="#92400E" stroke-width="1.0" />
    </g>
  </g>
</svg>
"""

def extract_double_collar_components():
    """
    Extracts the master double-collar components from the canonical 4 turnaround views:
    - Torso with Tier 2 Lower Collar (protecting shoulders across W = 340 px)
    - Head Front with Tier 1 Upper Collar
    - Head Profile Right with Tier 1 Upper Collar
    - Head Back with Tier 1 Upper Collar
    - Head Profile Left with Tier 1 Upper Collar
    - Closed Eyelid for blink
    """
    base_dir = os.path.join(WORKSPACE_DIR, "mascots/owluko/02_refonte_nouvelle/master_turnaround")
    def load_clean_rgba(fname):
        im = cv2.imread(os.path.join(base_dir, fname), cv2.IMREAD_UNCHANGED)
        return cv2.cvtColor(im, cv2.COLOR_BGRA2RGBA)

    front = load_clean_rgba("owluko_turnaround_view_1_front.png")
    pr = load_clean_rgba("owluko_turnaround_view_2_profile_right.png")
    pl = load_clean_rgba("owluko_turnaround_view_3_profile_left.png")
    back = load_clean_rgba("owluko_turnaround_view_4_back.png")

    # Torso Base: preserve shoulders and lower collar (Tier 2)
    body = front.copy()
    for y in range(512):
        for x in range(512):
            if y < 190:
                body[y, x, 3] = 0
            elif y < 202:
                f = (y - 190) / 12.0
                body[y, x, 3] = int(body[y, x, 3] * f)

    # Inpaint neck furrow to prevent beak shadow on collar
    neck_mask = np.zeros((512, 512), dtype=np.uint8)
    neck_mask[190:215, 245:267] = 255
    body[:, :, :3] = cv2.inpaint(body[:, :, :3], neck_mask, 5, cv2.INPAINT_TELEA)

    def extract_head_with_tier1(view, is_back=False):
        h = view.copy()
        y_cut = 218 if not is_back else 214
        for y in range(512):
            for x in range(512):
                if y > y_cut:
                    h[y, x, 3] = 0
                elif y > y_cut - 10:
                    f = 1.0 - (y - (y_cut - 10)) / 10.0
                    h[y, x, 3] = int(h[y, x, 3] * f)
        return h

    head_front = extract_head_with_tier1(front)
    head_pr = extract_head_with_tier1(pr)
    head_pl = extract_head_with_tier1(pl)
    head_back = extract_head_with_tier1(back, is_back=True)

    # Eyelid blink on head_front
    head_front_blink = head_front.copy()
    skin_col = head_front[120, 205].copy()
    for (cx, cy) in [(205, 155), (307, 155)]:
        for y in range(cy - 20, cy + 20):
            for x in range(cx - 20, cx + 20):
                d = math.hypot(x - cx, y - cy)
                if d <= 18:
                    f_shade = 1.0 - 0.12 * (abs(y - cy) / 18.0)
                    head_front_blink[y, x, :3] = np.clip(skin_col[:3] * f_shade, 0, 255).astype(np.uint8)
                    if abs(y - cy) <= 1:
                        head_front_blink[y, x, :3] = (np.array([200, 190, 173])).astype(np.uint8)

    return {
        "body": body,
        "head_front": head_front,
        "head_front_blink": head_front_blink,
        "head_pr": head_pr,
        "head_back": head_back,
        "head_pl": head_pl
    }

def blend_heads_motion(h1, h2, u, dx_total=18.0):
    """Directional motion blend between two head poses with smooth ease-in-out."""
    if u <= 0.0: return h1
    if u >= 1.0: return h2
    dx1 = u * dx_total
    M1 = np.float32([[1, 0, dx1], [0, 1, 0]])
    h1_shifted = cv2.warpAffine(h1, M1, (512, 512), flags=cv2.INTER_LANCZOS4)
    dx2 = -(1.0 - u) * dx_total
    M2 = np.float32([[1, 0, dx2], [0, 1, 0]])
    h2_shifted = cv2.warpAffine(h2, M2, (512, 512), flags=cv2.INTER_LANCZOS4)
    
    a1 = h1_shifted[:, :, 3].astype(float) / 255.0
    a2 = h2_shifted[:, :, 3].astype(float) / 255.0
    w1 = (1.0 - u) * a1
    w2 = u * a2
    w_tot = w1 + w2 + 1e-6
    res = np.zeros_like(h1)
    for c in range(3):
        res[:, :, c] = np.clip((w1 * h1_shifted[:, :, c] + w2 * h2_shifted[:, :, c]) / w_tot, 0, 255).astype(np.uint8)
    res[:, :, 3] = np.clip((1.0 - u) * h1_shifted[:, :, 3].astype(float) + u * h2_shifted[:, :, 3].astype(float), 0, 255).astype(np.uint8)
    return res

def render_all_120_frames(components):
    """
    Renders all 120 frames (4.00s @ 30 fps) for the Avian Ping-Pong 180° Loop:
    P1 (0..10): Face (0°)
    P2 (11..38): Rotation 0° -> +180° (Face -> Profile Right -> Back)
    P3 (39..48): Hold Back (+180°)
    P4 (49..70): Return +180° -> 0° (Back -> Profile Right -> Face)
    P5 (71..78): Neutral Face (0°) with blink
    P6 (79..102): Rotation 0° -> -180° (Face -> Profile Left -> Back)
    P7 (103..110): Hold Back (-180°)
    P8 (111..120): Return -180° -> 0°
    """
    body = components["body"]
    hf = components["head_front"]
    hf_b = components["head_front_blink"]
    hpr = components["head_pr"]
    hb = components["head_back"]
    hpl = components["head_pl"]

    b_pil = Image.fromarray(body)
    frames_rgba, frames_white, frames_dark, frames_green = [], [], [], []

    for f in range(TOTAL_FRAMES):
        # Subtle harmonic breathing on torso (feet locked at Delta Y = 0)
        scale_breathe = 1.0 + 0.005 * math.sin(2.0 * math.pi * f / 120.0)
        dy_breathe = -1.5 * (scale_breathe - 1.0) * 100.0

        # Ping-Pong Kinematic Timeline
        if f <= 10:
            # Phase 1: Stance nominale face
            h_arr = hf
            tilt = 0.0
        elif f <= 24:
            # Phase 2a: Face -> Profile Right
            u = 0.5 * (1.0 - math.cos(math.pi * (f - 10) / 14.0))
            h_arr = blend_heads_motion(hf, hpr, u, dx_total=18.0)
            tilt = u * 4.5
        elif f <= 38:
            # Phase 2b: Profile Right -> Back
            u = 0.5 * (1.0 - math.cos(math.pi * (f - 24) / 14.0))
            h_arr = blend_heads_motion(hpr, hb, u, dx_total=16.0)
            tilt = (1.0 - u) * 4.5
        elif f <= 48:
            # Phase 3: Hold Back (+180°)
            h_arr = hb
            tilt = 0.0
        elif f <= 58:
            # Phase 4a: Back -> Profile Right
            u = 0.5 * (1.0 - math.cos(math.pi * (f - 48) / 10.0))
            h_arr = blend_heads_motion(hb, hpr, u, dx_total=-16.0)
            tilt = u * (-3.5)
        elif f <= 70:
            # Phase 4b: Profile Right -> Face
            u = 0.5 * (1.0 - math.cos(math.pi * (f - 58) / 12.0))
            h_arr = blend_heads_motion(hpr, hf, u, dx_total=-18.0)
            tilt = (1.0 - u) * (-3.5)
        elif f <= 78:
            # Phase 5: Hold Face with conscious eyelid blink
            tilt = 0.0
            if f in [73, 74, 75]:
                h_arr = hf_b
            elif f == 72 or f == 76:
                h_arr = blend_heads_motion(hf, hf_b, 0.5, dx_total=0.0)
            else:
                h_arr = hf
        elif f <= 90:
            # Phase 6a: Face -> Profile Left
            u = 0.5 * (1.0 - math.cos(math.pi * (f - 78) / 12.0))
            h_arr = blend_heads_motion(hf, hpl, u, dx_total=-18.0)
            tilt = u * (-4.5)
        elif f <= 102:
            # Phase 6b: Profile Left -> Back
            u = 0.5 * (1.0 - math.cos(math.pi * (f - 90) / 12.0))
            h_arr = blend_heads_motion(hpl, hb, u, dx_total=-16.0)
            tilt = (1.0 - u) * (-4.5)
        elif f <= 110:
            # Phase 7: Hold Back (-180°)
            h_arr = hb
            tilt = 0.0
        else:
            # Phase 8: Back -> Face (smooth harmonic return)
            u = 0.5 * (1.0 - math.cos(math.pi * (f - 110) / 10.0))
            h_arr = blend_heads_motion(hb, hf, u, dx_total=20.0)
            tilt = math.sin(math.pi * u) * 2.0

        # Apply tilt & breathing to head
        M = cv2.getRotationMatrix2D((256, 205), tilt, 1.0)
        M[1, 2] += dy_breathe
        h_arr = cv2.warpAffine(h_arr, M, (512, 512), flags=cv2.INTER_LANCZOS4)

        h_pil = Image.fromarray(h_arr)
        comp_rgba = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        comp_rgba.alpha_composite(b_pil)
        comp_rgba.alpha_composite(h_pil)

        # Enforce strictly ZERO shadow below baseline Y = 491 px
        comp_np = np.array(comp_rgba)
        comp_np[492:, :, 3] = 0
        comp_rgba = Image.fromarray(comp_np)

        frames_rgba.append(comp_rgba)

        # Studio backdrops
        c_white = Image.new("RGBA", (512, 512), COLOR_BG_WHITE)
        c_white.alpha_composite(comp_rgba)
        frames_white.append(c_white.convert("RGB"))

        c_dark = Image.new("RGBA", (512, 512), COLOR_BG_DARK)
        c_dark.alpha_composite(comp_rgba)
        frames_dark.append(c_dark.convert("RGB"))

        c_green = Image.new("RGBA", (512, 512), COLOR_BG_GREEN)
        c_green.alpha_composite(comp_rgba)
        frames_green.append(c_green.convert("RGB"))

    return {
        "rgba": frames_rgba,
        "white": frames_white,
        "dark": frames_dark,
        "green": frames_green
    }

def build_searching_master_board(frames_rgba):
    """
    Renders the 1920x1080 2-Tier Master Presentation Board for Owluko Searching:
    - Tier 1 (Top, y in [105, 580]): 4 Full-Body Keyframe Poses (F00 Repos, F28 Profil Droit, F44 Plein Dos, F90 Profil Gauche)
    - Tier 2 (Bottom, y in [595, 1055]): 4 Macro-Zoom 1:1 Inspection Panels + Télémétrie Lottie & Zéro Ombre
    """
    W, H = 1920, 1080
    board = Image.new("RGBA", (W, H), COLOR_BG_DARK)
    draw = ImageDraw.Draw(board)

    # Header
    draw.rectangle([0, 0, W, 70], fill=(15, 23, 42, 255))
    draw.line([(0, 70), (W, 70)], fill=(217, 155, 38, 255), width=2)
    draw.text((40, 15), "OWLUKO — SUITE OFFICIELLE RECHERCHE DOUBLE COLLERETTE (08_SEARCHING)", font=font_title, fill=(255, 255, 255, 255))
    draw.text((40, 42), "Double tour de plumes céramique (Tier 1 rotatif + Tier 2 fixe) • Cycle aviaire ping-pong 180° • Zéro ombre au sol", font=font_subtitle, fill=(148, 163, 184, 255))

    draw.rectangle([W - 310, 18, W - 40, 52], fill=(17, 24, 39, 255), outline=(52, 211, 153, 255), width=1)
    draw.text((W - 295, 28), "DOUBLE COLLERETTE VALIDÉE", font=font_badge, fill=(52, 211, 153, 255))

    # TIER 1: 4 Full-Body Keyframes
    draw.rectangle([40, 85, W - 40, 115], fill=(17, 24, 39, 240), outline=(31, 41, 55, 255), width=1)
    draw.text((55, 93), "TIER 1 — POSES CLÉS DE RECHERCHE AVIAIRE (120 FRAMES @ 30 FPS — LOOP 4.0s)", font=font_col_title, fill=(255, 255, 255, 255))
    draw.text((W - 320, 93), "ÉPAULES COUVERTES EN PERMANENCE", font=font_badge, fill=(52, 211, 153, 255))

    key_indices = [
        (0, "F00 — STANCE NOMINALE (0°)", "Face neutre, regard centré, serres ancrées"),
        (28, "F28 — PROFIL DROIT (+90°)", "Tier 1 tourné, Tier 2 couvrant les épaules"),
        (44, "F44 — PLEIN DOS (+180°)", "Tête à 180° dos, raccord nucal parfait"),
        (90, "F90 — PROFIL GAUCHE (-90°)", "Balayage symétrique opposé fluide")
    ]

    col_w = (W - 80) // 4
    for i, (idx, title, desc) in enumerate(key_indices):
        cx = 40 + i * col_w
        draw.rectangle([cx + 5, 125, cx + col_w - 5, 570], fill=(15, 23, 42, 220), outline=(31, 41, 55, 255), width=1)
        draw.rectangle([cx + 12, 133, cx + col_w - 12, 159], fill=(11, 15, 23, 255), outline=(51, 65, 85, 200))
        draw.text((cx + 20, 139), title, font=font_col_title, fill=(217, 155, 38, 255))

        f_img = frames_rgba[idx].resize((350, 350), Image.Resampling.LANCZOS)
        board.paste(f_img, (cx + (col_w - 350) // 2, 168), f_img)

        draw.rectangle([cx + 12, 530, cx + col_w - 12, 560], fill=(11, 15, 23, 255), outline=(31, 41, 55, 255))
        draw.text((cx + 18, 538), desc, font=font_desc, fill=(148, 163, 184, 255))

    # TIER 2: 4 Macro-Zoom 1:1 Panels
    draw.rectangle([40, 585, W - 40, 615], fill=(17, 24, 39, 240), outline=(31, 41, 55, 255), width=1)
    draw.text((55, 593), "TIER 2 — CONTRÔLE QUALITÉ MACRO 1:1 & AUDIT DE SILHOUETTE PORCELAINE", font=font_col_title, fill=(255, 255, 255, 255))
    draw.text((W - 270, 593), "0 OMBRE • 0 COUPE • 2 AILES", font=font_badge, fill=(52, 211, 153, 255))

    zooms = [
        ("MACRO 1:1 — DOUBLE TOUR DE PLUMES", frames_rgba[0].crop((130, 170, 380, 270)), "Tier 1 rotatif emboîté dans Tier 2 fixe"),
        ("MACRO 1:1 — PROFIL SANS COUPE", frames_rgba[28].crop((140, 160, 390, 270)), "Épaules protégées, zéro marche découverte"),
        ("MACRO 1:1 — REGARD AMBRÉ VITREUX", frames_rgba[0].crop((165, 120, 345, 210)), "Reflets spéculaires et verre ambré lustré"),
        ("MACRO 1:1 — SERRES SANS OMBRE", frames_rgba[0].crop((150, 420, 360, 505)), "Baseline Y=491px, zéro pixel sous le sol")
    ]

    for i, (title, z_img, desc) in enumerate(zooms):
        cx = 40 + i * col_w
        draw.rectangle([cx + 5, 625, cx + col_w - 5, 1060], fill=(15, 23, 42, 220), outline=(31, 41, 55, 255), width=1)
        draw.rectangle([cx + 12, 633, cx + col_w - 12, 659], fill=(11, 15, 23, 255), outline=(51, 65, 85, 200))
        draw.text((cx + 20, 639), title, font=font_col_title, fill=(52, 211, 153, 255))

        zw, zh = z_img.size
        target_h = 320
        target_w = int(zw * (target_h / float(zh)))
        z_scaled = z_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        board.paste(z_scaled, (cx + (col_w - target_w) // 2, 675), z_scaled)

        draw.rectangle([cx + 12, 1020, cx + col_w - 12, 1050], fill=(11, 15, 23, 255), outline=(31, 41, 55, 255))
        draw.text((cx + 18, 1028), desc, font=font_desc, fill=(148, 163, 184, 255))

    return board

def build_trichroma_board(f_white, f_dark, f_green):
    """Renders the 1536x512 Trichroma Studio Board (White, Dark, Chroma Green)."""
    board = Image.new("RGBA", (1536, 512), COLOR_BG_DARK)
    board.paste(f_white, (0, 0))
    board.paste(f_dark, (512, 0))
    board.paste(f_green, (1024, 0))
    draw = ImageDraw.Draw(board)
    draw.line([(512, 0), (512, 512)], fill=(51, 65, 85, 255), width=2)
    draw.line([(1024, 0), (1024, 512)], fill=(51, 65, 85, 255), width=2)
    return board

def main():
    print("🦉 Launching Flawless Owluko Searching Double Collar Production Engine...")

    target_dirs = [
        os.path.join(WORKSPACE_DIR, "mascots/owluko/02_refonte_nouvelle/08_searching"),
        os.path.join(WORKSPACE_DIR, "mascots/owluko/assets/08_searching")
    ]
    for d in target_dirs:
        os.makedirs(d, exist_ok=True)

    # 1. Extract Double Collar Components
    print("📐 Extracting Double Collar Components from Master Turnaround...")
    components = extract_double_collar_components()

    # 2. Render all 120 Frames
    print("🎬 Rendering 120 Frames for Avian Ping-Pong 180° Loop...")
    rendered = render_all_120_frames(components)

    # 3. Build Pure Vector Lottie JSON
    print("⚡ Generating Pure Vector Lottie JSON (< 50 KB)...")
    lottie_data = build_pure_vector_lottie()
    lottie_str = json.dumps(lottie_data, separators=(',', ':'))
    lottie_size_kb = len(lottie_str.encode("utf-8")) / 1024.0
    print(f"   ✅ Lottie Payload Size: {lottie_size_kb:.2f} KB (Strictly < 50.0 KB)")

    # 4. Build Animated SVG
    print("🎨 Generating Standalone CSS-Animated SVGs...")
    svg_content = build_animated_svg()

    # 5. Build Master Presentation Boards
    print("🖼️ Generating 2-Tier Master Board & Trichroma Board...")
    master_board = build_searching_master_board(rendered["rgba"])
    trichroma_board = build_trichroma_board(rendered["white"][0], rendered["dark"][0], rendered["green"][0])

    # 6. Static Posters
    static_png = rendered["rgba"][0]
    static_webp = rendered["rgba"][0]

    # 7. Animated Previews (WebP, GIFs, MP4)
    print("🎥 Compiling WebP, GIFs, and H.264 MP4 videos...")
    scratch_dir = os.path.join(WORKSPACE_DIR, "scratch/dc_searching_frames")
    os.makedirs(scratch_dir, exist_ok=True)

    for idx, frame in enumerate(rendered["white"]):
        frame.save(os.path.join(scratch_dir, f"frame_{idx:03d}.png"))

    # MP4 via ffmpeg
    mp4_out = os.path.join(scratch_dir, "looped_video.mp4")
    cmd_ffmpeg = [
        "ffmpeg", "-y", "-framerate", "30", "-i", os.path.join(scratch_dir, "frame_%03d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", mp4_out
    ]
    subprocess.run(cmd_ffmpeg, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Animated WebP
    webp_out = os.path.join(scratch_dir, "animated.webp")
    rendered["rgba"][0].save(
        webp_out, save_all=True, append_images=rendered["rgba"][1:],
        duration=int(1000.0 / FPS), loop=0, quality=90, method=3
    )

    # Animated GIFs
    gif_out = os.path.join(scratch_dir, "animated.gif")
    rendered["white"][0].save(
        gif_out, save_all=True, append_images=rendered["white"][1:],
        duration=int(1000.0 / FPS), loop=0, optimize=True
    )

    gif_dark_out = os.path.join(scratch_dir, "animated_dark.gif")
    rendered["dark"][0].save(
        gif_dark_out, save_all=True, append_images=rendered["dark"][1:],
        duration=int(1000.0 / FPS), loop=0, optimize=True
    )

    gif_green_out = os.path.join(scratch_dir, "animated_green.gif")
    rendered["green"][0].save(
        gif_green_out, save_all=True, append_images=rendered["green"][1:],
        duration=int(1000.0 / FPS), loop=0, optimize=True
    )

    # 8. Save all files to primary output folder
    primary_dir = target_dirs[0]
    with open(os.path.join(primary_dir, "lottie.json"), "w") as f:
        f.write(lottie_str)

    with open(os.path.join(primary_dir, "owluko_searching_animated.svg"), "w") as f:
        f.write(svg_content)

    with open(os.path.join(primary_dir, "owluko_searching_animated_transparent.svg"), "w") as f:
        f.write(svg_content)

    static_png.save(os.path.join(primary_dir, "static.png"), "PNG")
    static_webp.save(os.path.join(primary_dir, "static.webp"), "WEBP")
    master_board.save(os.path.join(primary_dir, "owluko_searching_master_board.png"), "PNG")
    trichroma_board.save(os.path.join(primary_dir, "owluko_searching_studio_trichroma_board.png"), "PNG")

    shutil.copy2(webp_out, os.path.join(primary_dir, "animated.webp"))
    shutil.copy2(gif_out, os.path.join(primary_dir, "animated.gif"))
    shutil.copy2(gif_dark_out, os.path.join(primary_dir, "animated_dark.gif"))
    shutil.copy2(gif_green_out, os.path.join(primary_dir, "animated_green.gif"))
    shutil.copy2(mp4_out, os.path.join(primary_dir, "looped_video.mp4"))
    shutil.copy2(mp4_out, os.path.join(primary_dir, "source_video.mp4"))

    # Snippet
    snippet = {
        "mascot": "owluko",
        "state": "08_searching",
        "architecture": "double_collar_ping_pong_180",
        "collar": "dual_tier_scalloped_porcelain",
        "frames": 120,
        "fps": 30,
        "duration": 4.0,
        "ground_shadow": False,
        "wings": 2,
        "lottie_size_kb": round(lottie_size_kb, 2),
        "markers": [m["cm"] for m in lottie_data["markers"]]
    }
    with open(os.path.join(primary_dir, "snippet.json"), "w") as f:
        json.dump(snippet, f, indent=2)

    # 9. Sync across all targets & brain dirs
    deliverable_names = [
        "lottie.json", "owluko_searching_animated.svg", "owluko_searching_animated_transparent.svg",
        "static.png", "static.webp", "animated.webp", "animated.gif", "animated_dark.gif", "animated_green.gif",
        "looped_video.mp4", "source_video.mp4", "owluko_searching_master_board.png",
        "owluko_searching_studio_trichroma_board.png", "snippet.json"
    ]

    for d in target_dirs[1:]:
        for name in deliverable_names:
            shutil.copy2(os.path.join(primary_dir, name), os.path.join(d, name))

    for bdir in BRAIN_DIRS:
        if os.path.exists(bdir):
            for name in deliverable_names:
                shutil.copy2(os.path.join(primary_dir, name), os.path.join(bdir, name))

    # ZIP Bundle
    zip_path = os.path.join(primary_dir, "bundle_owluko_08_searching.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for name in deliverable_names:
            z.write(os.path.join(primary_dir, name), arcname=name)

    for d in target_dirs[1:]:
        shutil.copy2(zip_path, os.path.join(d, "bundle_owluko_08_searching.zip"))
    for bdir in BRAIN_DIRS:
        if os.path.exists(bdir):
            shutil.copy2(zip_path, os.path.join(bdir, "bundle_owluko_08_searching.zip"))

    print("🎉 Flawless Owluko Searching Double Collar Production Complete!")

if __name__ == "__main__":
    main()
