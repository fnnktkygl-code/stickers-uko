import sys
sys.path.append(".")
import cv2, numpy as np
from PIL import Image
from scripts.benchmark_owluko_fidelity import compute_ssim_numpy, render_svg

ref_full = np.array(Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA"))
ref_face = ref_full[120:230, 155:355]

def eval_face_svg(svg_path):
    png = render_svg(svg_path, "scratch/temp_face_eval.png")
    vec_full = np.array(Image.open(png).convert("RGBA"))
    vec_face = vec_full[120:230, 155:355]
    
    bg = np.array([11, 15, 23], dtype=np.float32)
    a_ref = ref_face[:, :, 3:4].astype(float) / 255.0
    r_comp = np.clip(ref_face[:, :, :3] * a_ref + bg * (1.0 - a_ref), 0, 255).astype(np.uint8)
    
    a_vec = vec_face[:, :, 3:4].astype(float) / 255.0
    v_comp = np.clip(vec_face[:, :, :3] * a_vec + bg * (1.0 - a_vec), 0, 255).astype(np.uint8)
    
    r_gray = cv2.cvtColor(r_comp, cv2.COLOR_RGB2GRAY)
    v_gray = cv2.cvtColor(v_comp, cv2.COLOR_RGB2GRAY)
    ssim = compute_ssim_numpy(r_gray, v_gray).mean()
    
    r_lab = cv2.cvtColor(r_comp, cv2.COLOR_RGB2LAB).astype(np.float32)
    v_lab = cv2.cvtColor(v_comp, cv2.COLOR_RGB2LAB).astype(np.float32)
    delta_e = np.sqrt(np.sum((r_lab - v_lab)**2, axis=2)).mean()
    
    r_flat = r_comp.astype(np.float32).ravel()
    v_flat = v_comp.astype(np.float32).ravel()
    ncc = np.corrcoef(r_flat, v_flat)[0, 1]
    
    print(f"FACE REGION: SSIM: {ssim*100:.2f}%, NCC: {ncc*100:.2f}%, Delta E: {delta_e:.2f}")
    return ssim, ncc, delta_e

if __name__ == "__main__":
    eval_face_svg("scratch/test_owluko_master_v1.svg")
