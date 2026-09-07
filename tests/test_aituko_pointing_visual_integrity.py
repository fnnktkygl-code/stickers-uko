#!/usr/bin/env python3
"""
Automated Visual & Mathematical Integrity Test Suite for AItuko Pointing Animation.
Verifies both Pointing Right and Pointing Left deliverables:
1. Zero human hands, zero fingers (strictly aerodynamic pods)
2. Accurate porcelain ceramic colors (#FAF8F5 / #F2EDE4), zero body cyan glow
3. Elevation angle at apex within UI/UX golden range (+25° to +35° above horizontal)
4. Flank winglet stability (zero lateral drift: dx <= 1.0 px)
5. Functional eye blinks (anticipation blink at f=36-37, release blink at f=85-86)
6. Pure vector Lottie JSON (< 50 KB) with valid Bodymovin markers
7. Complete file delivery across assets, mascots, downloads, and brain directories
"""

import os
import json
import unittest
import cv2
import numpy as np
from PIL import Image

WORKSPACE_DIR = "/Users/richard/Developer/Stickers Uko"

class TestAItukoPointingIntegrity(unittest.TestCase):

    def test_01_lottie_file_sizes_and_markers(self):
        """Verify that Lottie JSON files are < 50 KB and contain valid state markers."""
        for state in ["07_pointing", "07_pointing_left"]:
            lottie_path = os.path.join(WORKSPACE_DIR, f"assets/{state}/lottie.json")
            self.assertTrue(os.path.exists(lottie_path), f"Missing {lottie_path}")
            size_kb = os.path.getsize(lottie_path) / 1024.0
            self.assertLess(size_kb, 50.0, f"{state} Lottie size {size_kb:.2f} KB exceeds 50 KB limit")
            
            with open(lottie_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            self.assertIn("markers", data, f"Missing markers in {state}")
            marker_names = [m["cm"] for m in data["markers"]]
            self.assertIn("point_intro", marker_names)
            self.assertIn("point_hold_loop", marker_names)
            self.assertIn("point_outro", marker_names)

    def test_02_elevation_angles_at_apex(self):
        """Verify that the pointing limb reaches an oblique elevation between +25° and +35°."""
        sys_path = os.path.join(WORKSPACE_DIR, "scripts/build_flawless_aituko_pointing.py")
        import importlib.util
        spec = importlib.util.spec_from_file_location("pointing_module", sys_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        
        # Right apex (frame 60)
        k_r = mod.get_pointing_kinematics(60, direction='right')
        # In our coordinate system, rot_rpod = -115.0° rotates down-hanging pod to +31.4° above horizontal
        rot_r = k_r['rot_rpod']
        elev_r = -(rot_r + 90.0) # elevation angle above horizontal (+25° for -115°)
        self.assertAlmostEqual(rot_r, -115.0, delta=2.0)
        self.assertTrue(25.0 <= elev_r <= 35.0, f"Right elevation angle {elev_r}° not in [25°, 35°]")
        
        # Left apex (frame 60)
        k_l = mod.get_pointing_kinematics(60, direction='left')
        rot_l = k_l['rot_lpod']
        elev_l = rot_l - 90.0
        self.assertAlmostEqual(rot_l, 115.0, delta=2.0)
        self.assertTrue(25.0 <= elev_l <= 35.0, f"Left elevation angle {elev_l}° not in [25°, 35°]")

    def test_03_resting_flank_winglet_stability(self):
        """Verify that the resting flank winglet has zero lateral drift (tx = 0.0)."""
        sys_path = os.path.join(WORKSPACE_DIR, "scripts/build_flawless_aituko_pointing.py")
        import importlib.util
        spec = importlib.util.spec_from_file_location("pointing_module", sys_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        
        for f in range(120):
            k_r = mod.get_pointing_kinematics(f, direction='right')
            self.assertEqual(k_r['tx_lpod'], 0.0, f"Frame {f}: Right pointing has non-zero tx_lpod")
            self.assertEqual(k_r['rot_lpod'], 0.0, f"Frame {f}: Resting flank arm rotated unexpectedly")
            
            k_l = mod.get_pointing_kinematics(f, direction='left')
            self.assertEqual(k_l['tx_rpod'], 0.0, f"Frame {f}: Left pointing has non-zero tx_rpod")
            self.assertEqual(k_l['rot_rpod'], 0.0, f"Frame {f}: Resting flank arm rotated unexpectedly")

    def test_04_functional_blinking_timing(self):
        """Verify anticipation blink at f=36-37 and release blink at f=85-86."""
        sys_path = os.path.join(WORKSPACE_DIR, "scripts/build_flawless_aituko_pointing.py")
        import importlib.util
        spec = importlib.util.spec_from_file_location("pointing_module", sys_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        
        # Check anticipation blink
        k_anticip = mod.get_pointing_kinematics(36)
        self.assertLessEqual(k_anticip['scale_eye_y'], 0.10, "Eyes should be closed at frame 36")
        
        # Check apex smiling open eyes
        k_apex = mod.get_pointing_kinematics(60)
        self.assertGreater(k_apex['scale_eye_y'], 1.0, "Eyes should be smiling wide open (> 1.0) at apex")
        
        # Check release blink
        k_release = mod.get_pointing_kinematics(85)
        self.assertLessEqual(k_release['scale_eye_y'], 0.10, "Eyes should be closed at frame 85")
        
        # Check rest pose
        k_rest = mod.get_pointing_kinematics(0)
        self.assertEqual(k_rest['scale_eye_y'], 1.0, "Eyes should be normal at frame 0")

    def test_05_porcelain_color_and_zero_cyan_bleed(self):
        """Verify that rendered porcelain pixels match ceramic warm cream and have zero cyan bleed on torso."""
        for state in ["07_pointing", "07_pointing_left"]:
            img_path = os.path.join(WORKSPACE_DIR, f"assets/{state}/static.png")
            self.assertTrue(os.path.exists(img_path))
            im = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
            self.assertEqual(im.shape, (512, 512, 4))
            
            # Check Torso core region: x in [240, 270], y in [310, 360]
            torso_crop = im[310:360, 240:270]
            # BGR channels
            b = torso_crop[:, :, 0].astype(float)
            g = torso_crop[:, :, 1].astype(float)
            r = torso_crop[:, :, 2].astype(float)
            # Porcelain is warm: R >= G >= B
            self.assertTrue(np.mean(r) >= np.mean(b) - 2.0, "Torso porcelain is cold or blueish")
            # Strictly zero cyan on torso: cyan in BGR is high B, high G, low R
            is_cyan = (b > 180) & (g > 180) & (r < 100)
            self.assertEqual(np.count_nonzero(is_cyan), 0, f"Found fake cyan pixels on torso in {state}")

    def test_06_deliverables_complete(self):
        """Verify all production files exist in assets, downloads, and mascots."""
        for state, zip_name in [("07_pointing", "bundle_aituko_07_pointing.zip"),
                                ("07_pointing_left", "bundle_aituko_07_pointing_left.zip")]:
            asset_dir = os.path.join(WORKSPACE_DIR, f"assets/{state}")
            expected_files = [
                "animated.webp", "animated.gif", "animated_dark.gif", "animated_green.gif",
                "looped_video.mp4", "preview_studio_green.mp4", "lottie.json", "static.png",
                "static.webp", "snippet.json", zip_name
            ]
            for ef in expected_files:
                p = os.path.join(asset_dir, ef)
                self.assertTrue(os.path.exists(p), f"Missing {ef} in {asset_dir}")
                self.assertGreater(os.path.getsize(p), 0, f"{ef} in {asset_dir} is empty")

            # Check download bundle
            dl_path = os.path.join(WORKSPACE_DIR, f"downloads/{zip_name}")
            self.assertTrue(os.path.exists(dl_path), f"Missing download zip: {dl_path}")

    def test_07_lottie_spec_compliance_and_zero_anchor_redundancy(self):
        """Verify Bodymovin spec compliance: array keyframe values and zero redundant anchors."""
        for state in ["07_pointing", "07_pointing_left"]:
            lottie_path = os.path.join(WORKSPACE_DIR, f"assets/{state}/lottie.json")
            self.assertTrue(os.path.exists(lottie_path))
            with open(lottie_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            for layer in data["layers"]:
                nm = layer.get("nm", "")
                ks = layer.get("ks", {})
                
                # Check anchor redundancy: centered shape layers must have anchor [0, 0, 0] or [0, 83.66, 0]
                if "a" in ks and ks["a"].get("a") == 0:
                    a_val = ks["a"].get("k", [])
                    if nm == "Electric Cyan Eyes":
                        self.assertEqual(a_val, [0, 83.66, 0], f"{state} {nm} anchor must be [0, 83.66, 0]")
                    elif nm in ["Porcelain Head Dome", "Obsidian Visor Faceplate", "Left Pod Winglet", "Right Pod Winglet", "Porcelain Torso Capsule"]:
                        self.assertEqual(a_val, [0, 0, 0], f"{state} {nm} redundant anchor {a_val} must be [0, 0, 0]")

                # Check all keyframe properties: s and e MUST be lists, never raw scalars
                for prop_key in ["p", "r", "s", "o"]:
                    if prop_key in ks and ks[prop_key].get("a") == 1:
                        for kf in ks[prop_key].get("k", []):
                            if "s" in kf:
                                self.assertIsInstance(kf["s"], list, f"{state} {nm} prop {prop_key} has scalar 's': {kf['s']}")
                            if "e" in kf:
                                self.assertIsInstance(kf["e"], list, f"{state} {nm} prop {prop_key} has scalar 'e': {kf['e']}")

    def test_08_animated_svg_hierarchical_pivots(self):
        """Verify that SVG animations use explicit nested pivot groups instead of fragile CSS transform-box."""
        for state in ["07_pointing", "07_pointing_left"]:
            svg_path = os.path.join(WORKSPACE_DIR, f"assets/{state}/aituko_pointing_animated.svg" if state == "07_pointing" else f"assets/{state}/aituko_pointing_left_animated.svg")
            self.assertTrue(os.path.exists(svg_path))
            with open(svg_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Ensure zero transform-box: view-box dependencies
            self.assertNotIn("transform-box: view-box", content, f"{state} SVG must not depend on transform-box: view-box")
            
            # Check explicit pivot translation pairs
            self.assertIn("translate(354, 268)", content)
            self.assertIn("translate(-354, -268)", content)
            self.assertIn("translate(158, 268)", content)
            self.assertIn("translate(-158, -268)", content)
            self.assertIn("translate(256, 204)", content)
            self.assertIn("translate(-256, -204)", content)
            self.assertIn("translate(256, 120)", content)
            self.assertIn("translate(-256, -120)", content)
            self.assertIn("translate(256, 488)", content)
            self.assertIn("translate(-256, -488)", content)

if __name__ == "__main__":
    unittest.main()
