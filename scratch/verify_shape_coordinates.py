import json

with open('scratch/owluko_waving.scene.json') as f:
    scene = json.load(f)

# Global group centers:
# root: (512, 876)
# shadow_group: (512, 876)
# feet_group: (512, 876)
# body_group: (512, 498)
# wings_group: (512, 498)
# wing_l_group: (218, 498)
# wing_r_rest_group: (806, 498)
# wing_r_wave_group: (770, 560)
# belly_group: (512, 498)
# head_group: (512, 372)
# eye_l_group: (398, 362)
# eye_r_group: (626, 362)
# beak_group: (512, 416)

groups = {
    "root": (512, 876),
    "shadow_group": (512, 876),
    "feet_group": (512, 876),
    "body_group": (512, 498),
    "wings_group": (512, 498),
    "wing_l_group": (218, 498),
    "wing_r_rest_group": (806, 498),
    "wing_r_wave_group": (770, 560),
    "belly_group": (512, 498),
    "head_group": (512, 372),
    "eye_l_group": (398, 362),
    "eye_r_group": (626, 362),
    "beak_group": (512, 416)
}

print("Groups defined successfully.")
