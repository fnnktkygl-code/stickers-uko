#!/usr/bin/env python3
import os
import subprocess
import cv2
import numpy as np
from PIL import Image

# 1. Load image and perform meanshift + kmeans (24 colors)
img = cv2.imread("mascots/meoweko/meoweko_master_exact_512.png", cv2.IMREAD_UNCHANGED)
b, g, r, a = cv2.split(img)
bgr = cv2.merge([b, g, r])

mask = a > 30

# Meanshift filter for smooth color regions
shifted = cv2.pyrMeanShiftFiltering(bgr, sp=15, sr=30, maxLevel=2)

# K-means 24 colors
pixels = shifted[mask].astype(np.float32)
K = 24
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 25, 1.0)
_, labels, centers = cv2.kmeans(pixels, K, None, criteria, 10, cv2.KMEANS_PP_CENTERS)
centers = np.uint8(centers)

quantized = np.zeros_like(shifted)
quantized[mask] = centers[labels.flatten()]

# Order colors from background to foreground (dark/ginger to light/white, and eyes on top)
# Compute luminance or sort by area
color_counts = []
for i, c in enumerate(centers):
    c_mask = mask & (quantized[:,:,0] == c[0]) & (quantized[:,:,1] == c[1]) & (quantized[:,:,2] == c[2])
    color_counts.append((i, np.sum(c_mask), c))

# Sort by area descending so large base shapes are drawn first, fine details drawn on top!
color_counts.sort(key=lambda x: x[1], reverse=True)

# Generate SVG paths for each color
svg_paths = []
lottie_shapes = []

def contour_to_svg_path(pts):
    if len(pts) < 3:
        return ""
    # Use smooth cubic bezier
    n = len(pts)
    c_factor = 1.0 / 6.0
    d = [f"M {pts[0][0]:.1f} {pts[0][1]:.1f}"]
    for i in range(n):
        p_prev = pts[(i - 1) % n]
        p_curr = pts[i]
        p_next = pts[(i + 1) % n]
        p_next2 = pts[(i + 2) % n]
        c1_x = p_curr[0] + (p_next[0] - p_prev[0]) * c_factor
        c1_y = p_curr[1] + (p_next[1] - p_prev[1]) * c_factor
        c2_x = p_next[0] - (p_next2[0] - p_curr[0]) * c_factor
        c2_y = p_next[1] - (p_next2[1] - p_curr[1]) * c_factor
        d.append(f"C {c1_x:.1f} {c1_y:.1f}, {c2_x:.1f} {c2_y:.1f}, {p_next[0]:.1f} {p_next[1]:.1f}")
    d.append("Z")
    return " ".join(d)

for idx, count, c in color_counts:
    if count < 15:
        continue
    c_mask = mask & (quantized[:,:,0] == c[0]) & (quantized[:,:,1] == c[1]) & (quantized[:,:,2] == c[2])
    c_mask_u8 = c_mask.astype(np.uint8) * 255
    # Smooth slightly
    c_mask_u8 = cv2.morphologyEx(c_mask_u8, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    
    cnts, hier = cv2.findContours(c_mask_u8, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)
    hex_color = f"#{c[2]:02x}{c[1]:02x}{c[0]:02x}"
    
    path_d_list = []
    for cnt in cnts:
        area = cv2.contourArea(cnt)
        if area < 8:
            continue
        approx = cv2.approxPolyDP(cnt, 0.6, True)
        pts = approx.reshape(-1, 2)
        if len(pts) >= 3:
            path_d_list.append(contour_to_svg_path(pts))
            
    if path_d_list:
        combined_d = " ".join(path_d_list)
        svg_paths.append(f'<path d="{combined_d}" fill="{hex_color}" />')

# Build complete SVG
svg_str = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <rect width="512" height="512" fill="#0B0F17" />
  <g id="meoweko_vector_group">
    {' '.join(svg_paths)}
  </g>
</svg>"""

out_svg = "scratch/meoweko_vector_kmeans.svg"
with open(out_svg, "w") as f:
    f.write(svg_str)
print(f"✅ Saved vector SVG to {out_svg} (Size: {len(svg_str)/1024:.1f} KB)")

# Render with Chrome headless
preview_png = "scratch/meoweko_vector_kmeans_preview.png"
cmd = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "--headless",
    "--disable-gpu",
    f"--screenshot={preview_png}",
    "--window-size=512,512",
    "--default-background-color=00000000",
    f"file://{os.path.abspath(out_svg)}"
]
subprocess.run(cmd, check=True)
print(f"✅ Rendered PNG screenshot: {preview_png}")

# Create side-by-side comparison
ref = Image.open("mascots/meoweko/meoweko_master_exact_512.png").convert("RGBA")
vec = Image.open(preview_png).convert("RGBA")
comp = Image.new("RGBA", (1024, 512), (11, 15, 23, 255))
comp.paste(ref, (0, 0), ref.split()[3])
comp.paste(vec, (512, 0), vec.split()[3])
comp_path = "scratch/meoweko_vector_vs_3d_comparison.png"
comp.save(comp_path, "PNG")
print(f"✅ Saved side-by-side comparison to {comp_path}")
