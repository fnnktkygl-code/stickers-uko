import os
import shutil
import glob

dist = "dist_vercel"
if os.path.exists(dist):
    shutil.rmtree(dist)
os.makedirs(dist, exist_ok=True)

# Copy index.html
shutil.copy2("index.html", f"{dist}/index.html")

# Copy .vercel settings
os.makedirs(f"{dist}/.vercel", exist_ok=True)
shutil.copy2(".vercel/project.json", f"{dist}/.vercel/project.json")

# Copy web assets (WebP, GIF, PNG static)
for src_base, dst_base in [("assets", f"{dist}/assets"), ("mascots", f"{dist}/mascots")]:
    os.makedirs(dst_base, exist_ok=True)
    for root, dirs, files in os.walk(src_base):
        # Skip raw, temp, master
        if any(skip in root for skip in ["temp_frames", "temp_clean", "master", "downloads", "preview"]):
            continue
        rel_path = os.path.relpath(root, src_base)
        target_dir = os.path.join(dst_base, rel_path) if rel_path != "." else dst_base
        
        for f in files:
            # We deploy static.png, static.webp, animated.webp, animated.gif
            # We omit the 20MB animated.png to keep upload ultra-light and avoid Vercel limits
            if f in ["static.png", "static.webp", "animated.webp", "animated.gif"]:
                os.makedirs(target_dir, exist_ok=True)
                shutil.copy2(os.path.join(root, f), os.path.join(target_dir, f))

total_files = sum(len(files) for _, _, files in os.walk(dist))
total_size_mb = sum(os.path.getsize(os.path.join(root, f)) for root, _, files in os.walk(dist) for f in files) / (1024*1024)
print(f"🚀 Optimized dist_vercel for fast deployment: {total_files} files, {total_size_mb:.1f} MB")
