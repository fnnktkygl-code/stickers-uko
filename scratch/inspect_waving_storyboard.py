from PIL import Image
import os

im = Image.open('mascots/owluko/owluko_waving_storyboard_ref.png')
w, h = im.size
# 2 rows x 3 columns
cw = w // 3
ch = h // 2

os.makedirs('scratch/waving_panels', exist_ok=True)

panels = []
idx = 0
for r in range(2):
    for c in range(3):
        x0 = c * cw
        y0 = r * ch
        x1 = x0 + cw
        y1 = y0 + ch
        panel = im.crop((x0, y0, x1, y1))
        out_path = f'scratch/waving_panels/panel_{idx+1}.png'
        panel.save(out_path)
        panels.append(out_path)
        print(f"Panel {idx+1}: bounds=({x0},{y0}) to ({x1},{y1}) -> {out_path}")
        idx += 1
