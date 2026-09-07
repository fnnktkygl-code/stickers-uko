import shutil
import cv2
import numpy as np
import os
from PIL import Image

def render_animation():
    layers_dir = "mascots/owluko/rig_layers"
    out_dir = "mascots/owluko"
    assets_dir = "assets/00_idle"
    os.makedirs(assets_dir, exist_ok=True)
    
    # Load all 11 master layers
    shadow_raw = cv2.imread(f"{layers_dir}/00_shadow.png", cv2.IMREAD_UNCHANGED)
    lfoot_raw = cv2.imread(f"{layers_dir}/01_foot_left.png", cv2.IMREAD_UNCHANGED)
    rfoot_raw = cv2.imread(f"{layers_dir}/02_foot_right.png", cv2.IMREAD_UNCHANGED)
    body_raw = cv2.imread(f"{layers_dir}/03_body_porcelain.png", cv2.IMREAD_UNCHANGED)
    lwing_raw = cv2.imread(f"{layers_dir}/04_wing_left.png", cv2.IMREAD_UNCHANGED)
    rwing_raw = cv2.imread(f"{layers_dir}/05_wing_right.png", cv2.IMREAD_UNCHANGED)
    leye_raw = cv2.imread(f"{layers_dir}/06_eye_left.png", cv2.IMREAD_UNCHANGED)
    reye_raw = cv2.imread(f"{layers_dir}/07_eye_right.png", cv2.IMREAD_UNCHANGED)
    leyelid_raw = cv2.imread(f"{layers_dir}/08_eyelid_left.png", cv2.IMREAD_UNCHANGED)
    reyelid_raw = cv2.imread(f"{layers_dir}/09_eyelid_right.png", cv2.IMREAD_UNCHANGED)
    beak_raw = cv2.imread(f"{layers_dir}/10_beak.png", cv2.IMREAD_UNCHANGED)

    h, w = 512, 512
    fps = 30
    duration = 4.0
    total_frames = int(fps * duration) # 120 frames
    
    print(f"Rendering {total_frames} frames ({duration}s @ {fps} fps)...")
    
    frames_rgba = []
    
    for f in range(total_frames):
        t = f / float(fps)
        
        # 1. Kinematics calculations
        # Respiration cycle: 2.0s period (0.5 Hz)
        breath = np.sin(t * 2 * np.pi * 0.5)
        scale_y = 1.0 + breath * 0.018 # +1.8% / -1.8%
        scale_x = 1.0 - breath * 0.009 # -0.9% / +0.9%
        pelvis_bob = breath * 1.5 # +/- 1.5 px
        head_tilt = np.sin(t * 2 * np.pi * 0.25) * 1.5 # +/- 1.5 degrees

        # Wing secondary harmonic sway (phase lag of 0.12s)
        wing_phase = np.sin((t - 0.12) * 2 * np.pi * 0.5)
        l_wing_rot = -wing_phase * 2.4 # +/- 2.4 degrees
        r_wing_rot = wing_phase * 2.4

        # Blink calculation: 2 blinks at t = 1.2s and t = 3.1s
        blink_p = 0.0
        # Blink 1: t in [1.15, 1.35]
        if 1.15 <= t <= 1.35:
            p = (t - 1.15) / 0.20
            blink_p = np.sin(p * np.pi)
        # Blink 2: t in [3.05, 3.25]
        elif 3.05 <= t <= 3.25:
            p = (t - 3.05) / 0.20
            blink_p = np.sin(p * np.pi)
            
        blink_dy = blink_p * 16.0 # translates down 16px to close eye

        # Gaze saccade: shifts subtly left at t in [2.0, 2.8]
        gaze_dx = 0.0
        gaze_dy = 0.0
        if 2.0 <= t <= 2.8:
            gaze_dx = -2.0
            gaze_dy = 0.5

        # -------------------------------------------------------------
        # COMPOSITING FRAME
        # -------------------------------------------------------------
        frame = np.zeros((h, w, 4), dtype=np.uint8)

        # A. Shadow: scale from (256, 489)
        s_factor = 1.0 + breath * 0.012
        M_shadow = cv2.getRotationMatrix2D((256, 489), 0, s_factor)
        shadow_warped = cv2.warpAffine(shadow_raw, M_shadow, (w, h), flags=cv2.INTER_LINEAR)
        
        # B. Feet: stationary on floor
        # Over composite feet over shadow
        def blend_layer(base, top):
            a_top = top[:, :, 3:4] / 255.0
            a_base = base[:, :, 3:4] / 255.0
            out_a = a_top + a_base * (1.0 - a_top)
            nz = out_a[:, :, 0] > 0
            out_rgb = np.zeros_like(base[:, :, :3])
            out_rgb[nz] = (top[nz, :3] * a_top[nz] + base[nz, :3] * a_base[nz] * (1.0 - a_top[nz])) / out_a[nz]
            return np.dstack([out_rgb.astype(np.uint8), (out_a * 255.0).astype(np.uint8)])

        frame = blend_layer(frame, shadow_warped)
        frame = blend_layer(frame, lfoot_raw)
        frame = blend_layer(frame, rfoot_raw)

        # C. Body Rig (Body, Wings, Eyes, Eyelids, Beak)
        # Transformed by Body transform: Center at (256, 435 + pelvis_bob)
        body_comp = np.zeros((h, w, 4), dtype=np.uint8)
        body_comp = blend_layer(body_comp, body_raw)

        # Left Wing transformed around shoulder (128, 192)
        M_lw = cv2.getRotationMatrix2D((128, 192), l_wing_rot, 1.0)
        lw_warped = cv2.warpAffine(lwing_raw, M_lw, (w, h), flags=cv2.INTER_LINEAR)
        body_comp = blend_layer(body_comp, lw_warped)

        # Right Wing transformed around shoulder (384, 192)
        M_rw = cv2.getRotationMatrix2D((384, 192), r_wing_rot, 1.0)
        rw_warped = cv2.warpAffine(rwing_raw, M_rw, (w, h), flags=cv2.INTER_LINEAR)
        body_comp = blend_layer(body_comp, rw_warped)

        # Eyes: Left Eyeball & Right Eyeball with gaze saccade
        M_gaze = np.float32([[1, 0, gaze_dx], [0, 1, gaze_dy]])
        leye_warped = cv2.warpAffine(leye_raw, M_gaze, (w, h), flags=cv2.INTER_LINEAR)
        reye_warped = cv2.warpAffine(reye_raw, M_gaze, (w, h), flags=cv2.INTER_LINEAR)
        body_comp = blend_layer(body_comp, leye_warped)
        body_comp = blend_layer(body_comp, reye_warped)

        # Eyelids with blink_dy
        M_blink = np.float32([[1, 0, 0], [0, 1, blink_dy]])
        leyelid_warped = cv2.warpAffine(leyelid_raw, M_blink, (w, h), flags=cv2.INTER_LINEAR)
        reyelid_warped = cv2.warpAffine(reyelid_raw, M_blink, (w, h), flags=cv2.INTER_LINEAR)
        body_comp = blend_layer(body_comp, leyelid_warped)
        body_comp = blend_layer(body_comp, reyelid_warped)

        # Beak
        body_comp = blend_layer(body_comp, beak_raw)

        # Now apply the Body breathing + tilt + bob transform to the whole upper body
        # Pivot is pelvis: (256, 435)
        # Transform matrix: translate to origin, scale, rotate, translate back + pelvis_bob
        cos_t = np.cos(np.radians(head_tilt))
        sin_t = np.sin(np.radians(head_tilt))
        
        # Affine transform for scaleX, scaleY, rotation, translation
        # [ x' ] = [ cos -sin ] [ sx  0 ] [ x - 256 ] + [ 256 ]
        # [ y' ]   [ sin  cos ] [ 0  sy ] [ y - 435 ]   [ 435 + pelvis_bob ]
        T1 = np.float32([[1, 0, -256], [0, 1, -435], [0, 0, 1]])
        S = np.float32([[scale_x, 0, 0], [0, scale_y, 0], [0, 0, 1]])
        R = np.float32([[cos_t, -sin_t, 0], [sin_t, cos_t, 0], [0, 0, 1]])
        T2 = np.float32([[1, 0, 256], [0, 1, 435 + pelvis_bob], [0, 0, 1]])
        
        M_full = T2 @ R @ S @ T1
        body_transformed = cv2.warpAffine(body_comp, M_full[:2], (w, h), flags=cv2.INTER_LINEAR)

        # Final blend of body onto feet and shadow
        final_frame = blend_layer(frame, body_transformed)
        frames_rgba.append(final_frame)

    # -------------------------------------------------------------
    # EXPORT ANIMATED WEBP, GIF, MP4
    # -------------------------------------------------------------
    pil_frames = [Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGRA2RGBA)) for f in frames_rgba]

    # Looping WebP (512x512, transparent, 30fps = 33ms per frame)
    webp_path = os.path.join(out_dir, "owluko_idle_master.webp")
    pil_frames[0].save(
        webp_path,
        format="WEBP",
        save_all=True,
        append_images=pil_frames[1:],
        duration=33,
        loop=0,
        lossless=False,
        quality=90,
        method=4
    )
    print(f"Saved animated WebP: {webp_path} ({os.path.getsize(webp_path)/1024:.1f} KB)")
    
    # Copy to assets/00_idle/
    pil_frames[0].save(
        os.path.join(assets_dir, "animated.webp"),
        format="WEBP",
        save_all=True,
        append_images=pil_frames[1:],
        duration=33,
        loop=0,
        lossless=False,
        quality=90,
        method=4
    )

    # Looping GIF
    gif_path = os.path.join(out_dir, "owluko_idle_master.gif")
    pil_frames[0].save(
        gif_path,
        format="GIF",
        save_all=True,
        append_images=pil_frames[1:],
        duration=33,
        loop=0,
        disposal=2
    )
    print(f"Saved animated GIF: {gif_path} ({os.path.getsize(gif_path)/1024:.1f} KB)")
    shutil.copy(gif_path, os.path.join(assets_dir, "animated.gif"))

    # MP4 via OpenCV
    mp4_path = os.path.join(out_dir, "owluko_idle_master.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_vid = cv2.VideoWriter(mp4_path, fourcc, 30, (w, h))
    for f in frames_rgba:
        # Composite on dark studio bg for MP4
        bg = np.full((h, w, 3), 18, dtype=np.uint8)
        a = f[:, :, 3:4] / 255.0
        comp_rgb = (f[:, :, :3] * a + bg * (1.0 - a)).astype(np.uint8)
        out_vid.write(comp_rgb)
    out_vid.release()
    print(f"Saved MP4: {mp4_path}")

    # -------------------------------------------------------------
    # BUILD SIDE-BY-SIDE MASTER AUDIT BOARD
    # -------------------------------------------------------------
    # Extract 4 key frames from studio reference video
    ref_cap = cv2.VideoCapture("mascots/owluko/owluko_idle.mp4")
    ref_total = int(ref_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    ref_indices = [0, ref_total // 4, ref_total // 2, 3 * ref_total // 4]
    
    # 4 rows x 2 cols (Col 1: Studio 3D Reference, Col 2: After Effects / Rive Rig Render)
    board = np.zeros((4 * 280, 2 * 280, 3), dtype=np.uint8)
    
    target_indices = [0, 30, 60, 90]
    phase_labels = [
        "Phase 1: Resting Pose & Inquisitive Gaze",
        "Phase 2: Inhalation & Gentle Head Tilt",
        "Phase 3: Eyelid Blink Closure",
        "Phase 4: Exhalation & Gaze Settling"
    ]
    
    for row_idx in range(4):
        ref_cap.set(cv2.CAP_PROP_POS_FRAMES, ref_indices[row_idx])
        ret, rframe = ref_cap.read()
        # Crop square around owl in reference (1080x1080 center)
        rh, rw = rframe.shape[:2]
        crop_ref = rframe[:, (rw - rh)//2 : (rw + rh)//2]
        crop_ref_256 = cv2.resize(crop_ref, (256, 256))
        
        # Render frame
        my_frame = frames_rgba[target_indices[row_idx]]
        # Composite on studio dark
        bg = np.full((h, w, 3), 20, dtype=np.uint8)
        a = my_frame[:, :, 3:4] / 255.0
        my_comp = (my_frame[:, :, :3] * a + bg * (1.0 - a)).astype(np.uint8)
        my_comp_256 = cv2.resize(my_comp, (256, 256))
        
        y0, y1 = row_idx * 280 + 20, row_idx * 280 + 276
        board[y0:y1, 10:266] = crop_ref_256
        board[y0:y1, 280:536] = my_comp_256
        
        # Add labels
        cv2.putText(board, phase_labels[row_idx], (12, row_idx * 280 + 16), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (245, 158, 11), 1, cv2.LINE_AA)
        cv2.putText(board, "Reference Video (MP4)", (14, y0 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(board, "AE / Rive Rig Render", (284, y0 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)

    ref_cap.release()
    board_path = os.path.join(out_dir, "owluko_rig_master_board.png")
    cv2.imwrite(board_path, board)
    print(f"Saved side-by-side audit board: {board_path}")

if __name__ == "__main__":
    render_animation()
