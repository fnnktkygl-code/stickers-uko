import os, subprocess, cv2, numpy as np
from PIL import Image
from scripts.benchmark_owluko_fidelity import compute_ssim_numpy

def render_svg_chrome(svg_str, out_png):
    temp_svg = 'scratch/temp_owluko_eye.svg'
    with open(temp_svg, 'w') as f:
        f.write(svg_str)
    wrapper_html = f'''<!DOCTYPE html>
<html>
<head><style>body {{ margin: 0; padding: 0; background: transparent; overflow: hidden; }}</style></head>
<body><div style="width: 512px; height: 512px;">{svg_str}</div></body>
</html>'''
    temp_html = 'scratch/temp_owluko_eye.html'
    with open(temp_html, 'w') as f:
        f.write(wrapper_html)
    cmd = [
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        '--headless', '--disable-gpu',
        f'--screenshot={out_png}',
        '--window-size=512,512',
        '--default-background-color=00000000',
        temp_html
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

ref = np.array(Image.open('mascots/owluko/owluko_master_exact_512.png').convert('RGBA'))
ref_mask = ref[:, :, 3] > 20
ref_gray = cv2.cvtColor(ref[:, :, :3], cv2.COLOR_RGB2GRAY)
ref_lab = cv2.cvtColor(ref[:, :, :3], cv2.COLOR_RGB2LAB).astype(np.float32)

def evaluate(png_path):
    vec = np.array(Image.open(png_path).convert('RGBA'))
    vec_mask = vec[:, :, 3] > 20
    inter = ref_mask & vec_mask
    union = ref_mask | vec_mask
    iou = inter.sum() / float(union.sum())
    
    vec_gray = cv2.cvtColor(vec[:, :, :3], cv2.COLOR_RGB2GRAY)
    ssim_map = compute_ssim_numpy(ref_gray, vec_gray)
    ssim_val = ssim_map.mean()
    
    vec_lab = cv2.cvtColor(vec[:, :, :3], cv2.COLOR_RGB2LAB).astype(np.float32)
    delta_e = np.sqrt(np.sum((ref_lab - vec_lab)**2, axis=2))[inter].mean()
    
    ref_fg = ref[:, :, :3][inter].astype(np.float32)
    vec_fg = vec[:, :, :3][inter].astype(np.float32)
    ncc = np.mean([np.corrcoef(ref_fg[:, i], vec_fg[:, i])[0, 1] for i in range(3)])
    mse = np.mean((ref_fg - vec_fg)**2)
    return iou, ssim_val, ncc, delta_e, mse

# Read base SVG
with open('scratch/test_tune_feet.svg') as f:
    base_svg = f.read()

# Replace the eye section with anatomical sleepy eyelids
# In base_svg, section 3:
old_eyes = base_svg[base_svg.find('<!-- 3. Eye Sockets'):base_svg.find('<!-- 4. Beak')]

# Let's define new eyes with:
# 1. Socket background (dark chocolate)
# 2. Amber iris gradient (rich amber radiating from bottom-center)
# 3. Slumped sleepy pupil (dark ovate)
# 4. White specular reflection (x=188, y=154 on left, x=302, y=154 on right)
# 5. Drooping porcelain eyelids with soft drop shadow over the upper half!

new_eye_defs = '''
    <!-- Sleepy Eyelid Porcelain Shading -->
    <linearGradient id="eyelidGradL" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.9" />
      <stop offset="60%" stop-color="#EFE8DE" />
      <stop offset="90%" stop-color="#DCD3C7" />
      <stop offset="100%" stop-color="#8C7969" />
    </linearGradient>

    <linearGradient id="eyelidGradR" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#FAF5EE" stop-opacity="0.9" />
      <stop offset="60%" stop-color="#EAE3D9" />
      <stop offset="90%" stop-color="#D4C9BD" />
      <stop offset="100%" stop-color="#7C6B5C" />
    </linearGradient>

    <!-- Eyelid Cast Shadow on Iris -->
    <linearGradient id="eyelidShadow" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#0A0401" stop-opacity="0.85" />
      <stop offset="50%" stop-color="#2D1302" stop-opacity="0.45" />
      <stop offset="100%" stop-color="#6B3204" stop-opacity="0.0" />
    </linearGradient>
'''

new_eyes_group = '''  <!-- 3. Eye Sockets & Amber Eyes (Anatomical Sleepy Hooded Aperture) -->
  <!-- Left Eye -->
  <g id="left_eye">
    <!-- Socket Rim Deep Groove -->
    <ellipse cx="194" cy="157" rx="30" ry="24" fill="#3D2817" opacity="0.45" />
    <path d="M 166 142 C 165 166, 175 180, 194 180 C 213 180, 224 166, 223 142 C 205 139, 185 139, 166 142 Z" fill="#1C0C02" />
    
    <!-- Amber Iris (Half-Moon Sliced) -->
    <path d="M 167 143 C 166 165, 176 178, 194 178 C 212 178, 222 165, 221 143 C 205 140, 185 140, 167 143 Z" fill="url(#amberEyeL)" />
    
    <!-- Pupil centered in lower aperture -->
    <ellipse cx="194" cy="162" rx="15" ry="11" fill="url(#pupilGrad)" />
    
    <!-- Cast Shadow under eyelid -->
    <path d="M 167 143 C 185 140, 205 140, 221 143 L 221 152 C 205 151, 185 151, 167 152 Z" fill="url(#eyelidShadow)" />

    <!-- Specular Highlight Dot on Left Iris -->
    <circle cx="188" cy="154" r="3.2" fill="#FFFFFF" opacity="0.95" />
    <circle cx="188" cy="154" r="5.0" fill="#FFFFFF" opacity="0.30" />

    <!-- Drooping Porcelain Upper Eyelid Hood -->
    <path d="M 164 140 C 170 120, 218 120, 224 140 C 206 142, 184 142, 164 140 Z" fill="url(#eyelidGradL)" />
    <path d="M 165 141 C 185 143, 205 143, 224 141" stroke="#3D2817" stroke-width="1.2" stroke-linecap="round" fill="none" />
  </g>

  <!-- Right Eye -->
  <g id="right_eye">
    <!-- Socket Rim Deep Groove -->
    <ellipse cx="310" cy="157" rx="30" ry="24" fill="#301A0D" opacity="0.45" />
    <path d="M 282 142 C 281 166, 291 180, 310 180 C 329 180, 339 166, 338 142 C 322 139, 300 139, 282 142 Z" fill="#180A02" />
    
    <!-- Amber Iris (Half-Moon Sliced) -->
    <path d="M 283 143 C 282 165, 292 178, 310 178 C 328 178, 338 165, 337 143 C 322 140, 300 140, 283 143 Z" fill="url(#amberEyeR)" />
    
    <!-- Pupil centered in lower aperture -->
    <ellipse cx="310" cy="162" rx="15" ry="11" fill="url(#pupilGrad)" />
    
    <!-- Cast Shadow under eyelid -->
    <path d="M 283 143 C 300 140, 322 140, 337 143 L 337 152 C 322 151, 300 151, 283 152 Z" fill="url(#eyelidShadow)" />

    <!-- Specular Highlight Dot on Right Iris -->
    <circle cx="304" cy="154" r="2.8" fill="#FFFFFF" opacity="0.85" />
    <circle cx="304" cy="154" r="4.5" fill="#FFFFFF" opacity="0.25" />

    <!-- Drooping Porcelain Upper Eyelid Hood -->
    <path d="M 280 140 C 286 120, 334 120, 340 140 C 322 142, 300 142, 280 140 Z" fill="url(#eyelidGradR)" />
    <path d="M 281 141 C 300 143, 322 143, 340 141" stroke="#301A0D" stroke-width="1.2" stroke-linecap="round" fill="none" />
  </g>
'''

# Insert new defs before </defs>
insert_pos = base_svg.find('</defs>')
test_svg = base_svg[:insert_pos] + new_eye_defs + base_svg[insert_pos:]
test_svg = test_svg.replace(old_eyes, new_eyes_group)

render_svg_chrome(test_svg, 'scratch/test_owluko_eyes_opt.png')
iou, ssim_val, ncc, de, mse = evaluate('scratch/test_owluko_eyes_opt.png')
print(f'Results with Sleepy Eyelids:')
print(f'IoU:     {iou*100:.2f}%')
print(f'SSIM:    {ssim_val*100:.2f}%')
print(f'NCC:     {ncc*100:.2f}%')
print(f'Delta E: {de:.2f}')
print(f'MSE:     {mse:.2f}')

with open('scratch/test_owluko_opt_v1.svg', 'w') as f:
    f.write(test_svg)
