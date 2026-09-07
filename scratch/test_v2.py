import sys
sys.path.append(".")
from scripts.benchmark_owluko_fidelity import render_svg, evaluate_fidelity

with open("scratch/owluko_body_path_131.txt", "r") as f:
    body_d = f.read().strip()

with open("scratch/test_owluko_calibrated.svg", "r") as f:
    lines = f.readlines()

new_lines = []
for l in lines:
    if l.strip().startswith('<path') and 'fill="url(#bodyGrad)"' in l:
        new_lines.append(f'  <path d="{body_d}" fill="url(#bodyGrad)" />\n')
    else:
        new_lines.append(l)

with open("scratch/test_owluko_calibrated_v2.svg", "w") as f:
    f.writelines(new_lines)

out_png = render_svg("scratch/test_owluko_calibrated_v2.svg", "scratch/test_owluko_v2.png")
res = evaluate_fidelity(out_png)
