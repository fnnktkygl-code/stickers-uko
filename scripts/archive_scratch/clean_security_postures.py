from PIL import Image
import numpy as np
import cv2
from matte_engine import perfect_matte

# 1. Clean Owluko 11_security: Pure vigilant guardian posture without the neon shield
raw_sec = sorted(glob.glob("mascots/owluko/assets/11_security/temp_frames/f_*.png")) if 'glob' in locals() else []
import glob
raw_sec = sorted(glob.glob("mascots/owluko/assets/11_security/temp_frames/f_*.png"))

clean_owl_sec = []
master_owl = Image.open("mascots/owluko/assets/00_idle/static.png").convert("RGBA")
master_belly = master_owl.crop((185, 270, 325, 410))

for rf in raw_sec:
    cf = perfect_matte(Image.open(rf))
    # Inpaint belly to remove raw spark artifacts cleanly
    draw_mask = np.zeros((master_belly.height, master_belly.width), dtype=np.uint8)
    cv2.circle(draw_mask, (draw_mask.shape[1]//2, draw_mask.shape[0]//2), 48, 255, -1)
    draw_mask = cv2.GaussianBlur(draw_mask, (21, 21), 0)
    soft_mask = Image.fromarray(draw_mask)
    cf.paste(master_belly, (185, 270), soft_mask)
    clean_owl_sec.append(cf)

# Save pure posture version for preview
clean_owl_sec[min(35, len(clean_owl_sec)-1)].save("preview/owluko_pure_security_posture.png")

# 2. Clean AItuko 11_security: Pure porcelain defensive posture without blue fire cloud
master_ait = Image.open("assets/00_idle/static.png").convert("RGBA")
ait_belly = master_ait.crop((190, 240, 320, 420))

clean_ait_sec = []
for rf in sorted(glob.glob("assets/11_security/temp_frames/f_*.png")):
    cf = perfect_matte(Image.open(rf))
    draw_mask = np.zeros((ait_belly.height, ait_belly.width), dtype=np.uint8)
    cv2.circle(draw_mask, (draw_mask.shape[1]//2, draw_mask.shape[0]//2), 45, 255, -1)
    draw_mask = cv2.GaussianBlur(draw_mask, (21, 21), 0)
    soft_mask = Image.fromarray(draw_mask)
    cf.paste(ait_belly, (190, 240), soft_mask)
    clean_ait_sec.append(cf)

clean_ait_sec[min(35, len(clean_ait_sec)-1)].save("preview/aituko_pure_security_posture.png")

print("Saved pure posture previews for Owluko and AItuko!")
