import os, sys, subprocess, re, cv2, numpy as np
from PIL import Image

ref = np.array(Image.open('mascots/owluko/owluko_master_exact_512.png').convert('RGBA'))
ref_lab = cv2.cvtColor(ref[:,:,:3], cv2.COLOR_RGB2LAB).astype(np.float32)

face_mask = np.zeros((512,512), dtype=bool)
face_mask[100:220, 150:360] = True
le_mask = np.zeros((512,512), dtype=bool)
le_mask[135:185, 165:228] = True
re_mask = np.zeros((512,512), dtype=bool)
re_mask[135:185, 275:345] = True
beak_mask = np.zeros((512,512), dtype=bool)
beak_mask[145:212, 235:275] = True
fh_mask = np.zeros((512,512), dtype=bool)
fh_mask[95:135, 180:330] = True
ref_mask = ref[:,:,3] > 20

def test_svg_content(svg_content):
    tmp_svg = 'scratch/eval_tmp.svg'
    tmp_png = 'scratch/eval_tmp.png'
    with open(tmp_svg, 'w') as f:
        f.write(svg_content)
    cmd = [
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        '--headless',
        '--disable-gpu',
        '--run-all-compositor-stages-before-draw',
        f'--screenshot={os.path.abspath(tmp_png)}',
        '--window-size=512,512',
        '--default-background-color=00000000',
        f'file://{os.path.abspath(tmp_svg)}'
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    vec = np.array(Image.open(tmp_png).convert('RGBA'))
    vec_lab = cv2.cvtColor(vec[:,:,:3], cv2.COLOR_RGB2LAB).astype(np.float32)
    de = np.sqrt(np.sum((ref_lab - vec_lab)**2, axis=2))
    
    inter = ref_mask & (vec[:,:,3] > 20)
    return {
        'face_de': float(de[face_mask].mean()),
        'le_de': float(de[le_mask].mean()),
        're_de': float(de[re_mask].mean()),
        'beak_de': float(de[beak_mask].mean()),
        'fh_de': float(de[fh_mask].mean()),
        'global_de': float(de[inter].mean())
    }

# Read original
with open('mascots/owluko/owluko_master_exact_512.svg', 'r') as f:
    base_svg = f.read()

res_base = test_svg_content(base_svg)
print("Base:", res_base)

