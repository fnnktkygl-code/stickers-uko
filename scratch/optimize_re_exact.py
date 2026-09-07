import sys, re
sys.path.append('.')
from scratch.tune_masterpiece import test_svg_content, base_svg

# Base with winning LE, Forehead, Beak
with open('scratch/test_integrated_masterpiece.svg', 'r') as f:
    s = f.read()

# Apply winning LE
le_bowl = "M 169 142 C 168 150, 168 158, 172 166 C 178 174, 186 180, 195.5 180 C 205 180, 213 174, 219 166 C 223.5 158, 223.5 150, 223 143 C 210 140.5, 180 140.5, 169 142 Z"
s = re.sub(r'<path d=\"M 168\.5 142.*?>', f'<path d=\"{le_bowl}\" fill=\"url(#amberEyeL)\" />', s)

# Forehead op=0.30, col=#846C5A
new_brow = '''    <!-- Soft Right Brow Ambient Falloff (Warm porcelain tone, natural cranial shading) -->
    <radialGradient id=\"rBrowSoft\" cx=\"50%\" cy=\"50%\" r=\"50%\">
      <stop offset=\"0%\" stop-color=\"#846C5A\" stop-opacity=\"0.30\" />
      <stop offset=\"70%\" stop-color=\"#846C5A\" stop-opacity=\"0.11\" />
      <stop offset=\"100%\" stop-color=\"#846C5A\" stop-opacity=\"0\" />
    </radialGradient>'''
s = re.sub(r'    <!-- Soft Right Brow Ambient Falloff.*?    </radialGradient>', new_brow, s, flags=re.DOTALL)

best_re_de = 999
best_params = None

for x_top_l in [281, 281.5]:
    for x_bot_l in [280.5, 281, 281.5]:
        for y_bot in [179.5, 180, 180.5]:
            for x_bot_r in [339.5, 340, 340.5]:
                re_bowl = f"M {x_top_l} 143.5 C {x_bot_l} 150, {x_bot_l} 158, 285 166 C 291 174, 299 {y_bot}, 310.5 {y_bot} C 319 {y_bot}, 327 174, 333 166 C {x_bot_r} 158, {x_bot_r} 150, 340 142 C 326 140.5, 296 140.5, {x_top_l} 143.5 Z"
                s_test = re.sub(r'<path d=\"M 281 143\.5.*?>', f'<path d=\"{re_bowl}\" fill=\"url(#amberEyeR)\" />', s)
                res = test_svg_content(s_test)
                if res['re_de'] < best_re_de:
                    best_re_de = res['re_de']
                    best_params = (x_top_l, x_bot_l, y_bot, x_bot_r)
                    print(f"New best RE: {best_re_de:.3f} with params={best_params}, face_de={res['face_de']:.2f}, global_de={res['global_de']:.2f}")

print("Final best RE DE:", best_re_de, "params:", best_params)
