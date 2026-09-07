#!/usr/bin/env python3
import os
import cv2
import numpy as np
from PIL import Image

WORKSPACE_DIR = "/Users/richard/Developer/Stickers Uko"
front = cv2.imread(os.path.join(WORKSPACE_DIR, "mascots/owluko/02_refonte_nouvelle/master_turnaround/owluko_turnaround_view_1_front.png"), cv2.IMREAD_UNCHANGED)
pr = cv2.imread(os.path.join(WORKSPACE_DIR, "mascots/owluko/02_refonte_nouvelle/master_turnaround/owluko_turnaround_view_2_profile_right.png"), cv2.IMREAD_UNCHANGED)
pl = cv2.imread(os.path.join(WORKSPACE_DIR, "mascots/owluko/02_refonte_nouvelle/master_turnaround/owluko_turnaround_view_3_profile_left.png"), cv2.IMREAD_UNCHANGED)
back = cv2.imread(os.path.join(WORKSPACE_DIR, "mascots/owluko/02_refonte_nouvelle/master_turnaround/owluko_turnaround_view_4_back.png"), cv2.IMREAD_UNCHANGED)

# Let's inspect the collar region in front view:
# In front view:
# Head top: Y = 42
# Eyes: Y = 140..170
# Beak: Y = 165..195
# Collar (Tier 1 + Tier 2): Y = 195..245
# Torso: Y = 240..491

# We want:
# 1. Torso Base: keep everything from Y = 200 down to 491.
# The Tier 2 lower collar is the lower ruff resting on shoulders (Y in [200, 245]).
body = front.copy()
# Smooth feathering above Y = 200
for y in range(512):
    for x in range(512):
        if y < 192:
            body[y, x, 3] = 0
        elif y < 202:
            f = (y - 192) / 10.0
            body[y, x, 3] = int(body[y, x, 3] * f)

# Inpaint any beak residue in the neck furrow if needed
neck_mask = np.zeros((512, 512), dtype=np.uint8)
neck_mask[192:215, 245:267] = 255
body[:, :, :3] = cv2.inpaint(body[:, :, :3], neck_mask, 5, cv2.INPAINT_TELEA)

# 2. Head with Tier 1 upper collar:
# Keep head from Y = 0 down to Y = 215 (just below chin and upper scalloped ruff)
def extract_head_with_tier1(view, is_back=False):
    h = view.copy()
    y_cut = 218 if not is_back else 214
    for y in range(512):
        for x in range(512):
            if y > y_cut:
                h[y, x, 3] = 0
            elif y > y_cut - 10:
                f = 1.0 - (y - (y_cut - 10)) / 10.0
                h[y, x, 3] = int(h[y, x, 3] * f)
    return h

h_front = extract_head_with_tier1(front)
h_pr = extract_head_with_tier1(pr)
h_pl = extract_head_with_tier1(pl)
h_back = extract_head_with_tier1(back, is_back=True)

# Test compositing:
b_pil = Image.fromarray(body)

for name, h_arr in [("front", h_front), ("pr", h_pr), ("back", h_back), ("pl", h_pl)]:
    h_pil = Image.fromarray(h_arr)
    comp = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    comp.alpha_composite(b_pil)
    comp.alpha_composite(h_pil)
    
    # Save test image
    comp.save(f"scratch/test_dc_{name}.png")
    print(f"Saved scratch/test_dc_{name}.png")

