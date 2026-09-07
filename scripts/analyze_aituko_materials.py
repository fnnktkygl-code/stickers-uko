import cv2
import numpy as np

img = cv2.imread('preview/aituko_3d_master_crop_512.png', cv2.IMREAD_UNCHANGED)
b, g, r, a = cv2.split(img)

# 1. Visor Glass: sample colors inside the visor
visor_samples = []
for dy in range(-30, 31, 10):
    for dx in range(-50, 51, 20):
        px = 256 + dx
        py = 100 + dy
        visor_samples.append(img[py, px, :3])
v_mean = np.mean(visor_samples, axis=0)
print('Visor glass avg BGR:', [round(x,1) for x in v_mean], '-> Hex RGB: #%02x%02x%02x' % (int(v_mean[2]), int(v_mean[1]), int(v_mean[0])))

# 2. Porcelain Body: sample colors across the torso
torso_samples = []
for dy in range(-40, 41, 20):
    for dx in range(-40, 41, 20):
        px = 256 + dx
        py = 315 + dy
        torso_samples.append(img[py, px, :3])
t_mean = np.mean(torso_samples, axis=0)
print('Torso porcelain avg BGR:', [round(x,1) for x in t_mean], '-> Hex RGB: #%02x%02x%02x' % (int(t_mean[2]), int(t_mean[1]), int(t_mean[0])))

# 3. Cyan Eyes: sample colors in the cyan glowing core
hsv = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2HSV)
cyan = (a > 100) & (hsv[:,:,0] >= 75) & (hsv[:,:,0] <= 115) & (hsv[:,:,1] >= 100) & (hsv[:,:,2] >= 150)
cy_bgr = img[cyan][:, :3]
c_mean = np.mean(cy_bgr, axis=0)
print('Cyan eye avg BGR:', [round(x,1) for x in c_mean], '-> Hex RGB: #%02x%02x%02x' % (int(c_mean[2]), int(c_mean[1]), int(c_mean[0])))
c_max = np.max(cy_bgr, axis=0)
print('Cyan eye peak BGR:', [int(x) for x in c_max], '-> Hex RGB: #%02x%02x%02x' % (int(c_max[2]), int(c_max[1]), int(c_max[0])))

# 4. Specular highlight on dome:
dome_highlight = img[20:50, 230:280, :3].reshape(-1, 3)
h_mean = np.mean(dome_highlight, axis=0)
print('Dome highlight BGR:', [round(x,1) for x in h_mean], '-> Hex RGB: #%02x%02x%02x' % (int(h_mean[2]), int(h_mean[1]), int(h_mean[0])))

# 5. Feet / Pods:
feet_samples = img[460:490, 200:310, :3].reshape(-1, 3)
f_mean = np.mean(feet_samples, axis=0)
print('Feet avg BGR:', [round(x,1) for x in f_mean], '-> Hex RGB: #%02x%02x%02x' % (int(f_mean[2]), int(f_mean[1]), int(f_mean[0])))

# 6. Arms:
arm_samples = img[280:380, 115:145, :3].reshape(-1, 3)
a_mean = np.mean(arm_samples, axis=0)
print('Left arm avg BGR:', [round(x,1) for x in a_mean], '-> Hex RGB: #%02x%02x%02x' % (int(a_mean[2]), int(a_mean[1]), int(a_mean[0])))
