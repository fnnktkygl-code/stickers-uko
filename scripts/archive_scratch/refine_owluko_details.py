from PIL import Image
import numpy as np
import cv2

# 1. Clean 3D Orange Loupe: Keep ONLY the orange rim, handle and glass lens
ait_loupe = Image.open("preview/aituko_clean_loupe.png").convert("RGBA")
arr_l = np.array(ait_loupe)

# Orange rim + handle: (R > 180, G: 60..155, B < 60)
orange_part = (arr_l[:,:,0] > 180) & (arr_l[:,:,1] > 60) & (arr_l[:,:,1] < 155) & (arr_l[:,:,2] < 60)
# Glass lens reflection: (R > 150, G > 180, B > 180, and near center)
lens_part = (arr_l[:,:,1] > 190) & (arr_l[:,:,2] > 200) & (arr_l[:,:,0] < 120)

# Mask of loupe alone (exclude robot fingers which are white/grey and below/beside handle)
pure_loupe_mask = orange_part | lens_part
pure_loupe_arr = np.zeros_like(arr_l)
pure_loupe_arr[pure_loupe_mask] = arr_l[pure_loupe_mask]
pure_loupe_img = Image.fromarray(pure_loupe_arr, mode="RGBA")
pure_loupe_img.save("preview/pure_orange_loupe.png")

# 2. Refine 08_searching for Owluko
owl_search_anim = Image.open("mascots/owluko/assets/08_searching/animated.png")
frames_08 = []
l_w, l_h = int(pure_loupe_img.width * 0.9), int(pure_loupe_img.height * 0.9)
scaled_loupe = pure_loupe_img.resize((l_w, l_h), Image.Resampling.LANCZOS)

for idx in range(getattr(owl_search_anim, 'n_frames', 1)):
    owl_search_anim.seek(idx)
    f = owl_search_anim.convert("RGBA")
    # Paste pure orange loupe over left eye/wing
    f.paste(scaled_loupe, (108, 122), scaled_loupe)
    frames_08.append(f)

d08 = "mascots/owluko/assets/08_searching"
frames_08[min(35, len(frames_08)-1)].save(f"{d08}/static.png", optimize=True)
frames_08[min(35, len(frames_08)-1)].save(f"{d08}/static.webp", quality=92)
frames_08[0].save(f"{d08}/animated.png", save_all=True, append_images=frames_08[1:], duration=41, loop=0)
frames_08[0].save(f"{d08}/animated.webp", save_all=True, append_images=frames_08[1:], duration=41, loop=0, quality=88, method=4)

# 3. Refine 11_security for Owluko: Seamless feather inpainting
owl_sec_anim = Image.open("mascots/owluko/assets/11_security/animated.png")
frames_11 = []
master_owl = Image.open("mascots/owluko/assets/00_idle/static.png").convert("RGBA")
master_belly = master_owl.crop((180, 260, 330, 420))

for idx in range(getattr(owl_sec_anim, 'n_frames', 1)):
    owl_sec_anim.seek(idx)
    f = owl_sec_anim.convert("RGBA")
    # Blend natural feathered belly onto chest area with soft feathered alpha mask
    mask_blend = Image.new("L", master_belly.size, 0)
    draw_mask = np.array(mask_blend)
    cv2.circle(draw_mask, (draw_mask.shape[1]//2, draw_mask.shape[0]//2), 50, 220, -1)
    draw_mask = cv2.GaussianBlur(draw_mask, (25, 25), 0)
    soft_mask = Image.fromarray(draw_mask)
    f.paste(master_belly, (180, 260), soft_mask)
    frames_11.append(f)

d11 = "mascots/owluko/assets/11_security"
frames_11[min(35, len(frames_11)-1)].save(f"{d11}/static.png", optimize=True)
frames_11[min(35, len(frames_11)-1)].save(f"{d11}/static.webp", quality=92)
frames_11[0].save(f"{d11}/animated.png", save_all=True, append_images=frames_11[1:], duration=41, loop=0)
frames_11[0].save(f"{d11}/animated.webp", save_all=True, append_images=frames_11[1:], duration=41, loop=0, quality=88, method=4)

print("✅ Owluko 08_searching and 11_security surgically refined!")
