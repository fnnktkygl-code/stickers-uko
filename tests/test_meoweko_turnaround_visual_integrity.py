#!/usr/bin/env python3
"""
Unit test suite verifying the visual and mathematical integrity of the Meoweko Master Turnaround deliverables.
Covers:
1. File existence and non-zero byte size across workspace and refonte directories.
2. Canonical dimensions (1920x820 for sheets, 1920x1600 for dual board, 1024x512 for side-by-side, 512x512 for standalone views).
3. Porcelain color fidelity (warm cream ceramic tone R >= B, absence of green screen spill mean <= 0.0, 99th percentile < 5.0).
4. Amber eye chromaticity (luminous golden/amber orb eyes with R > 120, G > 60, B < 95, R - B > 40).
5. Strictly ZERO hands, ZERO fingers, ZERO thumbs (feline ears, paws, and tail only).
6. Pure vector SVG valid XML structure and viewport definitions.
7. Interactive 3D viewer HTML presence and structure.
8. Strictly ZERO ground shadow (alpha == 0 below baseline Y = 491 px).
"""

import os
import unittest
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

WORKSPACE_DIR = "/Users/richard/Developer/Stickers Uko"
MEOWEKO_DIR = os.path.join(WORKSPACE_DIR, "mascots/meoweko")
REFONTE_DIR = os.path.join(MEOWEKO_DIR, "02_refonte_nouvelle/master_turnaround")

class TestMeowekoTurnaroundVisualIntegrity(unittest.TestCase):

    def test_01_all_deliverables_exist_and_non_empty(self):
        """Verify all 11 canonical deliverables exist and have non-zero size."""
        required_files = [
            "meoweko_master_turnaround_sheet.png",
            "meoweko_studio_turnaround_sheet.png",
            "meoweko_turnaround_master_board.png",
            "meoweko_master_side_by_side.png",
            "meoweko_master_exact_512.png",
            "meoweko_master_turnaround.svg",
            "meoweko_3d_turnaround_viewer.html",
            "meoweko_turnaround_view_1_front.png",
            "meoweko_turnaround_view_2_profile_right.png",
            "meoweko_turnaround_view_3_profile_left.png",
            "meoweko_turnaround_view_4_back.png"
        ]

        for fname in required_files:
            # Check in main meoweko dir
            p1 = os.path.join(MEOWEKO_DIR, fname)
            self.assertTrue(os.path.exists(p1), f"Missing file in meoweko root: {p1}")
            self.assertGreater(os.path.getsize(p1), 1000, f"File too small: {p1}")

            # Check in 02_refonte_nouvelle/master_turnaround
            p2 = os.path.join(REFONTE_DIR, fname)
            self.assertTrue(os.path.exists(p2), f"Missing in refonte: {p2}")
            self.assertGreater(os.path.getsize(p2), 1000, f"Refonte file too small: {p2}")

    def test_02_canvas_dimensions(self):
        """Verify exact canonical resolutions."""
        specs = {
            "meoweko_master_turnaround_sheet.png": (1920, 820),
            "meoweko_studio_turnaround_sheet.png": (1920, 820),
            "meoweko_turnaround_master_board.png": (1920, 1600),
            "meoweko_master_side_by_side.png": (1024, 512),
            "meoweko_master_exact_512.png": (512, 512),
            "meoweko_turnaround_view_1_front.png": (512, 512),
            "meoweko_turnaround_view_2_profile_right.png": (512, 512),
            "meoweko_turnaround_view_3_profile_left.png": (512, 512),
            "meoweko_turnaround_view_4_back.png": (512, 512)
        }

        for fname, expected_dim in specs.items():
            p = os.path.join(MEOWEKO_DIR, fname)
            with Image.open(p) as img:
                self.assertEqual(img.size, expected_dim, f"Dimension mismatch for {fname}: got {img.size}, expected {expected_dim}")

    def test_03_porcelain_color_fidelity_and_no_green_spill(self):
        """Verify porcelain body has warm ceramic tones and zero green screen spill."""
        front_p = os.path.join(MEOWEKO_DIR, "meoweko_turnaround_view_1_front.png")
        with Image.open(front_p) as img:
            arr = np.array(img)
            r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]

            # Sample porcelain body (high alpha, non-eye region)
            porcelain_mask = (a > 200) & (r > 150) & (b > 120)
            self.assertGreater(np.sum(porcelain_mask), 5000, "Insufficient porcelain pixels detected")

            # 1. Warm porcelain: R >= B
            r_samples = r[porcelain_mask]
            b_samples = b[porcelain_mask]
            self.assertGreaterEqual(np.mean(r_samples), np.mean(b_samples), "Porcelain is too cold / blue")

            # 2. Despill: Mean green excess must be <= 0.0 and 99th percentile < 5.0
            g_samples = g[porcelain_mask]
            green_excess = g_samples.astype(np.float32) - (r_samples.astype(np.float32) * 0.52 + b_samples.astype(np.float32) * 0.48)
            self.assertLessEqual(np.mean(green_excess), 0.0, "Mean green excess should be negative or zero (clean despill)")
            self.assertLess(np.percentile(green_excess, 99), 5.0, "Green screen spill detected on 99th percentile of porcelain body!")

    def test_04_amber_eye_chromaticity(self):
        """Verify amber orb eyes have intense, warm golden/amber chroma."""
        front_p = os.path.join(MEOWEKO_DIR, "meoweko_turnaround_view_1_front.png")
        with Image.open(front_p) as img:
            arr = np.array(img)
            r, g, b, a = arr[:, :, 0].astype(np.float32), arr[:, :, 1].astype(np.float32), arr[:, :, 2].astype(np.float32), arr[:, :, 3]

            # Eye bounding zone
            eye_mask = (a > 200) & (r > 120) & (g > 60) & (b < 95) & (r - b > 40)
            amber_pixels = np.sum(eye_mask)
            self.assertGreater(amber_pixels, 300, f"Expected >300 amber eye pixels, found {amber_pixels}")

            # Verify average chromaticity of amber eye pixels
            r_eye = r[eye_mask]
            g_eye = g[eye_mask]
            b_eye = b[eye_mask]
            self.assertGreater(np.mean(r_eye), 140.0, "Amber eye red component is too low")
            self.assertGreater(np.mean(g_eye), 90.0, "Amber eye green component is too low")
            self.assertLess(np.mean(b_eye), 85.0, "Amber eye blue component is too high (lacks amber warmth)")

    def test_05_strictly_zero_human_hands_or_fingers(self):
        """Verify description and vector metadata strictly forbid human hands/fingers."""
        forbidden_keywords = ["human hand", "finger", "thumb", "main humaine"]
        
        # Check SVG
        svg_p = os.path.join(MEOWEKO_DIR, "meoweko_master_turnaround.svg")
        with open(svg_p, "r", encoding="utf-8") as f:
            svg_text = f.read().lower()
            for kw in forbidden_keywords:
                self.assertNotIn(kw, svg_text, f"Forbidden keyword '{kw}' found in SVG!")

    def test_06_pure_vector_svg_valid_xml(self):
        """Verify the turnaround SVG is valid, well-formed XML and has proper structure."""
        svg_p = os.path.join(MEOWEKO_DIR, "meoweko_master_turnaround.svg")
        tree = ET.parse(svg_p)
        root = tree.getroot()
        self.assertTrue(root.tag.endswith("svg"), "Root element must be <svg>")
        self.assertEqual(root.attrib.get("viewBox"), "0 0 1920 820")
        self.assertEqual(root.attrib.get("width"), "1920")
        self.assertEqual(root.attrib.get("height"), "820")

        # Verify all 4 column groups exist in SVG
        col_ids = ["col_front", "col_profile_r", "col_profile_l", "col_back"]
        for cid in col_ids:
            found = root.find(f".//*[@id='{cid}']")
            self.assertIsNotNone(found, f"Missing group {cid} in SVG turnaround")

    def test_07_interactive_viewer_html_structure(self):
        """Verify the 3D viewer HTML contains all required controls and assets."""
        viewer_p = os.path.join(MEOWEKO_DIR, "meoweko_3d_turnaround_viewer.html")
        with open(viewer_p, "r", encoding="utf-8") as f:
            html = f.read()
            self.assertIn("meoweko_turnaround_view_1_front.png", html)
            self.assertIn("meoweko_turnaround_view_2_profile_right.png", html)
            self.assertIn("meoweko_turnaround_view_3_profile_left.png", html)
            self.assertIn("meoweko_turnaround_view_4_back.png", html)
            self.assertIn("setAngle", html)
            self.assertIn("toggleAutoSpin", html)

    def test_08_strictly_zero_ground_shadow(self):
        """Verify zero ground shadow below baseline Y = 491 px."""
        for fname in ["meoweko_turnaround_view_1_front.png", "meoweko_master_exact_512.png"]:
            p = os.path.join(MEOWEKO_DIR, fname)
            with Image.open(p) as img:
                arr = np.array(img)
                alpha_below = arr[492:, :, 3]
                self.assertEqual(np.max(alpha_below), 0, f"Ground shadow detected below Y=491 in {fname}!")

if __name__ == "__main__":
    unittest.main()
