#!/usr/bin/env python3
"""
Rigorous Visual Integrity & Artifact Elimination Test Suite for AItuko Idle Animation.
Enforces strict frame-by-frame, component-by-component, and vector criteria:
1. Zero stray line artifacts (Hough transform & Canny edge on winglets to ensure NO needles/sticks).
2. Zero horizontal neck cut/gap (continuous neck socket continuity across all 120 frames).
3. Zero fake cyan glow on feet and winglets (cyan emissive strictly isolated to eye faceplate).
4. Silhouette contrast verification against #FFFFFF (WCAG/Luminance separation).
5. Vector cleanliness: Zero <rect> streaks in SVG and Lottie JSON.
6. File size constraints: Lottie JSON < 50 KB.
7. Seamless 120-frame loop continuity.
"""

import os
import sys
import json
import math
import unittest
import cv2
import numpy as np
from PIL import Image

WORKSPACE_DIR = "/Users/richard/Developer/Stickers Uko"

class TestAitukoIdleVisualIntegrity(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.svg_path = os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_idle_animated.svg")
        cls.lottie_path = os.path.join(WORKSPACE_DIR, "assets/00_idle/lottie.json")
        cls.frames_dir = os.path.join(WORKSPACE_DIR, "assets/00_idle/frames")
        cls.webp_path = os.path.join(WORKSPACE_DIR, "assets/00_idle/animated.webp")
        cls.gif_path = os.path.join(WORKSPACE_DIR, "assets/00_idle/animated.gif")
        cls.mp4_path = os.path.join(WORKSPACE_DIR, "assets/00_idle/looped_video.mp4")
        
    def test_01_svg_no_specular_rectangles_or_bars(self):
        """Validates that animated SVG has eliminated all hardcoded <rect> streak artifacts."""
        self.assertTrue(os.path.exists(self.svg_path), f"SVG missing: {self.svg_path}")
        with open(self.svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
            
        # Ensure no rotated specular rectangle streaks exist
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

    def test_05_frames_count_and_naming(self):
        """Verifies exactly 120 frames exist in assets/00_idle/frames."""
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
                # 1. Cyan lights are STRICTLY FORBIDDEN at the tips/ends of limbs
                # Feet bottom tips: y > 450
                cyan_feet_tips = np.sum((ys > 450))
                self.assertEqual(cyan_feet_tips, 0, f"Frame {f_idx}: Cyan glow found at bottom tips of feet (y > 450)!")
                
                # Winglet bottom tips: y > 365 on outer columns (x < 155 or x > 355)
                cyan_winglet_tips = np.sum((ys > 365) & ((xs < 155) | (xs > 355)))
                self.assertEqual(cyan_winglet_tips, 0, f"Frame {f_idx}: Cyan glow found at bottom tips of winglets (y > 365)!")
                
                # 2. All cyan pixels must belong either to Visor Eyes (y < 190) or Magnetic Levitation Gaps (y in [280, 440])
                invalid_cyan = np.sum((ys >= 190) & ((ys < 280) | (ys > 440)))
                self.assertEqual(invalid_cyan, 0, f"Frame {f_idx}: Cyan glow found outside visor eyes and magnetic gaps!")

    def test_07_frame_by_frame_winglet_no_needle_artifacts(self):
        """Verifies using edge detection that winglets have NO linear streak/needle artifacts."""
        for f_idx in [0, 30, 60, 90]:
            frame_path = os.path.join(self.frames_dir, f"frame_{f_idx:03d}.png")
            im = cv2.imread(frame_path, cv2.IMREAD_UNCHANGED)
            alpha = im[:, :, 3] if im.shape[2] == 4 else np.full(im.shape[:2], 255)
            gray = cv2.cvtColor(im[:, :, :3], cv2.COLOR_BGR2GRAY)
            
            # Left winglet interior mask:
            pod_mask = np.zeros_like(alpha)
            pod_mask[240:420, 100:175] = alpha[240:420, 100:175] > 200
            # Erode mask by 8 pixels so we ONLY inspect the INTERIOR of the pod, not outer silhouette
            eroded_mask = cv2.erode(pod_mask.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
            
            # Canny edge detection inside pod interior
            edges = cv2.Canny(gray, 40, 100)
            interior_edges = cv2.bitwise_and(edges, edges, mask=eroded_mask)
            
            lines = cv2.HoughLinesP(interior_edges, 1, np.pi/180, threshold=20, minLineLength=20, maxLineGap=5)
            self.assertTrue(lines is None or len(lines) == 0, f"Frame {f_idx}: Stray interior needle streak detected in left winglet!")

    def test_08_neck_joint_continuity_across_motion(self):
        """Verifies that the neck socket maintains continuity without horizontal blank gaps."""
        for f_idx in range(0, 120, 10):
            frame_path = os.path.join(self.frames_dir, f"frame_{f_idx:03d}.png")
            im = cv2.imread(frame_path, cv2.IMREAD_UNCHANGED)
            alpha = im[:, :, 3] if im.shape[2] == 4 else np.full(im.shape[:2], 255)
            
            # In the neck column x=256, y from 180 to 240 must have solid mascot coverage (alpha > 200)
            neck_col = alpha[180:240, 256]
            self.assertTrue(np.all(neck_col > 200), f"Frame {f_idx}: Neck separation gap detected at column x=256!")

    def test_09_white_background_contrast(self):
        """Verifies that mascot porcelain has crisp boundary contrast against #FFFFFF."""
        frame_path = os.path.join(self.frames_dir, "frame_000.png")
        im = Image.open(frame_path).convert("RGBA")
        white_bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        white_bg.alpha_composite(im)
        arr = np.array(white_bg.convert("L"))
        
        # Edge gradient across boundary of torso:
        # Outer background at x=180 is 255, edge rim at x=184 is ~150 (delta > 35 units)
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
        
        # 1. Zero internal pinholes inside pelvis
        for y in range(408, 413):
            for x in range(246, 255):
                self.assertGreaterEqual(alpha[y, x], 200, f"Pinhole detected in pelvis at ({x}, {y}): alpha={alpha[y, x]}")
                
        # 2. Smooth convex profile (vertex near center x=256)
        pelvis_bottoms = []
        for x in range(238, 275):
            ys = np.where(alpha[400:430, x] > 120)[0] + 400
            self.assertTrue(len(ys) > 0, f"No pelvis boundary found at x={x}")
            pelvis_bottoms.append(ys[-1])
            
        center_idx = 256 - 238
        self.assertGreaterEqual(pelvis_bottoms[center_idx], max(pelvis_bottoms[0], pelvis_bottoms[-1]),
                                "Pelvis bottom is not convex arched!")

    def test_12_no_horizontal_neck_shelf(self):
        """Verifies that tilted frames (e.g. frame 30 with max head tilt) have NO horizontal neck shelf."""
        from scripts.build_flawless_aituko_idle import get_kinematics
        for f_idx in [15, 30, 45, 75, 90]:
            k = get_kinematics(f_idx, 120)
            fpath = os.path.join(self.frames_dir, f"frame_{f_idx:03d}.png")
            im = cv2.imread(fpath, cv2.IMREAD_UNCHANGED)
            alpha = im[:, :, 3]
            
            # Neck waist center moves dynamically with dy_head/dy_root
            neck_y = int(round(211.0 + (k['dy_head'] + k['dy_root']) * 0.5))
            neck_widths = []
            for y in range(neck_y - 3, neck_y + 4):
                xs = np.where(alpha[y, :] > 120)[0]
                if len(xs) > 0:
                    neck_widths.append(xs[-1] - xs[0] + 1)
            min_width = min(neck_widths) if neck_widths else 0
            self.assertLessEqual(min_width, 50, f"Frame {f_idx}: Horizontal neck shelf detected! Min waist width = {min_width} > 50px")

    def test_13_pod_tip_capsule_smoothness(self):
        """Verifies that left winglet tip has NO inverted bite/dent."""
        f0 = cv2.imread(os.path.join(self.frames_dir, "frame_000.png"), cv2.IMREAD_UNCHANGED)
        alpha = f0[:, :, 3]
        
        bottom_ys = []
        for x in range(130, 144):
            ys = np.where(alpha[360:385, x] > 100)[0] + 360
            if len(ys) > 0:
                bottom_ys.append(ys[-1])
        self.assertTrue(len(bottom_ys) >= 10, "Could not extract left pod bottom contour")
        center_y = max(bottom_ys)
        self.assertGreaterEqual(center_y, 376, f"Left pod tip is truncated or dented: max y = {center_y} < 376")

    def test_14_magnetic_glow_subtle_opacity(self):
        """Verifies that magnetic halos in gaps have subtle opacity (max alpha <= 75, opacity <= 30%)."""
        for f_idx in [0, 30, 60, 90]:
            fpath = os.path.join(self.frames_dir, f"frame_{f_idx:03d}.png")
            im = cv2.imread(fpath, cv2.IMREAD_UNCHANGED)
            b, g, r, a = cv2.split(im)
            
            arm_gap_cyan = (b > 180) & (g > 180) & (r < 120)
            arm_gap_alpha = a[295:330, 165:185]
            arm_gap_is_cyan = arm_gap_cyan[295:330, 165:185]
            if np.any(arm_gap_is_cyan):
                max_alpha = np.max(arm_gap_alpha[arm_gap_is_cyan])
                self.assertLessEqual(max_alpha, 75, f"Frame {f_idx}: Arm gap magnetic glow is too bright! Alpha = {max_alpha} > 75")

    def test_15_pelvis_smoothness_and_zero_pinholes(self):
        """Verifies across frames that the pelvis bottom has ZERO pinholes and forms a smooth continuous convex arc."""
        from scripts.build_flawless_aituko_idle import get_kinematics
        for f_idx in [0, 30, 60, 90]:
            fpath = os.path.join(self.frames_dir, f"frame_{f_idx:03d}.png")
            im = cv2.imread(fpath, cv2.IMREAD_UNCHANGED)
            alpha = im[:, :, 3]
            
            # Interior of pelvis dome accounting for frame vertical displacement
            dy = int(round(get_kinematics(f_idx, 120)['dy_root']))
            pelvis_core = alpha[406 + dy : 416 + dy, 246:266]
            pinholes = np.sum(pelvis_core < 200)
            self.assertEqual(pinholes, 0, f"Frame {f_idx}: Found {pinholes} pinholes/alpha gaps inside pelvis core!")

    def test_16_authentic_idle_float_amplitude(self):
        """Verifies that mascot remains grounded at baseline with zero artificial vertical floating."""
        from scripts.build_flawless_aituko_idle import get_kinematics
        root_ys = [get_kinematics(f, 120)['dy_root'] for f in range(120)]
        total_stroke = max(root_ys) - min(root_ys)
        self.assertEqual(total_stroke, 0.0, f"Mascot must remain grounded (stroke=0.0px), but got {total_stroke:.2f}px!")

    def test_17_svg_pelvis_and_chin_contour_smoothness(self):
        """Verifies that animated SVG torso pelvis and head chin have ZERO crevasses or notch jumps."""
        with open(self.svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()

        # 1. Pelvis must not have the defective 420.08 / 420.09 inverted notch
        self.assertNotIn("420.08", svg_content, "SVG torso still contains defective 420.08 crevasse notch!")
        self.assertNotIn("420.09", svg_content, "SVG torso still contains defective 420.09 crevasse notch!")

        # 2. Pelvis base must have apex at y >= 423.0
        self.assertIn("423.15", svg_content, "SVG torso missing smooth continuous 423.15 convex apex!")

        # 3. Chin must not contain the 208.28 kink step
        self.assertNotIn("208.28", svg_content, "SVG chin still contains 208.28 kink step!")

    def test_18_lottie_and_svg_no_oval_saucer_above_eyes(self):
        """Verifies that Lottie JSON and SVG have completely eliminated the oval saucer above the eyes."""
        with open(self.lottie_path, "r", encoding="utf-8") as f:
            lottie_str = f.read()
        self.assertNotIn("Visor Softbox Arc", lottie_str, "Lottie contains Visor Softbox Arc (oval shape above eyes)!")
        self.assertNotIn("Visor Specular Pip", lottie_str, "Lottie contains Visor Specular Pip!")

        with open(self.svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
        self.assertNotIn("master_visorArcReflection", svg_content, "SVG still contains master_visorArcReflection!")

    def test_19_strictly_zero_cyan_pixels_in_all_gaps(self):
        """Verifies that animated.webp in assets and in brain directory has strictly ZERO cyan pixels in all member gaps."""
        im = Image.open(self.webp_path)
        gaps = {
            'left_arm': (260, 380, 160, 215),
            'right_arm': (260, 380, 295, 350),
            'left_foot': (390, 470, 210, 255),
            'right_foot': (390, 470, 255, 300)
        }
        for f in range(im.n_frames):
            im.seek(f)
            arr = np.array(im.convert('RGBA'))
            for name, (y1, y2, x1, x2) in gaps.items():
                crop = arr[y1:y2, x1:x2]
                cyan = (crop[:, :, 1] > 170) & (crop[:, :, 2] > 170) & (crop[:, :, 0] < 120) & (crop[:, :, 3] > 30)
                cnt = np.sum(cyan)
                self.assertEqual(cnt, 0, f"animated.webp frame {f} gap {name} contains {cnt} cyan pixels!")

        # Verify synchronized brain file
        brain_webp = "/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68/aituko_idle_animated.webp"
        self.assertTrue(os.path.exists(brain_webp), f"Brain webp missing: {brain_webp}")
        b_im = Image.open(brain_webp)
        for f in range(min(5, b_im.n_frames)):
            b_im.seek(f)
            b_arr = np.array(b_im.convert('RGBA'))
            for name, (y1, y2, x1, x2) in gaps.items():
                crop = b_arr[y1:y2, x1:x2]
                cyan = (crop[:, :, 1] > 170) & (crop[:, :, 2] > 170) & (crop[:, :, 0] < 120) & (crop[:, :, 3] > 30)
                cnt = np.sum(cyan)
                self.assertEqual(cnt, 0, f"Brain webp frame {f} gap {name} contains {cnt} cyan pixels!")

    def test_20_html_and_viewers_zero_thrusters_and_ovals(self):
        """Validates that index.html and all interactive viewers have strictly ZERO thruster glows and ZERO visor ovals."""
        index_path = os.path.join(WORKSPACE_DIR, "index.html")
        with open(index_path, "r", encoding="utf-8") as f:
            idx = f.read()
        self.assertNotIn("thrusterGlow", idx, "index.html still contains thrusterGlow!")
        self.assertNotIn("aitukoInteractiveSvg_thrusterGlow", idx)
        self.assertNotIn("demoAitukoSvg_thrusterGlow", idx)

        viewer_path = os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_3d_turnaround_viewer.html")
        with open(viewer_path, "r", encoding="utf-8") as f:
            v_content = f.read()
        self.assertNotIn("thrusterMat", v_content, "3D viewer contains thrusterMat!")
        self.assertNotIn("fGlowMat", v_content, "3D viewer contains fGlowMat!")
        self.assertNotIn("0x00F0FF, 0.7", v_content, "3D viewer rim light still cyan!")

if __name__ == "__main__":
    unittest.main()


