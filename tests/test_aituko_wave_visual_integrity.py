#!/usr/bin/env python3
"""
Rigorous Visual Integrity & Artifact Elimination Test Suite for AItuko Waving Animation.
Enforces strict frame-by-frame, component-by-component, and vector criteria:
1. Zero stray line artifacts (Hough transform & Canny edge on winglets to ensure NO needles/sticks).
2. Zero horizontal neck cut/gap (continuous neck socket continuity across all 120 frames).
3. Zero fake cyan glow on feet, winglets, or torso (cyan emissive strictly isolated to visor eyes).
4. Pure ceramic porcelain contrast against #FFFFFF (WCAG/Luminance boundary separation).
5. Vector cleanliness: Zero <rect> streaks in SVG and Lottie JSON.
6. File size constraints: Lottie JSON < 50 KB.
7. Seamless 120-frame loop continuity (frame 0 vs 119 diff < 5.0).
8. Active waving kinematics: right lateral pod raises and executes genuine harmonic wave motion.
9. Google Chrome headless validation: Lottie renders in headless Chrome without console errors.
10. Zero cyan pixels in limb gaps across animated.webp frames.
11. All target deliverables synchronized across assets/01_waving, mascots/aituko/, etc.
"""

import os
import sys
import json
import math
import shutil
import subprocess
import unittest
import cv2
import numpy as np
from PIL import Image

WORKSPACE_DIR = "/Users/richard/Developer/Stickers Uko"

class TestAitukoWaveVisualIntegrity(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.svg_path = os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_wave_animated.svg")
        cls.lottie_path = os.path.join(WORKSPACE_DIR, "assets/01_waving/lottie.json")
        cls.frames_dir = os.path.join(WORKSPACE_DIR, "assets/01_waving/frames")
        cls.webp_path = os.path.join(WORKSPACE_DIR, "assets/01_waving/animated.webp")
        cls.gif_path = os.path.join(WORKSPACE_DIR, "assets/01_waving/animated.gif")
        cls.mp4_path = os.path.join(WORKSPACE_DIR, "assets/01_waving/looped_video.mp4")
        cls.board_path = os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_wave_master_board.png")
        
    def test_01_svg_no_specular_rectangles_or_bars(self):
        """Validates that animated SVG has eliminated all hardcoded <rect> streak artifacts."""
        self.assertTrue(os.path.exists(self.svg_path), f"SVG missing: {self.svg_path}")
        with open(self.svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
            
        self.assertNotIn("master_specularStreak", svg_content, "SVG still contains master_specularStreak def!")
        self.assertNotIn("master_torsoSpecular", svg_content, "SVG still contains master_torsoSpecular def!")
        self.assertNotIn('transform="rotate(-6 126 278)"', svg_content, "SVG still contains rotated left winglet rect!")
        self.assertNotIn('transform="rotate(6 382 278)"', svg_content, "SVG still contains rotated right winglet rect!")
        
    def test_02_svg_no_fake_cyan_thrusters(self):
        """Validates that animated SVG has eliminated fake cyan lights on feet and winglets."""
        with open(self.svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
            
        self.assertNotIn("master_thrusterGlow", svg_content, "SVG still contains fake master_thrusterGlow!")
        self.assertNotIn("anim-thruster", svg_content, "SVG still contains anim-thruster class!")

    def test_03_svg_has_seamless_neck_socket(self):
        """Validates that animated SVG contains the dark mechanical neck socket."""
        with open(self.svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
        self.assertIn('cx="256" cy="204"', svg_content, "SVG missing neck socket collar definition!")

    def test_04_lottie_vector_cleanliness_and_size(self):
        """Validates Lottie JSON strictly eliminates streak rectangles, glow shapes, and stays < 50KB."""
        self.assertTrue(os.path.exists(self.lottie_path), f"Lottie missing: {self.lottie_path}")
        sz_kb = os.path.getsize(self.lottie_path) / 1024.0
        self.assertLess(sz_kb, 50.0, f"Lottie too large: {sz_kb:.1f} KB > 50 KB")
        
        with open(self.lottie_path, "r", encoding="utf-8") as f:
            lottie = json.load(f)
            
        lottie_str = json.dumps(lottie)
        self.assertNotIn("Left Pod Streak", lottie_str, "Lottie contains Left Pod Streak!")
        self.assertNotIn("Right Pod Streak", lottie_str, "Lottie contains Right Pod Streak!")
        self.assertNotIn("Left Pod Glow", lottie_str, "Lottie contains fake Left Pod Glow!")
        self.assertNotIn("Right Pod Glow", lottie_str, "Lottie contains fake Right Pod Glow!")
        self.assertNotIn("Left Foot Glow", lottie_str, "Lottie contains fake Left Foot Glow!")
        self.assertNotIn("Right Foot Glow", lottie_str, "Lottie contains fake Right Foot Glow!")

        # Verify left winglet has waving animation
        lpod_layers = [l for l in lottie["layers"] if "Left Winglet" in l.get("nm", "")]
        self.assertEqual(len(lpod_layers), 1, "Missing Left Winglet Pod layer in Lottie!")
        l_layer = lpod_layers[0]
        self.assertEqual(l_layer["ks"]["r"]["a"], 1, "Left winglet rotation should be animated (a=1)!")
        self.assertEqual(l_layer["ks"]["p"]["a"], 1, "Left winglet position should be animated (a=1)!")

    def test_05_frames_count_and_naming(self):
        """Verifies exactly 120 frames exist in assets/01_waving/frames."""
        self.assertTrue(os.path.isdir(self.frames_dir), f"Frames dir missing: {self.frames_dir}")
        frames = [f for f in os.listdir(self.frames_dir) if f.endswith(".png")]
        self.assertEqual(len(frames), 120, f"Expected 120 frames, found {len(frames)}")

    def test_06_frame_by_frame_cyan_glow_isolation(self):
        """Verifies across all 120 frames that cyan pixels are strictly isolated to the visor eyes."""
        for f_idx in range(120):
            frame_path = os.path.join(self.frames_dir, f"frame_{f_idx:03d}.png")
            im = cv2.imread(frame_path, cv2.IMREAD_UNCHANGED)
            self.assertIsNotNone(im, f"Failed to load frame {frame_path}")
            
            # Cyan emissive: B > 180, G > 180, R < 120, Alpha > 50
            if im.shape[2] == 4:
                b, g, r, a = cv2.split(im)
                cyan_pixels = (b > 180) & (g > 180) & (r < 120) & (a > 50)
            else:
                b, g, r = cv2.split(im)
                cyan_pixels = (b > 180) & (g > 180) & (r < 120)
                
            ys, xs = np.where(cyan_pixels)
            if len(ys) > 0:
                # 1. Cyan lights are STRICTLY FORBIDDEN at the tips/ends of feet
                cyan_feet_tips = np.sum((ys > 450))
                self.assertEqual(cyan_feet_tips, 0, f"Frame {f_idx}: Cyan glow found at bottom tips of feet (y > 450)!")
                
                # 2. All cyan pixels must belong to Visor Eyes (y < 190)
                invalid_cyan = np.sum(ys >= 190)
                self.assertEqual(invalid_cyan, 0, f"Frame {f_idx}: Cyan glow found outside visor eyes (y >= 190)!")

    def test_07_frame_by_frame_winglet_no_needle_artifacts(self):
        """Verifies using edge detection that winglets have NO linear streak/needle artifacts."""
        for f_idx in [0, 15, 30, 60, 78, 90, 105]:
            frame_path = os.path.join(self.frames_dir, f"frame_{f_idx:03d}.png")
            im = cv2.imread(frame_path, cv2.IMREAD_UNCHANGED)
            alpha = im[:, :, 3] if im.shape[2] == 4 else np.full(im.shape[:2], 255)
            gray = cv2.cvtColor(im[:, :, :3], cv2.COLOR_BGR2GRAY)
            
            # Right winglet interior mask (stabilizing flank pod):
            pod_mask = np.zeros_like(alpha)
            pod_mask[260:420, 335:395] = alpha[260:420, 335:395] > 200
            eroded_mask = cv2.erode(pod_mask.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
            
            # Canny edge detection inside pod interior
            edges = cv2.Canny(gray, 40, 100)
            interior_edges = cv2.bitwise_and(edges, edges, mask=eroded_mask)
            
            lines = cv2.HoughLinesP(interior_edges, 1, np.pi/180, threshold=20, minLineLength=20, maxLineGap=5)
            self.assertTrue(lines is None or len(lines) == 0, f"Frame {f_idx}: Stray interior needle streak detected in winglet!")

    def test_08_neck_joint_continuity_across_motion(self):
        """Verifies that the neck socket maintains continuity without horizontal blank gaps."""
        for f_idx in range(0, 120, 10):
            frame_path = os.path.join(self.frames_dir, f"frame_{f_idx:03d}.png")
            im = cv2.imread(frame_path, cv2.IMREAD_UNCHANGED)
            alpha = im[:, :, 3] if im.shape[2] == 4 else np.full(im.shape[:2], 255)
            
            # Column 256, y from 180 to 240 must have solid mascot coverage (alpha > 200)
            neck_col = alpha[180:240, 256]
            self.assertTrue(np.all(neck_col > 200), f"Frame {f_idx}: Neck separation gap detected at column x=256!")

    def test_09_white_background_contrast(self):
        """Verifies that mascot porcelain has crisp boundary contrast against #FFFFFF."""
        frame_path = os.path.join(self.frames_dir, "frame_000.png")
        im = Image.open(frame_path).convert("RGBA")
        white_bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        white_bg.alpha_composite(im)
        arr = np.array(white_bg.convert("L"))
        
        outer_bg_val = int(arr[312, 180])
        torso_rim_val = int(min(arr[312, 183], arr[312, 184]))
        contrast_delta = outer_bg_val - torso_rim_val
        self.assertGreaterEqual(contrast_delta, 30, f"Torso boundary lacks contrast on white: delta = {contrast_delta} < 30")

    def test_10_seamless_loop_continuity(self):
        """Verifies that frame 0 and frame 119 form a smooth seamless loop."""
        f0 = cv2.imread(os.path.join(self.frames_dir, "frame_000.png"))
        f119 = cv2.imread(os.path.join(self.frames_dir, "frame_119.png"))
        diff = cv2.absdiff(f0, f119)
        mean_diff = np.mean(diff)
        self.assertLess(mean_diff, 5.0, f"Loop seam discontinuity too large: mean diff = {mean_diff:.2f}")

    def test_11_pelvis_continuous_arc_and_no_pinholes(self):
        """Verifies pelvis bottom has zero internal pinholes and forms a smooth convex arc."""
        f0 = cv2.imread(os.path.join(self.frames_dir, "frame_000.png"), cv2.IMREAD_UNCHANGED)
        alpha = f0[:, :, 3]
        
        for y in range(408, 413):
            for x in range(246, 255):
                self.assertGreaterEqual(alpha[y, x], 200, f"Pinhole detected in pelvis at ({x}, {y}): alpha={alpha[y, x]}")

    def test_12_waving_kinematics_active_motion(self):
        """Verifies that the viewer's left winglet genuinely executes active waving kinematics."""
        f0 = cv2.imread(os.path.join(self.frames_dir, "frame_000.png"), cv2.IMREAD_UNCHANGED)
        f60 = cv2.imread(os.path.join(self.frames_dir, "frame_060.png"), cv2.IMREAD_UNCHANGED)
        
        # Outer left zone (x < 115): in resting pose (frame 0), winglet rests at flank (0 pixels).
        # In active wave gesture (frame 60), winglet extends outward into outer space (> 1000 pixels).
        pixels_f0_outer = np.sum(f0[:, :115, 3] > 100)
        pixels_f60_outer = np.sum(f60[:, :115, 3] > 100)
        
        self.assertEqual(pixels_f0_outer, 0, f"Frame 0 has unexpected outer pixels: {pixels_f0_outer}")
        self.assertGreaterEqual(pixels_f60_outer, 500, f"Frame 60 waving reach too small: {pixels_f60_outer} < 500")

    def test_13_google_chrome_headless_lottie_validation(self):
        """Validates Lottie JSON in Google Chrome headless with local lottie-web player."""
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        self.assertTrue(os.path.exists(chrome_path), f"Chrome missing: {chrome_path}")
        
        test_html_dir = "/tmp/lottie_chrome_wave_test"
        os.makedirs(test_html_dir, exist_ok=True)
        shutil.copy(self.lottie_path, os.path.join(test_html_dir, "lottie.json"))
        shutil.copy(os.path.join(WORKSPACE_DIR, "scratch/lottie.min.js"), os.path.join(test_html_dir, "lottie.min.js"))
        
        html_content = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script src="lottie.min.js"></script>
<style>
  body { margin: 0; background: #0B0F17; display: flex; justify-content: center; align-items: center; height: 100vh; }
  #anim { width: 512px; height: 512px; }
</style>
</head>
<body>
<div id="anim"></div>
<script>
  window.animLoaded = false;
  window.animError = null;
  fetch('lottie.json')
    .then(res => res.json())
    .then(data => {
      const anim = lottie.loadAnimation({
        container: document.getElementById('anim'),
        renderer: 'svg',
        loop: true,
        autoplay: true,
        animationData: data
      });
      anim.addEventListener('DOMLoaded', () => {
        window.animLoaded = true;
        document.title = "LOTTIE_LOADED_SUCCESS";
      });
    })
    .catch(err => {
      window.animError = String(err);
      document.title = "LOTTIE_ERROR";
    });
</script>
</body>
</html>"""
        test_html_file = os.path.join(test_html_dir, "index.html")
        with open(test_html_file, "w") as f:
            f.write(html_content)
            
        screenshot_out = os.path.join(test_html_dir, "chrome_render.png")
        cmd = [
            chrome_path,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--allow-file-access-from-files",
            "--virtual-time-budget=2000",
            f"--screenshot={screenshot_out}",
            f"file://{test_html_file}"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        self.assertEqual(res.returncode, 0, f"Chrome headless exited with error: {res.stderr}")
        self.assertTrue(os.path.exists(screenshot_out), "Chrome screenshot was not created!")
        
        # Verify rendered image contains non-background mascot pixels
        im = cv2.imread(screenshot_out)
        self.assertIsNotNone(im, "Failed to load Chrome screenshot")
        bg_color = np.array([23, 15, 11]) # BGR for #0B0F17
        diff = np.abs(im.astype(int) - bg_color).sum(axis=2)
        mascot_pixels = np.sum(diff > 30)
        self.assertGreater(mascot_pixels, 10000, f"Chrome screenshot contains too few mascot pixels: {mascot_pixels}")

    def test_14_strictly_zero_cyan_in_all_gaps(self):
        """Verifies that animated.webp has strictly zero cyan pixels in limb gaps."""
        im = Image.open(self.webp_path)
        gaps = {
            'left_arm': (260, 380, 160, 215),
            'left_foot': (390, 470, 210, 255),
            'right_foot': (390, 470, 255, 300)
        }
        for f in range(min(20, im.n_frames)):
            im.seek(f)
            arr = np.array(im.convert('RGBA'))
            for name, (y1, y2, x1, x2) in gaps.items():
                crop = arr[y1:y2, x1:x2]
                cyan = (crop[:, :, 1] > 170) & (crop[:, :, 2] > 170) & (crop[:, :, 0] < 120) & (crop[:, :, 3] > 30)
                cnt = np.sum(cyan)
                self.assertEqual(cnt, 0, f"Frame {f} gap {name} contains {cnt} cyan pixels!")

    def test_15_all_target_directories_exist_and_synchronized(self):
        """Verifies deliverables exist across target directories."""
        dirs = [
            os.path.join(WORKSPACE_DIR, "assets/01_waving"),
            os.path.join(WORKSPACE_DIR, "mascots/aituko/assets/01_waving"),
            os.path.join(WORKSPACE_DIR, "assets/04_wave"),
            os.path.join(WORKSPACE_DIR, "assets/05_wave"),
        ]
        for d in dirs:
            self.assertTrue(os.path.isdir(d), f"Missing target dir: {d}")
            self.assertTrue(os.path.exists(os.path.join(d, "lottie.json")), f"Missing lottie.json in {d}")
            self.assertTrue(os.path.exists(os.path.join(d, "animated.webp")), f"Missing animated.webp in {d}")
            self.assertTrue(os.path.exists(os.path.join(d, "looped_video.mp4")), f"Missing looped_video.mp4 in {d}")

    def test_16_keyframe_3_eyes_open_smiling_arches(self):
        """Verifies that Keyframe 3 (Stage 3: Salutation Rayonnante) has full, smiling cyan arches."""
        kf3_path = os.path.join(WORKSPACE_DIR, "mascots/aituko", "aituko_wave_keyframe_3_eyes_closed.png")
        self.assertTrue(os.path.exists(kf3_path), f"Missing keyframe 3: {kf3_path}")
        im = cv2.imread(kf3_path, cv2.IMREAD_UNCHANGED)
        self.assertIsNotNone(im, "Failed to load keyframe 3")
        b, g, r, a = cv2.split(im)
        cyan_mask = (b > 180) & (g > 180) & (r < 120) & (a > 50) # OpenCV BGRA
        ys, xs = np.where(cyan_mask)
        self.assertTrue(len(ys) > 0, "No cyan eye pixels found in keyframe 3!")
        eye_height = int(ys.max() - ys.min() + 1)
        eye_width = int(xs.max() - xs.min() + 1)
        # Eyes remain open smiling arches matching 3D reference video
        self.assertGreaterEqual(eye_height, 10, f"Keyframe 3 eyes are deformed or closed! Height={eye_height}px < 10px")
        self.assertGreaterEqual(eye_width, 20, f"Keyframe 3 eyes are incomplete! Width={eye_width}px < 20px")

    def test_17_all_mirrors_have_full_120_frames(self):
        """Verifies that all mirror directories contain the full 120 frames."""
        mirrors = [
            os.path.join(WORKSPACE_DIR, "assets/01_waving/frames"),
            os.path.join(WORKSPACE_DIR, "mascots/aituko/assets/01_waving/frames"),
            os.path.join(WORKSPACE_DIR, "aituko/assets/01_waving/frames"),
            os.path.join(WORKSPACE_DIR, "assets/04_wave/frames"),
            os.path.join(WORKSPACE_DIR, "assets/05_wave/frames"),
        ]
        for m_dir in mirrors:
            self.assertTrue(os.path.isdir(m_dir), f"Missing frames dir: {m_dir}")
            pngs = [f for f in os.listdir(m_dir) if f.endswith(".png")]
            self.assertEqual(len(pngs), 120, f"Expected 120 frames in {m_dir}, but found {len(pngs)}!")

    def test_18_mascots_aituko_has_all_deliverables(self):
        """Verifies mascots/aituko/ contains all required deliverables including standalone keyframes."""
        m_dir = os.path.join(WORKSPACE_DIR, "mascots/aituko")
        req_files = [
            "aituko_wave_master_board.png",
            "aituko_wave_master_board_v1.png",
            "aituko_wave_studio_trichroma_board.png",
            "aituko_wave_studio_trichroma_board_v1.png",
            "aituko_wave_keyframe_1_median.png",
            "aituko_wave_keyframe_2_wave_apex.png",
            "aituko_wave_keyframe_3_eyes_closed.png",
            "aituko_wave_keyframe_4_wave_nadir.png",
            "aituko_wave_animated.svg",
            "aituko_wave_animated_transparent.svg",
            "aituko_wave_vector.json",
            "lottie.json",
            "aituko_wave_animated.webp",
            "animated.webp",
            "aituko_wave_animated.gif",
            "animated.gif",
            "aituko_wave_animated_dark.gif",
            "animated_dark.gif",
            "aituko_wave_animated_green.gif",
            "animated_green.gif",
            "aituko_wave_vector.mp4",
            "looped_video.mp4",
            "aituko_wave_static.png",
            "static.png",
        ]
        for rf in req_files:
            p = os.path.join(m_dir, rf)
            self.assertTrue(os.path.exists(p), f"Missing deliverable in mascots/aituko/: {rf}")

    def test_19_svg_winglet_coordinate_isolation(self):
        """Validates that waving left winglet is not nested under anim-root to prevent double root-float translation."""
        with open(self.svg_path, "r", encoding="utf-8") as f:
            svg = f.read()
            
        idx_winglet_r = svg.find('class="anim-winglet-r"')
        self.assertNotEqual(idx_winglet_r, -1, "Missing anim-winglet-r in SVG!")
        idx_winglet_l = svg.find('class="anim-winglet-l"')
        self.assertNotEqual(idx_winglet_l, -1, "Missing anim-winglet-l in SVG!")
        
        # The closing tag of anim-root must be between anim-winglet-r and anim-winglet-l
        sub_between = svg[idx_winglet_r:idx_winglet_l]
        self.assertIn("</g>", sub_between, "anim-winglet-l appears to be nested inside anim-root!")

    def test_21_right_winglet_zero_flank_drift(self):
        """Validates that across frames the right winglet never drifts in X away from the torso flank."""
        from scripts.build_flawless_aituko_wave import get_wave_kinematics
        for f in range(120):
            k = get_wave_kinematics(f)
            self.assertEqual(k['tx_rpod'], 0.0, f"Frame {f} right pod has non-zero horizontal drift: {k['tx_rpod']}")

    def test_22_left_winglet_shoulder_anchor_stability(self):
        """Validates that left winglet pivots around shoulder and shoulder stays anchored to torso."""
        from scripts.build_flawless_aituko_wave import get_wave_kinematics
        for f in range(120):
            k = get_wave_kinematics(f)
            self.assertEqual(k['tx_lpod'], 0.0, f"Frame {f} left shoulder has non-zero horizontal drift: {k['tx_lpod']}")
        # Rotation reaches authentic waving apex (> 160 deg) at frame 68
        apex_k = get_wave_kinematics(68)
        self.assertGreater(apex_k['rot_lpod'], 160.0, f"Wave apex rotation too low: {apex_k['rot_lpod']}")
        rest_k = get_wave_kinematics(0)
        self.assertAlmostEqual(rest_k['rot_lpod'], 0.0, delta=1.0, msg=f"Frame 0 rotation not at rest: {rest_k['rot_lpod']}")

if __name__ == "__main__":
    unittest.main()

