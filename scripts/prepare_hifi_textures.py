import cv2
import numpy as np
import os

os.makedirs('mascots/owluko/components/hifi', exist_ok=True)
img = cv2.imread('/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68/.user_uploaded/media_1788764972449.png')

# 1. Base Body Texture (Panel 2)
# Crop the base without text
p2 = img[25:315, 365:655]
# Make transparent where background is pure white
diff = 255.0 - np.min(p2.astype(np.float32), axis=2)
alpha = np.clip(diff / 8.0, 0.0, 1.0)
rgba_base = np.zeros((p2.shape[0], p2.shape[1], 4), dtype=np.uint8)
rgba_base[:, :, :3] = p2
rgba_base[:, :, 3] = (alpha * 255.0).astype(np.uint8)

# Resize base texture to 540x650
base_resized = cv2.resize(rgba_base, (540, 650), interpolation=cv2.INTER_LANCZOS4)
cv2.imwrite('mascots/owluko/components/hifi/base_body.png', base_resized)
print('Saved hifi base_body.png:', base_resized.shape)

# 2. Eyes (Panel 4)
p4 = img[360:640, 25:315]
# Left eye
eye_l_raw = p4[40:220, 20:140]
# Make circular mask
hl, wl = eye_l_raw.shape[:2]
diff_l = 255.0 - np.min(eye_l_raw.astype(np.float32), axis=2)
alpha_l = np.clip(diff_l / 12.0, 0.0, 1.0)
rgba_el = np.zeros((hl, wl, 4), dtype=np.uint8)
rgba_el[:, :, :3] = eye_l_raw
rgba_el[:, :, 3] = (alpha_l * 255.0).astype(np.uint8)
# Crop to bbox
coords = cv2.findNonZero(rgba_el[:, :, 3])
x, y, w, h = cv2.boundingRect(coords)
eye_l_crop = cv2.resize(rgba_el[y:y+h, x:x+w], (128, 128), interpolation=cv2.INTER_LANCZOS4)
cv2.imwrite('mascots/owluko/components/hifi/eye_left.png', eye_l_crop)

# Right eye
eye_r_raw = p4[40:220, 150:270]
hr, wr = eye_r_raw.shape[:2]
diff_r = 255.0 - np.min(eye_r_raw.astype(np.float32), axis=2)
alpha_r = np.clip(diff_r / 12.0, 0.0, 1.0)
rgba_er = np.zeros((hr, wr, 4), dtype=np.uint8)
rgba_er[:, :, :3] = eye_r_raw
rgba_er[:, :, 3] = (alpha_r * 255.0).astype(np.uint8)
coords = cv2.findNonZero(rgba_er[:, :, 3])
x, y, w, h = cv2.boundingRect(coords)
eye_r_crop = cv2.resize(rgba_er[y:y+h, x:x+w], (128, 128), interpolation=cv2.INTER_LANCZOS4)
cv2.imwrite('mascots/owluko/components/hifi/eye_right.png', eye_r_crop)
print('Saved hifi eyes (128x128).')

# 3. Beak (Panel 5)
p5 = img[380:610, 390:630]
diff_b = 255.0 - np.min(p5.astype(np.float32), axis=2)
alpha_b = np.clip(diff_b / 10.0, 0.0, 1.0)
rgba_b = np.zeros((p5.shape[0], p5.shape[1], 4), dtype=np.uint8)
rgba_b[:, :, :3] = p5
rgba_b[:, :, 3] = (alpha_b * 255.0).astype(np.uint8)
coords = cv2.findNonZero(rgba_b[:, :, 3])
x, y, w, h = cv2.boundingRect(coords)
beak_crop = cv2.resize(rgba_b[y:y+h, x:x+w], (72, 76), interpolation=cv2.INTER_LANCZOS4)
cv2.imwrite('mascots/owluko/components/hifi/beak.png', beak_crop)
print('Saved hifi beak (72x76).')

# 4. Feet (Panel 6)
p6 = img[440:590, 710:990]
diff_f = 255.0 - np.min(p6.astype(np.float32), axis=2)
alpha_f = np.clip(diff_f / 10.0, 0.0, 1.0)
rgba_f = np.zeros((p6.shape[0], p6.shape[1], 4), dtype=np.uint8)
rgba_f[:, :, :3] = p6
rgba_f[:, :, 3] = (alpha_f * 255.0).astype(np.uint8)
coords = cv2.findNonZero(rgba_f[:, :, 3])
x, y, w, h = cv2.boundingRect(coords)
feet_crop = cv2.resize(rgba_f[y:y+h, x:x+w], (280, 68), interpolation=cv2.INTER_LANCZOS4)
cv2.imwrite('mascots/owluko/components/hifi/feet.png', feet_crop)
print('Saved hifi feet (280x68).')

# 5. Wing (Panel 3)
p3 = img[25:315, 700:1000]
diff_w = 255.0 - np.min(p3.astype(np.float32), axis=2)
alpha_w = np.clip(diff_w / 8.0, 0.0, 1.0)
rgba_w = np.zeros((p3.shape[0], p3.shape[1], 4), dtype=np.uint8)
rgba_w[:, :, :3] = p3
rgba_w[:, :, 3] = (alpha_w * 255.0).astype(np.uint8)
coords = cv2.findNonZero(rgba_w[:, :, 3])
x, y, w, h = cv2.boundingRect(coords)
wing_crop = cv2.resize(rgba_w[y:y+h, x:x+w], (220, 220), interpolation=cv2.INTER_LANCZOS4)
cv2.imwrite('mascots/owluko/components/hifi/wing.png', wing_crop)
print('Saved hifi wing (220x220).')

print('All Hi-Fi textures prepared successfully.')
