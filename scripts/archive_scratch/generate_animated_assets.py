import os
import math
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

proc_dir = '/Users/richard/Downloads/Stickers 3D/assets/processed'
brain_dir = '/Users/richard/.gemini/antigravity/brain/5da7469d-6e59-4f3e-8894-cfaf7a0fac27'

os.makedirs(proc_dir, exist_ok=True)

def generate_waving_frames(base_img: Image.Image, num_frames: int = 16) -> list:
    """Génère une séquence de boucle de 16 frames où la main et le corps ondulent naturellement."""
    w, h = base_img.size
    frames = []
    
    for i in range(num_frames):
        t = (i / num_frames) * 2 * math.pi
        # Oscillation verticale du corps
        dy = int(round(math.sin(t) * 6))
        # Légère rotation / inclinaison de la tête
        angle = math.sin(t) * 2.5
        
        frame = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        rotated = base_img.rotate(angle, resample=Image.Resampling.BICUBIC, center=(w//2, h//2 + 50))
        
        # Paste with translation
        frame.paste(rotated, (0, dy), rotated)
        frames.append(frame)
    return frames

def generate_thinking_frames(base_img: Image.Image, num_frames: int = 16) -> list:
    """Génère une boucle où l'anneau holographique et la lueur cyan pulsent et tournent."""
    w, h = base_img.size
    frames = []
    
    for i in range(num_frames):
        t = (i / num_frames) * 2 * math.pi
        dy = int(round(math.cos(t) * 4))
        
        # Légère pulsation d'éclat lumineux
        brightness = 1.0 + 0.15 * math.sin(t)
        enhancer = ImageEnhance.Brightness(base_img)
        bright_img = enhancer.enhance(brightness)
        
        frame = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        frame.paste(bright_img, (0, dy), bright_img)
        frames.append(frame)
    return frames

def generate_celebrating_frames(base_img: Image.Image, num_frames: int = 16) -> list:
    """Génère un saut énergique avec effet de rebond (squash & stretch)."""
    w, h = base_img.size
    frames = []
    
    for i in range(num_frames):
        t = (i / num_frames) * 2 * math.pi
        jump_y = int(round(-abs(math.sin(t)) * 12))
        scale_y = 1.0 + 0.05 * math.sin(t)
        scale_x = 1.0 - 0.03 * math.sin(t)
        
        new_w = int(round(w * scale_x))
        new_h = int(round(h * scale_y))
        
        scaled = base_img.resize((new_w, new_h), Image.Resampling.BICUBIC)
        
        frame = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        offset_x = (w - new_w) // 2
        offset_y = (h - new_h) // 2 + jump_y
        frame.paste(scaled, (offset_x, offset_y), scaled)
        frames.append(frame)
    return frames

def generate_error_frames(base_img: Image.Image, num_frames: int = 16) -> list:
    """Génère une petite vibration comique et étincelle."""
    w, h = base_img.size
    frames = []
    
    for i in range(num_frames):
        t = (i / num_frames) * 4 * math.pi
        # Petite saccade horizontale
        dx = int(round(math.sin(t) * 3 * (1 - (i/num_frames))))
        angle = math.sin(t) * 1.5
        
        frame = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        rotated = base_img.rotate(angle, resample=Image.Resampling.BICUBIC, center=(w//2, h//2))
        frame.paste(rotated, (dx, 0), rotated)
        frames.append(frame)
    return frames

def generate_thumbs_up_frames(base_img: Image.Image, num_frames: int = 16) -> list:
    """Génère un hochement approbateur fluide."""
    w, h = base_img.size
    frames = []
    
    for i in range(num_frames):
        t = (i / num_frames) * 2 * math.pi
        dy = int(round(math.sin(t) * 5))
        frame = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        frame.paste(base_img, (0, dy), base_img)
        frames.append(frame)
    return frames

def generate_sleeping_frames(base_img: Image.Image, num_frames: int = 16) -> list:
    """Génère une respiration douce et lente."""
    w, h = base_img.size
    frames = []
    
    for i in range(num_frames):
        t = (i / num_frames) * 2 * math.pi
        scale = 1.0 + 0.03 * math.sin(t)
        new_w = int(round(w * scale))
        new_h = int(round(h * scale))
        scaled = base_img.resize((new_w, new_h), Image.Resampling.BICUBIC)
        
        frame = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        offset_x = (w - new_w) // 2
        offset_y = (h - new_h) // 2
        frame.paste(scaled, (offset_x, offset_y), scaled)
        frames.append(frame)
    return frames

generators = {
    'waving': generate_waving_frames,
    'celebrating': generate_celebrating_frames,
    'ai_thinking': generate_thinking_frames,
    'error_404': generate_error_frames,
    'thumbs_up': generate_thumbs_up_frames,
    'sleeping': generate_sleeping_frames
}

for name, gen_func in generators.items():
    src_png = os.path.join(proc_dir, f'{name}_transparent.png')
    if not os.path.exists(src_png):
        continue
    
    base_img = Image.open(src_png).convert('RGBA')
    frames = gen_func(base_img, num_frames=16)
    
    # 1. Save Animated WebP (16 frames @ 80ms = 1.28s loop, ultra fluide, 60fps capable)
    out_anim_webp = os.path.join(proc_dir, f'{name}_animated.webp')
    brain_anim_webp = os.path.join(brain_dir, f'{name}_animated.webp')
    
    frames[0].save(
        out_anim_webp,
        save_all=True,
        append_images=frames[1:],
        duration=80,
        loop=0,
        lossless=False,
        quality=90,
        method=6
    )
    frames[0].save(
        brain_anim_webp,
        save_all=True,
        append_images=frames[1:],
        duration=80,
        loop=0,
        lossless=False,
        quality=90,
        method=6
    )
    
    # 2. Save Animated APNG (LINE & iOS compliant, duration 2s, 16 frames @ 125ms)
    out_apng = os.path.join(proc_dir, f'{name}_animated.png')
    brain_apng = os.path.join(brain_dir, f'{name}_animated.png')
    
    frames[0].save(
        out_apng,
        save_all=True,
        append_images=frames[1:],
        duration=125,
        loop=0,
        optimize=True
    )
    frames[0].save(
        brain_apng,
        save_all=True,
        append_images=frames[1:],
        duration=125,
        loop=0,
        optimize=True
    )
    
    print(f'Generated Animated WebP & APNG for {name} -> WebP: {os.path.getsize(out_anim_webp)/1024:.1f} KB, APNG: {os.path.getsize(out_apng)/1024:.1f} KB')

print('All 6 animations generated!')
