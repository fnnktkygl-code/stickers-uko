import cv2
import numpy as np
import os

def build():
    front_path = "mascots/owluko/owluko_turnaround_view_1_front.png"
    img = cv2.imread(front_path, cv2.IMREAD_UNCHANGED)
    h, w, c = img.shape
    
    out_dir = "mascots/owluko/rig_layers"
    os.makedirs(out_dir, exist_ok=True)
    
    # 0. CHROMA DESPILL on source image
    # Eliminates all green rim pixels (G > max(R, B))
    b, g, r, a = img[:, :, 0], img[:, :, 1], img[:, :, 2], img[:, :, 3]
    g_despill = np.minimum(g, np.maximum(r, b))
    img_clean = img.copy()
    img_clean[:, :, 1] = g_despill

    # 1. GROUND CONTACT SHADOW
    shadow = np.zeros((h, w, 4), dtype=np.uint8)
    cv2.ellipse(shadow, (198, 487), (36, 8), 0, 0, 360, (25, 25, 28, 170), -1)
    cv2.ellipse(shadow, (312, 487), (36, 8), 0, 0, 360, (25, 25, 28, 170), -1)
    cv2.ellipse(shadow, (256, 488), (70, 10), 0, 0, 360, (30, 30, 32, 90), -1)
    shadow[:, :, 3] = cv2.GaussianBlur(shadow[:, :, 3], (21, 21), 0)

    # 2. FEET (AVIAN 3-TOED PORCELAIN FEET)
    lfoot = np.zeros_like(img_clean)
    rfoot = np.zeros_like(img_clean)
    
    lf_mask = (img_clean[:, :, 3] > 20) & (np.arange(h)[:, None] >= 415) & (np.arange(w)[None, :] < 250)
    rf_mask = (img_clean[:, :, 3] > 20) & (np.arange(h)[:, None] >= 415) & (np.arange(w)[None, :] >= 262)
    
    # Exclude pixels above belly arc
    for y in range(415, 445):
        for x in range(155, 250):
            dx = (x - 256.0) / 95.0
            y_belly = 444.0 - dx**2 * 18.0
            if y < y_belly - 8.0:
                lf_mask[y, x] = False
        for x in range(262, 357):
            dx = (x - 256.0) / 95.0
            y_belly = 444.0 - dx**2 * 18.0
            if y < y_belly - 8.0:
                rf_mask[y, x] = False
                
    lfoot[lf_mask] = img_clean[lf_mask]
    rfoot[rf_mask] = img_clean[rf_mask]
    
    # Smooth feathering on ankle top joint
    for y in range(415, 426):
        mult = (y - 415.0) / 11.0
        lfoot[y, :, 3] = (lfoot[y, :, 3] * mult).astype(np.uint8)
        rfoot[y, :, 3] = (rfoot[y, :, 3] * mult).astype(np.uint8)

    # 3. WINGS (LEFT & RIGHT)
    lwing = np.zeros_like(img_clean)
    rwing = np.zeros_like(img_clean)
    
    lw_mask = (img_clean[:, :, 3] > 20) & (np.arange(w)[None, :] <= 134) & (np.arange(h)[:, None] >= 180) & (np.arange(h)[:, None] <= 412)
    rw_mask = (img_clean[:, :, 3] > 20) & (np.arange(w)[None, :] >= 376) & (np.arange(h)[:, None] >= 180) & (np.arange(h)[:, None] <= 412)
    
    lwing[lw_mask] = img_clean[lw_mask]
    rwing[rw_mask] = img_clean[rw_mask]
    
    # Soften inner edge by 2px
    for y in range(180, 413):
        xs_l = np.where(lwing[y, :, 3] > 0)[0]
        if len(xs_l) > 0:
            xm = xs_l.max()
            lwing[y, xm, 3] = int(lwing[y, xm, 3] * 0.5)
            if xm - 1 >= 0:
                lwing[y, xm - 1, 3] = int(lwing[y, xm - 1, 3] * 0.8)
        xs_r = np.where(rwing[y, :, 3] > 0)[0]
        if len(xs_r) > 0:
            xm = xs_r.min()
            rwing[y, xm, 3] = int(rwing[y, xm, 3] * 0.5)
            if xm + 1 < w:
                rwing[y, xm + 1, 3] = int(rwing[y, xm + 1, 3] * 0.8)

    # 4. BEAK
    beak = np.zeros_like(img_clean)
    beak_mask = np.zeros((h, w), dtype=bool)
    for y in range(162, 236):
        t = (y - 162.0) / 74.0
        hw = int(round(18.0 * (1.0 - 0.72 * t)))
        beak_mask[y, 256 - hw : 256 + hw + 1] = True
    beak_mask = beak_mask & (img_clean[:, :, 3] > 20)
    beak[beak_mask] = img_clean[beak_mask]

    # 5. EYEBALLS & EYELIDS
    leye_ball = np.zeros((h, w, 4), dtype=np.uint8)
    reye_ball = np.zeros((h, w, 4), dtype=np.uint8)
    leyelid = np.zeros((h, w, 4), dtype=np.uint8)
    reyelid = np.zeros((h, w, 4), dtype=np.uint8)
    
    leye_circ = np.zeros((h, w), dtype=np.uint8)
    reye_circ = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(leye_circ, (193, 160), 36, 255, -1)
    cv2.circle(reye_circ, (315, 163), 36, 255, -1)
    
    for y in range(h):
        for x in range(w):
            if leye_circ[y, x] and img_clean[y, x, 3] > 20:
                b_val, g_val, r_val = img_clean[y, x, :3]
                is_porcelain = (r_val > 180 and g_val > 165 and b_val > 145)
                if is_porcelain or y < 145:
                    leyelid[y, x] = img_clean[y, x]
                else:
                    leye_ball[y, x] = img_clean[y, x]
            if reye_circ[y, x] and img_clean[y, x, 3] > 20:
                b_val, g_val, r_val = img_clean[y, x, :3]
                is_porcelain = (r_val > 180 and g_val > 165 and b_val > 145)
                if is_porcelain or y < 147:
                    reyelid[y, x] = img_clean[y, x]
                else:
                    reye_ball[y, x] = img_clean[y, x]
                    
    # Inpaint top half of eyeballs to make complete 360 glassy spheres
    for eball, cx, cy, r_rad in [(leye_ball, 193, 160, 36), (reye_ball, 315, 163, 36)]:
        miss = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(miss, (cx, cy), r_rad, 255, -1)
        miss[eball[:, :, 3] > 20] = 0
        infilled = cv2.inpaint(eball[:, :, :3], miss, 9, cv2.INPAINT_TELEA)
        eball[:, :, :3] = infilled
        for y in range(cy - r_rad - 2, cy + r_rad + 3):
            for x in range(cx - r_rad - 2, cx + r_rad + 3):
                dist = np.sqrt((x - cx)**2 + (y - cy)**2)
                if dist <= r_rad - 1:
                    eball[y, x, 3] = 255
                elif dist <= r_rad + 1:
                    eball[y, x, 3] = int(255 * (r_rad + 1 - dist) / 2.0)
                else:
                    eball[y, x, 3] = 0

    # 6. PORCELAIN BODY CAPSULE
    body = img_clean.copy()
    # 6A. Remove feet from body
    body[445:, :, :] = 0
    belly_mask = np.zeros((h, w), dtype=np.uint8)
    for x in range(150, 365):
        dx = (x - 256.0) / 95.0
        if abs(dx) <= 1.0:
            y_max = int(round(444.0 - dx**2 * 18.0))
            for y in range(415, y_max + 1):
                if lf_mask[y, x] or rf_mask[y, x]:
                    belly_mask[y, x] = 255
                    body[y, x, 3] = 255
            body[y_max + 1:, x, :] = 0
    # Telea inpaint belly
    body[:, :, :3] = cv2.inpaint(body[:, :, :3], belly_mask, 7, cv2.INPAINT_TELEA)
    
    # 6B. Inpaint face sockets so eyes/beak can move independently
    face_mask = (beak_mask | (leye_circ > 0) | (reye_circ > 0)).astype(np.uint8) * 255
    face_mask = face_mask & (body[:, :, 3] > 20).astype(np.uint8) * 255
    body[:, :, :3] = cv2.inpaint(body[:, :, :3], face_mask, 9, cv2.INPAINT_TELEA)
    
    # 6C. Continuous egg flanks behind wings
    # Smooth porcelain transition:
    # Instead of dilating into transparent background, we inpaint strictly within existing porcelain alpha!
    # And we extend body alpha by 6px under the wings with porcelain colors
    flank_inpaint_mask = np.zeros((h, w), dtype=np.uint8)
    for y in range(180, 412):
        # left flank: x in [120, 138]
        flank_inpaint_mask[y, 122:138] = 255
        # right flank: x in [374, 390]
        flank_inpaint_mask[y, 374:390] = 255
    flank_inpaint_mask = flank_inpaint_mask & (body[:, :, 3] > 20).astype(np.uint8) * 255
    body[:, :, :3] = cv2.inpaint(body[:, :, :3], flank_inpaint_mask, 7, cv2.INPAINT_TELEA)

    # 7. SAVE MASTER RIG LAYERS
    layers = {
        "00_shadow.png": shadow,
        "01_foot_left.png": lfoot,
        "02_foot_right.png": rfoot,
        "03_body_porcelain.png": body,
        "04_wing_left.png": lwing,
        "05_wing_right.png": rwing,
        "06_eye_left.png": leye_ball,
        "07_eye_right.png": reye_ball,
        "08_eyelid_left.png": leyelid,
        "09_eyelid_right.png": reyelid,
        "10_beak.png": beak
    }
    
    print("Master Rig Layers:")
    for fname, l_img in layers.items():
        p = os.path.join(out_dir, fname)
        cv2.imwrite(p, l_img)
        # Check green spill
        m = l_img[:, :, 3] > 20
        g_spill = 0
        if np.sum(m) > 0:
            b_c, g_c, r_c = l_img[m, 0], l_img[m, 1], l_img[m, 2]
            g_spill = np.sum((g_c > 90) & (r_c < 60) & (b_c < 60))
        print(f"  {fname:22s} | Non-zero alpha: {np.sum(l_img[:, :, 3] > 0):6d} px | Green spill: {g_spill} px")

    # Build Preview Grid
    grid = np.zeros((3 * 256, 4 * 256, 4), dtype=np.uint8)
    names = list(layers.keys())
    for idx, name in enumerate(names):
        r_idx = idx // 4
        c_idx = idx % 4
        y0, y1 = r_idx * 256, (r_idx + 1) * 256
        x0, x1 = c_idx * 256, (c_idx + 1) * 256
        
        l_img = cv2.resize(layers[name], (256, 256), interpolation=cv2.INTER_AREA)
        cb = np.full((256, 256, 3), 45, dtype=np.uint8)
        for y in range(0, 256, 16):
            for x in range(0, 256, 16):
                if ((x // 16) + (y // 16)) % 2 == 0:
                    cb[y:y+16, x:x+16] = 60
        alpha = l_img[:, :, 3:4] / 255.0
        comp_rgb = (l_img[:, :, :3] * alpha + cb * (1.0 - alpha)).astype(np.uint8)
        comp_rgba = np.dstack([comp_rgb, np.full((256, 256), 255, dtype=np.uint8)])
        cv2.putText(comp_rgba, name.replace(".png", ""), (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        grid[y0:y1, x0:x1] = comp_rgba
        
    preview_path = "mascots/owluko/rig_layers_preview.png"
    cv2.imwrite(preview_path, grid)
    print("Saved preview:", preview_path)

if __name__ == "__main__":
    build()
