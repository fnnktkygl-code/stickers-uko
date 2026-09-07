with open("scripts/blender/build_owluko_3d.py", "r") as f:
    code = f.read()

target = """    # Warm studio ambient bounce
    world = scene.world
    world.use_nodes = True"""

replacement = """    # Warm studio ambient bounce
    if scene.world is None:
        scene.world = bpy.data.worlds.new("World")
    world = scene.world
    world.use_nodes = True"""

code = code.replace(target, replacement)
with open("scripts/blender/build_owluko_3d.py", "w") as f:
    f.write(code)
print("Fixed world initialization.")
