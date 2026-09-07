import os
import sys
import glob
import json
import shutil
import zipfile
import subprocess
from PIL import Image

os.environ["U2NET_HOME"] = os.path.abspath(".cache/u2net")
import rembg

session = rembg.new_session("u2net")

REMAINING_STATES = {
    "05_thumbs_up": {"prefix": "aituko_thumbs_up", "title": "Pouce en l'Air & Validation"},
    "06_sleeping": {"prefix": "aituko_sleeping", "title": "Veille & Sommeil Zzz"},
    "07_pointing": {"prefix": "aituko_pointing", "title": "Pointage & Guidage"},
    "08_searching": {"prefix": "aituko_searching", "title": "Recherche & Scan à la Loupe"},
    "09_loading": {"prefix": "aituko_loading", "title": "Chargement & Orbite Étoile"},
    "10_idea": {"prefix": "aituko_idea", "title": "Idée Trouvée & Ampoule"},
    "11_security": {"prefix": "aituko_security", "title": "Sécurité & Protection"},
    "12_goodbye": {"prefix": "aituko_goodbye", "title": "Au Revoir & Départ"}
}

for st_id, info in REMAINING_STATES.items():
    prefix = info["prefix"]
    title = info["title"]
    
    src_img = f"mascots/aituko/{prefix}.jpeg"
    src_mp4 = f"mascots/aituko/{prefix}.mp4"
    
    if not os.path.exists(src_img) or not os.path.exists(src_mp4):
        print(f"⚠️ Missing source for {st_id}")
        continue
        
    print(f"\n🚀 Traitement Google Flow Labs : {st_id} ({title})...", flush=True)
    
    out_dir = f"assets/{st_id}"
    m_dir = f"mascots/aituko/assets/{st_id}"
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(m_dir, exist_ok=True)
    
    tmp_raw = f"{out_dir}/_tmp_raw"
    tmp_clean = f"{out_dir}/_tmp_clean"
    os.makedirs(tmp_raw, exist_ok=True)
    os.makedirs(tmp_clean, exist_ok=True)
    
    # 1. Static Image Matting
    im_static = Image.open(src_img)
    w, h = im_static.size
    left = (w - h) // 2
    im_static_sq = im_static.crop((left, 0, left + h, h))
    static_clean = rembg.remove(im_static_sq, session=session, alpha_matting=False)
    
    static_clean.save(f"{out_dir}/static.png", "PNG")
    static_clean.save(f"{out_dir}/static.webp", "WEBP", quality=95)
    static_clean.save(f"{m_dir}/static.png", "PNG")
    static_clean.save(f"{m_dir}/static.webp", "WEBP", quality=95)
    
    # 2. Video Looping & Frame Extraction
    looped_mp4 = f"{out_dir}/looped_video.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-t", "2.0", "-i", src_mp4,
        "-filter_complex", "[0:v]split[v1][v2];[v2]reverse[v2rev];[v1][v2rev]concat=n=2:v=1[v]",
        "-map", "[v]", "-r", "24", "-c:v", "libx264", "-pix_fmt", "yuv420p", looped_mp4
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    shutil.copy(looped_mp4, f"{m_dir}/looped_video.mp4")
    
    # Extract frames
    subprocess.run([
        "ffmpeg", "-y", "-i", looped_mp4,
        "-vf", "fps=24", f"{tmp_raw}/f_%03d.png"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    raw_frames = sorted(glob.glob(f"{tmp_raw}/f_*.png"))
    clean_frames = []
    
    for idx, rf in enumerate(raw_frames):
        frm = Image.open(rf)
        fw, fh = frm.size
        if fw != fh:
            fleft = (fw - fh) // 2
            frm = frm.crop((fleft, 0, fleft + fh, fh))
            
        cfrm = rembg.remove(frm, session=session, alpha_matting=False)
        clean_frames.append(cfrm)
        cfrm.save(f"{tmp_clean}/f_{idx+1:03d}.png", "PNG")
        
    # 3. Animated WebP
    webp_path = f"{out_dir}/animated.webp"
    clean_frames[0].save(
        webp_path,
        format="WEBP",
        save_all=True,
        append_images=clean_frames[1:],
        duration=int(1000 / 24),
        loop=0,
        quality=90,
        method=4
    )
    shutil.copy(webp_path, f"{m_dir}/animated.webp")
    
    # 4. Animated GIF
    gif_path = f"{out_dir}/animated.gif"
    subprocess.run([
        "ffmpeg", "-y", "-framerate", "24", "-i", f"{tmp_clean}/f_%03d.png",
        "-filter_complex", "[0:v]split[a][b];[a]palettegen=reserve_transparent=on:transparency_color=ffffff00[p];[b][p]paletteuse=alpha_threshold=128:dither=bayer:bayer_scale=3",
        gif_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(gif_path):
        shutil.copy(gif_path, f"{m_dir}/animated.gif")
        
    # 5. APNG (animated.png)
    apng_path = f"{out_dir}/animated.png"
    clean_frames[0].save(
        apng_path,
        format="PNG",
        save_all=True,
        append_images=clean_frames[1:],
        duration=int(1000 / 24),
        loop=0
    )
    shutil.copy(apng_path, f"{m_dir}/animated.png")
    
    # 6. Snippet JSON
    name_cap = st_id.split("_")[1].capitalize()
    snippet_data = {
        "name": f"AItuko - {title}",
        "html": f'<picture>\n  <source srcset="assets/{st_id}/animated.webp" type="image/webp">\n  <img src="assets/{st_id}/animated.gif" alt="AItuko {title}" width="512" height="512">\n</picture>',
        "react": f'import React from "react";\n\nexport const Aituko{name_cap} = ({{ size = 180, className = "" }}) => (\n  <picture>\n    <source srcSet="/assets/{st_id}/animated.webp" type="image/webp" />\n    <img src="/assets/{st_id}/animated.gif" alt="AItuko {title}" width={{size}} height={{size}} className={{"object-contain " + className}} />\n  </picture>\n);',
        "vue": f'<template>\n  <picture>\n    <source :srcset="`/assets/{st_id}/animated.webp`" type="image/webp">\n    <img :src="`/assets/{st_id}/animated.gif`" :alt="`AItuko {title}`" :width="size" :height="size" class="object-contain">\n  </picture>\n</template>\n<script setup>\ndefineProps({{ size: {{ type: Number, default: 180 }} }});\n</script>',
        "flutter": f'// Flutter Widget for AItuko {title}\nImage.asset("assets/{st_id}/animated.webp", width: 180.0, height: 180.0, fit: BoxFit.contain);'
    }
    with open(f"{out_dir}/snippet.json", "w", encoding="utf-8") as f:
        json.dump(snippet_data, f, indent=2, ensure_ascii=False)
    shutil.copy(f"{out_dir}/snippet.json", f"{m_dir}/snippet.json")
    
    # 7. ZIP Bundle
    zip_path = f"{out_dir}/bundle_aituko_{st_id}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(f"{out_dir}/static.png", "static.png")
        z.write(f"{out_dir}/static.webp", "static.webp")
        z.write(f"{out_dir}/animated.webp", "animated.webp")
        if os.path.exists(gif_path):
            z.write(gif_path, "animated.gif")
        z.write(apng_path, "animated.png")
        z.write(looped_mp4, "video_loop.mp4")
        z.write(f"{out_dir}/snippet.json", "snippet.json")
    shutil.copy(zip_path, f"{m_dir}/bundle_aituko_{st_id}.zip")
    
    # Cleanup tmp immediately
    shutil.rmtree(tmp_raw, ignore_errors=True)
    shutil.rmtree(tmp_clean, ignore_errors=True)
    print(f"✨ [OK] {st_id} ({title}) finalisé avec succès !", flush=True)

print("\n🎉 TOUS LES ÉTATS D'AITUKO SONT TRAITÉS ET INTÉGRÉS !")
