from PIL import Image
import numpy as np

ref = Image.open("mascots/owluko/owluko_user_master_ref.png").convert("RGBA")
vec = Image.open("scratch/owluko_user_exact_master.png").convert("RGBA")

# 1. Left Eye: crop [280:440, 310:470]
crop_le_ref = ref.crop((310, 280, 470, 440))
crop_le_vec = vec.crop((310, 280, 470, 440))

# 2. Right Eye Wink: crop [310:410, 550:710]
crop_re_ref = ref.crop((550, 310, 710, 410))
crop_re_vec = vec.crop((550, 310, 710, 410))

# 3. Beak & Mouth: crop [360:480, 440:580]
crop_bk_ref = ref.crop((440, 360, 580, 480))
crop_bk_vec = vec.crop((440, 360, 580, 480))

# 4. Chest Scallops: crop [550:750, 320:700]
crop_sc_ref = ref.crop((320, 550, 700, 750))
crop_sc_vec = vec.crop((320, 550, 700, 750))

# 5. Left Wing Tip: crop [600:750, 150:280]
crop_lw_ref = ref.crop((150, 600, 280, 750))
crop_lw_vec = vec.crop((150, 600, 280, 750))

# 6. Feet: crop [810:890, 330:690]
crop_ft_ref = ref.crop((330, 810, 690, 890))
crop_ft_vec = vec.crop((330, 810, 690, 890))

# Save crops
crop_le_ref.save("scratch/crop_le_ref.png")
crop_le_vec.save("scratch/crop_le_vec.png")
crop_re_ref.save("scratch/crop_re_ref.png")
crop_re_vec.save("scratch/crop_re_vec.png")
crop_bk_ref.save("scratch/crop_bk_ref.png")
crop_bk_vec.save("scratch/crop_bk_vec.png")
crop_sc_ref.save("scratch/crop_sc_ref.png")
crop_sc_vec.save("scratch/crop_sc_vec.png")
crop_lw_ref.save("scratch/crop_lw_ref.png")
crop_lw_vec.save("scratch/crop_lw_vec.png")
crop_ft_ref.save("scratch/crop_ft_ref.png")
crop_ft_vec.save("scratch/crop_ft_vec.png")
print("Crops saved successfully!")
