import os
import subprocess
import re
import cv2

with open("scratch/test_rwing_fix.svg") as f:
    text = f.read()

# Let's find all elements inside the svg
# We know only_body gave [0,0,0,0].
# Now let's test adding elements one by one inside <svg>
defs_match = re.search(r'<defs>.*?</defs>', text, re.DOTALL)
defs = defs_match.group(0)

body_path = re.search(r'<path d="M 213 46.*?" fill="url\(#bodyGrad\)" />', text).group(0)

# What about elements inside <g clip-path="url(#bodyClip)">?
clip_group = re.search(r'<g clip-path="url\(#bodyClip\)">(.*?)</g>\s*<!-- 3\.', text, re.DOTALL).group(1)

# Split elements in clip_group
elements = re.findall(r'(<[a-z]+.*?(?:/>|</[a-z]+>))', clip_group, re.DOTALL)
print(f"Found {len(elements)} elements inside clipped group")

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

for i, el in enumerate(elements):
    test_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
    {defs}
    {body_path}
    <g clip-path="url(#bodyClip)">
      {el}
    </g>
    </svg>"""
    val = test_svg(test_content)
    if val[3] > 0:
        print(f"Element {i} colored (465, 255): {val}, snippet: {el[:60]}...")
