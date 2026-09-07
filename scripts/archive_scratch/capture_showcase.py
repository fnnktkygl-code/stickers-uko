import os
import time
import subprocess

ART_DIR = "/Users/richard/.gemini/antigravity/brain/5da7469d-6e59-4f3e-8894-cfaf7a0fac27"
SHOTS_DIR = f"{ART_DIR}/local_preview"
os.makedirs(SHOTS_DIR, exist_ok=True)

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# 1. Desktop full Hero + Studio
subprocess.run([
    CHROME,
    "--headless",
    "--disable-gpu",
    "--window-size=1440,1100",
    "--hide-scrollbars",
    f"--screenshot={SHOTS_DIR}/desktop_studio_aituko.png",
    "http://localhost:3000"
], check=True)

print("Captured desktop_studio_aituko.png")

# 2. Mobile iPhone View (390x844)
subprocess.run([
    CHROME,
    "--headless",
    "--disable-gpu",
    "--window-size=390,844",
    "--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
    "--hide-scrollbars",
    f"--screenshot={SHOTS_DIR}/mobile_hero.png",
    "http://localhost:3000"
], check=True)

print("Captured mobile_hero.png")

