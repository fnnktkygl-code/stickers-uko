with open("scripts/build_flawless_meoweko_idle.py", "r") as f:
    content = f.read()

# Replace the manual crop coordinates in load_and_despill_reference_video with auto-bounding box
new_crop_logic = """
        ys, xs = np.where(alpha > 30)
        if len(ys) == 0:
            crop = rgba
        else:
            crop = rgba[ys.min():ys.max()+1, xs.min():xs.max()+1]
        
        TARGET_H = 450.0
        scale = TARGET_H / float(crop.shape[0])
        nw = int(round(crop.shape[1] * scale))
        nh = int(round(TARGET_H))
        scaled = cv2.resize(crop, (nw, nh), interpolation=cv2.INTER_LANCZOS4)
        
        canvas = np.zeros((512, 512, 4), dtype=np.uint8)
        px = (512 - nw) // 2
        py = 491 - nh
        canvas[py:py+nh, px:px+nw] = scaled
        canvas[492:, :, 3] = 0 # zero shadow
"""

import re
content = re.sub(
    r'# Scale & center exactly as standard.*?canvas\[492:, :, 3\] = 0 # zero shadow',
    new_crop_logic,
    content,
    flags=re.DOTALL
)

with open("scripts/build_flawless_meoweko_idle.py", "w") as f:
    f.write(content)
