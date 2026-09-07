import cv2
import numpy as np
import os

def build_v2_layers():
    front_path = "mascots/owluko/owluko_turnaround_view_1_front.png"
    back_path = "mascots/owluko/owluko_turnaround_view_4_back.png"
    img = cv2.imread(front_path, cv2.IMREAD_UNCHANGED)
    back_img = cv2.imread(back_path, cv2.IMREAD_UNCHANGED)
    h, w, c = img.shape
    
    out_dir = "mascots/owluko/rig_layers_v2"
    os.makedirs(out_dir, exist_ok=True)
    
    # -------------------------------------------------------------
    # 0. GROUND CONTACT SHADOW
    # -------------------------------------------------------------
    shadow = np.zeros((h, w, 4), dtype=np.uint8)
    # Elliptical contact shadow under left and right feet
    cv2.ellipse(shadow, (198, 487), (38, 9), 0, 0, 360, (20, 20, 25, 160), -1)
    cv2.ellipse(shadow, (312, 487), (38, 9), 0, 0, 360, (20, 20, 25, 160), -1)
    # Central soft ambient shadow
    cv2.ellipse(shadow, (256, 488), (75, 11), 0, 0, 360, (25, 25, 30, 80), -1)
    # Soft gaussian blur on shadow
    shadow[:, :, 3] = cv2.GaussianBlur(shadow[:, :, 3], (25, 25), 0)
    
    # -------------------------------------------------------------
    # 1. FEET ISOLATION (ZERO GREEN, CLEAN PORCELAIN AVIA)
    # -------------------------------------------------------------
    lfoot = np.zeros_like(img)
    rfoot = np.zeros_like(img)
    
    # Left foot: ankle emerges from y=415, down to y=489, x in [155, 245]
    lf_mask = (img[:, :, 3] > 20) & (np.arange(h)[:, None] >= 415) & (np.arange(w)[None, :] < 250)
    # Exclude any pixels that belong to the belly dome contour
    for y in range(415, 445):
        for x in range(155, 250):
            # Check if this pixel is inside the belly interior
            dx = (x - 256.0) / 95.0
            y_belly = 444.0 - dx**2 * 18.0
            if y < y_belly - 12.0:
                lf_mask[y, x] = False
                
    # Right foot: ankle emerges from y=415, down to y=489, x in [262, 357]
    rf_mask = (img[:, :, 3] > 20) & (np.arange(h)[:, None] >= 415) & (np.arange(w)[None, :] >= 262)
    for y in range(415, 445):
        for x in range(262, 357):
            dx = (x - 256.0) / 95.0
            y_belly = 444.0 - dx**2 * 18.0
            if y < y_belly - 12.0:
                rf_mask[y, x] = False
                
    lfoot[lf_mask] = img[lf_mask]
    rfoot[rf_mask] = img[rf_mask]
    
    # Feather top of ankle slightly so it slides smoothly behind/under the belly
    for y in range(415, 428):
        alpha_mult = (y - 415.0) / 13.0
        lfoot[y, :, 3] = (lfoot[y, :, 3] * alpha_mult).astype(np.uint8)
        rfoot[y, :, 3] = (rfoot[y, :, 3] * alpha_mult).astype(np.uint8)

    # -------------------------------------------------------------
    # 2. WINGS ISOLATION
    # -------------------------------------------------------------
    lwing = np.zeros_like(img)
    rwing = np.zeros_like(img)
    
    # Left wing: X in [87, 136], Y in [180, 410]
    lw_mask = (img[:, :, 3] > 20) & (np.arange(w)[None, :] <= 136) & (np.arange(h)[:, None] >= 180) & (np.arange(h)[:, None] <= 415)
    # Right wing: X in [374, 425], Y in [180, 410]
    rw_mask = (img[:, :, 3] > 20) & (np.arange(w)[None, :] >= 374) & (np.arange(h)[:, None] >= 180) & (np.arange(h)[:, None] <= 415)
    
    lwing[lw_mask] = img[lw_mask]
    rwing[rw_mask] = img[rw_mask]
    
    # Smooth inner edge of wings so there is no harsh pixelated cut
    # We soften the inner 2 pixels of alpha
    for y in range(180, 415):
        # for left wing, inner edge is at max x
        xs = np.where(lwing[y, :, 3] > 0)[0]
        if len(xs) > 0:
            xmax = xs.max()
            if xmax > 0:
                lwing[y, xmax, 3] = int(lwing[y, xmax, 3] * 0.6)
                if xmax - 1 >= 0:
                    lwing[y, xmax - 1, 3] = int(lwing[y, xmax - 1, 3] * 0.85)
                    
        # for right wing, inner edge is at min x
        xs = np.where(rwing[y, :, 3] > 0)[0]
        if len(xs) > 0:
            xmin = xs.min()
            if xmin < w - 1:
                rwing[y, xmin, 3] = int(rwing[y, xmin, 3] * 0.6)
                if xmin + 1 < w:
                    rwing[y, xmin + 1, 3] = int(rwing[y, xmin + 1, 3] * 0.85)

    # -------------------------------------------------------------
    # 3. BEAK ISOLATION
    # -------------------------------------------------------------
    beak = np.zeros_like(img)
    beak_mask = np.zeros((h, w), dtype=bool)
    for y in range(162, 236):
        t = (y - 162.0) / 74.0
        hw = int(round(18.0 * (1.0 - 0.72 * t)))
        beak_mask[y, 256 - hw : 256 + hw + 1] = True
    beak_mask = beak_mask & (img[:, :, 3] > 20)
    beak[beak_mask] = img[beak_mask]

    # -------------------------------------------------------------
    # 4. EYES & EYELIDS ISOLATION
    # -------------------------------------------------------------
    # Left eye center ~ (193, 160), radius ~ 36
    # Right eye center ~ (315, 163), radius ~ 36
    leye_ball = np.zeros_like(img)
    reye_ball = np.zeros_like(img)
    leyelid = np.zeros_like(img)
    reyelid = np.zeros_like(img)
    
    # Eyeball circle masks
    leye_circ = np.zeros((h, w), dtype=np.uint8)
    reye_circ = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(leye_circ, (193, 160), 36, 255, -1)
    cv2.circle(reye_circ, (315, 163), 36, 255, -1)
    
    # Separate eyeball amber iris from upper porcelain eyelid
    # The eyelid covers roughly y <= 152 for left eye, y <= 155 for right eye
    for y in range(h):
        for x in range(w):
            if leye_circ[y, x] and img[y, x, 3] > 20:
                # Eyelid threshold based on amber color vs porcelain color
                b, g, r = img[y, x, :3]
                # Amber iris has high R/B ratio and dark pupil/golden hue
                is_amber = (r > 100 and g > 60 and b < 50) or (r < 80 and g < 60 and b < 50)  # pupil or amber
                if is_amber and y >= 148:
                    leye_ball[y, x] = img[y, x]
                else:
                    leyelid[y, x] = img[y, x]
                    
            if reye_circ[y, x] and img[y, x, 3] > 20:
                b, g, r = img[y, x, :3]
                is_amber = (r > 100 and g > 60 and b < 50) or (r < 80 and g < 60 and b < 50)
                if is_amber and y >= 150:
                    reye_ball[y, x] = img[y, x]
                else:
                    reyelid[y, x] = img[y, x]

    # Fill the eyeball completely behind the eyelid so when eyelid moves/blinks, eyeball is a full round glassy sphere!
    # Inpaint eyeball top with amber iris gradient
    for eball, cx, cy, r in [(leye_ball, 193, 160, 36), (reye_ball, 315, 163, 36)]:
        missing_mask = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(missing_mask, (cx, cy), r - 1, 255, -1)
        missing_mask[eball[:, :, 3] > 20] = 0
        missing_mask = missing_mask & (img[:, :, 3] > 20)
        
        # Inpaint amber eyeball
        amber_sample = eball[cy:cy+15, cx-10:cx+10, :3]
        if np.sum(eball[:, :, 3] > 20) > 0:
            infilled = cv2.inpaint(eball[:, :, :3], missing_mask, 7, cv2.INPAINT_TELEA)
            eball[:, :, :3] = infilled
            eball[missing_mask > 0, 3] = 255

    # -------------------------------------------------------------
    # 5. PORCELAIN BODY CAPSULE (CLEAN, NO FEET, NO WINGS DUPLICATE)
    # -------------------------------------------------------------
    body = img.copy()
    
    # 5A. Completely eliminate feet from body
    body[445:, :, :] = 0
    # Belly contour interpolation
    belly_mask = np.zeros((h, w), dtype=np.uint8)
    for x in range(150, 365):
        dx = (x - 256.0) / 95.0
        if abs(dx) <= 1.0:
            y_max = int(round(444.0 - dx**2 * 18.0))
            for y in range(415, y_max + 1):
                if lf_mask[y, x] or rf_mask[y, x]:
                    belly_mask[y, x] = 255
                    body[y, x, 3] = 255
            # Clear anything below y_max
            body[y_max + 1:, x, :] = 0
            
    # Inpaint lower belly using porcelain color
    bgr_clean = cv2.inpaint(body[:, :, :3], belly_mask, 7, cv2.INPAINT_TELEA)
    body[:, :, :3] = bgr_clean
    
    # 5B. Inpaint behind beak & eyes so body has continuous porcelain face
    face_mask = (beak_mask | (leye_circ > 0) | (reye_circ > 0)).astype(np.uint8) * 255
    face_mask = face_mask & (body[:, :, 3] > 20).astype(np.uint8) * 255
    # Smooth inpaint face eye sockets with Telea
    body_face_clean = cv2.inpaint(body[:, :, :3], face_mask, 9, cv2.INPAINT_TELEA)
    body[:, :, :3] = body_face_clean
    
    # 5C. Smooth flanks behind wings using porcelain texture from back view or Telea inpaint
    # Flank regions where wings attach:
    flank_mask = (lw_mask | rw_mask).astype(np.uint8) * 255
    # Keep only outer 15 pixels of flank mask to retain body volume behind wings
    flank_inpaint_mask = cv2.dilate(flank_mask, np.ones((5, 5), np.uint8)) & (body[:, :, 3] > 20).astype(np.uint8) * 255
    body_flank_clean = cv2.inpaint(body[:, :, :3], flank_inpaint_mask, 9, cv2.INPAINT_TELEA)
    body[:, :, :3] = body_flank_clean

    # -------------------------------------------------------------
    # SAVE ALL RIG LAYERS
    # -------------------------------------------------------------
    layer_dict = {
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
    
    print("Saving v2 rig layers:")
    for fname, l_img in layer_dict.items():
        p = os.path.join(out_dir, fname)
        cv2.imwrite(p, l_img)
        non_zero = np.sum(l_img[:, :, 3] > 0)
        # Check green spill:
        g_spill = 0
        if non_zero > 0:
            m = l_img[:, :, 3] > 20
            b, g, r = l_img[m, 0], l_img[m, 1], l_img[m, 2]
            g_spill = np.sum((g > 90) & (r < 60) & (b < 60))
        print(f"  {fname:22s} | Alpha px: {non_zero:6d} | Green spill px: {g_spill}")

    # Build verification preview grid (3 rows x 4 cols)
    grid = np.zeros((3 * 256, 4 * 256, 4), dtype=np.uint8)
    names = list(layer_dict.keys())
    for idx, name in enumerate(names):
        r = idx // 4
        c = idx % 4
        y0, y1 = r * 256, (r + 1) * 256
        x0, x1 = c * 256, (c + 1) * 256
        
        l_img = cv2.resize(layer_dict[name], (256, 256), interpolation=cv2.INTER_AREA)
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
        
    cv2.imwrite("mascots/owluko/rig_layers_v2_preview.png", grid)
    print("Saved preview: mascots/owluko/rig_layers_v2_preview.png")

if __name__ == "__main__":
    build_v2_layers()
