import numpy as np
from PIL import Image

vec = np.array(Image.open("scratch/temp_svg_rendered.png").convert("RGBA"))
print("Vec at (X=255, Y=465):", vec[465, 255])
print("Vec at (X=250, Y=450):", vec[450, 250])
print("Vec at (X=250, Y=480):", vec[480, 250])
