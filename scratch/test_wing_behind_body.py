import json

with open('mascots/owluko/owluko_pure_vector.scene.json') as f:
    scene = json.load(f)

shapes = scene['shapes']

# Find wing_wave shapes and move them right before body_silhouette
wave_shapes = [s for s in shapes if 'wing_wave' in s['id']]
other_shapes = [s for s in shapes if 'wing_wave' not in s['id']]

body_idx = 0
for i, s in enumerate(other_shapes):
    if s['id'] == 'owluko_wave_body_silhouette':
        body_idx = i
        break

new_shapes = other_shapes[:body_idx] + wave_shapes + other_shapes[body_idx:]
scene['shapes'] = new_shapes

with open('scratch/scene_test_behind.json', 'w') as f:
    json.dump(scene, f, indent=2)

print("Saved scratch/scene_test_behind.json with wave wing behind body.")
