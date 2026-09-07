import os
import glob
import subprocess
from PIL import Image
from process_all_luneko_states import key_luneko_ultimate

raw_mp4 = "preview/test_veo_aituko_idea_cyan.mp4"
looped_mp4 = "preview/test_aituko_idea_looped.mp4"
temp_dir = "preview/temp_idea_frames"
os.makedirs(temp_dir, exist_ok=True)

# 1. Ping-pong loop
subprocess.run([
    "ffmpeg", "-y", "-t", "2.0", "-i", raw_mp4,
    "-filter_complex", "[0:v]split[v1][v2];[v2]reverse[v2rev];[v1][v2rev]concat=n=2:v=1[v]",
    "-map", "[v]", "-r", "24", "-c:v", "libx264", "-pix_fmt", "yuv420p", looped_mp4
], check=True)

# 2. Extract frames
for f in glob.glob(f"{temp_dir}/*"):
    os.remove(f)
subprocess.run([
    "ffmpeg", "-y", "-i", looped_mp4,
    "-vf", "crop=720:720:280:0,fps=24,scale=512:512",
    f"{temp_dir}/f_%03d.png"
], check=True)

# 3. Matte frames
raw_frames = sorted(glob.glob(f"{temp_dir}/f_*.png"))
clean_frames = [key_luneko_ultimate(Image.open(rf)) for rf in raw_frames]

# 4. Save preview static & animated gif
clean_frames[min(20, len(clean_frames)-1)].save("preview/aituko_idea_preview_static.png")

gif_frames = []
for f in clean_frames:
    alpha = f.split()[3]
    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
    p_frame = f.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE)
    p_frame.paste(255, mask)
    p_frame.info['transparency'] = 255
    gif_frames.append(p_frame)
gif_frames[0].save("preview/aituko_idea_preview.gif", save_all=True, append_images=gif_frames[1:], duration=41, loop=0, disposal=2)

print("Saved preview/aituko_idea_preview_static.png and preview/aituko_idea_preview.gif!")
