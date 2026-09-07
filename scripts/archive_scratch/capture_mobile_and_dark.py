import subprocess
import os

ART_DIR = "/Users/richard/.gemini/antigravity/brain/5da7469d-6e59-4f3e-8894-cfaf7a0fac27/local_preview"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

shots = [
    ("mobile_full_iphone_showcase", 390, 3600, "http://localhost:3000"),
    ("desktop_dark_mode_studio", 1440, 2400, "http://localhost:3000?dark=1&mascot=inuko&pose=7"),
    ("desktop_inuko_searching", 1440, 2400, "http://localhost:3000?mascot=inuko&pose=7"),
    ("desktop_pricing_no_truncation", 1440, 1100, "http://localhost:3000?scroll=tarifs")
]

for idx, (name, w, h, url) in enumerate(shots, 1):
    out_path = f"{ART_DIR}/{name}.png"
    u_dir = f"/tmp/chrome_mob_{idx}"
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-first-run",
        "--no-default-browser-check",
        "--virtual-time-budget=2000",
        f"--user-data-dir={u_dir}",
        f"--window-size={w},{h}",
        "--hide-scrollbars",
        f"--screenshot={out_path}",
        url
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Captured {name}.png ({w}x{h})")

print("Mobile and dark captures ready!")
