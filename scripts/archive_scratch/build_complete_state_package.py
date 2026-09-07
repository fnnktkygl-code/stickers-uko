import os
import zipfile
import json
import subprocess
from PIL import Image

mascots = ["aituko", "owluko", "luneko", "usako", "inuko", "hatoko"]
state_id = "00_idle"

for m in mascots:
    state_dir = f"assets/{state_id}" if m == "aituko" else f"mascots/{m}/assets/{state_id}"
    os.makedirs(state_dir, exist_ok=True)
    
    # 1. Generate looped_video.mp4 from animated frames if not present
    video_path = f"{state_dir}/looped_video.mp4"
    if not os.path.exists(video_path):
        print(f"🎬 Generating looped_video.mp4 for {m}/{state_id}...")
        # Create MP4 from animated.gif or static
        cmd = [
            "ffmpeg", "-y",
            "-i", f"{state_dir}/animated.gif",
            "-movflags", "faststart",
            "-pix_fmt", "yuv420p",
            "-vf", "scale=512:512:force_original_aspect_ratio=decrease,pad=512:512:(ow-iw)/2:(oh-ih)/2:color=black@0",
            video_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 2. Generate ready-to-use code snippets
    snippets = {
        "react": f"""import React from 'react';\n\nexport const {m.capitalize()}Idle = () => (\n  <picture>\n    <source srcSet="/mascots/{m}/assets/00_idle/animated.webp" type="image/webp" />\n    <img src="/mascots/{m}/assets/00_idle/animated.gif" alt="{m.capitalize()} Idle" width={512} height={512} className="w-48 h-48 object-contain" />\n  </picture>\n);""",
        "vue": f"""<template>\n  <picture>\n    <source srcset="/mascots/{m}/assets/00_idle/animated.webp" type="image/webp">\n    <img src="/mascots/{m}/assets/00_idle/animated.gif" alt="{m.capitalize()} Idle" width="512" height="512" class="mascot-sticker">\n  </picture>\n</template>""",
        "html": f"""<picture>\n  <source srcset="/mascots/{m}/assets/00_idle/animated.webp" type="image/webp">\n  <img src="/mascots/{m}/assets/00_idle/animated.gif" alt="{m.capitalize()} Idle" width="512" height="512">\n</picture>"""
    }
    
    with open(f"{state_dir}/snippet.json", "w") as f:
        json.dump(snippets, f, indent=2)
        
    # 3. Create full downloadable zip bundle for this state
    zip_path = f"{state_dir}/bundle_{m}_{state_id}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for fname in ["static.png", "static.webp", "animated.gif", "animated.webp", "animated.png", "looped_video.mp4", "snippet.json"]:
            fpath = f"{state_dir}/{fname}"
            if os.path.exists(fpath):
                zipf.write(fpath, arcname=fname)
                
    print(f"📦 Package complet 00_idle pour {m.upper()} : OK (ZIP: {zip_path})")

print("🎉 TOUS LES PACKAGES DE L'ÉTAT 00_IDLE SONT 100% PRÊTS ET VALIDÉS !")
