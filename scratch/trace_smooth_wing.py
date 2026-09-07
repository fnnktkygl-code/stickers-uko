import cv2
import numpy as np

# Let's inspect wing_p3 (inward wave)
# Crop size: 121 x 240
im3 = cv2.imread('scratch/waving_panels/wing_p3.png')
# Background is pure white (255, 255, 255)
gray3 = cv2.cvtColor(im3, cv2.COLOR_BGR2GRAY)
mask3 = (gray3 < 250).astype(np.uint8) * 255

# In wing_p3, the mascot body is on the left (x < 35)
# Wing starts at x ~ 30..40 and extends to x ~ 100
# Let's find the contour of the wing
contours, _ = cv2.findContours(mask3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
c = max(contours, key=cv2.contourArea)

# Let's upscale to 1024x1024 coordinates
# In our calibration:
# Scale = 10.0 / 3.0 = 3.33333
# Panel 3 was in row 0, col 2: bounds=(682, 0) to (1023, 285)
# Crop was (220, 0, 341, 240) in panel 3
# So in full storyboard (1024x571):
# x_sb = 682 + 220 + x_crop = 902 + x_crop?
# Wait! Let's check which panel wing_p3 came from!
# In scratch/crop_waving_details.py:
# p = Image.open(f'scratch/waving_panels/panel_{i}.png')
# wing_crop = p.crop((220, 0, 341, 240))
# So x in panel 3 is x_crop + 220, y is y_crop.
# And from scratch/align_storyboard_to_master.py:
# inv_s = 3.33333, tx = -53.33, ty = 23.33
# So:
# x_1024 = (220 + x_crop) * 3.33333 - 53.33
# y_1024 = y_crop * 3.33333 + 23.33

pts_1024 = []
for pt in c[:, 0, :]:
    xc, yc = pt
    # Only keep the wing part (xc > 20)
    if xc >= 20:
        gx = (220 + xc) * (10.0 / 3.0) - 53.33
        gy = yc * (10.0 / 3.0) + 23.33
        pts_1024.append((gx, gy))

pts_1024 = np.array(pts_1024)
print(f"Wing 1024 bounds: x=[{pts_1024[:,0].min():.1f}, {pts_1024[:,0].max():.1f}], y=[{pts_1024[:,1].min():.1f}, {pts_1024[:,1].max():.1f}]")

# Let's find the 3 finger tips in 1024 coordinates:
# Tip 1 (tallest, leftmost): min gy
idx_tip1 = np.argmin(pts_1024[:, 1])
tip1 = pts_1024[idx_tip1]
print(f"Tip 1 (tallest, primary): ({tip1[0]:.1f}, {tip1[1]:.1f})")

# Find points where x > 850
pts_right = pts_1024[pts_1024[:, 0] > 850]
# Tip 2 (middle): local minimum in y for x in [850, 930]
pts_mid = pts_1024[(pts_1024[:, 0] > 840) & (pts_1024[:, 0] < 920)]
if len(pts_mid) > 0:
    tip2 = pts_mid[np.argmin(pts_mid[:, 1])]
    print(f"Tip 2 (middle): ({tip2[0]:.1f}, {tip2[1]:.1f})")

# Tip 3 (lowest, outermost): local minimum in y for x > 910
pts_low = pts_1024[pts_1024[:, 0] > 910]
if len(pts_low) > 0:
    tip3 = pts_low[np.argmin(pts_low[:, 1])]
    print(f"Tip 3 (outermost): ({tip3[0]:.1f}, {tip3[1]:.1f})")

