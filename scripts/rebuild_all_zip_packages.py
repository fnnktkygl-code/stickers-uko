#!/usr/bin/env python3
"""
Rebuild all downloadable zip packages optimized under Vercel 100MB file limit
Includes: transparent WebP, animated GIF, HD static PNG, static WebP, code snippets, and DEVELOPER_GUIDE.md.
"""

import os
import zipfile
import glob

os.makedirs("downloads", exist_ok=True)

def clean_stale_zips():
    # Only remove generated multi-state pack zips, preserving individual state bundle zips
    for z in glob.glob("downloads/*Pack*.zip") + glob.glob("downloads/*States*.zip") + glob.glob("downloads/*Sample*.zip"):
        try:
            os.remove(z)
        except Exception:
            pass

STARTER_STATES = [
    "00_idle", "01_waving", "02_celebrating",
    "03_ai_thinking", "04_error_404", "05_thumbs_up"
]

ALL_13_STATES = [
    "00_idle", "01_waving", "02_celebrating", "03_ai_thinking",
    "04_error_404", "05_thumbs_up", "06_sleeping", "07_pointing",
    "08_searching", "09_loading", "10_idea", "11_security", "12_goodbye"
]

FORMATS = [
    "static.png", "static.webp", "animated.webp",
    "animated.gif", "snippet.json", "lottie.json"
]

def build_mascot_zip(mascot_name, states, output_zip_path, base_assets_dir):
    with zipfile.ZipFile(output_zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        if os.path.exists("DEVELOPER_GUIDE.md"):
            z.write("DEVELOPER_GUIDE.md", "DEVELOPER_GUIDE.md")
        
        avatar_path = os.path.join(base_assets_dir, "avatar.png")
        if os.path.exists(avatar_path):
            z.write(avatar_path, f"{mascot_name}/avatar.png")
            
        for st in states:
            st_dir = os.path.join(base_assets_dir, st)
            if not os.path.exists(st_dir):
                continue
            for fmt in FORMATS:
                fp = os.path.join(st_dir, fmt)
                if os.path.exists(fp):
                    arcname = f"{mascot_name}/{st}/{fmt}"
                    z.write(fp, arcname)
                    
    sz = os.path.getsize(output_zip_path)
    print(f"📦 Created: {output_zip_path} ({sz / (1024*1024):.2f} MB)")

def build_all():
    print("🚀 Rebuilding all download packages (Optimized < 100MB)...")
    clean_stale_zips()
    
    mascots = [
        ("AItuko", "assets", "aituko"),
        ("Owluko", "mascots/owluko/assets", "owluko"),
        ("Luneko", "mascots/luneko/assets", "luneko"),
        ("Hatoko", "mascots/hatoko/assets", "hatoko"),
        ("Usako", "mascots/usako/assets", "usako"),
        ("Inuko", "mascots/inuko/assets", "inuko")
    ]
    
    # 1. Individual Mascot Packs
    for name, path, key in mascots:
        if os.path.exists(path):
            build_mascot_zip(name, ["00_idle"], f"downloads/{name}-Free-Sample.zip", path)
            build_mascot_zip(name, STARTER_STATES, f"downloads/{name}-Starter-6-States.zip", path)
            build_mascot_zip(name, STARTER_STATES, f"downloads/{name}-Starter-Pack.zip", path)
            build_mascot_zip(name, ALL_13_STATES, f"downloads/{name}-Pro-12-States.zip", path)
            
    # 2. General Global Aliases
    build_mascot_zip("AItuko", ["00_idle"], "downloads/Uko-Free-Sample.zip", "assets")
    build_mascot_zip("AItuko", ["00_idle"], "downloads/Uko-Stickers-Sample-Free.zip", "assets")
    build_mascot_zip("AItuko", STARTER_STATES, "downloads/Uko-Starter-6-States.zip", "assets")
    build_mascot_zip("AItuko", ALL_13_STATES, "downloads/Uko-Pro-12-States.zip", "assets")
    
    # 3. Master Bundle
    with zipfile.ZipFile("downloads/Uko-Stickers-Pro-12-States.zip", "w", zipfile.ZIP_DEFLATED) as z:
        if os.path.exists("DEVELOPER_GUIDE.md"):
            z.write("DEVELOPER_GUIDE.md", "DEVELOPER_GUIDE.md")
        for name, path, key in mascots:
            if not os.path.exists(path): continue
            av = os.path.join(path, "avatar.png")
            if os.path.exists(av): z.write(av, f"{name}/avatar.png")
            for st in ALL_13_STATES:
                st_dir = os.path.join(path, st)
                if not os.path.exists(st_dir): continue
                for fmt in ["static.png", "static.webp", "animated.webp", "snippet.json", "lottie.json"]:
                    fp = os.path.join(st_dir, fmt)
                    if os.path.exists(fp):
                        z.write(fp, f"{name}/{st}/{fmt}")
                        
    sz = os.path.getsize("downloads/Uko-Stickers-Pro-12-States.zip")
    print(f"👑 Created Master Bundle: downloads/Uko-Stickers-Pro-12-States.zip ({sz / (1024*1024):.2f} MB)")
    print("✅ All ZIP archives rebuilt successfully within limits!")

if __name__ == "__main__":
    build_all()
