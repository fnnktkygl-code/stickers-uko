import re

with open("scripts/build_owluko_user_exact_rive.js", "r") as f:
    content = f.read()

# Remove stroke from eyelid_l_cover
old_cover = '''      points: eyelidCoverPoints,
      opacity: 0,
      fill: { color: "#FAF6EE" },
      stroke: { color: "#5C3D2E", thickness: 3.5, cap: "round", join: "round" }'''

new_cover = '''      points: eyelidCoverPoints,
      opacity: 0,
      fill: { color: "#FAF6EE" }'''

content = content.replace(old_cover, new_cover)

with open("scripts/build_owluko_user_exact_rive.js", "w") as f:
    f.write(content)
print("Updated build_owluko_user_exact_rive.js")
