import sys
sys.path.append('.')
from scratch.fit_rive_wing import render_rive_polygon
import cv2
import numpy as np
from scipy.optimize import minimize
import json

gt = cv2.imread('scratch/gt_wing_mask.png', cv2.IMREAD_GRAYSCALE)
gt_bool = gt > 0
origin = (224, 590)

# 8 points relative to origin (224, 590):
# 0: shoulder_top   (0, -155)     [224, 435]
# 1: shoulder_curve (-28, -115)   [196, 475]
# 2: upper_flank    (-48, -60)    [176, 530]
# 3: mid_apex       (-59, 10)     [165, 600]
# 4: lower_outer    (-44, 90)     [180, 680]
# 5: tip_apex       (26, 156)     [250, 746]
# 6: crease_lower   (12, 90)      [236, 680]
# 7: crease_mid     (-3, 0)       [221, 590]

initial_params = np.array([
    # x, y, rot, outD, inRot, inD
    0.0, -155.0, 130.0, 35.0, -75.0, 35.0,
    -28.0, -115.0, 115.0, 30.0, -65.0, 30.0,
    -48.0, -60.0, 95.0, 35.0, -85.0, 35.0,
    -59.0, 10.0, 80.0, 45.0, -100.0, 45.0,
    -44.0, 90.0, 55.0, 40.0, -125.0, 40.0,
    26.0, 156.0, -25.0, 30.0, 155.0, 30.0,
    12.0, 90.0, -85.0, 45.0, 95.0, 45.0,
    -3.0, 0.0, -95.0, 50.0, 85.0, 50.0
])

def unpack_params(p):
    pts = []
    for i in range(8):
        idx = i * 6
        pts.append({
            'x': p[idx],
            'y': p[idx+1],
            'cubic': {
                'rotation': p[idx+2],
                'outDistance': max(2.0, p[idx+3]),
                'inRotation': p[idx+4],
                'inDistance': max(2.0, p[idx+5])
            }
        })
    return pts

def loss_func(p):
    pts = unpack_params(p)
    pred, _ = render_rive_polygon(pts, origin)
    pred_bool = pred > 0
    inter = np.logical_and(gt_bool, pred_bool).sum()
    union = np.logical_or(gt_bool, pred_bool).sum()
    if union == 0: return 1.0
    return 1.0 - (inter / union)

print("Starting 8-point optimization...")
res = minimize(loss_func, initial_params, method='Powell', options={'maxiter': 20, 'disp': True})
best_iou = (1.0 - res.fun) * 100
print(f"Optimized 8-Point IoU: {best_iou:.2f}%")

best_pts = unpack_params(res.x)
with open('scratch/optimized_8pts_wing.json', 'w') as f:
    json.dump({'origin': origin, 'points': best_pts, 'iou': best_iou}, f, indent=2)

pred, _ = render_rive_polygon(best_pts, origin)
pred_bool = pred > 0
vis = np.zeros((1024, 1024, 3), dtype=np.uint8)
vis[gt_bool] = [100, 220, 100]
vis[pred_bool] = [50, 100, 255]
vis[np.logical_and(gt_bool, pred_bool)] = [255, 255, 255]
cv2.imwrite('scratch/wing_8pts_fit.png', vis[400:800, 120:320])
print("Saved scratch/wing_8pts_fit.png")
