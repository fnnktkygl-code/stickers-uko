#!/usr/bin/env python3
"""
Automated Visual & Mathematical Integrity Test Suite for AItuko Error 404 Animation.
Verifies all deliverables of state 04_error_404 strictly following user specifications:
1. Pure vector Lottie JSON (< 50 KB) with valid Bodymovin markers and zero floating card
2. Option Idéale feet kinematics (rot ±12°, dx ±8px, dy +22px) and grounded torso (dy=72px, base y~485..487px)
3. Diegetic visor telemetry (100% RED: '! !' in alert phase 2, 7-segment ERR in slump phase 4)
4. Zero human hands, zero fingers (strictly aerodynamic pods)
5. Authentic porcelain ceramic colors, strictly ZERO cyan during error (body and visor)
6. Strictly ZERO foreign foot assets / ZERO foot swapping (canonical components only)
7. Complete file delivery across assets, mascots, downloads, and brain directories
"""


import os
import re
import json
import unittest
import cv2
import numpy as np
from PIL import Image

WORKSPACE_DIR = "/Users/richard/Developer/Stickers Uko"


class TestAItukoError404Integrity(unittest.TestCase):

    def test_01_lottie_file_sizes_and_markers(self):
        """Verify that Lottie JSON is strictly < 50 KB, contains valid markers with exact timings, and correct layer ordering."""
        lottie_path = os.path.join(WORKSPACE_DIR, "assets/04_error_404/lottie.json")
        self.assertTrue(os.path.exists(lottie_path), f"Missing {lottie_path}")
        size_kb = os.path.getsize(lottie_path) / 1024.0
        self.assertLess(size_kb, 50.0, f"Error 404 Lottie size {size_kb:.2f} KB exceeds 50 KB limit")
        
        with open(lottie_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        self.assertIn("markers", data, "Missing markers in Error 404 Lottie")
        markers_dict = {m["cm"]: (m["tm"], m.get("dr", 0)) for m in data["markers"]}
        self.assertIn("error_intro", markers_dict)
        self.assertIn("error_slump_loop", markers_dict)
        self.assertIn("error_reboot", markers_dict)
        
        # Verify exact frame ranges: error_intro (0..34), error_slump_loop (35..74), error_reboot (75..119)
        self.assertEqual(markers_dict["error_intro"], (0, 35), "error_intro should span f=0..34 (dr=35)")
        self.assertEqual(markers_dict["error_slump_loop"], (35, 40), "error_slump_loop should span f=35..74 (dr=40)")
        self.assertEqual(markers_dict["error_reboot"], (75, 45), "error_reboot should span f=75..119 (dr=45)")

        layer_names = [l.get("nm", "") for l in data.get("layers", [])]
        self.assertTrue(any("ERR" in name or "Telemetry" in name for name in layer_names),
                        "Missing Red Visor Telemetry layer in Lottie layers")
        self.assertTrue(any("Foot" in name for name in layer_names),
                        "Missing Canonical Feet layers in Lottie layers")
        self.assertFalse(any("Floating" in name or "Badge" in name for name in layer_names),
                         "Floating 404 card layer must be completely removed from Lottie")

        # Verify Layer Stacking: Feet must render IN FRONT of Torso (i.e. foot layer index < torso layer index)
        foot_indices = [idx for idx, name in enumerate(layer_names) if "Foot" in name]
        torso_indices = [idx for idx, name in enumerate(layer_names) if "Torso" in name]
        self.assertTrue(len(foot_indices) > 0 and len(torso_indices) > 0)
        self.assertTrue(max(foot_indices) < min(torso_indices),
                        f"Canonical feet (indices {foot_indices}) must be composited in front of torso (indices {torso_indices})")

        # Verify Exact Seated Keyframes per Directive 1, 2, 4 (t=35 seated posture)
        layer_by_name = {l.get("nm", ""): l for l in data.get("layers", [])}
        
        # Torso seated pos = [256.0, 384.0, 0.0], sc = [106.0, 93.0, 100.0]
        torso_l = layer_by_name.get("Porcelain Torso Capsule", {})
        t_pos_kfs = {kf["t"]: kf["s"] for kf in torso_l.get("ks", {}).get("p", {}).get("k", []) if isinstance(kf, dict)}
        t_sc_kfs = {kf["t"]: kf["s"] for kf in torso_l.get("ks", {}).get("s", {}).get("k", []) if isinstance(kf, dict)}
        self.assertEqual(t_pos_kfs.get(35), [256.0, 384.0, 0.0], "Torso seated pos must be [256.0, 384.0, 0.0]")
        self.assertEqual(t_sc_kfs.get(35), [106.0, 93.0, 100.0], "Torso seated scale must be [106.0, 93.0, 100.0]")

        # Head seated pos = [256.0, 282.0, 0.0], rot = 3.6°
        head_l = layer_by_name.get("Porcelain Head Dome", {})
        h_pos_kfs = {kf["t"]: kf["s"] for kf in head_l.get("ks", {}).get("p", {}).get("k", []) if isinstance(kf, dict)}
        h_rot_kfs = {kf["t"]: kf["s"] for kf in head_l.get("ks", {}).get("r", {}).get("k", []) if isinstance(kf, dict)}
        self.assertEqual(h_pos_kfs.get(35), [256.0, 282.0, 0.0], "Head seated pos must be [256.0, 282.0, 0.0]")
        self.assertEqual(h_rot_kfs.get(35), [3.6], "Head seated rot must be 3.6°")

        # Left foot: rot = +12.0°, pos = [206.0, 470.0, 0.0], sc = [112.0, 88.0, 100.0]
        lf_l = layer_by_name.get("Left Foot Pod (Seated Flare)", {})
        lf_pos_kfs = {kf["t"]: kf["s"] for kf in lf_l.get("ks", {}).get("p", {}).get("k", []) if isinstance(kf, dict)}
        lf_rot_kfs = {kf["t"]: kf["s"] for kf in lf_l.get("ks", {}).get("r", {}).get("k", []) if isinstance(kf, dict)}
        lf_sc_kfs = {kf["t"]: kf["s"] for kf in lf_l.get("ks", {}).get("s", {}).get("k", []) if isinstance(kf, dict)}
        self.assertEqual(lf_pos_kfs.get(35), [206.0, 470.0, 0.0], "Left foot seated pos must be [206.0, 470.0, 0.0]")
        self.assertEqual(lf_rot_kfs.get(35), [12.0], "Left foot seated rot must be +12.0°")
        self.assertEqual(lf_sc_kfs.get(35), [112.0, 88.0, 100.0], "Left foot seated scale must be [112.0, 88.0, 100.0]")

        # Right foot: rot = -12.0°, pos = [306.0, 470.0, 0.0], sc = [112.0, 88.0, 100.0]
        rf_l = layer_by_name.get("Right Foot Pod (Seated Flare)", {})
        rf_pos_kfs = {kf["t"]: kf["s"] for kf in rf_l.get("ks", {}).get("p", {}).get("k", []) if isinstance(kf, dict)}
        rf_rot_kfs = {kf["t"]: kf["s"] for kf in rf_l.get("ks", {}).get("r", {}).get("k", []) if isinstance(kf, dict)}
        rf_sc_kfs = {kf["t"]: kf["s"] for kf in rf_l.get("ks", {}).get("s", {}).get("k", []) if isinstance(kf, dict)}
        self.assertEqual(rf_pos_kfs.get(35), [306.0, 470.0, 0.0], "Right foot seated pos must be [306.0, 470.0, 0.0]")
        self.assertEqual(rf_rot_kfs.get(35), [-12.0], "Right foot seated rot must be -12.0°")
        self.assertEqual(rf_sc_kfs.get(35), [112.0, 88.0, 100.0], "Right foot seated scale must be [112.0, 88.0, 100.0]")

    def test_02_slump_kinematics_and_ground_contact(self):
        """Verify canonical physical slump, head bow, winglet floor rest, and flared canonical feet."""
        sys_path = os.path.join(WORKSPACE_DIR, "scripts/build_flawless_aituko_error_404.py")
        import importlib.util
        spec = importlib.util.spec_from_file_location("error_module", sys_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        
        # Nominal float (frame 0)
        k0 = mod.get_error_404_kinematics(0)
        self.assertAlmostEqual(k0['dy_root'], 0.0, delta=0.5)
        self.assertAlmostEqual(k0['rot_head'], 0.0, delta=0.5)
        self.assertLess(k0['shadow_a'], 160)
        
        # Grounded slump (frame 55) — 100% Canonical Seated Posture
        k55 = mod.get_error_404_kinematics(55)
        self.assertGreaterEqual(k55['dy_root'], 65.0, "Torso should drop >= 65px in slump (firmly grounded on floor)")
        self.assertAlmostEqual(k55['rot_head'], 3.6, delta=0.5, msg="Head should bow forward ~3.6°")
        self.assertAlmostEqual(k55['rot_lpod'], 14.0, delta=2.0, msg="Left pod should rest flared at floor")
        self.assertAlmostEqual(k55['rot_rpod'], -14.0, delta=2.0, msg="Right pod should rest flared at floor")
        
        # Option Idéale feet specific checks per Directive 1
        self.assertEqual(k55['dx_lfoot'], -8.0, "Left foot should spread -8px outward when seated")
        self.assertEqual(k55['dx_rfoot'], 8.0, "Right foot should spread +8px outward when seated")
        self.assertGreater(k55['rot_lfoot'], 5.0, "Left foot rot must be > +5° (Option Idéale: +12°)")
        self.assertLess(k55['rot_rfoot'], -5.0, "Right foot rot must be < -5° (Option Idéale: -12°)")
        self.assertEqual(k55['rot_lfoot'], 12.0, "Left foot should tilt +12° (Option Idéale)")
        self.assertEqual(k55['rot_rfoot'], -12.0, "Right foot should tilt -12° (Option Idéale)")
        self.assertEqual(k55['scale_feet_x'], 1.12, "Feet scale_x should be 1.12 against the ground")
        self.assertEqual(k55['scale_feet_y'], 0.88, "Feet scale_y should be 0.88 against the ground")
        self.assertEqual(k55['dy_feet'], 22.0, "dy_feet should be 22px")
        
        self.assertAlmostEqual(k55['scale_torso_x'], 1.06, delta=0.01, msg="Torso scale_x should be 1.06 in seated slump")
        self.assertAlmostEqual(k55['scale_torso_y'], 0.93, delta=0.01, msg="Torso scale_y should be 0.93 in seated slump")
        self.assertGreaterEqual(k55['shadow_a'], 200, "Ground shadow should darken (contact occlusion >= 200)")
        # Direct pixel ground measurement: verify torso base touches floor plane y in [485..488]
        comps = mod.load_master_components()
        w_torso = mod.transform_rgba(comps['torso'], (256.0, 314.0), angle_deg=0.0,
                                     scale=(k55['scale_torso_x'], k55['scale_torso_y']), translate=(0.0, k55['dy_root']))
        ys_t, _ = np.where(w_torso[:, :, 3] > 10)
        self.assertTrue(485 <= ys_t.max() <= 488, f"Torso base bottom y={ys_t.max()} must sit squarely on floor plane [485..488]")

        # Loop bouclage (frame 119)
        k119 = mod.get_error_404_kinematics(119)
        self.assertAlmostEqual(k119['dy_root'], 0.0, delta=0.8)
        self.assertAlmostEqual(k119['rot_head'], 0.0, delta=0.5)

    def test_03_diegetic_visor_telemetry_timing(self):
        """Verify red exclamation marks '! !' in alert phase 2, red digital 7-segment ERR in slump phase 4, zero cyan during error."""
        sys_path = os.path.join(WORKSPACE_DIR, "scripts/build_flawless_aituko_error_404.py")
        import importlib.util
        spec = importlib.util.spec_from_file_location("error_module", sys_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        
        # Frame 0: Cyan eyes lit, ERR and Excl off
        k0 = mod.get_error_404_kinematics(0)
        self.assertEqual(k0['eye_opacity'], 1.0)
        self.assertEqual(k0['err_opacity'], 0.0)
        self.assertEqual(k0['excl_opacity'], 0.0)
        
        # Frame 25: Phase 2 Alert/Shock: Cyan eyes OFF, Red Alert '! !' lit (excl_opacity == 1.0)
        k25 = mod.get_error_404_kinematics(25)
        self.assertEqual(k25['eye_opacity'], 0.0, "Cyan eyes must be completely OFF during alert phase 2")
        self.assertEqual(k25['excl_opacity'], 1.0, "Red exclamation marks '! !' must be lit at frame 25")
        self.assertEqual(k25['err_opacity'], 0.0, "ERR must be off during alert phase 2")
        
        # Frame 55: Phase 4 Grounded slump: Cyan eyes OFF, Excl off, Red 7-segment ERR lit (> 0.8)
        k55 = mod.get_error_404_kinematics(55)
        self.assertEqual(k55['eye_opacity'], 0.0, "Cyan eyes must be completely OFF during error slump phase 4")
        self.assertEqual(k55['excl_opacity'], 0.0, "Exclamation marks must be off during slump phase 4")
        self.assertGreater(k55['err_opacity'], 0.8, "Red digital 7-segment ERR must be lit at frame 55")
        
        # Frame 82: Phase 5 Reignited cyan eyes, red telemetry extinguishes
        k82 = mod.get_error_404_kinematics(82)
        self.assertGreater(k82['eye_opacity'], 0.9, "Cheerful cyan arch eyes must reignite at reboot")
        self.assertEqual(k82['err_opacity'], 0.0, "Red ERR must extinguish upon reboot")
        self.assertEqual(k82['excl_opacity'], 0.0, "Red ! ! must be extinguished upon reboot")
        
        # Frame 105: Phase 6 Conscious settle blink
        k105 = mod.get_error_404_kinematics(105)
        self.assertLessEqual(k105['scale_eye_y'], 0.15, "Eyes should blink closed at frame 105")

    def test_04_zero_human_hands_and_fingers(self):
        """Strict anatomical check: pods have zero hand/finger morphology."""
        sys_path = os.path.join(WORKSPACE_DIR, "scripts/build_flawless_aituko_idle.py")
        import importlib.util
        spec = importlib.util.spec_from_file_location("idle_module", sys_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        comps = mod.load_master_components()
        
        for pod_name in ['lpod', 'rpod']:
            pod_rgba = comps[pod_name]
            alpha = pod_rgba[:, :, 3]
            contours, _ = cv2.findContours((alpha > 50).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            self.assertEqual(len(contours), 1, f"{pod_name} must be a single cohesive aerodynamic pod")
            cnt = contours[0]
            hull = cv2.convexHull(cnt, returnPoints=False)
            defects = cv2.convexityDefects(cnt, hull)
            deep_defects = 0
            if defects is not None:
                for i in range(defects.shape[0]):
                    d = (defects[i, 0, 3] if defects.ndim == 3 else defects[i, 3]) / 256.0
                    if d > 8.0:
                        deep_defects += 1
            self.assertEqual(deep_defects, 0, f"{pod_name} has indentation defects reminiscent of human fingers!")

    def test_05_porcelain_colors_and_zero_cyan_during_error(self):
        """Verify warm porcelain ceramic shading and strict absence of cyan anywhere across all error frames and static posters."""
        sys_path = os.path.join(WORKSPACE_DIR, "scripts/build_flawless_aituko_error_404.py")
        import importlib.util
        spec = importlib.util.spec_from_file_location("error_module", sys_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        comps = mod.load_master_components()
        
        # Test across entire error sequence: f=25 (alert ! !), f=30 (touchdown), f=55 (slump ERR), f=70 (slump loop)
        for test_f in [25, 30, 55, 70]:
            frame_img = mod.render_error_404_frame(test_f, comps, backdrop=None)
            arr = np.array(frame_img)
            hsv_all = cv2.cvtColor(arr[:, :, :3], cv2.COLOR_RGB2HSV)
            cyan_mask = (hsv_all[:, :, 0] >= 80) & (hsv_all[:, :, 0] <= 105) & (hsv_all[:, :, 1] >= 100) & (hsv_all[:, :, 2] >= 100) & (arr[:, :, 3] > 100)
            cyan_count = np.sum(cyan_mask)
            self.assertEqual(cyan_count, 0, f"Detected {cyan_count} cyan pixels in error frame {test_f}! Error must be 100% red with zero cyan.")

        # Also check hero static poster files on disk
        for p_name in [
            "assets/04_error_404/static.png",
            "mascots/aituko/aituko_error_404_static.png",
            "mascots/aituko/assets/04_error_404/static.png",
            "aituko/assets/04_error_404/static.png",
            "assets/04_error_404/keyframe_02_shock_stutter.png",
            "assets/04_error_404/keyframe_03_grounded_slump_err.png"
        ]:
            fp = os.path.join(WORKSPACE_DIR, p_name)
            if os.path.exists(fp):
                arr = np.array(Image.open(fp).convert("RGBA"))
                hsv = cv2.cvtColor(arr[:, :, :3], cv2.COLOR_RGB2HSV)
                cyan_mask = (hsv[:, :, 0] >= 80) & (hsv[:, :, 0] <= 105) & (hsv[:, :, 1] >= 100) & (hsv[:, :, 2] >= 100) & (arr[:, :, 3] > 100)
                cyan_count = np.sum(cyan_mask)
                self.assertEqual(cyan_count, 0, f"Detected {cyan_count} cyan pixels in on-disk asset {p_name}!")

    def test_06_deliverables_completeness(self):
        """Verify that all production formats and deliverables are generated and exist across assets, mascots, aituko, and downloads."""
        output_dir = os.path.join(WORKSPACE_DIR, "assets/04_error_404")
        expected_files = [
            "lottie.json",
            "animated.svg",
            "animated.webp",
            "animated.png",
            "animated.gif",
            "animated_dark.gif",
            "animated_green.gif",
            "looped_video.mp4",
            "static.png",
            "static.webp",
            "aituko_error_404_master_board.png",
            "aituko_error_404_studio_trichroma_board.png",
            "aituko_error_404_bundle.zip"
        ]
        for ef in expected_files:
            fp = os.path.join(output_dir, ef)
            self.assertTrue(os.path.exists(fp), f"Missing production deliverable in assets/04_error_404: {fp}")

        # Check mascots/aituko deliverables
        mascots_dir = os.path.join(WORKSPACE_DIR, "mascots/aituko")
        for mf in ["aituko_error_404_vector.json", "aituko_error_404_animated.svg", "aituko_error_404.webp", "aituko_error_404.mp4", "aituko_error_404_static.png"]:
            fp = os.path.join(mascots_dir, mf)
            self.assertTrue(os.path.exists(fp), f"Missing deliverable in mascots/aituko: {fp}")

        # Check aituko/assets/04_error_404 deliverables and confirm zero legacy floating badge
        aituko_dir = os.path.join(WORKSPACE_DIR, "aituko/assets/04_error_404")
        aituko_lottie = os.path.join(aituko_dir, "lottie.json")
        self.assertTrue(os.path.exists(aituko_lottie), f"Missing aituko/assets/04_error_404/lottie.json")
        with open(aituko_lottie, "r", encoding="utf-8") as f:
            a_data = json.load(f)
        a_layer_names = [l.get("nm", "") for l in a_data.get("layers", [])]
        self.assertFalse(any("Badge" in name or "Card" in name for name in a_layer_names),
                         "aituko/assets/04_error_404/lottie.json must not contain legacy floating badge/card")
        self.assertTrue(any("ERR" in name or "Telemetry" in name for name in a_layer_names),
                         "aituko/assets/04_error_404/lottie.json must contain Red Visor Telemetry")

        # Check mascots/aituko/assets/04_error_404 deliverables and confirm zero legacy floating badge
        mascots_assets_dir = os.path.join(WORKSPACE_DIR, "mascots/aituko/assets/04_error_404")
        self.assertTrue(os.path.exists(mascots_assets_dir), f"Missing {mascots_assets_dir}")
        for mf in ["lottie.json", "animated.svg", "animated.webp", "static.png", "bundle_aituko_04_error_404.zip"]:
            fp = os.path.join(mascots_assets_dir, mf)
            self.assertTrue(os.path.exists(fp), f"Missing deliverable in mascots/aituko/assets/04_error_404: {fp}")
        with open(os.path.join(mascots_assets_dir, "lottie.json"), "r", encoding="utf-8") as f:
            ma_data = json.load(f)
        ma_layer_names = [l.get("nm", "") for l in ma_data.get("layers", [])]
        self.assertFalse(any("Badge" in name or "Card" in name for name in ma_layer_names),
                         "mascots/aituko/assets/04_error_404/lottie.json must not contain legacy floating badge/card")
        self.assertTrue(any("ERR" in name or "Telemetry" in name for name in ma_layer_names),
                         "mascots/aituko/assets/04_error_404/lottie.json must contain Red Visor Telemetry")

        # Check downloads
        self.assertTrue(os.path.exists(os.path.join(WORKSPACE_DIR, "downloads/aituko_error_404_bundle.zip")),
                        "Missing downloads/aituko_error_404_bundle.zip")

    def test_07_zero_external_foot_assets_and_zero_floating_card(self):
        """Verify strict absence of external foot texture files and floating card assets in code."""
        sys_path = os.path.join(WORKSPACE_DIR, "scripts/build_flawless_aituko_error_404.py")
        with open(sys_path, "r", encoding="utf-8") as f:
            code = f.read()

        forbidden_symbols = [
            "LF_SEATED_PATH",
            "RF_SEATED_PATH",
            "_get_seated_feet_assets",
            "CARD_404_PATH",
            "_get_card_404_asset",
            "aituko_seated_lfoot.png",
            "aituko_seated_rfoot.png",
            "aituko_error_404_card.png"
        ]
        for sym in forbidden_symbols:
            self.assertNotIn(sym, code, f"Forbidden asset or symbol '{sym}' found in build script! Must use canonical components only.")

    def test_08_svg_transforms_and_zero_pod_or_head_drift(self):
        """Verify SVG CSS animations: zero double-origin translation on pods, zero sideways rotation drift on head."""
        svg_path = os.path.join(WORKSPACE_DIR, "assets/04_error_404/animated.svg")
        self.assertTrue(os.path.exists(svg_path), f"Missing {svg_path}")
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()

        # Validate transform-origins
        self.assertIn(".anim-lpod { animation: leftPodMotion 4s ease-in-out infinite; transform-origin: 158px 268px; }", svg_content)
        self.assertIn(".anim-rpod { animation: rightPodMotion 4s ease-in-out infinite; transform-origin: 354px 268px; }", svg_content)
        self.assertIn(".anim-head { animation: headMotion 4s ease-in-out infinite; transform-origin: 256px 204px; }", svg_content)
        self.assertIn(".anim-shadow { animation: shadowMotion 4s ease-in-out infinite; transform-origin: 256px 488px; }", svg_content)
        self.assertIn(".anim-root { animation: rootMotion 4s ease-in-out infinite; transform-origin: 256px 312px; }", svg_content)
        self.assertIn(".anim-lfoot { animation: leftFootMotion 4s ease-in-out infinite; transform-origin: 214px 448px; }", svg_content)
        self.assertIn(".anim-rfoot { animation: rightFootMotion 4s ease-in-out infinite; transform-origin: 298px 448px; }", svg_content)

        # Validate keyframes delta translations (no double-origin translation)
        self.assertIn("29.2% { transform: translate(-4px, 70px) rotate(14deg); }", svg_content)
        self.assertIn("29.2% { transform: translate(4px, 70px) rotate(-14deg); }", svg_content)
        self.assertIn("29.2% { transform: translateY(78px) rotate(3.6deg); }", svg_content)
        self.assertIn("29.2% { transform: translate(-8px, 22px) rotate(12deg) scale(1.12, 0.88); }", svg_content)
        self.assertIn("29.2% { transform: translate(8px, 22px) rotate(-12deg) scale(1.12, 0.88); }", svg_content)

        # Validate layer ordering: feet must be placed AFTER torso in SVG DOM (rendered in front)
        pos_root = svg_content.find('class="anim-root"')
        pos_lfoot = svg_content.find('class="anim-lfoot"')
        pos_rfoot = svg_content.find('class="anim-rfoot"')
        self.assertTrue(pos_root > 0 and pos_lfoot > 0 and pos_rfoot > 0)
        self.assertTrue(pos_root < pos_lfoot and pos_root < pos_rfoot,
                        "Feet (<g class='anim-lfoot'> and <g class='anim-rfoot'>) must be rendered after torso (<g class='anim-root'>) in SVG DOM")

    def test_09_option_01_7seg_telemetry_and_geometry(self):
        """Verify Option 01: 7-Segments Classique Industriel ('E r r') in Lottie, SVG, and raster renderer."""
        # 1. Verify in Lottie JSON
        lottie_path = os.path.join(WORKSPACE_DIR, "assets/04_error_404/lottie.json")
        self.assertTrue(os.path.exists(lottie_path))
        with open(lottie_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        telemetry_layer = None
        for layer in data.get("layers", []):
            if "Telemetry" in layer.get("nm", "") or "ERR" in layer.get("nm", ""):
                telemetry_layer = layer
                break
        self.assertIsNotNone(telemetry_layer, "Missing telemetry layer in Lottie")
        
        # Check for Digital 7-Segment ERR shape group
        err_group = None
        for sh in telemetry_layer.get("shapes", []):
            if "7-Segment" in sh.get("nm", "") or "ERR" in sh.get("nm", ""):
                err_group = sh
                break
        self.assertIsNotNone(err_group, "Missing 7-Segment ERR shape group in Lottie telemetry layer")
        
        # Verify sub-groups: Ghost Segments, Active Red Segments, and Inner Highlights
        sub_names = [it.get("nm", "") for it in err_group.get("it", []) if it.get("ty") == "gr"]
        self.assertTrue(any("Ghost" in name for name in sub_names), "Missing Ghost Segments group in Lottie ERR group")
        self.assertTrue(any("Active" in name for name in sub_names), "Missing Active Red Segments group in Lottie ERR group")
        self.assertTrue(any("Highlight" in name for name in sub_names), "Missing Inner Highlights group in Lottie ERR group")
        
        # Verify segment shape counts: 12 ghost + 9 active = 21 segments total
        ghost_group = next(it for it in err_group["it"] if "Ghost" in it.get("nm", ""))
        active_group = next(it for it in err_group["it"] if "Active" in it.get("nm", ""))
        ghost_shapes = [it for it in ghost_group.get("it", []) if it.get("ty") == "sh"]
        active_shapes = [it for it in active_group.get("it", []) if it.get("ty") == "sh"]
        self.assertEqual(len(ghost_shapes), 12, f"Expected 12 ghost segments, found {len(ghost_shapes)}")
        self.assertEqual(len(active_shapes), 9, f"Expected 9 active segments, found {len(active_shapes)}")
        
        # Verify vertices are closed polygonal chamfered shapes (each having 4 or 6 vertices)
        for sh in ghost_shapes + active_shapes:
            verts = sh.get("ks", {}).get("k", {}).get("v", [])
            self.assertIn(len(verts), [4, 6], f"Segment shape {sh.get('nm')} must be a 4 or 6 vertex polygon")
            self.assertTrue(sh.get("ks", {}).get("k", {}).get("c", False), "Segment polygon must be closed")

        # Verify ghost fill and active fill colors
        fl_ghost = next(it for it in ghost_group.get("it", []) if it.get("ty") == "fl")
        self.assertAlmostEqual(fl_ghost["c"]["k"][0], 45/255.0, places=2)
        self.assertAlmostEqual(fl_ghost["c"]["k"][1], 14/255.0, places=2)
        self.assertAlmostEqual(fl_ghost["c"]["k"][2], 16/255.0, places=2)
        self.assertEqual(fl_ghost["o"]["k"], 35.0)

        fl_active = next(it for it in active_group.get("it", []) if it.get("ty") == "fl")
        self.assertEqual(fl_active["o"]["k"], 100.0)

        # Verify inner highlights: exactly 9 stroke paths
        hl_group = next(it for it in err_group["it"] if "Highlight" in it.get("nm", ""))
        hl_shapes = [it for it in hl_group.get("it", []) if it.get("ty") == "sh"]
        self.assertEqual(len(hl_shapes), 9, f"Expected 9 inner highlight shapes, found {len(hl_shapes)}")

        # Test orientation of highlights: 4 vertical highlights (E_e, E_f, r1_e, r2_e) and 5 horizontal (E_a, E_d, E_g, r1_g, r2_g)
        vert_hl = 0
        horiz_hl = 0
        for sh in hl_shapes:
            verts = sh.get("ks", {}).get("k", {}).get("v", [])
            self.assertEqual(len(verts), 2, "Highlight stroke must have exactly 2 vertices (a line segment)")
            dx = abs(verts[1][0] - verts[0][0])
            dy = abs(verts[1][1] - verts[0][1])
            if dy > 8.0 and dx < 1.0:
                vert_hl += 1
            elif dx > 8.0 and dy < 1.0:
                horiz_hl += 1
        self.assertEqual(vert_hl, 4, f"Expected 4 vertical highlight lines (E_e, E_f, r1_e, r2_e), found {vert_hl}")
        self.assertEqual(horiz_hl, 5, f"Expected 5 horizontal highlight lines (E_a, E_d, E_g, r1_g, r2_g), found {horiz_hl}")
            
        # 2. Verify in Animated SVG
        svg_path = os.path.join(WORKSPACE_DIR, "assets/04_error_404/animated.svg")
        self.assertTrue(os.path.exists(svg_path))
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
        self.assertIn("#2D0E10", svg_content, "SVG must contain ghost segments color #2D0E10")
        self.assertIn("#FF3B30", svg_content, "SVG must contain active cyber red color #FF3B30")
        self.assertIn("#FFD0D0", svg_content, "SVG must contain inner highlight color #FFD0D0")
        self.assertIn('class="anim-err"', svg_content, "SVG must contain anim-err group")

        anim_err_match = re.search(r'<g class="anim-err".*?</g>', svg_content, re.DOTALL)
        self.assertIsNotNone(anim_err_match, "Missing anim-err group in animated.svg")
        hl_path_match = re.search(r'<path d="([^"]+)"[^>]*stroke="#FFD0D0"', anim_err_match.group(0))
        self.assertIsNotNone(hl_path_match, "Missing inner highlights path with stroke #FFD0D0 in anim-err SVG group")
        err_hls = re.findall(r"M\s+([\d.]+)\s+([\d.]+)\s+L\s+([\d.]+)\s+([\d.]+)", hl_path_match.group(1))
        self.assertEqual(len(err_hls), 9, f"Expected 9 highlight paths in anim-err SVG group, found {len(err_hls)}")
        svg_vert_hl = sum(1 for x1, y1, x2, y2 in err_hls if abs(float(y2) - float(y1)) > 8.0 and abs(float(x2) - float(x1)) < 1.0)
        svg_horiz_hl = sum(1 for x1, y1, x2, y2 in err_hls if abs(float(x2) - float(x1)) > 8.0 and abs(float(y2) - float(y1)) < 1.0)
        self.assertEqual(svg_vert_hl, 4, f"Expected 4 vertical SVG highlights in anim-err, found {svg_vert_hl}")
        self.assertEqual(svg_horiz_hl, 5, f"Expected 5 horizontal SVG highlights in anim-err, found {svg_horiz_hl}")
        
        # 3. Verify in Frame Renderer
        sys_path = os.path.join(WORKSPACE_DIR, "scripts/build_flawless_aituko_error_404.py")
        import importlib.util
        spec = importlib.util.spec_from_file_location("error_mod", sys_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        comps = mod.load_master_components()

        # A. Verify glyph drawing in visor coordinates y in [105, 138]
        from PIL import ImageDraw
        test_visor_layer = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        dv = ImageDraw.Draw(test_visor_layer)
        e_segs = {'a': True, 'f': True, 'g': True, 'e': True, 'd': True}
        r_segs = {'e': True, 'g': True}
        mod.draw_7seg_glyph(dv, e_segs, 214, 105, w=20, h=32, sw=3.8, g=1.0)
        mod.draw_7seg_glyph(dv, r_segs, 244, 105, w=20, h=32, sw=3.8, g=1.0)
        mod.draw_7seg_glyph(dv, r_segs, 274, 105, w=20, h=32, sw=3.8, g=1.0)
        bbox = test_visor_layer.getbbox()
        self.assertEqual(bbox, (214, 105, 295, 138), f"Glyphs must span exactly y in [105, 138], found {bbox}")

        # B. Verify slumped frame f=55 on canvas
        f55_img = mod.render_error_404_frame(55, comps)
        arr = np.array(f55_img)
        
        # Red pixels on slumped head visor (y in [180, 222], x in [210, 295])
        red_mask = (arr[:, :, 0] > 200) & (arr[:, :, 1] < 100) & (arr[:, :, 2] < 100)
        ys_red, xs_red = np.where(red_mask)
        self.assertGreater(len(ys_red), 50, "Frame 55 must contain active glowing red 7-segment pixels")
        self.assertTrue(180 <= ys_red.min() and ys_red.max() <= 222,
                        f"Red telemetry y range [{ys_red.min()}, {ys_red.max()}] must be on slumped visor [180, 222]")
        self.assertTrue(210 <= xs_red.min() and xs_red.max() <= 295,
                        f"Red telemetry x range [{xs_red.min()}, {xs_red.max()}] must be within visor width [210, 295]")

        # Ghost dark pixels (R in [25, 65], G < 25, B < 25) around unlit segments
        crop = arr[180:222, 210:295]
        ghost_mask = (crop[:, :, 0] >= 25) & (crop[:, :, 0] <= 65) & (crop[:, :, 1] < 25) & (crop[:, :, 2] < 25)
        self.assertGreater(np.sum(ghost_mask), 10, "Frame 55 must contain unlit ghost segment pixels (#2D0E10)")


if __name__ == "__main__":
    unittest.main()
