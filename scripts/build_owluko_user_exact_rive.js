const fs = require("fs");
const path = require("path");
const { callMcpTool } = require("./rive_mcp_client.js");

const kappa = 0.5522847498307936;

async function buildOwlukoCanonicalRive() {
  console.log("===================================================================");
  console.log("  BUILDING CANONICAL OWLUKO RIVE ASSET (100% USER ANATOMY MATCH)   ");
  console.log("  - Pure Vector Bezier Shapes, Real Gradients, Full 60 FPS Rig     ");
  console.log("===================================================================");

  const fragmentPath = path.resolve(__dirname, "../scratch/owluko_user_exact.scene.json");
  if (!fs.existsSync(fragmentPath)) {
    throw new Error("Missing fragment: " + fragmentPath);
  }
  const fragment = JSON.parse(fs.readFileSync(fragmentPath, "utf-8"));
  console.log(`Loaded fragment with ${fragment.shapes.length} imported shapes.`);

  // 1. Define Rig Groups Hierarchy (1024 x 1024 Artboard Space)
  const groups = [
    { id: "root", x: 512, y: 876 },
    { id: "shadow_group", parent: "root", x: 0, y: 0 },
    { id: "feet_group", parent: "root", x: 0, y: 0 },
    { id: "body_group", parent: "root", x: 0, y: -378 }, // global: (512, 498)
    { id: "wings_group", parent: "body_group", x: 0, y: 0 },
    { id: "wing_l_group", parent: "wings_group", x: -294, y: 0 }, // global: (218, 498)
    { id: "wing_r_group", parent: "wings_group", x: 294, y: 0 }, // global: (806, 498)
    { id: "chest_group", parent: "body_group", x: 0, y: 0 },
    { id: "head_group", parent: "body_group", x: 0, y: -126 }, // global: (512, 372)
    { id: "eye_l_group", parent: "head_group", x: -114.5, y: -10.5 }, // global: (397.5, 361.5)
    { id: "eye_r_group", parent: "head_group", x: 120, y: -16 }, // global: (632, 356)
    { id: "beak_group", parent: "head_group", x: 0, y: 44 } // global: (512, 416)
  ];

  // Helper to compute global origin of each group
  const groupMap = {};
  for (const g of groups) groupMap[g.id] = g;
  function getGroupGlobal(gid) {
    let gx = 0, gy = 0;
    let curr = groupMap[gid];
    while (curr) {
      gx += curr.x;
      gy += curr.y;
      curr = curr.parent ? groupMap[curr.parent] : null;
    }
    return { gx, gy };
  }

  // Map each shape to its target group and compute relative coordinates
  const shapeTargetGroup = {
    // Ground shadow
    owlukop0: "shadow_group",
    owlukop1: "shadow_group",

    // Left foot (p2..p7)
    owlukop2: "feet_group",
    owlukop3: "feet_group",
    owlukop4: "feet_group",
    owlukop5: "feet_group",
    owlukop6: "feet_group",
    owlukop7: "feet_group",

    // Right foot (p8..p13)
    owlukop8: "feet_group",
    owlukop9: "feet_group",
    owlukop10: "feet_group",
    owlukop11: "feet_group",
    owlukop12: "feet_group",
    owlukop13: "feet_group",

    // Body
    owlukobody_silhouette: "body_group",

    // Wings
    owlukop14: "wing_l_group",
    owlukowing_left_main: "wing_l_group",
    owlukop15: "wing_r_group",
    owlukowing_right_main: "wing_r_group",

    // Chest scallops (p16..p25)
    owlukop16: "chest_group",
    owlukop17: "chest_group",
    owlukop18: "chest_group",
    owlukop19: "chest_group",
    owlukop20: "chest_group",
    owlukop21: "chest_group",
    owlukop22: "chest_group",
    owlukop23: "chest_group",
    owlukop24: "chest_group",
    owlukop25: "chest_group",

    // Head / Facial mask (p26..p28)
    owlukop26: "head_group",
    owlukofacial_mask_silhouette: "head_group",
    owlukop27: "head_group",
    owlukop28: "head_group",

    // Left Eye (p29..p36)
    owlukop29: "eye_l_group",
    owlukop30: "eye_l_group",
    owlukop31: "eye_l_group",
    owlukop32: "eye_l_group",
    owlukop33: "eye_l_group",
    owlukop34: "eye_l_group",
    owlukop35: "eye_l_group",
    owlukop36: "eye_l_group",

    // Right Eye Wink (p37, wink_main_stroke)
    owlukop37: "eye_r_group",
    owlukowink_main_stroke: "eye_r_group",

    // Beak & mouth
    owlukobeak_lower_cup: "beak_group",
    owlukomouth_cavity: "beak_group",
    owlukomouth_tongue: "beak_group",
    owlukop38: "beak_group",
    owlukobeak_upper_dome: "beak_group",
    owlukop39: "beak_group",
    owlukop40: "beak_group",
    owlukop41: "beak_group"
  };

  const processedShapes = [];

  for (const s of fragment.shapes) {
    const targetGid = shapeTargetGroup[s.id];
    if (targetGid) {
      const gOrigin = getGroupGlobal(targetGid);
      s.parent = targetGid;
      s.x = s.x - gOrigin.gx;
      s.y = s.y - gOrigin.gy;
    }
    processedShapes.push(s);
  }

  // Add Eyelid Cover & Seam for Left Eye (Centered at 0, 0 in eye_l_group)
  const r_eye = 63.5;
  const eyelidCoverPoints = [
    { x: -r_eye, y: 0, cubic: { inRotation: 90, inDistance: r_eye * kappa, rotation: 270, outDistance: r_eye * kappa } },
    { x: 0, y: -r_eye, cubic: { inRotation: 180, inDistance: r_eye * kappa, rotation: 0, outDistance: r_eye * kappa } },
    { x: r_eye, y: 0, cubic: { inRotation: 270, inDistance: r_eye * kappa, rotation: 90, outDistance: r_eye * kappa } },
    { x: 0, y: r_eye, cubic: { inRotation: 0, inDistance: r_eye * kappa, rotation: 180, outDistance: r_eye * kappa } }
  ];

  // Closed eye smile arc
  const closedEyeArc = [
    { x: -40, y: 3, cubic: { inRotation: 0, inDistance: 0, rotation: 22, outDistance: 20 } },
    { x: 0, y: 16, cubic: { inRotation: -22, inDistance: 20, rotation: -22, outDistance: 20 } },
    { x: 40, y: 3, cubic: { inRotation: 22, inDistance: 20, rotation: 0, outDistance: 0 } }
  ];

  processedShapes.push(
    {
      id: "eyelid_l_cover",
      type: "polygon",
      parent: "eye_l_group",
      x: 0,
      y: 0,
      points: eyelidCoverPoints,
      opacity: 0,
      fill: { color: "#FAF6EE" }
    },
    {
      id: "eyelid_l_seam",
      type: "polygon",
      closed: false,
      parent: "eye_l_group",
      x: 0,
      y: 0,
      points: closedEyeArc,
      opacity: 0,
      stroke: { color: "#5C3D2E", thickness: 4.0, cap: "round", join: "round" }
    }
  );

  // 2. Fluid 60 FPS Animations (120 frames = 2.0s seamless loop)
  const animations = [
    {
      name: "idle",
      fps: 60,
      duration: 120,
      loop: "loop",
      tracks: [
        // Body Respiration (Organic squash and stretch)
        {
          target: "body_group",
          property: "scaleY",
          keyframes: [
            { frame: 0, value: 1.0 },
            { frame: 60, value: 1.025, easing: "ease-in-out" },
            { frame: 120, value: 1.0, easing: "ease-in-out" }
          ]
        },
        {
          target: "body_group",
          property: "scaleX",
          keyframes: [
            { frame: 0, value: 1.0 },
            { frame: 60, value: 0.988, easing: "ease-in-out" },
            { frame: 120, value: 1.0, easing: "ease-in-out" }
          ]
        },
        // Wings Subtle Harmonic Respiration Tilt
        {
          target: "wing_l_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0.0 },
            { frame: 60, value: -1.6, easing: "ease-in-out" },
            { frame: 120, value: 0.0, easing: "ease-in-out" }
          ]
        },
        {
          target: "wing_r_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0.0 },
            { frame: 60, value: 1.6, easing: "ease-in-out" },
            { frame: 120, value: 0.0, easing: "ease-in-out" }
          ]
        },
        // Head Subtle Harmonic Bob & Gentle Tilt
        {
          target: "head_group",
          property: "y",
          keyframes: [
            { frame: 0, value: -126.0 },
            { frame: 65, value: -129.5, easing: "ease-in-out" },
            { frame: 120, value: -126.0, easing: "ease-in-out" }
          ]
        },
        {
          target: "head_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0.0 },
            { frame: 35, value: 0.8, easing: "ease-in-out" },
            { frame: 85, value: -0.6, easing: "ease-in-out" },
            { frame: 120, value: 0.0, easing: "ease-in-out" }
          ]
        },
        // Ground Shadow Subtle Expansion with Breath
        {
          target: "shadow_group",
          property: "scaleX",
          keyframes: [
            { frame: 0, value: 1.0 },
            { frame: 60, value: 1.03, easing: "ease-in-out" },
            { frame: 120, value: 1.0, easing: "ease-in-out" }
          ]
        },
        // Conscious Blink at frame 70..86
        {
          target: "eyelid_l_cover",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 68, value: 0 },
            { frame: 74, value: 1, easing: "ease-in" },
            { frame: 80, value: 1 },
            { frame: 86, value: 0, easing: "ease-out" },
            { frame: 120, value: 0 }
          ]
        },
        {
          target: "eyelid_l_seam",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 68, value: 0 },
            { frame: 74, value: 1, easing: "ease-in" },
            { frame: 80, value: 1 },
            { frame: 86, value: 0, easing: "ease-out" },
            { frame: 120, value: 0 }
          ]
        }
      ]
    },
    {
      name: "blink",
      fps: 60,
      duration: 20,
      loop: "one-shot",
      tracks: [
        {
          target: "eyelid_l_cover",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 6, value: 1, easing: "ease-in" },
            { frame: 12, value: 1 },
            { frame: 18, value: 0, easing: "ease-out" },
            { frame: 20, value: 0 }
          ]
        },
        {
          target: "eyelid_l_seam",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 6, value: 1, easing: "ease-in" },
            { frame: 12, value: 1 },
            { frame: 18, value: 0, easing: "ease-out" },
            { frame: 20, value: 0 }
          ]
        }
      ]
    }
  ];

  // 3. State Machine Declaration
  const stateMachine = {
    name: "SM_Owluko",
    inputs: [
      { name: "isWinking", type: "bool", value: true },
      { name: "triggerBlink", type: "trigger" }
    ],
    states: [
      { name: "Respiration", animation: "idle" },
      { name: "Blink_State", animation: "blink" }
    ],
    transitions: [
      { from: "entry", to: "Respiration" },
      { from: "Respiration", to: "Blink_State", condition: { input: "triggerBlink" } },
      { from: "Blink_State", to: "Respiration", exitTimeMs: 333 }
    ]
  };

  const scene = {
    artboard: {
      name: "Owluko_Canonical",
      width: 1024,
      height: 1024
    },
    backgroundColor: "#FFFFFF",
    groups,
    shapes: processedShapes,
    animations,
    stateMachine
  };

  // Write scene.json for live hot-reload in Rive Studio daemon
  const scenePath = path.resolve(__dirname, "../mascots/owluko/owluko_pure_vector.scene.json");
  fs.writeFileSync(scenePath, JSON.stringify(scene, null, 2));
  console.log("Written updated scene to " + scenePath);

  // Compile native Rive .riv binary
  const outRivPath = path.resolve(__dirname, "../mascots/owluko/owluko_pure_vector.riv");
  console.log("Compiling pure vector binary to " + outRivPath + "...");
  const createRes = await callMcpTool("riv_create", {
    outPath: outRivPath,
    scene: scene
  });

  if (createRes && createRes.isError) {
    console.error("Compilation error:", JSON.stringify(createRes, null, 2));
    process.exit(1);
  }

  const stat = fs.statSync(outRivPath);
  console.log(`Compiled pure vector .riv: ${stat.size} bytes (${(stat.size / 1024).toFixed(1)} KB)`);

  // Render Frame 0
  const frame0Path = path.resolve(__dirname, "../mascots/owluko/owluko_pure_vector_frame0.png");
  console.log("Rendering frame 0...");
  await callMcpTool("riv_render_frame", {
    path: outRivPath,
    outPath: frame0Path,
    animation: "idle",
    time: 0,
    background: "#FFFFFF"
  });

  // Render Blink Frame
  const frameBlinkPath = path.resolve(__dirname, "../mascots/owluko/owluko_pure_vector_blink.png");
  console.log("Rendering blink frame (t=1.3s)...");
  await callMcpTool("riv_render_frame", {
    path: outRivPath,
    outPath: frameBlinkPath,
    animation: "idle",
    time: 1.3,
    background: "#FFFFFF"
  });

  // Render Looping GIF
  const gifPath = path.resolve(__dirname, "../mascots/owluko/owluko_pure_vector.gif");
  console.log("Rendering 2.0s looping GIF...");
  await callMcpTool("riv_render_gif", {
    path: outRivPath,
    outPath: gifPath,
    animation: "idle",
    fps: 30,
    duration: 2.0,
    background: "#FFFFFF"
  });

  console.log("=== CANONICAL OWLUKO COMPILED SUCCESSFULLY ===");
}

buildOwlukoCanonicalRive().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
