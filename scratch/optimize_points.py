import cv2
import numpy as np
import math
from scratch.fit_rive_wing import render_rive_polygon

gt = cv2.imread('scratch/gt_wing_mask.png', cv2.IMREAD_GRAYSCALE)
gt_bool = gt > 0

# 6 anchor points:
# P0: shoulder_top  (0, -155)
# P1: upper_flank   (-50, -70)
# P2: outer_apex    (-59, 10)
# P3: lower_flank   (-39, 100)
# P4: wing_tip      (31, 152)
# P5: mid_crease    (0, 20)

points = [
  {
    "x": 0,
    "y": -155,
    "cubic": {
      "rotation": 125.0,
      "outDistance": 48.0,
      "inRotation": -75.0,
      "inDistance": 50.0
    }
  },
  {
    "x": -50,
    "y": -70,
    "cubic": {
      "rotation": 95.0,
      "outDistance": 40.0,
      "inRotation": -85.0,
      "inDistance": 40.0
    }
  },
  {
    "x": -59,
    "y": 10,
    "cubic": {
      "rotation": 80.0,
      "outDistance": 45.0,
      "inRotation": -100.0,
      "inDistance": 45.0
    }
  },
  {
    "x": -39,
    "y": 100,
    "cubic": {
      "rotation": 55.0,
      "outDistance": 42.0,
      "inRotation": -125.0,
      "inDistance": 42.0
    }
  },
  {
    "x": 31,
    "y": 152,
    "cubic": {
      "rotation": -30.0,
      "outDistance": 32.0,
      "inRotation": 150.0,
      "inDistance": 28.0
    }
  },
  {
    "x": 0,
    "y": 20,
    "cubic": {
      "rotation": -95.0,
      "outDistance": 75.0,
      "inRotation": 85.0,
      "inDistance": 60.0
    }
  }
]

origin = (224, 590)
pred, _ = render_rive_polygon(points, origin)
pred_bool = pred > 0

inter = np.logical_and(gt_bool, pred_bool).sum()
union = np.logical_or(gt_bool, pred_bool).sum()
iou = inter / union
print(f"Initial IoU: {iou*100:.2f}% (inter={inter}, union={union})")

# Save visual comparison
vis = np.zeros((1024, 1024, 3), dtype=np.uint8)
vis[gt_bool] = [100, 200, 100] # GT green
vis[pred_bool] = [50, 100, 255] # Pred orange
vis[np.logical_and(gt_bool, pred_bool)] = [255, 255, 255] # Overlap white
cv2.imwrite('scratch/wing_fit_initial.png', vis[400:800, 120:320])
