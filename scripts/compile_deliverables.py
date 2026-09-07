#!/usr/bin/env python3
"""
Compiles all final deliverables from the 120 rendered frames:
1. Animated WebP (transparent)
2. Animated GIF (transparent, dark, green, white)
3. MP4 videos (dark, green)
4. Trichroma Board (White, Dark, Green)
5. Master Keyframe Board (1920x1080)
6. Bundle ZIPs
7. Visual Artifacts
"""

import os
import sys
import shutil
import zipfile
import subprocess
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

WORKSPACE_DIR = "/Users/richard/Developer/Stickers Uko"
BRAIN_DIRS = [
    "/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68",
    "/Users/richard/.gemini/antigravity/brain/467a784a-d1d2-4cca-89a3-7ecb1a862229"
]
TARGET_DIRS = [
    os.path.join(WORKSPACE_DIR, "assets/00_idle"),
    os.path.join(WORKSPACE_DIR, "mascots/aituko/assets/00_idle"),
    os.path.join(WORKSPACE_DIR, "aituko/assets/00_idle"),
]

def run():
    print("🎬 Step 1: Loading frames...")
    frames_rgba = [Image.open(f"assets/00_idle/frames/frame_{i:03d}.png") for i in range(120)]
    frames_dark = [Image.open(f"assets/00_idle/temp_dark_frames/frame_{i:03d}.png") for i in range(120)]
    frames_green = [Image.open(f"assets/00_idle/temp_green_frames/frame_{i:03d}.png") for i in range(120)]

    # 1. Animated WebP (Transparent)
    print("🎬 Step 2: Compiling Animated WebP...")
    webp_path = os.path.join(TARGET_DIRS[0], "animated.webp")
    frames_rgba[0].save(
        webp_path,
        save_all=True,
        append_images=frames_rgba[1:],
        duration=33,
        loop=0,
        quality=92,
        method=4
    )
    for td in TARGET_DIRS[1:]:
        os.makedirs(td, exist_ok=True)
        shutil.copy(webp_path, os.path.join(td, "animated.webp"))
    print("   ✅ Animated WebP saved.")

    # 2. Animated GIF (Transparent)
    print("🎬 Step 3: Compiling Animated GIF (Transparent)...")
    gif_frames = []
    for f_im in frames_rgba:
        alpha = f_im.split()[3]
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        p_frame = f_im.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE)
        p_frame.paste(255, mask)
        p_frame.info['transparency'] = 255
        gif_frames.append(p_frame)

    gif_path = os.path.join(TARGET_DIRS[0], "animated.gif")
    gif_frames[0].save(
        gif_path,
        save_all=True,
        append_images=gif_frames[1:],
        duration=33,
        loop=0,
        disposal=2
    )
    for td in TARGET_DIRS[1:]:
        shutil.copy(gif_path, os.path.join(td, "animated.gif"))
    print("   ✅ Animated GIF (Transparent) saved.")

    # 3. Animated GIF on Studio Dark & Chroma Green
    print("🎬 Step 4: Compiling Studio Dark & Chroma Green GIFs...")
    dark_gif_path = os.path.join(TARGET_DIRS[0], "animated_dark.gif")
    dark_q = [f.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE) for f in frames_dark]
    dark_q[0].save(dark_gif_path, save_all=True, append_images=dark_q[1:], duration=33, loop=0)
    for td in TARGET_DIRS[1:]:
        shutil.copy(dark_gif_path, os.path.join(td, "animated_dark.gif"))

    green_gif_path = os.path.join(TARGET_DIRS[0], "animated_green.gif")
    green_q = [f.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE) for f in frames_green]
    green_q[0].save(green_gif_path, save_all=True, append_images=green_q[1:], duration=33, loop=0)
    for td in TARGET_DIRS[1:]:
        shutil.copy(green_gif_path, os.path.join(td, "animated_green.gif"))
    print("   ✅ Studio Dark & Chroma Green GIFs saved.")

    # 4. Copy MP4 videos to all targets
    print("🎬 Step 5: Distributing MP4 videos...")
    for td in TARGET_DIRS[1:]:
        shutil.copy(os.path.join(TARGET_DIRS[0], "looped_video.mp4"), os.path.join(td, "looped_video.mp4"))
        shutil.copy(os.path.join(TARGET_DIRS[0], "preview_studio_green.mp4"), os.path.join(td, "preview_studio_green.mp4"))
    shutil.copy(os.path.join(TARGET_DIRS[0], "looped_video.mp4"), os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_idle_vector.mp4"))
    print("   ✅ MP4 videos distributed.")

    # 5. Build Trichroma Board
    print("🖼️ Step 6: Building Trichroma Verification Board...")
    # Composite frame 0 on pure white
    white_bg = Image.new("RGBA", (512, 512), (255, 255, 255, 255))
    white_bg.alpha_composite(frames_rgba[0])
    
    trichroma = Image.new("RGB", (1536, 512), (0, 0, 0))
    trichroma.paste(white_bg.convert("RGB"), (0, 0))
    trichroma.paste(frames_dark[0].convert("RGB"), (512, 0))
    trichroma.paste(frames_green[0].convert("RGB"), (1024, 0))
    
    t_draw = ImageDraw.Draw(trichroma)
    t_draw.line([(512, 0), (512, 512)], fill=(50, 50, 50), width=2)
    t_draw.line([(1024, 0), (1024, 512)], fill=(50, 50, 50), width=2)
    
    font_path = "/System/Library/Fonts/Helvetica.ttc"
    font = ImageFont.truetype(font_path, 13)
    
    # Badges
    t_draw.rectangle([16, 16, 230, 46], fill=(240, 240, 240), outline=(180, 180, 180), width=1)
    t_draw.text((26, 24), "1. FOND BLANC (#FFFFFF)", fill=(20, 20, 20), font=font)
    
    t_draw.rectangle([528, 16, 760, 46], fill=(15, 23, 42), outline=(0, 240, 255), width=1)
    t_draw.text((538, 24), "2. STUDIO DARK (#0B0F17)", fill=(0, 240, 255), font=font)
    
    t_draw.rectangle([1040, 16, 1290, 46], fill=(15, 23, 42), outline=(52, 211, 153), width=1)
    t_draw.text((1050, 24), "3. CHROMA GREEN (#00FF00)", fill=(52, 211, 153), font=font)
    
    for p in [
        os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_idle_studio_trichroma_board.png"),
        os.path.join(BRAIN_DIRS[0], "aituko_idle_studio_trichroma_board.png"),
        os.path.join(BRAIN_DIRS[1], "aituko_idle_studio_trichroma_board.png")
    ]:
        trichroma.save(p, "PNG")
    print("   ✅ Trichroma Verification Board saved.")

    # 6. Build Master Presentation Board (1920x1080)
    print("🖼️ Step 7: Building Master 1080p Presentation Board...")
    from scripts.build_flawless_aituko_idle import build_presentation_board
    master_board = build_presentation_board(frames_dark, frames_rgba)
    for p in [
        os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_idle_master_board.png"),
        os.path.join(BRAIN_DIRS[0], "aituko_idle_master_board.png"),
        os.path.join(BRAIN_DIRS[1], "aituko_idle_master_board.png")
    ]:
        master_board.save(p, "PNG")
    print("   ✅ Master Presentation Board saved.")

    # 7. Package Zip Bundles
    print("📦 Step 8: Packaging ZIP bundles...")
    bundle_files = [
        "static.png", "static.webp", "animated.webp", "animated.gif",
        "animated_dark.gif", "animated_green.gif", "snippet.json",
        "looped_video.mp4", "preview_studio_green.mp4", "lottie.json",
        "aituko_idle_animated.svg", "aituko_idle_animated_transparent.svg"
    ]
    for td in TARGET_DIRS:
        zip_path = os.path.join(td, "bundle_aituko_00_idle.zip")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for bf in bundle_files:
                fp = os.path.join(td, bf)
                if os.path.exists(fp):
                    z.write(fp, bf)
        print(f"   ✅ Saved {zip_path}")

    # Update downloads zip archives
    starter_zip = os.path.join(WORKSPACE_DIR, "downloads/AItuko-Starter-Pack.zip")
    if os.path.exists(starter_zip):
        with zipfile.ZipFile(starter_zip, "a") as z:
            z.write(os.path.join(TARGET_DIRS[0], "lottie.json"), "00_idle/lottie.json")
            z.write(os.path.join(TARGET_DIRS[0], "animated.webp"), "00_idle/animated.webp")
            z.write(os.path.join(TARGET_DIRS[0], "animated.gif"), "00_idle/animated.gif")

    pro_zip = os.path.join(WORKSPACE_DIR, "downloads/AItuko-Pro-12-States.zip")
    if os.path.exists(pro_zip):
        with zipfile.ZipFile(pro_zip, "a") as z:
            z.write(os.path.join(TARGET_DIRS[0], "lottie.json"), "00_idle/lottie.json")
            z.write(os.path.join(TARGET_DIRS[0], "animated.webp"), "00_idle/animated.webp")
            z.write(os.path.join(TARGET_DIRS[0], "animated.gif"), "00_idle/animated.gif")
    print("   ✅ Downloads bundles updated.")

    # 8. Clean up temp folders
    print("🧹 Step 9: Cleaning up temp folders...")
    shutil.rmtree(os.path.join(WORKSPACE_DIR, "assets/00_idle/temp_dark_frames"), ignore_errors=True)
    shutil.rmtree(os.path.join(WORKSPACE_DIR, "assets/00_idle/temp_green_frames"), ignore_errors=True)
    print("   ✅ Cleanup complete.")

    # 9. Update Visual Artifacts
    print("📝 Step 10: Updating visual artifacts...")
    from scripts.build_flawless_aituko_idle import update_visual_artifacts
    update_visual_artifacts()
    print("🎉 ALL DELIVERABLES FULLY COMPILED AND READY!")

if __name__ == "__main__":
    run()
