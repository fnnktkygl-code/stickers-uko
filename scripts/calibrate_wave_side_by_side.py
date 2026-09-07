import json
import numpy as np
from scipy.interpolate import CubicSpline
import cv2
from PIL import Image, ImageDraw, ImageFilter
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_flawless_aituko_idle import load_master_components, transform_rgba

with open('scratch/wave_ref_tracking_96.json') as f:
    raw_data = json.load(f)

# Reference times (96 frames at 24 fps -> 4.0s)
t_ref = np.linspace(0, 4.0, 97)
data_periodic = raw_data + [raw_data[0]]

# Extract trajectories
# Head:
head_dys = [d['eye'][1] - raw_data[0]['eye'][1] for d in data_periodic]
head_rots = [d['eye'][2] for d in data_periodic]

# Calibration factor to map 720p ref coordinates to 512x512 canvas:
scale = 0.82

lw_dxs = [(d['lw'][0] - raw_data[0]['lw'][0]) * scale for d in data_periodic]
lw_dys = [(d['lw'][1] - raw_data[0]['lw'][1]) * scale for d in data_periodic]
# In reference, delta angle from rest:
lw_drots = [-(d['lw'][2] - raw_data[0]['lw'][2]) for d in data_periodic]

rw_dxs = [(d['rw'][0] - raw_data[0]['rw'][0]) * scale for d in data_periodic]
rw_dys = [(d['rw'][1] - raw_data[0]['rw'][1]) * scale for d in data_periodic]
rw_drots = [d['rw'][2] - raw_data[0]['rw'][2] for d in data_periodic]

cs_head_dy = CubicSpline(t_ref, head_dys, bc_type='periodic')
cs_head_rot = CubicSpline(t_ref, head_rots, bc_type='periodic')
cs_lw_dx = CubicSpline(t_ref, lw_dxs, bc_type='periodic')
cs_lw_dy = CubicSpline(t_ref, lw_dys, bc_type='periodic')
cs_lw_drot = CubicSpline(t_ref, lw_drots, bc_type='periodic')
cs_rw_dx = CubicSpline(t_ref, rw_dxs, bc_type='periodic')
cs_rw_dy = CubicSpline(t_ref, rw_dys, bc_type='periodic')
cs_rw_drot = CubicSpline(t_ref, rw_drots, bc_type='periodic')

master_components = load_master_components()

def render_frame_at_time(t, backdrop=(0, 255, 0, 255)):
    canvas = Image.new('RGBA', (512, 512), backdrop)
    
    # 1. Ground Contact Shadow
    dy_root = float(cs_head_dy(t)) * 0.6
    sh_layer = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(sh_layer)
    cx, cy = 256, 488
    rx = int(95 * (1.0 - 0.05 * (dy_root / 15.0)))
    ry = int(12 * (1.0 - 0.05 * (dy_root / 15.0)))
    sh_draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(0, 0, 0, 130))
    sh_layer = sh_layer.filter(ImageFilter.GaussianBlur(radius=6))
    canvas.alpha_composite(sh_layer)
    
    # 2. Feet
    dy_feet = float(cs_head_dy(t)) * 0.8
    feet_pivot = (256.0, 448.0)
    w_lfoot = transform_rgba(master_components["lfoot"], feet_pivot, angle_deg=0.0,
                             scale=(1.0, 1.0), translate=(0.0, dy_feet))
    w_rfoot = transform_rgba(master_components["rfoot"], feet_pivot, angle_deg=0.0,
                             scale=(1.0, 1.0), translate=(0.0, dy_feet))
    canvas.alpha_composite(Image.fromarray(w_lfoot))
    canvas.alpha_composite(Image.fromarray(w_rfoot))
    
    # 3. Torso
    torso_pivot = (256.0, 312.0)
    w_torso = transform_rgba(master_components["torso"], torso_pivot, angle_deg=0.0,
                             scale=(1.0, 1.0), translate=(0.0, dy_root))
    canvas.alpha_composite(Image.fromarray(w_torso))
    
    # 4. Neck collar
    neck_layer = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
    neck_cy = int(204.0 + float(cs_head_dy(t)))
    ImageDraw.Draw(neck_layer).ellipse([256 - 15, neck_cy - 7, 256 + 15, neck_cy + 7], fill=(24, 27, 38, 255))
    canvas.alpha_composite(neck_layer)
    
    # 5. Head
    head_pivot = (256.0, 204.0)
    rot_h = float(cs_head_rot(t))
    dy_h = float(cs_head_dy(t))
    w_head = transform_rgba(master_components["head"], head_pivot, angle_deg=rot_h,
                            scale=(1.0, 1.0), translate=(0.0, dy_h))
    canvas.alpha_composite(Image.fromarray(w_head))
    
    # 6. Eyes (Always bright smiling cyan arches!)
    w_eyes = transform_rgba(master_components["eyes"], head_pivot, angle_deg=rot_h,
                            scale=(1.0, 1.0), translate=(0.0, dy_h))
    eyes_im = Image.fromarray(w_eyes)
    e_bloom1 = eyes_im.filter(ImageFilter.GaussianBlur(radius=6))
    e_bloom2 = eyes_im.filter(ImageFilter.GaussianBlur(radius=2))
    canvas.alpha_composite(e_bloom1)
    canvas.alpha_composite(e_bloom2)
    canvas.alpha_composite(eyes_im)
    
    # 7. Right winglet (resting/stabilizing float on viewer right)
    tx_r = float(cs_rw_dx(t))
    ty_r = float(cs_rw_dy(t))
    rot_r = float(cs_rw_drot(t))
    w_rpod = transform_rgba(master_components["rpod"], (355.0, 345.0), angle_deg=rot_r,
                            scale=(1.0, 1.0), translate=(tx_r, ty_r))
    canvas.alpha_composite(Image.fromarray(w_rpod))
    
    # 8. Left winglet (WAVING WINGLET on viewer left)
    tx_l = float(cs_lw_dx(t))
    ty_l = float(cs_lw_dy(t))
    rot_l = float(cs_lw_drot(t))
    w_lpod = transform_rgba(master_components["lpod"], (147.0, 321.0), angle_deg=rot_l,
                            scale=(1.0, 1.0), translate=(tx_l, ty_l))
    canvas.alpha_composite(Image.fromarray(w_lpod))
    
    return canvas

# Render test frames
os.makedirs('scratch/test_renders', exist_ok=True)
test_frames = [
    (1, 0.0),
    (30, 29 / 24.0),
    (45, 44 / 24.0),
    (60, 59 / 24.0),
    (75, 74 / 24.0),
]

for frame_no, t in test_frames:
    rendered = render_frame_at_time(t, backdrop=(0, 255, 0, 255))
    rendered.save(f'scratch/test_renders/rendered_f{frame_no:03d}.png')
    print(f'Rendered frame {frame_no:03d} at t={t:.2f}s')

print('Calibration render complete!')
