#!/usr/bin/env python3
"""
Unit Test Suite for Meoweko Idle (00_idle) — Visual Integrity & Contract Verification.
Verifies all strict project contracts:
1. All 15 required deliverables exist across assets/00_idle and 02_refonte_nouvelle/00_idle
2. Pure vector Lottie JSON is strictly < 50.0 KB
3. Strictly ZERO ground shadow (0 shadow layers in Lottie, 0 shadow elements in SVG, 0 below baseline Y=491)
4. Grounded paws: Delta Y = 0 px (Meoweko sits firmly on the ground, zero levitation)
5. Bodymovin markers: idle_start, blink_1, ear_twitch, blink_2
6. Porcelain color palette conformity (warm cream ceramic R >= B, despill green excess <= 0.0)
7. Amber eye chromaticity (luminous golden/amber orb eyes R > 140, G > 90, B < 85)
8. Strictly ZERO human hands or fingers (feline ears, paws, and tail only)
"""

import os
import json
import unittest
import numpy as np
from PIL import Image

WORKSPACE_DIR = "/Users/richard/Developer/Stickers Uko"
IDLE_DIR = os.path.join(WORKSPACE_DIR, "mascots/meoweko/assets/00_idle")
REFONTE_DIR = os.path.join(WORKSPACE_DIR, "mascots/meoweko/02_refonte_nouvelle/00_idle")

REQUIRED_FILES = [
    "lottie.json",
    "meoweko_idle_animated.svg",
    "meoweko_idle_animated_transparent.svg",
    "animated.webp",
    "animated.gif",
    "animated_dark.gif",
    "animated_green.gif",
    "looped_video.mp4",
    "source_video.mp4",
    "static.png",
    "static.webp",
    "meoweko_idle_master_board.png",
    "meoweko_idle_studio_trichroma_board.png",
    "bundle_meoweko_00_idle.zip",
    "snippet.json"
]

class TestMeowekoIdleVisualIntegrity(unittest.TestCase):

    def test_01_all_deliverables_exist(self):
        """Verify all 15 required deliverables exist in both production directories."""
        for d in [IDLE_DIR, REFONTE_DIR]:
            self.assertTrue(os.path.exists(d), f"Directory does not exist: {d}")
            for fname in REQUIRED_FILES:
                p = os.path.join(d, fname)
                self.assertTrue(os.path.exists(p), f"Missing deliverable in {d}: {fname}")
                self.assertGreater(os.path.getsize(p), 0, f"File is empty: {p}")

    def test_02_pure_vector_lottie_under_50kb(self):
        """Verify pure vector Lottie JSON payload is strictly < 50.0 KB."""
        lottie_path = os.path.join(IDLE_DIR, "lottie.json")
        self.assertTrue(os.path.exists(lottie_path))
        size_kb = os.path.getsize(lottie_path) / 1024.0
        self.assertLess(size_kb, 50.0, f"Lottie payload too large: {size_kb:.2f} KB >= 50.0 KB")

        with open(lottie_path) as f:
            data = json.load(f)

        self.assertEqual(data.get("w"), 512)
        self.assertEqual(data.get("h"), 512)
        self.assertEqual(data.get("fr"), 30.0)
        self.assertEqual(data.get("op"), 120)
        self.assertEqual(len(data.get("assets", [])), 0, "Lottie must be 100% pure vector with 0 raster assets")

    def test_03_strictly_zero_ground_shadow(self):
        """Verify strictly ZERO ground shadow in Lottie, SVG, and raster deliverables."""
        with open(os.path.join(IDLE_DIR, "lottie.json")) as f:
            data = json.load(f)
        for layer in data.get("layers", []):
            layer_name = layer.get("nm", "").lower()
            self.assertNotIn("shadow", layer_name, f"Found ground shadow layer in Lottie: {layer_name}")
            self.assertNotIn("ombre", layer_name, f"Found ground shadow layer in Lottie: {layer_name}")

        with open(os.path.join(IDLE_DIR, "meoweko_idle_animated.svg")) as f:
            svg_text = f.read().lower()
        self.assertNotIn("ground-shadow", svg_text, "Found ground shadow class in SVG")
        self.assertNotIn("groundshadow", svg_text, "Found ground shadow ID in SVG")

        # Check static poster: no shadow below feet (Y >= 492)
        static_img = Image.open(os.path.join(IDLE_DIR, "static.png"))
        arr = np.array(static_img)
        sub_floor_alpha = arr[492:, :, 3]
        self.assertEqual(np.max(sub_floor_alpha), 0, "Found non-zero alpha below floor line (artificial ground shadow)")

    def test_04_grounded_paws_stationary_delta_y_zero(self):
        """Verify grounded paws are stationary with Delta Y = 0 px."""
        with open(os.path.join(IDLE_DIR, "lottie.json")) as f:
            data = json.load(f)
        paws_layer = None
        for layer in data.get("layers", []):
            if "paws" in layer.get("nm", "").lower():
                paws_layer = layer
                break
        self.assertIsNotNone(paws_layer, "Could not find grounded paws layer in Lottie")
        p_prop = paws_layer["ks"]["p"]
        self.assertEqual(p_prop["a"], 0, "Paws position must be static (a=0)")
        self.assertEqual(p_prop["k"], [256.0, 465.0, 0.0], "Paws position must be anchored at [256, 465]")

    def test_05_bodymovin_markers(self):
        """Verify idle markers in Lottie JSON."""
        with open(os.path.join(IDLE_DIR, "lottie.json")) as f:
            data = json.load(f)
        marker_names = [m.get("cm") for m in data.get("markers", [])]
        expected_markers = ["idle_start", "blink_1", "ear_twitch", "blink_2"]
        for em in expected_markers:
            self.assertIn(em, marker_names, f"Missing marker in Lottie: {em}")

    def test_06_porcelain_color_palette_and_no_green_spill(self):
        """Verify porcelain body has warm ceramic tones and zero green screen spill."""
        static_p = os.path.join(IDLE_DIR, "static.png")
        with Image.open(static_p) as img:
            arr = np.array(img)
            r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]

            porcelain_mask = (a > 200) & (r > 150) & (b > 120)
            self.assertGreater(np.sum(porcelain_mask), 5000, "Insufficient porcelain pixels detected")

            r_samples = r[porcelain_mask]
            b_samples = b[porcelain_mask]
            self.assertGreaterEqual(np.mean(r_samples), np.mean(b_samples), "Porcelain is too cold / blue")

            g_samples = g[porcelain_mask]
            green_excess = g_samples.astype(np.float32) - (r_samples.astype(np.float32) * 0.52 + b_samples.astype(np.float32) * 0.48)
            self.assertLessEqual(np.mean(green_excess), 0.0, "Mean green excess should be negative or zero (clean despill)")
            self.assertLess(np.percentile(green_excess, 99), 5.0, "Green screen spill detected on 99th percentile of porcelain body!")

    def test_07_amber_eye_chromaticity(self):
        """Verify amber orb eyes have intense, warm golden/amber chroma."""
        static_p = os.path.join(IDLE_DIR, "static.png")
        with Image.open(static_p) as img:
            arr = np.array(img)
            r, g, b, a = arr[:, :, 0].astype(np.float32), arr[:, :, 1].astype(np.float32), arr[:, :, 2].astype(np.float32), arr[:, :, 3]

            eye_mask = (a > 200) & (r > 120) & (g > 60) & (b < 95) & (r - b > 40)
            amber_pixels = np.sum(eye_mask)
            self.assertGreater(amber_pixels, 300, f"Expected >300 amber eye pixels, found {amber_pixels}")

            r_eye = r[eye_mask]
            g_eye = g[eye_mask]
            b_eye = b[eye_mask]
            self.assertGreater(np.mean(r_eye), 140.0, "Amber eye red component is too low")
            self.assertGreater(np.mean(g_eye), 90.0, "Amber eye green component is too low")
            self.assertLess(np.mean(b_eye), 85.0, "Amber eye blue component is too high (lacks amber warmth)")

    def test_08_strictly_zero_human_hands_or_fingers(self):
        """Verify description and vector metadata strictly forbid human hands/fingers."""
        forbidden_keywords = ["human hand", "finger", "thumb", "main humaine"]
        
        svg_p = os.path.join(IDLE_DIR, "meoweko_idle_animated.svg")
        with open(svg_p, "r", encoding="utf-8") as f:
            svg_text = f.read().lower()
            for kw in forbidden_keywords:
                self.assertNotIn(kw, svg_text, f"Forbidden keyword '{kw}' found in SVG!")

    def test_09_full_tail_uncropped_across_all_frames(self):
        """Verify that the feline tail is NEVER clipped or cropped across all 120 frames."""
        webp_p = os.path.join(IDLE_DIR, "animated.webp")
        self.assertTrue(os.path.exists(webp_p))
        with Image.open(webp_p) as img:
            for i in range(img.n_frames):
                img.seek(i)
                arr = np.array(img.convert("RGBA"))
                ys, xs = np.where(arr[:, :, 3] > 20)
                left_margin = xs.min()
                right_margin = 511 - xs.max()
                self.assertGreater(left_margin, 40, f"Tail is clipped on left in frame {i} (margin: {left_margin} px)")
                self.assertGreater(right_margin, 40, f"Mascot touches right edge in frame {i} (margin: {right_margin} px)")

if __name__ == "__main__":
    unittest.main()
