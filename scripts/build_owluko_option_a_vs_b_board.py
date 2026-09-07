import cv2
import numpy as np
import shutil
import os

def create_board():
    ref = cv2.imread('mascots/owluko/components/mascot_assembled_ref.png')
    opt_a = cv2.imread('mascots/owluko/owluko_hifi_frame0.png')
    opt_b = cv2.imread('mascots/owluko/owluko_wave_p1_rest.png')

    card_w = 480
    card_h = 520
    header_h = 130
    margin = 32
    gap = 24
    total_w = margin * 2 + 3 * card_w + 2 * gap
    total_h = margin * 2 + header_h + card_h + 40

    canvas = np.full((total_h, total_w, 3), (250, 248, 246), dtype=np.uint8)

    # Header
    cv2.rectangle(canvas, (margin, margin), (total_w - margin, margin + header_h), (255, 255, 255), -1)
    cv2.rectangle(canvas, (margin, margin), (total_w - margin, margin + header_h), (220, 215, 205), 2)

    cv2.putText(canvas, "COMPARAISON DIRECTE : OPTION A (SPRITES DECOUPES) VS OPTION B (VECTORIEL PUR)",
                (margin + 24, margin + 42), cv2.FONT_HERSHEY_DUPLEX, 0.85, (30, 25, 20), 2, cv2.LINE_AA)
    cv2.putText(canvas, "Verdict Technique & Radical Honesty : Pourquoi le Vectoriel Pur Rive surpasse le decoupage raster",
                (margin + 24, margin + 74), cv2.FONT_HERSHEY_SIMPLEX, 0.60, (100, 90, 80), 1, cv2.LINE_AA)
    cv2.putText(canvas, "Ref: Panel 1 Planche  |  Option A: 500.7 KB (Sans masque, flou 300px)  |  Option B: 15.8 KB (Masque complet, net infini)",
                (margin + 24, margin + 104), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (180, 80, 30), 2, cv2.LINE_AA)

    y_card = margin + header_h + 24

    cards = [
        ("1. REFERENCE CIBLE (Planche Panel 1)", ref, (70, 60, 50), (215, 210, 200),
         ["Mascotte assemblee de reference", "Presence du masque facial d'effraie", "Plastron ventral duvet creme", "Poids : Image source"]),
        ("2. OPTION A : SPRITES RIVE (.riv 500.7 KB)", opt_a, (180, 50, 40), (180, 160, 220),
         ["Base Panel 2 nue (sans masque d'effraie)", "Yeux colles sur l'oeuf sans orbites", "Ailes plates collees sur les flancs", "Resolution basse (300px upscaled)"]),
        ("3. OPTION B : VECTORIEL PUR (.riv 15.8 KB)", opt_b, (30, 120, 40), (160, 210, 160),
         ["Masque facial d'effraie complet", "Plastron ventral en coeur soyeux", "Ailes galbees parfaitement integrees", "Nettete infinie 60 FPS (32x plus leger)"])
    ]

    for i, (title, img, title_col, border_col, bullets) in enumerate(cards):
        x = margin + i * (card_w + gap)

        # Draw card background
        cv2.rectangle(canvas, (x, y_card), (x + card_w, y_card + card_h), (255, 255, 255), -1)
        cv2.rectangle(canvas, (x, y_card), (x + card_w, y_card + card_h), border_col, 2)

        # Draw Title
        cv2.rectangle(canvas, (x, y_card), (x + card_w, y_card + 38), (245, 242, 238), -1)
        cv2.putText(canvas, title, (x + 12, y_card + 25), cv2.FONT_HERSHEY_DUPLEX, 0.48, title_col, 1, cv2.LINE_AA)

        # Place image
        if img is not None:
            # Crop center if large
            if img.shape[0] == 1024:
                crop = img[100:920, 150:870]
            else:
                crop = img
            h, w = crop.shape[:2]
            scale = min((card_w - 24) / w, 340 / h)
            nw, nh = int(w * scale), int(h * scale)
            resized = cv2.resize(crop, (nw, nh), interpolation=cv2.INTER_LANCZOS4)

            ox = x + (card_w - nw) // 2
            oy = y_card + 48 + (340 - nh) // 2
            canvas[oy:oy+nh, ox:ox+nw] = resized

        # Draw Bullets
        y_text = y_card + 400
        for b in bullets:
            cv2.circle(canvas, (x + 20, y_text - 4), 3, title_col, -1)
            cv2.putText(canvas, b, (x + 32, y_text), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (50, 45, 40), 1, cv2.LINE_AA)
            y_text += 22

    out_path = "mascots/owluko/owluko_option_a_vs_b_comparison.png"
    cv2.imwrite(out_path, canvas)
    print(f"Saved comparison board to {out_path} ({total_w}x{total_h})")

    brain_dir = "/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68"
    if os.path.exists(brain_dir):
        shutil.copyfile(out_path, os.path.join(brain_dir, "owluko_option_a_vs_b_comparison.png"))
        print("Copied to brain directory.")

create_board()
