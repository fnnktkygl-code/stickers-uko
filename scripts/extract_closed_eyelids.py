import cv2
import numpy as np

# Load reference blink frame
blink_frame = cv2.imread("scratch/ref_blink_frame_18.png", cv2.IMREAD_UNCHANGED)
# Crop center 1080x1080 to match 512x512
h, w = blink_frame.shape[:2]
crop = blink_frame[:, (w - h)//2 : (w + h)//2]
crop_512 = cv2.resize(crop, (512, 512), interpolation=cv2.INTER_AREA)

# Despill green screen on blink frame
b, g, r = crop_512[:, :, 0], crop_512[:, :, 1], crop_512[:, :, 2]
g_despill = np.minimum(g, np.maximum(r, b))
crop_clean = crop_512.copy()
crop_clean[:, :, 1] = g_despill

# Align blink frame with front turnaround
# Front eye centers: Left (193, 160), Right (315, 163)
# Find eye centers in crop_clean:
# Eyes have dark crease line across (193, 160) and (315, 163)
closed_eyes = np.zeros((512, 512, 4), dtype=np.uint8)

# Left eye closed dome: center (193, 160), radius 34
# Right eye closed dome: center (315, 163), radius 34
for cx, cy in [(193, 160), (315, 163)]:
    for y in range(cy - 34, cy + 35):
        for x in range(cx - 34, cx + 35):
            dist = np.sqrt((x - cx)**2 + (y - cy)**2)
            if dist <= 31:
                closed_eyes[y, x, :3] = crop_clean[y, x, :3]
                closed_eyes[y, x, 3] = 255
            elif dist <= 33:
                closed_eyes[y, x, :3] = crop_clean[y, x, :3]
                closed_eyes[y, x, 3] = int(255 * (33.0 - dist) / 2.0)

cv2.imwrite("mascots/owluko/rig_layers/08_closed_eyes.png", closed_eyes)
print("Saved closed eyes layer: mascots/owluko/rig_layers/08_closed_eyes.png")
