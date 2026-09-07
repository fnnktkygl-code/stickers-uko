import cv2
import numpy as np
import os
import json

def build_rive_pack():
    src_dir = "mascots/owluko/rig_layers"
    out_dir = "mascots/owluko/rive"
    assets_dir = os.path.join(out_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    layers_meta = {}
    
    # Process and crop each layer to its bounding box
    layer_files = sorted([f for f in os.listdir(src_dir) if f.endswith(".png")])
    
    for f in layer_files:
        p = os.path.join(src_dir, f)
        img = cv2.imread(p, cv2.IMREAD_UNCHANGED)
        alpha = img[:, :, 3]
        ys, xs = np.where(alpha > 0)
        
        if len(ys) == 0:
            continue
            
        x_min, x_max = int(xs.min()), int(xs.max())
        y_min, y_max = int(ys.min()), int(ys.max())
        
        cropped = img[y_min:y_max+1, x_min:x_max+1]
        crop_path = os.path.join(assets_dir, f)
        cv2.imwrite(crop_path, cropped)
        
        layers_meta[f.replace(".png", "")] = {
            "file": f"assets/{f}",
            "full_canvas_bbox": {
                "x_min": x_min, "x_max": x_max,
                "y_min": y_min, "y_max": y_max,
                "width": x_max - x_min + 1,
                "height": y_max - y_min + 1
            },
            "center": [float((x_min + x_max) / 2.0), float((y_min + y_max) / 2.0)]
        }
        
    # Build complete Rive specification JSON
    rive_spec = {
        "format": "Rive State Machine & Bone Rig Specification",
        "version": "1.0",
        "mascot": "Owluko",
        "artboard": {
            "name": "Owluko_Artboard",
            "width": 512,
            "height": 512,
            "fps": 60,
            "origin": [0, 0]
        },
        "bones": [
            {
                "id": "root_bone",
                "name": "Root",
                "position": [256.0, 489.0],
                "length": 0.0,
                "rotation": 0.0,
                "parent": None
            },
            {
                "id": "shadow_bone",
                "name": "Bone_Shadow",
                "position": [256.0, 489.0],
                "length": 10.0,
                "rotation": 0.0,
                "parent": "root_bone"
            },
            {
                "id": "pelvis_bone",
                "name": "Bone_Pelvis",
                "position": [256.0, 435.0],
                "length": 135.0,
                "rotation": -90.0,
                "parent": "root_bone"
            },
            {
                "id": "l_foot_bone",
                "name": "Bone_Foot_L",
                "position": [204.0, 425.0],
                "length": 64.0,
                "rotation": 90.0,
                "parent": "root_bone"
            },
            {
                "id": "r_foot_bone",
                "name": "Bone_Foot_R",
                "position": [308.0, 425.0],
                "length": 64.0,
                "rotation": 90.0,
                "parent": "root_bone"
            },
            {
                "id": "spine_bone",
                "name": "Bone_Spine",
                "position": [256.0, 300.0],
                "length": 125.0,
                "rotation": -90.0,
                "parent": "pelvis_bone"
            },
            {
                "id": "head_bone",
                "name": "Bone_Head",
                "position": [256.0, 175.0],
                "length": 135.0,
                "rotation": -90.0,
                "parent": "spine_bone"
            },
            {
                "id": "beak_bone",
                "name": "Bone_Beak",
                "position": [256.0, 175.0],
                "length": 55.0,
                "rotation": 90.0,
                "parent": "head_bone"
            },
            {
                "id": "l_eye_bone",
                "name": "Bone_Eye_L",
                "position": [193.0, 160.0],
                "length": 10.0,
                "rotation": 0.0,
                "parent": "head_bone"
            },
            {
                "id": "r_eye_bone",
                "name": "Bone_Eye_R",
                "position": [315.0, 163.0],
                "length": 10.0,
                "rotation": 0.0,
                "parent": "head_bone"
            },
            {
                "id": "l_eyelid_bone",
                "name": "Bone_Eyelid_L",
                "position": [193.0, 145.0],
                "length": 20.0,
                "rotation": 90.0,
                "parent": "head_bone"
            },
            {
                "id": "r_eyelid_bone",
                "name": "Bone_Eyelid_R",
                "position": [315.0, 147.0],
                "length": 20.0,
                "rotation": 90.0,
                "parent": "head_bone"
            },
            {
                "id": "l_wing_bone",
                "name": "Bone_Wing_L",
                "position": [128.0, 192.0],
                "length": 190.0,
                "rotation": 85.0,
                "parent": "pelvis_bone"
            },
            {
                "id": "r_wing_bone",
                "name": "Bone_Wing_R",
                "position": [384.0, 192.0],
                "length": 190.0,
                "rotation": 95.0,
                "parent": "pelvis_bone"
            }
        ],
        "state_machine": {
            "name": "Owluko_StateMachine",
            "inputs": [
                {"name": "isBreathing", "type": "Boolean", "default": True},
                {"name": "blinkTrigger", "type": "Trigger"},
                {"name": "lookX", "type": "Number", "min": -100.0, "max": 100.0, "default": 0.0},
                {"name": "lookY", "type": "Number", "min": -100.0, "max": 100.0, "default": 0.0},
                {"name": "isHovering", "type": "Boolean", "default": False}
            ],
            "layers": [
                {
                    "name": "Base_Breathing",
                    "states": [
                        {"name": "Idle_Respiration", "type": "Animation", "timeline": "idle_breath", "loop": True}
                    ]
                },
                {
                    "name": "Eyelid_Blink",
                    "states": [
                        {"name": "Drowsy_Rest", "type": "Entry"},
                        {"name": "Do_Blink", "type": "Animation", "timeline": "blink_action", "loop": False}
                    ],
                    "transitions": [
                        {"from": "Drowsy_Rest", "to": "Do_Blink", "condition": "blinkTrigger"},
                        {"from": "Do_Blink", "to": "Drowsy_Rest", "condition": "onAnimationEnd"}
                    ]
                },
                {
                    "name": "Gaze_Tracking",
                    "states": [
                        {"name": "Blend_Gaze", "type": "BlendTree2D", "inputs": ["lookX", "lookY"]}
                    ]
                },
                {
                    "name": "Wing_Secondary",
                    "states": [
                        {"name": "Wing_Harmonics", "type": "Animation", "timeline": "wing_sway", "loop": True}
                    ]
                }
            ]
        },
        "layers": layers_meta
    }
    
    spec_path = os.path.join(out_dir, "owluko_rive_spec.json")
    with open(spec_path, "w") as f:
        json.dump(rive_spec, f, indent=2)
    print("Saved Rive Spec JSON:", spec_path)
    
    # Create Layered SVG for Rive Studio import
    # Rive Web Studio accepts SVG where groups map directly to nodes & bones!
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
  </defs>
  <!-- Root Controller -->
  <g id="Root" transform="translate(0, 0)">
    <!-- 00 Ground Contact Shadow -->
    <g id="Shadow">
      <ellipse cx="256" cy="488" rx="70" ry="10" fill="#1e1e20" opacity="0.35" filter="url(#softShadow)"/>
      <ellipse cx="198" cy="487" rx="36" ry="8" fill="#18181a" opacity="0.65" filter="url(#softShadow)"/>
      <ellipse cx="312" cy="487" rx="36" ry="8" fill="#18181a" opacity="0.65" filter="url(#softShadow)"/>
    </g>
    <!-- 01 Feet -->
    <g id="Foot_Left" transform-origin="204 425">
      <image href="assets/01_foot_left.png" x="0" y="0" width="512" height="512"/>
    </g>
    <g id="Foot_Right" transform-origin="308 425">
      <image href="assets/02_foot_right.png" x="0" y="0" width="512" height="512"/>
    </g>
    <!-- 02 Body Master -->
    <g id="Body_Master" transform-origin="256 435">
      <image href="assets/03_body_porcelain.png" x="0" y="0" width="512" height="512"/>
      
      <!-- Wings parented to Body -->
      <g id="Wing_Left" transform-origin="128 192">
        <image href="assets/04_wing_left.png" x="0" y="0" width="512" height="512"/>
      </g>
      <g id="Wing_Right" transform-origin="384 192">
        <image href="assets/05_wing_right.png" x="0" y="0" width="512" height="512"/>
      </g>
      
      <!-- Head features parented to Body -->
      <g id="Head" transform-origin="256 175">
        <g id="Eye_Left" transform-origin="193 160">
          <image href="assets/06_eye_left.png" x="0" y="0" width="512" height="512"/>
        </g>
        <g id="Eye_Right" transform-origin="315 163">
          <image href="assets/07_eye_right.png" x="0" y="0" width="512" height="512"/>
        </g>
        <g id="Eyelid_Left" transform-origin="193 145">
          <image href="assets/08_eyelid_left.png" x="0" y="0" width="512" height="512"/>
        </g>
        <g id="Eyelid_Right" transform-origin="315 147">
          <image href="assets/09_eyelid_right.png" x="0" y="0" width="512" height="512"/>
        </g>
        <g id="Beak" transform-origin="256 175">
          <image href="assets/10_beak.png" x="0" y="0" width="512" height="512"/>
        </g>
      </g>
    </g>
  </g>
</svg>
'''
    svg_path = os.path.join(out_dir, "owluko_rive_rig.svg")
    with open(svg_path, "w") as f:
        f.write(svg_content)
    print("Saved Rive Rig SVG:", svg_path)

if __name__ == "__main__":
    build_rive_pack()
