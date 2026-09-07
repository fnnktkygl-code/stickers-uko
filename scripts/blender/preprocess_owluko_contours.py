import cv2
import numpy as np
import json
import os
from scipy.ndimage import gaussian_filter1d

def extract():
    front = cv2.imread('mascots/owluko/owluko_turnaround_view_1_front.png', cv2.IMREAD_UNCHANGED)
    profile = cv2.imread('mascots/owluko/owluko_turnaround_view_2_profile_right.png', cv2.IMREAD_UNCHANGED)
    
    alpha_f = front[:, :, 3]
    alpha_p = profile[:, :, 3]
    
    # Analyze where alpha starts at the top
    top_ys, top_xs = np.where(alpha_f > 20)
    y_min = int(top_ys.min())
    print(f"Alpha starts at Y={y_min}") # should be 38-40
    
    num_rings = 100
    y_values = np.linspace(y_min + 1, 442, num_rings)
    
    raw_rx, raw_cx = [], []
    raw_ry, raw_cy = [], []
    z_values = []
    
    for y in y_values:
        y_int = int(round(y))
        xf = np.where(alpha_f[y_int, :] > 40)[0]
        xp = np.where(alpha_p[y_int, :] > 40)[0]
        
        rx = (xf.max() - xf.min()) / 2.0 * 0.005 if len(xf) > 0 else 0.05
        cx = ((xf.max() + xf.min()) / 2.0 - 255.5) * 0.005 if len(xf) > 0 else 0.0
        
        ry = (xp.max() - xp.min()) / 2.0 * 0.005 if len(xp) > 0 else 0.05
        cy = ((xp.max() + xp.min()) / 2.0 - 256.0) * 0.005 if len(xp) > 0 else 0.0
        
        z = 0.970 + (256.0 - y) * 0.005
        
        raw_rx.append(rx)
        raw_cx.append(cx)
        raw_ry.append(ry)
        raw_cy.append(cy)
        z_values.append(z)
        
    smooth_rx = gaussian_filter1d(raw_rx, sigma=1.5)
    smooth_cx = gaussian_filter1d(raw_cx, sigma=1.5)
    smooth_ry = gaussian_filter1d(raw_ry, sigma=1.5)
    smooth_cy = gaussian_filter1d(raw_cy, sigma=1.5)
    
    rings = []
    for i in range(num_rings):
        rings.append({
            'y_img': float(y_values[i]),
            'z_3d': float(z_values[i]),
            'rx': float(smooth_rx[i]),
            'cx': float(smooth_cx[i]),
            'ry': float(smooth_ry[i]),
            'cy': float(smooth_cy[i])
        })
        
    data = {
        'num_rings': num_rings,
        'rings': rings,
        'top_pole_z': float(0.970 + (256.0 - float(y_min)) * 0.005),
        'top_pole_cx': float(smooth_cx[0]),
        'top_pole_cy': float(smooth_cy[0]),
        'bottom_pole_z': float(0.970 + (256.0 - 446.0) * 0.005),
        'bottom_pole_cx': float(smooth_cx[-1]),
        'bottom_pole_cy': float(smooth_cy[-1]),
        'ortho_scale': 2.560,
        'cam_z': 0.970
    }
    
    os.makedirs("scratch", exist_ok=True)
    out_path = "scratch/owluko_contours.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Preprocessed {num_rings} smoothed contour rings to {out_path}")

if __name__ == "__main__":
    extract()
