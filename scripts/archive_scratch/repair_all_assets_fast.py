import os
import glob
import time
import zipfile
import numpy as np
from PIL import Image
from scipy import ndimage
from concurrent.futures import ProcessPoolExecutor, as_completed

def clean_alpha_holes_fast(rgba_arr):
    """Fast vectorized morphological hole filling & green despill."""
    r, g, b, a = rgba_arr[:,:,0], rgba_arr[:,:,1], rgba_arr[:,:,2], rgba_arr[:,:,3]
    
    # Internal holes in body mask
    opaque_mask = a > 160
    filled = ndimage.binary_fill_holes(opaque_mask)
    
    # Update alpha where there were holes
    new_a = np.where(filled & (a < 160), 255, a).astype(np.uint8)
    
    # Green despill
    max_rb = np.maximum(r, b)
    is_green_fringe = (g > max_rb) & (new_a > 0)
    despilled_g = np.where(is_green_fringe, max_rb, g).astype(np.uint8)
    
    return np.dstack([r, despilled_g, b, new_a])

def process_single_state(args):
    m_key, d, s = args
    if not os.path.exists(d):
        return f"SKIP {m_key}/{s}"
        
    apng_path = f"{d}/animated.png"
    gif_path = f"{d}/animated.gif"
    webp_path = f"{d}/animated.webp"
    static_png = f"{d}/static.png"
    static_webp = f"{d}/static.webp"
    
    if not os.path.exists(apng_path):
        return f"NO APNG {m_key}/{s}"
        
    # Read APNG
    anim = Image.open(apng_path)
    n_frames = getattr(anim, 'n_frames', 1)
    
    clean_frames = []
    durations = []
    
    for idx in range(n_frames):
        anim.seek(idx)
        f_rgba = np.array(anim.convert("RGBA"))
        
        # Clean alpha holes & despill
        clean_arr = clean_alpha_holes_fast(f_rgba)
        f_pil = Image.fromarray(clean_arr, mode="RGBA")
        
        # Ensure 512x512
        w, h = f_pil.size
        if (w, h) != (512, 512):
            canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
            if w > 512 or h > 512:
                f_pil.thumbnail((512, 512), Image.Resampling.LANCZOS)
                w, h = f_pil.size
            canvas.paste(f_pil, ((512 - w) // 2, (512 - h) // 2), f_pil)
            f_pil = canvas
            
        clean_frames.append(f_pil)
        durations.append(anim.info.get('duration', 41))
        
    if not clean_frames:
        return f"EMPTY {m_key}/{s}"
        
    # 1. Update Static PNG & WebP
    if os.path.exists(static_png):
        st = Image.open(static_png)
        st_arr = clean_alpha_holes_fast(np.array(st.convert("RGBA")))
        st_pil = Image.fromarray(st_arr, mode="RGBA")
        w, h = st_pil.size
        if (w, h) != (512, 512):
            canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
            if w > 512 or h > 512:
                st_pil.thumbnail((512, 512), Image.Resampling.LANCZOS)
                w, h = st_pil.size
            canvas.paste(st_pil, ((512 - w) // 2, (512 - h) // 2), st_pil)
            st_pil = canvas
        st_pil.save(static_png, optimize=True)
        st_pil.save(static_webp, quality=92)
    else:
        clean_frames[0].save(static_png, optimize=True)
        clean_frames[0].save(static_webp, quality=92)
        
    # 2. Save Animated WebP (quality 88, method=4)
    clean_frames[0].save(
        webp_path,
        save_all=True,
        append_images=clean_frames[1:],
        duration=durations,
        loop=0,
        quality=88,
        method=4
    )
    
    # 3. Save Animated GIF (Quantize with transparency palette, 0 green background)
    gif_frames = []
    for f in clean_frames:
        alpha = f.split()[3]
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        p_frame = f.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE)
        p_frame.paste(255, mask)
        p_frame.info['transparency'] = 255
        gif_frames.append(p_frame)
        
    gif_frames[0].save(
        gif_path,
        save_all=True,
        append_images=gif_frames[1:],
        duration=durations,
        loop=0,
        disposal=2
    )
    
    # Remove stray files if any
    stray = f"{d}/looped.mp4"
    if os.path.exists(stray):
        os.remove(stray)
        
    return f"✅ DONE {m_key}/{s}"

def main():
    start_time = time.time()
    print("⚡️ LAUNCHING HIGH-PERFORMANCE PARALLEL ASSET REPAIR...")

    mascots_dirs = [
        ("aituko", "mascots/aituko/assets"),
        ("aituko_root", "assets"),
        ("hatoko", "mascots/hatoko/assets"),
        ("inuko", "mascots/inuko/assets"),
        ("luneko", "mascots/luneko/assets"),
        ("owluko", "mascots/owluko/assets"),
        ("usako", "mascots/usako/assets"),
    ]

    states = [
        '01_waving', '02_celebrating', '03_ai_thinking', '04_error_404',
        '05_thumbs_up', '06_sleeping', '07_pointing', '08_searching',
        '09_loading', '10_idea', '11_security', '12_goodbye'
    ]

    tasks = []
    for m_key, base_dir in mascots_dirs:
        for s in states:
            d = f"{base_dir}/{s}"
            tasks.append((m_key, d, s))

    print(f"Total parallel tasks: {len(tasks)}")

    completed_count = 0
    with ProcessPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(process_single_state, t) for t in tasks]
        for future in as_completed(futures):
            res = future.result()
            completed_count += 1
            print(f"[{completed_count}/{len(tasks)}] {res}")

    print(f"\n🎉 All {len(tasks)} assets repaired in {time.time() - start_time:.1f}s!")

if __name__ == "__main__":
    main()
