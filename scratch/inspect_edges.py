from PIL import Image
import numpy as np

img = Image.open("mascots/owluko/owluko_user_master_ref.png").convert("RGB")
arr = np.array(img)
print("Corners and borders:")
print("Top-left 5x5:", arr[:5, :5, 0])
print("Left edge min R:", arr[:, 0, 0].min(), "max R:", arr[:, 0, 0].max())
print("Right edge min R:", arr[:, -1, 0].min(), "max R:", arr[:, -1, 0].max())
print("Top edge min R:", arr[0, :, 0].min(), "max R:", arr[0, :, 0].max())
print("Bottom edge min R:", arr[-1, :, 0].min(), "max R:", arr[-1, :, 0].max())
