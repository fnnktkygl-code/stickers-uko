import cv2
import numpy as np
import json
import os
from scipy.ndimage import gaussian_filter1d

def extract():
    front = cv2.imread('scratch/ref_plane_front.png', cv2.IMREAD_UNCHANGED)
    profile = cv2.imread('scratch/ref_plane_profile.png', cv2.IMREAD_UNCHANGED)
    
    alpha_f = front[:, :, 3]
    alpha_p = profile[:, :, 3]
    
    # Analyze vertical range: top of head at Y=40, pelvic base at Y=420
    # Baseline for feet is Y=489
    y_min = 40
    y_pelvis_end = 415
    
    num_rings = 120
    y_vals = np.linspace(y_min + 1, y_pelvis_end, num_rings)
    
    rings = []
    
    raw_rx, raw_cx = [], []
    raw_ry_front, raw_ry_back, raw_cy = [], [], []
    z_vals = []
    
    for y in y_vals:
        y_int = int(round(y))
        
        # Front slice: gives left/right profile in X
        xf = np.where(alpha_f[y_int, :] > 30)[0]
        if len(xf) > 0:
            rx = (xf.max() - xf.min()) / 2.0 * 0.005
            cx = ((xf.max() + xf.min()) / 2.0 - 256.0) * 0.005
        else:
            rx = 0.05
            cx = 0.0
            
        # Profile slice: bird faces LEFT in profile!
        # x_min is front of bird (-Y in Blender), x_max is back of bird (+Y in Blender)
        xp = np.where(alpha_p[y_int, :] > 30)[0]
        if len(xp) > 0:
            # We want Y in Blender to be 0 at the center of the bird
            # Reference center is around 250 in profile image
            y_front_px = xp.min() # -Y in Blender
            y_back_px = xp.max()  # +Y in Blender
            
            # Midpoint of bird in profile
            mid_p = (y_front_px + y_back_px) / 2.0
            cy = (mid_p - 248.0) * 0.005
            
            # Front radius and back radius (allowing asymmetric body!)
            ry_front = (mid_p - y_front_px) * 0.005
            ry_back = (y_back_px - mid_p) * 0.005
        else:
            cy = 0.0
            ry_front = 0.05
            ry_back = 0.05
            
        z = 0.970 + (256.0 - y) * 0.005
        
        raw_rx.append(rx)
        raw_cx.append(cx)
        raw_ry_front.append(ry_front)
        raw_ry_back.append(ry_back)
        raw_cy.append(cy)
        z_vals.append(z)
        
    smooth_rx = gaussian_filter1d(raw_rx, sigma=1.2)
    smooth_cx = gaussian_filter1d(raw_cx, sigma=1.2)
    smooth_ry_front = gaussian_filter1d(raw_ry_front, sigma=1.2)
    smooth_ry_back = gaussian_filter1d(raw_ry_back, sigma=1.2)
    smooth_cy = gaussian_filter1d(raw_cy, sigma=1.2)
    
    for i in range(num_rings):
        rings.append({
            'y_img': float(y_vals[i]),
            'z_3d': float(z_vals[i]),
            'rx': float(smooth_rx[i]),
            'cx': float(smooth_cx[i]),
            'ry_front': float(smooth_ry_front[i]),
            'ry_back': float(smooth_ry_back[i]),
            'cy': float(smooth_cy[i])
        })
        
    out_data = {
        'num_rings': num_rings,
        'rings': rings,
        'top_pole_z': float(0.970 + (256.0 - 40.0) * 0.005),
        'top_pole_cx': float(smooth_cx[0]),
        'top_pole_cy': float(smooth_cy[0]),
        'bottom_pole_z': float(0.970 + (256.0 - 422.0) * 0.005),
        'bottom_pole_cx': float(smooth_cx[-1]),
        'bottom_pole_cy': float(smooth_cy[-1])
    }
    
    out_path = 'scratch/owluko_dual_ortho_contours.json'
    with open(out_path, 'w') as f:
        json.dump(out_data, f, indent=2)
    print(f'Extracted {num_rings} dual-ortho rings to {out_path}')

if __name__ == '__main__':
    extract()
