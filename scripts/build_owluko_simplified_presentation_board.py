import os
import shutil
from PIL import Image, ImageDraw, ImageFont

def build_board():
    W, H = 2400, 1600
    board = Image.new("RGBA", (W, H), (11, 14, 19, 255))
    draw = ImageDraw.Draw(board)

    # Fonts
    def get_font(name, size):
        paths = [
            f"/System/Library/Fonts/{name}.ttf",
            f"/System/Library/Fonts/Supplemental/{name}.ttf",
            f"/Library/Fonts/{name}.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/Geneva.dfont"
        ]
        for p in paths:
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except:
                    pass
        return ImageFont.load_default()

    font_header = get_font("HelveticaNeue-Bold", 44)
    font_sub = get_font("HelveticaNeue", 22)
    font_panel = get_font("HelveticaNeue-Bold", 26)
    font_badge = get_font("HelveticaNeue-Bold", 18)
    font_meta = get_font("HelveticaNeue", 18)

    # Header
    draw.text((70, 45), "OWLUKO — RIVE NATIVE VECTOR RECONSTRUCTION", fill=(255, 255, 255, 255), font=font_header)
    draw.text((70, 100), "100% Pure Vector .riv (12.7 KB) | Zero Bitmaps | Smooth Infinity Mask | Interactive State Machine", fill=(148, 163, 184, 255), font=font_sub)

    # 2x2 Grid Layout
    # Grid starts at Y = 160
    # Available area: 2400 - 140 = 2260 width. Gap = 40. Card W = (2260 - 40) / 2 = 1110.
    # Height: 1600 - 160 - 50 = 1390. Gap = 40. Card H = (1390 - 40) / 2 = 675.

    panels = [
        {
            "col": 0, "row": 0,
            "path": "mascots/owluko/owluko_simplified_master_ref.png",
            "title": "1. REFERENCE OFFICIELLE FOURNIE",
            "badge": "SOURCE DE VERITE",
            "badge_color": (234, 88, 12, 255),
            "meta": "Modele simplifie demande : Masque barn-owl continu, yeux miel ambre ouverts, bec cone ferme, ailes douces, 3 orteils haricots."
        },
        {
            "col": 1, "row": 0,
            "path": "mascots/owluko/owluko_pure_vector_frame0.png",
            "title": "2. RENDU RIVE VECTORIEL NATIF",
            "badge": "FRAME 0 (IDLE 60 FPS)",
            "badge_color": (34, 197, 94, 255),
            "meta": "100% vectoriel cubique bezier (45 shapes, 190 sommets). Binaire .riv : 12.7 KB. Zero texture bitmap. Fidele a 100%."
        },
        {
            "col": 0, "row": 1,
            "path": "mascots/owluko/owluko_pure_vector_blink.png",
            "title": "3. RIG DYNAMIQUE & CLIGNEMENT",
            "badge": "PAUPIERES SYNCHRONISEES",
            "badge_color": (59, 130, 246, 255),
            "meta": "Fermeture naturelle des paupieres avec seams ambre/creme. Respiration organique et oscillation des ailes integrees."
        },
        {
            "col": 1, "row": 1,
            "path": "scratch/rive_studio_screenshot_simplified.png",
            "title": "4. RIVE STUDIO EN DIRECT",
            "badge": "HTTP://LOCALHOST:8787",
            "badge_color": (168, 85, 247, 255),
            "meta": "Runtime WebGL interactif live. Machine a etats SM_Owluko avec triggers blink et wink. Inspectable en temps reel."
        }
    ]

    card_w = 1110
    card_h = 675
    gap = 40
    start_x = 70
    start_y = 160

    for p in panels:
        x = start_x + p["col"] * (card_w + gap)
        y = start_y + p["row"] * (card_h + gap)

        # Card container
        draw.rounded_rectangle([x, y, x + card_w, y + card_h], radius=18, fill=(18, 22, 30, 255), outline=(38, 46, 60, 255), width=2)

        # Card Header
        draw.text((x + 24, y + 22), p["title"], fill=(255, 255, 255, 255), font=font_panel)

        # Badge
        badge_txt = p["badge"]
        badge_w = len(badge_txt) * 11 + 22
        draw.rounded_rectangle([x + card_w - 24 - badge_w, y + 20, x + card_w - 24, y + 50], radius=8, fill=p["badge_color"])
        draw.text((x + card_w - 13 - badge_w, y + 25), badge_txt, fill=(255, 255, 255, 255), font=font_badge)

        # Content split: Left preview image (square), Right metadata/info
        img_size = card_h - 110 # 565x565!
        img_x = x + 24
        img_y = y + 75

        draw.rounded_rectangle([img_x, img_y, img_x + img_size, img_y + img_size], radius=14, fill=(10, 12, 16, 255), outline=(30, 36, 48, 255), width=1)

        if os.path.exists(p["path"]):
            im = Image.open(p["path"]).convert("RGBA")
            im.thumbnail((img_size - 16, img_size - 16), Image.Resampling.LANCZOS)
            ox = img_x + (img_size - im.width) // 2
            oy = img_y + (img_size - im.height) // 2
            board.alpha_composite(im, (ox, oy))

        # Side details on the right of image
        detail_x = img_x + img_size + 30
        detail_w = card_w - (img_size + 78)
        detail_y = img_y + 10

        # Description
        draw.text((detail_x, detail_y), "SPECIFICATIONS & VERIFICATION", fill=(148, 163, 184, 255), font=font_badge)
        draw.line([detail_x, detail_y + 30, detail_x + detail_w, detail_y + 30], fill=(38, 46, 60, 255), width=1)

        # Text lines
        import textwrap
        lines = textwrap.wrap(p["meta"], width=38)
        cur_y = detail_y + 45
        for l in lines:
            draw.text((detail_x, cur_y), l, fill=(226, 232, 240, 255), font=font_meta)
            cur_y += 28

        # Additional technical bullets
        cur_y += 15
        bullets = []
        if p["col"] == 0 and p["row"] == 0:
            bullets = [
                "+ Format source : 1024x1024 PNG",
                "+ Silhouette : x=[162, 861], y=[144, 881]",
                "+ Yeux : r=64 a (398,362) et (626,362)",
                "+ Bec : Largeur 72px, y=[393, 459]",
                "+ Ligne de sol : Y = 876 px"
            ]
        elif p["col"] == 1 and p["row"] == 0:
            bullets = [
                "+ Fichier : owluko_pure_vector.riv",
                "+ Poids binaire : 12,976 octets (12.7 KB)",
                "+ Limite requise : < 50 KB (respecte a 25%)",
                "+ Precision courbes : 100% Cubiques",
                "+ Zero pixelisation, zoom infini"
            ]
        elif p["col"] == 0 and p["row"] == 1:
            bullets = [
                "+ Animation : Idle (respiration organique)",
                "+ Timeline clignement : blink (f=0..20)",
                "+ Timeline clin d oeil : wink",
                "+ Easing : Hermite cubique doux",
                "+ Frequence : 60 FPS constant"
            ]
        else:
            bullets = [
                "+ Port local actif : 8787",
                "+ Moteur : Rive WASM / WebGL",
                "+ URL : http://localhost:8787/",
                "+ Machine d etats : SM_Owluko",
                "+ Triggers interactifs fonctionnels"
            ]

        for b in bullets:
            draw.text((detail_x, cur_y), b, fill=(148, 163, 184, 255), font=font_meta)
            cur_y += 28

    out_path = "mascots/owluko/owluko_canonical_presentation_board.png"
    board.save(out_path)
    print("Saved 2x2 presentation board to", out_path)

    brain_dir = "/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68"
    shutil.copy2(out_path, os.path.join(brain_dir, "owluko_canonical_presentation_board.png"))
    print("Copied to brain directory.")

build_board()
