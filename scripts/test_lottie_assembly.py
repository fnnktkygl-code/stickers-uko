#!/usr/bin/env python3
import json
import os
import sys

from scripts.test_animated_svg_and_lottie import (
    body_pts, tail_pts, flank_l_pts, flank_r_pts, white_coat_pts,
    points_to_lottie_shape, make_lottie_kf
)

def build_pure_vector_lottie():
    # Kinematics
    torso_pos_kf = [
        make_lottie_kf(0, [256, 360, 0], [256, 362.5, 0]),
        make_lottie_kf(30, [256, 362.5, 0], [256, 360, 0]),
        make_lottie_kf(60, [256, 360, 0], [256, 357.5, 0]),
        make_lottie_kf(90, [256, 357.5, 0], [256, 360, 0]),
        make_lottie_kf(120, [256, 360, 0])
    ]
    torso_scale_kf = [
        make_lottie_kf(0, [100, 100, 100], [100.8, 99.2, 100]),
        make_lottie_kf(30, [100.8, 99.2, 100], [100, 100, 100]),
        make_lottie_kf(60, [100, 100, 100], [99.2, 100.8, 100]),
        make_lottie_kf(90, [99.2, 100.8, 100], [100, 100, 100]),
        make_lottie_kf(120, [100, 100, 100])
    ]
    tail_rot_kf = [
        make_lottie_kf(0, -3.5, 0.0),
        make_lottie_kf(30, 0.0, 3.5),
        make_lottie_kf(60, 3.5, 0.0),
        make_lottie_kf(90, 0.0, -3.5),
        make_lottie_kf(120, -3.5)
    ]
    eye_blink_kf = [
        make_lottie_kf(0, [100, 100, 100]),
        make_lottie_kf(20, [100, 100, 100], [100, 8, 100]),
        make_lottie_kf(24, [100, 8, 100], [100, 100, 100]),
        make_lottie_kf(28, [100, 100, 100]),
        make_lottie_kf(80, [100, 100, 100], [100, 8, 100]),
        make_lottie_kf(84, [100, 8, 100], [100, 100, 100]),
        make_lottie_kf(88, [100, 100, 100]),
        make_lottie_kf(120, [100, 100, 100])
    ]

    # Colors
    C_STROKE = [0.57, 0.25, 0.04, 1.0]
    C_WHITE_STROKE = [0.78, 0.74, 0.68, 1.0]

    # Layer 7: Grounded Paws (Delta Y = 0)
    paws_layer = {
        "ddd": 0, "ind": 7, "ty": 4, "nm": "Grounded Porcelain Paws", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0},
            "p": {"a": 0, "k": [256.0, 465.0, 0.0]},
            "a": {"a": 0, "k": [0.0, 0.0, 0.0]},
            "s": {"a": 0, "k": [100.0, 100.0, 100.0]}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Paws Base",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [48, 28]}, "p": {"a": 0, "k": [-38, 12]}, "nm": "LeftPaw"},
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [48, 28]}, "p": {"a": 0, "k": [38, 12]}, "nm": "RightPaw"},
                    {"ty": "fl", "c": {"a": 0, "k": [0.98, 0.97, 0.95, 1.0]}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"ty": "st", "c": {"a": 0, "k": C_WHITE_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # Layer 6: Tail
    tail_layer = {
        "ddd": 0, "ind": 6, "ty": 4, "nm": "Harmonic Cat Tail", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 1, "k": tail_rot_kf},
            "p": {"a": 0, "k": [185.0, 445.0, 0.0]},
            "a": {"a": 0, "k": [185.0, 445.0, 0.0]},
            "s": {"a": 0, "k": [100.0, 100.0, 100.0]}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Tail Shell",
                "it": [
                    points_to_lottie_shape(tail_pts, 0.0, 0.0),
                    {
                        "ty": "gf", "nm": "Tail Gradient", "o": {"a": 0, "k": 100}, "t": 1,
                        "s": {"a": 0, "k": [130, 420]}, "e": {"a": 0, "k": [180, 480]},
                        "g": {"p": 3, "k": {"a": 0, "k": [0.0, 0.92, 0.53, 0.21, 0.5, 0.80, 0.41, 0.11, 1.0, 0.65, 0.28, 0.03]}}
                    },
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.0}, "lc": 2, "lj": 2, "nm": "St"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # Layer 5: Body Base (Ginger Shell)
    body_layer = {
        "ddd": 0, "ind": 5, "ty": 4, "nm": "Ginger Body Shell", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0},
            "p": {"a": 1, "k": torso_pos_kf},
            "a": {"a": 0, "k": [256.0, 360.0, 0.0]},
            "s": {"a": 1, "k": torso_scale_kf}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Master Silhouette",
                "it": [
                    points_to_lottie_shape(body_pts, 0.0, 0.0),
                    {
                        "ty": "gf", "nm": "Ginger Coat Gradient", "o": {"a": 0, "k": 100}, "t": 1,
                        "s": {"a": 0, "k": [200, 100]}, "e": {"a": 0, "k": [320, 450]},
                        "g": {"p": 4, "k": {"a": 0, "k": [0.0, 0.97, 0.68, 0.39, 0.35, 0.92, 0.53, 0.21, 0.7, 0.82, 0.43, 0.13, 1.0, 0.70, 0.31, 0.06]}}
                    },
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.0}, "lc": 2, "lj": 2, "nm": "St"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # Layer 4: White Fur Coat (Blaze, Chubby Cheeks, Chest, Front Legs)
    white_layer = {
        "ddd": 0, "ind": 4, "ty": 4, "nm": "White Porcelain Coat", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0},
            "p": {"a": 1, "k": torso_pos_kf},
            "a": {"a": 0, "k": [256.0, 360.0, 0.0]},
            "s": {"a": 1, "k": torso_scale_kf}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "White Marking",
                "it": [
                    points_to_lottie_shape(white_coat_pts, 0.0, 0.0),
                    {
                        "ty": "gf", "nm": "Porcelain Shading", "o": {"a": 0, "k": 100}, "t": 2,
                        "s": {"a": 0, "k": [256, 220]}, "e": {"a": 0, "k": [380, 220]},
                        "g": {"p": 4, "k": {"a": 0, "k": [0.0, 1.0, 1.0, 1.0, 0.4, 0.98, 0.97, 0.95, 0.75, 0.93, 0.90, 0.84, 1.0, 0.84, 0.79, 0.71]}}
                    },
                    {"ty": "st", "c": {"a": 0, "k": C_WHITE_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 0.8}, "lc": 2, "lj": 2, "nm": "St"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # Layer 3: Glassy Amber Eyes (Orb iris, black pupil, specular highlights, organic blink)
    eyes_layer = {
        "ddd": 0, "ind": 3, "ty": 4, "nm": "Glassy Amber Eyes", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0},
            "p": {"a": 1, "k": torso_pos_kf},
            "a": {"a": 0, "k": [256.0, 360.0, 0.0]},
            "s": {"a": 0, "k": [100.0, 100.0, 100.0]}
        },
        "ao": 0,
        "shapes": [
            # Left Eye Group
            {
                "ty": "gr", "nm": "Left Eye",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [46, 50]}, "p": {"a": 0, "k": [216, 172]}, "nm": "Eyeliner"},
                    {"ty": "fl", "c": {"a": 0, "k": [0.11, 0.06, 0.02, 1.0]}, "o": {"a": 0, "k": 100}, "nm": "FlEyeliner"},
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [43, 47]}, "p": {"a": 0, "k": [216, 172]}, "nm": "Iris"},
                    {
                        "ty": "gf", "nm": "Amber Gradient", "o": {"a": 0, "k": 100}, "t": 2,
                        "s": {"a": 0, "k": [220, 180]}, "e": {"a": 0, "k": [235, 180]},
                        "g": {"p": 4, "k": {"a": 0, "k": [0.0, 1.0, 0.94, 0.40, 0.35, 0.90, 0.71, 0.17, 0.7, 0.61, 0.45, 0.08, 1.0, 0.23, 0.14, 0.01]}}
                    },
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [30, 34]}, "p": {"a": 0, "k": [217, 172]}, "nm": "Pupil"},
                    {"ty": "fl", "c": {"a": 0, "k": [0.05, 0.03, 0.01, 1.0]}, "o": {"a": 0, "k": 100}, "nm": "FlPupil"},
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [15, 15]}, "p": {"a": 0, "k": [218, 165]}, "nm": "MainSpecular"},
                    {"ty": "fl", "c": {"a": 0, "k": [1.0, 1.0, 1.0, 1.0]}, "o": {"a": 0, "k": 100}, "nm": "FlSpec"},
                    {"ty": "tr", "p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [216, 172]}, "s": {"a": 1, "k": eye_blink_kf}, "r": {"a": 0, "k": -3}, "o": {"a": 0, "k": 100}}
                ]
            },
            # Right Eye Group
            {
                "ty": "gr", "nm": "Right Eye",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [46, 50]}, "p": {"a": 0, "k": [296, 172]}, "nm": "Eyeliner"},
                    {"ty": "fl", "c": {"a": 0, "k": [0.11, 0.06, 0.02, 1.0]}, "o": {"a": 0, "k": 100}, "nm": "FlEyeliner"},
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [43, 47]}, "p": {"a": 0, "k": [296, 172]}, "nm": "Iris"},
                    {
                        "ty": "gf", "nm": "Amber Gradient", "o": {"a": 0, "k": 100}, "t": 2,
                        "s": {"a": 0, "k": [292, 180]}, "e": {"a": 0, "k": [307, 180]},
                        "g": {"p": 4, "k": {"a": 0, "k": [0.0, 1.0, 0.94, 0.40, 0.35, 0.90, 0.71, 0.17, 0.7, 0.61, 0.45, 0.08, 1.0, 0.23, 0.14, 0.01]}}
                    },
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [30, 34]}, "p": {"a": 0, "k": [295, 172]}, "nm": "Pupil"},
                    {"ty": "fl", "c": {"a": 0, "k": [0.05, 0.03, 0.01, 1.0]}, "o": {"a": 0, "k": 100}, "nm": "FlPupil"},
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [15, 15]}, "p": {"a": 0, "k": [298, 165]}, "nm": "MainSpecular"},
                    {"ty": "fl", "c": {"a": 0, "k": [1.0, 1.0, 1.0, 1.0]}, "o": {"a": 0, "k": 100}, "nm": "FlSpec"},
                    {"ty": "tr", "p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [296, 172]}, "s": {"a": 1, "k": eye_blink_kf}, "r": {"a": 0, "k": 3}, "o": {"a": 0, "k": 100}}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # Layer 2: Inner Ears & Forehead Tabby Stripes
    ears_layer = {
        "ddd": 0, "ind": 2, "ty": 4, "nm": "Inner Ears & Tabby Stripes", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0},
            "p": {"a": 1, "k": torso_pos_kf},
            "a": {"a": 0, "k": [256.0, 360.0, 0.0]},
            "s": {"a": 1, "k": torso_scale_kf}
        },
        "ao": 0,
        "shapes": [
            # Left Inner Ear
            {
                "ty": "gr", "nm": "Left Ear Cavity",
                "it": [
                    {"ty": "sh", "ks": {"a": 0, "k": {"c": True, "v": [[176, 72], [215, 138], [172, 136]], "i": [[0,0], [10,-20], [-5,15]], "o": [[15,25], [-10,5], [0,-30]]}}, "nm": "CavityL"},
                    {"ty": "fl", "c": {"a": 0, "k": [0.99, 0.79, 0.74, 1.0]}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"ty": "st", "c": {"a": 0, "k": [0.75, 0.33, 0.25, 1.0]}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 0.8}, "nm": "St"}
                ]
            },
            # Right Inner Ear
            {
                "ty": "gr", "nm": "Right Ear Cavity",
                "it": [
                    {"ty": "sh", "ks": {"a": 0, "k": {"c": True, "v": [[336, 72], [340, 136], [297, 138]], "i": [[0,0], [5,-30], [-10,-5]], "o": [[-15,25], [0,15], [10,-20]]}}, "nm": "CavityR"},
                    {"ty": "fl", "c": {"a": 0, "k": [0.99, 0.79, 0.74, 1.0]}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"ty": "st", "c": {"a": 0, "k": [0.75, 0.33, 0.25, 1.0]}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 0.8}, "nm": "St"}
                ]
            },
            # Tabby Stripes
            {
                "ty": "gr", "nm": "Tabby Stripes",
                "it": [
                    {"ty": "sh", "ks": {"a": 0, "k": {"c": False, "v": [[256, 75], [256, 130]], "i": [[0,0],[0,0]], "o": [[0,0],[0,0]]}}, "nm": "StripeCenter"},
                    {"ty": "sh", "ks": {"a": 0, "k": {"c": False, "v": [[235, 84], [244, 126]], "i": [[0,0],[0,0]], "o": [[0,0],[0,0]]}}, "nm": "StripeLeft"},
                    {"ty": "sh", "ks": {"a": 0, "k": {"c": False, "v": [[277, 84], [268, 126]], "i": [[0,0],[0,0]], "o": [[0,0],[0,0]]}}, "nm": "StripeRight"},
                    {"ty": "st", "c": {"a": 0, "k": [0.72, 0.32, 0.06, 0.85]}, "o": {"a": 0, "k": 85}, "w": {"a": 0, "k": 6.5}, "lc": 2, "lj": 2, "nm": "St"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # Layer 1: Nose, Muzzle & Whiskers
    face_details_layer = {
        "ddd": 0, "ind": 1, "ty": 4, "nm": "Nose Muzzle & Whiskers", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0},
            "p": {"a": 1, "k": torso_pos_kf},
            "a": {"a": 0, "k": [256.0, 360.0, 0.0]},
            "s": {"a": 1, "k": torso_scale_kf}
        },
        "ao": 0,
        "shapes": [
            # Nose
            {
                "ty": "gr", "nm": "Nose",
                "it": [
                    {"ty": "sh", "ks": {"a": 0, "k": {"c": True, "v": [[250, 195], [262, 195], [256, 203]], "i": [[0,0],[0,0],[0,0]], "o": [[0,0],[0,0],[0,0]]}}, "nm": "NosePath"},
                    {"ty": "fl", "c": {"a": 0, "k": [0.97, 0.62, 0.54, 1.0]}, "o": {"a": 0, "k": 100}, "nm": "FlNose"},
                    {"ty": "st", "c": {"a": 0, "k": [0.87, 0.44, 0.36, 1.0]}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 0.8}, "nm": "StNose"}
                ]
            },
            # Mouth line ω
            {
                "ty": "gr", "nm": "Mouth",
                "it": [
                    {"ty": "sh", "ks": {"a": 0, "k": {"c": False, "v": [[256, 203], [256, 208]], "i": [[0,0],[0,0]], "o": [[0,0],[0,0]]}}, "nm": "Stem"},
                    {"ty": "sh", "ks": {"a": 0, "k": {"c": False, "v": [[246, 211], [256, 208], [266, 211]], "i": [[-2,3], [0,0], [2,3]], "o": [[2,3], [0,0], [-2,3]]}}, "nm": "Lips"},
                    {"ty": "st", "c": {"a": 0, "k": [0.56, 0.49, 0.44, 1.0]}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.3}, "lc": 2, "lj": 2, "nm": "StMouth"}
                ]
            },
            # Whiskers
            {
                "ty": "gr", "nm": "Whiskers",
                "it": [
                    {"ty": "sh", "ks": {"a": 0, "k": {"c": False, "v": [[238, 205], [176, 216]], "i": [[0,0],[15,-5]], "o": [[-15,5],[0,0]]}}, "nm": "WL1"},
                    {"ty": "sh", "ks": {"a": 0, "k": {"c": False, "v": [[236, 210], [180, 230]], "i": [[0,0],[15,-5]], "o": [[-15,5],[0,0]]}}, "nm": "WL2"},
                    {"ty": "sh", "ks": {"a": 0, "k": {"c": False, "v": [[237, 216], [188, 245]], "i": [[0,0],[15,-5]], "o": [[-15,5],[0,0]]}}, "nm": "WL3"},
                    {"ty": "sh", "ks": {"a": 0, "k": {"c": False, "v": [[274, 205], [336, 216]], "i": [[0,0],[-15,-5]], "o": [[15,5],[0,0]]}}, "nm": "WR1"},
                    {"ty": "sh", "ks": {"a": 0, "k": {"c": False, "v": [[276, 210], [332, 230]], "i": [[0,0],[-15,-5]], "o": [[15,5],[0,0]]}}, "nm": "WR2"},
                    {"ty": "sh", "ks": {"a": 0, "k": {"c": False, "v": [[275, 216], [324, 245]], "i": [[0,0],[-15,-5]], "o": [[15,5],[0,0]]}}, "nm": "WR3"},
                    {"ty": "st", "c": {"a": 0, "k": [1.0, 1.0, 1.0, 0.9]}, "o": {"a": 0, "k": 90}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "StWhiskers"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    lottie_data = {
        "v": "5.7.4", "fr": 30, "ip": 0, "op": 120, "w": 512, "h": 512,
        "nm": "Meoweko Flawless Idle (Pure Vector, Bicolor Ginger/Cream Porcelain)",
        "layers": [
            face_details_layer, ears_layer, eyes_layer, white_layer,
            body_layer, tail_layer, paws_layer
        ],
        "markers": [
            {"tm": 0, "cm": "idle_start", "dr": 0},
            {"tm": 20, "cm": "blink_1", "dr": 12},
            {"tm": 48, "cm": "ear_twitch", "dr": 8},
            {"tm": 80, "cm": "blink_2", "dr": 12}
        ]
    }
    return lottie_data

data = build_pure_vector_lottie()
s = json.dumps(data, separators=(',', ':'))
size_kb = len(s.encode('utf-8')) / 1024.0
print(f"✅ Complete Lottie JSON assembled! Size: {size_kb:.2f} KB (Target < 50.0 KB)")
assert size_kb < 50.0, f"Size {size_kb} >= 50.0 KB"

with open("scratch/meoweko_pure_vector_lottie.json", "w") as f:
    f.write(s)
print("✅ Saved scratch/meoweko_pure_vector_lottie.json")
