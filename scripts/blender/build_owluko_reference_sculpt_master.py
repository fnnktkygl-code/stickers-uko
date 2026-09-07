import bpy
import bmesh
import math
import os
import json
import numpy as np

def reset_blender_scene():
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
        # Warm golden cream studio ambient bounce
        bg.inputs['Color'].default_value = (0.97, 0.91, 0.83, 1.0)
        bg.inputs['Strength'].default_value = 0.50
    return scene

def create_porcelain_material(name="Porcelain_Ivory", base_linear=(0.95, 0.88, 0.78), roughness=0.22):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*base_linear, 1.0)
        bsdf.inputs['Roughness'].default_value = roughness
        if 'Subsurface Weight' in bsdf.inputs:
            bsdf.inputs['Subsurface Weight'].default_value = 0.42
        elif 'Subsurface' in bsdf.inputs:
            bsdf.inputs['Subsurface'].default_value = 0.42
            
        if 'Subsurface Radius' in bsdf.inputs:
            bsdf.inputs['Subsurface Radius'].default_value = (1.0, 0.72, 0.48)
        if 'Coat Weight' in bsdf.inputs:
            bsdf.inputs['Coat Weight'].default_value = 0.70
        elif 'Clearcoat' in bsdf.inputs:
            bsdf.inputs['Clearcoat'].default_value = 0.70
        if 'Coat Roughness' in bsdf.inputs:
            bsdf.inputs['Coat Roughness'].default_value = 0.06
        elif 'Clearcoat Roughness' in bsdf.inputs:
            bsdf.inputs['Clearcoat Roughness'].default_value = 0.06
    return mat

def create_beak_material():
    return create_porcelain_material(name="Beak_Porcelain", base_linear=(0.86, 0.69, 0.52), roughness=0.24)

def create_feet_material():
    return create_porcelain_material(name="Feet_Bisque", base_linear=(0.68, 0.53, 0.41), roughness=0.28)

def create_concentric_amber_eye_material():
    mat = bpy.data.materials.new(name="Amber_Eye_Concentric")
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
    
    # (Z - 0.035)^2 -> Shift pupil UP under sleepy eyelid
    sub_z = nodes.new('ShaderNodeMath')
    sub_z.operation = 'SUBTRACT'
    links.new(sep.outputs['Z'], sub_z.inputs[0])
    sub_z.inputs[1].default_value = 0.035
    
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
    div_norm.inputs[1].default_value = 0.145
    
    ramp = nodes.new('ShaderNodeValToRGB')
    # Pupil center: deep dark espresso
    ramp.color_ramp.elements[0].position = 0.42
    ramp.color_ramp.elements[0].color = (0.008, 0.004, 0.002, 1.0)
    
    # Deep cognac amber transition
    elem1 = ramp.color_ramp.elements[1]
    elem1.position = 0.60
    elem1.color = (0.46, 0.18, 0.01, 1.0)
    
    # Vibrant rich golden amber iris
    elem2 = ramp.color_ramp.elements.new(0.80)
    elem2.color = (0.92, 0.50, 0.04, 1.0)
    
    # Luminous golden caustic glow
    elem3 = ramp.color_ramp.elements.new(0.93)
    elem3.color = (1.0, 0.85, 0.30, 1.0)
    
    # Deep espresso eyeliner rim
    elem4 = ramp.color_ramp.elements.new(0.99)
    elem4.color = (0.06, 0.02, 0.01, 1.0)
    
    links.new(div_norm.outputs['Value'], ramp.inputs['Fac'])
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = 0.02
    bsdf.inputs['IOR'].default_value = 1.52
    if 'Coat Weight' in bsdf.inputs:
        bsdf.inputs['Coat Weight'].default_value = 1.0
    elif 'Clearcoat' in bsdf.inputs:
        bsdf.inputs['Clearcoat'].default_value = 1.0
        
    if 'Emission Color' in bsdf.inputs:
        links.new(ramp.outputs['Color'], bsdf.inputs['Emission Color'])
        if 'Emission Strength' in bsdf.inputs:
            bsdf.inputs['Emission Strength'].default_value = 0.25
            
    out_node = nodes.new('ShaderNodeOutputMaterial')
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])
    return mat

def build_owluko_body(porcelain_mat, json_path="scratch/owluko_clean_body_slices.json"):
    with open(json_path, "r") as f:
        slices = json.load(f)
        
    num_sectors = 64
    
    # Filter slices: from crown (Y=40) to pelvis end (Y=416)
    body_slices = [s for s in slices if s['y'] <= 416]
    
    top_z = 2.050
    cx_top = 0.0
    cy_top = (slices[0]['p_center_px'] - 248.0) * 0.005
    
    mesh = bpy.data.meshes.new("Owluko_Body")
    bm = bmesh.new()
    
    v_top = bm.verts.new((cx_top, cy_top, top_z))
    
    ring_verts = []
    for s_data in body_slices:
        z = s_data['z_3d']
        
        # Front dimensions
        rx = (s_data['f_width_px'] / 2.0) * 0.005
        cx = (s_data['f_center_px'] - 256.0) * 0.005
        
        # Profile dimensions
        p_mid = s_data['p_center_px']
        cy = (p_mid - 248.0) * 0.005
        ry_front = (p_mid - s_data['p_front_px']) * 0.005
        ry_back = (s_data['p_back_px'] - p_mid) * 0.005
        
        cur = []
        for s in range(num_sectors):
            angle = 2.0 * math.pi * s / num_sectors
            vx = cx + rx * math.sin(angle)
            
            cos_a = math.cos(angle)
            if cos_a <= 0.0:
                vy = cy + ry_front * cos_a
            else:
                vy = cy + ry_back * cos_a
                
            cur.append(bm.verts.new((vx, vy, z)))
        ring_verts.append(cur)
        
    # Pelvic bottom cap pole
    last_s = body_slices[-1]
    bot_z = last_s['z_3d'] - 0.04
    bot_cx = (last_s['f_center_px'] - 256.0) * 0.005
    bot_cy = (last_s['p_center_px'] - 248.0) * 0.005
    v_bot = bm.verts.new((bot_cx, bot_cy, bot_z))
    
    # Top fan
    for s in range(num_sectors):
        s_next = (s + 1) % num_sectors
        bm.faces.new((v_top, ring_verts[0][s], ring_verts[0][s_next]))
        
    # Body quads
    for r in range(len(ring_verts) - 1):
        for s in range(num_sectors):
            s_next = (s + 1) % num_sectors
            v1 = ring_verts[r][s]
            v2 = ring_verts[r][s_next]
            v3 = ring_verts[r + 1][s_next]
            v4 = ring_verts[r + 1][s]
            bm.faces.new((v1, v2, v3, v4))
            
    # Bottom fan
    for s in range(num_sectors):
        s_next = (s + 1) % num_sectors
        bm.faces.new((ring_verts[-1][s_next], ring_verts[-1][s], v_bot))
        
    bm.to_mesh(mesh)
    bm.free()
    
    obj = bpy.data.objects.new("Owluko_Body", mesh)
    bpy.context.collection.objects.link(obj)
    
    for poly in mesh.polygons:
        poly.use_smooth = True
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2
    
    obj.data.materials.append(porcelain_mat)
    return obj

def build_owluko_eyes(eye_mat, porcelain_mat):
    # Left eye: X = -0.315, Z = 1.455
    # Right eye: X = +0.295, Z = 1.435
    # Recessed depth: Y = -0.500 (radius 0.145, cornea apex at Y = -0.645)
    eyes = []
    eye_radius = 0.145
    
    configs = [
        ('Left', -0.315, 1.455),
        ('Right', 0.295, 1.435)
    ]
    
    for side, cx, cz in configs:
        # 1. Eyeball Sphere
        bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=eye_radius, location=(cx, -0.500, cz))
        eyeball = bpy.context.active_object
        eyeball.name = f"Eye_{side}_Ball"
        eyeball.data.materials.append(eye_mat)
        for poly in eyeball.data.polygons:
            poly.use_smooth = True
            
        # 2. Sleek Porcelain Upper Eyelid Hood (covering top ~45% of eyeball with smooth downward curve)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=eye_radius * 1.035, location=(cx, -0.500, cz))
        hood = bpy.context.active_object
        hood.name = f"Eye_{side}_Hood"
        
        bm = bmesh.new()
        bm.from_mesh(hood.data)
        to_delete = []
        for v in bm.verts:
            ang = math.atan2(v.co.y, v.co.x)
            # Organic droop
            cutoff = -0.010 - 0.012 * math.cos(ang)
            if v.co.z < cutoff:
                to_delete.append(v)
        bmesh.ops.delete(bm, geom=to_delete, context='VERTS')
        bm.to_mesh(hood.data)
        bm.free()
        
        hood.data.materials.append(porcelain_mat)
        for poly in hood.data.polygons:
            poly.use_smooth = True
            
        solid = hood.modifiers.new(name="Solidify", type='SOLIDIFY')
        solid.thickness = 0.016
        solid.offset = 0.5
        
        subsurf = hood.modifiers.new(name="Subdivision", type='SUBSURF')
        subsurf.levels = 1
        
        # 3. Specular Glint Sphere (crisp white studio reflection)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.015, location=(cx - 0.030, -0.645, cz + 0.025))
        glint = bpy.context.active_object
        glint.name = f"Eye_{side}_Glint"
        glint_mat = bpy.data.materials.new(name=f"Glint_{side}")
        glint_mat.use_nodes = True
        bsdf_g = glint_mat.node_tree.nodes.get("Principled BSDF")
        bsdf_g.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
        if 'Emission Color' in bsdf_g.inputs:
            bsdf_g.inputs['Emission Color'].default_value = (1.0, 1.0, 1.0, 1.0)
            if 'Emission Strength' in bsdf_g.inputs:
                bsdf_g.inputs['Emission Strength'].default_value = 5.0
        glint.data.materials.append(glint_mat)
        
        eyes.extend([eyeball, hood, glint])
    return eyes

def build_owluko_beak(beak_mat):
    # Plump rounded teardrop seed beak nestled between the eyes
    # Top base at Z = 1.425, tip at Z = 1.075
    z_mid = (1.425 + 1.075) / 2.0
    depth = 1.425 - 1.075 # 0.350
    bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=0.075, radius2=0.022, depth=depth, location=(0.0, -0.600, z_mid))
    beak = bpy.context.active_object
    beak.name = "Owluko_Beak"
    beak.rotation_euler = (math.radians(168), 0, 0)
    beak.scale = (1.25, 1.40, 1.0)
    for poly in beak.data.polygons:
        poly.use_smooth = True
    subsurf = beak.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    beak.data.materials.append(beak_mat)
    return beak

def build_owluko_wings(porcelain_mat):
    # Smooth teardrop wings nestled against the flanks matching the profile view!
    wings = []
    for side, cx, sgn in [('Left', -0.64, -1.0), ('Right', 0.64, 1.0)]:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.18, location=(cx, 0.08, 0.92))
        wing = bpy.context.active_object
        wing.name = f"Wing_{side}"
        wing.scale = (0.35, 1.20, 2.05)
        wing.rotation_euler = (math.radians(15), sgn * math.radians(-7), sgn * math.radians(5))
        for poly in wing.data.polygons:
            poly.use_smooth = True
        subsurf = wing.modifiers.new(name="Subdivision", type='SUBSURF')
        subsurf.levels = 1
        wing.data.materials.append(porcelain_mat)
        wings.append(wing)
    return wings

def build_owluko_legs_and_feet(feet_mat):
    # Calibrated from clean turnaround views:
    # Left foot center X = -0.275 (px 201), Right foot center X = +0.285 (px 313)
    elements = []
    for side, cx in [('Left', -0.275), ('Right', 0.285)]:
        # 1. Smooth Tapering Leg Shank
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.078, depth=0.22, location=(cx, -0.05, 0.02))
        shank = bpy.context.active_object
        shank.name = f"Leg_{side}_Shank"
        shank.scale = (1.0, 1.15, 1.0)
        shank.data.materials.append(feet_mat)
        for poly in shank.data.polygons:
            poly.use_smooth = True
        subsurf = shank.modifiers.new(name="Subdivision", type='SUBSURF')
        subsurf.levels = 1
        elements.append(shank)
        
        # 2. Foot Ankle Base
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.076, location=(cx, -0.08, -0.08))
        ankle = bpy.context.active_object
        ankle.name = f"Foot_{side}_Ankle"
        ankle.scale = (1.10, 1.25, 0.85)
        ankle.data.materials.append(feet_mat)
        for poly in ankle.data.polygons:
            poly.use_smooth = True
        subsurf = ankle.modifiers.new(name="Subdivision", type='SUBSURF')
        subsurf.levels = 1
        elements.append(ankle)
        
        # 3. Three Grounded Rounded Toes (Resting on baseline Z = -0.195)
        toes_config = [
            (-20, -0.050, 0.008, 0.170),
            (0,    0.000, 0.000, 0.210),
            (20,   0.050, 0.008, 0.165)
        ]
        for t_idx, (angle, dx, dz, length) in enumerate(toes_config):
            bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.046, location=(cx + dx, -0.19, -0.168 + dz))
            toe = bpy.context.active_object
            toe.name = f"Foot_{side}_Toe_{t_idx}"
            toe.scale = (1.0, length / 0.046, 0.82)
            rot = angle if side == 'Right' else -angle
            toe.rotation_euler = (0, 0, math.radians(rot))
            for poly in toe.data.polygons:
                poly.use_smooth = True
            subsurf_t = toe.modifiers.new(name="Subdivision", type='SUBSURF')
            subsurf_t.levels = 1
            toe.data.materials.append(feet_mat)
            elements.append(toe)
            
    return elements

def setup_lighting():
    # Warm golden key (upper-left)
    bpy.ops.object.light_add(type='AREA', location=(-2.6, -4.2, 3.2))
    key = bpy.context.active_object
    key.name = "Key_Light"
    key.data.energy = 320
    key.data.size = 2.8
    key.data.color = (1.0, 0.94, 0.86)
    key.rotation_euler = (math.radians(52), math.radians(12), math.radians(-28))
    
    # Fill Light (right)
    bpy.ops.object.light_add(type='AREA', location=(3.2, -3.6, 1.8))
    fill = bpy.context.active_object
    fill.name = "Fill_Light"
    fill.data.energy = 160
    fill.data.size = 3.2
    fill.data.color = (0.98, 0.95, 0.92)
    fill.rotation_euler = (math.radians(48), math.radians(-18), math.radians(38))
    
    # Rim Light (back-top)
    bpy.ops.object.light_add(type='AREA', location=(0.0, 3.2, 3.2))
    rim = bpy.context.active_object
    rim.name = "Rim_Light"
    rim.data.energy = 220
    rim.data.size = 2.2
    rim.data.color = (1.0, 0.94, 0.86)
    rim.rotation_euler = (math.radians(-50), 0, math.radians(180))
    
    # Under-Bounce Light
    bpy.ops.object.light_add(type='AREA', location=(0.0, -1.0, -1.2))
    bounce = bpy.context.active_object
    bounce.name = "Bounce_Light"
    bounce.data.energy = 70
    bounce.data.size = 3.2
    bounce.data.color = (0.98, 0.92, 0.84)
    bounce.rotation_euler = (math.radians(-90), 0, 0)

def setup_camera():
    bpy.ops.object.camera_add(location=(0.0, -10.0, 0.970), rotation=(math.radians(90), 0, 0))
    cam = bpy.context.active_object
    cam.name = "Camera_Front_Ortho"
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = 2.560
    bpy.context.scene.camera = cam
    return cam

def main():
    scene = reset_blender_scene()
    
    porcelain_mat = create_porcelain_material()
    eye_mat = create_concentric_amber_eye_material()
    beak_mat = create_beak_material()
    feet_mat = create_feet_material()
    
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = "Owluko_Rig_Root"
    
    body = build_owluko_body(porcelain_mat)
    wings = build_owluko_wings(porcelain_mat)
    eyes = build_owluko_eyes(eye_mat, porcelain_mat)
    beak = build_owluko_beak(beak_mat)
    legs_and_feet = build_owluko_legs_and_feet(feet_mat)
    
    all_objs = [body, beak] + wings + eyes + legs_and_feet
    for obj in all_objs:
        obj.parent = root
        
    setup_lighting()
    cam = setup_camera()
    
    out_dir = os.path.abspath("scratch/owluko_clean_sculpt")
    os.makedirs(out_dir, exist_ok=True)
    
    # 4 Turnaround Angles (0°, 45°, 90°, 180°)
    angles = [
        ("front_000", 0.0),
        ("three_quarter_045", 45.0),
        ("profile_090", 90.0),
        ("back_180", 180.0)
    ]
    
    for name, deg in angles:
        root.rotation_euler = (0, 0, math.radians(-deg))
        out_path = os.path.join(out_dir, f"owluko_{name}.png")
        scene.render.filepath = out_path
        bpy.ops.render.render(write_still=True)
        print(f"Rendered {name}: {out_path}")
        
    # Export Draco GLB
    glb_out = os.path.abspath("mascots/owluko/owluko_3d_master.glb")
    root.rotation_euler = (0, 0, 0)
    bpy.ops.export_scene.gltf(filepath=glb_out, export_draco_mesh_compression_enable=True)
    print(f"Exported Draco GLB: {glb_out}")

if __name__ == "__main__":
    main()
