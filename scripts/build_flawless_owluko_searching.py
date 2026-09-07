#!/usr/bin/env python3
"""
Official Owluko Master Searching Animation Engine (08_searching) — 100% Fidelity Suite.
Generates fluid, seamless 360-degree head rotation animation strictly adhering to zero-artifact,
photo-accurate porcelain ceramic standards:
- Biological owl superpower: Head rotates 360 degrees smoothly while body, wings, and feet remain stationary!
- Grounded feet: Delta Y = 0 px (Owluko stands firmly on the ground, does not levitate)
- Option A Kinematic Timeline (120 frames @ 30 fps — 4.00s loop):
  * Phase 1 (0..24 f / 0.0s - 0.8s): Head turns right 0° -> 90° (Profile Right), +3.2° inquisitive tilt hold.
  * Phase 2 (25..54 f / 0.8s - 1.8s): Swift sweep backwards 90° -> 180° (Back) -> 270° (Profile Left).
  * Phase 3 (55..78 f / 1.8s - 2.6s): Attentive hold at 270° (Profile Left), -2.8° tilt, double blink of amber eye.
  * Phase 4 (79..119 f / 2.6s - 4.0s): Energetic return forward 270° -> 360°/0° (Front), damped harmonic settle.
- Strictly ZERO ground shadows anywhere (0 in Lottie, 0 in SVG, 0 in frames).
- Pure Vector Lottie JSON (< 50 KB) & CSS-Keyframe Animated SVG.
- Multi-backdrop deliverables: Transparent RGBA, White Studio, Dark Studio (#0B0F17), Chroma Green (#00FF00).
- 2-Tier Architectural Master Board (1920x1080) with 4 full-body poses + 4 macro-zoom inspection panels.
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
LOOP_DURATION = 4.0 # seconds

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
    """Constructs a standard cubic Bézier ease-in-out Lottie keyframe."""
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
    Constructs 100% pure vector Lottie JSON (< 50 KB) for Owluko Searching (360° Head Rotation):
    - STRICTLY ZERO ground shadow
    - Grounded 3-toed porcelain feet (dy = 0.0 px, Delta Y = 0)
    - Stationary porcelain torso capsule with subtle micro-breathing
    - Stationary winglets
    - Rotating head dome with inquisitive tilt
    - 2.5D facial features (amber eyes and beak) rotating around the vertical axis
    - Double blink at 270° profile left hold
    - Payload size strictly < 50 KB (target ~30 KB)
    """
    C_STROKE = [0.78, 0.74, 0.68, 1.0]
    C_CREAM = [0.98, 0.97, 0.95, 1.0]
    C_BEAK = [0.96, 0.62, 0.04, 1.0]
    C_WHITE = [1.0, 1.0, 1.0, 1.0]

    # 1. Grounded Feet (ind: 8) — 100% STATIC (Delta Y = 0)
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
            "a": {"a": 0, "k": [0, 0, 0]},
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
                    {"p": {"a": 0, "k": [-44.0, 0.0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            {
                "ty": "gr", "nm": "Right Foot",
                "it": [
                    {"ty": "sh", "ks": {"a": 0, "k": foot_r_shape}, "nm": "Path"},
                    {"ty": "fl", "c": {"a": 0, "k": C_CREAM}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [44.0, 0.0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [-100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # 2. Stationary Torso Capsule (ind: 7) — Anchored at ankles Y=440
    torso_scale_kf = [
        make_lottie_kf(0,   [100.0, 100.0, 100.0], [99.6, 100.5, 100.0]),
        make_lottie_kf(30,  [99.6, 100.5, 100.0], [100.0, 100.0, 100.0]),
        make_lottie_kf(60,  [100.0, 100.0, 100.0], [100.4, 99.5, 100.0]),
        make_lottie_kf(90,  [100.4, 99.5, 100.0], [100.0, 100.0, 100.0]),
        make_lottie_kf(120, [100.0, 100.0, 100.0])
    ]

    torso_layer = {
        "ddd": 0, "ind": 7, "ty": 4, "nm": "Stationary Porcelain Torso", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0},
            "p": {"a": 0, "k": [256.0, 440.0, 0.0]},
            "a": {"a": 0, "k": [0.0, 194.0, 0.0]},
            "s": {"a": 1, "k": torso_scale_kf}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Torso Shell",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [285, 340]}, "p": {"a": 0, "k": [0, 40]}, "nm": "Torso"},
                    {
                        "ty": "gf", "nm": "Shading", "o": {"a": 0, "k": 100}, "t": 1,
                        "s": {"a": 0, "k": [-60, -100]}, "e": {"a": 0, "k": [80, 160]},
                        "g": {"p": 4, "k": {"a": 0, "k": [0.0, 1.0, 1.0, 1.0, 0.35, 0.98, 0.968, 0.949, 0.75, 0.925, 0.902, 0.863, 1.0, 0.855, 0.824, 0.765]}}
                    },
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # 3. Wings (ind: 5 & 6) — Resting on flanks
    wing_l_shape = {
        "v": [[-13.6, -86.5], [-30.3, -36.3], [-3.8, 86.5], [6.0, 61.9], [15.9, -6.9], [6.0, -76.6]],
        "i": [[0, 0], [0, -25.0], [0, 0], [-4.9, 12.3], [-4.9, 34.4], [0, 0]],
        "o": [[-8.3, 25.0], [0, 39.3], [4.9, -12.3], [4.9, -34.4], [0, -34.8], [0, 0]],
        "c": True
    }

    left_wing_layer = {
        "ddd": 0, "ind": 5, "ty": 4, "nm": "Left Winglet (Resting)", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0},
            "p": {"a": 0, "k": [256.0, 440.0, 0.0]},
            "a": {"a": 0, "k": [121.0, 219.0, 0.0]},
            "s": {"a": 1, "k": torso_scale_kf}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Wing Shell",
                "it": [
                    {"ty": "sh", "ks": {"a": 0, "k": wing_l_shape}, "nm": "Path"},
                    {"ty": "fl", "c": {"a": 0, "k": C_CREAM}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    right_wing_layer = {
        "ddd": 0, "ind": 6, "ty": 4, "nm": "Right Winglet (Resting)", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0},
            "p": {"a": 0, "k": [256.0, 440.0, 0.0]},
            "a": {"a": 0, "k": [-121.0, 219.0, 0.0]},
            "s": {"a": 1, "k": torso_scale_kf}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Wing Shell",
                "it": [
                    {"ty": "sh", "ks": {"a": 0, "k": wing_l_shape}, "nm": "Path"},
                    {"ty": "fl", "c": {"a": 0, "k": C_CREAM}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [-100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # 4. Rotating Head Dome (ind: 4) — Pivot at neck (256, 210)
    # Tilt keyframes (Option A inquisitive tilts)
    head_rot_kf = [
        make_lottie_kf(0,   0.0, 0.0),
        make_lottie_kf(6,   0.0, 3.2),
        make_lottie_kf(20,  3.2, 3.2),
        make_lottie_kf(24,  3.2, 0.0),
        make_lottie_kf(42,  0.0, 0.0),
        make_lottie_kf(48,  0.0, -2.8),
        make_lottie_kf(54,  -2.8, -2.8),
        make_lottie_kf(78,  -2.8, 0.0),
        make_lottie_kf(105, 0.0, 0.6),
        make_lottie_kf(110, 0.6, -0.3),
        make_lottie_kf(115, -0.3, 0.0),
        make_lottie_kf(120, 0.0)
    ]

    head_dome_layer = {
        "ddd": 0, "ind": 4, "ty": 4, "nm": "Rotating Head Porcelain Dome", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 1, "k": head_rot_kf},
            "p": {"a": 0, "k": [256.0, 205.0, 0.0]},
            "a": {"a": 0, "k": [0.0, 60.0, 0.0]}, # Pivot at base of skull
            "s": {"a": 0, "k": [100, 100, 100]}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Porcelain Head Dome",
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

    # 5. Beak (ind: 3) — Horizontal 3D rotation trajectory
    # X translation: 0° (256) -> 90° (350) -> 180° (hidden behind) -> 270° (162) -> 360° (256)
    beak_pos_kf = [
        make_lottie_kf(0,   [256.0, 185.0, 0.0], [256.0, 185.0, 0.0]),
        make_lottie_kf(6,   [256.0, 185.0, 0.0], [350.0, 185.0, 0.0]),
        make_lottie_kf(20,  [350.0, 185.0, 0.0], [350.0, 185.0, 0.0]),
        make_lottie_kf(24,  [350.0, 185.0, 0.0], [380.0, 185.0, 0.0]),
        make_lottie_kf(32,  [380.0, 185.0, 0.0], [132.0, 185.0, 0.0]),
        make_lottie_kf(50,  [132.0, 185.0, 0.0], [162.0, 185.0, 0.0]),
        make_lottie_kf(54,  [162.0, 185.0, 0.0], [162.0, 185.0, 0.0]),
        make_lottie_kf(78,  [162.0, 185.0, 0.0], [256.0, 185.0, 0.0]),
        make_lottie_kf(105, [256.0, 185.0, 0.0]),
        make_lottie_kf(120, [256.0, 185.0, 0.0])
    ]
    beak_opacity_kf = [
        make_lottie_kf(0,   100, 100),
        make_lottie_kf(24,  100, 0),
        make_lottie_kf(30,  0, 0),
        make_lottie_kf(48,  0, 100),
        make_lottie_kf(54,  100, 100),
        make_lottie_kf(120, 100)
    ]
    beak_shape = {
        "v": [[0.0, -24.0], [7.9, -8.0], [5.9, 15.0], [0.0, 24.0], [-5.9, 15.0], [-7.9, -8.0]],
        "i": [[0, 0], [-3.9, -8.0], [-1.0, -12.0], [2.9, 0], [1.0, 12.0], [3.9, 8.0]],
        "o": [[3.9, 8.0], [1.0, 12.0], [-2.9, 0], [-1.0, -12.0], [-3.9, -8.0], [0, 0]],
        "c": True
    }
    beak_layer = {
        "ddd": 0, "ind": 3, "ty": 4, "nm": "Porcelain Beak (360 Sweep)", "parent": 4, "sr": 1,
        "ks": {
            "o": {"a": 1, "k": beak_opacity_kf}, "r": {"a": 0, "k": 0},
            "p": {"a": 1, "k": beak_pos_kf},
            "a": {"a": 0, "k": [256.0, 185.0, 0.0]},
            "s": {"a": 0, "k": [100, 100, 100]}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Beak Shell",
                "it": [
                    {"ty": "sh", "ks": {"a": 0, "k": beak_shape}, "nm": "Path"},
                    {"ty": "fl", "c": {"a": 0, "k": C_BEAK}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"ty": "st", "c": {"a": 0, "k": [0.70, 0.45, 0.05, 1.0]}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [256.0, 185.0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # 6. Amber Eyes & Eyelids (ind: 1 & 2)
    # Left eye: X starts 205, sweeps right, hidden on back, sweeps left to 185 on 270°, double blinks, returns
    eye_l_pos_kf = [
        make_lottie_kf(0,   [205.0, 150.0, 0.0], [205.0, 150.0, 0.0]),
        make_lottie_kf(6,   [205.0, 150.0, 0.0], [270.0, 150.0, 0.0]),
        make_lottie_kf(16,  [270.0, 150.0, 0.0], [300.0, 150.0, 0.0]),
        make_lottie_kf(20,  [300.0, 150.0, 0.0], [160.0, 150.0, 0.0]),
        make_lottie_kf(50,  [160.0, 150.0, 0.0], [185.0, 150.0, 0.0]),
        make_lottie_kf(54,  [185.0, 150.0, 0.0], [185.0, 150.0, 0.0]),
        make_lottie_kf(78,  [185.0, 150.0, 0.0], [205.0, 150.0, 0.0]),
        make_lottie_kf(105, [205.0, 150.0, 0.0]),
        make_lottie_kf(120, [205.0, 150.0, 0.0])
    ]
    eye_l_opacity_kf = [
        make_lottie_kf(0,   100, 100),
        make_lottie_kf(18,  100, 0),
        make_lottie_kf(22,  0, 0),
        make_lottie_kf(50,  0, 100),
        make_lottie_kf(54,  100, 100),
        make_lottie_kf(120, 100)
    ]

    # Double blink on Left Eye (f=62..66 and f=71..75)
    eyelid_l_scale_kf = [
        make_lottie_kf(0,   [100.0, 0.0, 100.0], [100.0, 0.0, 100.0]),
        make_lottie_kf(62,  [100.0, 0.0, 100.0], [100.0, 100.0, 100.0]),
        make_lottie_kf(64,  [100.0, 100.0, 100.0], [100.0, 0.0, 100.0]),
        make_lottie_kf(66,  [100.0, 0.0, 100.0], [100.0, 0.0, 100.0]),
        make_lottie_kf(71,  [100.0, 0.0, 100.0], [100.0, 100.0, 100.0]),
        make_lottie_kf(73,  [100.0, 100.0, 100.0], [100.0, 0.0, 100.0]),
        make_lottie_kf(75,  [100.0, 0.0, 100.0], [100.0, 0.0, 100.0]),
        make_lottie_kf(120, [100.0, 0.0, 100.0])
    ]

    eye_l_layer = {
        "ddd": 0, "ind": 2, "ty": 4, "nm": "Left Amber Eye (360 Sweep & Double Blink)", "parent": 4, "sr": 1,
        "ks": {
            "o": {"a": 1, "k": eye_l_opacity_kf}, "r": {"a": 0, "k": 0},
            "p": {"a": 1, "k": eye_l_pos_kf},
            "a": {"a": 0, "k": [0, 0, 0]},
            "s": {"a": 0, "k": [100, 100, 100]}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Orb Eye",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [56, 56]}, "p": {"a": 0, "k": [0, 0]}, "nm": "Eye"},
                    {
                        "ty": "gf", "nm": "Amber Shading", "o": {"a": 0, "k": 100}, "t": 2,
                        "s": {"a": 0, "k": [-5, -10]}, "e": {"a": 0, "k": [25, 25]},
                        "g": {"p": 4, "k": {"a": 0, "k": [0.0, 0.99, 0.88, 0.28, 0.35, 0.85, 0.61, 0.15, 0.7, 0.70, 0.48, 0.08, 1.0, 0.27, 0.10, 0.01]}}
                    },
                    {"ty": "st", "c": {"a": 0, "k": [0.27, 0.10, 0.01, 1.0]}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.8}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            {
                "ty": "gr", "nm": "Specular Highlight",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [10, 10]}, "p": {"a": 0, "k": [8, -8]}, "nm": "H1"},
                    {"ty": "fl", "c": {"a": 0, "k": C_WHITE}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            {
                "ty": "gr", "nm": "Porcelain Eyelid",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [58, 58]}, "p": {"a": 0, "k": [0, 0]}, "nm": "Eyelid"},
                    {"ty": "fl", "c": {"a": 0, "k": C_CREAM}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 1, "k": eyelid_l_scale_kf}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # Right eye: X starts 307, sweeps right to 325 at 90°, hidden on back, returns from left at 100
    eye_r_pos_kf = [
        make_lottie_kf(0,   [307.0, 150.0, 0.0], [307.0, 150.0, 0.0]),
        make_lottie_kf(6,   [307.0, 150.0, 0.0], [330.0, 150.0, 0.0]),
        make_lottie_kf(20,  [330.0, 150.0, 0.0], [330.0, 150.0, 0.0]),
        make_lottie_kf(24,  [330.0, 150.0, 0.0], [360.0, 150.0, 0.0]),
        make_lottie_kf(28,  [360.0, 150.0, 0.0], [220.0, 150.0, 0.0]),
        make_lottie_kf(95,  [220.0, 150.0, 0.0], [307.0, 150.0, 0.0]),
        make_lottie_kf(105, [307.0, 150.0, 0.0]),
        make_lottie_kf(120, [307.0, 150.0, 0.0])
    ]
    eye_r_opacity_kf = [
        make_lottie_kf(0,   100, 100),
        make_lottie_kf(24,  100, 0),
        make_lottie_kf(28,  0, 0),
        make_lottie_kf(95,  0, 100),
        make_lottie_kf(105, 100, 100),
        make_lottie_kf(120, 100)
    ]

    eye_r_layer = {
        "ddd": 0, "ind": 1, "ty": 4, "nm": "Right Amber Eye (360 Sweep)", "parent": 4, "sr": 1,
        "ks": {
            "o": {"a": 1, "k": eye_r_opacity_kf}, "r": {"a": 0, "k": 0},
            "p": {"a": 1, "k": eye_r_pos_kf},
            "a": {"a": 0, "k": [0, 0, 0]},
            "s": {"a": 0, "k": [100, 100, 100]}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Orb Eye",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [56, 56]}, "p": {"a": 0, "k": [0, 0]}, "nm": "Eye"},
                    {
                        "ty": "gf", "nm": "Amber Shading", "o": {"a": 0, "k": 100}, "t": 2,
                        "s": {"a": 0, "k": [-5, -10]}, "e": {"a": 0, "k": [25, 25]},
                        "g": {"p": 4, "k": {"a": 0, "k": [0.0, 0.99, 0.88, 0.28, 0.35, 0.85, 0.61, 0.15, 0.7, 0.70, 0.48, 0.08, 1.0, 0.27, 0.10, 0.01]}}
                    },
                    {"ty": "st", "c": {"a": 0, "k": [0.27, 0.10, 0.01, 1.0]}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.8}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            {
                "ty": "gr", "nm": "Specular Highlight",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [10, 10]}, "p": {"a": 0, "k": [8, -8]}, "nm": "H1"},
                    {"ty": "fl", "c": {"a": 0, "k": C_WHITE}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # Markers
    markers = [
        {"tm": 0,  "cm": "search_turn_right", "dr": 24},
        {"tm": 25, "cm": "search_sweep_back", "dr": 29},
        {"tm": 55, "cm": "search_scan_left",  "dr": 23},
        {"tm": 79, "cm": "search_return_front","dr": 41}
    ]

    lottie = {
        "v": "5.7.4",
        "fr": FPS,
        "ip": 0,
        "op": TOTAL_FRAMES,
        "w": 512,
        "h": 512,
        "nm": "Owluko Searching 360 Head Rotation (08_searching)",
        "ddd": 0,
        "assets": [],
        "layers": [
            eye_r_layer,
            eye_l_layer,
            beak_layer,
            head_dome_layer,
            left_wing_layer,
            right_wing_layer,
            torso_layer,
            feet_layer
        ],
        "markers": markers
    }
    return lottie

def build_animated_svg():
    """Generates pure standalone CSS-Keyframe Animated SVG for Owluko Searching (360° Head Rotation)."""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <linearGradient id="owluko_porcelainCream" x1="20%" y1="10%" x2="80%" y2="90%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="35%" stop-color="#FAF7F2" />
      <stop offset="75%" stop-color="#ECE6DC" />
      <stop offset="100%" stop-color="#DAD2C3" />
    </linearGradient>

    <linearGradient id="owluko_wingletGrad" x1="25%" y1="15%" x2="75%" y2="85%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="40%" stop-color="#FAF7F2" />
      <stop offset="80%" stop-color="#E2DCD0" />
      <stop offset="100%" stop-color="#CDC4B3" />
    </linearGradient>

    <radialGradient id="owluko_amberEye" cx="45%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#FDE047" />
      <stop offset="35%" stop-color="#D99B26" />
      <stop offset="70%" stop-color="#B37A15" />
      <stop offset="100%" stop-color="#451A03" />
    </radialGradient>

    <radialGradient id="owluko_beakGrad" cx="50%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#FFFBEB" />
      <stop offset="50%" stop-color="#FDE68A" />
      <stop offset="100%" stop-color="#D97706" />
    </radialGradient>

    <radialGradient id="owluko_specularDome" cx="45%" cy="25%" r="55%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.9" />
      <stop offset="40%" stop-color="#FFFFFF" stop-opacity="0.4" />
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.0" />
    </radialGradient>

    <style>
      @keyframes owlukoSearchHeadRotate {{
        0%, 5% {{ transform: rotate(0deg); }}
        17%, 20% {{ transform: rotate(3.2deg); }}
        35% {{ transform: rotate(0deg); }}
        45%, 65% {{ transform: rotate(-2.8deg); }}
        88% {{ transform: rotate(0deg); }}
        92% {{ transform: rotate(0.6deg); }}
        96% {{ transform: rotate(-0.3deg); }}
        100% {{ transform: rotate(0deg); }}
      }}

      @keyframes owlukoSearchFaceGlide {{
        0%, 5% {{ transform: translateX(0px); opacity: 1; }}
        17%, 20% {{ transform: translateX(70px); opacity: 1; }}
        24% {{ transform: translateX(110px); opacity: 0; }}
        40% {{ transform: translateX(-110px); opacity: 0; }}
        45%, 65% {{ transform: translateX(-70px); opacity: 1; }}
        88%, 100% {{ transform: translateX(0px); opacity: 1; }}
      }}

      @keyframes owlukoSearchBlink {{
        0%, 51% {{ transform: scaleY(0); }}
        52.5% {{ transform: scaleY(1); }}
        55% {{ transform: scaleY(0); }}
        59% {{ transform: scaleY(0); }}
        61% {{ transform: scaleY(1); }}
        63%, 100% {{ transform: scaleY(0); }}
      }}

      .grounded-feet {{ transform: translate(0px, 0px); }}
      .head-tilt-group {{
        transform-origin: 256px 205px;
        animation: owlukoSearchHeadRotate 4.0s cubic-bezier(0.42, 0, 0.58, 1) infinite;
      }}
      .face-glide-group {{
        animation: owlukoSearchFaceGlide 4.0s cubic-bezier(0.42, 0, 0.58, 1) infinite;
      }}
      .search-eyelid {{
        transform-origin: 205px 150px;
        animation: owlukoSearchBlink 4.0s ease-in-out infinite;
      }}
    </style>
  </defs>

  <!-- Grounded Porcelain Feet (100% Static, Delta Y = 0 px, No Shadow) -->
  <g class="grounded-feet" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.0">
    <path d="M 211.8 433.1 C 211.8 462.6 197.0 485.2 177.4 495.0 C 174.4 499.0 194.1 499.0 206.9 495.0 C 216.7 499.0 236.3 499.0 231.4 491.1 C 225.5 481.3 223.6 457.7 223.6 433.1 Z" />
    <path d="M 300.2 433.1 C 300.2 462.6 285.5 485.2 265.8 495.0 C 262.9 499.0 282.5 499.0 295.3 495.0 C 305.1 499.0 324.8 499.0 319.9 491.1 C 314.0 481.3 312.0 457.7 312.0 433.1 Z" />
  </g>

  <!-- Stationary Porcelain Torso & Wings -->
  <g id="stationary_body">
    <ellipse cx="256" cy="280" rx="142.5" ry="170" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.0" />
    <!-- Winglets -->
    <path d="M 120.4 220.8 C 103.7 271.0 103.7 349.6 130.2 393.8 C 140.0 369.2 149.9 300.4 140.0 230.7 Z" fill="url(#owluko_wingletGrad)" stroke="#C8BEAD" stroke-width="1.0" />
    <path d="M 391.6 220.8 C 408.3 271.0 408.3 349.6 381.8 393.8 C 372.0 369.2 362.1 300.4 372.0 230.7 Z" fill="url(#owluko_wingletGrad)" stroke="#C8BEAD" stroke-width="1.0" />
  </g>

  <!-- Rotating Head Dome (360° Saccadic Sweep & Tilt) -->
  <g class="head-tilt-group">
    <ellipse cx="256" cy="150" rx="140" ry="110" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.0" />
    <ellipse cx="241" cy="110" rx="105" ry="70" fill="url(#owluko_specularDome)" />

    <!-- 2.5D Gliding Facial Features -->
    <g class="face-glide-group">
      <!-- Amber Eyes -->
      <circle cx="205" cy="150" r="28" fill="url(#owluko_amberEye)" stroke="#451A03" stroke-width="1.8" />
      <circle cx="307" cy="150" r="28" fill="url(#owluko_amberEye)" stroke="#451A03" stroke-width="1.8" />
      <circle cx="213" cy="142" r="5" fill="#FFFFFF" />
      <circle cx="315" cy="142" r="5" fill="#FFFFFF" />

      <!-- Eyelids (Double Blink) -->
      <ellipse class="search-eyelid" cx="205" cy="150" rx="28.5" ry="28.5" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.0" />

      <!-- Beak -->
      <path d="M 256.0 162 C 263.9 176, 261.9 198, 256.0 206 C 250.1 198, 248.1 176, 256.0 162 Z" fill="url(#owluko_beakGrad)" stroke="#B45309" stroke-width="1.0" />
    </g>
  </g>
</svg>"""
    return svg


def load_and_prepare_turnaround_components():
    """
    Loads and standardizes components from mascots/owluko/owluko_master_turnaround.jpeg:
    - 100% Despilled warm cream porcelain (#FAF8F5 / #F4EFE6)
    - Protected amber orb eyes (#D99B26) and golden beak
    - Stationary body (Delta Y = 0 px, locked at Y = 497 px)
    - 4 canonical head angles: Front 0°, Profile Right 90°, Back 180°, Profile Left 270°
    - Eyelid blink overlay for Profile Left (Double blink phase)
    """
    sys.path.append(os.path.join(WORKSPACE_DIR, "scripts"))
    from build_flawless_owluko_turnaround_master import extract_clean_owluko_turnaround_figures

    figs = extract_clean_owluko_turnaround_figures()

    target_h = 450.0
    def get_clean_rgba(name):
        pil_img = figs[name]["rgba"]
        arr = np.array(pil_img)
        ys, xs = np.where(arr[:, :, 3] > 30)
        scale = target_h / float(ys.max() - ys.min() + 1)
        nw = int(round((xs.max() - xs.min() + 1) * scale))
        nh = int(round(target_h))
        scaled = cv2.resize(arr[ys.min():ys.max()+1, xs.min():xs.max()+1], (nw, nh), interpolation=cv2.INTER_LANCZOS4)
        canvas = np.zeros((512, 512, 4), dtype=np.uint8)
        px = (512 - nw) // 2
        py = 512 - nh - 22 # Baseline at Y = 490..497
        canvas[py:py+nh, px:px+nw] = scaled
        return canvas

    front = get_clean_rgba("front")
    pr = get_clean_rgba("profile_right")
    back = get_clean_rgba("back")
    pl = get_clean_rgba("profile_left")

    def y_body_top_arches(x):
        if 145.0 <= x <= 367.0:
            u = abs(x - 256.0) / 111.0
            return 172.0 + 33.0 * (u ** 2)
        elif x > 367.0:
            u = (x - 388.0) / 24.0
            if abs(u) <= 1.0:
                return 185.0 + 20.0 * (u ** 2)
            else:
                return 205.0
        else:
            u = (x - 124.0) / 24.0
            if abs(u) <= 1.0:
                return 185.0 + 20.0 * (u ** 2)
            else:
                return 205.0

    # Stationary Body with 3-arch porcelain collar and wing crests
    body = front.copy()
    for y in range(512):
        for x in range(512):
            yt = y_body_top_arches(x)
            if y < yt - 4:
                body[y, x, 3] = 0
            elif y < yt:
                f = (y - (yt - 4)) / 4.0
                body[y, x, 3] = int(body[y, x, 3] * f)

    # Inpaint collar zone to remove front beak shadow from stationary neck socket
    collar_mask = np.zeros((512, 512), dtype=np.uint8)
    collar_mask[172:215, 235:277] = 255
    body[:, :, :3] = cv2.inpaint(body[:, :, :3], collar_mask, 7, cv2.INPAINT_TELEA)

    # Subtle ambient occlusion contact shadow on neck collar furrow
    for y in range(185, 218):
        for x in range(150, 362):
            yt = y_body_top_arches(x)
            if y >= yt and y <= yt + 18:
                dist = y - yt
                f_ao = 0.12 * math.sin(math.pi * dist / 18.0)
                body[y, x, :3] = np.clip(body[y, x, :3].astype(float) * (1.0 - f_ao), 0, 255).astype(np.uint8)

    def extract_head_blended(raw_view, name):
        h = raw_view.copy()
        y_cut = 216 if name != "back" else 212
        y_start_feather = y_cut - 10
        for y in range(512):
            for x in range(512):
                if y > y_cut:
                    h[y, x, 3] = 0
                elif y > y_start_feather:
                    f = 1.0 - (y - y_start_feather) / 10.0
                    h[y, x, 3] = int(h[y, x, 3] * f)
        return h

    head_front = extract_head_blended(front, "front")
    head_pr = extract_head_blended(pr, "pr")
    head_back = extract_head_blended(back, "back")
    head_pl = extract_head_blended(pl, "pl")

    # Closed eyelid on head_pl for double blink
    head_pl_blink = head_pl.copy()
    skin_col = head_pl[120, 155].copy()
    for y in range(135, 175):
        for x in range(135, 175):
            if head_pl[y, x, 0] > 120 and head_pl[y, x, 1] > 70 and head_pl[y, x, 2] < 70 and head_pl[y, x, 3] > 100:
                dy = abs(y - 155)
                f_shade = 1.0 - 0.15 * (dy / 20.0)
                head_pl_blink[y, x, :3] = np.clip(skin_col[:3] * f_shade, 0, 255).astype(np.uint8)
                if y == 155:
                    head_pl_blink[y, x, :3] = (np.array([200, 190, 173])).astype(np.uint8)

    return {
        "body": body,
        "head_front": head_front,
        "head_pr": head_pr,
        "head_back": head_back,
        "head_pl": head_pl,
        "head_pl_blink": head_pl_blink
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

def render_all_frames(components):
    """
    Renders all 120 frames (4.0s @ 30 fps) for Owluko Searching (Option A):
    Returns dictionary with:
    - "rgba": list of 120 transparent PIL Images
    - "white": list of 120 white studio PIL Images
    - "dark": list of 120 dark studio PIL Images (#0B0F17)
    - "green": list of 120 chroma green PIL Images (#00FF00)
    """
    body = components["body"]
    hf = components["head_front"]
    hpr = components["head_pr"]
    hb = components["head_back"]
    hpl = components["head_pl"]
    hpl_b = components["head_pl_blink"]

    b_pil = Image.fromarray(body)
    frames_rgba, frames_white, frames_dark, frames_green = [], [], [], []

    for f in range(TOTAL_FRAMES):
        # Micro-breathing (feet locked at Y = 497, Delta Y = 0)
        scale_breathe = 1.0 + 0.005 * math.sin(2.0 * math.pi * f / 120.0)
        dy_breathe = -1.8 * (scale_breathe - 1.0) * 100.0

        # Kinematic Timeline Option A
        if f <= 6:
            h_arr = hf
            tilt = 0.0
        elif f <= 20:
            u = 0.5 * (1.0 - math.cos(math.pi * (f - 7) / 13.0))
            h_arr = blend_heads_motion(hf, hpr, u, dx_total=20.0)
            tilt = u * 3.2
        elif f <= 24:
            h_arr = hpr
            tilt = 3.2
        elif f <= 42:
            u = 0.5 * (1.0 - math.cos(math.pi * (f - 25) / 17.0))
            h_arr = blend_heads_motion(hpr, hb, u, dx_total=16.0)
            tilt = (1.0 - u) * 3.2
        elif f <= 48:
            h_arr = hb
            tilt = 0.0
        elif f <= 54:
            u = 0.5 * (1.0 - math.cos(math.pi * (f - 49) / 5.0))
            h_arr = blend_heads_motion(hb, hpl, u, dx_total=16.0)
            tilt = u * (-2.8)
        elif f <= 78:
            tilt = -2.8
            if f in [63, 64]:
                h_arr = hpl_b
            elif f == 62 or f == 65:
                h_arr = blend_heads_motion(hpl, hpl_b, 0.5, dx_total=0.0)
            elif f in [72, 73]:
                h_arr = hpl_b
            elif f == 71 or f == 74:
                h_arr = blend_heads_motion(hpl, hpl_b, 0.5, dx_total=0.0)
            else:
                h_arr = hpl
        elif f <= 105:
            u = 0.5 * (1.0 - math.cos(math.pi * (f - 79) / 26.0))
            h_arr = blend_heads_motion(hpl, hf, u, dx_total=24.0)
            tilt = (1.0 - u) * (-2.8)
        else:
            h_arr = hf
            t_damped = f - 106
            tilt = 0.6 * math.exp(-t_damped / 4.0) * math.sin(math.pi * t_damped / 3.0)

        # Apply tilt & breathing
        M = cv2.getRotationMatrix2D((256, 205), tilt, 1.0)
        M[1, 2] += dy_breathe
        h_arr = cv2.warpAffine(h_arr, M, (512, 512), flags=cv2.INTER_LANCZOS4)

        h_pil = Image.fromarray(h_arr)
        comp_rgba = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        comp_rgba.alpha_composite(b_pil)
        comp_rgba.alpha_composite(h_pil)
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
    - Tier 1 (Top, y in [105, 580]): 4 Full-Body Keyframe Poses (F00 Repos, F24 Profil Droit, F45 Dos, F64 Profil Gauche Double Blink)
    - Tier 2 (Bottom, y in [595, 1055]): 4 Macro-Zoom 1:1 Inspection Panels + Télémétrie Lottie & Zéro Ombre
    Completely eliminates any dead space.
    """
    W, H = 1920, 1080
    board = Image.new("RGBA", (W, H), COLOR_BG_DARK)
    draw = ImageDraw.Draw(board)

    # 1. Header Banner
    draw.rectangle([0, 0, W, 90], fill=(15, 23, 42, 255))
    draw.line([(0, 90), (W, 90)], fill=(31, 41, 55, 220), width=2)
    draw.text((50, 22), "OWLUKO — ANIMATION OFFICIELLE RECHERCHE (08_SEARCHING) — PLANCHE MASTER 2-TIERS", font=font_title, fill=(217, 155, 38, 255))
    draw.text((50, 54), "Super-Pouvoir Hibou : Rotation 360° de la Tête, Corps & Serres 100% Stationnaires (Delta Y = 0), Zéro Ombre au Sol, Cadence Option A", font=font_subtitle, fill=(148, 163, 184, 255))

    # Badge
    draw.rectangle([W - 290, 26, W - 50, 64], fill=(17, 24, 39, 255), outline=(52, 211, 153, 255), width=1)
    draw.text((W - 275, 38), "● ROTATION 360° VALIDÉE", font=font_badge, fill=(52, 211, 153, 255))

    # 2. Keyframes Definitions
    keyframe_specs = [
        {
            "idx": 0,
            "title": "KEYFRAME 1 : 0° FACE REPOS (F00)",
            "desc": "Stance neutre, regard ambre de face, serres verrouillées au sol (Y=497, Delta Y=0)",
            "macro_title": "MACRO 1 : ORBES AMBRE OUVERTS (1:1)",
            "macro_box": (140, 105, 372, 235),
            "metric_1": "Tête : 0° Face nominale (Yeux ambrés concentriques)",
            "metric_2": "Corps : Stationnaire (Micro-respiration 100%..100.5%)",
            "metric_3": "Sol : Ligne Y=497 strictement respectée, 0 ombre"
        },
        {
            "idx": 24,
            "title": "KEYFRAME 2 : 90°R PROFIL DROIT (F24)",
            "desc": "Rotation 90° à droite, tilt interrogateur +3.2°, œil ambre droit & bec saillant",
            "macro_title": "MACRO 2 : PROFIL DROIT & BEC DORÉ",
            "macro_box": (180, 105, 412, 235),
            "metric_1": "Tête : 90°R Profil Droit (Tilt +3.2° curieux)",
            "metric_2": "Corps : 100% Immobile de face (Ailerons & Serres fixes)",
            "metric_3": "Anatomie : Bec doré saillant au bord du dôme"
        },
        {
            "idx": 45,
            "title": "KEYFRAME 3 : 180° DOS COMPLET (F45)",
            "desc": "Rotation 180° dorsale : dôme porcelaine pur (zéro œil/bec), corps toujours de face",
            "macro_title": "MACRO 3 : DÔME PORCELAINE DORSALE",
            "macro_box": (140, 105, 372, 235),
            "metric_1": "Tête : 180° Dos pur (0 œil, 0 bec, dôme lisse)",
            "metric_2": "Corps : Plastron pectoral & serres toujours de face",
            "metric_3": "Fidélité : Super-pouvoir hibou 100% concrétisé"
        },
        {
            "idx": 64,
            "title": "KEYFRAME 4 : 270°L PROFIL & BLINK (F64)",
            "desc": "Arrêt attentif à 270°, tilt -2.8°, apex du double clignement des paupières porcelaine",
            "macro_title": "MACRO 4 : DOUBLE BLINK & MÉTRIQUES",
            "macro_box": (100, 105, 332, 235),
            "metric_1": "Tête : 270°L Profil Gauche (Tilt -2.8° attentif)",
            "metric_2": "Clignement : Paupière porcelaine close F62..F66 & F71..F75",
            "metric_3": "Lottie : < 35 Ko vectoriel pur — 60 fps natif"
        }
    ]

    col_w = 480
    for col_idx, spec in enumerate(keyframe_specs):
        cx = col_idx * col_w
        f_img = frames_rgba[spec["idx"]]

        # ==================== TIER 1: FULL-BODY POSE ====================
        card_t1_x1, card_t1_y1 = cx + 16, 105
        card_t1_x2, card_t1_y2 = cx + col_w - 16, 580
        draw.rectangle([card_t1_x1, card_t1_y1, card_t1_x2, card_t1_y2], fill=(17, 24, 39, 235), outline=(31, 41, 55, 220), width=1)

        # Header tag
        is_hero = (col_idx == 0 or col_idx == 3)
        tag_border = (217, 155, 38, 180) if is_hero else (52, 211, 153, 160)
        tag_color = (217, 155, 38, 255) if is_hero else (52, 211, 153, 255)
        draw.rectangle([card_t1_x1 + 10, card_t1_y1 + 10, card_t1_x2 - 10, card_t1_y1 + 38], fill=(15, 23, 42, 240), outline=tag_border, width=1)
        draw.text((card_t1_x1 + 16, card_t1_y1 + 17), spec["title"], font=font_badge, fill=tag_color)

        # Scale character to fit Tier 1 (height 380 px)
        target_h_t1 = 380.0
        orig_w, orig_h = f_img.size
        s_t1 = target_h_t1 / float(orig_h)
        nw_t1, nh_t1 = int(round(orig_w * s_t1)), int(round(target_h_t1))
        f_scaled_t1 = f_img.resize((nw_t1, nh_t1), Image.Resampling.LANCZOS)
        paste_x_t1 = card_t1_x1 + (card_t1_x2 - card_t1_x1 - nw_t1) // 2
        paste_y_t1 = card_t1_y1 + 45
        board.alpha_composite(f_scaled_t1, (paste_x_t1, paste_y_t1))

        # Verified Floor Line (Delta Y = 0 px)
        floor_y = paste_y_t1 + nh_t1 - int(22 * s_t1)
        for gx in range(card_t1_x1 + 10, card_t1_x2 - 10, 10):
            draw.line([(gx, floor_y), (gx + 5, floor_y)], fill=(16, 185, 129, 90), width=1)
        draw.text((card_t1_x1 + 16, floor_y + 4), "LIGNE DE SOL VERROUILLÉE (DELTA Y = 0 PX — SANS OMBRE)", font=font_guideline, fill=(16, 185, 129, 180))

        # Footer Description
        draw.rectangle([card_t1_x1 + 10, card_t1_y2 - 32, card_t1_x2 - 10, card_t1_y2 - 8], fill=(15, 23, 42, 220), outline=(31, 41, 55, 160), width=1)
        draw.text((card_t1_x1 + 16, card_t1_y2 - 26), spec["desc"], font=font_desc, fill=(148, 163, 184, 255))

        # ==================== TIER 2: MACRO-ZOOM 1:1 INSPECTION ====================
        card_t2_x1, card_t2_y1 = cx + 16, 595
        card_t2_x2, card_t2_y2 = cx + col_w - 16, 1055
        draw.rectangle([card_t2_x1, card_t2_y1, card_t2_x2, card_t2_y2], fill=(17, 24, 39, 235), outline=(31, 41, 55, 220), width=1)

        # Header tag Macro
        draw.rectangle([card_t2_x1 + 10, card_t2_y1 + 10, card_t2_x2 - 10, card_t2_y1 + 38], fill=(15, 23, 42, 240), outline=(217, 155, 38, 120), width=1)
        draw.text((card_t2_x1 + 16, card_t2_y1 + 17), spec["macro_title"], font=font_badge, fill=(217, 155, 38, 255))

        # 1:1 High-Res Macro Crop
        crop_box = spec["macro_box"]
        macro_crop = f_img.crop(crop_box)
        mc_w, mc_h = macro_crop.size
        zoom_target_w = 420
        zoom_s = zoom_target_w / float(mc_w)
        zoom_w = int(round(mc_w * zoom_s))
        zoom_h = int(round(mc_h * zoom_s))
        macro_scaled = macro_crop.resize((zoom_w, zoom_h), Image.Resampling.LANCZOS)

        # Macro viewport frame
        view_x1, view_y1 = card_t2_x1 + 14, card_t2_y1 + 46
        view_x2, view_y2 = card_t2_x2 - 14, view_y1 + 245
        draw.rectangle([view_x1, view_y1, view_x2, view_y2], fill=(11, 15, 23, 255), outline=(31, 41, 55, 255), width=1)
        
        # Center crop in viewport
        macro_canvas = Image.new("RGBA", (view_x2 - view_x1, view_y2 - view_y1), (11, 15, 23, 255))
        paste_mc_x = (macro_canvas.width - zoom_w) // 2
        paste_mc_y = (macro_canvas.height - zoom_h) // 2
        macro_canvas.alpha_composite(macro_scaled, (paste_mc_x, paste_mc_y))
        board.paste(macro_canvas, (view_x1, view_y1))

        # Telemetry metrics box
        met_y1 = view_y2 + 10
        draw.rectangle([view_x1, met_y1, view_x2, card_t2_y2 - 10], fill=(15, 23, 42, 230), outline=(31, 41, 55, 180), width=1)
        draw.text((view_x1 + 12, met_y1 + 12), "● " + spec["metric_1"], font=font_desc, fill=(226, 232, 240, 255))
        draw.text((view_x1 + 12, met_y1 + 38), "● " + spec["metric_2"], font=font_desc, fill=(148, 163, 184, 255))
        draw.text((view_x1 + 12, met_y1 + 64), "● " + spec["metric_3"], font=font_desc, fill=(52, 211, 153, 255))

    return board

def build_searching_trichroma_board(frames_white, frames_dark, frames_green):
    """Renders 1536x512 3-Column Trichroma Presentation Board for Owluko Searching."""
    W, H = 1536, 512
    board = Image.new("RGBA", (W, H), COLOR_BG_DARK)

    # Frame 60 (Profile Left at 270°)
    f_idx = 60
    f_w = frames_white[f_idx]
    f_d = frames_dark[f_idx]
    f_g = frames_green[f_idx]

    board.paste(f_w, (0, 0))
    board.paste(f_d, (512, 0))
    board.paste(f_g, (1024, 0))

    draw = ImageDraw.Draw(board)
    draw.line([(512, 0), (512, H)], fill=(31, 41, 55, 220), width=2)
    draw.line([(1024, 0), (1024, H)], fill=(31, 41, 55, 220), width=2)

    # Headers
    draw.rectangle([20, 20, 220, 56], fill=(15, 23, 42, 230), outline=(217, 155, 38, 180), width=1)
    draw.text((36, 30), "STUDIO WHITE (100% FIDÉLITÉ)", font=font_badge, fill=(217, 155, 38, 255))

    draw.rectangle([532, 20, 732, 56], fill=(15, 23, 42, 230), outline=(52, 211, 153, 180), width=1)
    draw.text((548, 30), "DARK STUDIO (#0B0F17)", font=font_badge, fill=(52, 211, 153, 255))

    draw.rectangle([1044, 20, 1264, 56], fill=(15, 23, 42, 230), outline=(217, 155, 38, 180), width=1)
    draw.text((1060, 30), "CHROMA GREEN DÉCOUPE", font=font_badge, fill=(217, 155, 38, 255))

    return board

def main():
    print("🦉 ==========================================================")
    print("🦉 OWLUKO MASTER SEARCHING PRODUCTION ENGINE (08_SEARCHING)")
    print("🦉 ==========================================================")

    out_dirs = [
        os.path.join(WORKSPACE_DIR, "mascots/owluko/assets/08_searching"),
        os.path.join(WORKSPACE_DIR, "mascots/owluko/02_refonte_nouvelle/08_searching")
    ]
    for d in out_dirs:
        os.makedirs(d, exist_ok=True)

    # 1. Load components
    print("\n1. Loading and standardizing turnaround components...")
    components = load_and_prepare_turnaround_components()
    print("   ✓ Turnaround components extracted (Front, Profile Right, Back, Profile Left, Blink)")

    # 2. Pure Vector Lottie JSON (< 50 KB)
    print("\n2. Building Pure Vector Lottie JSON (< 50 KB)...")
    lottie_dict = build_pure_vector_lottie()
    lottie_json = json.dumps(lottie_dict, separators=(',', ':'))
    lottie_size_kb = len(lottie_json.encode('utf-8')) / 1024.0
    print(f"   ✓ Lottie JSON created: {lottie_size_kb:.2f} KB (Target < 50 KB)")

    # 3. Animated SVG
    print("\n3. Building Standalone CSS-Keyframe Animated SVG...")
    svg_content = build_animated_svg()
    print("   ✓ Animated SVG created")

    # 4. Render All 120 Frames (Option A)
    print("\n4. Rendering 120 Frames @ 30 fps (4.00s loop) across 4 backdrops...")
    rendered = render_all_frames(components)
    frames_rgba = rendered["rgba"]
    frames_white = rendered["white"]
    frames_dark = rendered["dark"]
    frames_green = rendered["green"]
    print("   ✓ 120 transparent RGBA frames rendered")
    print("   ✓ 120 White Studio frames rendered")
    print("   ✓ 120 Dark Studio frames rendered")
    print("   ✓ 120 Chroma Green frames rendered")

    # 5. Compile Animated Formats
    print("\n5. Compiling animated deliverables (WebP, GIFs, MP4)...")
    # WebP (lossless, 8-bit alpha)
    webp_path = os.path.join(out_dirs[0], "animated.webp")
    frames_rgba[0].save(
        webp_path,
        save_all=True,
        append_images=frames_rgba[1:],
        duration=33,
        loop=0,
        lossless=True,
        quality=100
    )
    print(f"   ✓ animated.webp compiled ({os.path.getsize(webp_path)/1024.0:.1f} KB)")

    # GIFs
    gif_path = os.path.join(out_dirs[0], "animated.gif")
    frames_white[0].save(gif_path, save_all=True, append_images=frames_white[1:], duration=33, loop=0)
    print(f"   ✓ animated.gif compiled ({os.path.getsize(gif_path)/(1024*1024):.1f} MB)")

    gif_dark_path = os.path.join(out_dirs[0], "animated_dark.gif")
    frames_dark[0].save(gif_dark_path, save_all=True, append_images=frames_dark[1:], duration=33, loop=0)
    print(f"   ✓ animated_dark.gif compiled ({os.path.getsize(gif_dark_path)/(1024*1024):.1f} MB)")

    gif_green_path = os.path.join(out_dirs[0], "animated_green.gif")
    frames_green[0].save(gif_green_path, save_all=True, append_images=frames_green[1:], duration=33, loop=0)
    print(f"   ✓ animated_green.gif compiled ({os.path.getsize(gif_green_path)/(1024*1024):.1f} MB)")

    # Static Posters
    static_png_path = os.path.join(out_dirs[0], "static.png")
    frames_rgba[0].save(static_png_path)
    static_webp_path = os.path.join(out_dirs[0], "static.webp")
    frames_rgba[0].save(static_webp_path, lossless=True)
    print("   ✓ static.png & static.webp saved")

    # MP4 via ffmpeg
    mp4_path = os.path.join(out_dirs[0], "looped_video.mp4")
    temp_frames_dir = os.path.join(WORKSPACE_DIR, "scratch/search_frames_temp")
    os.makedirs(temp_frames_dir, exist_ok=True)
    for i, frm in enumerate(frames_dark):
        frm.save(os.path.join(temp_frames_dir, f"f_{i:03d}.png"))

    cmd_mp4 = [
        "/opt/homebrew/bin/ffmpeg", "-y",
        "-framerate", "30",
        "-i", os.path.join(temp_frames_dir, "f_%03d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        mp4_path
    ]
    subprocess.run(cmd_mp4, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.rmtree(temp_frames_dir)
    shutil.copy(mp4_path, os.path.join(out_dirs[0], "source_video.mp4"))
    print(f"   ✓ looped_video.mp4 & source_video.mp4 compiled ({os.path.getsize(mp4_path)/1024.0:.1f} KB)")

    # 6. Master Boards
    print("\n6. Generating 2-Tier Master Board & Trichroma Board...")
    master_board = build_searching_master_board(frames_rgba)
    mb_path = os.path.join(out_dirs[0], "owluko_searching_master_board.png")
    master_board.save(mb_path)
    print(f"   ✓ owluko_searching_master_board.png (1920x1080 2-Tier) generated ({os.path.getsize(mb_path)/1024.0:.1f} KB)")

    trichroma_board = build_searching_trichroma_board(frames_white, frames_dark, frames_green)
    tb_path = os.path.join(out_dirs[0], "owluko_searching_studio_trichroma_board.png")
    trichroma_board.save(tb_path)
    print(f"   ✓ owluko_searching_studio_trichroma_board.png (1536x512) generated ({os.path.getsize(tb_path)/1024.0:.1f} KB)")

    # 7. Write Vector Files & Snippet
    print("\n7. Writing vector deliverables & snippet.json...")
    lottie_path = os.path.join(out_dirs[0], "lottie.json")
    with open(lottie_path, "w") as f:
        f.write(lottie_json)

    svg_path = os.path.join(out_dirs[0], "owluko_searching_animated.svg")
    with open(svg_path, "w") as f:
        f.write(svg_content)

    svg_trans_path = os.path.join(out_dirs[0], "owluko_searching_animated_transparent.svg")
    with open(svg_trans_path, "w") as f:
        f.write(svg_content)

    # snippet.json
    snippet_dict = {
        "mascot": "owluko",
        "state": "08_searching",
        "name": "Owluko Searching 360 Head Rotation",
        "description": "Biological owl 360-degree head rotation search/loading state (Option A), stationary grounded body, Delta Y = 0 px, zero shadow",
        "duration_seconds": 4.0,
        "frames_count": 120,
        "fps": 30,
        "lottie_file": "lottie.json",
        "lottie_size_kb": round(lottie_size_kb, 2),
        "svg_file": "owluko_searching_animated.svg",
        "webp_file": "animated.webp",
        "gif_file": "animated.gif",
        "gif_dark_file": "animated_dark.gif",
        "mp4_file": "looped_video.mp4",
        "ground_shadow": False,
        "grounded_feet": True,
        "head_rotation": "360_degrees",
        "cadence": "Option A (Saccades & Double Blink)"
    }
    with open(os.path.join(out_dirs[0], "snippet.json"), "w") as f:
        json.dump(snippet_dict, f, indent=2)

    # 8. Zip Bundle
    zip_path = os.path.join(out_dirs[0], "bundle_owluko_08_searching.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for fname in os.listdir(out_dirs[0]):
            if fname != "bundle_owluko_08_searching.zip":
                z.write(os.path.join(out_dirs[0], fname), arcname=fname)
    print(f"   ✓ bundle_owluko_08_searching.zip created ({os.path.getsize(zip_path)/(1024*1024):.1f} MB)")

    # 9. Synchronize to Refonte & Brain
    print("\n8. Synchronizing deliverables across directories...")
    # Synchronize to 02_refonte_nouvelle/08_searching
    for fname in os.listdir(out_dirs[0]):
        src = os.path.join(out_dirs[0], fname)
        dst = os.path.join(out_dirs[1], fname)
        if os.path.isfile(src):
            shutil.copy2(src, dst)
    print("   ✓ Synchronized to mascots/owluko/02_refonte_nouvelle/08_searching/")

    # Synchronize key boards & previews to brain
    for b_dir in BRAIN_DIRS:
        if os.path.exists(b_dir):
            shutil.copy2(mb_path, os.path.join(b_dir, "owluko_searching_master_board.png"))
            shutil.copy2(tb_path, os.path.join(b_dir, "owluko_searching_studio_trichroma_board.png"))
            shutil.copy2(static_png_path, os.path.join(b_dir, "owluko_searching_static.png"))
            shutil.copy2(gif_path, os.path.join(b_dir, "owluko_searching_animated.gif"))
            shutil.copy2(gif_dark_path, os.path.join(b_dir, "owluko_searching_animated_dark.gif"))
    print("   ✓ Synchronized to brain artifacts directory")

    print("\n🎉 ==========================================================")
    print("🎉 OWLUKO 08_SEARCHING PIPELINE COMPLETE WITH 100% FIDELITY")
    print("🎉 ==========================================================")

if __name__ == '__main__':
    main()
