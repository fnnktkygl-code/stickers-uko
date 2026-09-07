import re

def get_new_lottie_code():
    return '''def build_pure_vector_lottie():
    """
    Constructs 100% pure vector Lottie JSON (< 50 KB) for Meoweko Idle:
    - Grounded porcelain front paws (dy = 0.0 px, Delta Y = 0)
    - Feline tail harmonic swish (Ginger/Apricot)
    - Porcelain torso capsule with organic breathing (squash & stretch)
    - Ginger/Apricot flanks, shoulders, and skull dome
    - Cream-white blaze, belly, and muzzle
    - Head with pointed feline ears & micro-alert twitch
    - Glassy amber orb eyes with dual specular reflections
    - Porcelain eyelids closing on frames 20..30 and 80..90
    - Triangular nose, subtle muzzle, and whiskers
    - STRICTLY ZERO ground shadow!
    """
    C_STROKE = [0.78, 0.74, 0.68, 1.0]
    C_CREAM = [0.98, 0.97, 0.95, 1.0]
    C_PINK = [0.99, 0.73, 0.45, 1.0]
    C_WHITE = [1.0, 1.0, 1.0, 1.0]
    C_WHISKER = [0.80, 0.84, 0.88, 1.0]

    # Ginger gradients
    # #D97706 to #FDBA74
    # R: 0.85, 0.46, 0.02
    # R: 0.99, 0.73, 0.45

    def make_kf(t, s, e=None):
        if e is None:
            return {"t": t, "s": s}
        return {"t": t, "s": s, "e": e}

    # 1. Grounded Porcelain Paws (ind: 7)
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
                "ty": "gr", "nm": "Left Paw",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [46, 32]}, "p": {"a": 0, "k": [-45, 0]}, "nm": "El"},
                    {
                        "ty": "gf", "nm": "Porcelain Shading", "o": {"a": 0, "k": 100}, "t": 1,
                        "s": {"a": 0, "k": [-45, -16]}, "e": {"a": 0, "k": [-45, 16]},
                        "g": {"p": 2, "k": {"a": 0, "k": [0.0, 1.0, 1.0, 1.0, 1.0, 0.89, 0.85, 0.80]}}
                    },
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.5}, "lc": 2, "lj": 2, "nm": "St"},
                    # Toes
                    {"ty": "sh", "ks": {"a": 0, "k": {"v": [[-55, 10], [-55, 16]], "i": [[0,0],[0,0]], "o": [[0,0],[0,0]], "c": False}}, "nm": "Toe1"},
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "StT1"},
                    {"ty": "sh", "ks": {"a": 0, "k": {"v": [[-35, 10], [-35, 16]], "i": [[0,0],[0,0]], "o": [[0,0],[0,0]], "c": False}}, "nm": "Toe2"},
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "StT2"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            {
                "ty": "gr", "nm": "Right Paw",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [46, 32]}, "p": {"a": 0, "k": [45, 0]}, "nm": "El"},
                    {
                        "ty": "gf", "nm": "Porcelain Shading", "o": {"a": 0, "k": 100}, "t": 1,
                        "s": {"a": 0, "k": [45, -16]}, "e": {"a": 0, "k": [45, 16]},
                        "g": {"p": 2, "k": {"a": 0, "k": [0.0, 1.0, 1.0, 1.0, 1.0, 0.89, 0.85, 0.80]}}
                    },
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.5}, "lc": 2, "lj": 2, "nm": "St"},
                    # Toes
                    {"ty": "sh", "ks": {"a": 0, "k": {"v": [[35, 10], [35, 16]], "i": [[0,0],[0,0]], "o": [[0,0],[0,0]], "c": False}}, "nm": "Toe1"},
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "StT1"},
                    {"ty": "sh", "ks": {"a": 0, "k": {"v": [[55, 10], [55, 16]], "i": [[0,0],[0,0]], "o": [[0,0],[0,0]], "c": False}}, "nm": "Toe2"},
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "StT2"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # 2. Feline Tail Harmonic Sway (ind: 6)
    tail_rot_kf = [
        make_kf(0,   0.0, -3.5),
        make_kf(30,  -3.5, 0.0),
        make_kf(60,  0.0, 3.5),
        make_kf(90,  3.5, 0.0),
        make_kf(120, 0.0)
    ]
    tail_shape = {
        "v": [[0, 0], [-25, -45], [-35, -110], [-20, -155], [-10, -145], [-20, -100], [-10, -40]],
        "i": [[0, 0], [10, 15], [0, 25], [-8, 12], [0, -5], [5, -20], [5, -15]],
        "o": [[-10, -15], [-5, -25], [0, -25], [5, -8], [0, 10], [-5, 20], [0, 0]],
        "c": True
    }
    tail_layer = {
        "ddd": 0, "ind": 6, "ty": 4, "nm": "Ginger Tail (Harmonic Sway)", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 1, "k": tail_rot_kf},
            "p": {"a": 0, "k": [185.0, 440.0, 0.0]},
            "a": {"a": 0, "k": [0.0, 0.0, 0.0]},
            "s": {"a": 0, "k": [100.0, 100.0, 100.0]}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Tail Shell",
                "it": [
                    {"ty": "sh", "ks": {"a": 0, "k": tail_shape}, "nm": "Path"},
                    {
                        "ty": "gf", "nm": "Ginger Gradient", "o": {"a": 0, "k": 100}, "t": 1,
                        "s": {"a": 0, "k": [-30, -150]}, "e": {"a": 0, "k": [-10, 0]},
                        "g": {"p": 2, "k": {"a": 0, "k": [0.0, 0.85, 0.46, 0.02, 1.0, 0.99, 0.73, 0.45]}}
                    },
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # 3. Porcelain Torso & Head with Organic Breathing (ind: 5)
    torso_pos_kf = [
        make_kf(0,   [256.0, 335.0, 0.0], [256.0, 338.5, 0.0]),
        make_kf(30,  [256.0, 338.5, 0.0], [256.0, 335.0, 0.0]),
        make_kf(60,  [256.0, 335.0, 0.0], [256.0, 331.5, 0.0]),
        make_kf(90,  [256.0, 331.5, 0.0], [256.0, 335.0, 0.0]),
        make_kf(120, [256.0, 335.0, 0.0])
    ]
    torso_scale_kf = [
        make_kf(0,   [100.0, 100.0, 100.0], [101.0, 98.5, 100.0]),
        make_kf(30,  [101.0, 98.5, 100.0],  [100.0, 100.0, 100.0]),
        make_kf(60,  [100.0, 100.0, 100.0], [99.0, 101.5, 100.0]),
        make_kf(90,  [99.0, 101.5, 100.0],  [100.0, 100.0, 100.0]),
        make_kf(120, [100.0, 100.0, 100.0])
    ]

    torso_shape = {
        "v": [[0, -30], [90, 50], [115, 180], [60, 230], [-60, 230], [-115, 180], [-90, 50]],
        "i": [[0, 0], [0, -50], [20, -50], [40, 0], [0, 0], [-20, 50], [0, 50]],
        "o": [[0, 0], [0, 50], [-20, 50], [0, 0], [-40, 0], [20, -50], [0, -50]],
        "c": True
    }
    
    ginger_flank_left = {
        "v": [[-100, 100], [-115, 180], [-60, 230], [-40, 180], [-60, 130]],
        "i": [[0, 0], [-20, 50], [0, 0], [0, 20], [10, 10]],
        "o": [[-10, 20], [20, -50], [-20, -10], [0, -20], [-10, -10]],
        "c": True
    }
    ginger_flank_right = {
        "v": [[100, 100], [115, 180], [60, 230], [40, 180], [60, 130]],
        "i": [[0, 0], [20, 50], [0, 0], [0, 20], [-10, 10]],
        "o": [[10, 20], [-20, -50], [20, -10], [0, -20], [10, -10]],
        "c": True
    }

    torso_layer = {
        "ddd": 0, "ind": 5, "ty": 4, "nm": "Porcelain Torso Capsule (Organic Breathing)", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0},
            "p": {"a": 1, "k": torso_pos_kf},
            "a": {"a": 0, "k": [0.0, 95.0, 0.0]},
            "s": {"a": 1, "k": torso_scale_kf}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Cream Base",
                "it": [
                    {"ty": "sh", "ks": {"a": 0, "k": torso_shape}, "nm": "Path"},
                    {
                        "ty": "gf", "nm": "Porcelain Shading", "o": {"a": 0, "k": 100}, "t": 1,
                        "s": {"a": 0, "k": [0, -30]}, "e": {"a": 0, "k": [0, 230]},
                        "g": {"p": 2, "k": {"a": 0, "k": [0.0, 1.0, 1.0, 1.0, 1.0, 0.89, 0.85, 0.80]}}
                    },
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            {
                "ty": "gr", "nm": "Ginger Left Flank",
                "it": [
                    {"ty": "sh", "ks": {"a": 0, "k": ginger_flank_left}, "nm": "Path"},
                    {
                        "ty": "gf", "nm": "Ginger Grad", "o": {"a": 0, "k": 100}, "t": 1,
                        "s": {"a": 0, "k": [-115, 180]}, "e": {"a": 0, "k": [-40, 180]},
                        "g": {"p": 2, "k": {"a": 0, "k": [0.0, 0.85, 0.46, 0.02, 1.0, 0.99, 0.73, 0.45]}}
                    },
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            {
                "ty": "gr", "nm": "Ginger Right Flank",
                "it": [
                    {"ty": "sh", "ks": {"a": 0, "k": ginger_flank_right}, "nm": "Path"},
                    {
                        "ty": "gf", "nm": "Ginger Grad", "o": {"a": 0, "k": 100}, "t": 1,
                        "s": {"a": 0, "k": [115, 180]}, "e": {"a": 0, "k": [40, 180]},
                        "g": {"p": 2, "k": {"a": 0, "k": [0.0, 0.85, 0.46, 0.02, 1.0, 0.99, 0.73, 0.45]}}
                    },
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # 4. Head Dome with Pointed Feline Ears (ind: 4)
    ear_rot_kf = [
        make_kf(0,   0.0, 0.0),
        make_kf(48,  0.0, -2.5),
        make_kf(52,  -2.5, 2.0),
        make_kf(56,  2.0, 0.0),
        make_kf(120, 0.0)
    ]

    ear_l_shape = {
        "v": [[-75, -220], [-40, -140], [-105, -155]],
        "i": [[0, 0], [0, 0], [0, 0]], "o": [[0, 0], [0, 0], [0, 0]], "c": True
    }
    ear_l_inner = {
        "v": [[-70, -205], [-45, -145], [-95, -158]],
        "i": [[0, 0], [0, 0], [0, 0]], "o": [[0, 0], [0, 0], [0, 0]], "c": True
    }
    ear_r_shape = {
        "v": [[75, -220], [105, -155], [40, -140]],
        "i": [[0, 0], [0, 0], [0, 0]], "o": [[0, 0], [0, 0], [0, 0]], "c": True
    }
    ear_r_inner = {
        "v": [[70, -205], [95, -158], [45, -145]],
        "i": [[0, 0], [0, 0], [0, 0]], "o": [[0, 0], [0, 0], [0, 0]], "c": True
    }

    ginger_crown_shape = {
        "v": [[0, -173], [100, -150], [120, -75], [50, -120], [0, -100], [-50, -120], [-120, -75], [-100, -150]],
        "i": [[0, 0], [-20, -10], [0, -30], [20, 10], [20, -10], [10, 10], [0, -30], [20, -10]],
        "o": [[0, 0], [20, 10], [0, 30], [-20, -10], [-20, 10], [-10, -10], [0, 30], [-20, 10]],
        "c": True
    }

    head_layer = {
        "ddd": 0, "ind": 4, "ty": 4, "nm": "Head & Feline Ears (Porcelain)", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 1, "k": ear_rot_kf},
            "p": {"a": 1, "k": torso_pos_kf},
            "a": {"a": 0, "k": [0.0, -75.0, 0.0]},
            "s": {"a": 1, "k": torso_scale_kf}
        },
        "ao": 0,
        "shapes": [
            # Left Ear Outer & Inner
            {"ty": "gr", "nm": "Left Ear Outer", "it": [
                {"ty": "sh", "ks": {"a": 0, "k": ear_l_shape}, "nm": "P"},
                {
                    "ty": "gf", "nm": "Ginger Grad", "o": {"a": 0, "k": 100}, "t": 1,
                    "s": {"a": 0, "k": [-105, -220]}, "e": {"a": 0, "k": [-40, -140]},
                    "g": {"p": 2, "k": {"a": 0, "k": [0.0, 0.85, 0.46, 0.02, 1.0, 0.99, 0.73, 0.45]}}
                },
                {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
            ]},
            {"ty": "gr", "nm": "Left Ear Inner", "it": [
                {"ty": "sh", "ks": {"a": 0, "k": ear_l_inner}, "nm": "P"},
                {"ty": "fl", "c": {"a": 0, "k": C_PINK}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
            ]},
            # Right Ear Outer & Inner
            {"ty": "gr", "nm": "Right Ear Outer", "it": [
                {"ty": "sh", "ks": {"a": 0, "k": ear_r_shape}, "nm": "P"},
                {
                    "ty": "gf", "nm": "Ginger Grad", "o": {"a": 0, "k": 100}, "t": 1,
                    "s": {"a": 0, "k": [105, -220]}, "e": {"a": 0, "k": [40, -140]},
                    "g": {"p": 2, "k": {"a": 0, "k": [0.0, 0.85, 0.46, 0.02, 1.0, 0.99, 0.73, 0.45]}}
                },
                {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
            ]},
            {"ty": "gr", "nm": "Right Ear Inner", "it": [
                {"ty": "sh", "ks": {"a": 0, "k": ear_r_inner}, "nm": "P"},
                {"ty": "fl", "c": {"a": 0, "k": C_PINK}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
            ]},
            # Head Dome Base (Cream)
            {
                "ty": "gr", "nm": "Head Dome Base",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [250, 196]}, "p": {"a": 0, "k": [0, -75]}, "nm": "El"},
                    {
                        "ty": "gf", "nm": "Porcelain Shading", "o": {"a": 0, "k": 100}, "t": 1,
                        "s": {"a": 0, "k": [-40, -140]}, "e": {"a": 0, "k": [50, 20]},
                        "g": {"p": 2, "k": {"a": 0, "k": [0.0, 1.0, 1.0, 1.0, 1.0, 0.89, 0.85, 0.80]}}
                    },
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            # Ginger Crown Patch
            {
                "ty": "gr", "nm": "Ginger Crown",
                "it": [
                    {"ty": "sh", "ks": {"a": 0, "k": ginger_crown_shape}, "nm": "Path"},
                    {
                        "ty": "gf", "nm": "Ginger Grad", "o": {"a": 0, "k": 100}, "t": 1,
                        "s": {"a": 0, "k": [0, -170]}, "e": {"a": 0, "k": [0, -75]},
                        "g": {"p": 2, "k": {"a": 0, "k": [0.0, 0.85, 0.46, 0.02, 1.0, 0.99, 0.73, 0.45]}}
                    },
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # 5. Amber Orb Eyes (ind: 3)
    eye_layer = {
        "ddd": 0, "ind": 3, "ty": 4, "nm": "Glassy Amber Orb Eyes", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0},
            "p": {"a": 1, "k": torso_pos_kf},
            "a": {"a": 0, "k": [0.0, -75.0, 0.0]},
            "s": {"a": 1, "k": torso_scale_kf}
        },
        "ao": 0,
        "shapes": [
            # Left Eye Orb
            {
                "ty": "gr", "nm": "Left Amber Eye",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [52, 52]}, "p": {"a": 0, "k": [-46, -75]}, "nm": "El"},
                    {
                        "ty": "gf", "nm": "Amber Radial", "o": {"a": 0, "k": 100}, "t": 2,
                        "s": {"a": 0, "k": [-46, -75]}, "e": {"a": 0, "k": [-20, -75]},
                        "g": {"p": 4, "k": {"a": 0, "k": [0.0, 0.99, 0.83, 0.30, 0.45, 0.85, 0.61, 0.15, 0.85, 0.57, 0.25, 0.05, 1.0, 0.27, 0.10, 0.01]}}
                    },
                    {"ty": "st", "c": {"a": 0, "k": [0.27, 0.10, 0.01, 1.0]}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.8}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            # Right Eye Orb
            {
                "ty": "gr", "nm": "Right Amber Eye",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [52, 52]}, "p": {"a": 0, "k": [46, -75]}, "nm": "El"},
                    {
                        "ty": "gf", "nm": "Amber Radial", "o": {"a": 0, "k": 100}, "t": 2,
                        "s": {"a": 0, "k": [46, -75]}, "e": {"a": 0, "k": [72, -75]},
                        "g": {"p": 4, "k": {"a": 0, "k": [0.0, 0.99, 0.83, 0.30, 0.45, 0.85, 0.61, 0.15, 0.85, 0.57, 0.25, 0.05, 1.0, 0.27, 0.10, 0.01]}}
                    },
                    {"ty": "st", "c": {"a": 0, "k": [0.27, 0.10, 0.01, 1.0]}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.8}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            # Specular Highlights
            {
                "ty": "gr", "nm": "Left Highlight",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [10, 10]}, "p": {"a": 0, "k": [-38, -82]}, "nm": "El"},
                    {"ty": "fl", "c": {"a": 0, "k": C_WHITE}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            {
                "ty": "gr", "nm": "Right Highlight",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [10, 10]}, "p": {"a": 0, "k": [54, -82]}, "nm": "El"},
                    {"ty": "fl", "c": {"a": 0, "k": C_WHITE}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # 6. Eyelids Double Blink (ind: 2)
    eyelid_scale_y_kf = [
        make_kf(0,   0.0, 0.0),
        make_kf(20,  0.0, 100.0),
        make_kf(24,  100.0, 100.0),
        make_kf(28,  100.0, 0.0),
        make_kf(32,  0.0, 0.0),
        make_kf(80,  0.0, 100.0),
        make_kf(84,  100.0, 100.0),
        make_kf(88,  100.0, 0.0),
        make_kf(92,  0.0, 0.0),
        make_kf(120, 0.0)
    ]

    eyelid_layer = {
        "ddd": 0, "ind": 2, "ty": 4, "nm": "Porcelain Eyelids (Double Blink)", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0},
            "p": {"a": 1, "k": torso_pos_kf},
            "a": {"a": 0, "k": [0.0, -75.0, 0.0]},
            "s": {"a": 1, "k": torso_scale_kf}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Left Eyelid",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [54, 54]}, "p": {"a": 0, "k": [0, 0]}, "nm": "El"},
                    {"ty": "fl", "c": {"a": 0, "k": C_CREAM}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [-46.0, -75.0]}, "a": {"a": 0, "k": [0, -27.0]}, "s": {"a": 1, "k": [[kf["t"], [100, kf["s"]], kf.get("e", [100, 0])] if type(kf["s"]) is not list else [kf["t"], [100, kf["s"][0]], kf.get("e", [100, 0])] for kf in eyelid_scale_y_kf]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            {
                "ty": "gr", "nm": "Right Eyelid",
                "it": [
                    {"ty": "el", "d": 1, "s": {"a": 0, "k": [54, 54]}, "p": {"a": 0, "k": [0, 0]}, "nm": "El"},
                    {"ty": "fl", "c": {"a": 0, "k": C_CREAM}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"ty": "st", "c": {"a": 0, "k": C_STROKE}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [46.0, -75.0]}, "a": {"a": 0, "k": [0, -27.0]}, "s": {"a": 1, "k": [[kf["t"], [100, kf["s"]], kf.get("e", [100, 0])] if type(kf["s"]) is not list else [kf["t"], [100, kf["s"][0]], kf.get("e", [100, 0])] for kf in eyelid_scale_y_kf]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    # 7. Nose, Muzzle & Whiskers (ind: 1)
    nose_shape = {
        "v": [[0, -48], [-4, -42], [4, -42]],
        "i": [[0, 0], [0, 0], [0, 0]], "o": [[0, 0], [0, 0], [0, 0]], "c": True
    }
    w_l1 = {"v": [[-80, -50], [-135, -55]], "i": [[0, 0], [0, 0]], "o": [[0, 0], [0, 0]], "c": False}
    w_l2 = {"v": [[-80, -42], [-135, -38]], "i": [[0, 0], [0, 0]], "o": [[0, 0], [0, 0]], "c": False}
    w_r1 = {"v": [[80, -50], [135, -55]], "i": [[0, 0], [0, 0]], "o": [[0, 0], [0, 0]], "c": False}
    w_r2 = {"v": [[80, -42], [135, -38]], "i": [[0, 0], [0, 0]], "o": [[0, 0], [0, 0]], "c": False}
    mouth_shape = {
        "v": [[-8, -36], [0, -38], [8, -36]],
        "i": [[0, 0], [-4, 4], [0, 0]],
        "o": [[4, 4], [4, 4], [0, 0]],
        "c": False
    }

    face_details_layer = {
        "ddd": 0, "ind": 1, "ty": 4, "nm": "Nose Muzzle & Whiskers", "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0},
            "p": {"a": 1, "k": torso_pos_kf},
            "a": {"a": 0, "k": [0.0, -75.0, 0.0]},
            "s": {"a": 1, "k": torso_scale_kf}
        },
        "ao": 0,
        "shapes": [
            {
                "ty": "gr", "nm": "Nose",
                "it": [
                    {"ty": "sh", "ks": {"a": 0, "k": nose_shape}, "nm": "Path"},
                    {"ty": "fl", "c": {"a": 0, "k": [0.98, 0.73, 0.45, 1.0]}, "o": {"a": 0, "k": 100}, "nm": "Fl"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            {
                "ty": "gr", "nm": "Mouth",
                "it": [
                    {"ty": "sh", "ks": {"a": 0, "k": mouth_shape}, "nm": "Path"},
                    {"ty": "st", "c": {"a": 0, "k": [0.58, 0.64, 0.72, 1.0]}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.2}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            {
                "ty": "gr", "nm": "Whiskers L",
                "it": [
                    {"ty": "sh", "ks": {"a": 0, "k": w_l1}, "nm": "W1"},
                    {"ty": "sh", "ks": {"a": 0, "k": w_l2}, "nm": "W2"},
                    {"ty": "st", "c": {"a": 0, "k": C_WHISKER}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.0}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            },
            {
                "ty": "gr", "nm": "Whiskers R",
                "it": [
                    {"ty": "sh", "ks": {"a": 0, "k": w_r1}, "nm": "W1"},
                    {"ty": "sh", "ks": {"a": 0, "k": w_r2}, "nm": "W2"},
                    {"ty": "st", "c": {"a": 0, "k": C_WHISKER}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 1.0}, "lc": 2, "lj": 2, "nm": "St"},
                    {"p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "ty": "tr"}
                ]
            }
        ],
        "ip": 0, "op": 120, "st": 0, "bm": 0
    }

    lottie_data = {
        "v": "5.7.4", "fr": 30, "ip": 0, "op": 120, "w": 512, "h": 512,
        "nm": "Meoweko Flawless Idle (Pure Vector, Bicolor Ginger/Cream)",
        "layers": [
            face_details_layer, eyelid_layer, eye_layer, head_layer,
            torso_layer, tail_layer, paws_layer
        ],
        "markers": [
            {"tm": 0, "cm": "idle_start", "dr": 0},
            {"tm": 20, "cm": "blink_1", "dr": 12},
            {"tm": 48, "cm": "ear_twitch", "dr": 8},
            {"tm": 80, "cm": "blink_2", "dr": 12}
        ]
    }
    return lottie_data
'''

def get_new_svg_code():
    return '''def build_animated_svg(bg_mode="dark"):
    """
    Constructs the standalone animated SVG for Meoweko Flawless Idle.
    """
    bg_fill = "#0B0F17" if bg_mode == "dark" else "#10B981" if bg_mode == "green" else "transparent"
    bg_rect = f'<rect width="512" height="512" fill="{bg_fill}" />' if bg_fill != "transparent" else ""

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <radialGradient id="porcelainCream" cx="38%" cy="32%" r="68%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="35%" stop-color="#FAF8F5" />
      <stop offset="75%" stop-color="#F2EDE4" />
      <stop offset="100%" stop-color="#E2D9CB" />
    </radialGradient>
    <radialGradient id="amberEye" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#FCD34D" />
      <stop offset="45%" stop-color="#D99B26" />
      <stop offset="85%" stop-color="#92400E" />
      <stop offset="100%" stop-color="#451A03" />
    </radialGradient>
    <radialGradient id="pinkEar" cx="40%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#FED7AA" />
      <stop offset="60%" stop-color="#FDBA74" />
      <stop offset="100%" stop-color="#FB923C" />
    </radialGradient>
    <linearGradient id="gingerGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#D97706" />
      <stop offset="100%" stop-color="#FDBA74" />
    </linearGradient>

    <style>
      @keyframes breathe_pos {{
        0% {{ transform: translate(256px, 335px); }}
        25% {{ transform: translate(256px, 338.5px); }}
        50% {{ transform: translate(256px, 335px); }}
        75% {{ transform: translate(256px, 331.5px); }}
        100% {{ transform: translate(256px, 335px); }}
      }}
      @keyframes breathe_scale {{
        0% {{ transform: scale(1, 1); }}
        25% {{ transform: scale(1.01, 0.985); }}
        50% {{ transform: scale(1, 1); }}
        75% {{ transform: scale(0.99, 1.015); }}
        100% {{ transform: scale(1, 1); }}
      }}
      @keyframes tail_sway {{
        0% {{ transform: rotate(-3.5deg); }}
        25% {{ transform: rotate(0deg); }}
        50% {{ transform: rotate(3.5deg); }}
        75% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(-3.5deg); }}
      }}
      @keyframes ear_twitch {{
        0%, 35%, 55%, 100% {{ transform: rotate(0deg); }}
        40% {{ transform: rotate(-2.5deg); }}
        45% {{ transform: rotate(2.0deg); }}
        50% {{ transform: rotate(0deg); }}
      }}
      @keyframes blink_y {{
        0%, 15%, 26%, 60%, 75%, 100% {{ transform: scaleY(0); }}
        18%, 23%, 68%, 73% {{ transform: scaleY(1); }}
      }}
      
      .torso_group {{
        animation: breathe_pos 4s ease-in-out infinite;
      }}
      .torso_scale {{
        animation: breathe_scale 4s ease-in-out infinite;
      }}
      .head_group {{
        transform: translate(0, -75px);
        animation: ear_twitch 4s ease-in-out infinite;
      }}
      .tail_group {{
        transform-origin: 185px 440px;
        animation: tail_sway 4s ease-in-out infinite;
      }}
      .eyelid {{
        transform-origin: 0 -27px;
        animation: blink_y 4s ease-in-out infinite;
      }}
    </style>
  </defs>

  {bg_rect}

  <!-- Layer 7: Grounded Paws (dy=0) -->
  <g transform="translate(256, 465)">
    <!-- Left Paw -->
    <ellipse cx="-45" cy="0" rx="23" ry="16" fill="url(#porcelainCream)" stroke="#C8BEAD" stroke-width="1.5" />
    <path d="M -55 5 L -55 12" stroke="#C8BEAD" stroke-width="1.2" fill="none" stroke-linecap="round"/>
    <path d="M -35 5 L -35 12" stroke="#C8BEAD" stroke-width="1.2" fill="none" stroke-linecap="round"/>
    <!-- Right Paw -->
    <ellipse cx="45" cy="0" rx="23" ry="16" fill="url(#porcelainCream)" stroke="#C8BEAD" stroke-width="1.5" />
    <path d="M 35 5 L 35 12" stroke="#C8BEAD" stroke-width="1.2" fill="none" stroke-linecap="round"/>
    <path d="M 55 5 L 55 12" stroke="#C8BEAD" stroke-width="1.2" fill="none" stroke-linecap="round"/>
  </g>

  <!-- Layer 6: Tail -->
  <g class="tail_group">
    <g transform="translate(185, 440)">
      <path d="M 0 0 C 10 15 0 25 -25 -45 C -8 12 0 -5 -35 -110 C 5 -20 5 -15 -40 -170 C -15 -20 -10 -30 -15 -180 C 0 -35 10 -10 -10 -120 C 0 15 -5 30 -15 -50 Z" fill="url(#gingerGrad)" stroke="#C8BEAD" stroke-width="1.2" />
    </g>
  </g>

  <!-- Layers 5 to 1: Torso, Head, Face -->
  <g class="torso_group">
    <g class="torso_scale">
      
      <!-- Torso Base (Cream) -->
      <g transform="translate(0, 95)">
        <path d="M 0 -30 C 0 0 0 -50 90 50 C 20 -50 40 0 115 180 C 0 0 -20 50 60 230 C 0 50 -40 0 -60 230 C 20 -50 0 -50 -115 180 C 0 50 0 0 -90 50 Z" fill="url(#porcelainCream)" stroke="#C8BEAD" stroke-width="1.2" />
        <path d="M -100 100 C 0 0 -20 50 -115 180 C 0 0 0 20 -60 230 C -10 20 20 -50 -40 180 C -20 -10 10 10 -60 130 Z" fill="url(#gingerGrad)" />
        <path d="M 100 100 C 0 0 20 50 115 180 C 0 0 0 20 60 230 C 10 20 -20 -50 40 180 C 20 -10 -10 10 60 130 Z" fill="url(#gingerGrad)" />
      </g>

      <!-- Head Base & Ears -->
      <g class="head_group">
        <!-- Left Ear -->
        <polygon points="-75,-220 -40,-140 -105,-155" fill="url(#gingerGrad)" stroke="#C8BEAD" stroke-width="1.2" />
        <polygon points="-70,-205 -45,-145 -95,-158" fill="url(#pinkEar)" />
        <!-- Right Ear -->
        <polygon points="75,-220 105,-155 40,-140" fill="url(#gingerGrad)" stroke="#C8BEAD" stroke-width="1.2" />
        <polygon points="70,-205 95,-158 45,-145" fill="url(#pinkEar)" />
        
        <!-- Head Dome (Cream Base) -->
        <ellipse cx="0" cy="0" rx="125" ry="98" fill="url(#porcelainCream)" stroke="#C8BEAD" stroke-width="1.2" />
        <!-- Ginger Crown Patch -->
        <path d="M 0 -173 C 0 0 -20 -10 100 -150 C 0 -30 20 10 120 -75 C 20 -10 10 10 50 -120 C 0 -30 20 -10 0 -100 C -20 10 -10 -10 -50 -120 C 0 30 -20 -10 -120 -75 C 20 10 0 -30 -100 -150 Z" fill="url(#gingerGrad)" />
        
        <!-- Amber Eyes -->
        <circle cx="-46" cy="0" r="26" fill="url(#amberEye)" stroke="#451A03" stroke-width="1.8" />
        <circle cx="46" cy="0" r="26" fill="url(#amberEye)" stroke="#451A03" stroke-width="1.8" />
        <!-- Specular Highlights -->
        <circle cx="-38" cy="-7" r="5" fill="#FFFFFF" />
        <circle cx="54" cy="-7" r="5" fill="#FFFFFF" />
        
        <!-- Eyelids (Blink) -->
        <g transform="translate(-46, 0)">
          <ellipse cx="0" cy="0" rx="27" ry="27" class="eyelid" fill="url(#porcelainCream)" stroke="#C8BEAD" stroke-width="1.2" />
        </g>
        <g transform="translate(46, 0)">
          <ellipse cx="0" cy="0" rx="27" ry="27" class="eyelid" fill="url(#porcelainCream)" stroke="#C8BEAD" stroke-width="1.2" />
        </g>

        <!-- Nose -->
        <polygon points="0,27 -4,33 4,33" fill="#FDBA74" />
        <path d="M -8 39 C -4 43 0 41 0 37 C 0 41 4 43 8 39" fill="none" stroke="#94A3B8" stroke-width="1.2" />
        
        <!-- Whiskers -->
        <line x1="-80" y1="25" x2="-135" y2="20" stroke="#CBD5E1" stroke-width="1.0" />
        <line x1="-80" y1="33" x2="-135" y2="37" stroke="#CBD5E1" stroke-width="1.0" />
        <line x1="80" y1="25" x2="135" y2="20" stroke="#CBD5E1" stroke-width="1.0" />
        <line x1="80" y1="33" x2="135" y2="37" stroke="#CBD5E1" stroke-width="1.0" />
      </g>
    </g>
  </g>
</svg>"""
    return svg
'''

with open("scripts/build_flawless_meoweko_idle.py", "r") as f:
    content = f.read()

# Replace build_pure_vector_lottie
new_lottie = get_new_lottie_code()
content = re.sub(
    r'def build_pure_vector_lottie\(\):.*?(?=def build_animated_svg)',
    new_lottie + '\n',
    content,
    flags=re.DOTALL
)

# Replace build_animated_svg
new_svg = get_new_svg_code()
content = re.sub(
    r'def build_animated_svg\(bg_mode="dark"\):.*?(?=def run_meoweko_idle_production)',
    new_svg + '\n',
    content,
    flags=re.DOTALL
)

with open("scripts/build_flawless_meoweko_idle.py", "w") as f:
    f.write(content)

