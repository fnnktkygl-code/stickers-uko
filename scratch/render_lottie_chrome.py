import os
import sys
import json
import subprocess

def render_lottie_at_frame(json_path, frame_idx, output_png):
    with open(json_path, 'r', encoding='utf-8') as f:
        anim_data = json.load(f)

    html_content = f"""<!DOCTYPE html>
<html>
<head>
<script src="{os.path.abspath('scratch/lottie.min.js')}"></script>
<style>
  body, html {{ margin: 0; padding: 0; width: 512px; height: 512px; overflow: hidden; background: #0B0F17; }}
  #container {{ width: 512px; height: 512px; }}
</style>
</head>
<body>
<div id="container"></div>
<script>
  window.addEventListener('DOMContentLoaded', () => {{
    const anim = lottie.loadAnimation({{
      container: document.getElementById('container'),
      renderer: 'svg',
      loop: false,
      autoplay: false,
      animationData: {json.dumps(anim_data)}
    }});
    anim.addEventListener('DOMLoaded', () => {{
      anim.goToAndStop({frame_idx}, true);
      document.title = 'READY';
    }});
  }});
</script>
</body>
</html>"""

    html_file = f"scratch/render_tmp_{frame_idx}.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    chrome_cmd = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        "--window-size=512,512",
        f"--screenshot={output_png}",
        os.path.abspath(html_file)
    ]
    subprocess.run(chrome_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(html_file):
        os.remove(html_file)

if __name__ == "__main__":
    json_p = sys.argv[1]
    f_idx = int(sys.argv[2])
    out_p = sys.argv[3]
    render_lottie_at_frame(json_p, f_idx, out_p)
    print(f"Rendered frame {f_idx} to {out_p}")
