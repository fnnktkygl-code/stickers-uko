import sys, re
sys.path.append(".")
from scripts.benchmark_owluko_fidelity import render_svg, evaluate_fidelity

with open("scratch/test_right_brow.svg", "r") as f:
    base_svg = f.read()

best_ncc = 0.8379
best_ssim = 0.8190
best_params = None

# Sweep bodyGrad angles and stops
for x1 in [20, 25, 30]:
    for x2 in [65, 70, 75]:
        for y2 in [90, 95, 100]:
            # replace x1, x2, y2
            svg = re.sub(r'linearGradient id="bodyGrad" x1="[^"]+" y1="[^"]+" x2="[^"]+" y2="[^"]+"',
                         f'linearGradient id="bodyGrad" x1="{x1}%" y1="5%" x2="{x2}%" y2="{y2}%"', base_svg)
            
            with open("scratch/temp_sweep.svg", "w") as f:
                f.write(svg)
            out_png = render_svg("scratch/temp_sweep.svg", "scratch/temp_sweep.png")
            # compute metrics quickly
            from PIL import Image
            import numpy as np, cv2
            from scripts.benchmark_owluko_fidelity import compute_ssim_numpy
            ref = np.array(Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA"))
            vec = np.array(Image.open(out_png).convert("RGBA"))
            inter = (ref[:, :, 3] > 20) & (vec[:, :, 3] > 20)
            
            r_flat = ref[:, :, :3][inter].astype(float).ravel()
            v_flat = vec[:, :, :3][inter].astype(float).ravel()
            ncc = np.corrcoef(r_flat, v_flat)[0, 1]
            
            r_gray = cv2.cvtColor(ref[:, :, :3], cv2.COLOR_RGB2GRAY)
            v_gray = cv2.cvtColor(vec[:, :, :3], cv2.COLOR_RGB2GRAY)
            ssim = np.pad(compute_ssim_numpy(r_gray, v_gray), 5, mode="edge")[inter].mean()
            
            print(f"x1={x1}, x2={x2}, y2={y2} -> SSIM={ssim*100:.2f}%, NCC={ncc*100:.2f}%")
            if ssim + ncc > best_ssim + best_ncc:
                best_ssim = ssim
                best_ncc = ncc
                best_params = (x1, x2, y2)

print(f"\nBest params: {best_params} -> SSIM={best_ssim*100:.2f}%, NCC={best_ncc*100:.2f}%")
