import cv2
import numpy as np
import os

def dissect():
    front_path = "mascots/owluko/owluko_turnaround_view_1_front.png"
    img = cv2.imread(front_path, cv2.IMREAD_UNCHANGED)
    h, w = img.shape[:2]
    
    out_dir = "mascots/owluko/rig_layers"
    os.makedirs(out_dir, exist_ok=True)
    
    # 1. Isolate Feet
    # Feet are in Y in [410, 489]
    feet_mask = np.zeros((h, w), dtype=np.uint8)
    # Left foot: X in [155, 235], Y in [410, 489]
    # Right foot: X in [277, 357], Y in [410, 489]
    lfoot_layer = np.zeros_like(img)
    rfoot_layer = np.zeros_like(img)
    
    # Left foot mask
    lf_mask = (img[:, :, 3] > 20)
    lf_mask[:415, :] = False
    lf_mask[:, 245:] = False
    lfoot_layer[lf_mask] = img[lf_mask]
    
    # Right foot mask
    rf_mask = (img[:, :, 3] > 20)
    rf_mask[:415, :] = False
    rf_mask[:, :265] = False
    rfoot_layer[rf_mask] = img[rf_mask]
    
    # 2. Isolate Beak
    # Beak is centered around X=256, Y in [165, 235]
    beak_layer = np.zeros_like(img)
    beak_mask = np.zeros((h, w), dtype=bool)
    # Beak triangular/seed bounding box
    for y in range(165, 235):
        # width narrows from 32 down to 10
        t = (y - 165) / 70.0
        hw = int(round(16 * (1.0 - 0.7 * t)))
        beak_mask[y, 256-hw:256+hw] = True
    beak_mask = beak_mask & (img[:, :, 3] > 20)
    beak_layer[beak_mask] = img[beak_mask]
    
    # 3. Isolate Eyes & Eyelids
    # Left eye: X in [150, 225], Y in [135, 185]
    # Right eye: X in [285, 360], Y in [135, 185]
    leye_layer = np.zeros_like(img)
    reye_layer = np.zeros_like(img)
    
    leye_mask = np.zeros((h, w), dtype=bool)
    cv2.circle(leye_mask.view(np.uint8), (193, 160), 38, 1, -1)
    leye_mask = (leye_mask == 1) & (img[:, :, 3] > 20)
    leye_layer[leye_mask] = img[leye_mask]
    
    reye_mask = np.zeros((h, w), dtype=bool)
    cv2.circle(reye_mask.view(np.uint8), (315, 163), 38, 1, -1)
    reye_mask = (reye_mask == 1) & (img[:, :, 3] > 20)
    reye_layer[reye_mask] = img[reye_mask]
    
    # 4. Isolate Wings
    # Left wing: X in [87, 135], Y in [180, 410]
    # Right wing: X in [375, 424], Y in [180, 410]
    lwing_layer = np.zeros_like(img)
    rwing_layer = np.zeros_like(img)
    
    lwing_mask = (img[:, :, 3] > 20) & (np.arange(w) < 135)[None, :] & (np.arange(h) >= 180)[:, None] & (np.arange(h) <= 415)[:, None]
    lwing_layer[lwing_mask] = img[lwing_mask]
    
    rwing_mask = (img[:, :, 3] > 20) & (np.arange(w) > 375)[None, :] & (np.arange(h) >= 180)[:, None] & (np.arange(h) <= 415)[:, None]
    rwing_layer[rwing_mask] = img[rwing_mask]
    
    # 5. Clean Inpainted Porcelain Body
    # Inpaint behind eyes, beak, and feet so the body is a 100% continuous porcelain canvas
    body_clean = img.copy()
    inpaint_mask = (beak_mask | leye_mask | reye_mask | lf_mask | rf_mask).astype(np.uint8) * 255
    # Dilate inpaint mask slightly
    inpaint_mask = cv2.dilate(inpaint_mask, np.ones((7, 7), np.uint8))
    # Keep only inside body alpha
    inpaint_mask = inpaint_mask & (img[:, :, 3] > 20).astype(np.uint8) * 255
    
    # Telea inpainting on RGB
    bgr_clean = cv2.inpaint(body_clean[:, :, :3], inpaint_mask, 9, cv2.INPAINT_TELEA)
    body_clean[:, :, :3] = bgr_clean
    
    # Save all layers
    layers = [
        ("01_body_porcelain.png", body_clean),
        ("02_wing_left.png", lwing_layer),
        ("03_wing_right.png", rwing_layer),
        ("04_eye_left.png", leye_layer),
        ("05_eye_right.png", reye_layer),
        ("06_beak.png", beak_layer),
        ("07_foot_left.png", lfoot_layer),
        ("08_foot_right.png", rfoot_layer)
    ]
    
    for fname, l_img in layers:
        p = os.path.join(out_dir, fname)
        cv2.imwrite(p, l_img)
        print(f"Saved layer: {p} (non-zero alpha: {np.sum(l_img[:, :, 3] > 0)} px)")
        
    # Recomposite verification
    comp = np.zeros_like(img)
    for _, l_img in layers:
        a = l_img[:, :, 3:4] / 255.0
        comp = (l_img[:, :, :3] * a + comp[:, :, :3] * (1.0 - a)).astype(np.uint8)
        comp_a = np.maximum(comp, l_img[:, :, 3:4])
        
    print("Dissection complete!")

if __name__ == "__main__":
    dissect()
