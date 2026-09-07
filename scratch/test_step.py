import sys
import numpy as np
import cv2
from PIL import Image
from scripts.benchmark_owluko_fidelity import render_svg, evaluate_fidelity

ref_png = "mascots/owluko/owluko_master_exact_512.png"

# Read body path
with open("scratch/owluko_body_path_131.txt", "r") as f:
    body_d = f.read().strip()

print(f"Loaded body path with length {len(body_d)}")
