import os
import subprocess
import re
import cv2

with open("scratch/test_rwing_fix.svg") as f:
    text = f.read()

def test_svg(svg_content):
    with open("scratch/test_tmp.svg", "w") as f:
        f.write(svg_content)
    cmd = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--headless",
        "--disable-gpu",
        "--screenshot=scratch/test_tmp.png",
        "--window-size=512,512",
        "--default-background-color=00000000",
        f"file://{os.path.abspath('scratch/test_tmp.svg')}"
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    im = cv2.imread("scratch/test_tmp.png", cv2.IMREAD_UNCHANGED)
    return im[465, 255]

only_body = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <linearGradient id="bodyGrad" x1="34%" y1="5%" x2="65%" y2="90%">
      <stop offset="0%" stop-color="#E8E0D8" />
      <stop offset="100%" stop-color="#726052" />
    </linearGradient>
  </defs>
  <path d="{re.search(r'<path d="([^"]+)" fill="url\(#bodyGrad\)"', text).group(1)}" fill="url(#bodyGrad)" />
</svg>"""

print("Only body path at (465, 255):", test_svg(only_body))
