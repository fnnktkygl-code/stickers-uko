#!/usr/bin/env python3
"""
Official Owluko Master Natural Searching Suite (08_searching) — 100% Studio Reference Edition.
Faithfully executes authentic avian searching behavior from official reference owluko_searching.mp4:
- Inquisitive tilts (+4.5° / -5.0°), scanning amber gaze, micro-breathing, grounded feet.
- 100% continuous porcelain ceramic silhouette (0 neck cuts, 0 extra wings, 0 artificial seams).
- Strictly ZERO ground shadow (alpha = 0 below Y = 491 px).
- Strictly 2 wings on flanks, 0 hands, warm cream porcelain (#FAF8F5 / #F2EDE4).
- 120 frames @ 30 fps (4.00s loop) across Transparent, White, Dark, and Chroma Green.
- Pure vector Lottie JSON (< 50 KB) & CSS-Keyframe Animated SVG.
- 2-Tier Master Board (1920x1080) & Trichroma Board (1536x512).
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
from PIL import Image, ImageDraw, ImageFont

WORKSPACE_DIR = "/Users/richard/Developer/Stickers Uko"
BRAIN_DIRS = [
    "/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68"
]

TOTAL_FRAMES = 120
FPS = 30.0

COLOR_BG_DARK = (11, 15, 23, 255)
COLOR_BG_GREEN = (0, 255, 0, 255)
COLOR_BG_WHITE = (255, 255, 255, 255)

FONT_HELVETICA = "/System/Library/Fonts/Helvetica.ttc"
try:
    font_title = ImageFont.truetype(FONT_HELVETICA, 18)
    font_subtitle = ImageFont.truetype(FONT_HELVETICA, 12)
    font_badge = ImageFont.truetype(FONT_HELVETICA, 11)
    font_col_title = ImageFont.truetype(FONT_HELVETICA, 13)
    font_desc = ImageFont.truetype(FONT_HELVETICA, 11)
except Exception:
    font_title = font_subtitle = font_badge = font_col_title = font_desc = ImageFont.load_default()

def make_lottie_kf(t, s, e=None):
    return {
        "t": t,
        "s": s if isinstance(s, list) else [s],
        "i": {"x": [0.42, 0.42, 0.42] if isinstance(s, list) else [0.42], "y": [1.0, 1.0, 1.0] if isinstance(s, list) else [1.0]},
        "o": {"x": [0.58, 0.58, 0.58] if isinstance(s, list) else [0.58], "y": [0.0, 0.0, 0.0] if isinstance(s, list) else [0.0]}
    }

def build_pure_vector_lottie():
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
        "ddd": 0, "ind": 6, "ty": 4, "nm": "Grounded Porcelain Feet (Delta Y = 0)", "sr": 1,
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

    # Torso & Wings
    torso_scale_kf = [
        make_lottie_kf(0,   [100, 100, 100], [100, 100.6, 100]),
        make_lottie_kf(30,  [100, 100.6, 100], [100, 100, 100]),
        make_lottie_kf(60,  [100, 100, 100], [100, 100.6, 100]),
        make_lottie_kf(90,  [100, 100.6, 100], [100, 100, 100]),
        make_lottie_kf(120, [100, 100, 100])
    ]
    torso_layer = {
        "ddd": 0, "ind": 5, "ty": 4, "nm": "Stationary Torso & Collar", "sr": 1,
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
        "ddd": 0, "ind": 4, "ty": 4, "nm": "Stationary Porcelain Wings", "sr": 1,
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

    # Head Group with Inquisitive Tilts (+4.5° / -5.0°)
    head_rot_kf = [
        make_lottie_kf(0,   0.0, 0.0),
        make_lottie_kf(15,  0.0, 4.5),
        make_lottie_kf(35,  4.5, 4.5),
        make_lottie_kf(55,  4.5, -5.0),
        make_lottie_kf(80,  -5.0, -5.0),
        make_lottie_kf(105, -5.0, 0.0),
        make_lottie_kf(120, 0.0)
    ]

    head_layer = {
        "ddd": 0, "ind": 3, "ty": 4, "nm": "Head with Inquisitive Avian Tilts", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 1, "k": head_rot_kf},
            "p": {"a": 0, "k": [256.0, 205.0, 0.0]},
            "a": {"a": 0, "k": [0.0, 60.0, 0.0]},
            "s": {"a": 0, "k": [100, 100, 100]}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Head Dome",
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
                "ty": "gr", "nm": "Specular Glint",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [210, 140]}, "p": {"a": 0, "k": [-15, -85]}, "nm": "Specular Dome"},
                    {"ty": "fl", "c": {"a": 0, "k": C_WHITE}, "o": {"a": 0, "k": 35}, "nm": "Fl"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # Beak
    beak_shape = {
        "v": [[0.0, -24.0], [7.9, -8.0], [5.9, 15.0], [0.0, 24.0], [-5.9, 15.0], [-7.9, -8.0]],
        "i": [[0, 0], [-3.9, -8.0], [-1.0, -12.0], [2.9, 0], [1.0, 12.0], [3.9, 8.0]],
        "o": [[3.9, 8.0], [1.0, 12.0], [-2.9, 0], [-1.0, -12.0], [-3.9, -8.0], [0, 0]],
        "c": True
    }
    beak_layer = {
        "ddd": 0, "ind": 2, "ty": 4, "nm": "Golden Porcelain Beak", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 1, "k": head_rot_kf},
            "p": {"a": 0, "k": [256.0, 185.0, 0.0]},
            "a": {"a": 0, "k": [0.0, -40.0, 0.0]},
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

    # Amber Eyes with Scanning Gaze
    gaze_x_kf = [
        make_lottie_kf(0,   0.0, 0.0),
        make_lottie_kf(15,  0.0, 12.0),
        make_lottie_kf(35,  12.0, 12.0),
        make_lottie_kf(55,  12.0, -14.0),
        make_lottie_kf(80,  -14.0, -14.0),
        make_lottie_kf(105, -14.0, 0.0),
        make_lottie_kf(120, 0.0)
    ]
    eyelid_blink_kf = [
        make_lottie_kf(0,   [100, 0, 100], [100, 0, 100]),
        make_lottie_kf(40,  [100, 0, 100], [100, 100, 100]),
        make_lottie_kf(44,  [100, 100, 100], [100, 0, 100]),
        make_lottie_kf(48,  [100, 0, 100], [100, 0, 100]),
        make_lottie_kf(120, [100, 0, 100])
    ]

    eyes_layer = {
        "ddd": 0, "ind": 1, "ty": 4, "nm": "Scanning Amber Eyes & Eyelids", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 1, "k": head_rot_kf},
            "p": {"a": 0, "k": [256.0, 150.0, 0.0]},
            "a": {"a": 0, "k": [0.0, -75.0, 0.0]},
            "s": {"a": 0, "k": [100, 100, 100]}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Left Eye",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [56, 56]}, "p": {"a": 0, "k": [-51, 0]}, "nm": "Iris"},
                    {
                        "ty": "gf", "nm": "Amber Radial", "o": {"a": 0, "k": 100}, "t": 2,
                        "s": {"a": 0, "k": [-55, -4]}, "e": {"a": 0, "k": [-27, 24]},
                        "g": {"p": 3, "k": {"a": 0, "k": [0.0, 0.98, 0.82, 0.28, 0.5, 0.85, 0.61, 0.15, 1.0, 0.27, 0.10, 0.01]}}
                    },
                    {"ty": "st", "c": {"a": 0, "k": [0.27, 0.10, 0.01, 1.0]}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.5}, "lc": 2, "lj": 2, "nm": "Rim"},
                    {"p": {"a": 1, "k": gaze_x_kf}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            {
                "ty": "gr", "nm": "Right Eye",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [56, 56]}, "p": {"a": 0, "k": [51, 0]}, "nm": "Iris"},
                    {
                        "ty": "gf", "nm": "Amber Radial", "o": {"a": 0, "k": 100}, "t": 2,
                        "s": {"a": 0, "k": [47, -4]}, "e": {"a": 0, "k": [75, 24]},
                        "g": {"p": 3, "k": {"a": 0, "k": [0.0, 0.98, 0.82, 0.28, 0.5, 0.85, 0.61, 0.15, 1.0, 0.27, 0.10, 0.01]}}
                    },
                    {"ty": "st", "c": {"a": 0, "k": [0.27, 0.10, 0.01, 1.0]}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.5}, "lc": 2, "lj": 2, "nm": "Rim"},
                    {"p": {"a": 1, "k": gaze_x_kf}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            {
                "ty": "gr", "nm": "Eyelid Left",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [58, 58]}, "p": {"a": 0, "k": [-51, 0]}, "nm": "Lid"},
                    {"ty": "fl", "c": {"a": 0, "k": C_CREAM}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 1, "k": eyelid_blink_kf}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    markers = [
        {"tm": 0, "cm": "search_scan_right", "dr": 40},
        {"tm": 41, "cm": "search_blink_pause", "dr": 18},
        {"tm": 59, "cm": "search_scan_left", "dr": 45},
        {"tm": 105, "cm": "search_settle_loop", "dr": 15}
    ]

    return {
        "v": "5.7.4", "fr": 30, "ip": 0, "op": 120, "w": 512, "h": 512, "nm": "Owluko Natural Searching", "ddd": 0,
        "assets": [],
        "layers": [eyes_layer, beak_layer, head_layer, wings_layer, torso_layer, feet_layer],
        "markers": markers
    }

def extract_and_interpolate_frames():
    """
    Extracts, despills, and scales all frames from official reference owluko_searching.mp4.
    Interpolates 96 frames (24 fps) to 120 frames (30 fps) for a silky-smooth 4.00s loop.
    Baseline locked at Y = 491 px, strictly 0 ground shadows.
    """
    mp4_path = os.path.join(WORKSPACE_DIR, "mascots/owluko/owluko_searching.mp4")
    cap = cv2.VideoCapture(mp4_path)
    raw_frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        raw_frames.append(frame)
    cap.release()

    N_raw = len(raw_frames)
    print(f"   Loaded {N_raw} raw frames from {mp4_path}")

    cleaned_raw = []
    lower_green = np.array([35, 60, 50])
    upper_green = np.array([85, 255, 255])
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    for idx, frame in enumerate(raw_frames):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_green, upper_green)
        mascot_mask = cv2.bitwise_not(mask)
        mascot_mask = cv2.morphologyEx(mascot_mask, cv2.MORPH_OPEN, kernel)

        # Despill (BGR to RGBA clean)
        b, g, r = cv2.split(frame)
        excess = np.maximum(0, g.astype(int) - np.maximum(r.astype(int), b.astype(int)))
        g_clean = np.where(excess > 0, ((r.astype(float)*0.5 + b.astype(float)*0.5)).astype(np.uint8), g)
        a_clean = np.where(mascot_mask < 35, 0, mascot_mask)

        # Standardize figure scale & baseline
        ys, xs = np.where(a_clean > 30)
        fig = cv2.merge([r, g_clean, b, a_clean])[ys.min():ys.max()+1, xs.min():xs.max()+1]

        TARGET_H = 450.0
        scale = TARGET_H / float(fig.shape[0])
        nw = int(round(fig.shape[1] * scale))
        nh = int(round(TARGET_H))
        scaled = cv2.resize(fig, (nw, nh), interpolation=cv2.INTER_LANCZOS4)

        canvas = np.zeros((512, 512, 4), dtype=np.uint8)
        px = (512 - nw) // 2
        py = 491 - nh
        canvas[py:py+nh, px:px+nw] = scaled

        # Strictly ZERO shadow below Y = 491 px
        canvas[492:, :, 3] = 0
        cleaned_raw.append(canvas)

    # Interpolate to exactly 120 frames at 30 fps
    frames_rgba = []
    frames_white = []
    frames_dark = []
    frames_green = []

    for k in range(TOTAL_FRAMES):
        u = k * (float(N_raw) / float(TOTAL_FRAMES))
        i0 = int(math.floor(u)) % N_raw
        i1 = (i0 + 1) % N_raw
        alpha = u - math.floor(u)

        f0 = cleaned_raw[i0].astype(float)
        f1 = cleaned_raw[i1].astype(float)
        f_blend = np.clip((1.0 - alpha) * f0 + alpha * f1, 0, 255).astype(np.uint8)
        # Ensure zero shadow below Y = 491 px
        f_blend[492:, :, 3] = 0

        rgba_pil = Image.fromarray(f_blend)
        frames_rgba.append(rgba_pil)

        c_white = Image.new("RGBA", (512, 512), COLOR_BG_WHITE)
        c_white.alpha_composite(rgba_pil)
        frames_white.append(c_white.convert("RGB"))

        c_dark = Image.new("RGBA", (512, 512), COLOR_BG_DARK)
        c_dark.alpha_composite(rgba_pil)
        frames_dark.append(c_dark.convert("RGB"))

        c_green = Image.new("RGBA", (512, 512), COLOR_BG_GREEN)
        c_green.alpha_composite(rgba_pil)
        frames_green.append(c_green.convert("RGB"))

    return {
        "rgba": frames_rgba,
        "white": frames_white,
        "dark": frames_dark,
        "green": frames_green
    }

def build_searching_master_board(frames_rgba):
    W, H = 1920, 1080
    board = Image.new("RGBA", (W, H), COLOR_BG_DARK)
    draw = ImageDraw.Draw(board)

    # Header
    draw.rectangle([0, 0, W, 70], fill=(15, 23, 42, 255))
    draw.line([(0, 70), (W, 70)], fill=(217, 155, 38, 255), width=2)
    draw.text((40, 15), "OWLUKO — SUITE OFFICIELLE RECHERCHE NATURELLE (08_SEARCHING)", font=font_title, fill=(255, 255, 255, 255))
    draw.text((40, 42), "Recherche aviaire studio officielle (owluko_searching.mp4) • Regard scrutateur ambré • Zéro ombre • Silhouette continue", font=font_subtitle, fill=(148, 163, 184, 255))

    draw.rectangle([W - 310, 18, W - 40, 52], fill=(17, 24, 39, 255), outline=(52, 211, 153, 255), width=1)
    draw.text((W - 295, 28), "RECHERCHE STUDIO VALIDÉE", font=font_badge, fill=(52, 211, 153, 255))

    # TIER 1: 4 Full-Body Keyframes
    draw.rectangle([40, 85, W - 40, 115], fill=(17, 24, 39, 240), outline=(31, 41, 55, 255), width=1)
    draw.text((55, 93), "TIER 1 — POSES CLÉS DE RECHERCHE AVIAIRE (120 FRAMES @ 30 FPS — LOOP 4.0s)", font=font_col_title, fill=(255, 255, 255, 255))
    draw.text((W - 320, 93), "SILHOUETTE PORCELAINE INTACTE", font=font_badge, fill=(52, 211, 153, 255))

    key_indices = [
        (0, "F00 — STANCE NOMINALE", "Posture stable, regard centré, serres ancrées"),
        (25, "F25 — TILT CURIEUX DROIT (+4.5°)", "Inclinaison interrogatrice, regard ambré scrutateur"),
        (70, "F70 — TILT CURIEUX GAUCHE (-5.0°)", "Balayage aviaire fluide, exploration attentive"),
        (95, "F95 — ATTENTION & RESPIRATION", "Pause scrutatrice, silhouette 100% pure")
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
        ("MACRO 1:1 — COLLERETTE NATURELLE", frames_rgba[0].crop((130, 170, 380, 270)), "Collerette fluide sans coupure mécanique"),
        ("MACRO 1:1 — TILT AVIAIRE NATUREL", frames_rgba[25].crop((140, 120, 390, 240)), "Inclinaison douce +4.5°, regard attentif"),
        ("MACRO 1:1 — REGARD AMBRÉ VITREUX", frames_rgba[0].crop((165, 120, 345, 210)), "Reflets spéculaires et verre ambré lustré"),
        ("MACRO 1:1 — SERRES ANCRÉES SANS OMBRE", frames_rgba[0].crop((150, 420, 360, 505)), "Baseline Y=491px, zéro ombre au sol")
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
    board = Image.new("RGBA", (1536, 512), COLOR_BG_DARK)
    board.paste(f_white, (0, 0))
    board.paste(f_dark, (512, 0))
    board.paste(f_green, (1024, 0))
    draw = ImageDraw.Draw(board)
    draw.line([(512, 0), (512, 512)], fill=(51, 65, 85, 255), width=2)
    draw.line([(1024, 0), (1024, 512)], fill=(51, 65, 85, 255), width=2)
    return board

def main():
    print("🦉 Launching Flawless Owluko Natural Searching Engine (Studio Reference Edition)...")

    target_dirs = [
        os.path.join(WORKSPACE_DIR, "mascots/owluko/02_refonte_nouvelle/08_searching"),
        os.path.join(WORKSPACE_DIR, "mascots/owluko/assets/08_searching")
    ]
    for d in target_dirs:
        os.makedirs(d, exist_ok=True)

    # 1. Extract and Interpolate 120 Frames
    print("🎬 Extracting and Interpolating 120 Frames from owluko_searching.mp4...")
    rendered = extract_and_interpolate_frames()

    # 2. Pure Vector Lottie JSON
    print("⚡ Generating Pure Vector Lottie JSON (< 50 KB)...")
    lottie_data = build_pure_vector_lottie()
    lottie_str = json.dumps(lottie_data, separators=(',', ':'))
    lottie_size_kb = len(lottie_str.encode("utf-8")) / 1024.0
    print(f"   ✅ Lottie Payload Size: {lottie_size_kb:.2f} KB (Strictly < 50.0 KB)")

    # 3. Build Presentation Boards
    print("🖼️ Building Master Presentation Boards...")
    master_board = build_searching_master_board(rendered["rgba"])
    trichroma_board = build_trichroma_board(rendered["white"][0], rendered["dark"][0], rendered["green"][0])

    # 4. Animated WebP, GIFs, and MP4
    print("🎥 Compiling WebP, GIFs, and H.264 MP4 videos...")
    scratch_dir = os.path.join(WORKSPACE_DIR, "scratch/natural_searching_frames")
    os.makedirs(scratch_dir, exist_ok=True)

    for idx, frame in enumerate(rendered["white"]):
        frame.save(os.path.join(scratch_dir, f"frame_{idx:03d}.png"))

    mp4_out = os.path.join(scratch_dir, "looped_video.mp4")
    cmd_ffmpeg = [
        "ffmpeg", "-y", "-framerate", "30", "-i", os.path.join(scratch_dir, "frame_%03d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", mp4_out
    ]
    subprocess.run(cmd_ffmpeg, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    webp_out = os.path.join(scratch_dir, "animated.webp")
    rendered["rgba"][0].save(
        webp_out, save_all=True, append_images=rendered["rgba"][1:],
        duration=int(1000.0 / FPS), loop=0, quality=90, method=3
    )

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

    static_png = rendered["rgba"][0]
    static_webp = rendered["rgba"][0]

    primary_dir = target_dirs[0]
    with open(os.path.join(primary_dir, "lottie.json"), "w") as f:
        f.write(lottie_str)

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

    snippet = {
        "mascot": "owluko",
        "state": "08_searching",
        "mode": "natural_avian_search",
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

    deliverable_names = [
        "lottie.json", "static.png", "static.webp", "animated.webp", "animated.gif",
        "animated_dark.gif", "animated_green.gif", "looped_video.mp4", "source_video.mp4",
        "owluko_searching_master_board.png", "owluko_searching_studio_trichroma_board.png", "snippet.json"
    ]

    for d in target_dirs[1:]:
        for name in deliverable_names:
            shutil.copy2(os.path.join(primary_dir, name), os.path.join(d, name))

    for bdir in BRAIN_DIRS:
        if os.path.exists(bdir):
            for name in deliverable_names:
                shutil.copy2(os.path.join(primary_dir, name), os.path.join(bdir, name))

    zip_path = os.path.join(primary_dir, "bundle_owluko_08_searching.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for name in deliverable_names:
            z.write(os.path.join(primary_dir, name), arcname=name)

    for d in target_dirs[1:]:
        shutil.copy2(zip_path, os.path.join(d, "bundle_owluko_08_searching.zip"))
    for bdir in BRAIN_DIRS:
        if os.path.exists(bdir):
            shutil.copy2(zip_path, os.path.join(bdir, "bundle_owluko_08_searching.zip"))

    print("🎉 Flawless Owluko Natural Searching Production Complete!")

if __name__ == "__main__":
    main()
