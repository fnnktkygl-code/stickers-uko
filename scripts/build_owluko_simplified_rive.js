const fs = require("fs");
const path = require("path");
const { callMcpTool } = require("./rive_mcp_client.js");

const kappa = 0.5522847498307936;

async function buildOwlukoSimplifiedRive() {
  console.log("===================================================================");
  console.log("  BUILDING CANONICAL SIMPLIFIED OWLUKO RIVE ASSET (media_1788762944348)");
  console.log("  - Pure Vector Bezier Shapes, Real Gradients, 60 FPS Rig & SM     ");
  console.log("===================================================================");

  const fragmentPath = path.resolve(__dirname, "../scratch/owluko_simplified.scene.json");
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
    { id: "belly_group", parent: "body_group", x: 0, y: 0 }, // global: (512, 498)
    { id: "head_group", parent: "body_group", x: 0, y: -126 }, // global: (512, 372)
    { id: "eye_l_group", parent: "head_group", x: -114, y: -10 }, // global: (398, 362)
    { id: "eye_r_group", parent: "head_group", x: 114, y: -10 }, // global: (626, 362)
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
    owluko_simpp0: "shadow_group",
    owluko_simpp1: "shadow_group",

    // Left foot (p2..p7)
    owluko_simpp2: "feet_group",
    owluko_simpp3: "feet_group",
    owluko_simpp4: "feet_group",
    owluko_simpp5: "feet_group",
    owluko_simpp6: "feet_group",
    owluko_simpp7: "feet_group",

    // Right foot (p8..p13)
    owluko_simpp8: "feet_group",
    owluko_simpp9: "feet_group",
    owluko_simpp10: "feet_group",
    owluko_simpp11: "feet_group",
    owluko_simpp12: "feet_group",
    owluko_simpp13: "feet_group",

    // Body
    owluko_simpbody_silhouette: "body_group",

    // Wings
    owluko_simpp14: "wing_l_group",
    owluko_simpwing_left_main: "wing_l_group",
    owluko_simpp15: "wing_r_group",
    owluko_simpwing_right_main: "wing_r_group",

    // Belly patch
    owluko_simpbelly_patch: "belly_group",

    // Head / Facial mask (p16..p18)
    owluko_simpp16: "head_group",
    owluko_simpfacial_mask_main: "head_group",
    owluko_simpp17: "head_group",
    owluko_simpp18: "head_group",

    // Left Eye (p19..p26)
    owluko_simpp19: "eye_l_group",
    owluko_simpp20: "eye_l_group",
    owluko_simpp21: "eye_l_group",
    owluko_simpp22: "eye_l_group",
    owluko_simpp23: "eye_l_group",
    owluko_simpp24: "eye_l_group",
    owluko_simpp25: "eye_l_group",
    owluko_simpp26: "eye_l_group",

    // Right Eye (p27..p34)
    owluko_simpp27: "eye_r_group",
    owluko_simpp28: "eye_r_group",
    owluko_simpp29: "eye_r_group",
    owluko_simpp30: "eye_r_group",
    owluko_simpp31: "eye_r_group",
    owluko_simpp32: "eye_r_group",
    owluko_simpp33: "eye_r_group",
    owluko_simpp34: "eye_r_group",

    // Beak
    owluko_simpp35: "beak_group",
    owluko_simpbeak_cone: "beak_group",
    owluko_simpp36: "beak_group",
    owluko_simpp37: "beak_group",
    owluko_simpp38: "beak_group"
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

  // Add Eyelid Covers & Seams for BOTH Eyes (Centered at 0, 0 in eye_l_group and eye_r_group)
  const r_eye = 64.0;
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

  // Left Eye Eyelid
  processedShapes.push(
    {
      id: "eyelid_l_cover",
      type: "polygon",
      parent: "eye_l_group",
      x: 0,
      y: 0,
      points: eyelidCoverPoints,
      opacity: 0,
      fill: { color: "#FAF6EC" }
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
      stroke: { color: "#5C3D2E", thickness: 3.6, cap: "round", join: "round" }
    }
  );

  // Right Eye Eyelid
  processedShapes.push(
    {
      id: "eyelid_r_cover",
      type: "polygon",
      parent: "eye_r_group",
      x: 0,
      y: 0,
      points: eyelidCoverPoints,
      opacity: 0,
      fill: { color: "#FAF6EC" }
    },
    {
      id: "eyelid_r_seam",
      type: "polygon",
      closed: false,
      parent: "eye_r_group",
      x: 0,
      y: 0,
      points: closedEyeArc,
      opacity: 0,
      stroke: { color: "#5C3D2E", thickness: 3.6, cap: "round", join: "round" }
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
        // Synchronized Conscious Blink at frame 70..86
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
        },
        {
          target: "eyelid_r_cover",
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
          target: "eyelid_r_seam",
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
        },
        {
          target: "eyelid_r_cover",
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
          target: "eyelid_r_seam",
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
    },
    {
      name: "wink",
      fps: 60,
      duration: 30,
      loop: "one-shot",
      tracks: [
        {
          target: "eyelid_r_cover",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 6, value: 1, easing: "ease-in" },
            { frame: 20, value: 1 },
            { frame: 28, value: 0, easing: "ease-out" },
            { frame: 30, value: 0 }
          ]
        },
        {
          target: "eyelid_r_seam",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 6, value: 1, easing: "ease-in" },
            { frame: 20, value: 1 },
            { frame: 28, value: 0, easing: "ease-out" },
            { frame: 30, value: 0 }
          ]
        }
      ]
    }
  ];

  // 3. State Machine Declaration
  const stateMachine = {
    name: "SM_Owluko",
    inputs: [
      { name: "triggerBlink", type: "trigger" },
      { name: "triggerWink", type: "trigger" }
    ],
    states: [
      { name: "Respiration", animation: "idle" },
      { name: "Blink_State", animation: "blink" },
      { name: "Wink_State", animation: "wink" }
    ],
    transitions: [
      { from: "entry", to: "Respiration" },
      { from: "Respiration", to: "Blink_State", condition: { input: "triggerBlink" } },
      { from: "Blink_State", to: "Respiration", exitTimeMs: 333 },
      { from: "Respiration", to: "Wink_State", condition: { input: "triggerWink" } },
      { from: "Wink_State", to: "Respiration", exitTimeMs: 500 }
    ]
  };

  const scene = {
    artboard: {
      name: "Owluko_Simplified",
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

  console.log("=== CANONICAL SIMPLIFIED OWLUKO COMPILED SUCCESSFULLY ===");
}

buildOwlukoSimplifiedRive().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
