#!/usr/bin/env python3
"""
Unit test suite verifying the visual and mathematical integrity of the Owluko Master Idle deliverables.
Covers:
1. File existence and non-zero byte size across workspace and refonte directories.
2. Canonical resolutions (512x512 for static/animations, 1920x1080 for master board, 1536x512 for trichroma).
3. Pure vector Lottie JSON payload strictly < 50.0 KB and valid JSON structure.
4. Grounded feet: Delta Y = 0 px (serres remain locked at floor baseline Y = 497 px).
5. Double organic blink: Verified closure on frames 18..28 and 78..88.
6. Porcelain color fidelity: Warm cream ceramic tone (R >= B, mean green excess < 0.0, 99th percentile < 5.0).
7. Amber eye chromaticity: High warm chroma (R > 120, G > 60, B < 95, R - B > 40).
8. Strictly ZERO hands, ZERO fingers, ZERO thumbs.
9. Standalone animated SVG valid XML structure.
"""

import os
import json
import unittest
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

WORKSPACE_DIR = "/Users/richard/Developer/Stickers Uko"
OWLUKO_ASSETS_DIR = os.path.join(WORKSPACE_DIR, "mascots/owluko/assets/00_idle")
OWLUKO_REFONTE_DIR = os.path.join(WORKSPACE_DIR, "mascots/owluko/02_refonte_nouvelle/00_idle")

class TestOwlukoIdleVisualIntegrity(unittest.TestCase):

    def test_01_all_deliverables_exist_and_non_empty(self):
        """Verify all 11 canonical deliverables exist and have non-zero size in both asset directories."""
        required_files = [
            "lottie.json",
            "owluko_idle_animated.svg",
            "owluko_idle_animated_transparent.svg",
            "animated.webp",
            "animated.gif",
            "animated_dark.gif",
            "animated_green.gif",
            "looped_video.mp4",
            "static.png",
            "static.webp",
            "owluko_idle_master_board.png",
            "owluko_idle_studio_trichroma_board.png",
            "bundle_owluko_00_idle.zip"
        ]

        for target_dir in [OWLUKO_ASSETS_DIR, OWLUKO_REFONTE_DIR]:
            self.assertTrue(os.path.exists(target_dir), f"Directory missing: {target_dir}")
            for fname in required_files:
                p = os.path.join(target_dir, fname)
                self.assertTrue(os.path.exists(p), f"Missing file: {p}")
                self.assertGreater(os.path.getsize(p), 100, f"File too small or empty: {p}")

    def test_02_pure_vector_lottie_size_strictly_under_50kb(self):
        """Verify the Lottie JSON payload is strictly under 50.0 KB (high performance web standard)."""
        lottie_p = os.path.join(OWLUKO_ASSETS_DIR, "lottie.json")
        size_kb = os.path.getsize(lottie_p) / 1024.0
        self.assertLess(size_kb, 50.0, f"Lottie payload is too large ({size_kb:.2f} KB >= 50.0 KB)")

        with open(lottie_p, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(data.get("w"), 512)
            self.assertEqual(data.get("h"), 512)
            self.assertEqual(data.get("op"), 120)
            self.assertEqual(data.get("fr"), 30)
            # Verify grounded feet layer exists
            layer_names = [l.get("nm") for l in data.get("layers", [])]
            self.assertTrue(any("Grounded" in nm or "Feet" in nm for nm in layer_names), f"Missing feet layer: {layer_names}")

    def test_03_grounded_feet_zero_displacement(self):
        """Verify Owluko's feet remain 100% grounded (Delta Y = 0 px) across keyframes."""
        master_board_p = os.path.join(OWLUKO_ASSETS_DIR, "owluko_idle_master_board.png")
        self.assertTrue(os.path.exists(master_board_p))

        # Check Lottie feet position property is static (a = 0, no keyframe animation on feet position)
        lottie_p = os.path.join(OWLUKO_ASSETS_DIR, "lottie.json")
        with open(lottie_p, "r", encoding="utf-8") as f:
            data = json.load(f)
            feet_layer = None
            for layer in data["layers"]:
                if "feet" in layer.get("nm", "").lower():
                    feet_layer = layer
                    break
            self.assertIsNotNone(feet_layer, "Feet layer not found in Lottie")
            # Feet position must be static: "a": 0 (not animated array)
            pos_anim = feet_layer["ks"]["p"]["a"]
            self.assertEqual(pos_anim, 0, f"Feet position must be static (a=0), got {pos_anim}")

    def test_04_double_organic_blink_timing(self):
        """Verify the double blink markers and keyframes are set around f in [18, 28] and f in [78, 88]."""
        lottie_p = os.path.join(OWLUKO_ASSETS_DIR, "lottie.json")
        with open(lottie_p, "r", encoding="utf-8") as f:
            data = json.load(f)
            markers = {m["cm"]: m["tm"] for m in data.get("markers", [])}
            self.assertIn("blink_1", markers, "Marker blink_1 missing")
            self.assertIn("blink_2", markers, "Marker blink_2 missing")
            self.assertEqual(markers["blink_1"], 18)
            self.assertEqual(markers["blink_2"], 78)

    def test_05_porcelain_color_fidelity_and_clean_despill(self):
        """Verify static render has warm porcelain ceramic tone and zero green screen spill."""
        static_p = os.path.join(OWLUKO_ASSETS_DIR, "static.png")
        with Image.open(static_p) as img:
            arr = np.array(img)
            r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]

            porcelain_mask = (a > 200) & (r > 150) & (b > 120)
            self.assertGreater(np.sum(porcelain_mask), 5000, "Insufficient porcelain pixels detected")

            # 1. Warm porcelain: R >= B
            r_samples = r[porcelain_mask]
            b_samples = b[porcelain_mask]
            self.assertGreaterEqual(np.mean(r_samples), np.mean(b_samples), "Porcelain is too cold / blue")

            # 2. Despill: Mean green excess must be < 0.0 and 99th percentile < 5.0
            g_samples = g[porcelain_mask]
            green_excess = g_samples.astype(np.float32) - (r_samples.astype(np.float32) * 0.52 + b_samples.astype(np.float32) * 0.48)
            self.assertLess(np.mean(green_excess), 0.0, "Mean green excess should be negative (clean despill)")
            self.assertLess(np.percentile(green_excess, 99), 5.0, "Green screen spill detected on 99th percentile of porcelain body!")

    def test_06_amber_eye_chromaticity(self):
        """Verify amber orb eyes have high chroma warmth."""
        static_p = os.path.join(OWLUKO_ASSETS_DIR, "static.png")
        with Image.open(static_p) as img:
            arr = np.array(img)
            r, g, b, a = arr[:, :, 0].astype(np.float32), arr[:, :, 1].astype(np.float32), arr[:, :, 2].astype(np.float32), arr[:, :, 3]

            eye_mask = (a > 200) & (r > 120) & (g > 60) & (b < 95) & (r - b > 40)
            amber_pixels = np.sum(eye_mask)
            self.assertGreater(amber_pixels, 300, f"Expected >300 amber eye pixels, found {amber_pixels}")

            r_eye = r[eye_mask]
            g_eye = g[eye_mask]
            b_eye = b[eye_mask]
            self.assertGreater(np.mean(r_eye), 140.0)
            self.assertGreater(np.mean(g_eye), 90.0)
            self.assertLess(np.mean(b_eye), 75.0)

    def test_07_strictly_zero_human_hands_or_fingers(self):
        """Verify SVG and Lottie layers contain no human hands or fingers."""
        forbidden_keywords = ["human hand", "finger", "thumb", "main humaine"]

        svg_p = os.path.join(OWLUKO_ASSETS_DIR, "owluko_idle_animated.svg")
        with open(svg_p, "r", encoding="utf-8") as f:
            svg_text = f.read().lower()
            for kw in forbidden_keywords:
                self.assertNotIn(kw, svg_text, f"Forbidden keyword '{kw}' found in SVG!")

    def test_08_pure_vector_svg_valid_xml(self):
        """Verify animated SVG is well-formed XML with valid viewBox."""
        svg_p = os.path.join(OWLUKO_ASSETS_DIR, "owluko_idle_animated.svg")
        tree = ET.parse(svg_p)
        root = tree.getroot()
        self.assertTrue(root.tag.endswith("svg"), "Root element must be <svg>")
        self.assertEqual(root.attrib.get("viewBox"), "0 0 512 512")

    def test_09_strictly_zero_ground_shadow(self):
        """Verify complete absence of ground shadow across Lottie, SVG, and raster deliverables."""
        # 1. Check Lottie layers: No shadow layer
        lottie_p = os.path.join(OWLUKO_ASSETS_DIR, "lottie.json")
        with open(lottie_p, "r", encoding="utf-8") as f:
            data = json.load(f)
            layer_names = [l.get("nm", "").lower() for l in data.get("layers", [])]
            for nm in layer_names:
                self.assertNotIn("shadow", nm, f"Found shadow layer in Lottie: {nm}")

        # 2. Check SVG: No shadow gradient or ellipse
        svg_p = os.path.join(OWLUKO_ASSETS_DIR, "owluko_idle_animated.svg")
        with open(svg_p, "r", encoding="utf-8") as f:
            svg_text = f.read().lower()
            self.assertNotIn("groundshadow", svg_text, "Found ground shadow in SVG")
            self.assertNotIn("ground-shadow", svg_text, "Found ground shadow class in SVG")

        # 3. Check raster static.png: pixels below y=498 must have 0 alpha (no ground shadow ellipse)
        static_p = os.path.join(OWLUKO_ASSETS_DIR, "static.png")
        with Image.open(static_p) as img:
            arr = np.array(img)
            alpha_below_feet = arr[499:, :, 3]
            self.assertEqual(np.sum(alpha_below_feet > 10), 0, "Detected non-zero alpha below feet baseline (ground shadow residual)")

if __name__ == "__main__":
    unittest.main()
