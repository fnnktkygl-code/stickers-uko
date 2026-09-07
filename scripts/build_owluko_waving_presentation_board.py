import cv2
import numpy as np
import os
import shutil

def create_waving_storyboard_board():
    ref_panels = [
        ("Panel 1: Repos (Idle)", "scratch/waving_panels/panel_1.png"),
        ("Panel 2: Lever d'aile (Ascent)", "scratch/waving_panels/panel_2.png"),
        ("Panel 3: Coucou interieur", "scratch/waving_panels/panel_3.png"),
        ("Panel 4: Balancement exterieur", "scratch/waving_panels/panel_4.png"),
        ("Panel 5: Sourire yeux fermes (^ ^)", "scratch/waving_panels/panel_5.png"),
        ("Panel 6: Retour au repos", "scratch/waving_panels/panel_6.png"),
    ]

    rive_panels = [
        ("Rive t=0.00s (f=0)", "mascots/owluko/owluko_wave_p1_rest.png"),
        ("Rive t=0.75s (f=45)", "mascots/owluko/owluko_wave_p2_raising.png"),
        ("Rive t=1.42s (f=85)", "mascots/owluko/owluko_wave_p3_inward.png"),
        ("Rive t=1.83s (f=110)", "mascots/owluko/owluko_wave_p4_outward.png"),
        ("Rive t=2.37s (f=142)", "mascots/owluko/owluko_wave_p5_smile.png"),
        ("Rive t=4.00s (f=240)", "mascots/owluko/owluko_wave_p6_return.png"),
    ]

    panel_w = 340
    panel_h = 320
    header_h = 130
    row_gap = 40
    col_gap = 16
    margin = 32
    n_cols = 6

    total_w = margin * 2 + n_cols * panel_w + (n_cols - 1) * col_gap
    total_h = margin * 2 + header_h + 2 * panel_h + row_gap + 70

    canvas = np.full((total_h, total_w, 3), (250, 248, 246), dtype=np.uint8)

    # Header Card
    cv2.rectangle(canvas, (margin, margin), (total_w - margin, margin + header_h), (255, 255, 255), -1)
    cv2.rectangle(canvas, (margin, margin), (total_w - margin, margin + header_h), (220, 215, 205), 2)

    cv2.putText(canvas, "OWLUKO WAVING -- ALIGNEMENT STORYBOARD CANONIQUE (6 PHASES)",
                (margin + 24, margin + 42), cv2.FONT_HERSHEY_DUPLEX, 0.95, (30, 25, 20), 2, cv2.LINE_AA)
    cv2.putText(canvas, "Fidelite 1:1 au Storyboard Utilisateur | Rive 60 FPS (Duree 4.0s) | Maintien du salut sans battement spastique",
                (margin + 24, margin + 74), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (100, 90, 80), 1, cv2.LINE_AA)
    cv2.putText(canvas, "Ligne 1: Storyboard Reference (media_1788763379758)  vs  Ligne 2: Rive Pure Vector Render (.riv 15.8 KB)",
                (margin + 24, margin + 104), cv2.FONT_HERSHEY_SIMPLEX, 0.60, (180, 80, 30), 2, cv2.LINE_AA)

    y_ref = margin + header_h + 24
    y_rive = y_ref + panel_h + row_gap

    # Row Titles
    cv2.putText(canvas, "[1] STORYBOARD DE REFERENCE (CANONIQUE UTILISATEUR)", (margin, y_ref - 8),
                cv2.FONT_HERSHEY_DUPLEX, 0.65, (70, 60, 50), 2, cv2.LINE_AA)
    cv2.putText(canvas, "[2] RIVE NATIVE VECTOR RENDER (.RIV A 60 FPS)", (margin, y_rive - 8),
                cv2.FONT_HERSHEY_DUPLEX, 0.65, (30, 110, 40), 2, cv2.LINE_AA)

    # Place Ref Panels
    for i, (title, path) in enumerate(ref_panels):
        x = margin + i * (panel_w + col_gap)
        img = cv2.imread(path)
        if img is not None:
            h, w = img.shape[:2]
            scale = min((panel_w - 8) / w, (panel_h - 40) / h)
            nw, nh = int(w * scale), int(h * scale)
            resized = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_LANCZOS4)

            cv2.rectangle(canvas, (x, y_ref), (x + panel_w, y_ref + panel_h), (255, 255, 255), -1)
            cv2.rectangle(canvas, (x, y_ref), (x + panel_w, y_ref + panel_h), (215, 210, 200), 1)

            ox = x + (panel_w - nw) // 2
            oy = y_ref + (panel_h - 36 - nh) // 2
            canvas[oy:oy+nh, ox:ox+nw] = resized

            cv2.rectangle(canvas, (x, y_ref + panel_h - 32), (x + panel_w, y_ref + panel_h), (240, 235, 225), -1)
            cv2.putText(canvas, title, (x + 8, y_ref + panel_h - 11),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.44, (40, 35, 30), 1, cv2.LINE_AA)

    # Place Rive Panels (Fit complete 1024x1024 artboard into card with zero cropping!)
    for i, (title, path) in enumerate(rive_panels):
        x = margin + i * (panel_w + col_gap)
        img = cv2.imread(path)
        if img is not None:
            h, w = img.shape[:2]
            scale = min((panel_w - 8) / w, (panel_h - 40) / h)
            nw, nh = int(w * scale), int(h * scale)
            resized = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_LANCZOS4)

            cv2.rectangle(canvas, (x, y_rive), (x + panel_w, y_rive + panel_h), (255, 255, 255), -1)
            cv2.rectangle(canvas, (x, y_rive), (x + panel_w, y_rive + panel_h), (160, 200, 160), 2)

            ox = x + (panel_w - nw) // 2
            oy = y_rive + (panel_h - 36 - nh) // 2
            canvas[oy:oy+nh, ox:ox+nw] = resized

            cv2.rectangle(canvas, (x, y_rive + panel_h - 32), (x + panel_w, y_rive + panel_h), (230, 245, 230), -1)
            cv2.putText(canvas, title, (x + 8, y_rive + panel_h - 11),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.48, (20, 90, 30), 1, cv2.LINE_AA)

    out_path = "mascots/owluko/owluko_waving_storyboard_comparison.png"
    cv2.imwrite(out_path, canvas)
    print(f"Saved storyboard comparison board to {out_path} ({total_w}x{total_h})")

    brain_dir = "/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68"
    if os.path.exists(brain_dir):
        shutil.copyfile(out_path, os.path.join(brain_dir, "owluko_waving_storyboard_comparison.png"))
        print("Copied to brain directory.")
    return True

if __name__ == "__main__":
    create_waving_storyboard_board()
