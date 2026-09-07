import bpy
import bmesh
import math
import os

def build_clean_box_owluko():
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
        bg.inputs['Color'].default_value = (0.97, 0.92, 0.84, 1.0)
        bg.inputs['Strength'].default_value = 0.52

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

    # Porcelain Material
    mat_p = bpy.data.materials.new(name="Porcelain_Ivory")
    mat_p.use_nodes = True
    bsdf = mat_p.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (0.95, 0.88, 0.78, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.22
    if 'Subsurface Weight' in bsdf.inputs:
        bsdf.inputs['Subsurface Weight'].default_value = 0.45
    if 'Coat Weight' in bsdf.inputs:
        bsdf.inputs['Coat Weight'].default_value = 0.70

    # 1. Clean Quad Egg Body: UV Sphere with 16 segments x 12 rings
    # Scaled and shaped to match Front, Side, and Back
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, radius=1.0, location=(0, 0, 0))
    body = bpy.context.active_object
    body.name = "Owluko_Egg"
    
    # Shape vertices to match egg silhouette
    bm = bmesh.new()
    bm.from_mesh(body.data)
    
    # Ground truth bounds:
    # Z in [0.20, 2.05], center Z = 1.125, half-height = 0.925
    # X width in front view: half-width = 0.82 at belly (Z ~ 1.0), half-width = 0.55 at head (Z ~ 1.7)
    # Y depth in profile view: front belly at Y = -0.74, back at Y = +0.66
    for v in bm.verts:
        # Normalize sphere coord: v.co in [-1, 1]
        sz = v.co.z # -1 to 1
        
        # Height mapping: z from 0.18 to 2.05
        z_world = 1.115 + sz * 0.935
        
        # Width factor: chubby lower belly, tapering dome head
        # At sz = 0 (equator, Z=1.115): rx ~ 0.82
        # At sz = 0.6 (head, Z=1.67): rx ~ 0.62
        # At sz = -0.6 (pelvis, Z=0.55): rx ~ 0.70
        t = (sz + 1.0) / 2.0 # 0 (bottom) to 1 (top)
        
        # Organic egg taper formula
        width_profile = math.sin(t * math.pi) ** 0.85
        # Asymmetry: thicker in lower half
        belly_bulge = 1.0 + 0.22 * (1.0 - t) * math.sin(t * math.pi)
        
        rx = 0.825 * width_profile * belly_bulge
        
        # In Y: front is round, back has slight tail flare at bottom
        ry_front = 0.730 * width_profile * belly_bulge
        ry_back = 0.670 * width_profile
        
        # Tail flare at lower back (sz between -0.8 and -0.2, y > 0)
        if -0.85 < sz < -0.15 and v.co.y > 0:
            tail_fac = math.sin((sz + 0.85) / 0.70 * math.pi)
            ry_back += 0.18 * tail_fac * (v.co.y ** 2)
            
        vx = v.co.x * rx / max(0.001, math.sqrt(max(0.0001, 1.0 - sz**2))) if abs(sz) < 0.999 else 0.0
        vy_factor = ry_back if v.co.y >= 0 else ry_front
        vy = v.co.y * vy_factor / max(0.001, math.sqrt(max(0.0001, 1.0 - sz**2))) if abs(sz) < 0.999 else 0.0
        
        # Recess eye sockets on front face (Z in [1.32, 1.58], X in [-0.45, -0.12] and [0.12, 0.45], Y < 0)
        for ex, ez in [(-0.28, 1.45), (0.28, 1.45)]:
            d_sock = math.sqrt((vx - ex)**2 + (z_world - ez)**2)
            if d_sock < 0.18 and vy < 0:
                indent = 0.055 * (math.cos(math.pi * d_sock / 0.18) + 1.0) / 2.0
                vy += indent # push back into head
                
        v.co.x = vx
        v.co.y = vy
        v.co.z = z_world
        
    bm.to_mesh(body.data)
    bm.free()
    
    body.data.materials.append(mat_p)
    for p in body.data.polygons:
        p.use_smooth = True
        
    subsurf = body.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2
    
    # Render Front, 3/4, Profile, Back
    angles = [
        ("front", 0.0),
        ("three_quarter", 45.0),
        ("profile", 90.0),
        ("back", 180.0)
    ]
    
    out_frames = []
    for name, deg in angles:
        body.rotation_euler = (0, 0, math.radians(-deg))
        out_p = os.path.abspath(f"scratch/test_clean_egg_{name}.png")
        scene.render.filepath = out_p
        bpy.ops.render.render(write_still=True)
        out_frames.append(out_p)
        print(f"Rendered {name}: {out_p}")

if __name__ == "__main__":
    build_clean_box_owluko()
