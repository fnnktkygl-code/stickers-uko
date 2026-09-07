import sys, os

content = r'''const fs = require("fs");
const path = require("path");
const { callMcpTool } = require("./rive_mcp_client.js");

const kappa = 0.5522847498307936;

async function buildOwlukoSixStatesRive() {
  console.log("===================================================================");
  console.log("  BUILDING CANONICAL OWLUKO 6-STATE MASTER RIVE RIG                ");
  console.log("  - 00_idle, 01_waving, 02_celebrating, 03_thinking, 04_error_404, 06_sleeping");
  console.log("  - Pure Vector Bezier Splines, 100% Anatomical Bilateral Symmetry ");
  console.log("  - Unified State Machine (SM_Owluko) with Trigger & Bool Inputs    ");
  console.log("===================================================================");

  const fragmentPath = path.resolve(__dirname, "../scratch/owluko_waving.scene.json");
  if (!fs.existsSync(fragmentPath)) {
    throw new Error("Missing fragment: " + fragmentPath);
  }
  const fragment = JSON.parse(fs.readFileSync(fragmentPath, "utf-8"));
  console.log(`Loaded fragment with ${fragment.shapes.length} imported shapes.`);

  // 1. Define Rig Groups Hierarchy (1152 x 1024 Artboard Space)
  // Centered at x: 576. Left and right symmetric pivots.
  const groups = [
    { id: "root", x: 576, y: 876 },
    { id: "shadow_group", parent: "root", x: 0, y: 0 },
    { id: "feet_group", parent: "root", x: 0, y: 0 },
    { id: "body_group", parent: "root", x: 0, y: -378 }, // global: (576, 498)
    { id: "wings_group", parent: "body_group", x: 0, y: 0 },
    { id: "wing_l_group", parent: "wings_group", x: -288, y: 92 }, // global: (288, 590) - left resting wing
    { id: "wing_r_rest_group", parent: "wings_group", x: 288, y: 92 }, // global: (864, 590) - right resting wing
    { id: "wing_r_wave_group", parent: "wings_group", x: 258, y: 62 }, // global: (834, 560) - right wave pivot
    { id: "wing_l_wave_group", parent: "wings_group", x: -258, y: 62 }, // global: (318, 560) - left wave pivot (celebration)
    { id: "belly_group", parent: "body_group", x: 0, y: 0 },
    { id: "head_group", parent: "body_group", x: 0, y: -126 },
    { id: "eye_l_group", parent: "head_group", x: -114, y: -10 },
    { id: "eye_r_group", parent: "head_group", x: 114, y: -10 },
    { id: "beak_group", parent: "head_group", x: 0, y: 44 }
  ];

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

  // Create mirrored left waving wing for celebration
  const rWaveWing = fragment.shapes.find(s => s.id === "owluko_wave_wing_wave_smooth_main");
  const lWaveWing = JSON.parse(JSON.stringify(rWaveWing));
  lWaveWing.id = "owluko_wave_wing_wave_l_main";
  const dxR = lWaveWing.x - 512;
  lWaveWing.x = 512 - dxR;
  for (const sp of (lWaveWing.subpaths || [])) {
    for (const pt of (sp.points || [])) {
      pt.x = -pt.x;
      if (pt.cubic) {
        pt.cubic.rotation = 180.0 - pt.cubic.rotation;
        pt.cubic.inRotation = 180.0 - pt.cubic.inRotation;
      }
    }
  }
  if (lWaveWing.fill && lWaveWing.fill.gradient) {
    const g = lWaveWing.fill.gradient;
    if (g.start) g.start.x = -g.start.x;
    if (g.end) g.end.x = -g.end.x;
  }
  fragment.shapes.push(lWaveWing);

  // Map each shape to its target group
  const shapeTargetGroup = {
    owluko_wave_ground_shadow_outer: "shadow_group",
    owluko_wave_ground_shadow_dense: "shadow_group",

    owluko_wave_toe_l1: "feet_group",
    owluko_wave_toe_l2: "feet_group",
    owluko_wave_toe_l3: "feet_group",
    owluko_wave_toe_l1_hi: "feet_group",
    owluko_wave_toe_l2_hi: "feet_group",
    owluko_wave_toe_l3_hi: "feet_group",

    owluko_wave_toe_r1: "feet_group",
    owluko_wave_toe_r2: "feet_group",
    owluko_wave_toe_r3: "feet_group",
    owluko_wave_toe_r1_hi: "feet_group",
    owluko_wave_toe_r2_hi: "feet_group",
    owluko_wave_toe_r3_hi: "feet_group",

    owluko_wave_wing_left_shadow: "wing_l_group",
    owluko_wave_wing_left_main: "wing_l_group",

    owluko_wave_wing_wave_l_main: "wing_l_wave_group",
    owluko_wave_wing_wave_shadow: "wing_r_wave_group",
    owluko_wave_wing_wave_smooth_main: "wing_r_wave_group",

    owluko_wave_body_silhouette: "body_group",

    owluko_wave_wing_right_shadow: "wing_r_rest_group",
    owluko_wave_wing_right_main: "wing_r_rest_group",

    owluko_wave_belly_patch: "belly_group",

    owluko_wave_facial_mask_shadow: "head_group",
    owluko_wave_facial_mask_main: "head_group",
    owluko_wave_socket_left: "head_group",
    owluko_wave_socket_right: "head_group",

    owluko_wave_eye_l_outer_rim: "eye_l_group",
    owluko_wave_eye_l_iris: "eye_l_group",
    owluko_wave_eye_l_crescent: "eye_l_group",
    owluko_wave_eye_l_pupil: "eye_l_group",
    owluko_wave_eye_l_pupil_inner: "eye_l_group",
    owluko_wave_eye_l_glint_major: "eye_l_group",
    owluko_wave_eye_l_glint_minor: "eye_l_group",
    owluko_wave_happy_eye_l: "eye_l_group",

    owluko_wave_eye_r_outer_rim: "eye_r_group",
    owluko_wave_eye_r_iris: "eye_r_group",
    owluko_wave_eye_r_crescent: "eye_r_group",
    owluko_wave_eye_r_pupil: "eye_r_group",
    owluko_wave_eye_r_pupil_inner: "eye_r_group",
    owluko_wave_eye_r_glint_major: "eye_r_group",
    owluko_wave_eye_r_glint_minor: "eye_r_group",
    owluko_wave_happy_eye_r: "eye_r_group",

    owluko_wave_beak_shadow: "beak_group",
    owluko_wave_beak_cone: "beak_group",
    owluko_wave_beak_highlight: "beak_group",
    owluko_wave_beak_tip_point: "beak_group"
  };

  // Eyelids geometry for natural blinking
  const r_eye = 64.0;
  const eyelidCoverPoints = [
    { x: -r_eye, y: 0, cubic: { inRotation: 90, inDistance: r_eye * kappa, rotation: 270, outDistance: r_eye * kappa } },
    { x: 0, y: -r_eye, cubic: { inRotation: 180, inDistance: r_eye * kappa, rotation: 0, outDistance: r_eye * kappa } },
    { x: r_eye, y: 0, cubic: { inRotation: 270, inDistance: r_eye * kappa, rotation: 90, outDistance: r_eye * kappa } },
    { x: 0, y: r_eye, cubic: { inRotation: 0, inDistance: r_eye * kappa, rotation: 180, outDistance: r_eye * kappa } }
  ];

  const closedEyeArc = [
    { x: -40, y: 3, cubic: { inRotation: 0, inDistance: 0, rotation: 22, outDistance: 20 } },
    { x: 0, y: 16, cubic: { inRotation: -22, inDistance: 20, rotation: -22, outDistance: 20 } },
    { x: 40, y: 3, cubic: { inRotation: 22, inDistance: 20, rotation: 0, outDistance: 0 } }
  ];

  const eyelidL = {
    id: "eyelid_l_cover",
    type: "polygon",
    parent: "eye_l_group",
    x: 0,
    y: 0,
    points: eyelidCoverPoints,
    opacity: 0,
    fill: { color: "#FAF6EC" }
  };
  const eyelidLSeam = {
    id: "eyelid_l_seam",
    type: "polygon",
    closed: false,
    parent: "eye_l_group",
    x: 0,
    y: 0,
    points: closedEyeArc,
    opacity: 0,
    stroke: { color: "#5C3D2E", thickness: 3.6, cap: "round", join: "round" }
  };
  const eyelidR = {
    id: "eyelid_r_cover",
    type: "polygon",
    parent: "eye_r_group",
    x: 0,
    y: 0,
    points: eyelidCoverPoints,
    opacity: 0,
    fill: { color: "#FAF6EC" }
  };
  const eyelidRSeam = {
    id: "eyelid_r_seam",
    type: "polygon",
    closed: false,
    parent: "eye_r_group",
    x: 0,
    y: 0,
    points: closedEyeArc,
    opacity: 0,
    stroke: { color: "#5C3D2E", thickness: 3.6, cap: "round", join: "round" }
  };

  const artboardWidth = 1152;
  const dx = (artboardWidth - 1024) / 2; // 64px shift
  const shapeMap = {};
  for (const s of fragment.shapes) {
    s.x += dx;
    const targetGid = shapeTargetGroup[s.id];
    if (targetGid) {
      const gOrigin = getGroupGlobal(targetGid);
      s.parent = targetGid;
      s.x = s.x - gOrigin.gx;
      s.y = s.y - gOrigin.gy;
    }
    if (s.id.startsWith("owluko_wave_wing_wave_")) {
      s.opacity = 0;
    }
    if (s.id === "owluko_wave_happy_eye_l" || s.id === "owluko_wave_happy_eye_r") {
      s.opacity = 0;
    }
    shapeMap[s.id] = s;
  }

  const orderedShapeIds = [
    // Shadows
    "owluko_wave_ground_shadow_outer",
    "owluko_wave_ground_shadow_dense",
    // Feet
    "owluko_wave_toe_l1",
    "owluko_wave_toe_l2",
    "owluko_wave_toe_l3",
    "owluko_wave_toe_l1_hi",
    "owluko_wave_toe_l2_hi",
    "owluko_wave_toe_l3_hi",
    "owluko_wave_toe_r1",
    "owluko_wave_toe_r2",
    "owluko_wave_toe_r3",
    "owluko_wave_toe_r1_hi",
    "owluko_wave_toe_r2_hi",
    "owluko_wave_toe_r3_hi",
    // Raised Wings (Behind Body)
    "owluko_wave_wing_wave_l_main",
    "owluko_wave_wing_wave_shadow",
    "owluko_wave_wing_wave_smooth_main",
    // Body Silhouette
    "owluko_wave_body_silhouette",
    // Flank Resting Wings
    "owluko_wave_wing_left_shadow",
    "owluko_wave_wing_left_main",
    "owluko_wave_wing_right_shadow",
    "owluko_wave_wing_right_main",
    // Belly
    "owluko_wave_belly_patch",
    // Head Mask
    "owluko_wave_facial_mask_shadow",
    "owluko_wave_facial_mask_main",
    "owluko_wave_socket_left",
    "owluko_wave_socket_right",
    // Left Eye
    "owluko_wave_eye_l_outer_rim",
    "owluko_wave_eye_l_iris",
    "owluko_wave_eye_l_crescent",
    "owluko_wave_eye_l_pupil",
    "owluko_wave_eye_l_pupil_inner",
    "owluko_wave_eye_l_glint_major",
    "owluko_wave_eye_l_glint_minor",
    "eyelid_l_cover",
    "eyelid_l_seam",
    "owluko_wave_happy_eye_l",
    // Right Eye
    "owluko_wave_eye_r_outer_rim",
    "owluko_wave_eye_r_iris",
    "owluko_wave_eye_r_crescent",
    "owluko_wave_eye_r_pupil",
    "owluko_wave_eye_r_pupil_inner",
    "owluko_wave_eye_r_glint_major",
    "owluko_wave_eye_r_glint_minor",
    "eyelid_r_cover",
    "eyelid_r_seam",
    "owluko_wave_happy_eye_r",
    // Beak
    "owluko_wave_beak_shadow",
    "owluko_wave_beak_cone",
    "owluko_wave_beak_highlight",
    "owluko_wave_beak_tip_point"
  ];

  const processedShapes = [];
  for (const id of orderedShapeIds) {
    if (id === "eyelid_l_cover") processedShapes.push(eyelidL);
    else if (id === "eyelid_l_seam") processedShapes.push(eyelidLSeam);
    else if (id === "eyelid_r_cover") processedShapes.push(eyelidR);
    else if (id === "eyelid_r_seam") processedShapes.push(eyelidRSeam);
    else if (shapeMap[id]) processedShapes.push(shapeMap[id]);
  }

  // 2. Animations Definition (ALL 6 CANONICAL STATES)
  const animations = [
    // -------------------------------------------------------------
    // 00_IDLE: Calm breathing, subtle micro-bob, natural blinking (120 frames = 2.0s loop)
    // -------------------------------------------------------------
    {
      name: "idle",
      fps: 60,
      duration: 120,
      loop: "loop",
      tracks: [
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
          target: "wing_r_rest_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0.0 },
            { frame: 60, value: 1.6, easing: "ease-in-out" },
            { frame: 120, value: 0.0, easing: "ease-in-out" }
          ]
        },
        {
          target: "owluko_wave_wing_left_main",
          property: "opacity",
          keyframes: [{ frame: 0, value: 1 }, { frame: 120, value: 1 }]
        },
        {
          target: "owluko_wave_wing_left_shadow",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0.22 }, { frame: 120, value: 0.22 }]
        },
        {
          target: "owluko_wave_wing_right_main",
          property: "opacity",
          keyframes: [{ frame: 0, value: 1 }, { frame: 120, value: 1 }]
        },
        {
          target: "owluko_wave_wing_right_shadow",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0.22 }, { frame: 120, value: 0.22 }]
        },
        {
          target: "owluko_wave_wing_wave_smooth_main",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0 }, { frame: 120, value: 0 }]
        },
        {
          target: "owluko_wave_wing_wave_l_main",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0 }, { frame: 120, value: 0 }]
        },
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
        {
          target: "shadow_group",
          property: "scaleX",
          keyframes: [
            { frame: 0, value: 1.0 },
            { frame: 60, value: 1.03, easing: "ease-in-out" },
            { frame: 120, value: 1.0, easing: "ease-in-out" }
          ]
        },
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
        },
        {
          target: "owluko_wave_happy_eye_l",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0 }, { frame: 120, value: 0 }]
        },
        {
          target: "owluko_wave_happy_eye_r",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0 }, { frame: 120, value: 0 }]
        }
      ]
    },

    // -------------------------------------------------------------
    // 01_WAVING: Full waving performance (240 frames = 4.0s)
    // -------------------------------------------------------------
    {
      name: "waving",
      fps: 60,
      duration: 240,
      loop: "one-shot",
      tracks: [
        {
          target: "owluko_wave_wing_right_main",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 1 },
            { frame: 30, value: 1 },
            { frame: 45, value: 0, easing: "ease-out" },
            { frame: 200, value: 0 },
            { frame: 218, value: 1, easing: "ease-in" },
            { frame: 240, value: 1 }
          ]
        },
        {
          target: "owluko_wave_wing_right_shadow",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0.22 },
            { frame: 30, value: 0.22 },
            { frame: 45, value: 0, easing: "ease-out" },
            { frame: 200, value: 0 },
            { frame: 218, value: 0.22, easing: "ease-in" },
            { frame: 240, value: 0.22 }
          ]
        },
        {
          target: "owluko_wave_wing_wave_smooth_main",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 30, value: 0 },
            { frame: 45, value: 1, easing: "ease-in" },
            { frame: 200, value: 1 },
            { frame: 218, value: 0, easing: "ease-out" },
            { frame: 240, value: 0 }
          ]
        },
        {
          target: "owluko_wave_wing_left_main",
          property: "opacity",
          keyframes: [{ frame: 0, value: 1 }, { frame: 240, value: 1 }]
        },
        {
          target: "owluko_wave_wing_left_shadow",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0.22 }, { frame: 240, value: 0.22 }]
        },
        {
          target: "owluko_wave_wing_wave_l_main",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0 }, { frame: 240, value: 0 }]
        },
        {
          target: "wing_r_wave_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: -18.0 },
            { frame: 30, value: -18.0 },
            { frame: 45, value: -6.0, easing: "ease-out" },
            { frame: 60, value: 0.0, easing: "ease-in-out" },
            { frame: 85, value: -10.0, easing: "ease-in-out" },
            { frame: 110, value: 8.0, easing: "ease-in-out" },
            { frame: 135, value: -8.0, easing: "ease-in-out" },
            { frame: 155, value: 4.0, easing: "ease-in-out" },
            { frame: 175, value: 0.0, easing: "ease-in-out" },
            { frame: 195, value: -8.0, easing: "ease-in-out" },
            { frame: 215, value: -16.0, easing: "ease-in-out" },
            { frame: 228, value: -18.0, easing: "ease-out" },
            { frame: 240, value: -18.0 }
          ]
        },
        {
          target: "head_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0.0 },
            { frame: 30, value: -0.8, easing: "ease-out" },
            { frame: 60, value: 1.0, easing: "ease-in-out" },
            { frame: 85, value: 1.6, easing: "ease-in-out" },
            { frame: 110, value: -1.2, easing: "ease-in-out" },
            { frame: 135, value: 1.8, easing: "ease-in-out" },
            { frame: 150, value: 2.2, easing: "ease-in-out" },
            { frame: 175, value: 0.6, easing: "ease-in-out" },
            { frame: 210, value: -0.4, easing: "ease-in-out" },
            { frame: 240, value: 0.0, easing: "ease-out" }
          ]
        },
        {
          target: "head_group",
          property: "y",
          keyframes: [
            { frame: 0, value: -126.0 },
            { frame: 30, value: -125.0, easing: "ease-out" },
            { frame: 60, value: -128.5, easing: "ease-in-out" },
            { frame: 85, value: -127.0, easing: "ease-in-out" },
            { frame: 110, value: -128.0, easing: "ease-in-out" },
            { frame: 145, value: -124.0, easing: "ease-in-out" },
            { frame: 175, value: -126.5, easing: "ease-in-out" },
            { frame: 210, value: -125.5, easing: "ease-in-out" },
            { frame: 240, value: -126.0, easing: "ease-out" }
          ]
        },
        {
          target: "body_group",
          property: "scaleY",
          keyframes: [
            { frame: 0, value: 1.0 },
            { frame: 30, value: 0.992, easing: "ease-in" },
            { frame: 60, value: 1.018, easing: "ease-out" },
            { frame: 85, value: 1.008, easing: "ease-in-out" },
            { frame: 110, value: 1.014, easing: "ease-in-out" },
            { frame: 145, value: 0.995, easing: "ease-in-out" },
            { frame: 175, value: 1.008, easing: "ease-in-out" },
            { frame: 210, value: 0.994, easing: "ease-in-out" },
            { frame: 240, value: 1.0, easing: "ease-out" }
          ]
        },
        {
          target: "body_group",
          property: "scaleX",
          keyframes: [
            { frame: 0, value: 1.0 },
            { frame: 30, value: 1.006, easing: "ease-in" },
            { frame: 60, value: 0.990, easing: "ease-out" },
            { frame: 85, value: 0.995, easing: "ease-in-out" },
            { frame: 110, value: 0.991, easing: "ease-in-out" },
            { frame: 145, value: 1.005, easing: "ease-in-out" },
            { frame: 175, value: 0.994, easing: "ease-in-out" },
            { frame: 210, value: 1.005, easing: "ease-in-out" },
            { frame: 240, value: 1.0, easing: "ease-out" }
          ]
        },
        {
          target: "wing_l_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0.0 },
            { frame: 30, value: 0.6, easing: "ease-in" },
            { frame: 60, value: -1.2, easing: "ease-out" },
            { frame: 85, value: -1.8, easing: "ease-in-out" },
            { frame: 110, value: 0.8, easing: "ease-in-out" },
            { frame: 135, value: -1.4, easing: "ease-in-out" },
            { frame: 160, value: 0.4, easing: "ease-in-out" },
            { frame: 210, value: -0.8, easing: "ease-in-out" },
            { frame: 240, value: 0.0, easing: "ease-out" }
          ]
        },
        {
          target: "eyelid_l_cover",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 120, value: 0 },
            { frame: 130, value: 1, easing: "ease-in" },
            { frame: 155, value: 1 },
            { frame: 168, value: 0, easing: "ease-out" },
            { frame: 240, value: 0 }
          ]
        },
        {
          target: "eyelid_r_cover",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 120, value: 0 },
            { frame: 130, value: 1, easing: "ease-in" },
            { frame: 155, value: 1 },
            { frame: 168, value: 0, easing: "ease-out" },
            { frame: 240, value: 0 }
          ]
        },
        {
          target: "owluko_wave_happy_eye_l",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 120, value: 0 },
            { frame: 130, value: 1, easing: "ease-in" },
            { frame: 155, value: 1 },
            { frame: 168, value: 0, easing: "ease-out" },
            { frame: 240, value: 0 }
          ]
        },
        {
          target: "owluko_wave_happy_eye_r",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 120, value: 0 },
            { frame: 130, value: 1, easing: "ease-in" },
            { frame: 155, value: 1 },
            { frame: 168, value: 0, easing: "ease-out" },
            { frame: 240, value: 0 }
          ]
        }
      ]
    },

    // -------------------------------------------------------------
    // 02_CELEBRATING: Squat anticipation, vertical victory leap, both wings raised, joyful eyes (180 frames = 3.0s loop)
    // -------------------------------------------------------------
    {
      name: "celebrating",
      fps: 60,
      duration: 180,
      loop: "loop",
      tracks: [
        // Flank resting wings fade during leap, restored upon landing
        {
          target: "owluko_wave_wing_left_main",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 1 },
            { frame: 25, value: 1 },
            { frame: 40, value: 0, easing: "ease-out" },
            { frame: 135, value: 0 },
            { frame: 150, value: 1, easing: "ease-in" },
            { frame: 180, value: 1 }
          ]
        },
        {
          target: "owluko_wave_wing_left_shadow",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0.22 },
            { frame: 25, value: 0.22 },
            { frame: 40, value: 0, easing: "ease-out" },
            { frame: 135, value: 0 },
            { frame: 150, value: 0.22, easing: "ease-in" },
            { frame: 180, value: 0.22 }
          ]
        },
        {
          target: "owluko_wave_wing_right_main",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 1 },
            { frame: 25, value: 1 },
            { frame: 40, value: 0, easing: "ease-out" },
            { frame: 135, value: 0 },
            { frame: 150, value: 1, easing: "ease-in" },
            { frame: 180, value: 1 }
          ]
        },
        {
          target: "owluko_wave_wing_right_shadow",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0.22 },
            { frame: 25, value: 0.22 },
            { frame: 40, value: 0, easing: "ease-out" },
            { frame: 135, value: 0 },
            { frame: 150, value: 0.22, easing: "ease-in" },
            { frame: 180, value: 0.22 }
          ]
        },
        // Both raised waving wings appear during jump
        {
          target: "owluko_wave_wing_wave_l_main",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 25, value: 0 },
            { frame: 40, value: 1, easing: "ease-in" },
            { frame: 135, value: 1 },
            { frame: 150, value: 0, easing: "ease-out" },
            { frame: 180, value: 0 }
          ]
        },
        {
          target: "owluko_wave_wing_wave_smooth_main",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 25, value: 0 },
            { frame: 40, value: 1, easing: "ease-in" },
            { frame: 135, value: 1 },
            { frame: 150, value: 0, easing: "ease-out" },
            { frame: 180, value: 0 }
          ]
        },
        // Wing rotations: Flapping celebration gesture in mid-air
        {
          target: "wing_l_wave_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 18.0 },
            { frame: 25, value: 18.0 },
            { frame: 45, value: 0.0, easing: "ease-out" },
            { frame: 65, value: -16.0, easing: "ease-in-out" },
            { frame: 85, value: 12.0, easing: "ease-in-out" },
            { frame: 105, value: -14.0, easing: "ease-in-out" },
            { frame: 125, value: 8.0, easing: "ease-in-out" },
            { frame: 145, value: 18.0, easing: "ease-out" },
            { frame: 180, value: 18.0 }
          ]
        },
        {
          target: "wing_r_wave_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: -18.0 },
            { frame: 25, value: -18.0 },
            { frame: 45, value: 0.0, easing: "ease-out" },
            { frame: 65, value: 16.0, easing: "ease-in-out" },
            { frame: 85, value: -12.0, easing: "ease-in-out" },
            { frame: 105, value: 14.0, easing: "ease-in-out" },
            { frame: 125, value: -8.0, easing: "ease-in-out" },
            { frame: 145, value: -18.0, easing: "ease-out" },
            { frame: 180, value: -18.0 }
          ]
        },
        // Vertical Root Hop: Squat at frame 25 -> Leap up -85px at frame 65..95 -> Touchdown at frame 145
        {
          target: "root",
          property: "y",
          keyframes: [
            { frame: 0, value: 876 },
            { frame: 25, value: 896, easing: "ease-in" }, // squat anticipation
            { frame: 50, value: 810, easing: "ease-out" }, // explosive jump
            { frame: 75, value: 785, easing: "ease-in-out" }, // apex float
            { frame: 100, value: 792, easing: "ease-in-out" },
            { frame: 125, value: 825, easing: "ease-in" },
            { frame: 145, value: 892, easing: "ease-in-out" }, // landing squash
            { frame: 165, value: 872, easing: "ease-out" },
            { frame: 180, value: 876 }
          ]
        },
        // Torso Squash & Stretch
        {
          target: "body_group",
          property: "scaleY",
          keyframes: [
            { frame: 0, value: 1.0 },
            { frame: 25, value: 0.92, easing: "ease-in" }, // squash
            { frame: 45, value: 1.09, easing: "ease-out" }, // stretch on takeoff
            { frame: 75, value: 1.04, easing: "ease-in-out" },
            { frame: 125, value: 1.06, easing: "ease-in" },
            { frame: 145, value: 0.93, easing: "ease-out" }, // landing impact
            { frame: 165, value: 1.02, easing: "ease-out" },
            { frame: 180, value: 1.0 }
          ]
        },
        {
          target: "body_group",
          property: "scaleX",
          keyframes: [
            { frame: 0, value: 1.0 },
            { frame: 25, value: 1.08, easing: "ease-in" },
            { frame: 45, value: 0.93, easing: "ease-out" },
            { frame: 75, value: 0.97, easing: "ease-in-out" },
            { frame: 125, value: 0.95, easing: "ease-in" },
            { frame: 145, value: 1.07, easing: "ease-out" },
            { frame: 165, value: 0.98, easing: "ease-out" },
            { frame: 180, value: 1.0 }
          ]
        },
        // Ground Shadow expands/contracts with leap height
        {
          target: "shadow_group",
          property: "scaleX",
          keyframes: [
            { frame: 0, value: 1.0 },
            { frame: 25, value: 1.15, easing: "ease-in" },
            { frame: 75, value: 0.65, easing: "ease-out" }, // shrinks at jump apex
            { frame: 145, value: 1.18, easing: "ease-in" }, // expands on touchdown
            { frame: 180, value: 1.0 }
          ]
        },
        // Joyful smiling eyes during victory peak (frames 45..140)
        {
          target: "eyelid_l_cover",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 35, value: 0 },
            { frame: 45, value: 1, easing: "ease-in" },
            { frame: 130, value: 1 },
            { frame: 145, value: 0, easing: "ease-out" },
            { frame: 180, value: 0 }
          ]
        },
        {
          target: "eyelid_r_cover",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 35, value: 0 },
            { frame: 45, value: 1, easing: "ease-in" },
            { frame: 130, value: 1 },
            { frame: 145, value: 0, easing: "ease-out" },
            { frame: 180, value: 0 }
          ]
        },
        {
          target: "owluko_wave_happy_eye_l",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 35, value: 0 },
            { frame: 45, value: 1, easing: "ease-in" },
            { frame: 130, value: 1 },
            { frame: 145, value: 0, easing: "ease-out" },
            { frame: 180, value: 0 }
          ]
        },
        {
          target: "owluko_wave_happy_eye_r",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 35, value: 0 },
            { frame: 45, value: 1, easing: "ease-in" },
            { frame: 130, value: 1 },
            { frame: 145, value: 0, easing: "ease-out" },
            { frame: 180, value: 0 }
          ]
        }
      ]
    },

    // -------------------------------------------------------------
    // 03_THINKING: Inquisitive head tilt, contemplative gaze, thoughtful blinks (180 frames = 3.0s loop)
    // -------------------------------------------------------------
    {
      name: "thinking",
      fps: 60,
      duration: 180,
      loop: "loop",
      tracks: [
        {
          target: "owluko_wave_wing_left_main",
          property: "opacity",
          keyframes: [{ frame: 0, value: 1 }, { frame: 180, value: 1 }]
        },
        {
          target: "owluko_wave_wing_left_shadow",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0.22 }, { frame: 180, value: 0.22 }]
        },
        {
          target: "owluko_wave_wing_right_main",
          property: "opacity",
          keyframes: [{ frame: 0, value: 1 }, { frame: 180, value: 1 }]
        },
        {
          target: "owluko_wave_wing_right_shadow",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0.22 }, { frame: 180, value: 0.22 }]
        },
        {
          target: "owluko_wave_wing_wave_smooth_main",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0 }, { frame: 180, value: 0 }]
        },
        {
          target: "owluko_wave_wing_wave_l_main",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0 }, { frame: 180, value: 0 }]
        },
        // Marked Head Tilt: Inquisitive lean to the right (+6.5°), saccade to the left (-5.2°)
        {
          target: "head_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0.0 },
            { frame: 35, value: 6.5, easing: "ease-in-out" },
            { frame: 80, value: 7.2, easing: "ease-in-out" },
            { frame: 110, value: -5.2, easing: "ease-in-out" },
            { frame: 145, value: -4.5, easing: "ease-in-out" },
            { frame: 180, value: 0.0, easing: "ease-in-out" }
          ]
        },
        {
          target: "head_group",
          property: "y",
          keyframes: [
            { frame: 0, value: -126.0 },
            { frame: 45, value: -129.0, easing: "ease-in-out" },
            { frame: 110, value: -127.5, easing: "ease-in-out" },
            { frame: 180, value: -126.0, easing: "ease-in-out" }
          ]
        },
        // Body subtle counter-balance
        {
          target: "body_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0.0 },
            { frame: 45, value: -1.2, easing: "ease-in-out" },
            { frame: 110, value: 1.0, easing: "ease-in-out" },
            { frame: 180, value: 0.0, easing: "ease-in-out" }
          ]
        },
        {
          target: "body_group",
          property: "scaleY",
          keyframes: [
            { frame: 0, value: 1.0 },
            { frame: 90, value: 1.015, easing: "ease-in-out" },
            { frame: 180, value: 1.0, easing: "ease-in-out" }
          ]
        },
        // Wings micro-adjust to tilt
        {
          target: "wing_l_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0.0 },
            { frame: 45, value: -2.5, easing: "ease-in-out" },
            { frame: 110, value: 1.8, easing: "ease-in-out" },
            { frame: 180, value: 0.0, easing: "ease-in-out" }
          ]
        },
        {
          target: "wing_r_rest_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0.0 },
            { frame: 45, value: 1.5, easing: "ease-in-out" },
            { frame: 110, value: -2.2, easing: "ease-in-out" },
            { frame: 180, value: 0.0, easing: "ease-in-out" }
          ]
        },
        // Thoughtful contemplative blink in middle of thinking (frames 70..85)
        {
          target: "eyelid_l_cover",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 68, value: 0 },
            { frame: 75, value: 1, easing: "ease-in" },
            { frame: 82, value: 1 },
            { frame: 88, value: 0, easing: "ease-out" },
            { frame: 180, value: 0 }
          ]
        },
        {
          target: "eyelid_l_seam",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 68, value: 0 },
            { frame: 75, value: 1, easing: "ease-in" },
            { frame: 82, value: 1 },
            { frame: 88, value: 0, easing: "ease-out" },
            { frame: 180, value: 0 }
          ]
        },
        {
          target: "eyelid_r_cover",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 68, value: 0 },
            { frame: 75, value: 1, easing: "ease-in" },
            { frame: 82, value: 1 },
            { frame: 88, value: 0, easing: "ease-out" },
            { frame: 180, value: 0 }
          ]
        },
        {
          target: "eyelid_r_seam",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 68, value: 0 },
            { frame: 75, value: 1, easing: "ease-in" },
            { frame: 82, value: 1 },
            { frame: 88, value: 0, easing: "ease-out" },
            { frame: 180, value: 0 }
          ]
        }
      ]
    },

    // -------------------------------------------------------------
    // 04_ERROR_404: Shock alert -> slumped squashed posture -> drooped wings & head (180 frames = 3.0s loop)
    // -------------------------------------------------------------
    {
      name: "error_404",
      fps: 60,
      duration: 180,
      loop: "loop",
      tracks: [
        {
          target: "owluko_wave_wing_left_main",
          property: "opacity",
          keyframes: [{ frame: 0, value: 1 }, { frame: 180, value: 1 }]
        },
        {
          target: "owluko_wave_wing_left_shadow",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0.22 }, { frame: 180, value: 0.22 }]
        },
        {
          target: "owluko_wave_wing_right_main",
          property: "opacity",
          keyframes: [{ frame: 0, value: 1 }, { frame: 180, value: 1 }]
        },
        {
          target: "owluko_wave_wing_right_shadow",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0.22 }, { frame: 180, value: 0.22 }]
        },
        {
          target: "owluko_wave_wing_wave_smooth_main",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0 }, { frame: 180, value: 0 }]
        },
        {
          target: "owluko_wave_wing_wave_l_main",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0 }, { frame: 180, value: 0 }]
        },
        // Slump down: Root moves downward into squashed posture
        {
          target: "root",
          property: "y",
          keyframes: [
            { frame: 0, value: 876 },
            { frame: 20, value: 866, easing: "ease-out" }, // startle hop
            { frame: 50, value: 914, easing: "ease-in" },  // slump into floor
            { frame: 120, value: 918, easing: "ease-in-out" },
            { frame: 180, value: 876, easing: "ease-out" }
          ]
        },
        // Body squash: wider and shorter
        {
          target: "body_group",
          property: "scaleY",
          keyframes: [
            { frame: 0, value: 1.0 },
            { frame: 20, value: 1.06, easing: "ease-out" }, // surprise stretch
            { frame: 50, value: 0.88, easing: "ease-in" },  // squashed slump
            { frame: 120, value: 0.89, easing: "ease-in-out" },
            { frame: 180, value: 1.0, easing: "ease-out" }
          ]
        },
        {
          target: "body_group",
          property: "scaleX",
          keyframes: [
            { frame: 0, value: 1.0 },
            { frame: 20, value: 0.95, easing: "ease-out" },
            { frame: 50, value: 1.10, easing: "ease-in" }, // flattened out
            { frame: 120, value: 1.09, easing: "ease-in-out" },
            { frame: 180, value: 1.0, easing: "ease-out" }
          ]
        },
        // Head bowed down low
        {
          target: "head_group",
          property: "y",
          keyframes: [
            { frame: 0, value: -126.0 },
            { frame: 20, value: -134.0, easing: "ease-out" },
            { frame: 50, value: -112.0, easing: "ease-in" }, // drooped head
            { frame: 120, value: -114.0, easing: "ease-in-out" },
            { frame: 180, value: -126.0, easing: "ease-out" }
          ]
        },
        // Drooped wings: Wings rotate inward / down against body
        {
          target: "wing_l_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0.0 },
            { frame: 20, value: -3.0, easing: "ease-out" },
            { frame: 50, value: 8.5, easing: "ease-in" }, // drooped inward
            { frame: 120, value: 7.5, easing: "ease-in-out" },
            { frame: 180, value: 0.0, easing: "ease-out" }
          ]
        },
        {
          target: "wing_r_rest_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0.0 },
            { frame: 20, value: 3.0, easing: "ease-out" },
            { frame: 50, value: -8.5, easing: "ease-in" }, // drooped inward
            { frame: 120, value: -7.5, easing: "ease-in-out" },
            { frame: 180, value: 0.0, easing: "ease-out" }
          ]
        },
        // Dense contact shadow during slump
        {
          target: "shadow_group",
          property: "scaleX",
          keyframes: [
            { frame: 0, value: 1.0 },
            { frame: 20, value: 0.90, easing: "ease-out" },
            { frame: 50, value: 1.20, easing: "ease-in" },
            { frame: 180, value: 1.0 }
          ]
        }
      ]
    },

    // -------------------------------------------------------------
    // 06_SLEEPING: Deep peaceful sleep, closed eyelids throughout, gentle 4.0s rhythmic breathing (240 frames = 4.0s loop)
    // -------------------------------------------------------------
    {
      name: "sleeping",
      fps: 60,
      duration: 240,
      loop: "loop",
      tracks: [
        {
          target: "owluko_wave_wing_left_main",
          property: "opacity",
          keyframes: [{ frame: 0, value: 1 }, { frame: 240, value: 1 }]
        },
        {
          target: "owluko_wave_wing_left_shadow",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0.22 }, { frame: 240, value: 0.22 }]
        },
        {
          target: "owluko_wave_wing_right_main",
          property: "opacity",
          keyframes: [{ frame: 0, value: 1 }, { frame: 240, value: 1 }]
        },
        {
          target: "owluko_wave_wing_right_shadow",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0.22 }, { frame: 240, value: 0.22 }]
        },
        {
          target: "owluko_wave_wing_wave_smooth_main",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0 }, { frame: 240, value: 0 }]
        },
        {
          target: "owluko_wave_wing_wave_l_main",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0 }, { frame: 240, value: 0 }]
        },
        // EYELIDS ARE 100% CLOSED THROUGHOUT ENTIRE SLEEP ANIMATION
        {
          target: "eyelid_l_cover",
          property: "opacity",
          keyframes: [{ frame: 0, value: 1 }, { frame: 240, value: 1 }]
        },
        {
          target: "eyelid_l_seam",
          property: "opacity",
          keyframes: [{ frame: 0, value: 1 }, { frame: 240, value: 1 }]
        },
        {
          target: "eyelid_r_cover",
          property: "opacity",
          keyframes: [{ frame: 0, value: 1 }, { frame: 240, value: 1 }]
        },
        {
          target: "eyelid_r_seam",
          property: "opacity",
          keyframes: [{ frame: 0, value: 1 }, { frame: 240, value: 1 }]
        },
        {
          target: "owluko_wave_happy_eye_l",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0 }, { frame: 240, value: 0 }]
        },
        {
          target: "owluko_wave_happy_eye_r",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0 }, { frame: 240, value: 0 }]
        },
        // Deep slow rhythmic respiration (4.0s breath cycle)
        {
          target: "body_group",
          property: "scaleY",
          keyframes: [
            { frame: 0, value: 0.985 },
            { frame: 120, value: 1.035, easing: "ease-in-out" },
            { frame: 240, value: 0.985, easing: "ease-in-out" }
          ]
        },
        {
          target: "body_group",
          property: "scaleX",
          keyframes: [
            { frame: 0, value: 1.015 },
            { frame: 120, value: 0.985, easing: "ease-in-out" },
            { frame: 240, value: 1.015, easing: "ease-in-out" }
          ]
        },
        // Head tucked slightly down and gently nodding in rhythm
        {
          target: "head_group",
          property: "y",
          keyframes: [
            { frame: 0, value: -122.0 },
            { frame: 120, value: -128.0, easing: "ease-in-out" },
            { frame: 240, value: -122.0, easing: "ease-in-out" }
          ]
        },
        {
          target: "head_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 3.5 },
            { frame: 120, value: 4.8, easing: "ease-in-out" },
            { frame: 240, value: 3.5, easing: "ease-in-out" }
          ]
        },
        // Flank wings breathing
        {
          target: "wing_l_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0.0 },
            { frame: 120, value: -2.2, easing: "ease-in-out" },
            { frame: 240, value: 0.0, easing: "ease-in-out" }
          ]
        },
        {
          target: "wing_r_rest_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0.0 },
            { frame: 120, value: 2.2, easing: "ease-in-out" },
            { frame: 240, value: 0.0, easing: "ease-in-out" }
          ]
        },
        {
          target: "shadow_group",
          property: "scaleX",
          keyframes: [
            { frame: 0, value: 1.02 },
            { frame: 120, value: 0.98, easing: "ease-in-out" },
            { frame: 240, value: 1.02, easing: "ease-in-out" }
          ]
        }
      ]
    },

    // -------------------------------------------------------------
    // EXTRA UTILITY TIMELINES: wave_loop, blink, wink
    // -------------------------------------------------------------
    {
      name: "wave_loop",
      fps: 60,
      duration: 120,
      loop: "loop",
      tracks: [
        {
          target: "owluko_wave_wing_right_main",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0 }, { frame: 120, value: 0 }]
        },
        {
          target: "owluko_wave_wing_right_shadow",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0 }, { frame: 120, value: 0 }]
        },
        {
          target: "owluko_wave_wing_wave_smooth_main",
          property: "opacity",
          keyframes: [{ frame: 0, value: 1 }, { frame: 120, value: 1 }]
        },
        {
          target: "owluko_wave_wing_wave_shadow",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0 }, { frame: 120, value: 0 }]
        },
        {
          target: "owluko_wave_wing_wave_l_main",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0 }, { frame: 120, value: 0 }]
        },
        {
          target: "wing_r_wave_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0.0 },
            { frame: 30, value: -10.0, easing: "ease-in-out" },
            { frame: 60, value: 0.0, easing: "ease-in-out" },
            { frame: 90, value: 8.0, easing: "ease-in-out" },
            { frame: 120, value: 0.0, easing: "ease-in-out" }
          ]
        },
        {
          target: "head_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0.0 },
            { frame: 30, value: 1.6, easing: "ease-in-out" },
            { frame: 60, value: 0.0, easing: "ease-in-out" },
            { frame: 90, value: -1.2, easing: "ease-in-out" },
            { frame: 120, value: 0.0, easing: "ease-in-out" }
          ]
        },
        {
          target: "body_group",
          property: "scaleY",
          keyframes: [
            { frame: 0, value: 1.0 },
            { frame: 30, value: 1.012, easing: "ease-in-out" },
            { frame: 60, value: 1.0, easing: "ease-in-out" },
            { frame: 90, value: 1.008, easing: "ease-in-out" },
            { frame: 120, value: 1.0, easing: "ease-in-out" }
          ]
        },
        {
          target: "body_group",
          property: "scaleX",
          keyframes: [
            { frame: 0, value: 1.0 },
            { frame: 30, value: 0.992, easing: "ease-in-out" },
            { frame: 60, value: 1.0, easing: "ease-in-out" },
            { frame: 90, value: 0.994, easing: "ease-in-out" },
            { frame: 120, value: 1.0, easing: "ease-in-out" }
          ]
        },
        {
          target: "eyelid_l_cover",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 50, value: 0 },
            { frame: 56, value: 1, easing: "ease-in" },
            { frame: 62, value: 1 },
            { frame: 68, value: 0, easing: "ease-out" },
            { frame: 120, value: 0 }
          ]
        },
        {
          target: "eyelid_l_seam",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 50, value: 0 },
            { frame: 56, value: 1, easing: "ease-in" },
            { frame: 62, value: 1 },
            { frame: 68, value: 0, easing: "ease-out" },
            { frame: 120, value: 0 }
          ]
        },
        {
          target: "eyelid_r_cover",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 50, value: 0 },
            { frame: 56, value: 1, easing: "ease-in" },
            { frame: 62, value: 1 },
            { frame: 68, value: 0, easing: "ease-out" },
            { frame: 120, value: 0 }
          ]
        },
        {
          target: "eyelid_r_seam",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 50, value: 0 },
            { frame: 56, value: 1, easing: "ease-in" },
            { frame: 62, value: 1 },
            { frame: 68, value: 0, easing: "ease-out" },
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

  // 3. State Machine Declaration (SM_Owluko)
  const stateMachine = {
    name: "SM_Owluko",
    inputs: [
      { name: "triggerIdle", type: "trigger" },
      { name: "triggerWave", type: "trigger" },
      { name: "triggerCelebrate", type: "trigger" },
      { name: "triggerThink", type: "trigger" },
      { name: "triggerError", type: "trigger" },
      { name: "triggerSleep", type: "trigger" },
      { name: "isWaving", type: "bool", initial: false },
      { name: "triggerBlink", type: "trigger" },
      { name: "triggerWink", type: "trigger" }
    ],
    states: [
      { name: "State_Idle", animation: "idle" },
      { name: "State_Waving", animation: "waving" },
      { name: "State_Celebrating", animation: "celebrating" },
      { name: "State_Thinking", animation: "thinking" },
      { name: "State_Error_404", animation: "error_404" },
      { name: "State_Sleeping", animation: "sleeping" },
      { name: "State_Wave_Continuous", animation: "wave_loop" },
      { name: "State_Blink", animation: "blink" },
      { name: "State_Wink", animation: "wink" }
    ],
    transitions: [
      { from: "entry", to: "State_Idle" },
      { from: "State_Idle", to: "State_Waving", condition: { input: "triggerWave" } },
      { from: "State_Waving", to: "State_Idle", exitTimeMs: 4000 },
      { from: "State_Idle", to: "State_Celebrating", condition: { input: "triggerCelebrate" } },
      { from: "State_Celebrating", to: "State_Idle", condition: { input: "triggerIdle" } },
      { from: "State_Idle", to: "State_Thinking", condition: { input: "triggerThink" } },
      { from: "State_Thinking", to: "State_Idle", condition: { input: "triggerIdle" } },
      { from: "State_Idle", to: "State_Error_404", condition: { input: "triggerError" } },
      { from: "State_Error_404", to: "State_Idle", condition: { input: "triggerIdle" } },
      { from: "State_Idle", to: "State_Sleeping", condition: { input: "triggerSleep" } },
      { from: "State_Sleeping", to: "State_Idle", condition: { input: "triggerIdle" } },
      { from: "State_Idle", to: "State_Wave_Continuous", condition: { input: "isWaving" } },
      { from: "State_Wave_Continuous", to: "State_Idle", condition: { input: "isWaving", op: "!=" } },
      { from: "State_Idle", to: "State_Blink", condition: { input: "triggerBlink" } },
      { from: "State_Blink", to: "State_Idle", exitTimeMs: 333 },
      { from: "State_Idle", to: "State_Wink", condition: { input: "triggerWink" } },
      { from: "State_Wink", to: "State_Idle", exitTimeMs: 500 }
    ]
  };

  const scene = {
    artboard: {
      name: "Owluko_Master_Artboard",
      width: 1152,
      height: 1024
    },
    backgroundColor: "#FFFFFF",
    groups,
    shapes: processedShapes,
    animations,
    stateMachine
  };

  // Write scene.json
  const scenePath = path.resolve(__dirname, "../mascots/owluko/owluko_pure_vector.scene.json");
  fs.writeFileSync(scenePath, JSON.stringify(scene, null, 2));
  console.log("Written master 6-state scene to " + scenePath);

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

  // Render representative preview frames for all 6 states
  const stateFrames = [
    { state: "00_idle", anim: "idle", time: 0.0 },
    { state: "01_waving", anim: "waving", time: 1.83 },
    { state: "02_celebrating", anim: "celebrating", time: 1.25 },
    { state: "03_thinking", anim: "thinking", time: 1.35 },
    { state: "04_error_404", anim: "error_404", time: 1.20 },
    { state: "06_sleeping", anim: "sleeping", time: 2.00 }
  ];

  for (const sf of stateFrames) {
    const fPath = path.resolve(__dirname, `../mascots/owluko/owluko_state_${sf.state}.png`);
    console.log(`Rendering frame for ${sf.state} (time=${sf.time}s)...`);
    await callMcpTool("riv_render_frame", {
      path: outRivPath,
      outPath: fPath,
      animation: sf.anim,
      time: sf.time,
      background: "#FFFFFF"
    });
  }

  // Render preview GIFs for all 6 states
  const stateGifs = [
    { state: "00_idle", anim: "idle", fps: 30, dur: 2.0 },
    { state: "01_waving", anim: "waving", fps: 30, dur: 4.0 },
    { state: "02_celebrating", anim: "celebrating", fps: 30, dur: 3.0 },
    { state: "03_thinking", anim: "thinking", fps: 30, dur: 3.0 },
    { state: "04_error_404", anim: "error_404", fps: 30, dur: 3.0 },
    { state: "06_sleeping", anim: "sleeping", fps: 30, dur: 4.0 }
  ];

  for (const sg of stateGifs) {
    const gPath = path.resolve(__dirname, `../mascots/owluko/owluko_state_${sg.state}.gif`);
    console.log(`Rendering GIF for ${sg.state} (${sg.dur}s)...`);
    await callMcpTool("riv_render_gif", {
      path: outRivPath,
      outPath: gPath,
      animation: sg.anim,
      fps: sg.fps,
      duration: sg.dur,
      background: "#FFFFFF"
    });
  }

  console.log("=== ALL 6 OWLUKO STATES COMPILED AND RENDERED SUCCESSFULLY ON RIVE ===");
}

buildOwlukoSixStatesRive().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
'''

with open("scripts/build_owluko_six_states_rive.js", "w") as f:
    f.write(content)

print(f"Wrote scripts/build_owluko_six_states_rive.js ({len(content)} bytes)")
