import json, copy, os

# Load fragment
with open('scratch/owluko_waving.scene.json') as f:
    frag = json.load(f)

print(f"Loaded {len(frag['shapes'])} base shapes from fragment.")

# Mirror wing function
def mirror_shape(s, new_id):
    s = copy.deepcopy(s)
    s['id'] = new_id
    dx = s['x'] - 512
    s['x'] = 512 - dx
    for sp in s.get('subpaths', []):
        for pt in sp.get('points', []):
            pt['x'] = -pt['x']
            if 'cubic' in pt:
                c = pt['cubic']
                c['rotation'] = 180.0 - c['rotation']
                c['inRotation'] = 180.0 - c['inRotation']
    if 'fill' in s and 'gradient' in s['fill']:
        g = s['fill']['gradient']
        if 'start' in g:
            g['start']['x'] = -g['start']['x']
        if 'end' in g:
            g['end']['x'] = -g['end']['x']
    return s

# Create mirrored left wave wing
r_wave = next(s for s in frag['shapes'] if s['id'] == 'owluko_wave_wing_wave_smooth_main')
l_wave = mirror_shape(r_wave, 'owluko_wave_wing_wave_l_main')

print("Mirrored left wing ready.")
