import os, sys, subprocess, re
import cv2, numpy as np
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

def render_svg_chrome(svg_path, out_png):
    abs_svg = os.path.abspath(svg_path)
    abs_out = os.path.abspath(out_png)
    
    html_wrap = f"scratch/temp_wrap_{os.path.basename(svg_path)}.html"
    with open(abs_svg, "r", encoding="utf-8") as f:
        svg_content = f.read()
    svg_content = re.sub(r'style="[^"]*background-color:\s*#[^;"]+;?[^"]*"', 'style="background: transparent; overflow: visible;"', svg_content)
    svg_content = re.sub(r'style="[^"]*background:\s*#[^;"]+;?[^"]*"', 'style="background: transparent; overflow: visible;"', svg_content)

    with open(html_wrap, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html><html><head><style>
html, body {{ margin: 0; padding: 0; width: 512px; height: 512px; overflow: hidden; background: transparent; }}
svg {{ display: block; width: 512px; height: 512px; }}
</style></head><body>{svg_content}</body></html>""")

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

mascots = [
    {
        "id": "owluko",
        "name": "1. OWLUKO (HIBOU - CAPSULE PORCELAINE SANS COL)",
        "ref_path": "mascots/owluko/owluko_master_exact_512.png",
        "svg_path": "mascots/owluko/owluko_master_exact_512.svg",
        "rendered_png": "scratch/temp_owluko_master_rendered.png",
        "bg_dark": (11, 15, 23)
    },
    {
        "id": "aituko",
        "name": "2. AITUKO (ROBOT - VISIÈRE OBSIDIENNE & YEUX CYAN)",
        "ref_path": "mascots/aituko/aituko_master_exact_512.png",
        "svg_path": "mascots/aituko/aituko_master_exact_512.svg",
        "rendered_png": "scratch/temp_aituko_master_rendered.png",
        "bg_dark": (11, 15, 23)
    },
    {
        "id": "meoweko",
        "name": "3. MEOWEKO (CHAT - MANTEAU ROUX & CRÈME BICOLORE)",
        "ref_path": "mascots/meoweko/meoweko_master_exact_512.png",
        "svg_path": "mascots/meoweko/meoweko_master_exact_512.svg",
        "rendered_png": "scratch/temp_meoweko_master_rendered.png",
        "bg_dark": (11, 15, 23)
    }
]

board_w = 512 * 3 + 60
board_h = 420 * 3 + 180
board = Image.new("RGBA", (board_w, board_h), (11, 15, 23, 255))
draw = ImageDraw.Draw(board)

try:
    font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    font_metric = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 13)
except:
    font_title = font_metric = font_sub = ImageFont.load_default()

# Header
draw.rectangle([0, 0, board_w, 85], fill=(15, 23, 42, 255))
draw.line([(0, 85), (board_w, 85)], fill=(217, 155, 38), width=2)
draw.text((30, 16), "AUDIT COMPARATIF STUDIO : MASTER SVG PUR DES 3 MASCOTTES VS 3D CGI (CHROME HEADLESS 512x512)", fill=(255, 255, 255), font=font_title)
draw.text((30, 52), "Mesures mathématiques objectives au pixel près sans concession (Silhouette IoU, SSIM, NCC, Delta E, MSE)", fill=(148, 163, 184), font=font_sub)

results = []

for idx, m in enumerate(mascots):
    y_top = 100 + idx * 430
    
    # 1. Render SVG
    render_svg_chrome(m["svg_path"], m["rendered_png"])
    
    # 2. Load ref and vec
    ref = np.array(Image.open(m["ref_path"]).convert("RGBA"))
    vec = np.array(Image.open(m["rendered_png"]).convert("RGBA"))
    
    ref_mask = ref[:, :, 3] > 20
    vec_mask = vec[:, :, 3] > 20
    
    inter = ref_mask & vec_mask
    union = ref_mask | vec_mask
    iou = inter.sum() / (union.sum() + 1e-6)
    
    bg = np.array(m["bg_dark"], dtype=np.float32)
    a_ref = ref[:, :, 3:4].astype(float) / 255.0
    ref_comp = np.clip(ref[:, :, :3] * a_ref + bg * (1.0 - a_ref), 0, 255).astype(np.uint8)
    
    a_vec = vec[:, :, 3:4].astype(float) / 255.0
    vec_comp = np.clip(vec[:, :, :3] * a_vec + bg * (1.0 - a_vec), 0, 255).astype(np.uint8)
    
    ref_gray = cv2.cvtColor(ref[:, :, :3], cv2.COLOR_RGB2GRAY)
    vec_gray = cv2.cvtColor(vec[:, :, :3], cv2.COLOR_RGB2GRAY)
    ssim_map = compute_ssim_numpy(ref_gray, vec_gray)
    ssim_val = np.pad(ssim_map, 5, mode='edge')[inter].mean()
    
    ref_flat = ref[:, :, :3][inter].astype(np.float32).ravel()
    vec_flat = vec[:, :, :3][inter].astype(np.float32).ravel()
    ncc = np.corrcoef(ref_flat, vec_flat)[0, 1]
    
    ref_lab = cv2.cvtColor(ref[:, :, :3], cv2.COLOR_RGB2LAB).astype(np.float32)
    vec_lab = cv2.cvtColor(vec[:, :, :3], cv2.COLOR_RGB2LAB).astype(np.float32)
    delta_e = np.sqrt(np.sum((ref_lab - vec_lab)**2, axis=2))
    mean_delta_e = delta_e[inter].mean()
    
    mse = np.mean((ref[:, :, :3][inter].astype(np.float32) - vec[:, :, :3][inter].astype(np.float32))**2)
    psnr = 10 * np.log10(255**2 / (mse + 1e-6))
    
    delta_e_vis = np.clip(delta_e * 2.5, 0, 255).astype(np.uint8)
    heatmap = cv2.applyColorMap(delta_e_vis, cv2.COLORMAP_JET)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
    heatmap[~union] = [11, 15, 23]
    
    p_w, p_h = 480, 380
    ref_panel = Image.fromarray(ref_comp).resize((p_w, p_h), Image.LANCZOS)
    vec_panel = Image.fromarray(vec_comp).resize((p_w, p_h), Image.LANCZOS)
    heat_panel = Image.fromarray(heatmap).resize((p_w, p_h), Image.LANCZOS)
    
    x_gap = (board_w - 3 * p_w) // 4
    x1 = x_gap
    x2 = x1 + p_w + x_gap
    x3 = x2 + p_w + x_gap
    
    board.paste(ref_panel, (x1, y_top + 40))
    board.paste(vec_panel, (x2, y_top + 40))
    board.paste(heat_panel, (x3, y_top + 40))
    
    # Text headers for this row
    draw.text((x1, y_top), m["name"], fill=(245, 158, 11), font=font_metric)
    
    # Status metrics
    status_text = f"SILHOUETTE IoU: {iou*100:.2f}%  |  SSIM: {ssim_val*100:.2f}%  |  NCC: {ncc*100:.2f}%  |  DELTA E: {mean_delta_e:.2f}  |  MSE: {mse:.1f}"
    status_color = (74, 222, 128) if (iou >= 0.98 and mean_delta_e <= 20.0 and ncc >= 0.85) else (248, 113, 113)
    draw.text((x2, y_top), status_text, fill=status_color, font=font_metric)
    
    # Column Labels
    draw.text((x1 + 10, y_top + 45), "1. 3D CGI GROUND TRUTH", fill=(255, 255, 255), font=font_sub)
    draw.text((x2 + 10, y_top + 45), "2. VECTOR SVG (CHROME HEADLESS)", fill=(56, 189, 248), font=font_sub)
    draw.text((x3 + 10, y_top + 45), "3. HEATMAP DELTA E", fill=(239, 68, 68), font=font_sub)
    
    results.append({
        "mascot": m["id"],
        "name": m["name"],
        "iou": float(iou),
        "ssim": float(ssim_val),
        "ncc": float(ncc),
        "delta_e": float(mean_delta_e),
        "mse": float(mse),
        "psnr": float(psnr)
    })
    print(f"[{m['id'].upper()}] IoU: {iou*100:.2f}%, SSIM: {ssim_val*100:.2f}%, NCC: {ncc*100:.2f}%, Delta E: {mean_delta_e:.2f}")

out_board = "scratch/three_mascots_studio_audit_board.png"
board.save(out_board)
print(f"Master 3-mascot audit board saved to {out_board}")

out_master_board = "mascots/three_mascots_master_audit_board.png"
board.save(out_master_board)
print(f"Master 3-mascot audit board saved to {out_master_board}")

import json
with open("scratch/three_mascots_audit_results.json", "w") as f:
    json.dump(results, f, indent=2)
