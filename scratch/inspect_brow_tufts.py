from PIL import Image
ref = Image.open("mascots/owluko/owluko_user_master_ref.png").convert("RGBA")
brow = ref.crop((280, 180, 744, 330))
brow.save("scratch/crop_brow_tufts_ref.png")
print("Saved brow crop to scratch/crop_brow_tufts_ref.png")
