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

# Copy only production asset files from assets/
os.makedirs(f"{dist}/assets", exist_ok=True)
for s in glob.glob("assets/*"):
    if os.path.isdir(s) and not s.endswith(("temp_frames", "temp_clean", "master")):
        s_name = os.path.basename(s)
        target_s = f"{dist}/assets/{s_name}"
        os.makedirs(target_s, exist_ok=True)
        for ext in ["static.png", "static.webp", "animated.png", "animated.webp", "animated.gif"]:
            src_f = f"{s}/{ext}"
            if os.path.exists(src_f):
                shutil.copy2(src_f, f"{target_s}/{ext}")

# Copy only production asset files from mascots/
os.makedirs(f"{dist}/mascots", exist_ok=True)
for m in glob.glob("mascots/*"):
    if os.path.isdir(m):
        m_name = os.path.basename(m)
        for s in glob.glob(f"{m}/assets/*"):
            if os.path.isdir(s):
                s_name = os.path.basename(s)
                target_s = f"{dist}/mascots/{m_name}/assets/{s_name}"
                os.makedirs(target_s, exist_ok=True)
                for ext in ["static.png", "static.webp", "animated.png", "animated.webp", "animated.gif"]:
                    src_f = f"{s}/{ext}"
                    if os.path.exists(src_f):
                        shutil.copy2(src_f, f"{target_s}/{ext}")

# Count total files in dist_vercel
total_files = sum(len(files) for _, _, files in os.walk(dist))
total_size_mb = sum(os.path.getsize(os.path.join(root, f)) for root, _, files in os.walk(dist) for f in files) / (1024*1024)
print(f"📦 Prepared clean dist_vercel: {total_files} files, {total_size_mb:.1f} MB")
