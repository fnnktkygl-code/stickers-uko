import os
import pathspec

with open(".vercelignore", "r") as f:
    ignore_lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

# Add explicit rules
ignore_patterns = [
    ".venv", ".venv/**", "**/.venv/**",
    "downloads", "downloads/**", "**/downloads/**",
    "preview", "preview/**",
    "__pycache__", "**/__pycache__/**",
    "*.py", "**/*.py",
    "*.pyc", "**/*.pyc",
    "*.pyi", "**/*.pyi",
    "*.so", "**/*.so",
    "*.dylib", "**/*.dylib",
    "*.mp4", "**/*.mp4",
    "*.mat", "**/*.mat",
    "*.txt", "**/*.txt",
    "*.json", "**/*.json",
    "*.log", "**/*.log",
    "*.DS_Store", "**/.DS_Store",
    "**/master/**", "master/**",
    "temp_frames/**", "**/temp_frames/**",
    "temp_clean/**", "**/temp_clean/**"
]

spec = pathspec.PathSpec.from_lines("gitwildmatch", ignore_patterns)

matched_files = []
ignored_files = []

total_upload_size = 0

for root, dirs, files in os.walk("."):
    for f in files:
        rel_path = os.path.relpath(os.path.join(root, f), ".")
        if spec.match_file(rel_path):
            ignored_files.append(rel_path)
        else:
            sz = os.path.getsize(rel_path)
            total_upload_size += sz
            matched_files.append((rel_path, sz))

print(f"Total files in directory: {len(matched_files) + len(ignored_files)}")
print(f"Ignored files: {len(ignored_files)}")
print(f"Files to upload to Vercel: {len(matched_files)}")
print(f"Total upload size: {total_upload_size / (1024*1024):.2f} MB")
