from PIL import Image
import numpy as np

img = Image.open("mascots/owluko/owluko_user_master_ref.png").convert("RGB")
arr = np.array(img)

def sample_point(x, y, r=2):
    patch = arr[y-r:y+r+1, x-r:x+r+1]
    mean_rgb = patch.mean(axis=(0, 1)).astype(int)
    hex_code = "#{:02X}{:02X}{:02X}".format(*mean_rgb)
    return hex_code, mean_rgb

print("Body base top:", sample_point(512, 170))
print("Body cheek left:", sample_point(250, 420))
print("Body flank shadow left:", sample_point(200, 600))
print("Facial disk center forehead:", sample_point(512, 280))
print("Facial disk left brow:", sample_point(390, 260))
print("Facial disk cheek left:", sample_point(300, 400))
print("Facial disk chin under beak:", sample_point(512, 500))

print("\nLeft Eye:")
print("Eye socket rim:", sample_point(345, 360))
print("Eye iris amber top:", sample_point(410, 315))
print("Eye iris golden bottom:", sample_point(380, 415))
print("Eye pupil deep:", sample_point(420, 360))
print("Eye specular top-left:", sample_point(387, 345))
print("Eye specular bottom-right:", sample_point(433, 390))

print("\nWink Right:")
print("Wink stroke center:", sample_point(615, 355))
print("Wink shadow underneath:", sample_point(615, 368))

print("\nBeak & Mouth:")
print("Beak upper apex:", sample_point(513, 385))
print("Beak mid orange:", sample_point(513, 410))
print("Beak tip over mouth:", sample_point(513, 425))
print("Mouth cavity deep:", sample_point(513, 442))
print("Mouth tongue pink:", sample_point(513, 448))

print("\nChest Down Scallops:")
print("Chest background belly:", sample_point(512, 570))
print("Scallop 1 (top-left) shadow:", sample_point(395, 638))
print("Scallop 1 (top-left) highlight:", sample_point(395, 615))
print("Scallop 2 (top-mid) shadow:", sample_point(512, 642))
print("Scallop 2 (top-mid) highlight:", sample_point(512, 620))
print("Scallop 4 (bot-left) shadow:", sample_point(450, 705))
print("Scallop 4 (bot-left) highlight:", sample_point(450, 680))

print("\nWing Scallop Tips (Left):")
print("Wing outer flank:", sample_point(180, 560))
print("Wing scallop tip 1:", sample_point(178, 640))
print("Wing scallop tip 2:", sample_point(185, 680))
print("Wing scallop tip 3 (lowest):", sample_point(210, 725))

print("\nFeet:")
print("Foot left middle toe:", sample_point(410, 855))
print("Foot left middle toe highlight:", sample_point(410, 845))
print("Foot right middle toe:", sample_point(615, 855))

