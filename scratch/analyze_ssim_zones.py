import cv2
import numpy as np
from PIL import Image

def analyze():
    ref_img = Image.open("mascots/owluko/owluko_master_exact_512.png").convert("RGBA")
    vec_img = Image.open("scratch/test_direct_render.png").convert("RGBA")
    
    ref = np.array(ref_img)
    vec = np.array(vec_img)
    
    ref_alpha = ref[:, :, 3]
    vec_alpha = vec[:, :, 3]
    
    ref_mask = ref_alpha > 20
    bg = np.array([11, 15, 23], dtype=np.float32)
    vec_mask = np.linalg.norm(vec[:, :, :3].astype(float) - bg, axis=2) > 15
    if vec.shape[2] == 4 and np.any(vec[:, :, 3] < 250):
        vec_mask = vec_mask & (vec_alpha > 20)
    
    inter = np.logical_and(ref_mask, vec_mask)
    
    ref_gray = cv2.cvtColor(ref[:, :, :3], cv2.COLOR_RGB2GRAY).astype(np.float64)
    vec_gray = cv2.cvtColor(vec[:, :, :3], cv2.COLOR_RGB2GRAY).astype(np.float64)
    
    C1 = (0.01 * 255)**2
    C2 = (0.03 * 255)**2
    kernel = cv2.getGaussianKernel(11, 1.5)
    window = np.outer(kernel, kernel.transpose())
    mu1 = cv2.filter2D(ref_gray, -1, window)[5:-5, 5:-5]
    mu2 = cv2.filter2D(vec_gray, -1, window)[5:-5, 5:-5]
    mu1_sq = mu1**2
    mu2_sq = mu2**2
    mu1_mu2 = mu1 * mu2
    sigma1_sq = cv2.filter2D(ref_gray**2, -1, window)[5:-5, 5:-5] - mu1_sq
    sigma2_sq = cv2.filter2D(vec_gray**2, -1, window)[5:-5, 5:-5] - mu2_sq
    sigma12 = cv2.filter2D(ref_gray * vec_gray, -1, window)[5:-5, 5:-5] - mu1_mu2
    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))
    ssim_full = np.pad(ssim_map, 5, mode='edge')
    
    # Save SSIM error map
    ssim_err = np.clip((1.0 - ssim_full) * 255, 0, 255).astype(np.uint8)
    ssim_err_colored = cv2.applyColorMap(ssim_err, cv2.COLORMAP_MAGMA)
    ssim_err_colored[~inter] = [11, 15, 23]
    cv2.imwrite("scratch/ssim_error_map.png", ssim_err_colored)
    
    zones = {
        "Left Eye (150-240, 120-200)": (slice(120, 200), slice(150, 240)),
        "Right Eye (270-355, 120-200)": (slice(120, 200), slice(270, 355)),
        "Beak (240-270, 160-230)": (slice(160, 230), slice(240, 270)),
        "Head Upper (150-360, 40-130)": (slice(40, 130), slice(150, 360)),
        "Chest & Belly (160-350, 210-440)": (slice(210, 440), slice(160, 350)),
        "Left Wing/Flank (80-180, 180-440)": (slice(180, 440), slice(80, 180)),
        "Right Wing/Flank (330-430, 180-440)": (slice(180, 440), slice(330, 430)),
        "Feet (150-360, 440-500)": (slice(440, 500), slice(150, 360)),
    }
    
    print(f"OVERALL FOREGROUND SSIM: {ssim_full[inter].mean()*100:.2f}%")
    print("-" * 50)
    for name, (ys, xs) in zones.items():
        z_inter = inter[ys, xs]
        if z_inter.sum() > 0:
            z_ssim = ssim_full[ys, xs][z_inter].mean()
            z_ref = ref[ys, xs, :3][z_inter].astype(float)
            z_vec = vec[ys, xs, :3][z_inter].astype(float)
            z_mse = np.mean((z_ref - z_vec)**2)
            z_ncc = np.corrcoef(z_ref.ravel(), z_vec.ravel())[0, 1] if len(z_ref.ravel()) > 1 else 0
            print(f"{name:35s}: SSIM={z_ssim*100:5.2f}%, MSE={z_mse:6.1f}, NCC={z_ncc*100:5.2f}%, N_pixels={z_inter.sum()}")

if __name__ == "__main__":
    analyze()
