import cv2
import numpy as np

for name in ['panel_1', 'panel_2', 'panel_3', 'panel_4', 'panel_5']:
    p = cv2.imread(f'scratch/waving_panels/{name}.png')
    gray = cv2.cvtColor(p, cv2.COLOR_BGR2GRAY)
    # Find minimum gray in left eye region (x in [100, 160], y in [70, 130])
    l_reg = gray[70:130, 100:160]
    yl, xl = np.unravel_index(np.argmin(l_reg), l_reg.shape)
    left_pt = (xl + 100, yl + 70)
    
    # Right eye region (x in [170, 230], y in [70, 130])
    r_reg = gray[70:130, 170:230]
    yr, xr = np.unravel_index(np.argmin(r_reg), r_reg.shape)
    right_pt = (xr + 170, yr + 70)
    
    dist = right_pt[0] - left_pt[0]
    print(f"{name}: Left Eye={left_pt} (val={l_reg.min()}), Right Eye={right_pt} (val={r_reg.min()}), dist={dist}")
