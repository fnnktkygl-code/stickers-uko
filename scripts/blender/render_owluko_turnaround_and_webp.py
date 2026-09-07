import bpy
import math
import os
import sys

sys.path.append(os.path.abspath("scripts/blender"))
from build_owluko_3d_master import (
    reset_blender_scene, create_porcelain_material,
    create_concentric_amber_eye_material, create_beak_material,
    create_feet_material, build_owluko_body, build_owluko_wings,
    build_owluko_eyes, build_owluko_beak, build_owluko_legs_and_feet,
    setup_lighting, setup_camera
)

def render_turnaround_and_animation():
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
    
    out_dir = os.path.abspath("scratch/owluko_turnaround")
    os.makedirs(out_dir, exist_ok=True)
    
    # 1. Four Turnaround Angles (0°, 45°, 90°, 180°)
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
        
    # 2. Render 36 frames for smooth 360° turntable WebP (10° per frame)
    for f in range(36):
        deg = f * 10.0
        root.rotation_euler = (0, 0, math.radians(-deg))
        frame_path = os.path.join(out_dir, f"turntable_{f:02d}.png")
        scene.render.filepath = frame_path
        bpy.ops.render.render(write_still=True)
        
    # 3. Export Draco-compressed GLB
    glb_out = os.path.abspath("mascots/owluko/owluko_3d_master.glb")
    root.rotation_euler = (0, 0, 0)
    bpy.ops.export_scene.gltf(filepath=glb_out, export_draco_mesh_compression_enable=True)
    print(f"Exported Draco GLB: {glb_out}")

if __name__ == "__main__":
    render_turnaround_and_animation()
