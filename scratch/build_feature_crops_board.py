from PIL import Image, ImageDraw, ImageFont

# Load crops
le_ref = Image.open("scratch/crop_le_ref.png")
le_vec = Image.open("scratch/crop_le_vec.png")
re_ref = Image.open("scratch/crop_re_ref.png")
re_vec = Image.open("scratch/crop_re_vec.png")
bk_ref = Image.open("scratch/crop_bk_ref.png")
bk_vec = Image.open("scratch/crop_bk_vec.png")
sc_ref = Image.open("scratch/crop_sc_ref.png")
sc_vec = Image.open("scratch/crop_sc_vec.png")
lw_ref = Image.open("scratch/crop_lw_ref.png")
lw_vec = Image.open("scratch/crop_lw_vec.png")
ft_ref = Image.open("scratch/crop_ft_ref.png")
ft_vec = Image.open("scratch/crop_ft_vec.png")

# Create a composite board
board = Image.new("RGBA", (1400, 1000), (24, 26, 32, 255))
draw = ImageDraw.Draw(board)

draw.text((20, 20), "OWLUKO FEATURE-BY-FEATURE DISSECTION: MASTER REF (LEFT) VS VECTOR SVG (RIGHT)", fill=(255, 255, 255))

# Row 1: Left Eye & Right Eye Wink
# Left Eye (160x160)
draw.text((40, 60), "1. LEFT EYE (AMBER ORB)", fill=(245, 158, 11))
board.paste(le_ref, (40, 90))
board.paste(le_vec, (220, 90))

# Right Eye (160x100)
draw.text((440, 60), "2. RIGHT EYE (WINK)", fill=(245, 158, 11))
board.paste(re_ref, (440, 90))
board.paste(re_vec, (620, 90))

# Beak & Mouth (140x120)
draw.text((840, 60), "3. BEAK & MOUTH", fill=(245, 158, 11))
board.paste(bk_ref, (840, 90))
board.paste(bk_vec, (1000, 90))

# Row 2: Chest Scallops & Left Wing & Feet
# Chest Scallops (380x200)
draw.text((40, 280), "4. CHEST DOWN SCALLOPS (3 TOP, 2 BOTTOM)", fill=(245, 158, 11))
board.paste(sc_ref, (40, 310))
board.paste(sc_vec, (440, 310))

# Left Wing Tip (130x150)
draw.text((880, 280), "5. WING SCALLOP TIP", fill=(245, 158, 11))
board.paste(lw_ref, (880, 310))
board.paste(lw_vec, (1040, 310))

# Row 3: Feet (360x80)
draw.text((40, 540), "6. GROUNDED FEET (3 TOES PER FOOT)", fill=(245, 158, 11))
board.paste(ft_ref, (40, 570))
board.paste(ft_vec, (440, 570))

board.save("scratch/feature_dissection_board.png", "PNG")
print("Saved feature dissection board to scratch/feature_dissection_board.png")
