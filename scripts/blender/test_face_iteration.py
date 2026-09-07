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
        bg.inputs['Color'].default_value = (0.97, 0.91, 0.82, 1.0)
        bg.inputs['Strength'].default_value = 0.55
    return scene

def create_porcelain_material(name="Porcelain_Ivory", base_linear=(0.95, 0.87, 0.77), roughness=0.22):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*base_linear, 1.0)
        bsdf.inputs['Roughness'].default_value = roughness
        if 'Subsurface Weight' in bsdf.inputs:
            bsdf.inputs['Subsurface Weight'].default_value = 0.40
        elif 'Subsurface' in bsdf.inputs:
            bsdf.inputs['Subsurface'].default_value = 0.40
            
        if 'Subsurface Radius' in bsdf.inputs:
            bsdf.inputs['Subsurface Radius'].default_value = (1.0, 0.70, 0.45)
        if 'Coat Weight' in bsdf.inputs:
            bsdf.inputs['Coat Weight'].default_value = 0.65
        elif 'Clearcoat' in bsdf.inputs:
            bsdf.inputs['Clearcoat'].default_value = 0.65
        if 'Coat Roughness' in bsdf.inputs:
            bsdf.inputs['Coat Roughness'].default_value = 0.08
        elif 'Clearcoat Roughness' in bsdf.inputs:
            bsdf.inputs['Clearcoat Roughness'].default_value = 0.08
    return mat

def create_beak_material():
    return create_porcelain_material(name="Beak_Porcelain", base_linear=(0.88, 0.72, 0.55), roughness=0.25)

def create_feet_material():
    return create_porcelain_material(name="Feet_Bisque", base_linear=(0.72, 0.58, 0.45), roughness=0.30)

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
    
    # Z^2
    mul_z = nodes.new('ShaderNodeMath')
    mul_z.operation = 'MULTIPLY'
    links.new(sep.outputs['Z'], mul_z.inputs[0])
    links.new(sep.outputs['Z'], mul_z.inputs[1])
    
    # X^2 + Z^2
    add_xz = nodes.new('ShaderNodeMath')
    add_xz.operation = 'ADD'
    links.new(mul_x.outputs['Value'], add_xz.inputs[0])
    links.new(mul_z.outputs['Value'], add_xz.inputs[1])
    
    # sqrt(X^2 + Z^2) -> Planar radial distance from pupil center
    rad = nodes.new('ShaderNodeMath')
    rad.operation = 'SQRT'
    links.new(add_xz.outputs['Value'], rad.inputs[0])
    
    # Normalize by eyeball radius (0.165)
    div_norm = nodes.new('ShaderNodeMath')
    div_norm.operation = 'DIVIDE'
    links.new(rad.outputs['Value'], div_norm.inputs[0])
    div_norm.inputs[1].default_value = 0.165
    
    ramp = nodes.new('ShaderNodeValToRGB')
    # Pupil center: deep dark espresso (0.0 to 0.42)
    ramp.color_ramp.elements[0].position = 0.42
    ramp.color_ramp.elements[0].color = (0.015, 0.008, 0.003, 1.0)
    
    # Deep amber transition (0.55)
    elem1 = ramp.color_ramp.elements[1]
    elem1.position = 0.55
    elem1.color = (0.45, 0.18, 0.02, 1.0)
    
    # Rich golden amber iris (0.78)
    elem2 = ramp.color_ramp.elements.new(0.78)
    elem2.color = (0.92, 0.52, 0.05, 1.0)
    
    # Luminous golden caustic (0.92)
    elem3 = ramp.color_ramp.elements.new(0.92)
    elem3.color = (1.0, 0.85, 0.30, 1.0)
    
    # Deep espresso eyeliner rim (0.99)
    elem4 = ramp.color_ramp.elements.new(0.99)
    elem4.color = (0.08, 0.03, 0.01, 1.0)
    
    links.new(div_norm.outputs['Value'], ramp.inputs['Fac'])
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = 0.03
    bsdf.inputs['IOR'].default_value = 1.50
    if 'Coat Weight' in bsdf.inputs:
        bsdf.inputs['Coat Weight'].default_value = 1.0
    elif 'Clearcoat' in bsdf.inputs:
        bsdf.inputs['Clearcoat'].default_value = 1.0
    if 'Emission Color' in bsdf.inputs:
        links.new(ramp.outputs['Color'], bsdf.inputs['Emission Color'])
        if 'Emission Strength' in bsdf.inputs:
            bsdf.inputs['Emission Strength'].default_value = 0.18
            
    out_node = nodes.new('ShaderNodeOutputMaterial')
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])
    return mat

def build_owluko_body(porcelain_mat, json_path="scratch/owluko_contours.json"):
    with open(json_path, "r") as f:
        data = json.load(f)
        
    raw_rings = data['rings']
    num_sectors = 64
    
    body_rings = [r for r in raw_rings if r['y_img'] >= 60.0]
    first_body_ring = body_rings[0]
    
    top_z = 2.050
    z_base = first_body_ring['z_3d']
    h_dome = top_z - z_base
    r_target_x = first_body_ring['rx']
    r_target_y = first_body_ring['ry']
    cx_top = first_body_ring['cx']
    cy_top = first_body_ring['cy']
    
    dome_rings = []
    num_dome = 14
    for d in range(1, num_dome):
        theta = (d / float(num_dome)) * (math.pi / 2.0)
        z = top_z - h_dome * (1.0 - math.cos(theta))
        rx = r_target_x * math.sin(theta)
        ry = r_target_y * math.sin(theta)
        dome_rings.append({
            'y_img': 40.0 + (d / float(num_dome)) * 20.0,
            'z_3d': z,
            'rx': rx,
            'cx': cx_top,
            'ry': ry,
            'cy': cy_top
        })
        
    all_rings = dome_rings + body_rings
    
    # Smooth pelvic bottom cap
    last_ring = all_rings[-1]
    bot_z = last_ring['z_3d'] - 0.05
    bot_dome = []
    for d in range(1, 8):
        frac = d / 8.0
        z = last_ring['z_3d'] - 0.05 * frac
        rx = last_ring['rx'] * math.cos((math.pi/2.0) * frac)
        ry = last_ring['ry'] * math.cos((math.pi/2.0) * frac)
        bot_dome.append({
            'y_img': last_ring['y_img'] + frac * 6.0,
            'z_3d': z,
            'rx': rx,
            'cx': last_ring['cx'],
            'ry': last_ring['ry'],
            'cy': last_ring['cy']
        })
    all_rings.extend(bot_dome)
    
    mesh = bpy.data.meshes.new("Owluko_Body")
    bm = bmesh.new()
    
    v_top = bm.verts.new((cx_top, cy_top, top_z))
    
    ring_verts = []
    for ring in all_rings:
        cx = ring['cx']
        rx = ring['rx']
        cy = ring['cy']
        ry = ring['ry']
        z = ring['z_3d']
        
        cur = []
        for s in range(num_sectors):
            angle = 2.0 * math.pi * s / num_sectors
            vx = cx + rx * math.sin(angle)
            vy = cy + ry * math.cos(angle)
            cur.append(bm.verts.new((vx, vy, z)))
        ring_verts.append(cur)
        
    v_bot = bm.verts.new((last_ring['cx'], last_ring['cy'], bot_z))
    
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
    # Left eye: X = -0.305, Z = 1.450
    # Right eye: X = +0.295, Z = 1.450
    # Radius = 0.165 (larger, matching the reference eye proportions!)
    # Eyeball center at Y = -0.620, apex at Y = -0.785
    eyes = []
    eye_radius = 0.165
    
    for side, cx in [('Left', -0.305), ('Right', 0.295)]:
        # 1. Eyeball Sphere
        bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=eye_radius, location=(cx, -0.620, 1.450))
        eyeball = bpy.context.active_object
        eyeball.name = f"Eye_{side}_Ball"
        eyeball.data.materials.append(eye_mat)
        for poly in eyeball.data.polygons:
            poly.use_smooth = True
            
        # 2. Sleek Porcelain Upper Eyelid Hood (droopy, sleepy, covering ~45% of eyeball)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=eye_radius * 1.04, location=(cx, -0.620, 1.450))
        hood = bpy.context.active_object
        hood.name = f"Eye_{side}_Hood"
        
        # Keep vertices where Z > -0.010 (covering top 45% of eyeball for sleepy expression)
        bm = bmesh.new()
        bm.from_mesh(hood.data)
        to_delete = [v for v in bm.verts if v.co.z < -0.010]
        bmesh.ops.delete(bm, geom=to_delete, context='VERTS')
        bm.to_mesh(hood.data)
        bm.free()
        
        hood.data.materials.append(porcelain_mat)
        for poly in hood.data.polygons:
            poly.use_smooth = True
            
        # Give hood realistic thickness for soft shadow casting
        solid = hood.modifiers.new(name="Solidify", type='SOLIDIFY')
        solid.thickness = 0.018
        solid.offset = 0.5
        
        subsurf = hood.modifiers.new(name="Subdivision", type='SUBSURF')
        subsurf.levels = 1
        
        # 3. Soft Specular Glint Sphere (crisp white studio reflection on pupil)
        # Positioned at upper-left corner of pupil
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.020, location=(cx - 0.035, -0.782, 1.470))
        glint = bpy.context.active_object
        glint.name = f"Eye_{side}_Glint"
        glint_mat = bpy.data.materials.new(name=f"Glint_{side}")
        glint_mat.use_nodes = True
        bsdf_g = glint_mat.node_tree.nodes.get("Principled BSDF")
        bsdf_g.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
        if 'Emission Color' in bsdf_g.inputs:
            bsdf_g.inputs['Emission Color'].default_value = (1.0, 1.0, 1.0, 1.0)
            if 'Emission Strength' in bsdf_g.inputs:
                bsdf_g.inputs['Emission Strength'].default_value = 4.0
        glint.data.materials.append(glint_mat)
        
        eyes.extend([eyeball, hood, glint])
    return eyes

def build_owluko_beak(beak_mat):
    # Plump teardrop seed beak nestled between eyes
    # Top starts between eyes at Z = 1.48, tip extends to Z = 1.16
    z_mid = (1.480 + 1.160) / 2.0
    depth = 1.480 - 1.160 # 0.320
    bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=0.082, radius2=0.022, depth=depth, location=(0.0, -0.690, z_mid))
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

def build_owluko_legs_and_feet(feet_mat):
    # Smooth organic avian legs emerging from pelvic base and splaying into 3 bulbous toes
    elements = []
    
    for side, cx in [('Left', -0.340), ('Right', 0.340)]:
        # 1. Smooth Tapering Leg Shank (single organic lofted mesh, ZERO segmented rings!)
        bm = bmesh.new()
        
        # Upper ring (emerging from belly at Z = 0.22, radius 0.088)
        # Mid ring (Z = 0.05, radius 0.072)
        # Ankle ring (Z = -0.08, radius 0.082, flared forward)
        rings_def = [
            (0.22, 0.0, -0.08, 0.088),
            (0.12, 0.0, -0.10, 0.078),
            (0.02, 0.0, -0.12, 0.072),
            (-0.08, 0.0, -0.15, 0.082)
        ]
        
        num_s = 24
        prev_verts = None
        for z, dx, dy, r in rings_def:
            cur_verts = []
            for s in range(num_s):
                ang = 2.0 * math.pi * s / num_s
                vx = cx + dx + r * math.cos(ang)
                vy = dy + r * 1.15 * math.sin(ang)
                vz = z
                cur_verts.append(bm.verts.new((vx, vy, vz)))
            if prev_verts is not None:
                for s in range(num_s):
                    s_next = (s + 1) % num_s
                    bm.faces.new((prev_verts[s], prev_verts[s_next], cur_verts[s_next], cur_verts[s]))
            prev_verts = cur_verts
            
        mesh = bpy.data.meshes.new(f"Leg_{side}_Shank")
        bm.to_mesh(mesh)
        bm.free()
        
        shank = bpy.data.objects.new(f"Leg_{side}_Shank", mesh)
        bpy.context.collection.objects.link(shank)
        for poly in mesh.polygons:
            poly.use_smooth = True
        subsurf = shank.modifiers.new(name="Subdivision", type='SUBSURF')
        subsurf.levels = 2
        shank.data.materials.append(feet_mat)
        elements.append(shank)
        
        # 2. Three Bulbous Grounded Toes (smooth teardrop capsules resting at baseline Z = -0.195)
        # Middle toe points forward/slightly outward
        toes_config = [
            (-24, -0.055, 0.005, 0.170), # Inner toe
            (0,    0.000, 0.000, 0.210), # Center toe
            (24,   0.055, 0.005, 0.165)  # Outer toe
        ]
        for t_idx, (angle, dx, dz, length) in enumerate(toes_config):
            bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.048, location=(cx + dx, -0.27, -0.165 + dz))
            toe = bpy.context.active_object
            toe.name = f"Foot_{side}_Toe_{t_idx}"
            toe.scale = (1.0, length / 0.048, 0.82)
            toe.rotation_euler = (0, 0, math.radians(angle if side == 'Right' else -angle))
            for poly in toe.data.polygons:
                poly.use_smooth = True
            subsurf_t = toe.modifiers.new(name="Subdivision", type='SUBSURF')
            subsurf_t.levels = 1
            toe.data.materials.append(feet_mat)
            elements.append(toe)
            
    return elements

def build_owluko_wings(porcelain_mat):
    # Organic tucked wings on the flanks to give the distinct owl silhouette and ambient occlusion crease
    wings = []
    for side, cx, sgn in [('Left', -0.68, -1.0), ('Right', 0.68, 1.0)]:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.22, location=(cx, -0.15, 0.92))
        wing = bpy.context.active_object
        wing.name = f"Wing_{side}"
        wing.scale = (0.50, 1.30, 2.20)
        wing.rotation_euler = (math.radians(12), sgn * math.radians(-10), sgn * math.radians(8))
        for poly in wing.data.polygons:
            poly.use_smooth = True
        subsurf = wing.modifiers.new(name="Subdivision", type='SUBSURF')
        subsurf.levels = 1
        wing.data.materials.append(porcelain_mat)
        wings.append(wing)
    return wings

def setup_lighting():
    # Tuned studio lighting (soft golden illumination, warm porcelain bounce)
    # 1. Key Light: Warm golden key (upper-left)
    bpy.ops.object.light_add(type='AREA', location=(-2.6, -4.2, 3.2))
    key = bpy.context.active_object
    key.name = "Key_Light"
    key.data.energy = 320
    key.data.size = 2.8
    key.data.color = (1.0, 0.94, 0.86)
    key.rotation_euler = (math.radians(52), math.radians(12), math.radians(-28))
    
    # 2. Fill Light: Soft warm-neutral (right)
    bpy.ops.object.light_add(type='AREA', location=(3.4, -3.6, 1.8))
    fill = bpy.context.active_object
    fill.name = "Fill_Light"
    fill.data.energy = 160
    fill.data.size = 3.4
    fill.data.color = (0.98, 0.95, 0.92)
    fill.rotation_euler = (math.radians(48), math.radians(-18), math.radians(38))
    
    # 3. Eye Catch Light (front-left)
    bpy.ops.object.light_add(type='SPOT', location=(-0.8, -4.5, 1.8))
    spot = bpy.context.active_object
    spot.name = "Eye_Catch_Light"
    spot.data.energy = 70
    spot.data.spot_size = math.radians(25)
    spot.data.spot_blend = 0.5
    spot.data.color = (1.0, 0.98, 0.95)
    
    # 4. Rim Light: Back-Top
    bpy.ops.object.light_add(type='AREA', location=(0.0, 3.2, 3.2))
    rim = bpy.context.active_object
    rim.name = "Rim_Light"
    rim.data.energy = 220
    rim.data.size = 2.2
    rim.data.color = (1.0, 0.94, 0.86)
    rim.rotation_euler = (math.radians(-50), 0, math.radians(180))
    
    # 5. Under-Bounce Light
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
    
    body = build_owluko_body(porcelain_mat)
    wings = build_owluko_wings(porcelain_mat)
    eyes = build_owluko_eyes(eye_mat, porcelain_mat)
    beak = build_owluko_beak(beak_mat)
    legs_and_feet = build_owluko_legs_and_feet(feet_mat)
    
    setup_lighting()
    cam = setup_camera()
    
    out_dir = os.path.abspath("scratch")
    os.makedirs(out_dir, exist_ok=True)
    out_png = os.path.join(out_dir, "blender_owluko_v13.png")
    scene.render.filepath = out_png
    bpy.ops.render.render(write_still=True)
    print(f"Rendered Blender Owluko V13: {out_png}")

if __name__ == "__main__":
    main()
