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

def render_svg_chrome(svg_str, out_png="scratch/temp_meoweko_test.png"):
    abs_out = os.path.abspath(out_png)
    html_wrap = "scratch/temp_wrap_meoweko.html"
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

def evaluate(rendered_png, ref_png="mascots/meoweko/meoweko_master_exact_512.png"):
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

with open("mascots/meoweko/meoweko_master_exact_512.svg", "r", encoding="utf-8") as f:
    svg = f.read()

# 1. Replace the concrete leg rectangles and black crease:
old_legs = '''    <!-- 6. VOLUMETRIC FRONT LEGS (Smooth Organic Blending) -->
    <path d="M 235 350 C 228 390, 222 435, 228 472 L 271 472 L 271 335 C 260 335, 242 338, 235 350 Z" fill="url(#legLeftGrad)" opacity="0.85" />
    <path d="M 271 335 L 271 472 L 314 472 C 320 435, 314 390, 307 350 C 300 338, 282 335, 271 335 Z" fill="url(#legRightGrad)" opacity="0.85" />
    <!-- Ambient Occlusion Crease -->
    <path d="M 270.2 345 C 270.5 390, 269.0 450, 267.0 488 L 275.0 488 C 273.0 450, 272.5 390, 272.8 345 Z" fill="url(#creaseGrad)" />'''

new_legs = '''    <!-- 6. ORGANIC FRONT LEGS & SOFT INTER-LEG OCCLUSION -->
    <!-- Soft inter-leg shadow (Starts subtle at Y=380, deepens between paws) -->
    <ellipse cx="271.5" cy="430" rx="8" ry="32" fill="#8C7060" opacity="0.30" />
    <path d="M 270 440 C 270 460, 269 475, 268 488 L 274 488 C 273 475, 272 460, 272 440 Z" fill="#6A4E3E" opacity="0.45" />'''

svg = svg.replace(old_legs, new_legs)

# 2. Remove pitch black crease at baseline
old_crease = '''    <!-- Deep Pitch-Black Crease between front paws at baseline -->
    <path d="M 269 472 L 273 472 L 273 490 L 269 490 Z" fill="#6A4836" opacity="0.55" />'''
svg = svg.replace(old_crease, '')

# 3. Soften neck shadow
old_neck = '<stop offset="0%" stop-color="#8A6E5E" stop-opacity="0.60" />'
new_neck = '<stop offset="0%" stop-color="#8A6E5E" stop-opacity="0.25" />'
svg = svg.replace(old_neck, new_neck)

# 4. Remove chin mud
old_chin = '<ellipse cx="271.5" cy="232" rx="10" ry="4" fill="#C4B0A0" opacity="0.40" />'
svg = svg.replace(old_chin, '')

# 5. Add whiskers!
whiskers = '''    <!-- 10. FELINE VIBRISSAE / WHISKERS -->
    <!-- Left Whiskers -->
    <path d="M 235 214 C 215 210, 195 211, 175 215" stroke="#FFFFFF" stroke-width="1.6" stroke-linecap="round" fill="none" opacity="0.90" />
    <path d="M 233 221 C 213 222, 193 227, 173 234" stroke="#FFFFFF" stroke-width="1.6" stroke-linecap="round" fill="none" opacity="0.90" />
    <path d="M 234 227 C 216 233, 198 243, 182 254" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round" fill="none" opacity="0.85" />
    <!-- Right Whiskers -->
    <path d="M 308 214 C 328 210, 348 211, 368 215" stroke="#FFFFFF" stroke-width="1.6" stroke-linecap="round" fill="none" opacity="0.90" />
    <path d="M 310 221 C 330 222, 350 227, 370 234" stroke="#FFFFFF" stroke-width="1.6" stroke-linecap="round" fill="none" opacity="0.90" />
    <path d="M 309 227 C 327 233, 345 243, 361 254" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round" fill="none" opacity="0.85" />'''

svg = svg.replace('</g>\n</g>\n</svg>', whiskers + '\n  </g>\n</g>\n</svg>')

res = evaluate(render_svg_chrome(svg))
print(f"Step 1 Overhaul: IoU: {res['iou']*100:.2f}%, SSIM: {res['ssim']*100:.2f}%, NCC: {res['ncc']*100:.2f}%, Delta E: {res['delta_e']:.2f}")

with open("scratch/test_meoweko_step1.svg", "w", encoding="utf-8") as f:
    f.write(svg)
