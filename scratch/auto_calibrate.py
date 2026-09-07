import sys, os, time
sys.path.append(".")
import cv2, numpy as np
from PIL import Image
from scripts.benchmark_owluko_fidelity import compute_ssim_numpy, render_svg, evaluate_fidelity

ref_img = Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA")
ref = np.array(ref_img)
ref_mask = ref[:, :, 3] > 20
ref_gray = cv2.cvtColor(ref[:, :, :3], cv2.COLOR_RGB2GRAY)
ref_lab = cv2.cvtColor(ref[:, :, :3], cv2.COLOR_RGB2LAB).astype(np.float32)

with open("scratch/owluko_body_path_131.txt", "r") as f:
    body_d = f.read().strip()

def eval_svg(svg_str, name="scratch/temp_opt.svg"):
    with open(name, "w") as f:
        f.write(svg_str)
    out_png = render_svg(name, name.replace(".svg", ".png"))
    vec = np.array(Image.open(out_png).convert("RGBA"))
    
    vec_mask = vec[:, :, 3] > 20
    inter = ref_mask & vec_mask
    union = ref_mask | vec_mask
    iou = inter.sum() / (union.sum() + 1e-6)
    
    vec_gray = cv2.cvtColor(vec[:, :, :3], cv2.COLOR_RGB2GRAY)
    ssim_map = compute_ssim_numpy(ref_gray, vec_gray)
    ssim = np.pad(ssim_map, 5, mode="edge")[inter].mean()
    
    vec_lab = cv2.cvtColor(vec[:, :, :3], cv2.COLOR_RGB2LAB).astype(np.float32)
    delta_e = np.sqrt(np.sum((ref_lab - vec_lab)**2, axis=2))[inter].mean()
    
    r_flat = ref[:, :, :3][inter].astype(np.float32).ravel()
    v_flat = vec[:, :, :3][inter].astype(np.float32).ravel()
    ncc = np.corrcoef(r_flat, v_flat)[0, 1]
    
    return iou, ssim, ncc, delta_e

print("Optimizer evaluator ready.")
