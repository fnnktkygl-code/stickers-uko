import json

with open('mascots/owluko/owluko_pure_vector.scene.json') as f:
    scene = json.load(f)

# Let's check the points of each shape around global (780, 680)
# Remember: shape points are relative to parent group!
# Global origin of groups:
# root: (512, 876)
# body_group: (512, 498)
# wing_r_wave_group: (770, 560)
# wing_r_rest_group: (806, 498)

# Check wing_wave_smooth_main:
# Relative to wing_r_wave_group (770, 560):
for s in scene['shapes']:
    if s['id'] in ['owluko_wave_wing_wave_smooth_main', 'owluko_wave_wing_right_main', 'owluko_wave_body_silhouette']:
        print(s['id'], "parent:", s.get('parent'))
        pts = s.get('points', [])
        # Find points near local corresponding to global (780, 680)
        # If parent is wing_r_wave_group (770, 560), local is (10, 120)
        # If parent is body_group (512, 498), local is (268, 182)
        for i, p in enumerate(pts):
            print(f"  pt {i}: ({p['x']:.1f}, {p['y']:.1f})")
