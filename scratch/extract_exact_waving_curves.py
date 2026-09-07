import cv2
import numpy as np

# 1. Extract happy eyes in panel 5 aligned
p5 = cv2.imread('scratch/panel_5_aligned.png')
# Happy eyes are the darkest pixels in the eye region (x in [300, 724], y in [300, 420])
eye_reg = p5[300:420, 300:724]
gray_eye = cv2.cvtColor(eye_reg, cv2.COLOR_BGR2GRAY)
# Eye curves have gray < 90
mask_eyes = gray_eye < 90

# Left eye curve (viewer left): x in [300, 480] -> in reg: [0, 180]
# Right eye curve (viewer right): x in [540, 720] -> in reg: [240, 420]
mask_el = (gray_eye < 90) & (np.arange(eye_reg.shape[1])[None, :] < 200)
mask_er = (gray_eye < 90) & (np.arange(eye_reg.shape[1])[None, :] > 220)

yel, xel = np.where(mask_el)
yer, xer = np.where(mask_er)

print(f"Happy eye left: x=[{xel.min()+300}, {xel.max()+300}], y=[{yel.min()+300}, {yel.max()+300}]")
print(f"Happy eye right: x=[{xer.min()+300}, {xer.max()+300}], y=[{yer.min()+300}, {yer.max()+300}]")

# Let's find the skeleton / center line of the happy eye curves
# In 1024x1024:
# Left eye arch:
# start (inner): near (455, 368), peak: near (398, 335), end (outer): near (340, 368)
# Right eye arch:
# start (inner): near (569, 368), peak: near (626, 335), end (outer): near (684, 368)
print("Center of left eye in master is (398, 362), right eye is (626, 362)")

# 2. Extract waving wing in panel 4 aligned
p4 = cv2.imread('scratch/panel_4_aligned.png')
master = cv2.imread('mascots/owluko/owluko_master_ref_clean.png')

# The waving wing is visible on the right (x > 700) where p4 is not white (< 250)
p4_gray = cv2.cvtColor(p4, cv2.COLOR_BGR2GRAY)
wing_pixels = (p4_gray < 250) & (np.arange(1024)[None, :] > 730)
yw, xw = np.where(wing_pixels)
print(f"Waving wing (panel 4) bounds: x=[{xw.min()}, {xw.max()}], y=[{yw.min()}, {yw.max()}]")

# Let's find the 3 feather tips
# Find local maxima or contour
wing_mask = np.zeros((1024, 1024), dtype=np.uint8)
wing_mask[wing_pixels] = 255
contours, _ = cv2.findContours(wing_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
if contours:
    c = max(contours, key=cv2.contourArea)
    # Find points on contour with x > 850
    pts = c[:, 0, :]
    pts_outer = pts[pts[:, 0] > 800]
    print(f"Outer points count: {len(pts_outer)}")
    # Find tips:
    # Feather 1 (tallest): min y in outer
    tip1 = pts[np.argmin(pts[:, 1])]
    # Feather 2 (middle): max x
    tip2 = pts[np.argmax(pts[:, 0])]
    print(f"Tip 1 (tallest): {tip1}")
    print(f"Tip 2 (outermost): {tip2}")

# Also check panel 3 (inward tilt)
p3 = cv2.imread('scratch/panel_3_aligned.png')
p3_gray = cv2.cvtColor(p3, cv2.COLOR_BGR2GRAY)
wing_pixels_3 = (p3_gray < 250) & (np.arange(1024)[None, :] > 720)
yw3, xw3 = np.where(wing_pixels_3)
print(f"Waving wing (panel 3) bounds: x=[{xw3.min()}, {xw3.max()}], y=[{yw3.min()}, {yw3.max()}]")

