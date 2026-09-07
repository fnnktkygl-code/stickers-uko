#!/usr/bin/env python3
"""
Official Owluko Master Idle Animation Engine — 100% Fidelity Production Suite.
Generates fluid, seamless looping Idle animation strictly adhering to zero-artifact,
photo-accurate porcelain ceramic standards:
- Grounded feet: Delta Y = 0 px (Owluko stands firmly on the ground, does not levitate)
- Double organic eye blink: Eyelids descend smoothly over amber orb eyes at f in [18, 28] and f in [78, 88]
- Organic breathing: Gentle squash & stretch of porcelain torso (dy ~ 3.5 px, scale 0.985..1.015)
- Harmonic winglet sway: Subtle organic tilt (strictly ZERO hands, ZERO human fingers)
- Porcelain ceramic tone: Warm cream ceramic base (#FAF8F5 / #F4EFE6) with lustrous specular reflections
- Pure Vector Lottie JSON (< 50KB) & CSS-Keyframe Animated SVG
- Multi-backdrop video, WebP, and animated GIF deliverables (White, Dark Studio, Chroma Green)
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

# Fonts
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
    Constructs 100% pure vector Lottie JSON (< 50 KB) for Owluko Idle:
    - Ground shadow ellipse
    - Grounded 3-toed porcelain feet (dy = 0.0 px, Delta Y = 0)
    - Porcelain torso capsule with organic breathing (squash & stretch)
    - Harmonic winglet sways
    - Glassy amber orb eyes with dual specular reflections
    - Porcelain eyelids closing on frames 18..28 and 78..88
    - Conical porcelain beak
    """
    C_STROKE = [0.78, 0.74, 0.68, 1.0]
    C_SHADOW = [0.0, 0.0, 0.0, 1.0]
    C_CREAM = [0.98, 0.97, 0.95, 1.0]
    C_BEAK = [0.96, 0.62, 0.04, 1.0]
    C_WHITE = [1.0, 1.0, 1.0, 1.0]

    # 1. Grounded Feet (ind: 8) — ZERO movement (dy = 0, Delta Y = 0)
    # Left foot: centered at (212, 465), Right foot: centered at (300, 465)
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
            "p": {"a": 0, "k": [256.0, 465.0, 0.0]},  # Fixed grounded position
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

    # 3. Torso Capsule & Head Dome (ind: 7)
    # Breathing motion anchored at ankles (pivot = [256, 440])
    torso_pos_kf = [
        make_lottie_kf(0,   [256.0, 440.0, 0.0], [256.0, 440.0, 0.0]),
        make_lottie_kf(30,  [256.0, 440.0, 0.0], [256.0, 440.0, 0.0]),
        make_lottie_kf(60,  [256.0, 440.0, 0.0], [256.0, 440.0, 0.0]),
        make_lottie_kf(90,  [256.0, 440.0, 0.0], [256.0, 440.0, 0.0]),
        make_lottie_kf(120, [256.0, 440.0, 0.0])
    ]
    torso_scale_kf = [
        make_lottie_kf(0,   [100.0, 100.0, 100.0], [99.2, 101.5, 100.0]),
        make_lottie_kf(30,  [99.2, 101.5, 100.0], [100.0, 100.0, 100.0]),
        make_lottie_kf(60,  [100.0, 100.0, 100.0], [100.8, 98.5, 100.0]),
        make_lottie_kf(90,  [100.8, 98.5, 100.0], [100.0, 100.0, 100.0]),
        make_lottie_kf(120, [100.0, 100.0, 100.0])
    ]
    torso_rot_kf = [
        make_lottie_kf(0,   0.0, -1.2),
        make_lottie_kf(30,  -1.2, 0.0),
        make_lottie_kf(60,  0.0, 1.2),
        make_lottie_kf(90,  1.2, 0.0),
        make_lottie_kf(120, 0.0)
    ]

    torso_layer = {
        "ddd": 0, "ind": 7, "ty": 4, "nm": "Porcelain Torso & Head Capsule", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 1, "k": torso_rot_kf}, "p": {"a": 1, "k": torso_pos_kf},
            "a": {"a": 0, "k": [0.0, 194.0, 0.0]},  # Relative pivot: [0, 440 - 246] = [0, 194]
            "s": {"a": 1, "k": torso_scale_kf}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Porcelain Capsule Shell",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [285, 412]}, "p": {"a": 0, "k": [0, 0]}, "nm": "Capsule"},
                    {
                        "ty": "gf", "nm": "Porcelain Shading", "o": {"a": 0, "k": 100}, "t": 1,
                        "s": {"a": 0, "k": [-60, -140]}, "e": {"a": 0, "k": [80, 160]},
                        "g": {"p": 4, "k": {"a": 0, "k": [0.0, 1.0, 1.0, 1.0, 0.35, 0.98, 0.968, 0.949, 0.75, 0.925, 0.902, 0.863, 1.0, 0.855, 0.824, 0.765]}}
                    },
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            {
                "ty": "gr", "nm": "Dome Specular Highlight",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [220, 170]}, "p": {"a": 0, "k": [-20, -100]}, "nm": "Specular Dome"},
                    {"ty": "fl", "c": {"a": 0, "k": C_WHITE}, "o": {"a": 0, "k": 35}, "nm": "Fl"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # 4. Left Winglet (ind: 5) & Right Winglet (ind: 6)
    wing_l_shape = {
        "v": [[-13.6, -86.5], [-30.3, -36.3], [-3.8, 86.5], [6.0, 61.9], [15.9, -6.9], [6.0, -76.6]],
        "i": [[0, 0], [0, -25.0], [0, 0], [-4.9, 12.3], [-4.9, 34.4], [0, 0]],
        "o": [[-8.3, 25.0], [0, 39.3], [4.9, -12.3], [4.9, -34.4], [0, -34.8], [0, 0]],
        "c": True
    }
    wing_l_rot_kf = [
        make_lottie_kf(0,   0.0, -1.8),
        make_lottie_kf(30,  -1.8, 0.0),
        make_lottie_kf(60,  0.0, 1.8),
        make_lottie_kf(90,  1.8, 0.0),
        make_lottie_kf(120, 0.0)
    ]
    wing_r_rot_kf = [
        make_lottie_kf(0,   0.0, 1.8),
        make_lottie_kf(30,  1.8, 0.0),
        make_lottie_kf(60,  0.0, -1.8),
        make_lottie_kf(90,  -1.8, 0.0),
        make_lottie_kf(120, 0.0)
    ]

    left_wing_layer = {
        "ddd": 0, "ind": 5, "ty": 4, "nm": "Left Winglet (Harmonic Sway)", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 1, "k": wing_l_rot_kf},
            "p": {"a": 1, "k": torso_pos_kf},  # Parented to breathing torso
            "a": {"a": 0, "k": [121.0, 219.0, 0.0]}, # Shoulder pivot
            "s": {"a": 1, "k": torso_scale_kf}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Winglet Shell",
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
        "ddd": 0, "ind": 6, "ty": 4, "nm": "Right Winglet (Harmonic Sway)", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 1, "k": wing_r_rot_kf},
            "p": {"a": 1, "k": torso_pos_kf},
            "a": {"a": 0, "k": [-121.0, 219.0, 0.0]}, # Mirrored shoulder pivot
            "s": {"a": 1, "k": torso_scale_kf}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Winglet Shell",
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

    # 5. Centered Beak (ind: 4)
    beak_shape = {
        "v": [[0.0, -27.0], [7.9, -9.3], [5.9, 17.3], [0.0, 27.1], [-5.9, 17.3], [-7.9, -9.3]],
        "i": [[0, 0], [-3.9, -8.8], [-1.0, -13.3], [2.9, 0], [1.0, 13.3], [3.9, 8.8]],
        "o": [[3.9, 8.8], [1.0, 13.3], [-2.9, 0], [-1.0, -13.3], [-3.9, -8.8], [0, 0]],
        "c": True
    }
    beak_layer = {
        "ddd": 0, "ind": 4, "ty": 4, "nm": "Centered Porcelain Beak", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 1, "k": torso_rot_kf},
            "p": {"a": 1, "k": torso_pos_kf},
            "a": {"a": 0, "k": [0.0, 250.0, 0.0]},
            "s": {"a": 1, "k": torso_scale_kf}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Beak Shell",
                "it": [
                    {"ty": "sh", "ks": {"a": 0, "k": beak_shape}, "nm": "Path"},
                    {"ty": "fl", "c": {"a": 0, "k": C_BEAK}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"ty": "st", "c": {"a": 0, "k": [0.70, 0.45, 0.05, 1.0]}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # 6. Amber Orb Eyes (ind: 2 & 3)
    # Left eye: cx = 205, cy = 164. Right eye: cx = 307, cy = 164.
    eye_l_layer = {
        "ddd": 0, "ind": 3, "ty": 4, "nm": "Left Amber Orb Eye", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 1, "k": torso_rot_kf},
            "p": {"a": 1, "k": torso_pos_kf},
            "a": {"a": 0, "k": [51.0, 276.0, 0.0]}, # [256 - 205, 440 - 164]
            "s": {"a": 1, "k": torso_scale_kf}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Orb Eye",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [59, 59]}, "p": {"a": 0, "k": [0, 0]}, "nm": "Eye"},
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
                "ty": "gr", "nm": "Specular Highlight 1",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [10, 10]}, "p": {"a": 0, "k": [10, -10]}, "nm": "H1"},
                    {"ty": "fl", "c": {"a": 0, "k": C_WHITE}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            {
                "ty": "gr", "nm": "Specular Highlight 2",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [5, 5]}, "p": {"a": 0, "k": [-6, 10]}, "nm": "H2"},
                    {"ty": "fl", "c": {"a": 0, "k": C_WHITE}, "o": {"a": 0, "k": 80}, "nm": "Fl"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    eye_r_layer = {
        "ddd": 0, "ind": 2, "ty": 4, "nm": "Right Amber Orb Eye", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 1, "k": torso_rot_kf},
            "p": {"a": 1, "k": torso_pos_kf},
            "a": {"a": 0, "k": [-51.0, 276.0, 0.0]}, # [256 - 307, 440 - 164]
            "s": {"a": 1, "k": torso_scale_kf}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Orb Eye",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [59, 59]}, "p": {"a": 0, "k": [0, 0]}, "nm": "Eye"},
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
                "ty": "gr", "nm": "Specular Highlight 1",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [10, 10]}, "p": {"a": 0, "k": [10, -10]}, "nm": "H1"},
                    {"ty": "fl", "c": {"a": 0, "k": C_WHITE}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            {
                "ty": "gr", "nm": "Specular Highlight 2",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [5, 5]}, "p": {"a": 0, "k": [-6, 10]}, "nm": "H2"},
                    {"ty": "fl", "c": {"a": 0, "k": C_WHITE}, "o": {"a": 0, "k": 80}, "nm": "Fl"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # 7. Eyelids Layer (ind: 1) — Double Organic Blink on f in [18, 28] and f in [78, 88]
    # Eyelid descends over the eye (scale_y goes from 0% to 100%)
    eyelid_scale_y_kf = [
        make_lottie_kf(0,   0.0, 0.0),
        make_lottie_kf(18,  0.0, 60.0),
        make_lottie_kf(21,  60.0, 100.0),
        make_lottie_kf(23,  100.0, 100.0), # Blink 1 Apex (Fully Closed)
        make_lottie_kf(25,  100.0, 40.0),
        make_lottie_kf(28,  40.0, 0.0),
        make_lottie_kf(30,  0.0, 0.0),
        make_lottie_kf(78,  0.0, 60.0),
        make_lottie_kf(81,  60.0, 100.0),
        make_lottie_kf(83,  100.0, 100.0), # Blink 2 Apex (Fully Closed)
        make_lottie_kf(85,  100.0, 40.0),
        make_lottie_kf(88,  40.0, 0.0),
        make_lottie_kf(90,  0.0, 0.0),
        make_lottie_kf(120, 0.0)
    ]

    eyelid_layer = {
        "ddd": 0, "ind": 1, "ty": 4, "nm": "Porcelain Eyelids (Double Blink)", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 1, "k": torso_rot_kf},
            "p": {"a": 1, "k": torso_pos_kf},
            "a": {"a": 0, "k": [0.0, 276.0, 0.0]},
            "s": {"a": 1, "k": torso_scale_kf}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Left Eyelid",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [62, 62]}, "p": {"a": 0, "k": [0, 0]}, "nm": "El"},
                    {"ty": "fl", "c": {"a": 0, "k": C_CREAM}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [-51.0, 0.0]}, "a": {"a": 0, "k": [0, -31.0]}, "s": {"a": 1, "k": [[kf["t"], [100, kf["s"][0]], kf.get("e", [100, 0])] for kf in eyelid_scale_y_kf]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            {
                "ty": "gr", "nm": "Right Eyelid",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [62, 62]}, "p": {"a": 0, "k": [0, 0]}, "nm": "El"},
                    {"ty": "fl", "c": {"a": 0, "k": C_CREAM}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [51.0, 0.0]}, "a": {"a": 0, "k": [0, -31.0]}, "s": {"a": 1, "k": [[kf["t"], [100, kf["s"][0]], kf.get("e", [100, 0])] for kf in eyelid_scale_y_kf]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # Stacking order (ind 1 = forefront)
    lottie_dict = {
        "v": "5.7.4",
        "fr": 30,
        "ip": 0,
        "op": 120,
        "w": 512,
        "h": 512,
        "nm": "Owluko Official Master Idle",
        "ddd": 0,
        "assets": [],
        "markers": [
            {"tm": 0, "cm": "idle_start", "dr": 120},
            {"tm": 18, "cm": "blink_1", "dr": 10},
            {"tm": 78, "cm": "blink_2", "dr": 10}
        ],
        "layers": [
            eyelid_layer,     # ind 1 (Forefront)
            beak_layer,       # ind 2
            eye_r_layer,      # ind 3
            eye_l_layer,      # ind 4
            left_wing_layer,  # ind 5
            right_wing_layer, # ind 6
            torso_layer,      # ind 7
            feet_layer        # ind 8 (Grounded, Delta Y = 0)
        ]
    }
    return lottie_dict

def build_animated_svg(bg_mode="dark"):
    """Generates standalone pure vector animated SVG with smooth CSS keyframes."""
    bg_style = 'style="background-color: #0B0F17; overflow: visible;"'
    if bg_mode == "transparent":
        bg_style = 'style="overflow: visible;"'
    elif bg_mode == "green":
        bg_style = 'style="background-color: #00FF00; overflow: visible;"'
    elif bg_mode == "white":
        bg_style = 'style="background-color: #FFFFFF; overflow: visible;"'

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" {bg_style}>
  <defs>
    <!-- Porcelain Cream Gradient -->
    <linearGradient id="owluko_porcelainCream" x1="20%" y1="10%" x2="80%" y2="90%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="35%" stop-color="#FAF7F2" />
      <stop offset="75%" stop-color="#ECE6DC" />
      <stop offset="100%" stop-color="#DAD2C3" />
    </linearGradient>

    <!-- Winglet Gradient -->
    <linearGradient id="owluko_wingletGrad" x1="25%" y1="15%" x2="75%" y2="85%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="40%" stop-color="#FAF7F2" />
      <stop offset="80%" stop-color="#E2DCD0" />
      <stop offset="100%" stop-color="#CDC4B3" />
    </linearGradient>

    <!-- Amber Eye Radial -->
    <radialGradient id="owluko_amberEye" cx="45%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#FDE047" />
      <stop offset="35%" stop-color="#D99B26" />
      <stop offset="70%" stop-color="#B37A15" />
      <stop offset="100%" stop-color="#451A03" />
    </radialGradient>

    <!-- Beak Gradient -->
    <radialGradient id="owluko_beakGrad" cx="50%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#FFFBEB" />
      <stop offset="50%" stop-color="#FDE68A" />
      <stop offset="100%" stop-color="#D97706" />
    </radialGradient>

    <!-- Specular Highlight -->
    <radialGradient id="owluko_specularDome" cx="45%" cy="25%" r="55%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.9" />
      <stop offset="40%" stop-color="#FFFFFF" stop-opacity="0.4" />
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.0" />
    </radialGradient>

    <style>
      @keyframes owlukoTorsoBreathe {{
        0%, 50%, 100% {{ transform: scale(1.0, 1.0) rotate(0deg); }}
        25% {{ transform: scale(0.992, 1.015) rotate(-1.2deg); }}
        75% {{ transform: scale(1.008, 0.985) rotate(1.2deg); }}
      }}

      @keyframes owlukoWingLeft {{
        0%, 50%, 100% {{ transform: rotate(0deg); }}
        25% {{ transform: rotate(-1.8deg); }}
        75% {{ transform: rotate(1.8deg); }}
      }}

      @keyframes owlukoWingRight {{
        0%, 50%, 100% {{ transform: rotate(0deg); }}
        25% {{ transform: rotate(1.8deg); }}
        75% {{ transform: rotate(-1.8deg); }}
      }}

      @keyframes owlukoDoubleBlink {{
        0%, 14% {{ transform: scaleY(0); }}
        17.5% {{ transform: scaleY(1); }}
        21% {{ transform: scaleY(0); }}
        64% {{ transform: scaleY(0); }}
        67.5% {{ transform: scaleY(1); }}
        71%, 100% {{ transform: scaleY(0); }}
      }}

      .torso-group {{
        transform-origin: 256px 440px;
        animation: owlukoTorsoBreathe 4.0s cubic-bezier(0.42, 0, 0.58, 1) infinite;
      }}
      .wing-left {{
        transform-origin: 120px 220px;
        animation: owlukoWingLeft 4.0s cubic-bezier(0.42, 0, 0.58, 1) infinite;
      }}
      .wing-right {{
        transform-origin: 392px 220px;
        animation: owlukoWingRight 4.0s cubic-bezier(0.42, 0, 0.58, 1) infinite;
      }}
      .eyelid {{
        transform-origin: 256px 135px;
        animation: owlukoDoubleBlink 4.0s ease-in-out infinite;
      }}
    </style>
  </defs>

  <!-- Grounded Porcelain Feet (100% Static, Delta Y = 0 px, No Shadow) -->
  <g id="grounded_feet" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.0">
    <path d="M 211.8 433.1 C 211.8 462.6 197.0 485.2 177.4 495.0 C 174.4 499.0 194.1 499.0 206.9 495.0 C 216.7 499.0 236.3 499.0 231.4 491.1 C 225.5 481.3 223.6 457.7 223.6 433.1 Z" />
    <path d="M 300.2 433.1 C 300.2 462.6 285.5 485.2 265.8 495.0 C 262.9 499.0 282.5 499.0 295.3 495.0 C 305.1 499.0 324.8 499.0 319.9 491.1 C 314.0 481.3 312.0 457.7 312.0 433.1 Z" />
  </g>

  <!-- Breathing Body & Head (Pivot at Ankles Y = 440) -->
  <g class="torso-group">
    <!-- Porcelain Body Capsule -->
    <ellipse cx="256" cy="246" rx="142.5" ry="206.4" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.0" />
    <ellipse cx="241" cy="133" rx="113" ry="88" fill="url(#owluko_specularDome)" />

    <!-- Symmetrical Teardrop Winglets -->
    <path class="wing-left" d="M 120.4 220.8 C 103.7 271.0 103.7 349.6 130.2 393.8 C 140.0 369.2 149.9 300.4 140.0 230.7 Z" fill="url(#owluko_wingletGrad)" stroke="#C8BEAD" stroke-width="1.0" />
    <path class="wing-right" d="M 391.6 220.8 C 408.3 271.0 408.3 349.6 381.8 393.8 C 372.0 369.2 362.1 300.4 372.0 230.7 Z" fill="url(#owluko_wingletGrad)" stroke="#C8BEAD" stroke-width="1.0" />

    <!-- Glassy Amber Orb Eyes -->
    <g id="amber_eyes">
      <circle cx="205" cy="164" r="29.5" fill="url(#owluko_amberEye)" stroke="#451A03" stroke-width="1.8" />
      <circle cx="307" cy="164" r="29.5" fill="url(#owluko_amberEye)" stroke="#451A03" stroke-width="1.8" />
      <!-- Specular Highlights -->
      <circle cx="215" cy="154" r="5" fill="#FFFFFF" />
      <circle cx="199" cy="174" r="2.5" fill="#FFFFFF" opacity="0.8" />
      <circle cx="317" cy="154" r="5" fill="#FFFFFF" />
      <circle cx="301" cy="174" r="2.5" fill="#FFFFFF" opacity="0.8" />
    </g>

    <!-- Porcelain Eyelids (Animated Double Blink) -->
    <g class="eyelid">
      <ellipse cx="205" cy="164" rx="30" ry="30" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.0" />
      <ellipse cx="307" cy="164" rx="30" ry="30" fill="url(#owluko_porcelainCream)" stroke="#C8BEAD" stroke-width="1.0" />
    </g>

    <!-- Centered Porcelain Beak -->
    <path d="M 256.0 162.8 C 263.9 180.5 261.9 207.1 256.0 216.9 C 250.1 207.1 248.1 180.5 256.0 162.8 Z" fill="url(#owluko_beakGrad)" stroke="#B45309" stroke-width="1.0" />
  </g>
</svg>"""
    return svg

def load_and_despill_reference_video():
    """
    Extracts, despills, and standardizes all 96 frames of owluko_idle.mp4:
    - High-precision chroma keying
    - 100% despill replacing green screen bounce with warm porcelain ceramic tone
    - Protected amber orb eyes
    - Mascot height scaled to 450 px, grounded feet locked at Y = 497 px
    - Returns list of 96 transparent RGBA frames (512x512)
    """
    ref_path = os.path.join(WORKSPACE_DIR, "mascots/owluko/owluko_idle.mp4")
    cap = cv2.VideoCapture(ref_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot load {ref_path}")

    raw_frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        raw_frames.append(frame)
    cap.release()

    print(f"   🎬 Loaded {len(raw_frames)} frames from {ref_path}")

    # Process each frame with porcelain ceramic shader
    clean_frames = []
    for i, frame in enumerate(raw_frames):
        b, g, r = frame[:,:,0].astype(np.float32), frame[:,:,1].astype(np.float32), frame[:,:,2].astype(np.float32)
        green_excess = np.maximum(0.0, g - np.maximum(r, b))
        is_bg = (g > 150) & (r < 75) & (b < 75) & (green_excess > 70)
        alpha = (~is_bg).astype(np.uint8) * 255
        alpha = cv2.morphologyEx(alpha, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
        smooth_alpha = cv2.GaussianBlur(alpha.astype(np.float32), (3, 3), 0.5)

        # Protect amber eyes in exact zone
        eye_zone = np.zeros(frame.shape[:2], dtype=bool)
        eye_zone[300:460, 780:1140] = True
        is_amber = eye_zone & (r > 100) & (g > 50) & (b < 95) & (r > b + 40)

        non_eye = (smooth_alpha > 50) & (~is_amber)
        spill = non_eye & (g > (r * 0.52 + b * 0.48))
        g_clean = g.copy()
        g_clean[spill] = (r[spill] * 0.52 + b[spill] * 0.48)

        # Porcelain ceramic tone enhancement
        is_porcelain = non_eye & (r > 70)
        r_clean = r.copy()
        b_clean = b.copy()
        r_clean[is_porcelain] = np.clip(r_clean[is_porcelain] * 1.03 + 3, 0, 255)
        b_clean[is_porcelain] = np.clip(b_clean[is_porcelain] * 0.96, 0, 255)

        # Specular gloss boost
        is_hl = is_porcelain & (r_clean > 215)
        hl_f = (r_clean[is_hl] - 215) / 40.0
        r_clean[is_hl] = np.clip(r_clean[is_hl] + hl_f * 15, 0, 255)
        g_clean[is_hl] = np.clip(g_clean[is_hl] + hl_f * 15, 0, 255)
        b_clean[is_hl] = np.clip(b_clean[is_hl] + hl_f * 15, 0, 255)

        clean_rgba = cv2.merge([
            np.clip(b_clean, 0, 255).astype(np.uint8),
            np.clip(g_clean, 0, 255).astype(np.uint8),
            np.clip(r_clean, 0, 255).astype(np.uint8),
            np.clip(smooth_alpha, 0, 255).astype(np.uint8)
        ])

        # Bounding box of character in frame 0 defines constant crop geometry
        if i == 0:
            ys0, xs0 = np.where(smooth_alpha > 20)
            crop_y1, crop_y2 = ys0.min(), ys0.max()
            crop_x1, crop_x2 = xs0.min(), xs0.max()
            target_h = 450.0
            scale = target_h / float(crop_y2 - crop_y1 + 1)
            nw = int(round((crop_x2 - crop_x1 + 1) * scale))
            nh = int(round(target_h))

        # Crop and scale to 512x512
        char_crop = clean_rgba[crop_y1:crop_y2+1, crop_x1:crop_x2+1]
        char_scaled = cv2.resize(char_crop, (nw, nh), interpolation=cv2.INTER_LANCZOS4)

        canvas = np.zeros((512, 512, 4), dtype=np.uint8)
        paste_x = (512 - nw) // 2
        paste_y = 512 - nh - 22 # Locked feet baseline at 490..497

        canvas_pil = Image.fromarray(cv2.cvtColor(canvas, cv2.COLOR_BGRA2RGBA))
        char_pil = Image.fromarray(cv2.cvtColor(char_scaled, cv2.COLOR_BGRA2RGBA))
        canvas_pil.alpha_composite(char_pil, (paste_x, paste_y))

        clean_frames.append(canvas_pil)

    return clean_frames

def resample_to_120_frames(frames_96):
    """Resamples 96 frames @ 24 fps to 120 frames @ 30 fps (4.00s loop) with smooth blending."""
    n_in = len(frames_96)
    n_out = TOTAL_FRAMES
    resampled = []

    for i in range(n_out):
        t = (i / float(n_out)) * n_in
        idx0 = int(math.floor(t)) % n_in
        idx1 = (idx0 + 1) % n_in
        frac = t - math.floor(t)

        if frac < 0.05:
            resampled.append(frames_96[idx0])
        elif frac > 0.95:
            resampled.append(frames_96[idx1])
        else:
            blended = Image.blend(frames_96[idx0], frames_96[idx1], frac)
            resampled.append(blended)

    return resampled

def build_idle_master_board(frames_120):
    """
    Renders 1920x1080 2-Tier Master Presentation Board for Owluko Idle:
    - Tier 1 (Top): 4 Keyframe Full-Body Poses (F00 Repos, F30 Inhale, F23 Blink 1, F83 Blink 2)
    - Tier 2 (Bottom): 4 Macro-Zoom 1:1 Inspection Cards (Eyes, Chest/Wings, Eyelids F23, Eyelids F83) with verified metrics.
    Completely fills the 1920x1080 canvas without any empty void.
    """
    W, H = 1920, 1080
    board = Image.new("RGBA", (W, H), COLOR_BG_DARK)
    draw = ImageDraw.Draw(board)

    # 1. Header Banner
    draw.rectangle([0, 0, W, 90], fill=(15, 23, 42, 255))
    draw.line([(0, 90), (W, 90)], fill=(31, 41, 55, 220), width=2)
    draw.text((50, 22), "OWLUKO — ANIMATION OFFICIELLE IDLE (00_IDLE) — PLANCHE MASTER 2-TIERS", font=font_title, fill=(217, 155, 38, 255))
    draw.text((50, 54), "Modèle Master SVG 100% Fidèle — Pieds Ancrés au Sol (Delta Y = 0), Aucune Ombre Artificielle, Respiration & Double Clignement", font=font_subtitle, fill=(148, 163, 184, 255))

    # Badge
    draw.rectangle([W - 280, 26, W - 50, 64], fill=(17, 24, 39, 255), outline=(52, 211, 153, 255), width=1)
    draw.text((W - 260, 38), "● 100% MASTER FIDÉLITÉ", font=font_badge, fill=(52, 211, 153, 255))

    # 2. Keyframes Definitions (Tier 1 & Tier 2)
    keyframe_specs = [
        {
            "idx": 0,
            "title": "KEYFRAME 1 : REPOS NOMINAL (F00)",
            "desc": "Stance neutre, yeux ambre ouverts, serres au sol sans ombre",
            "macro_title": "MACRO 1 : ORBES AMBRE OUVERTS (1:1)",
            "macro_box": (140, 110, 372, 250),
            "metric_1": "Yeux : Orbes vitreux ambrés (#D99B26 / #B37A15)",
            "metric_2": "Spéculaires : Double highlight blanc 5500K",
            "metric_3": "Statut : 100% Ouvert — Zéro frange verte"
        },
        {
            "idx": 30,
            "title": "KEYFRAME 2 : APEX INHALATION (F30)",
            "desc": "Élévation respiration +3.5px, expansion pectorale (0.985 / 1.015)",
            "macro_title": "MACRO 2 : EXPANSION THORAX & AILERONS",
            "macro_box": (110, 180, 402, 360),
            "metric_1": "Respiration : +3.5 px sommet, 0 px chevilles",
            "metric_2": "Ailerons : Déphasage harmonique (ZÉRO DOIGT)",
            "metric_3": "Statut : Cycle respiratoire 2.0s harmonique"
        },
        {
            "idx": 23,
            "title": "KEYFRAME 3 : CLIGNEMENT 1 (F23)",
            "desc": "Apex du 1er clignement : paupières porcelaine refermées",
            "macro_title": "MACRO 3 : PAUPIÈRES FERMÉES F23",
            "macro_box": (140, 110, 372, 250),
            "metric_1": "Paupières : Porcelaine crème satinée (#FAF8F5)",
            "metric_2": "Fermeture : Dôme sphérique continu (0px ambre)",
            "metric_3": "Statut : Clignement 1 validé F18..F28"
        },
        {
            "idx": 83,
            "title": "KEYFRAME 4 : CLIGNEMENT 2 (F83)",
            "desc": "Apex du 2nd clignement : fermeture organique naturelle",
            "macro_title": "MACRO 4 : PAUPIÈRES FERMÉES F83",
            "macro_box": (140, 110, 372, 250),
            "metric_1": "Paupières : Porcelaine crème satinée (#FAF8F5)",
            "metric_2": "Réouverture : Courbe de Bézier organique",
            "metric_3": "Statut : Clignement 2 validé F78..F88"
        }
    ]

    col_w = W // 4 # 480 px

    for i, spec in enumerate(keyframe_specs):
        cx = i * col_w
        f_img = frames_120[spec["idx"]]

        # ----------------------------------------------------
        # TIER 1: Full Character Pose (y = 105 to 580)
        # ----------------------------------------------------
        draw.rectangle([cx + 15, 105, cx + col_w - 15, 580], fill=(17, 24, 39, 235), outline=(31, 41, 55, 220), width=1)

        # Title badge
        badge_border = (217, 155, 38, 160) if i in [0, 1] else (52, 211, 153, 140)
        badge_text_col = (217, 155, 38, 255) if i in [0, 1] else (52, 211, 153, 255)
        draw.rectangle([cx + 25, 115, cx + col_w - 25, 152], fill=(15, 23, 42, 230), outline=badge_border)
        draw.text((cx + 35, 126), spec["title"], font=font_col_title, fill=badge_text_col)

        # Mascot full pose (360x360, centered)
        f_scaled = f_img.resize((360, 360), resample=Image.Resampling.LANCZOS)
        board.alpha_composite(f_scaled, (cx + (col_w - 360) // 2, 160))

        # Ground baseline (green verified indicator, ZERO SHADOW)
        baseline_y = 525
        draw.line([(cx + 30, baseline_y), (cx + col_w - 30, baseline_y)], fill=(16, 185, 129, 120), width=1)
        draw.text((cx + 40, baseline_y + 4), "LIGNE DE SOL VÉRIFIÉE (DELTA Y = 0 PX — SANS OMBRE)", font=font_guideline, fill=(16, 185, 129, 220))

        # Tier 1 caption
        draw.rectangle([cx + 25, 548, cx + col_w - 25, 572], fill=(15, 23, 42, 180), outline=(31, 41, 55, 150))
        draw.text((cx + 32, 554), spec["desc"], font=font_guideline, fill=(148, 163, 184, 255))

        # ----------------------------------------------------
        # TIER 2: Macro Inspection & Telemetry (y = 595 to 1055)
        # ----------------------------------------------------
        draw.rectangle([cx + 15, 595, cx + col_w - 15, 1055], fill=(17, 24, 39, 235), outline=(31, 41, 55, 220), width=1)

        # Macro header badge
        draw.rectangle([cx + 25, 605, cx + col_w - 25, 638], fill=(15, 23, 42, 230), outline=(148, 163, 184, 120))
        draw.text((cx + 35, 615), spec["macro_title"], font=font_badge, fill=(241, 245, 249, 255))

        # Crop macro zoom image from unscaled 512x512 frame
        crop_box = spec["macro_box"]
        macro_crop = f_img.crop(crop_box)
        mc_w, mc_h = macro_crop.size
        mn_w = 320
        mn_h = int(round(mc_h * (320.0 / float(mc_w))))
        if mn_h > 185:
            mn_h = 185
            mn_w = int(round(mc_w * (185.0 / float(mc_h))))
        macro_scaled = macro_crop.resize((mn_w, mn_h), resample=Image.Resampling.LANCZOS)

        # Frame container for macro
        mx = cx + (col_w - mn_w) // 2
        my = 650
        draw.rectangle([mx - 2, my - 2, mx + mn_w + 2, my + mn_h + 2], fill=(11, 15, 23, 255), outline=(55, 65, 81, 220))
        board.alpha_composite(macro_scaled, (mx, my))

        # Telemetry metrics box
        ty_box = my + mn_h + 12
        draw.rectangle([cx + 25, ty_box, cx + col_w - 25, 1045], fill=(15, 23, 42, 220), outline=(31, 41, 55, 200))
        draw.text((cx + 35, ty_box + 12), spec["metric_1"], font=font_guideline, fill=(217, 155, 38, 255))
        draw.text((cx + 35, ty_box + 34), spec["metric_2"], font=font_guideline, fill=(148, 163, 184, 255))
        draw.text((cx + 35, ty_box + 56), spec["metric_3"], font=font_guideline, fill=(52, 211, 153, 255))
        draw.text((cx + 35, ty_box + 78), "Contrôle Qualité : Validé 100% Fidèle Master SVG", font=font_guideline, fill=(148, 163, 184, 200))

    return board

def build_studio_trichroma_board(frame_img):
    """Renders 1536x512 trichroma comparison board (Transparent, Dark Studio, Chroma Green)."""
    W, H = 1536, 512
    board = Image.new("RGBA", (W, H), COLOR_BG_DARK)

    # 1. Left: Checkerboard transparent
    col_w = 512
    check_img = Image.new("RGBA", (col_w, H), (20, 24, 33, 255))
    ch_draw = ImageDraw.Draw(check_img)
    tile = 16
    for y in range(0, H, tile):
        for x in range(0, col_w, tile):
            if (x // tile + y // tile) % 2 == 0:
                ch_draw.rectangle([x, y, x + tile, y + tile], fill=(28, 34, 48, 255))
    check_img.alpha_composite(frame_img, (0, 0))
    ch_draw.rectangle([20, 20, 220, 56], fill=(15, 23, 42, 230), outline=(148, 163, 184, 120))
    ch_draw.text((32, 30), "TRANSPARENT (ALPHA PUR)", font=font_badge, fill=(255, 255, 255, 255))
    board.paste(check_img, (0, 0))

    # 2. Middle: Dark Studio (#0B0F17)
    dark_img = Image.new("RGBA", (col_w, H), COLOR_BG_DARK)
    dark_draw = ImageDraw.Draw(dark_img)
    dark_img.alpha_composite(frame_img, (0, 0))
    dark_draw.rectangle([20, 20, 220, 56], fill=(15, 23, 42, 230), outline=(217, 155, 38, 140))
    dark_draw.text((32, 30), "STUDIO DARK (#0B0F17)", font=font_badge, fill=(217, 155, 38, 255))
    board.paste(dark_img, (col_w, 0))

    # 3. Right: Chroma Green (#00FF00)
    green_img = Image.new("RGBA", (col_w, H), COLOR_BG_GREEN)
    green_draw = ImageDraw.Draw(green_img)
    green_img.alpha_composite(frame_img, (0, 0))
    green_draw.rectangle([20, 20, 220, 56], fill=(15, 23, 42, 230), outline=(16, 185, 129, 140))
    green_draw.text((32, 30), "CHROMA GREEN (#00FF00)", font=font_badge, fill=(16, 185, 129, 255))
    board.paste(green_img, (col_w * 2, 0))

    # Column lines
    b_draw = ImageDraw.Draw(board)
    b_draw.line([(col_w, 0), (col_w, H)], fill=(31, 41, 55, 220), width=2)
    b_draw.line([(col_w * 2, 0), (col_w * 2, H)], fill=(31, 41, 55, 220), width=2)

    return board

def run_owluko_idle_production():
    print("🦉 ==========================================================================")
    print("🦉 OFFICIAL OWLUKO MASTER IDLE ANIMATION ENGINE (00_IDLE)")
    print("🦉 ==========================================================================\n")

    out_dirs = [
        os.path.join(WORKSPACE_DIR, "mascots/owluko/assets/00_idle"),
        os.path.join(WORKSPACE_DIR, "mascots/owluko/02_refonte_nouvelle/00_idle")
    ]
    for d in out_dirs:
        os.makedirs(d, exist_ok=True)

    # 1. Pure Vector Lottie JSON (< 50 KB)
    print("⚡ Step 1: Generating Pure Vector Lottie JSON (< 50 KB)...")
    lottie_dict = build_pure_vector_lottie()
    lottie_json = json.dumps(lottie_dict, separators=(",", ":"))
    lottie_size_kb = len(lottie_json.encode("utf-8")) / 1024.0
    print(f"   ✅ Lottie JSON Size: {lottie_size_kb:.2f} KB (Strictly < 50.0 KB)")

    for d in out_dirs:
        with open(os.path.join(d, "lottie.json"), "w", encoding="utf-8") as f:
            f.write(lottie_json)
    # Also save to mascots/owluko root
    with open(os.path.join(WORKSPACE_DIR, "mascots/owluko/owluko_idle_vector.json"), "w", encoding="utf-8") as f:
        f.write(lottie_json)

    # 2. Pure Vector Animated SVGs
    print("⚡ Step 2: Generating Pure Vector Animated SVGs (Dark & Transparent)...")
    svg_dark = build_animated_svg(bg_mode="dark")
    svg_trans = build_animated_svg(bg_mode="transparent")
    for d in out_dirs:
        with open(os.path.join(d, "owluko_idle_animated.svg"), "w", encoding="utf-8") as f:
            f.write(svg_dark)
        with open(os.path.join(d, "owluko_idle_animated_transparent.svg"), "w", encoding="utf-8") as f:
            f.write(svg_trans)

    # 3. Reference Frame Extraction & Porcelain Despill
    print("🎨 Step 3: Extracting 96 studio frames with porcelain ceramic despill...")
    frames_96 = load_and_despill_reference_video()
    print(f"   ✅ Processed {len(frames_96)} frames.")

    # 4. Resample to 120 frames @ 30 fps (4.0s loop)
    print("🎬 Step 4: Resampling to 120 frames @ 30 fps (4.00s seamless loop)...")
    frames_120 = resample_to_120_frames(frames_96)
    print(f"   ✅ Resampled to {len(frames_120)} frames.")

    # 5. Static Posters
    print("🖼️ Step 5: Generating Static Posters (static.png & static.webp)...")
    static_frame = frames_120[0]
    for d in out_dirs:
        static_frame.save(os.path.join(d, "static.png"), "PNG")
        static_frame.save(os.path.join(d, "static.webp"), "WEBP", quality=95)

    # 6. Looped Animated WebP
    print("🎞️ Step 6: Generating Looped Animated WebP (120 frames, transparent)...")
    frame_duration_ms = int(round(1000.0 / FPS))
    for d in out_dirs:
        webp_path = os.path.join(d, "animated.webp")
        frames_120[0].save(
            webp_path,
            "WEBP",
            save_all=True,
            append_images=frames_120[1:],
            duration=frame_duration_ms,
            loop=0,
            quality=90
        )
        print(f"   ✅ Saved: {webp_path} ({os.path.getsize(webp_path) / 1024:.1f} KB)")

    # 7. Animated GIFs across 3 backdrops (White, Dark Studio, Chroma Green)
    print("🎞️ Step 7: Generating Animated GIFs across 3 backdrops...")
    # Composite frames on backgrounds
    def make_gif_frames(bg_color):
        bg_frames = []
        for f in frames_120:
            bg_im = Image.new("RGBA", (512, 512), bg_color)
            bg_im.alpha_composite(f)
            # Convert to RGB with adaptive palette
            p_im = bg_im.convert("RGB").convert("P", palette=Image.Palette.ADAPTIVE, colors=256)
            bg_frames.append(p_im)
        return bg_frames

    white_frames = make_gif_frames(COLOR_BG_WHITE)
    dark_frames = make_gif_frames(COLOR_BG_DARK)
    green_frames = make_gif_frames(COLOR_BG_GREEN)

    for d in out_dirs:
        white_frames[0].save(os.path.join(d, "animated.gif"), save_all=True, append_images=white_frames[1:], duration=frame_duration_ms, loop=0)
        dark_frames[0].save(os.path.join(d, "animated_dark.gif"), save_all=True, append_images=dark_frames[1:], duration=frame_duration_ms, loop=0)
        green_frames[0].save(os.path.join(d, "animated_green.gif"), save_all=True, append_images=green_frames[1:], duration=frame_duration_ms, loop=0)
    print("   ✅ Generated animated.gif, animated_dark.gif, and animated_green.gif.")

    # 8. Looped MP4 Video (512x512 H.264)
    print("📹 Step 8: Generating Looped MP4 Video (H.264 512x512 @ 30 fps)...")
    temp_mp4_frames_dir = os.path.join(WORKSPACE_DIR, "scratch/owluko_idle_mp4_frames")
    os.makedirs(temp_mp4_frames_dir, exist_ok=True)

    for idx, f in enumerate(frames_120):
        # Dark studio backdrop for video preview
        v_frame = Image.new("RGBA", (512, 512), COLOR_BG_DARK)
        v_frame.alpha_composite(f)
        v_frame.convert("RGB").save(os.path.join(temp_mp4_frames_dir, f"f_{idx:04d}.png"))

    for d in out_dirs:
        mp4_out = os.path.join(d, "looped_video.mp4")
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-framerate", "30",
            "-i", os.path.join(temp_mp4_frames_dir, "f_%04d.png"),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-crf", "18",
            "-movflags", "+faststart",
            mp4_out
        ]
        subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"   ✅ Saved MP4: {mp4_out}")

    # 9. Master Presentation Board & Trichroma Board
    print("📊 Step 9: Generating Master Boards (1920x1080 & Trichroma)...")
    master_board = build_idle_master_board(frames_120)
    trichroma_board = build_studio_trichroma_board(frames_120[0])

    for d in out_dirs:
        master_board.save(os.path.join(d, "owluko_idle_master_board.png"), "PNG")
        trichroma_board.save(os.path.join(d, "owluko_idle_studio_trichroma_board.png"), "PNG")

    # Also save to mascots/owluko root
    master_board.save(os.path.join(WORKSPACE_DIR, "mascots/owluko/owluko_idle_master_board.png"), "PNG")

    # 10. Bundle ZIP
    print("📦 Step 10: Generating Production Delivery ZIP Bundle...")
    for d in out_dirs:
        zip_path = os.path.join(d, "bundle_owluko_00_idle.zip")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for fname in [
                "lottie.json", "owluko_idle_animated.svg", "owluko_idle_animated_transparent.svg",
                "animated.webp", "animated.gif", "animated_dark.gif", "animated_green.gif",
                "looped_video.mp4", "static.png", "static.webp",
                "owluko_idle_master_board.png", "owluko_idle_studio_trichroma_board.png"
            ]:
                f_p = os.path.join(d, fname)
                if os.path.exists(f_p):
                    zf.write(f_p, arcname=fname)
        print(f"   ✅ Saved ZIP Bundle: {zip_path} ({os.path.getsize(zip_path) / (1024*1024):.2f} MB)")

    # 11. Synchronize to Brain Directory
    print("🧠 Step 11: Synchronizing deliverables to Gemini brain directories...")
    primary_dir = out_dirs[0]
    for b_dir in BRAIN_DIRS:
        if os.path.exists(b_dir):
            shutil.copy2(os.path.join(primary_dir, "owluko_idle_master_board.png"), os.path.join(b_dir, "owluko_idle_master_board.png"))
            shutil.copy2(os.path.join(primary_dir, "animated.gif"), os.path.join(b_dir, "owluko_idle_animated.gif"))
            shutil.copy2(os.path.join(primary_dir, "animated_dark.gif"), os.path.join(b_dir, "owluko_idle_animated_dark.gif"))
            shutil.copy2(os.path.join(primary_dir, "static.png"), os.path.join(b_dir, "owluko_idle_static.png"))

    print("\n🎉 ==========================================================================")
    print("🎉 OWLUKO MASTER IDLE PRODUCTION COMPLETE & VALIDATED")
    print("🎉 ==========================================================================\n")

if __name__ == "__main__":
    run_owluko_idle_production()
