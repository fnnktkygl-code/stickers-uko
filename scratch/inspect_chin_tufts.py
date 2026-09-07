from PIL import Image
ref = Image.open("mascots/owluko/owluko_user_master_ref.png").convert("RGBA")
chin = ref.crop((400, 420, 624, 550))
chin.save("scratch/crop_chin_tufts_ref.png")
print("Saved chin crop to scratch/crop_chin_tufts_ref.png")
