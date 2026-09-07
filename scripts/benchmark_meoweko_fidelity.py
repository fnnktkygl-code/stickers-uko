import os, sys, subprocess
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

def benchmark_svg(svg_path, out_board_path="scratch/meoweko_fidelity_audit_board.png"):
    # 1. Render SVG using Chrome headless
    rendered_png = "scratch/temp_svg_rendered.png"
    cmd = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--headless",
        "--disable-gpu",
        f"--screenshot={rendered_png}",
        "--window-size=512,512",
        "--default-background-color=00000000",
        f"file://{os.path.abspath(svg_path)}"
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 2. Load images
    ref_img = Image.open("mascots/meoweko/meoweko_master_exact_512.png").convert("RGBA")
    vec_img = Image.open(rendered_png).convert("RGBA")
    
    ref = np.array(ref_img)
    vec = np.array(vec_img)
    
    ref_alpha = ref[:, :, 3]
    vec_alpha = vec[:, :, 3]
    
    ref_mask = ref_alpha > 20
    bg = np.array([11, 15, 23], dtype=np.float32)
    vec_mask = np.linalg.norm(vec[:, :, :3].astype(float) - bg, axis=2) > 15
    if vec.shape[2] == 4 and np.any(vec[:, :, 3] < 250):
        vec_mask = vec_mask & (vec_alpha > 20)
    
    # Silhouette IoU
    inter = np.logical_and(ref_mask, vec_mask)
    union = np.logical_or(ref_mask, vec_mask)
    iou = inter.sum() / (union.sum() + 1e-6)
    
    # Grayscale SSIM on foreground
    ref_gray = cv2.cvtColor(ref[:, :, :3], cv2.COLOR_RGB2GRAY)
    vec_gray = cv2.cvtColor(vec[:, :, :3], cv2.COLOR_RGB2GRAY)
    ssim_map = compute_ssim_numpy(ref_gray, vec_gray)
    ssim_full = np.pad(ssim_map, 5, mode='edge')
    fg_ssim = ssim_full[inter].mean()
    
    # Color Delta E (CIELAB)
    ref_lab = cv2.cvtColor(ref[:, :, :3], cv2.COLOR_RGB2LAB).astype(np.float32)
    vec_lab = cv2.cvtColor(vec[:, :, :3], cv2.COLOR_RGB2LAB).astype(np.float32)
    delta_e = np.sqrt(np.sum((ref_lab - vec_lab)**2, axis=2))
    fg_delta_e = delta_e[inter].mean()
    
    # Normalized Cross Correlation
    ref_flat = ref[:, :, :3][inter].astype(np.float32).ravel()
    vec_flat = vec[:, :, :3][inter].astype(np.float32).ravel()
    ncc = np.corrcoef(ref_flat, vec_flat)[0, 1]
    
    # MSE & PSNR
    mse = np.mean((ref[:, :, :3][inter].astype(np.float32) - vec[:, :, :3][inter].astype(np.float32))**2)
    psnr = 10 * np.log10(255**2 / (mse + 1e-6))
    
    print(f"--- BENCHMARK RESULTS ---")
    print(f"Silhouette IoU: {iou * 100:.2f}%")
    print(f"Foreground SSIM: {fg_ssim * 100:.2f}%")
    print(f"Foreground NCC: {ncc * 100:.2f}%")
    print(f"Foreground Delta E: {fg_delta_e:.2f}")
    print(f"Foreground MSE: {mse:.2f}, PSNR: {psnr:.2f} dB")
    
    # 3. Create Heatmap
    # Normalize delta E to 0..100 -> Colormap TURBO / JET
    delta_e_vis = np.clip(delta_e * 2.5, 0, 255).astype(np.uint8)
    heatmap = cv2.applyColorMap(delta_e_vis, cv2.COLORMAP_JET)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
    # Mask background
    heatmap[~union] = [11, 15, 23]
    
    # 4. Composite 3-panel comparison board
    board_w = 512 * 3 + 40
    board_h = 512 + 160
    board = Image.new("RGBA", (board_w, board_h), (11, 15, 23, 255))
    
    # Composite images on dark background
    bg = np.array([11, 15, 23], dtype=np.float32)
    def comp_dark(img_rgba):
        rgb = img_rgba[:, :, :3].astype(np.float32)
        a = (img_rgba[:, :, 3:4].astype(np.float32)) / 255.0
        return Image.fromarray(np.clip(rgb * a + bg * (1.0 - a), 0, 255).astype(np.uint8))
        
    ref_panel = comp_dark(ref)
    vec_panel = comp_dark(vec)
    heat_panel = Image.fromarray(heatmap)
    
    board.paste(ref_panel, (10, 140))
    board.paste(vec_panel, (512 + 20, 140))
    board.paste(heat_panel, (512 * 2 + 30, 140))
    
    # Draw HUD text
    draw = ImageDraw.Draw(board)
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        font_metric = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
    except:
        font_title = font_metric = font_sub = ImageFont.load_default()
        
    draw.text((20, 20), "AUDIT DE FIDÉLITÉ OBJECTIVE : MEOWEKO MASTER SVG VS RÉFÉRENCE 3D", fill=(255, 255, 255), font=font_title)
    
    hud_text = f"SILHOUETTE IoU: {iou*100:.1f}%  |  SSIM STRUCTURE: {fg_ssim*100:.1f}%  |  CORRELATION COULEUR (NCC): {ncc*100:.1f}%  |  DELTA E MOYEN: {fg_delta_e:.1f}"
    status_color = (74, 222, 128) if (iou > 0.95 and fg_ssim > 0.90) else (248, 113, 113)
    draw.text((20, 60), hud_text, fill=status_color, font=font_metric)
    
    draw.text((20, 95), "Mesure mathématique brute sans concession (AUCUNE extrapolation ni arrondi commercial)", fill=(156, 163, 175), font=font_sub)
    
    # Panel titles
    draw.text((10, 115), "1. RÉFÉRENCE 3D STUDIO (GROUND TRUTH)", fill=(245, 158, 11), font=font_metric)
    draw.text((512 + 20, 115), "2. MODÈLE VECTORIEL SVG", fill=(56, 189, 248), font=font_metric)
    draw.text((512 * 2 + 30, 115), "3. HEATMAP D'ÉCART (DELTA E / ERREUR)", fill=(239, 68, 68), font=font_metric)
    
    board.save(out_board_path)
    print(f"✅ Saved audit comparison board to {out_board_path}")
    return {
        "iou": iou,
        "ssim": fg_ssim,
        "ncc": ncc,
        "delta_e": fg_delta_e,
        "mse": mse,
        "psnr": psnr
    }

if __name__ == "__main__":
    svg_target = sys.argv[1] if len(sys.argv) > 1 else "scratch/meoweko_perfect_vector.svg"
    benchmark_svg(svg_target)
