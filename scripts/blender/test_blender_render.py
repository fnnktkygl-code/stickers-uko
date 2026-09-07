import bpy
import os

# Reset scene
bpy.ops.wm.read_factory_settings(use_empty=True)

scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'GPU'
scene.render.film_transparent = True
scene.render.resolution_x = 512
scene.render.resolution_y = 512

# Enable Metal
prefs = bpy.context.preferences
cpref = prefs.addons['cycles'].preferences
cpref.compute_device_type = 'METAL'
cpref.get_devices()
for d in cpref.devices:
    d.use = (d.type == 'METAL')

# Add camera
bpy.ops.object.camera_add(location=(0, -4, 0), rotation=(1.5708, 0, 0))
cam = bpy.context.active_object
scene.camera = cam

# Add light
bpy.ops.object.light_add(type='AREA', location=(2, -3, 3))
light = bpy.context.active_object
light.data.energy = 200
light.data.size = 2.0

# Add a smooth sphere
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 0, 0))
sphere = bpy.context.active_object
bpy.ops.object.modifier_add(type='SUBSURF')
sphere.modifiers["Subdivision"].levels = 2
bpy.ops.object.shade_smooth()

# Add porcelain material
mat = bpy.data.materials.new(name="Porcelain")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs['Base Color'].default_value = (0.95, 0.92, 0.88, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.18
    for input_name in ['Subsurface Weight', 'Subsurface']:
        if input_name in bsdf.inputs:
            bsdf.inputs[input_name].default_value = 0.15
            break
sphere.data.materials.append(mat)

# Render
out_path = os.path.abspath("scratch/test_blender_sphere.png")
scene.render.filepath = out_path
scene.cycles.samples = 32
bpy.ops.render.render(write_still=True)
print(f"Rendered test sphere to {out_path}")
