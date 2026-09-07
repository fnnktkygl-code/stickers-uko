import bpy
import bmesh
import math
import os

def test():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.film_transparent = True
    scene.render.resolution_x = 512
    scene.render.resolution_y = 512
    
    if scene.world is None:
        scene.world = bpy.data.worlds.new("World")
    world = scene.world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs['Color'].default_value = (0.97, 0.91, 0.83, 1.0)
        bg.inputs['Strength'].default_value = 0.50

    # Camera
    bpy.ops.object.camera_add(location=(0.0, -10.0, 0.970), rotation=(math.radians(90), 0, 0))
    cam = bpy.context.active_object
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = 2.560
    scene.camera = cam

    # Lighting
    bpy.ops.object.light_add(type='AREA', location=(-2.6, -4.2, 3.2))
    key = bpy.context.active_object
    key.data.energy = 320
    key.data.size = 2.8
    key.data.color = (1.0, 0.94, 0.86)
    key.rotation_euler = (math.radians(52), math.radians(12), math.radians(-28))
    
    bpy.ops.object.light_add(type='AREA', location=(3.2, -3.6, 1.8))
    fill = bpy.context.active_object
    fill.data.energy = 160
    fill.data.size = 3.2
    fill.data.color = (0.98, 0.95, 0.92)
    fill.rotation_euler = (math.radians(48), math.radians(-18), math.radians(38))
    
    bpy.ops.object.light_add(type='AREA', location=(0.0, -1.0, -1.2))
    bounce = bpy.context.active_object
    bounce.data.energy = 70
    bounce.data.size = 3.2
    bounce.data.color = (0.98, 0.92, 0.84)
    bounce.rotation_euler = (math.radians(-90), 0, 0)

    # Eye Material with pupil shifted UP in Z
    mat = bpy.data.materials.new(name="Amber_Eye_Tuned")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    tc = nodes.new('ShaderNodeTexCoord')
    sep = nodes.new('ShaderNodeSeparateXYZ')
    links.new(tc.outputs['Object'], sep.inputs['Vector'])
    
    # X^2
    mul_x = nodes.new('ShaderNodeMath')
    mul_x.operation = 'MULTIPLY'
    links.new(sep.outputs['X'], mul_x.inputs[0])
    links.new(sep.outputs['X'], mul_x.inputs[1])
    
    # (Z - 0.045)^2
    sub_z = nodes.new('ShaderNodeMath')
    sub_z.operation = 'SUBTRACT'
    links.new(sep.outputs['Z'], sub_z.inputs[0])
    sub_z.inputs[1].default_value = 0.045
    
    mul_z = nodes.new('ShaderNodeMath')
    mul_z.operation = 'MULTIPLY'
    links.new(sub_z.outputs['Value'], mul_z.inputs[0])
    links.new(sub_z.outputs['Value'], mul_z.inputs[1])
    
    add_xz = nodes.new('ShaderNodeMath')
    add_xz.operation = 'ADD'
    links.new(mul_x.outputs['Value'], add_xz.inputs[0])
    links.new(mul_z.outputs['Value'], add_xz.inputs[1])
    
    rad = nodes.new('ShaderNodeMath')
    rad.operation = 'SQRT'
    links.new(add_xz.outputs['Value'], rad.inputs[0])
    
    div_norm = nodes.new('ShaderNodeMath')
    div_norm.operation = 'DIVIDE'
    links.new(rad.outputs['Value'], div_norm.inputs[0])
    div_norm.inputs[1].default_value = 0.165
    
    ramp = nodes.new('ShaderNodeValToRGB')
    # Pupil center: deep black-espresso
    ramp.color_ramp.elements[0].position = 0.40
    ramp.color_ramp.elements[0].color = (0.008, 0.004, 0.002, 1.0)
    
    # Deep amber ring
    elem1 = ramp.color_ramp.elements[1]
    elem1.position = 0.58
    elem1.color = (0.45, 0.16, 0.01, 1.0)
    
    # Vibrant golden amber iris
    elem2 = ramp.color_ramp.elements.new(0.78)
    elem2.color = (0.92, 0.50, 0.03, 1.0)
    
    # Brilliant golden caustic glow
    elem3 = ramp.color_ramp.elements.new(0.92)
    elem3.color = (1.0, 0.84, 0.26, 1.0)
    
    # Limbal dark ring
    elem4 = ramp.color_ramp.elements.new(0.99)
    elem4.color = (0.05, 0.02, 0.005, 1.0)
    
    links.new(div_norm.outputs['Value'], ramp.inputs['Fac'])
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = 0.02
    bsdf.inputs['IOR'].default_value = 1.54
    if 'Coat Weight' in bsdf.inputs:
        bsdf.inputs['Coat Weight'].default_value = 1.0
    elif 'Clearcoat' in bsdf.inputs:
        bsdf.inputs['Clearcoat'].default_value = 1.0
        
    if 'Emission Color' in bsdf.inputs:
        links.new(ramp.outputs['Color'], bsdf.inputs['Emission Color'])
        if 'Emission Strength' in bsdf.inputs:
            bsdf.inputs['Emission Strength'].default_value = 0.30
            
    out_node = nodes.new('ShaderNodeOutputMaterial')
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])

    # Porcelain Material
    mat_p = bpy.data.materials.new(name="Porcelain")
    mat_p.use_nodes = True
    bsdf_p = mat_p.node_tree.nodes.get("Principled BSDF")
    bsdf_p.inputs['Base Color'].default_value = (0.95, 0.88, 0.78, 1.0)
    bsdf_p.inputs['Roughness'].default_value = 0.22
    if 'Subsurface Weight' in bsdf_p.inputs:
        bsdf_p.inputs['Subsurface Weight'].default_value = 0.42
    if 'Coat Weight' in bsdf_p.inputs:
        bsdf_p.inputs['Coat Weight'].default_value = 0.70

    # Add Left Eye Sphere
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=0.165, location=(-0.305, -0.620, 1.450))
    eye = bpy.context.active_object
    eye.data.materials.append(mat)
    for p in eye.data.polygons:
        p.use_smooth = True

    # Upper Eyelid Hood (angled droop)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=0.165 * 1.03, location=(-0.305, -0.620, 1.450))
    hood = bpy.context.active_object
    bm = bmesh.new()
    bm.from_mesh(hood.data)
    to_delete = []
    for v in bm.verts:
        ang = math.atan2(v.co.y, v.co.x)
        # Angled curve: lower towards beak (inner side X > 0 in local space)
        cutoff = 0.005 - 0.020 * math.sin(ang) - 0.015 * v.co.x
        if v.co.z < cutoff:
            to_delete.append(v)
    bmesh.ops.delete(bm, geom=to_delete, context='VERTS')
    bm.to_mesh(hood.data)
    bm.free()
    hood.data.materials.append(mat_p)
    for p in hood.data.polygons:
        p.use_smooth = True
    solid = hood.modifiers.new(name="Solidify", type='SOLIDIFY')
    solid.thickness = 0.018
    solid.offset = 0.5
    subsurf = hood.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 1

    # Lower Eyelid Rim (cups the bottom of the eye)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=0.165 * 1.025, location=(-0.305, -0.620, 1.450))
    lower_rim = bpy.context.active_object
    bm = bmesh.new()
    bm.from_mesh(lower_rim.data)
    to_del_low = [v for v in bm.verts if v.co.z > -0.110 or v.co.y > 0.0]
    bmesh.ops.delete(bm, geom=to_del_low, context='VERTS')
    bm.to_mesh(lower_rim.data)
    bm.free()
    lower_rim.data.materials.append(mat_p)
    for p in lower_rim.data.polygons:
        p.use_smooth = True
    solid_low = lower_rim.modifiers.new(name="Solidify", type='SOLIDIFY')
    solid_low.thickness = 0.016
    solid_low.offset = 0.5
    subsurf_low = lower_rim.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf_low.levels = 1

    # Glint
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.016, location=(-0.335, -0.780, 1.490))
    glint = bpy.context.active_object
    glint_mat = bpy.data.materials.new(name="Glint")
    glint_mat.use_nodes = True
    bsdf_g = glint_mat.node_tree.nodes.get("Principled BSDF")
    bsdf_g.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
    if 'Emission Color' in bsdf_g.inputs:
        bsdf_g.inputs['Emission Color'].default_value = (1.0, 1.0, 1.0, 1.0)
        bsdf_g.inputs['Emission Strength'].default_value = 5.0
    glint.data.materials.append(glint_mat)

    # Render
    out_png = os.path.abspath("scratch/test_eye_tuned2.png")
    scene.render.filepath = out_png
    bpy.ops.render.render(write_still=True)
    print("Rendered:", out_png)

if __name__ == "__main__":
    test()
