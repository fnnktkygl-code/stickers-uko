import cv2
import numpy as np

def get_contours():
    front = cv2.imread('mascots/owluko/owluko_turnaround_view_1_front.png', cv2.IMREAD_UNCHANGED)
    profile = cv2.imread('mascots/owluko/owluko_turnaround_view_2_profile_right.png', cv2.IMREAD_UNCHANGED)
    
    alpha_f = front[:, :, 3]
    alpha_p = profile[:, :, 3]
    
    # Analyze body rows from Y=40 to 450 (above feet)
    slices = []
    for y in range(40, 451, 10):
        xf = np.where(alpha_f[y, :] > 50)[0]
        xp = np.where(alpha_p[y, :] > 50)[0]
        if len(xf) > 0 and len(xp) > 0:
            wf = xf.max() - xf.min() + 1
            cf = (xf.max() + xf.min()) / 2.0
            wp = xp.max() - xp.min() + 1
            cp = (xp.max() + xp.min()) / 2.0
            slices.append((y, xf.min(), xf.max(), wf, cf, xp.min(), xp.max(), wp, cp))
            
    print(f"Extracted {len(slices)} cross-section slices.")
    print("Top slice (Y=40):", slices[0])
    print("Mid slice (Y=250):", [s for s in slices if s[0] == 250][0])
    print("Lower slice (Y=440):", slices[-1])

if __name__ == "__main__":
    get_contours()
