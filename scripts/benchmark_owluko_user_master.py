import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def render_svg_1024(svg_path, out_png):
    abs_svg = os.path.abspath(svg_path)
    abs_out = os.path.abspath(out_png)
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ width: 1024px; height: 1024px; background: transparent; overflow: hidden; }}
  img {{ width: 1024px; height: 1024px; display: block; }}
</style>
</head>
<body>
  <img src="file://{abs_svg}" />
</body>
</html>"""
    html_path = "scratch/render_1024_tmp.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    abs_html = os.path.abspath(html_path)

    cmd = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--screenshot={abs_out}",
        "--window-size=1024,1024",
        "--default-background-color=00000000",
        f"file://{abs_html}"
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Rendered SVG to {out_png}")

def make_comparison_board(ref_path, render_path, out_board):
    ref_img = Image.open(ref_path).convert("RGBA")
    render_img = Image.open(render_path).convert("RGBA")
    
    # Target size: 2120 x 1140
    board = Image.new("RGBA", (2100, 1140), (20, 22, 28, 255))
    draw = ImageDraw.Draw(board)
    
    # Paste reference and render
    board.paste(ref_img, (20, 90), ref_img)
    board.paste(render_img, (1060, 90), render_img)
    
    # Draw headers & labels
    draw.text((24, 24), "OWLUKO CANONICAL BENCHMARK : REFERENCE UTILISATEUR VS NOUVEAU MODELE VECTORIEL PUR", fill=(255, 255, 255))
    draw.text((30, 65), "1. IMAGE MASTER UTILISATEUR (media_1788762027946.png)", fill=(245, 158, 11))
    draw.text((1070, 65), "2. MODELE VECTORIEL RECONSTRUIT (scratch/owluko_user_exact_master.svg)", fill=(56, 189, 248))
    
    # Add subtle border around images
    draw.rectangle([(19, 89), (1045, 1115)], outline=(60, 65, 80), width=1)
    draw.rectangle([(1059, 89), (2085, 1115)], outline=(60, 65, 80), width=1)
    
    board.save(out_board, "PNG")
    print(f"Saved side-by-side board at {out_board}")

if __name__ == "__main__":
    render_svg_1024("scratch/owluko_user_exact_master.svg", "scratch/owluko_user_exact_master.png")
    make_comparison_board("mascots/owluko/owluko_user_master_ref.png", "scratch/owluko_user_exact_master.png", "scratch/owluko_user_exact_comp_board.png")
