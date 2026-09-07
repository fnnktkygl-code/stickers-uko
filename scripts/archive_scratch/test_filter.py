import os
import fnmatch

patterns = [
    "*.py", "*.pyc", "*.pyi", "*.so", "*.dylib", "*.mp4", "*.mat", "*.txt", "*.json", "*.log", ".DS_Store",
    "*.sh", "*.md"
]

ignore_dirs = [".venv", "downloads", "preview", "__pycache__", "master", "temp_frames", "temp_clean", ".vercel"]

upload_files = []
total_sz = 0

for root, dirs, files in os.walk("."):
    # prune ignore dirs
    dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith(".")]
    
    for f in files:
        if any(fnmatch.fnmatch(f, p) for p in patterns):
            continue
        fp = os.path.join(root, f)
        sz = os.path.getsize(fp)
        total_sz += sz
        upload_files.append((fp, sz))

print(f"Filtered files to upload: {len(upload_files)}")
print(f"Total size to upload: {total_sz / (1024*1024):.2f} MB")
for f, sz in upload_files[:15]:
    print(f" - {f} ({sz/1024:.1f} KB)")
