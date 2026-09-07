import cv2
import numpy as np
from PIL import Image

ref = np.array(Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA"))

# Left Eye
crop_l = ref[140:178, 170:224, :3]
# In Left Eye, where is luminance < 70? (pupil core)
lums = 0.299*crop_l[:,:,0] + 0.587*crop_l[:,:,1] + 0.114*crop_l[:,:,2]
ys, xs = np.where(lums < 65)
print(f"Left Eye Core (lum < 65): X=[{170+xs.min()}, {170+xs.max()}], Y=[{140+ys.min()}, {140+ys.max()}]")
print(f"Left Eye Core center: ({(170+xs.min()+170+xs.max())/2:.1f}, {(140+ys.min()+140+ys.max())/2:.1f}), rx={(xs.max()-xs.min())/2:.1f}, ry={(ys.max()-ys.min())/2:.1f}")

# Right Eye
crop_r = ref[140:178, 280:336, :3]
lums_r = 0.299*crop_r[:,:,0] + 0.587*crop_r[:,:,1] + 0.114*crop_r[:,:,2]
ys_r, xs_r = np.where(lums_r < 55)
print(f"\nRight Eye Core (lum < 55): X=[{280+xs_r.min()}, {280+xs_r.max()}], Y=[{140+ys_r.min()}, {140+ys_r.max()}]")
print(f"Right Eye Core center: ({(280+xs_r.min()+280+xs_r.max())/2:.1f}, {(140+ys_r.min()+140+ys_r.max())/2:.1f}), rx={(xs_r.max()-xs_r.min())/2:.1f}, ry={(ys_r.max()-ys_r.min())/2:.1f}")
