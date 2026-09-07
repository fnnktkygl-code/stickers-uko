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

def render_svg_chrome(svg_str, out_png="scratch/temp_meoweko_v2.png"):
    abs_out = os.path.abspath(out_png)
    html_wrap = "scratch/temp_wrap_m2.html"
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
    master_svg = f.read()

# Let's test modifications systematically:
# 1. Clean up whiteCoatGrad (make it warm ivory cream, avoid dirty grey at stop 70% and 100%)
svg_mod = master_svg.replace(
'''    <radialGradient id="whiteCoatGrad" cx="63.5%" cy="61.5%" r="42%">
      <stop offset="0%" stop-color="#EFE5DC" />
      <stop offset="35%" stop-color="#E4D6CB" />
      <stop offset="70%" stop-color="#C8B6A6" />
      <stop offset="100%" stop-color="#A69280" />
    </radialGradient>''',
'''    <radialGradient id="whiteCoatGrad" cx="60%" cy="58%" r="48%">
      <stop offset="0%" stop-color="#FBF7F0" />
      <stop offset="35%" stop-color="#F2E6DA" />
      <stop offset="70%" stop-color="#DCCDC0" />
      <stop offset="100%" stop-color="#BAA596" />
    </radialGradient>'''
)

# 2. Clean up blazeContinuousGrad & muzzleCheeksGrad
svg_mod = svg_mod.replace(
'''    <linearGradient id="blazeContinuousGrad" x1="45%" y1="0%" x2="55%" y2="100%">
      <stop offset="0%" stop-color="#DAC5B6" />
      <stop offset="20%" stop-color="#E4D2C5" />
      <stop offset="50%" stop-color="#E8D8CC" />
      <stop offset="80%" stop-color="#D6C2B2" />
      <stop offset="100%" stop-color="#C4AC9C" />
    </linearGradient>''',
'''    <linearGradient id="blazeContinuousGrad" x1="45%" y1="0%" x2="55%" y2="100%">
      <stop offset="0%" stop-color="#F2E7DC" />
      <stop offset="20%" stop-color="#FBF7F2" />
      <stop offset="50%" stop-color="#F8EFE7" />
      <stop offset="80%" stop-color="#E8D8CC" />
      <stop offset="100%" stop-color="#D6C2B2" />
    </linearGradient>'''
)

# 3. Remove circular cheek stickers and replace with soft blush
old_cheeks = '''    <ellipse cx="355" cy="195" rx="25" ry="22" fill="#FCD8A8" opacity="0.50" />
    <ellipse cx="188" cy="195" rx="20" ry="18" fill="#E8B888" opacity="0.22" />'''
new_cheeks = '''    <ellipse cx="348" cy="198" rx="22" ry="16" fill="#F8B884" opacity="0.28" />
    <ellipse cx="195" cy="198" rx="18" ry="14" fill="#D68A56" opacity="0.16" />'''
svg_mod = svg_mod.replace(old_cheeks, new_cheeks)

# 4. Refine the organic leg separation:
old_legs = '''    <!-- 6. VOLUMETRIC FRONT LEGS (Smooth Organic Blending) -->
    <path d="M 235 350 C 228 390, 222 435, 228 472 L 271 472 L 271 335 C 260 335, 242 338, 235 350 Z" fill="url(#legLeftGrad)" opacity="0.85" />
    <path d="M 271 335 L 271 472 L 314 472 C 320 435, 314 390, 307 350 C 300 338, 282 335, 271 335 Z" fill="url(#legRightGrad)" opacity="0.85" />
    <!-- Ambient Occlusion Crease -->
    <path d="M 270.2 345 C 270.5 390, 269.0 450, 267.0 488 L 275.0 488 C 273.0 450, 272.5 390, 272.8 345 Z" fill="url(#creaseGrad)" />'''

new_legs = '''    <!-- 6. VOLUMETRIC FRONT LEGS (Smooth Organic Curvature) -->
    <!-- Left Leg Form -->
    <path d="M 240 340 C 230 380, 224 430, 228 472 L 271 472 C 268 450, 269 410, 271.5 375 C 265 355, 252 342, 240 340 Z" fill="url(#legLeftGrad)" opacity="0.80" />
    <!-- Right Leg Form -->
    <path d="M 271.5 375 C 274 410, 275 450, 271 472 L 314 472 C 318 430, 312 380, 302 340 C 290 342, 278 355, 271.5 375 Z" fill="url(#legRightGrad)" opacity="0.80" />
    <!-- Ambient Occlusion Crease (starts at Y=375, gentle curve) -->
    <path d="M 271.5 375 C 271.5 405, 269.5 445, 268.5 488 L 274.5 488 C 273.5 445, 271.5 405, 271.5 375 Z" fill="url(#creaseGrad)" />'''

svg_mod = svg_mod.replace(old_legs, new_legs)

# 5. Add delicate whiskers:
whiskers = '''    <!-- 10. FELINE VIBRISSAE / WHISKERS -->
    <path d="M 235 214 C 215 210, 195 211, 175 215" stroke="#FFFFFF" stroke-width="1.6" stroke-linecap="round" fill="none" opacity="0.90" />
    <path d="M 233 221 C 213 222, 193 227, 173 234" stroke="#FFFFFF" stroke-width="1.6" stroke-linecap="round" fill="none" opacity="0.90" />
    <path d="M 234 227 C 216 233, 198 243, 182 254" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round" fill="none" opacity="0.85" />
    <path d="M 308 214 C 328 210, 348 211, 368 215" stroke="#FFFFFF" stroke-width="1.6" stroke-linecap="round" fill="none" opacity="0.90" />
    <path d="M 310 221 C 330 222, 350 227, 370 234" stroke="#FFFFFF" stroke-width="1.6" stroke-linecap="round" fill="none" opacity="0.90" />
    <path d="M 309 227 C 327 233, 345 243, 361 254" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round" fill="none" opacity="0.85" />'''

svg_mod = svg_mod.replace('</g>\n</g>\n</svg>', whiskers + '\n  </g>\n</g>\n</svg>')

rendered = render_svg_chrome(svg_mod)
res = evaluate(rendered)
print(f"Meoweko v2: IoU: {res['iou']*100:.2f}%, SSIM: {res['ssim']*100:.2f}%, NCC: {res['ncc']*100:.2f}%, Delta E: {res['delta_e']:.2f}")

with open("scratch/test_meoweko_v2.svg", "w", encoding="utf-8") as f:
    f.write(svg_mod)
