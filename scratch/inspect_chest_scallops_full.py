from PIL import Image
ref = Image.open("mascots/owluko/owluko_user_master_ref.png").convert("RGBA")
sc = ref.crop((320, 540, 704, 760))
sc.save("scratch/crop_chest_full_ref.png")
print("Saved chest crop to scratch/crop_chest_full_ref.png")
