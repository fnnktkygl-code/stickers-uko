import os
import numpy as np
from PIL import Image

# Ensure local cache for rembg models inside workspace
os.environ["U2NET_HOME"] = os.path.abspath(".cache/u2net")
os.makedirs(".cache/u2net", exist_ok=True)

import rembg

_SESSION = None

def get_rembg_session():
    global _SESSION
    if _SESSION is None:
        _SESSION = rembg.new_session("u2net")
    return _SESSION

def apply_color_despill(rgba_img: Image.Image) -> Image.Image:
    """
    VFX Color Despill suppression algorithm.
    Neutralizes green bounce/spill light reflecting on glossy surfaces.
    """
    arr = np.array(rgba_img, dtype=np.float32)
    r, g, b, a = arr[:,:,0], arr[:,:,1], arr[:,:,2], arr[:,:,3]
    
    # Where Green > average of Red and Blue, suppress excess green
    excess_green = g - np.maximum(r, b)
    mask_green = excess_green > 0
    
    g[mask_green] = (r[mask_green] + b[mask_green]) / 2.0
    arr[:,:,1] = g
    
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), mode="RGBA")

def key_greenscreen_master(img: Image.Image) -> Image.Image:
    """
    SOTA AI Matting Engine:
    1. Deep learning semantic background separation (rembg / u2net)
    2. VFX Color Despill Matrix (eliminates all green bounce on porcelain & glass)
    3. Continuous subpixel alpha gradient
    """
    session = get_rembg_session()
    
    # 1. AI Deep Segmentation
    raw_cut = rembg.remove(
        img,
        session=session,
        alpha_matting=True,
        alpha_matting_erode_size=5
    )
    
    # 2. VFX Color Despill
    clean_img = apply_color_despill(raw_cut)
    
    return clean_img
