from PIL import Image
ref = Image.open("mascots/owluko/owluko_user_master_ref.png").convert("RGBA")
wing = ref.crop((140, 420, 310, 760))
wing.save("scratch/crop_wing_full_ref.png")
print("Saved wing crop to scratch/crop_wing_full_ref.png")
