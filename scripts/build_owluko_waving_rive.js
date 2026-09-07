const fs = require("fs");
const path = require("path");
const { callMcpTool } = require("./rive_mcp_client.js");

const kappa = 0.5522847498307936;

async function buildOwlukoWavingRive() {
  console.log("===================================================================");
  console.log("  BUILDING CANONICAL OWLUKO WAVING RIVE RIG (media_1788763379758)   ");
  console.log("  - Pure Vector Bezier Shapes, Smooth 3-Finger Porcelain Wing       ");
  console.log("  - Joyful Espresso Smile Arches on Cream Eyelids (Panel 5)         ");
  console.log("  - 60 FPS State Machine (Waving Performance & Continuous Wave)     ");
  console.log("===================================================================");

  const fragmentPath = path.resolve(__dirname, "../scratch/owluko_waving.scene.json");
  if (!fs.existsSync(fragmentPath)) {
    throw new Error("Missing fragment: " + fragmentPath);
  }
  const fragment = JSON.parse(fs.readFileSync(fragmentPath, "utf-8"));
  console.log(`Loaded fragment with ${fragment.shapes.length} imported shapes.`);

  // 1. Define Rig Groups Hierarchy (1152 x 1024 Artboard Space)
  // Perfectly centered at x: 576. Provides a generous >= 98px margin for the extended waving wing tip (max X <= 1054)
  // and 100.0% mathematical symmetry between left and right resting flanks!
  const groups = [
    { id: "root", x: 576, y: 876 },
    { id: "shadow_group", parent: "root", x: 0, y: 0 },
    { id: "feet_group", parent: "root", x: 0, y: 0 },
    { id: "body_group", parent: "root", x: 0, y: -378 }, // global: (576, 498)
    { id: "wings_group", parent: "body_group", x: 0, y: 0 },
    { id: "wing_l_group", parent: "wings_group", x: -288, y: 92 }, // global: (288, 590) - organic sculpted left wing
    { id: "wing_r_rest_group", parent: "wings_group", x: 288, y: 92 }, // global: (864, 590) - organic sculpted right wing
    { id: "wing_r_wave_group", parent: "wings_group", x: 258, y: 62 }, // global: (834, 560) [pivot at shoulder!]
    { id: "belly_group", parent: "body_group", x: 0, y: 0 },
    { id: "head_group", parent: "body_group", x: 0, y: -126 },
    { id: "eye_l_group", parent: "head_group", x: -114, y: -10 },
    { id: "eye_r_group", parent: "head_group", x: 114, y: -10 },
    { id: "beak_group", parent: "head_group", x: 0, y: 44 }
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

    // Waving wing is layered BEHIND body silhouette
    owluko_wave_wing_wave_shadow: "wing_r_wave_group",
    owluko_wave_wing_wave_smooth_main: "wing_r_wave_group",

    // Body silhouette
    owluko_wave_body_silhouette: "body_group",

    // Resting wing is on the flank
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

  // Precise layer ordering:
  // 1. Shadows
  // 2. Feet
  // 3. Left wing
  // 4. Waving wing (behind body)
  // 5. Body silhouette
  // 6. Resting wing
  // 7. Belly patch
  // 8. Facial mask
  // 9. Eyes (open -> eyelid covers -> happy eyes)
  // 10. Beak

  const artboardWidth = 1152;
  const dx = (artboardWidth - 1024) / 2; // 64px shift to center from 1024 space into 1152 space
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
    // Right Waving Wing (BEHIND BODY - shoulder connects behind porcelain torso)
    "owluko_wave_wing_wave_shadow",
    "owluko_wave_wing_wave_smooth_main",
    // Body Silhouette
    "owluko_wave_body_silhouette",
    // Left Wing (Resting on Flank - in front of body, 100% symmetric to right wing)
    "owluko_wave_wing_left_shadow",
    "owluko_wave_wing_left_main",
    // Right Wing (Resting on Flank - in front of body)
    "owluko_wave_wing_right_shadow",
    "owluko_wave_wing_right_main",
    // Belly Patch
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
    // Left Eyelid & Happy Smile
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
    // Right Eyelid & Happy Smile
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

  // 2. Animations Definition
  const animations = [
    // IDLE (60 FPS, 120 frames = 2.0s seamless loop)
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
          target: "owluko_wave_wing_wave_smooth_main",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0 }, { frame: 120, value: 0 }]
        },
        {
          target: "owluko_wave_wing_wave_shadow",
          property: "opacity",
          keyframes: [{ frame: 0, value: 0 }, { frame: 120, value: 0 }]
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

    // WAVING PERFORMANCE (60 FPS, 240 frames = 4.0s)
    {
      name: "waving",
      fps: 60,
      duration: 240,
      loop: "one-shot",
      tracks: [
        // Resting Wing on Flank: 100% visible at frame 0..30 (true resting pose), fades smoothly as wave raises, fully restored by frame 220..240
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
        // Waving Wing: Strictly 0 at frame 0..30 and frame 218..240 (zero ghost wing at rest!)
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
          target: "owluko_wave_wing_wave_shadow",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 30, value: 0 },
            { frame: 45, value: 0 },
            { frame: 200, value: 0 },
            { frame: 218, value: 0 },
            { frame: 240, value: 0 }
          ]
        },
        // Waving Wing Rotation: Shoulder pivot at (770, 560)
        // 0..30: Rest anticipation -> 30..60: Smooth ascent -> 60..175: WING STAYS RAISED & WAVES -> 175..228: Graceful return
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
        // Head Expressive Tilts: Responsive counter-balance and endearing nod
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
        // Body Respiration & Cheerful Expansion
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
        // Left Wing Passive Balance
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
        // Eyelid Covers & Happy Smile Eyes (Panel 5 Joyful Expression at frames 120..168)
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

    // WAVE_LOOP: Continuous Waving Loop (60 FPS, 120 frames = 2.0s)
    // Wing is 100% RAISED and sways gently forever without ever lowering to the flank!
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
        // Cute natural blink in loop
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

    // BLINK (20 frames, one-shot)
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

    // WINK (30 frames, one-shot)
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
      { name: "triggerWave", type: "trigger" },
      { name: "isWaving", type: "bool", initial: false },
      { name: "triggerBlink", type: "trigger" },
      { name: "triggerWink", type: "trigger" }
    ],
    states: [
      { name: "Respiration", animation: "idle" },
      { name: "Waving_Performance", animation: "waving" },
      { name: "Wave_Continuous", animation: "wave_loop" },
      { name: "Blink_State", animation: "blink" },
      { name: "Wink_State", animation: "wink" }
    ],
    transitions: [
      { from: "entry", to: "Respiration" },
      { from: "Respiration", to: "Waving_Performance", condition: { input: "triggerWave" } },
      { from: "Waving_Performance", to: "Respiration", exitTimeMs: 4000 },
      { from: "Respiration", to: "Wave_Continuous", condition: { input: "isWaving" } },
      { from: "Wave_Continuous", to: "Respiration", condition: { input: "isWaving", op: "!=" } },
      { from: "Respiration", to: "Blink_State", condition: { input: "triggerBlink" } },
      { from: "Blink_State", to: "Respiration", exitTimeMs: 333 },
      { from: "Respiration", to: "Wink_State", condition: { input: "triggerWink" } },
      { from: "Wink_State", to: "Respiration", exitTimeMs: 500 }
    ]
  };

  const scene = {
    artboard: {
      name: "Owluko_Waving",
      width: 1152,
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

  // Render Key Frames for Verification (Matching 6-Panel Storyboard):
  // 1. Panel 1: Rest pose (t = 0.0s)
  const p1Path = path.resolve(__dirname, "../mascots/owluko/owluko_wave_p1_rest.png");
  console.log("Rendering Panel 1 (Rest pose, t=0.0s)...");
  await callMcpTool("riv_render_frame", {
    path: outRivPath,
    outPath: p1Path,
    animation: "waving",
    time: 0.0,
    background: "#FFFFFF"
  });

  // 2. Panel 2: Wing Raising (t = 0.75s, frame 45)
  const p2Path = path.resolve(__dirname, "../mascots/owluko/owluko_wave_p2_raising.png");
  console.log("Rendering Panel 2 (Wing raising, t=0.75s)...");
  await callMcpTool("riv_render_frame", {
    path: outRivPath,
    outPath: p2Path,
    animation: "waving",
    time: 0.75,
    background: "#FFFFFF"
  });

  // 3. Panel 3: Inward Wave (t = 1.42s, frame 85)
  const p3Path = path.resolve(__dirname, "../mascots/owluko/owluko_wave_p3_inward.png");
  console.log("Rendering Panel 3 (Inward tilt, t=1.42s)...");
  await callMcpTool("riv_render_frame", {
    path: outRivPath,
    outPath: p3Path,
    animation: "waving",
    time: 1.42,
    background: "#FFFFFF"
  });

  // 4. Panel 4: Outward Wave (t = 1.83s, frame 110)
  const p4Path = path.resolve(__dirname, "../mascots/owluko/owluko_wave_p4_outward.png");
  console.log("Rendering Panel 4 (Outward sway, t=1.83s)...");
  await callMcpTool("riv_render_frame", {
    path: outRivPath,
    outPath: p4Path,
    animation: "waving",
    time: 1.83,
    background: "#FFFFFF"
  });

  // 5. Panel 5: Joyful Smile (t = 2.37s, frame 142)
  const p5Path = path.resolve(__dirname, "../mascots/owluko/owluko_wave_p5_smile.png");
  console.log("Rendering Panel 5 (Joyful smile eyes, t=2.37s)...");
  await callMcpTool("riv_render_frame", {
    path: outRivPath,
    outPath: p5Path,
    animation: "waving",
    time: 2.37,
    background: "#FFFFFF"
  });

  // 6. Panel 6: Return to Rest (t = 4.00s, frame 240 - Complete Return to Peaceful Rest)
  const p6Path = path.resolve(__dirname, "../mascots/owluko/owluko_wave_p6_return.png");
  console.log("Rendering Panel 6 (Return to rest, t=4.00s)...");
  await callMcpTool("riv_render_frame", {
    path: outRivPath,
    outPath: p6Path,
    animation: "waving",
    time: 4.00,
    background: "#FFFFFF"
  });

  // Keep legacy filenames updated as well for compatibility
  fs.copyFileSync(p1Path, path.resolve(__dirname, "../mascots/owluko/owluko_wave_frame0_rest.png"));
  fs.copyFileSync(p3Path, path.resolve(__dirname, "../mascots/owluko/owluko_wave_frame28_inward.png"));
  fs.copyFileSync(p4Path, path.resolve(__dirname, "../mascots/owluko/owluko_wave_frame42_outward.png"));
  fs.copyFileSync(p5Path, path.resolve(__dirname, "../mascots/owluko/owluko_wave_frame90_smile.png"));

  // 7. Render 4.0s Complete Waving Performance GIF (fps: 30, duration: 4.0)
  const gifPath = path.resolve(__dirname, "../mascots/owluko/owluko_waving.gif");
  console.log("Rendering 4.0s complete waving GIF...");
  await callMcpTool("riv_render_gif", {
    path: outRivPath,
    outPath: gifPath,
    animation: "waving",
    fps: 30,
    duration: 4.0,
    background: "#FFFFFF"
  });

  // 8. Render 2.0s Continuous Wave Loop GIF (fps: 30, duration: 2.0)
  const gifLoopPath = path.resolve(__dirname, "../mascots/owluko/owluko_wave_loop.gif");
  console.log("Rendering 2.0s continuous wave loop GIF...");
  await callMcpTool("riv_render_gif", {
    path: outRivPath,
    outPath: gifLoopPath,
    animation: "wave_loop",
    fps: 30,
    duration: 2.0,
    background: "#FFFFFF"
  });

  console.log("=== CANONICAL OWLUKO WAVING COMPILED & RENDERED SUCCESSFULLY ===");
}

buildOwlukoWavingRive().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
