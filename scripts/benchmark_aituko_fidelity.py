import os, sys, re, subprocess, cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont

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

def render_svg_chrome(svg_path, out_png="scratch/temp_aituko_svg_rendered.png"):
    abs_svg = os.path.abspath(svg_path)
    abs_out = os.path.abspath(out_png)
    
    if svg_path.endswith(".html"):
        file_url = f"file://{abs_svg}"
    else:
        html_wrap = "scratch/temp_wrap_svg.html"
        with open(abs_svg, "r", encoding="utf-8") as f:
            svg_content = f.read()
        svg_content = re.sub(r'style="[^"]*background-color:\s*#[^;"]+;?[^"]*"', 'style="background: transparent; overflow: visible;"', svg_content)
        svg_content = re.sub(r'style="[^"]*background:\s*#[^;"]+;?[^"]*"', 'style="background: transparent; overflow: visible;"', svg_content)

        with open(html_wrap, "w", encoding="utf-8") as f:
            f.write(f"""<!DOCTYPE html><html><head><style>
html, body {{ margin: 0; padding: 0; width: 512px; height: 512px; overflow: hidden; background: transparent; }}
svg {{ display: block; width: 512px; height: 512px; }}
</style></head><body>{svg_content}</body></html>""")
        file_url = f"file://{os.path.abspath(html_wrap)}"

    cmd = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--screenshot={abs_out}",
        "--window-size=512,512",
        "--default-background-color=00000000",
        file_url
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return abs_out

def render_lottie_chrome(lottie_path, out_png="scratch/temp_aituko_lottie_rendered.png"):
    abs_out = os.path.abspath(out_png)
    with open(lottie_path, "r", encoding="utf-8") as f:
        lottie_json_str = f.read()

    with open("scratch/lottie.min.js", "r", encoding="utf-8") as js_f:
        lottie_min_js = js_f.read()
        
    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    html, body {{ width: 512px; height: 512px; background: transparent; overflow: hidden; }}
    #container {{ width: 512px; height: 512px; }}
  </style>
  <script>
    {lottie_min_js}
  </script>
</head>
<body>
  <div id="container"></div>
  <script>
    const animData = {lottie_json_str};
    window.anim = lottie.loadAnimation({{
      container: document.getElementById('container'),
      renderer: 'svg',
      loop: false,
      autoplay: false,
      animationData: animData
    }});
    window.anim.goToAndStop(0, true);
  </script>
</body>
</html>
"""
    html_path = "scratch/temp_render_lottie_aituko.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    abs_html = os.path.abspath(html_path)
    cmd = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=1000",
        f"--screenshot={abs_out}",
        "--window-size=512,512",
        "--default-background-color=00000000",
        f"file://{abs_html}"
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return abs_out

def evaluate_aituko(rendered_png, ref_png="mascots/aituko/aituko_master_exact_512.png"):
    ref_img = Image.open(ref_png).convert("RGBA")
    vec_img = Image.open(rendered_png).convert("RGBA")
    
    ref = np.array(ref_img)
    vec = np.array(vec_img)
    
    ref_alpha = ref[:, :, 3]
    vec_alpha = vec[:, :, 3]
    
    ref_mask = ref_alpha > 20
    vec_mask = vec_alpha > 20
    
    inter = np.logical_and(ref_mask, vec_mask)
    union = np.logical_or(ref_mask, vec_mask)
    iou = inter.sum() / (union.sum() + 1e-6)
    
    ref_gray = cv2.cvtColor(ref[:, :, :3], cv2.COLOR_RGB2GRAY)
    vec_gray = cv2.cvtColor(vec[:, :, :3], cv2.COLOR_RGB2GRAY)
    ssim_map = compute_ssim_numpy(ref_gray, vec_gray)
    ssim_full = np.pad(ssim_map, 5, mode='edge')
    fg_ssim = ssim_full[inter].mean()
    
    ref_lab = cv2.cvtColor(ref[:, :, :3], cv2.COLOR_RGB2LAB).astype(np.float32)
    vec_lab = cv2.cvtColor(vec[:, :, :3], cv2.COLOR_RGB2LAB).astype(np.float32)
    delta_e = np.sqrt(np.sum((ref_lab - vec_lab)**2, axis=2))
    fg_delta_e = delta_e[inter].mean()
    
    ref_flat = ref[:, :, :3][inter].astype(np.float32).ravel()
    vec_flat = vec[:, :, :3][inter].astype(np.float32).ravel()
    ncc = np.corrcoef(ref_flat, vec_flat)[0, 1]
    
    mse = np.mean((ref[:, :, :3][inter].astype(np.float32) - vec[:, :, :3][inter].astype(np.float32))**2)
    psnr = 10 * np.log10(255**2 / (mse + 1e-6))
    
    print(f"Silhouette IoU: {iou * 100:.4f}% ({iou:.6f})")
    print(f"Structural SSIM: {fg_ssim * 100:.4f}% ({fg_ssim:.6f})")
    print(f"Color Correlation (NCC): {ncc * 100:.4f}% ({ncc:.6f})")
    print(f"Delta E: {fg_delta_e:.4f}")
    print(f"MSE: {mse:.4f}")
    print(f"PSNR: {psnr:.4f} dB")
    
    return {
        "iou": float(iou),
        "ssim": float(fg_ssim),
        "ncc": float(ncc),
        "delta_e": float(fg_delta_e),
        "mse": float(mse),
        "psnr": float(psnr)
    }

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "scratch/test_aituko_calibrated.svg"
    if target.endswith(".json"):
        png = render_lottie_chrome(target)
    else:
        png = render_svg_chrome(target)
    evaluate_aituko(png)
