import subprocess
import os

ART_DIR = "/Users/richard/.gemini/antigravity/brain/5da7469d-6e59-4f3e-8894-cfaf7a0fac27/local_preview"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

shots = [
    ("01_desktop_hero_aituko", 1440, 950, "http://localhost:3000"),
    ("02_desktop_inuko_searching", 1440, 950, "http://localhost:3000?mascot=inuko&pose=7&scroll=studio"),
    ("03_desktop_inuko_sleeping", 1440, 950, "http://localhost:3000?mascot=inuko&pose=5&scroll=studio"),
    ("04_desktop_owluko_searching", 1440, 950, "http://localhost:3000?mascot=owluko&pose=7&scroll=studio"),
    ("05_desktop_luneko_searching", 1440, 950, "http://localhost:3000?mascot=luneko&pose=7&scroll=studio"),
    ("06_desktop_usako_idea", 1440, 950, "http://localhost:3000?mascot=usako&pose=9&scroll=studio"),
    ("07_desktop_catalog", 1440, 950, "http://localhost:3000?scroll=catalogue"),
    ("08_desktop_pricing", 1440, 950, "http://localhost:3000?scroll=tarifs"),
    ("09_desktop_dark_inuko", 1440, 950, "http://localhost:3000?mascot=inuko&pose=10&dark=1&scroll=studio"),
    ("10_mobile_hero", 390, 844, "http://localhost:3000"),
    ("11_mobile_inuko_studio", 390, 844, "http://localhost:3000?mascot=inuko&pose=7&scroll=studioBox"),
    ("12_mobile_pricing", 390, 844, "http://localhost:3000?scroll=tarifs")
]

for idx, (name, w, h, url) in enumerate(shots, 1):
    out_path = f"{ART_DIR}/{name}.png"
    u_dir = f"/tmp/fast_chrome_{idx}"
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-background-networking",
        "--disable-component-update",
        "--disable-sync",
        f"--user-data-dir={u_dir}",
        f"--window-size={w},{h}",
        "--hide-scrollbars",
        f"--screenshot={out_path}",
        url
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Captured [{idx}/{len(shots)}] {name}.png")

print("All screenshots captured!")
