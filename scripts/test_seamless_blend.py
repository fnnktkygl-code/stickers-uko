import cv2
import numpy as np

img = cv2.imread("mascots/owluko/owluko_turnaround_view_1_front.png", cv2.IMREAD_UNCHANGED)
h, w, c = img.shape

# Clean despill
b, g, r, a = img[:, :, 0], img[:, :, 1], img[:, :, 2], img[:, :, 3]
g_despill = np.minimum(g, np.maximum(r, b))
img_clean = img.copy()
img_clean[:, :, 1] = g_despill

# 1. FEET:
# The feet start at y=415. The belly bottom is at y=444.
# If the feet are layered ON TOP of the belly or UNDER the belly:
# Look at the feet in the original image:
# The feet are BEHIND the lower belly! The belly bulges forward over the ankles!
# In the original image, you see the lower belly curve OVER the ankles.
# So the layer order from back to front is:
# 1. Shadow
# 2. Feet (left & right)
# 3. Body (lower belly overlaps ankles naturally!)
# 4. Eyeballs (left & right)
# 5. Eyelids (left & right)
# 6. Beak
# 7. Wings (left & right)

# Let test this layer order!
# If Feet are BEHIND Body:
# The body does NOT need to be cut off at y=444! The body simply has its full rounded belly!
# The feet ankles extend up behind the belly (e.g. up to y=420) so they tuck under the belly!
# When the body breathes, it gently scales from its pelvis center, and the feet stay planted on the floor!
print("Testing back-to-front layer order: Feet BEHIND Body...")
