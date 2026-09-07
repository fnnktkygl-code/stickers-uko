import os
import time
import subprocess

ART_DIR = "/Users/richard/.gemini/antigravity/brain/5da7469d-6e59-4f3e-8894-cfaf7a0fac27/local_preview"
os.makedirs(ART_DIR, exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

shots = [
    # 1. Desktop AItuko
    ("01_desktop_hero_studio_aituko", 1440, 950, "http://localhost:3000"),
    
    # 2. Desktop Inuko Searching (3D orange loupe)
    ("02_desktop_studio_inuko_searching", 1440, 950, "http://localhost:3000?mascot=inuko&pose=7&scroll=studio"),
    
    # 3. Desktop Inuko Sleeping (Anatomical 4 legs)
    ("03_desktop_studio_inuko_sleeping", 1440, 950, "http://localhost:3000?mascot=inuko&pose=5&scroll=studio"),
    
    # 4. Desktop Owluko Searching (3D orange loupe)
    ("04_desktop_studio_owluko_searching", 1440, 950, "http://localhost:3000?mascot=owluko&pose=7&scroll=studio"),
    
    # 5. Desktop Luneko Searching (3D orange loupe)
    ("05_desktop_studio_luneko_searching", 1440, 950, "http://localhost:3000?mascot=luneko&pose=7&scroll=studio"),
    
    # 6. Desktop Usako Idea (3D Lightbulb)
    ("06_desktop_studio_usako_idea", 1440, 950, "http://localhost:3000?mascot=usako&pose=9&scroll=studio"),
    
    # 7. Desktop Catalog & Voting Section
    ("07_desktop_catalog_section", 1440, 950, "http://localhost:3000?scroll=catalogue"),
    
    # 8. Desktop Pricing Cards Section (No text truncation)
    ("08_desktop_pricing_section", 1440, 950, "http://localhost:3000?scroll=tarifs"),
    
    # 9. Desktop Dark Mode Studio with Inuko Security Shield
    ("09_desktop_dark_mode_security", 1440, 950, "http://localhost:3000?mascot=inuko&pose=10&dark=1&scroll=studio"),
    
    # 10. Mobile iPhone View: Hero & Switcher
    ("10_mobile_hero_switcher", 390, 844, "http://localhost:3000"),
    
    # 11. Mobile iPhone View: Inuko Studio Stage & Pills
    ("11_mobile_inuko_searching_stage", 390, 844, "http://localhost:3000?mascot=inuko&pose=7&scroll=studioBox"),
    
    # 12. Mobile iPhone View: Pricing Cards
    ("12_mobile_pricing_cards", 390, 844, "http://localhost:3000?scroll=tarifs")
]

for idx, (name, w, h, url) in enumerate(shots, 1):
    out_file = f"{ART_DIR}/{name}.png"
    tmp_user_dir = f"/tmp/chrome_shot_dir_{idx}"
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        f"--user-data-dir={tmp_user_dir}",
        f"--window-size={w},{h}",
        "--hide-scrollbars",
        f"--screenshot={out_file}",
        url
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[{idx}/{len(shots)}] ✅ {name}.png captured ({w}x{h})")
    except Exception as e:
        print(f"[{idx}/{len(shots)}] ❌ {name}: {e}")

print("\n🎉 ALL 12 SHOWCASE SCREENSHOTS GENERATED!")
