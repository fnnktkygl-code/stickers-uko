const fs = require("fs");
const path = require("path");
const { callMcpTool } = require("./rive_mcp_client.js");

const kappa = 0.5522847498307936;

async function buildOwlukoMasterpiece() {
  console.log("===============================================================");
  console.log("  BUILDING OWLUKO MASTERPIECE - FULL ANATOMICAL VECTOR RIG");
  console.log("  Marketplace Quality: Sculpted Toes, Layered Wings, Soulful Eyes");
  console.log("===============================================================");

  // 1. Hierarchy Groups
  // Canvas: 512x512
  // Root at ground baseline: (256, 470)
  const groups = [
    { id: "root", x: 256, y: 470 },
    { id: "shadow_group", parent: "root", x: 0, y: 0 },
    { id: "tail_group", parent: "root", x: 0, y: -45 },
    { id: "feet_group", parent: "root", x: 0, y: 0 },
    { id: "leg_l_group", parent: "feet_group", x: -55, y: 0 },
    { id: "leg_r_group", parent: "feet_group", x: 55, y: 0 },
    { id: "body_group", parent: "root", x: 0, y: -180 },
    { id: "wing_l_group", parent: "body_group", x: -140, y: 25 },
    { id: "wing_r_group", parent: "body_group", x: 140, y: 25 },
    { id: "head_group", parent: "body_group", x: 0, y: -82 },
    { id: "ear_tuft_l_group", parent: "head_group", x: -62, y: -65 },
    { id: "ear_tuft_r_group", parent: "head_group", x: 62, y: -65 },
    { id: "eye_l_group", parent: "head_group", x: -57, y: 0 },
    { id: "eye_r_group", parent: "head_group", x: 55, y: 0 },
    { id: "eyelid_l_group", parent: "eye_l_group", x: 0, y: 0 },
    { id: "eyelid_r_group", parent: "eye_r_group", x: 0, y: 0 },
    { id: "beak_group", parent: "head_group", x: 0, y: 26 }
  ];

  // 2. Sculpted Master Geometries

  // Body Sphere (Plump, round, cuddly baby owl: rx=168, ry=174)
  const rx_b = 168;
  const ry_b = 174;
  const bodyPoints = [
    { x: 0, y: -ry_b, cubic: { inRotation: 180, inDistance: rx_b * kappa, rotation: 0, outDistance: rx_b * kappa } },
    { x: rx_b, y: 12, cubic: { inRotation: 270, inDistance: ry_b * kappa, rotation: 90, outDistance: ry_b * kappa } },
    { x: 0, y: ry_b, cubic: { inRotation: 0, inDistance: rx_b * kappa, rotation: 180, outDistance: rx_b * kappa } },
    { x: -rx_b, y: 12, cubic: { inRotation: 90, inDistance: ry_b * kappa, rotation: 270, outDistance: ry_b * kappa } }
  ];

  // Body Cel-Shadow: crisp crescent giving clean spherical volume at base
  const bodyShadowPoints = [
    { x: -148, y: 35, cubic: { inRotation: 290, inDistance: 35, rotation: 110, outDistance: 35 } },
    { x: 0, y: 174, cubic: { inRotation: 180, inDistance: 120, rotation: 0, outDistance: 120 } },
    { x: 148, y: 35, cubic: { inRotation: 70, inDistance: 35, rotation: 250, outDistance: 35 } },
    { x: 0, y: 135, cubic: { inRotation: 0, inDistance: 95, rotation: 180, outDistance: 95 } }
  ];

  // Tail Feathers (3 rounded fans behind body)
  const tailPoints = [
    { x: -38, y: -10, radius: 4 },
    { x: -28, y: 24, radius: 8 },
    { x: 0, y: 32, radius: 10 },
    { x: 28, y: 24, radius: 8 },
    { x: 38, y: -10, radius: 4 }
  ];

  // Sculpted Avian Foot (3 distinct plump toes with knuckle creases and rear spur)
  // Left Foot:
  const footLPoints = [
    // Ankle cuff junction
    { x: -6, y: -22, radius: 3 },
    { x: 6, y: -22, radius: 3 },
    { x: 8, y: -12, radius: 3 },
    // Outer toe (right-facing in local coords, angled forward-out)
    { x: 22, y: -6, radius: 6 },
    { x: 26, y: 1, radius: 6 },
    { x: 20, y: 6, radius: 5 },
    { x: 10, y: -1, radius: 4 },
    // Middle toe (longest, pointing forward-down)
    { x: 5, y: 10, radius: 6 },
    { x: -2, y: 12, radius: 6 },
    { x: -8, y: 8, radius: 5 },
    { x: -6, y: 0, radius: 4 },
    // Inner toe (pointing left-forward)
    { x: -18, y: 6, radius: 5 },
    { x: -24, y: 2, radius: 6 },
    { x: -22, y: -5, radius: 6 },
    { x: -10, y: -8, radius: 4 },
    // Rear talon / heel spur
    { x: -12, y: -16, radius: 4 },
    { x: -6, y: -18, radius: 3 }
  ];

  // Right Foot (mirrored):
  const footRPoints = [
    { x: 6, y: -22, radius: 3 },
    { x: -6, y: -22, radius: 3 },
    { x: -8, y: -12, radius: 3 },
    // Outer toe
    { x: -22, y: -6, radius: 6 },
    { x: -26, y: 1, radius: 6 },
    { x: -20, y: 6, radius: 5 },
    { x: -10, y: -1, radius: 4 },
    // Middle toe
    { x: -5, y: 10, radius: 6 },
    { x: 2, y: 12, radius: 6 },
    { x: 8, y: 8, radius: 5 },
    { x: 6, y: 0, radius: 4 },
    // Inner toe
    { x: 18, y: 6, radius: 5 },
    { x: 24, y: 2, radius: 6 },
    { x: 22, y: -5, radius: 6 },
    { x: 10, y: -8, radius: 4 },
    // Rear spur
    { x: 12, y: -16, radius: 4 },
    { x: 6, y: -18, radius: 3 }
  ];

  // Toe crease shadow lines for 3D knuckle separation
  const footLCrease1 = [
    { x: 8, y: -2 },
    { x: 14, y: 3 }
  ];
  const footLCrease2 = [
    { x: -6, y: -1 },
    { x: -12, y: 4 }
  ];

  // Fluffy Leg Down Cuffs (soft puffs of down covering ankle joints)
  const legCuffPoints = [
    { x: -14, y: -12, radius: 4 },
    { x: -16, y: 0, radius: 6 },
    { x: -8, y: 6, radius: 5 },
    { x: 0, y: 4, radius: 5 },
    { x: 8, y: 6, radius: 5 },
    { x: 16, y: 0, radius: 6 },
    { x: 14, y: -12, radius: 4 }
  ];

  // Multi-layered Scalloped Left Wing
  // Layer 1: Base wing with 3 primary flight feather tips
  const wingLBasePoints = [
    { x: 0, y: 0, cubic: { inRotation: 180, inDistance: 15, rotation: 0, outDistance: 15 } },
    { x: -30, y: 35, cubic: { inRotation: 270, inDistance: 22, rotation: 90, outDistance: 22 } },
    // Primary Feather 1 (upper outer)
    { x: -35, y: 66, radius: 8 },
    { x: -26, y: 78, radius: 6 },
    // Primary Feather 2 (central blade, longest)
    { x: -22, y: 100, radius: 10 },
    { x: -8, y: 108, radius: 8 },
    // Primary Feather 3 (inner blade)
    { x: 6, y: 98, radius: 8 },
    { x: 14, y: 82, radius: 6 },
    // Inner contour tucking against flank
    { x: 20, y: 45, cubic: { inRotation: 85, inDistance: 30, rotation: 265, outDistance: 30 } }
  ];

  // Layer 2: Wing Covert Cap (Upper shoulder mantle layer)
  const wingLCovertPoints = [
    { x: 0, y: 0, cubic: { inRotation: 180, inDistance: 15, rotation: 0, outDistance: 15 } },
    { x: -28, y: 35, cubic: { inRotation: 270, inDistance: 18, rotation: 90, outDistance: 18 } },
    { x: -24, y: 55, radius: 8 },
    { x: -10, y: 62, radius: 8 },
    { x: 6, y: 56, radius: 7 },
    { x: 16, y: 38, cubic: { inRotation: 85, inDistance: 22, rotation: 265, outDistance: 22 } }
  ];

  // Right Wing (mirrored)
  const wingRBasePoints = [
    { x: 0, y: 0, cubic: { inRotation: 0, inDistance: 15, rotation: 180, outDistance: 15 } },
    { x: 30, y: 35, cubic: { inRotation: 270, inDistance: 22, rotation: 90, outDistance: 22 } },
    { x: 35, y: 66, radius: 8 },
    { x: 26, y: 78, radius: 6 },
    { x: 22, y: 100, radius: 10 },
    { x: 8, y: 108, radius: 8 },
    { x: -6, y: 98, radius: 8 },
    { x: -14, y: 82, radius: 6 },
    { x: -20, y: 45, cubic: { inRotation: 95, inDistance: 30, rotation: 275, outDistance: 30 } }
  ];

  const wingRCovertPoints = [
    { x: 0, y: 0, cubic: { inRotation: 0, inDistance: 15, rotation: 180, outDistance: 15 } },
    { x: 28, y: 35, cubic: { inRotation: 270, inDistance: 18, rotation: 90, outDistance: 18 } },
    { x: 24, y: 55, radius: 8 },
    { x: 10, y: 62, radius: 8 },
    { x: -6, y: 56, radius: 7 },
    { x: -16, y: 38, cubic: { inRotation: 95, inDistance: 22, rotation: 275, outDistance: 22 } }
  ];

  // Ear Tufts (Jaunty, plump, curved down crests on crown)
  const earTuftLPoints = [
    { x: 22, y: 14, radius: 4 },
    { x: -12, y: -24, cubic: { inRotation: 310, inDistance: 14, rotation: 130, outDistance: 12 } },
    { x: -32, y: -48, radius: 8 }, // Plump, rounded, expressive tip!
    { x: -16, y: -34, cubic: { inRotation: 130, inDistance: 14, rotation: 310, outDistance: 16 } },
    { x: -4, y: -8, radius: 4 },
    { x: 8, y: 10, radius: 4 }
  ];

  const earTuftRPoints = [
    { x: -22, y: 14, radius: 4 },
    { x: 12, y: -24, cubic: { inRotation: 230, inDistance: 14, rotation: 50, outDistance: 12 } },
    { x: 32, y: -48, radius: 8 },
    { x: 16, y: -34, cubic: { inRotation: 50, inDistance: 14, rotation: 230, outDistance: 16 } },
    { x: 4, y: -8, radius: 4 },
    { x: -8, y: 10, radius: 4 }
  ];

  // Cheek Fluff Tufts (3 tiered soft down flares on left & right cheeks)
  const cheekTuftLPoints = [
    { x: -100, y: -18, radius: 4 },
    { x: -130, y: -6, radius: 7 },
    { x: -118, y: 8, radius: 5 },
    { x: -134, y: 22, radius: 8 },
    { x: -115, y: 34, radius: 5 },
    { x: -125, y: 44, radius: 7 },
    { x: -95, y: 52, radius: 6 }
  ];

  const cheekTuftRPoints = [
    { x: 100, y: -18, radius: 4 },
    { x: 130, y: -6, radius: 7 },
    { x: 118, y: 8, radius: 5 },
    { x: 134, y: 22, radius: 8 },
    { x: 115, y: 34, radius: 5 },
    { x: 125, y: 44, radius: 7 },
    { x: 95, y: 52, radius: 6 }
  ];

  // Facial Disk (Barn owl double spectacle/heart contour)
  const facialDiskPoints = [
    { x: 0, y: -28, cubic: { inRotation: 145, inDistance: 22, rotation: 35, outDistance: 22 } },
    { x: 56, y: -64, cubic: { inRotation: 180, inDistance: 24, rotation: 0, outDistance: 24 } },
    { x: 116, y: 6, cubic: { inRotation: 270, inDistance: 34, rotation: 90, outDistance: 34 } },
    { x: 0, y: 62, cubic: { inRotation: 0, inDistance: 40, rotation: 180, outDistance: 40 } },
    { x: -116, y: 6, cubic: { inRotation: 90, inDistance: 34, rotation: 270, outDistance: 34 } },
    { x: -56, y: -64, cubic: { inRotation: 180, inDistance: 24, rotation: 0, outDistance: 24 } }
  ];

  // Brow Arches (Concentric, gentle, sweet curve over each eye socket)
  const browLPoints = [
    { x: -34, y: -16, radius: 3 },
    { x: 0, y: -40, cubic: { inRotation: 180, inDistance: 20, rotation: 0, outDistance: 20 } },
    { x: 34, y: -16, radius: 3 },
    { x: 30, y: -11, radius: 3 },
    { x: 0, y: -34, cubic: { inRotation: 0, inDistance: 17, rotation: 180, outDistance: 17 } },
    { x: -30, y: -11, radius: 3 }
  ];

  const browRPoints = [
    { x: -34, y: -16, radius: 3 },
    { x: 0, y: -40, cubic: { inRotation: 180, inDistance: 20, rotation: 0, outDistance: 20 } },
    { x: 34, y: -16, radius: 3 },
    { x: 30, y: -11, radius: 3 },
    { x: 0, y: -34, cubic: { inRotation: 0, inDistance: 17, rotation: 180, outDistance: 17 } },
    { x: -30, y: -11, radius: 3 }
  ];

  // Chest Feather Scallops (`u` crescent shapes)
  const featherScallop = [
    { x: -13, y: -4, radius: 2 },
    { x: 0, y: 6, cubic: { inRotation: 180, inDistance: 9, rotation: 0, outDistance: 9 } },
    { x: 13, y: -4, radius: 2 },
    { x: 10, y: -2, radius: 2 },
    { x: 0, y: 4, cubic: { inRotation: 0, inDistance: 7, rotation: 180, outDistance: 7 } },
    { x: -10, y: -2, radius: 2 }
  ];

  // Sculpted Beak (Upper bill + Smiling open lower jaw with pink tongue)
  const beakUpperPoints = [
    { x: 0, y: -16, cubic: { inRotation: 180, inDistance: 13, rotation: 0, outDistance: 13 } },
    { x: 16, y: -5, cubic: { inRotation: 270, inDistance: 6, rotation: 90, outDistance: 8 } },
    { x: 0, y: 14, radius: 4 },
    { x: -16, y: -5, cubic: { inRotation: 90, inDistance: 8, rotation: 270, outDistance: 6 } }
  ];

  const beakLowerPoints = [
    { x: -12, y: 2, radius: 2 },
    { x: 0, y: 16, radius: 5 },
    { x: 12, y: 2, radius: 2 }
  ];

  const tonguePoints = [
    { x: -7, y: 6, radius: 2 },
    { x: 0, y: 13, radius: 3 },
    { x: 7, y: 6, radius: 2 }
  ];

  // Eyelids (Smooth Circular Domes for blinking)
  const eyelidLPoints = [
    { x: -36, y: 0, cubic: { inRotation: 90, inDistance: 36 * kappa, rotation: 270, outDistance: 36 * kappa } },
    { x: 0, y: -36, cubic: { inRotation: 180, inDistance: 36 * kappa, rotation: 0, outDistance: 36 * kappa } },
    { x: 36, y: 0, cubic: { inRotation: 270, inDistance: 36 * kappa, rotation: 90, outDistance: 36 * kappa } },
    { x: 0, y: 20, cubic: { inRotation: 0, inDistance: 24, rotation: 180, outDistance: 24 } }
  ];

  const eyelidRPoints = [
    { x: -36, y: 0, cubic: { inRotation: 90, inDistance: 36 * kappa, rotation: 270, outDistance: 36 * kappa } },
    { x: 0, y: -36, cubic: { inRotation: 180, inDistance: 36 * kappa, rotation: 0, outDistance: 36 * kappa } },
    { x: 36, y: 0, cubic: { inRotation: 270, inDistance: 36 * kappa, rotation: 90, outDistance: 36 * kappa } },
    { x: 0, y: 20, cubic: { inRotation: 0, inDistance: 24, rotation: 180, outDistance: 24 } }
  ];

  // 3. Complete Shapes Hierarchy & Cel-Shading Palette
  const shapes = [
    // 01 Ground Contact Shadow
    {
      id: "ground_shadow_ambient",
      type: "ellipse",
      parent: "shadow_group",
      x: 0,
      y: 0,
      width: 320,
      height: 44,
      fill: {
        gradient: {
          type: "radial",
          stops: [
            { color: "#442A1C10", position: 0 },
            { color: "#182A1C10", position: 0.65 },
            { color: "#002A1C10", position: 1 }
          ]
        }
      }
    },
    {
      id: "ground_shadow_core",
      type: "ellipse",
      parent: "shadow_group",
      x: 0,
      y: 0,
      width: 220,
      height: 24,
      fill: {
        gradient: {
          type: "radial",
          stops: [
            { color: "#66201208", position: 0 },
            { color: "#00201208", position: 1 }
          ]
        }
      }
    },

    // 02 Tail Feathers
    {
      id: "tail_feathers",
      type: "polygon",
      parent: "tail_group",
      x: 0,
      y: 0,
      points: tailPoints,
      fill: { color: "#DFCBB0" }
    },

    // 03 Sculpted Feet & Toes
    // Left Foot
    {
      id: "foot_l_body",
      type: "polygon",
      parent: "leg_l_group",
      x: 0,
      y: 0,
      points: footLPoints,
      fill: {
        gradient: {
          type: "linear",
          start: { x: 0, y: -22 },
          end: { x: 0, y: 12 },
          stops: [
            { color: "#FB923C", position: 0 },
            { color: "#EA580C", position: 0.55 },
            { color: "#9A3412", position: 1 }
          ]
        }
      }
    },
    // Left Foot Down Puff Cuff
    {
      id: "foot_l_cuff",
      type: "polygon",
      parent: "leg_l_group",
      x: 0,
      y: -14,
      points: legCuffPoints,
      fill: { color: "#FAF6ED" }
    },
    // Right Foot
    {
      id: "foot_r_body",
      type: "polygon",
      parent: "leg_r_group",
      x: 0,
      y: 0,
      points: footRPoints,
      fill: {
        gradient: {
          type: "linear",
          start: { x: 0, y: -22 },
          end: { x: 0, y: 12 },
          stops: [
            { color: "#FB923C", position: 0 },
            { color: "#EA580C", position: 0.55 },
            { color: "#9A3412", position: 1 }
          ]
        }
      }
    },
    // Right Foot Down Puff Cuff
    {
      id: "foot_r_cuff",
      type: "polygon",
      parent: "leg_r_group",
      x: 0,
      y: -14,
      points: legCuffPoints,
      fill: { color: "#FAF6ED" }
    },

    // 04 Ear Tufts (Behind Head)
    {
      id: "ear_tuft_l_shadow",
      type: "polygon",
      parent: "ear_tuft_l_group",
      x: -2,
      y: 2,
      points: earTuftLPoints,
      fill: { color: "#D8C5AD" }
    },
    {
      id: "ear_tuft_l",
      type: "polygon",
      parent: "ear_tuft_l_group",
      x: 0,
      y: 0,
      points: earTuftLPoints,
      fill: { color: "#FAF6ED" }
    },
    {
      id: "ear_tuft_r_shadow",
      type: "polygon",
      parent: "ear_tuft_r_group",
      x: 2,
      y: 2,
      points: earTuftRPoints,
      fill: { color: "#D8C5AD" }
    },
    {
      id: "ear_tuft_r",
      type: "polygon",
      parent: "ear_tuft_r_group",
      x: 0,
      y: 0,
      points: earTuftRPoints,
      fill: { color: "#FAF6ED" }
    },

    // 05 Cheek Fluff Tufts (Behind Body)
    {
      id: "cheek_tuft_l",
      type: "polygon",
      parent: "head_group",
      x: 0,
      y: 0,
      points: cheekTuftLPoints,
      fill: { color: "#FAF6ED" }
    },
    {
      id: "cheek_tuft_r",
      type: "polygon",
      parent: "head_group",
      x: 0,
      y: 0,
      points: cheekTuftRPoints,
      fill: { color: "#FAF6ED" }
    },

    // 06 Body Base & Spherical Cel-Shadow
    {
      id: "body_sphere",
      type: "polygon",
      parent: "body_group",
      x: 0,
      y: 0,
      points: bodyPoints,
      fill: { color: "#FAF6ED" }
    },
    {
      id: "body_cel_shadow",
      type: "polygon",
      parent: "body_group",
      x: 0,
      y: 0,
      points: bodyShadowPoints,
      fill: { color: "#E0CEB7" }
    },

    // 07 Fluffy Belly Base
    {
      id: "fluffy_belly",
      type: "ellipse",
      parent: "body_group",
      x: 0,
      y: 65,
      width: 260,
      height: 190,
      fill: { color: "#FFFDF8" }
    },

    // 08 Chest Feather Scallops (`u u u` plumage)
    {
      id: "feather_scallop_row1_c",
      type: "polygon",
      parent: "body_group",
      x: 0,
      y: 35,
      points: featherScallop,
      fill: { color: "#CBB69E" }
    },
    {
      id: "feather_scallop_row1_l",
      type: "polygon",
      parent: "body_group",
      x: -42,
      y: 46,
      rotation: -8,
      points: featherScallop,
      fill: { color: "#CBB69E" }
    },
    {
      id: "feather_scallop_row1_r",
      type: "polygon",
      parent: "body_group",
      x: 42,
      y: 46,
      rotation: 8,
      points: featherScallop,
      fill: { color: "#CBB69E" }
    },
    {
      id: "feather_scallop_row2_l",
      type: "polygon",
      parent: "body_group",
      x: -24,
      y: 78,
      rotation: -4,
      points: featherScallop,
      fill: { color: "#CBB69E" }
    },
    {
      id: "feather_scallop_row2_r",
      type: "polygon",
      parent: "body_group",
      x: 24,
      y: 78,
      rotation: 4,
      points: featherScallop,
      fill: { color: "#CBB69E" }
    },
    {
      id: "feather_scallop_row3_c",
      type: "polygon",
      parent: "body_group",
      x: 0,
      y: 110,
      points: featherScallop,
      fill: { color: "#CBB69E" }
    },

    // 09 Layered Left Wing (Primary flight feathers + Covert mantle)
    {
      id: "wing_l_shadow",
      type: "polygon",
      parent: "wing_l_group",
      x: 3,
      y: 2,
      points: wingLBasePoints,
      fill: { color: "#D1BFAB" }
    },
    {
      id: "wing_l_base",
      type: "polygon",
      parent: "wing_l_group",
      x: 0,
      y: 0,
      points: wingLBasePoints,
      fill: { color: "#FAF6ED" }
    },
    {
      id: "wing_l_covert",
      type: "polygon",
      parent: "wing_l_group",
      x: 0,
      y: 0,
      points: wingLCovertPoints,
      fill: {
        gradient: {
          type: "linear",
          start: { x: 10, y: 0 },
          end: { x: -20, y: 60 },
          stops: [
            { color: "#FFFDF8", position: 0 },
            { color: "#EDE1CD", position: 1 }
          ]
        }
      }
    },

    // 10 Layered Right Wing
    {
      id: "wing_r_shadow",
      type: "polygon",
      parent: "wing_r_group",
      x: -3,
      y: 2,
      points: wingRBasePoints,
      fill: { color: "#D1BFAB" }
    },
    {
      id: "wing_r_base",
      type: "polygon",
      parent: "wing_r_group",
      x: 0,
      y: 0,
      points: wingRBasePoints,
      fill: { color: "#FAF6ED" }
    },
    {
      id: "wing_r_covert",
      type: "polygon",
      parent: "wing_r_group",
      x: 0,
      y: 0,
      points: wingRCovertPoints,
      fill: {
        gradient: {
          type: "linear",
          start: { x: -10, y: 0 },
          end: { x: 20, y: 60 },
          stops: [
            { color: "#FFFDF8", position: 0 },
            { color: "#EDE1CD", position: 1 }
          ]
        }
      }
    },

    // 11 Facial Disk (Pure Light Cream Barn Owl Mask)
    {
      id: "facial_disk_shadow",
      type: "polygon",
      parent: "head_group",
      x: 0,
      y: 2,
      points: facialDiskPoints,
      fill: { color: "#E0CEB7" }
    },
    {
      id: "facial_disk",
      type: "polygon",
      parent: "head_group",
      x: 0,
      y: 0,
      points: facialDiskPoints,
      fill: { color: "#FFFDF8" }
    },

    // 12 Cheek Blush
    {
      id: "blush_left",
      type: "ellipse",
      parent: "head_group",
      x: -88,
      y: 26,
      width: 38,
      height: 18,
      rotation: -6,
      fill: {
        gradient: {
          type: "radial",
          stops: [
            { color: "#3BED7855", position: 0 },
            { color: "#00ED7855", position: 1 }
          ]
        }
      }
    },
    {
      id: "blush_right",
      type: "ellipse",
      parent: "head_group",
      x: 88,
      y: 26,
      width: 38,
      height: 18,
      rotation: 6,
      fill: {
        gradient: {
          type: "radial",
          stops: [
            { color: "#3BED7855", position: 0 },
            { color: "#00ED7855", position: 1 }
          ]
        }
      }
    },

    // 13 Left Eye Architecture
    {
      id: "eye_l_brow",
      type: "polygon",
      parent: "eye_l_group",
      x: 0,
      y: -2,
      points: browLPoints,
      fill: { color: "#CBB69E" }
    },
    {
      id: "eye_l_socket",
      type: "ellipse",
      parent: "eye_l_group",
      x: 0,
      y: 0,
      width: 74,
      height: 74,
      fill: { color: "#1A0A02" }
    },
    {
      id: "eye_l_iris",
      type: "ellipse",
      parent: "eye_l_group",
      x: 0,
      y: 0,
      width: 70,
      height: 70,
      fill: {
        gradient: {
          type: "radial",
          start: { x: 0, y: 12 },
          end: { x: 30, y: -30 },
          stops: [
            { color: "#FCD34D", position: 0 },
            { color: "#F59E0B", position: 0.35 },
            { color: "#B45309", position: 0.72 },
            { color: "#1A0A02", position: 1 }
          ]
        }
      }
    },
    {
      id: "eye_l_pupil",
      type: "ellipse",
      parent: "eye_l_group",
      x: 0,
      y: 0,
      width: 44,
      height: 44,
      fill: { color: "#080301" }
    },
    {
      id: "eye_l_glint_primary",
      type: "ellipse",
      parent: "eye_l_group",
      x: -12,
      y: -11,
      width: 15,
      height: 15,
      fill: { color: "#FFFFFFFF" }
    },
    {
      id: "eye_l_glint_secondary",
      type: "ellipse",
      parent: "eye_l_group",
      x: -4,
      y: -16,
      width: 7,
      height: 7,
      fill: { color: "#DDFFFFFF" }
    },
    {
      id: "eye_l_glint_tertiary",
      type: "ellipse",
      parent: "eye_l_group",
      x: 16,
      y: 0,
      width: 5,
      height: 5,
      fill: { color: "#EEFFFFFF" }
    },
    {
      id: "eye_l_eyelid",
      type: "polygon",
      parent: "eyelid_l_group",
      x: 0,
      y: 0,
      opacity: 0,
      points: eyelidLPoints,
      fill: { color: "#FFFDF8" }
    },

    // 14 Right Eye Architecture
    {
      id: "eye_r_brow",
      type: "polygon",
      parent: "eye_r_group",
      x: 0,
      y: -2,
      points: browRPoints,
      fill: { color: "#CBB69E" }
    },
    {
      id: "eye_r_socket",
      type: "ellipse",
      parent: "eye_r_group",
      x: 0,
      y: 0,
      width: 74,
      height: 74,
      fill: { color: "#1A0A02" }
    },
    {
      id: "eye_r_iris",
      type: "ellipse",
      parent: "eye_r_group",
      x: 0,
      y: 0,
      width: 70,
      height: 70,
      fill: {
        gradient: {
          type: "radial",
          start: { x: 0, y: 12 },
          end: { x: 30, y: -30 },
          stops: [
            { color: "#FCD34D", position: 0 },
            { color: "#F59E0B", position: 0.35 },
            { color: "#B45309", position: 0.72 },
            { color: "#1A0A02", position: 1 }
          ]
        }
      }
    },
    {
      id: "eye_r_pupil",
      type: "ellipse",
      parent: "eye_r_group",
      x: 0,
      y: 0,
      width: 44,
      height: 44,
      fill: { color: "#080301" }
    },
    {
      id: "eye_r_glint_primary",
      type: "ellipse",
      parent: "eye_r_group",
      x: -12,
      y: -11,
      width: 15,
      height: 15,
      fill: { color: "#FFFFFFFF" }
    },
    {
      id: "eye_r_glint_secondary",
      type: "ellipse",
      parent: "eye_r_group",
      x: -4,
      y: -16,
      width: 7,
      height: 7,
      fill: { color: "#DDFFFFFF" }
    },
    {
      id: "eye_r_glint_tertiary",
      type: "ellipse",
      parent: "eye_r_group",
      x: 16,
      y: 0,
      width: 5,
      height: 5,
      fill: { color: "#EEFFFFFF" }
    },
    {
      id: "eye_r_eyelid",
      type: "polygon",
      parent: "eyelid_r_group",
      x: 0,
      y: 0,
      opacity: 0,
      points: eyelidRPoints,
      fill: { color: "#FFFDF8" }
    },

    // 15 Sculpted Beak & Cheerful Mouth
    {
      id: "beak_mouth_shadow",
      type: "polygon",
      parent: "beak_group",
      x: 0,
      y: 2,
      points: beakLowerPoints,
      fill: { color: "#7C2D12" }
    },
    {
      id: "beak_tongue",
      type: "polygon",
      parent: "beak_group",
      x: 0,
      y: 3,
      points: tonguePoints,
      fill: { color: "#FB7185" }
    },
    {
      id: "beak_upper",
      type: "polygon",
      parent: "beak_group",
      x: 0,
      y: 0,
      points: beakUpperPoints,
      fill: {
        gradient: {
          type: "linear",
          start: { x: 0, y: -16 },
          end: { x: 0, y: 14 },
          stops: [
            { color: "#FDBA74", position: 0 },
            { color: "#EA580C", position: 0.55 },
            { color: "#9A3412", position: 1 }
          ]
        }
      }
    },
    {
      id: "beak_glint",
      type: "ellipse",
      parent: "beak_group",
      x: 0,
      y: -8,
      width: 8,
      height: 5,
      fill: { color: "#FEF08A" }
    }
  ];

  // 4. Fluid 60 FPS Organic Animation
  const animations = [
    {
      name: "idle",
      fps: 60,
      duration: 120,
      loop: "loop",
      tracks: [
        // Torso squash & stretch
        {
          target: "body_group",
          property: "y",
          keyframes: [
            { frame: 0, value: -180, easing: "ease-in-out" },
            { frame: 60, value: -186, easing: "ease-in-out" },
            { frame: 120, value: -180, easing: "ease-in-out" }
          ]
        },
        {
          target: "body_group",
          property: "scaleY",
          keyframes: [
            { frame: 0, value: 1.0, easing: "ease-in-out" },
            { frame: 60, value: 1.035, easing: "ease-in-out" },
            { frame: 120, value: 1.0, easing: "ease-in-out" }
          ]
        },
        {
          target: "body_group",
          property: "scaleX",
          keyframes: [
            { frame: 0, value: 1.0, easing: "ease-in-out" },
            { frame: 60, value: 0.975, easing: "ease-in-out" },
            { frame: 120, value: 1.0, easing: "ease-in-out" }
          ]
        },
        // Wings breathing with harmonic delay
        {
          target: "wing_l_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0, easing: "ease-in-out" },
            { frame: 60, value: -3.5, easing: "ease-in-out" },
            { frame: 120, value: 0, easing: "ease-in-out" }
          ]
        },
        {
          target: "wing_r_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0, easing: "ease-in-out" },
            { frame: 60, value: 3.5, easing: "ease-in-out" },
            { frame: 120, value: 0, easing: "ease-in-out" }
          ]
        },
        // Ear tufts subtle organic spring
        {
          target: "ear_tuft_l_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0, easing: "ease-in-out" },
            { frame: 50, value: 3.0, easing: "ease-in-out" },
            { frame: 120, value: 0, easing: "ease-in-out" }
          ]
        },
        {
          target: "ear_tuft_r_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0, easing: "ease-in-out" },
            { frame: 50, value: -3.0, easing: "ease-in-out" },
            { frame: 120, value: 0, easing: "ease-in-out" }
          ]
        },
        // Tail breathing
        {
          target: "tail_group",
          property: "scaleX",
          keyframes: [
            { frame: 0, value: 1.0, easing: "ease-in-out" },
            { frame: 60, value: 1.05, easing: "ease-in-out" },
            { frame: 120, value: 1.0, easing: "ease-in-out" }
          ]
        },
        // Ground shadow pulsation
        {
          target: "shadow_group",
          property: "scaleX",
          keyframes: [
            { frame: 0, value: 1.0, easing: "ease-in-out" },
            { frame: 60, value: 0.94, easing: "ease-in-out" },
            { frame: 120, value: 1.0, easing: "ease-in-out" }
          ]
        },
        // Natural conscious double blink (frames 68..84)
        {
          target: "eye_l_eyelid",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 68, value: 0 },
            { frame: 74, value: 1, easing: "ease-in" },
            { frame: 78, value: 1 },
            { frame: 84, value: 0, easing: "ease-out" },
            { frame: 120, value: 0 }
          ]
        },
        {
          target: "eye_r_eyelid",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 68, value: 0 },
            { frame: 74, value: 1, easing: "ease-in" },
            { frame: 78, value: 1 },
            { frame: 84, value: 0, easing: "ease-out" },
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
          target: "eye_l_eyelid",
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
          target: "eye_r_eyelid",
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

  const stateMachine = {
    name: "Owluko_SM",
    inputs: [{ name: "triggerBlink", type: "trigger" }],
    states: [
      { name: "idle_state", animation: "idle" },
      { name: "blink_state", animation: "blink" }
    ],
    transitions: [
      { from: "entry", to: "idle_state" },
      { from: "idle_state", to: "blink_state", condition: { input: "triggerBlink" } },
      { from: "blink_state", to: "idle_state", exitTimeMs: 330 }
    ]
  };

  const scene = {
    artboard: { name: "Owluko_Masterpiece", width: 512, height: 512 },
    backgroundColor: "#FAFAFA",
    groups,
    shapes,
    animations,
    stateMachine
  };

  // 5. Export Scene JSON
  const scenePath = "mascots/owluko/owluko_pure_vector.scene.json";
  fs.writeFileSync(scenePath, JSON.stringify(scene, null, 2));
  console.log("Written updated scene to " + scenePath);

  // 6. Compile via riv_create
  const outRivPath = "mascots/owluko/owluko_pure_vector.riv";
  console.log("Compiling pure vector binary to " + outRivPath + "...");
  const createRes = await callMcpTool("riv_create", {
    outPath: outRivPath,
    scene: scene
  });

  if (createRes.isError) {
    console.error("Compilation error:", JSON.stringify(createRes, null, 2));
    process.exit(1);
  }

  const stat = fs.statSync(outRivPath);
  console.log(`Compiled pure vector .riv: ${stat.size} bytes (${(stat.size / 1024).toFixed(1)} KB)`);

  // 7. Render Preview Frames
  const frame0Path = "mascots/owluko/owluko_pure_vector_frame0.png";
  console.log("Rendering frame 0...");
  await callMcpTool("riv_render_frame", {
    path: outRivPath,
    outPath: frame0Path,
    animation: "idle",
    time: 0,
    background: "#FFFFFF"
  });

  const frameBlinkPath = "mascots/owluko/owluko_pure_vector_blink.png";
  console.log("Rendering blink frame...");
  await callMcpTool("riv_render_frame", {
    path: outRivPath,
    outPath: frameBlinkPath,
    animation: "idle",
    time: 1.25,
    background: "#FFFFFF"
  });

  const gifPath = "mascots/owluko/owluko_pure_vector.gif";
  console.log("Rendering 2.0s looping GIF...");
  await callMcpTool("riv_render_gif", {
    path: outRivPath,
    outPath: gifPath,
    animation: "idle",
    fps: 30,
    duration: 2.0,
    background: "#FFFFFF"
  });

  console.log("=== COMPLETED SUCCESSFULLY ===");
}

buildOwlukoMasterpiece().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
