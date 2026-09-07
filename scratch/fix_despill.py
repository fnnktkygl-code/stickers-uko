import re

with open("scripts/build_flawless_meoweko_idle.py", "r") as f:
    content = f.read()

new_despill = """
        bgr_clean = frame.copy()
        b_c, g_c, r_c = bgr_clean[:,:,0].astype(np.float32), bgr_clean[:,:,1].astype(np.float32), bgr_clean[:,:,2].astype(np.float32)
        spill = (alpha > 0) & (g_c > np.maximum(r_c, b_c))
        g_c[spill] = np.maximum(r_c[spill], b_c[spill])
        bgr_clean[:,:,0] = b_c.astype(np.uint8)
        bgr_clean[:,:,1] = g_c.astype(np.uint8)
        bgr_clean[:,:,2] = r_c.astype(np.uint8)
        rgba = cv2.cvtColor(bgr_clean, cv2.COLOR_BGR2RGBA)
"""

content = content.replace("bgr_clean = frame.copy()\n        rgba = cv2.cvtColor(bgr_clean, cv2.COLOR_BGR2RGBA)", new_despill)

with open("scripts/build_flawless_meoweko_idle.py", "w") as f:
    f.write(content)
