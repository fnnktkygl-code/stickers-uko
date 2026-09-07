import os, sys, re, subprocess, cv2, numpy as np
from PIL import Image

def compute_ssim_numpy(img1, img2):
    C1 = (0.01 * 255)**2
    C2 = (0.03 * 255)**2
    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)
    kernel = cv2.getGaussianKernel(11, 1.5)
    window = np.outer(kernel, kernel.transpose())
    mu1 = cv2.filter2D(img1, -1, window)[5:-5, 5:-5]
    mu2 = cv2.filter2D(img2, -1, window)[5:-5, 5:-5]
    mu1_sq = mu1**2
    mu2_sq = mu2**2
    mu1_mu2 = mu1 * mu2
    sigma1_sq = cv2.filter2D(img1**2, -1, window)[5:-5, 5:-5] - mu1_sq
    sigma2_sq = cv2.filter2D(img2**2, -1, window)[5:-5, 5:-5] - mu2_sq
    sigma12 = cv2.filter2D(img1 * img2, -1, window)[5:-5, 5:-5] - mu1_mu2
    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))
    return ssim_map

def render_svg_chrome(svg_str, out_png="scratch/temp_aituko_test.png"):
    abs_out = os.path.abspath(out_png)
    html_wrap = "scratch/temp_wrap_aituko.html"
    with open(html_wrap, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html><html><head><style>
html, body {{ margin: 0; padding: 0; width: 512px; height: 512px; overflow: hidden; background: transparent; }}
svg {{ display: block; width: 512px; height: 512px; }}
</style></head><body>{svg_str}</body></html>""")
    cmd = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--screenshot={abs_out}",
        "--window-size=512,512",
        "--default-background-color=00000000",
        f"file://{os.path.abspath(html_wrap)}"
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return abs_out

def evaluate(rendered_png, ref_png="mascots/aituko/aituko_master_exact_512.png"):
    ref = np.array(Image.open(ref_png).convert("RGBA"))
    vec = np.array(Image.open(rendered_png).convert("RGBA"))
    inter = (ref[:, :, 3] > 20) & (vec[:, :, 3] > 20)
    union = (ref[:, :, 3] > 20) | (vec[:, :, 3] > 20)
    iou = inter.sum() / (union.sum() + 1e-6)

    ref_gray = cv2.cvtColor(ref[:, :, :3], cv2.COLOR_BGR2GRAY)
    vec_gray = cv2.cvtColor(vec[:, :, :3], cv2.COLOR_BGR2GRAY)
    ssim_map = compute_ssim_numpy(ref_gray, vec_gray)
    ssim_val = np.pad(ssim_map, 5, mode='edge')[inter].mean()

    ref_flat = ref[:, :, :3][inter].astype(np.float32).ravel()
    vec_flat = vec[:, :, :3][inter].astype(np.float32).ravel()
    ncc = np.corrcoef(ref_flat, vec_flat)[0, 1]

    ref_lab = cv2.cvtColor(ref[:, :, :3], cv2.COLOR_BGR2LAB).astype(np.float32)
    vec_lab = cv2.cvtColor(vec[:, :, :3], cv2.COLOR_BGR2LAB).astype(np.float32)
    delta_e = np.sqrt(np.sum((ref_lab - vec_lab)**2, axis=2))[inter].mean()

    return {"iou": iou, "ssim": ssim_val, "ncc": ncc, "delta_e": delta_e}

with open("mascots/aituko/aituko_master_exact_512.svg", "r", encoding="utf-8") as f:
    master_svg = f.read()

# 1. Calibrate visorGlass to match measured curve
new_visor = '''    <!-- Obsidian Visor -->
    <linearGradient id="visorGlass" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#8C8278" />
      <stop offset="14%" stop-color="#5E564E" />
      <stop offset="28%" stop-color="#141312" />
      <stop offset="55%" stop-color="#0A0B0D" />
      <stop offset="100%" stop-color="#080707" />
    </linearGradient>'''
svg_mod = re.sub(r'<!-- Obsidian Visor -->\s*<linearGradient id="visorGlass".*?</linearGradient>', new_visor, master_svg, flags=re.DOTALL)

# 2. Visor stroke: remove bluish tint
svg_mod = svg_mod.replace('stroke="#2A3245" stroke-width="0.8"', 'stroke="#141312" stroke-width="0.6"')

# 3. Ground shadow smooth falloff
new_ground = '''    <!-- Ground Contact Shadow Calibrated -->
    <radialGradient id="groundShadow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.61" />
      <stop offset="50%" stop-color="#000000" stop-opacity="0.45" />
      <stop offset="80%" stop-color="#000000" stop-opacity="0.18" />
      <stop offset="92%" stop-color="#000000" stop-opacity="0.06" />
      <stop offset="100%" stop-color="#000000" stop-opacity="0.0" />
    </radialGradient>'''
svg_mod = re.sub(r'<!-- Ground Contact Shadow Calibrated -->\s*<radialGradient id="groundShadow".*?</radialGradient>', new_ground, svg_mod, flags=re.DOTALL)

# 4. Calibrate torsoGrad highlight (measured peak was [247, 232, 226], not [255, 253, 245])
old_torso = '''      <stop offset="0%" stop-color="#A89B8E" />
      <stop offset="12%" stop-color="#FFFDF5" />
      <stop offset="22%" stop-color="#FAF7F2" />'''
new_torso = '''      <stop offset="0%" stop-color="#A89B8E" />
      <stop offset="12%" stop-color="#F5EBE4" />
      <stop offset="22%" stop-color="#EADBCE" />'''
svg_mod = svg_mod.replace(old_torso, new_torso)

rendered = render_svg_chrome(svg_mod)
res = evaluate(rendered)
print(f"AItuko calibrated: IoU: {res['iou']*100:.2f}%, SSIM: {res['ssim']*100:.2f}%, NCC: {res['ncc']*100:.2f}%, Delta E: {res['delta_e']:.2f}")

with open("mascots/aituko/aituko_master_exact_512.svg", "w", encoding="utf-8") as f:
    f.write(svg_mod)
