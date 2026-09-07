from PIL import Image
import numpy as np

img = Image.open("mascots/owluko/owluko_user_master_ref.png").convert("RGB")
arr = np.array(img)

# Chin tufts are between x=380 and x=644, y=470 and y=550
# Mask is lighter (R>242, G>232, B>212), body below is darker (R<238, G<224, B<200)
chin_crop = arr[480:550, 380:644]
# Find transition y for each column x
boundary_pts = []
for col_idx in range(chin_crop.shape[1]):
    x_glob = 380 + col_idx
    col = chin_crop[:, col_idx]
    # compute gradient in brightness
    diff = np.diff(col[:, 0].astype(float))
    # min diff corresponds to sharpest transition from light mask to darker chest
    min_idx = np.argmin(diff)
    y_glob = 480 + min_idx
    boundary_pts.append((x_glob, y_glob))

# Sample every 5px
print("Sampled chin boundary points (x, y):")
for x, y in boundary_pts[::6]:
    print(f"({x}, {y})", end=", ")
print()

