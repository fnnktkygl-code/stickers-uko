import sys, re
sys.path.append('.')
from scratch.tune_masterpiece import test_svg_content, base_svg

best_le_de = 999
best_params = None

# Left eye variations
for x_top_l in [168.5, 169]:
    for x_bot_l in [167, 168]:
        for y_bot in [179.5, 180]:
            for x_bot_r in [223, 223.5]:
                le_bowl = f"M {x_top_l} 142 C {x_bot_l} 150, {x_bot_l} 158, 172 166 C 178 174, 186 {y_bot}, 195.5 {y_bot} C 205 {y_bot}, 213 174, 219 166 C {x_bot_r} 158, {x_bot_r} 150, 223 143 C 210 140.5, 180 140.5, {x_top_l} 142 Z"
                s = re.sub(r'<path d=\"M 169 142 L 169 158.*?>', f'<path d=\"{le_bowl}\" fill=\"url(#amberEyeL)\" />', base_svg)
                res = test_svg_content(s)
                if res['le_de'] < best_le_de:
                    best_le_de = res['le_de']
                    best_params = (x_top_l, x_bot_l, y_bot, x_bot_r)
                    print(f"New best LE: {best_le_de:.3f} with params={best_params}")

print("Final best LE DE:", best_le_de, "params:", best_params)
