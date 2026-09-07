from PIL import Image

ref = Image.open("mascots/owluko/owluko_simplified_master_ref.png").convert("RGBA")

# Crops
crop_le = ref.crop((320, 280, 480, 440))
crop_re = ref.crop((544, 280, 704, 440))
crop_bk = ref.crop((460, 370, 564, 470))
crop_lw = ref.crop((150, 440, 280, 740))
crop_ft = ref.crop((340, 820, 684, 885))
crop_mask = ref.crop((240, 210, 784, 460))
crop_belly = ref.crop((280, 500, 744, 840))

crop_le.save("scratch/simp_crop_le.png")
crop_re.save("scratch/simp_crop_re.png")
crop_bk.save("scratch/simp_crop_bk.png")
crop_lw.save("scratch/simp_crop_lw.png")
crop_ft.save("scratch/simp_crop_ft.png")
crop_mask.save("scratch/simp_crop_mask.png")
crop_belly.save("scratch/simp_crop_belly.png")

print("Simplified crops saved!")
