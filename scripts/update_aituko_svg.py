import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

from update_svg_elements import get_rig_svg

inter_svg_pattern = r'<svg id="aitukoInteractiveSvg".*?</svg>'
new_inter_svg = get_rig_svg("aitukoInteractiveSvg", "interactiveShadow", "interactivePods", "interactiveTorso", "interactiveHeadGroup", "interactiveEyesGroup", "interactiveLeftHand", "interactiveRightHand")

match_inter = re.search(inter_svg_pattern, content, re.DOTALL)
if match_inter:
    content = content[:match_inter.start()] + new_inter_svg + content[match_inter.end():]
    print("✅ aitukoInteractiveSvg updated in index.html")
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
else:
    print("⚠️ aitukoInteractiveSvg pattern not found")
