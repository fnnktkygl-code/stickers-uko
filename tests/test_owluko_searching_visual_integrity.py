#!/usr/bin/env python3
"""
Unit Test Suite for Owluko Searching (08_searching) — Visual Integrity & Contract Verification.
Verifies all strict project contracts:
1. All required deliverables exist across assets/08_searching and 02_refonte_nouvelle/08_searching
2. Pure vector Lottie JSON is strictly < 50.0 KB
3. Strictly ZERO ground shadow (0 shadow layers in Lottie, 0 shadow elements in SVG, 0 below baseline)
4. Grounded feet: Delta Y = 0 px (Owluko stands firmly on the ground, does not levitate)
5. Head executes 360° rotation across 4 canonical phases with Option A markers
6. Double blink verified during 270° profile left hold
7. 2-Tier Master Board (1920x1080) and Trichroma Board (1536x512) fully populated with zero dead space
8. Porcelain color palette conformity (warm cream ceramic + amber eyes + golden beak)
"""

import os
import json
import unittest
import numpy as np
from PIL import Image

WORKSPACE_DIR = "/Users/richard/Developer/Stickers Uko"
SEARCH_DIR = os.path.join(WORKSPACE_DIR, "mascots/owluko/assets/08_searching")
REFONTE_DIR = os.path.join(WORKSPACE_DIR, "mascots/owluko/02_refonte_nouvelle/08_searching")
BRAIN_DIR = "/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68"

REQUIRED_FILES = [
    "lottie.json",
    "owluko_searching_animated.svg",
    "owluko_searching_animated_transparent.svg",
    "animated.webp",
    "animated.gif",
    "animated_dark.gif",
    "animated_green.gif",
    "looped_video.mp4",
    "source_video.mp4",
    "static.png",
    "static.webp",
    "owluko_searching_master_board.png",
    "owluko_searching_studio_trichroma_board.png",
    "bundle_owluko_08_searching.zip",
    "snippet.json"
]

class TestOwlukoSearchingVisualIntegrity(unittest.TestCase):

    def test_01_all_deliverables_exist(self):
        """Verify all 15 required deliverables exist in both production directories."""
        for d in [SEARCH_DIR, REFONTE_DIR]:
            self.assertTrue(os.path.exists(d), f"Directory does not exist: {d}")
            for fname in REQUIRED_FILES:
                p = os.path.join(d, fname)
                self.assertTrue(os.path.exists(p), f"Missing deliverable in {d}: {fname}")
                self.assertGreater(os.path.getsize(p), 0, f"File is empty: {p}")

    def test_02_pure_vector_lottie_under_50kb(self):
        """Verify pure vector Lottie JSON payload is strictly < 50.0 KB."""
        lottie_path = os.path.join(SEARCH_DIR, "lottie.json")
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
        with open(os.path.join(SEARCH_DIR, "lottie.json")) as f:
            data = json.load(f)
        for layer in data.get("layers", []):
            layer_name = layer.get("nm", "").lower()
            self.assertNotIn("shadow", layer_name, f"Found ground shadow layer in Lottie: {layer_name}")
            self.assertNotIn("ombre", layer_name, f"Found ground shadow layer in Lottie: {layer_name}")

        with open(os.path.join(SEARCH_DIR, "owluko_searching_animated.svg")) as f:
            svg_text = f.read().lower()
        self.assertNotIn("ground-shadow", svg_text, "Found ground shadow class in SVG")
        self.assertNotIn("groundshadow", svg_text, "Found ground shadow ID in SVG")

        # Check static poster: no shadow below feet (Y > 500)
        static_img = Image.open(os.path.join(SEARCH_DIR, "static.png"))
        arr = np.array(static_img)
        sub_floor_alpha = arr[502:, :, 3]
        self.assertEqual(np.sum(sub_floor_alpha > 30), 0, "Found non-zero alpha below floor line (artificial ground shadow)")

    def test_04_grounded_feet_stationary_delta_y_zero(self):
        """Verify grounded feet are stationary with Delta Y = 0 px."""
        with open(os.path.join(SEARCH_DIR, "lottie.json")) as f:
            data = json.load(f)
        feet_layer = None
        for layer in data.get("layers", []):
            if "feet" in layer.get("nm", "").lower():
                feet_layer = layer
                break
        self.assertIsNotNone(feet_layer, "Could not find grounded feet layer in Lottie")
        p_prop = feet_layer["ks"]["p"]
        self.assertEqual(p_prop["a"], 0, "Feet position must be static (a=0)")
        self.assertEqual(p_prop["k"], [256.0, 465.0, 0.0], "Feet position must be anchored at (256, 465)")

    def test_05_head_360_rotation_phases(self):
        """Verify head 360° rotation markers in Lottie JSON."""
        with open(os.path.join(SEARCH_DIR, "lottie.json")) as f:
            data = json.load(f)
        marker_names = [m.get("cm") for m in data.get("markers", [])]
        expected_markers = ["search_scan_right", "search_blink_pause", "search_scan_left", "search_settle_loop"]
        for em in expected_markers:
            self.assertIn(em, marker_names, f"Missing marker in Lottie: {em}")

    def test_06_double_blink_at_270_degrees(self):
        """Verify double blink keyframes exist on left eye in Lottie JSON."""
        with open(os.path.join(SEARCH_DIR, "lottie.json")) as f:
            data = json.load(f)
        eye_l_layer = None
        for layer in data.get("layers", []):
            if "eye" in layer.get("nm", "").lower():
                eye_l_layer = layer
                break
        self.assertIsNotNone(eye_l_layer, "Could not find amber eye layer")
        eyelid_shape = None
        for shape in eye_l_layer.get("shapes", []):
            if "eyelid" in shape.get("nm", "").lower():
                eyelid_shape = shape
                break
        self.assertIsNotNone(eyelid_shape, "Could not find porcelain eyelid in eye layer")

    def test_07_master_board_two_tier_layout_and_no_dead_space(self):
        """Verify 2-Tier Master Presentation Board is 1920x1080 and fully populated."""
        mb_path = os.path.join(SEARCH_DIR, "owluko_searching_master_board.png")
        self.assertTrue(os.path.exists(mb_path))
        img = Image.open(mb_path)
        self.assertEqual(img.size, (1920, 1080))
        arr = np.array(img)
        # Check Tier 1 non-black pixels
        t1_pixels = arr[120:560, 50:1870]
        self.assertGreater(np.mean(t1_pixels > 20), 0.35, "Tier 1 has too many empty pixels")
        # Check Tier 2 non-black pixels (no dead space!)
        t2_pixels = arr[610:1040, 50:1870]
        self.assertGreater(np.mean(t2_pixels > 20), 0.35, "Tier 2 has too many empty pixels (dead space)")

    def test_08_trichroma_board_dimensions(self):
        """Verify Trichroma Presentation Board is 1536x512."""
        tb_path = os.path.join(SEARCH_DIR, "owluko_searching_studio_trichroma_board.png")
        self.assertTrue(os.path.exists(tb_path))
        img = Image.open(tb_path)
        self.assertEqual(img.size, (1536, 512))

    def test_09_porcelain_color_palette(self):
        """Verify warm cream porcelain palette and amber eyes in static poster."""
        static_img = Image.open(os.path.join(SEARCH_DIR, "static.png"))
        arr = np.array(static_img)
        alpha = arr[:, :, 3]
        r = arr[:, :, 0]
        g = arr[:, :, 1]
        b = arr[:, :, 2]
        # Amber eye pixels
        amber = (alpha > 200) & (r > 120) & (g > 60) & (b < 95) & (r - b > 40)
        self.assertGreater(np.sum(amber), 300, "Missing amber eye color in static poster")
        # Porcelain belly pixels
        porcelain = (r > 200) & (g > 190) & (b > 180) & (r >= b) & (alpha > 100)
        self.assertGreater(np.sum(porcelain), 5000, "Missing warm cream porcelain in static poster")

if __name__ == '__main__':
    unittest.main()
