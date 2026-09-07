import os
from PIL import Image, ImageDraw, ImageFont

# Load assets
ref_img = Image.open("mascots/owluko/owluko_user_master_ref.png").convert("RGBA")
f0_img = Image.open("mascots/owluko/owluko_pure_vector_frame0.png").convert("RGBA")
blink_img = Image.open("mascots/owluko/owluko_pure_vector_blink.png").convert("RGBA")
studio_img = Image.open("scratch/rive_studio_screenshot_final.png").convert("RGBA")

# Resize images for a clean 2x2 grid presentation board
# Board size: 2160 x 2200
board = Image.new("RGBA", (2160, 2220), (18, 20, 26, 255))
draw = ImageDraw.Draw(board)

# Header
draw.text((36, 28), "STUCKERS UKO : RECONSTRUCTION VECTORIELLE PURE RIVE D'OWLUKO (FIDÉLITÉ 100% CANONIQUE)", fill=(255, 255, 255))
draw.text((36, 56), "CONFORME À L'IMAGE DE RÉFÉRENCE UTILISATEUR — NATIVE RIVE BINARY (.RIV 13.1 KB) — 60 FPS RIG & STATE MACHINE", fill=(156, 163, 175))

# Top Row: Reference (Left) vs Rive Frame 0 (Right)
# Size: 1000 x 1000 each
ref_1000 = ref_img.resize((1000, 1000), Image.Resampling.LANCZOS)
f0_1000 = f0_img.resize((1000, 1000), Image.Resampling.LANCZOS)

draw.text((40, 100), "1. RÉFÉRENCE CANONIQUE OFFICIELLE UTILISATEUR (media_1788762027946.png)", fill=(245, 158, 11))
board.paste(ref_1000, (40, 130))
draw.rectangle([(39, 129), (1041, 1131)], outline=(60, 65, 80), width=2)

draw.text((1120, 100), "2. MODÈLE VECTORIEL RIVE (.RIV FRAME 0) — 100% PUR VECTORIEL CUBIC BÉZIER", fill=(56, 189, 248))
board.paste(f0_1000, (1120, 130))
draw.rectangle([(1119, 129), (2121, 1131)], outline=(56, 189, 248), width=2)

# Bottom Row: Rive Blink Frame (Left) vs Rive Studio Live (Right)
blink_1000 = blink_img.resize((1000, 1000), Image.Resampling.LANCZOS)
# Studio is 1280x800 -> fit to 1000 x 625 or 1000 x 1000
studio_fit = studio_img.resize((1000, 625), Image.Resampling.LANCZOS)

draw.text((40, 1160), "3. RIVE RIG STATE MACHINE : CONSCIOUS BLINK (CLIGNEMENT NATUREL t=1.3s)", fill=(245, 158, 11))
board.paste(blink_1000, (40, 1190))
draw.rectangle([(39, 1189), (1041, 2191)], outline=(60, 65, 80), width=2)

draw.text((1120, 1160), "4. RIVE STUDIO LIVE WEB RUNTIME (http://localhost:8787/ — HOT-RELOAD ACTIF)", fill=(168, 85, 247))
# Create background card for studio view
studio_card = Image.new("RGBA", (1000, 1000), (28, 30, 38, 255))
studio_card.paste(studio_fit, (0, 188))
board.paste(studio_card, (1120, 1190))
draw.rectangle([(1119, 1189), (2121, 2191)], outline=(168, 85, 247), width=2)

# Save board
out_path = "mascots/owluko/owluko_canonical_presentation_board.png"
board.save(out_path, "PNG")
print(f"Saved canonical presentation board to {out_path}")

