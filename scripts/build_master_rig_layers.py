import cv2
import numpy as np
import os

def build():
    front_path = "mascots/owluko/owluko_turnaround_view_1_front.png"
    img = cv2.imread(front_path, cv2.IMREAD_UNCHANGED)
    h, w, c = img.shape
    out_dir = "mascots/owluko/rig_layers"
    os.makedirs(out_dir, exist_ok=True)
    
    # 0. CHROMA DESPILL
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

    # 2. FEET (BEHIND BODY)
    # Left foot: X in [155, 245], Y in [415, 489]
    # Right foot: X in [265, 357], Y in [415, 489]
    lfoot = np.zeros_like(img_clean)
    rfoot = np.zeros_like(img_clean)
    
    # Mask of the feet from img_clean
    lf_mask = (img_clean[:, :, 3] > 20) & (np.arange(h)[:, None] >= 420) & (np.arange(w)[None, :] < 252)
    rf_mask = (img_clean[:, :, 3] > 20) & (np.arange(h)[:, None] >= 420) & (np.arange(w)[None, :] >= 260)
    
    lfoot[lf_mask] = img_clean[lf_mask]
    rfoot[rf_mask] = img_clean[rf_mask]
    
    # Inpaint ankle tops upward to Y=410 so they slip cleanly behind the belly
    for foot, f_mask, cx, cy in [(lfoot, lf_mask, 204, 420), (rfoot, rf_mask, 308, 420)]:
        # Extend ankle up by 12px
        ankle_ext = np.zeros((h, w), dtype=np.uint8)
        cv2.ellipse(ankle_ext, (cx, cy), (16, 12), 0, 0, 360, 255, -1)
        ankle_ext[foot[:, :, 3] > 20] = 0
        infilled = cv2.inpaint(foot[:, :, :3], ankle_ext, 7, cv2.INPAINT_TELEA)
        foot[:, :, :3] = infilled
        foot[ankle_ext > 0, 3] = 255
        # Soften very top 3 rows
        for y in range(cy - 12, cy - 8):
            foot[y, :, 3] = (foot[y, :, 3] * ((y - (cy - 12)) / 4.0)).astype(np.uint8)

    # 3. BODY PORCELAIN
    # The body is the porcelain egg capsule.
    # The lower belly curves down to Y=444.
    # We remove the feet from the body, inpainting the lower belly curve smoothly:
    body = img_clean.copy()
    # Feet removal from body: below the belly curve
    for x in range(w):
        dx = (x - 256.0) / 95.0
        if abs(dx) <= 1.0:
            y_belly = int(round(444.0 - dx**2 * 18.0))
            # Any feet pixels below the belly contour are cleared
            body[y_belly + 1:, x, :] = 0
        else:
            # Outside belly, feet do not exist below y=440
            body[435:, x, :] = 0
            
    # Inpaint belly where the feet touched the belly front rim (Y in [430, 444])
    belly_touch = np.zeros((h, w), dtype=np.uint8)
    for x in range(165, 345):
        dx = (x - 256.0) / 95.0
        y_belly = int(round(444.0 - dx**2 * 18.0))
        belly_touch[y_belly - 10 : y_belly + 1, x] = 255
    belly_touch = belly_touch & (body[:, :, 3] > 20).astype(np.uint8) * 255
    body[:, :, :3] = cv2.inpaint(body[:, :, :3], belly_touch, 7, cv2.INPAINT_TELEA)

    # Inpaint flanks behind wings:
    # Under the wings, extend porcelain body slightly so wing flapping reveals clean porcelain
    flank_touch = np.zeros((h, w), dtype=np.uint8)
    for y in range(180, 412):
        flank_touch[y, 118:136] = 255
        flank_touch[y, 374:392] = 255
    flank_touch = flank_touch & (body[:, :, 3] > 20).astype(np.uint8) * 255
    body[:, :, :3] = cv2.inpaint(body[:, :, :3], flank_touch, 7, cv2.INPAINT_TELEA)

    # 4. WINGS (LEFT & RIGHT)
    lwing = np.zeros_like(img_clean)
    rwing = np.zeros_like(img_clean)
    lw_mask = (img_clean[:, :, 3] > 20) & (np.arange(w)[None, :] <= 134) & (np.arange(h)[:, None] >= 180) & (np.arange(h)[:, None] <= 412)
    rw_mask = (img_clean[:, :, 3] > 20) & (np.arange(w)[None, :] >= 376) & (np.arange(h)[:, None] >= 180) & (np.arange(h)[:, None] <= 412)
    lwing[lw_mask] = img_clean[lw_mask]
    rwing[rw_mask] = img_clean[rw_mask]
    
    # 5. EYES: EYEBALLS (AMBER ORBS)
    # Left eye center ~ (193, 160), right eye center ~ (315, 163)
    leye_ball = np.zeros_like(img_clean)
    reye_ball = np.zeros_like(img_clean)
    
    for eball, cx, cy in [(leye_ball, 193, 160), (reye_ball, 315, 163)]:
        # Extract amber orb
        for y in range(cy - 25, cy + 26):
            for x in range(cx - 25, cx + 26):
                dist = np.sqrt((x - cx)**2 + (y - cy)**2)
                if dist <= 22:
                    eball[y, x] = img_clean[y, x]
        # Inpaint top of eyeball under eyelid to form complete sphere
        miss = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(miss, (cx, cy), 22, 255, -1)
        miss[eball[:, :, 3] > 20] = 0
        eball[:, :, :3] = cv2.inpaint(eball[:, :, :3], miss, 5, cv2.INPAINT_TELEA)
        eball[miss > 0, 3] = 255
        # Soft feathering on outer 2px of eyeball
        for y in range(cy - 24, cy + 25):
            for x in range(cx - 24, cx + 25):
                dist = np.sqrt((x - cx)**2 + (y - cy)**2)
                if dist > 20 and dist <= 22:
                    eball[y, x, 3] = int(255 * (22.0 - dist) / 2.0)
                elif dist > 22:
                    eball[y, x, 3] = 0

    # 6. EYELIDS (PORCELAIN BLINK HOODS)
    # Porcelain eyelid that covers the eye socket when blinking
    leyelid = np.zeros_like(img_clean)
    reyelid = np.zeros_like(img_clean)
    
    # Eyelid shape: porcelain crescent covering the eye from top
    for lid, cx, cy in [(leyelid, 193, 160), (reyelid, 315, 163)]:
        for y in range(cy - 30, cy + 24):
            for x in range(cx - 28, cx + 29):
                dist = np.sqrt((x - cx)**2 + (y - cy)**2)
                if dist <= 25:
                    # Sample porcelain eyelid from img_clean
                    b_val, g_val, r_val = img_clean[y, x, :3]
                    is_porcelain = (r_val > 180 and g_val > 165 and b_val > 145) or (y < cy - 8)
                    if is_porcelain:
                        lid[y, x] = img_clean[y, x]
                        
    # 7. BEAK
    beak = np.zeros_like(img_clean)
    beak_mask = np.zeros((h, w), dtype=bool)
    for y in range(162, 236):
        t = (y - 162.0) / 74.0
        hw = int(round(18.0 * (1.0 - 0.72 * t)))
        beak_mask[y, 256 - hw : 256 + hw + 1] = True
    beak_mask = beak_mask & (img_clean[:, :, 3] > 20)
    beak[beak_mask] = img_clean[beak_mask]

    # Save layers
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
    
    for fname, l_img in layers.items():
        p = os.path.join(out_dir, fname)
        cv2.imwrite(p, l_img)
        
    print("Master layers successfully saved to:", out_dir)
    
    # Test recomposite
    comp = shadow.copy()
    for name in ["01_foot_left.png", "02_foot_right.png", "03_body_porcelain.png", "04_wing_left.png", "05_wing_right.png", "10_beak.png"]:
        l_img = layers[name]
        a = l_img[:, :, 3:4] / 255.0
        comp_rgb = comp[:, :, :3] * (1.0 - a) + l_img[:, :, :3] * a
        comp_a = np.maximum(comp[:, :, 3:4], l_img[:, :, 3:4])
        comp = np.dstack([comp_rgb.astype(np.uint8), comp_a.astype(np.uint8)])
        
    cv2.imwrite("mascots/owluko/master_recomposite.png", comp)
    print("Saved master recomposite: mascots/owluko/master_recomposite.png")

if __name__ == "__main__":
    build()
