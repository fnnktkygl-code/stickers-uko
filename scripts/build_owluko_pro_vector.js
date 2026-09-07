const fs = require("fs");
const path = require("path");
const { callMcpTool } = require("./rive_mcp_client.js");

const kappa = 0.5522847498307936;

async function buildOwlukoPro() {
  console.log("=== BUILDING OWLUKO PRO VECTOR MASCOT (MARKETPLACE QUALITY) ===");

  // 1. Groups & Hierarchy
  const groups = [
    { id: "root", x: 256, y: 472 },
    { id: "feet_group", parent: "root", x: 0, y: 0 },
    { id: "foot_l_group", parent: "feet_group", x: -56, y: 0 },
    { id: "foot_r_group", parent: "feet_group", x: 54, y: 0 },
    { id: "tail_group", parent: "root", x: 0, y: -45 },
    { id: "body_group", parent: "root", x: 0, y: -184 },
    { id: "wing_l_group", parent: "body_group", x: -140, y: 30 },
    { id: "wing_r_group", parent: "body_group", x: 140, y: 30 },
    { id: "head_group", parent: "body_group", x: 0, y: -82 },
    { id: "ear_tuft_l_group", parent: "head_group", x: -65, y: -65 },
    { id: "ear_tuft_r_group", parent: "head_group", x: 65, y: -65 },
    { id: "eye_l_group", parent: "head_group", x: -57, y: 0 },
    { id: "eye_r_group", parent: "head_group", x: 55, y: 0 },
    { id: "eyelid_l_group", parent: "eye_l_group", x: 0, y: 0 },
    { id: "eyelid_r_group", parent: "eye_r_group", x: 0, y: 0 },
    { id: "beak_group", parent: "head_group", x: 0, y: 28 }
  ];

  // 2. Geometry & Points

  // Plump Chubby Body (rx=168, ry=174)
  const rx_b = 168;
  const ry_b = 174;
  const bodyPoints = [
    { x: 0, y: -ry_b, cubic: { inRotation: 180, inDistance: rx_b * kappa, rotation: 0, outDistance: rx_b * kappa } },
    { x: rx_b, y: 12, cubic: { inRotation: 270, inDistance: ry_b * kappa, rotation: 90, outDistance: ry_b * kappa } },
    { x: 0, y: ry_b, cubic: { inRotation: 0, inDistance: rx_b * kappa, rotation: 180, outDistance: rx_b * kappa } },
    { x: -rx_b, y: 12, cubic: { inRotation: 90, inDistance: ry_b * kappa, rotation: 270, outDistance: ry_b * kappa } }
  ];

  // Body Cel-Shadow on bottom/back
  const bodyShadowPoints = [
    { x: -150, y: 45, cubic: { inRotation: 290, inDistance: 40, rotation: 110, outDistance: 40 } },
    { x: 0, y: 174, cubic: { inRotation: 180, inDistance: 120, rotation: 0, outDistance: 120 } },
    { x: 150, y: 45, cubic: { inRotation: 70, inDistance: 40, rotation: 250, outDistance: 40 } },
    { x: 0, y: 135, cubic: { inRotation: 0, inDistance: 95, rotation: 180, outDistance: 95 } }
  ];

  // Tail Feathers peeking at bottom-back
  const tailPoints = [
    { x: -35, y: -10, radius: 4 },
    { x: -25, y: 25, radius: 8 },
    { x: 0, y: 32, radius: 10 },
    { x: 25, y: 25, radius: 8 },
    { x: 35, y: -10, radius: 4 }
  ];

  // Ear Tufts (cute jaunty feather crests)
  const earTuftLPoints = [
    { x: 15, y: 10, radius: 4 },
    { x: -28, y: -38, cubic: { inRotation: 300, inDistance: 12, rotation: 120, outDistance: 8 } },
    { x: -22, y: -45, radius: 6 }, // soft rounded tip
    { x: -8, y: -25, cubic: { inRotation: 140, inDistance: 12, rotation: 320, outDistance: 16 } },
    { x: 5, y: 5, radius: 4 }
  ];

  const earTuftRPoints = [
    { x: -15, y: 10, radius: 4 },
    { x: 28, y: -38, cubic: { inRotation: 240, inDistance: 12, rotation: 60, outDistance: 8 } },
    { x: 22, y: -45, radius: 6 },
    { x: 8, y: -25, cubic: { inRotation: 40, inDistance: 12, rotation: 220, outDistance: 16 } },
    { x: -5, y: 5, radius: 4 }
  ];

  // Cheek Fluff Tufts (feather flares on cheeks)
  const cheekTuftLPoints = [
    { x: -105, y: -12, radius: 4 },
    { x: -132, y: -2, radius: 7 },
    { x: -120, y: 12, radius: 5 },
    { x: -135, y: 24, radius: 7 },
    { x: -100, y: 38, radius: 6 }
  ];

  const cheekTuftRPoints = [
    { x: 105, y: -12, radius: 4 },
    { x: 132, y: -2, radius: 7 },
    { x: 120, y: 12, radius: 5 },
    { x: 135, y: 24, radius: 7 },
    { x: 100, y: 38, radius: 6 }
  ];

  // Scalloped Left Wing with 3 distinct feather fingers
  const wingLPoints = [
    { x: 0, y: 0, cubic: { inRotation: 180, inDistance: 12, rotation: 0, outDistance: 12 } },
    { x: -28, y: 35, cubic: { inRotation: 270, inDistance: 20, rotation: 90, outDistance: 20 } },
    // Feather finger 1
    { x: -32, y: 68, radius: 8 },
    { x: -24, y: 78, radius: 6 },
    // Feather finger 2 (longest)
    { x: -20, y: 98, radius: 10 },
    { x: -6, y: 105, radius: 8 },
    // Feather finger 3
    { x: 6, y: 96, radius: 8 },
    { x: 14, y: 80, radius: 6 },
    // Inner edge tucking into body
    { x: 18, y: 45, cubic: { inRotation: 85, inDistance: 28, rotation: 265, outDistance: 28 } }
  ];

  const wingRPoints = [
    { x: 0, y: 0, cubic: { inRotation: 0, inDistance: 12, rotation: 180, outDistance: 12 } },
    { x: 28, y: 35, cubic: { inRotation: 270, inDistance: 20, rotation: 90, outDistance: 20 } },
    // Feather finger 1
    { x: 32, y: 68, radius: 8 },
    { x: 24, y: 78, radius: 6 },
    // Feather finger 2
    { x: 20, y: 98, radius: 10 },
    { x: 6, y: 105, radius: 8 },
    // Feather finger 3
    { x: -6, y: 96, radius: 8 },
    { x: -14, y: 80, radius: 6 },
    // Inner edge
    { x: -18, y: 45, cubic: { inRotation: 95, inDistance: 28, rotation: 275, outDistance: 28 } }
  ];

  // Facial Disk with gentle heart curve
  const facialDiskPoints = [
    { x: 0, y: -28, cubic: { inRotation: 145, inDistance: 20, rotation: 35, outDistance: 20 } },
    { x: 56, y: -64, cubic: { inRotation: 180, inDistance: 24, rotation: 0, outDistance: 24 } },
    { x: 118, y: 6, cubic: { inRotation: 270, inDistance: 34, rotation: 90, outDistance: 34 } },
    { x: 0, y: 62, cubic: { inRotation: 0, inDistance: 40, rotation: 180, outDistance: 40 } },
    { x: -118, y: 6, cubic: { inRotation: 90, inDistance: 34, rotation: 270, outDistance: 34 } },
    { x: -56, y: -64, cubic: { inRotation: 180, inDistance: 24, rotation: 0, outDistance: 24 } }
  ];

  // Expressive Brow Arches
  const browLPoints = [
    { x: -32, y: -24, radius: 4 },
    { x: 0, y: -38, cubic: { inRotation: 180, inDistance: 18, rotation: 0, outDistance: 18 } },
    { x: 32, y: -24, radius: 4 },
    { x: 28, y: -19, radius: 3 },
    { x: 0, y: -33, cubic: { inRotation: 0, inDistance: 16, rotation: 180, outDistance: 16 } },
    { x: -28, y: -19, radius: 3 }
  ];

  const browRPoints = [
    { x: -32, y: -24, radius: 4 },
    { x: 0, y: -38, cubic: { inRotation: 180, inDistance: 18, rotation: 0, outDistance: 18 } },
    { x: 32, y: -24, radius: 4 },
    { x: 28, y: -19, radius: 3 },
    { x: 0, y: -33, cubic: { inRotation: 0, inDistance: 16, rotation: 180, outDistance: 16 } },
    { x: -28, y: -19, radius: 3 }
  ];

  // Chest Feather Scallops (`u` shapes)
  const featherScallop = [
    { x: -14, y: -5, radius: 3 },
    { x: 0, y: 6, cubic: { inRotation: 180, inDistance: 10, rotation: 0, outDistance: 10 } },
    { x: 14, y: -5, radius: 3 },
    { x: 11, y: -3, radius: 2 },
    { x: 0, y: 4, cubic: { inRotation: 0, inDistance: 8, rotation: 180, outDistance: 8 } },
    { x: -11, y: -3, radius: 2 }
  ];

  // Beak (Warm Golden Orange with interior smile)
  const beakUpperPoints = [
    { x: 0, y: -16, cubic: { inRotation: 180, inDistance: 12, rotation: 0, outDistance: 12 } },
    { x: 16, y: -4, cubic: { inRotation: 270, inDistance: 7, rotation: 90, outDistance: 8 } },
    { x: 0, y: 15, radius: 4 },
    { x: -16, y: -4, cubic: { inRotation: 90, inDistance: 8, rotation: 270, outDistance: 7 } }
  ];

  const beakSmilePoints = [
    { x: -10, y: 4, radius: 2 },
    { x: 0, y: 14, radius: 4 },
    { x: 10, y: 4, radius: 2 }
  ];

  // Eyelids (Smooth Circular Domes)
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

  // Feet
  const leftFootPoints = [
    { x: -4, y: -16, radius: 3 },
    { x: 4, y: -16, radius: 3 },
    { x: 6, y: -8, radius: 3 },
    { x: 20, y: -2, radius: 5 },
    { x: 18, y: 4, radius: 5 },
    { x: 7, y: -2, radius: 3 },
    { x: 0, y: 5, radius: 6 },
    { x: -7, y: -2, radius: 3 },
    { x: -18, y: -1, radius: 5 },
    { x: -20, y: -6, radius: 5 },
    { x: -6, y: -8, radius: 3 }
  ];

  const rightFootPoints = [
    { x: -4, y: -16, radius: 3 },
    { x: 4, y: -16, radius: 3 },
    { x: 6, y: -8, radius: 3 },
    { x: 20, y: -6, radius: 5 },
    { x: 18, y: -1, radius: 5 },
    { x: 7, y: -2, radius: 3 },
    { x: 0, y: 5, radius: 6 },
    { x: -7, y: -2, radius: 3 },
    { x: -18, y: 4, radius: 5 },
    { x: -20, y: -2, radius: 5 },
    { x: -6, y: -8, radius: 3 }
  ];

  // 3. Shapes with Crisp Cel-Shading & Vibrant Color Balancing
  const shapes = [
    // 01 Ground Contact Shadow
    {
      id: "ground_shadow",
      type: "ellipse",
      parent: "root",
      x: 0,
      y: 0,
      width: 300,
      height: 42,
      fill: {
        gradient: {
          type: "radial",
          stops: [
            { color: "#552A1C10", position: 0 },
            { color: "#222A1C10", position: 0.6 },
            { color: "#002A1C10", position: 1 }
          ]
        }
      }
    },
    // 02 Tail Feathers (behind body)
    {
      id: "tail_feathers",
      type: "polygon",
      parent: "tail_group",
      x: 0,
      y: 0,
      points: tailPoints,
      fill: { color: "#DFCDB5" }
    },
    // 03 Left Foot
    {
      id: "foot_left",
      type: "polygon",
      parent: "foot_l_group",
      x: 0,
      y: 0,
      points: leftFootPoints,
      fill: {
        gradient: {
          type: "linear",
          start: { x: 0, y: -16 },
          end: { x: 0, y: 5 },
          stops: [
            { color: "#FB923C", position: 0 },
            { color: "#EA580C", position: 0.5 },
            { color: "#9A3412", position: 1 }
          ]
        }
      }
    },
    // 04 Right Foot
    {
      id: "foot_right",
      type: "polygon",
      parent: "foot_r_group",
      x: 0,
      y: 0,
      points: rightFootPoints,
      fill: {
        gradient: {
          type: "linear",
          start: { x: 0, y: -16 },
          end: { x: 0, y: 5 },
          stops: [
            { color: "#FB923C", position: 0 },
            { color: "#EA580C", position: 0.5 },
            { color: "#9A3412", position: 1 }
          ]
        }
      }
    },
    // 05 Left Ear Tuft (Aigrette gauche)
    {
      id: "ear_tuft_l",
      type: "polygon",
      parent: "ear_tuft_l_group",
      x: 0,
      y: 0,
      points: earTuftLPoints,
      fill: { color: "#FAF5E5" }
    },
    // 06 Right Ear Tuft (Aigrette droite)
    {
      id: "ear_tuft_r",
      type: "polygon",
      parent: "ear_tuft_r_group",
      x: 0,
      y: 0,
      points: earTuftRPoints,
      fill: { color: "#FAF5E5" }
    },
    // 07 Left Cheek Tuft
    {
      id: "cheek_tuft_l",
      type: "polygon",
      parent: "head_group",
      x: 0,
      y: 0,
      points: cheekTuftLPoints,
      fill: { color: "#FAF5E5" }
    },
    // 08 Right Cheek Tuft
    {
      id: "cheek_tuft_r",
      type: "polygon",
      parent: "head_group",
      x: 0,
      y: 0,
      points: cheekTuftRPoints,
      fill: { color: "#FAF5E5" }
    },
    // 09 Body Sphere Base (Warm Cream Porcelain/Down)
    {
      id: "body_sphere",
      type: "polygon",
      parent: "body_group",
      x: 0,
      y: 0,
      points: bodyPoints,
      fill: { color: "#FAF5E5" }
    },
    // 10 Body Cel-Shadow (Crisp 3D volume at base)
    {
      id: "body_cel_shadow",
      type: "polygon",
      parent: "body_group",
      x: 0,
      y: 0,
      points: bodyShadowPoints,
      fill: { color: "#DFCBB0" }
    },
    // 11 Fluffy Belly Base
    {
      id: "fluffy_belly",
      type: "ellipse",
      parent: "body_group",
      x: 0,
      y: 65,
      width: 260,
      height: 190,
      fill: { color: "#FFFDF7" }
    },
    // 12 Chest Feather Scallops (`u u u`)
    {
      id: "feather_scallop_center",
      type: "polygon",
      parent: "body_group",
      x: 0,
      y: 35,
      points: featherScallop,
      fill: { color: "#D1BFAB" }
    },
    {
      id: "feather_scallop_left",
      type: "polygon",
      parent: "body_group",
      x: -42,
      y: 48,
      rotation: -8,
      points: featherScallop,
      fill: { color: "#D1BFAB" }
    },
    {
      id: "feather_scallop_right",
      type: "polygon",
      parent: "body_group",
      x: 42,
      y: 48,
      rotation: 8,
      points: featherScallop,
      fill: { color: "#D1BFAB" }
    },
    {
      id: "feather_scallop_low_l",
      type: "polygon",
      parent: "body_group",
      x: -22,
      y: 78,
      rotation: -4,
      points: featherScallop,
      fill: { color: "#D1BFAB" }
    },
    {
      id: "feather_scallop_low_r",
      type: "polygon",
      parent: "body_group",
      x: 22,
      y: 78,
      rotation: 4,
      points: featherScallop,
      fill: { color: "#D1BFAB" }
    },
    // 13 Left Wing (Scalloped feather fingers)
    {
      id: "wing_left",
      type: "polygon",
      parent: "wing_l_group",
      x: 0,
      y: 0,
      points: wingLPoints,
      fill: {
        gradient: {
          type: "linear",
          start: { x: 15, y: 0 },
          end: { x: -25, y: 95 },
          stops: [
            { color: "#FAF5E5", position: 0 },
            { color: "#EFE3CD", position: 0.5 },
            { color: "#D8C5AD", position: 1 }
          ]
        }
      }
    },
    // 14 Right Wing (Scalloped feather fingers)
    {
      id: "wing_right",
      type: "polygon",
      parent: "wing_r_group",
      x: 0,
      y: 0,
      points: wingRPoints,
      fill: {
        gradient: {
          type: "linear",
          start: { x: -15, y: 0 },
          end: { x: 25, y: 95 },
          stops: [
            { color: "#FAF5E5", position: 0 },
            { color: "#EFE3CD", position: 0.5 },
            { color: "#D8C5AD", position: 1 }
          ]
        }
      }
    },
    // 15 Facial Disk (Pure Light Cream Spectacles)
    {
      id: "facial_disk",
      type: "polygon",
      parent: "head_group",
      x: 0,
      y: 0,
      points: facialDiskPoints,
      fill: { color: "#FFFDF7" }
    },
    // 16 Cheek Blush
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
    // 17 Left Eye
    {
      id: "eye_l_brow",
      type: "polygon",
      parent: "eye_l_group",
      x: 0,
      y: -2,
      points: browLPoints,
      fill: { color: "#C4B097" }
    },
    {
      id: "eye_l_socket",
      type: "ellipse",
      parent: "eye_l_group",
      x: 0,
      y: 0,
      width: 72,
      height: 72,
      fill: { color: "#1C0D05" }
    },
    {
      id: "eye_l_iris",
      type: "ellipse",
      parent: "eye_l_group",
      x: 0,
      y: 0,
      width: 68,
      height: 68,
      fill: {
        gradient: {
          type: "radial",
          start: { x: 0, y: 12 },
          end: { x: 28, y: -28 },
          stops: [
            { color: "#FFA61A", position: 0 },
            { color: "#EA8C00", position: 0.45 },
            { color: "#873B00", position: 0.8 },
            { color: "#1C0D05", position: 1 }
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
      width: 42,
      height: 42,
      fill: { color: "#0A0402" }
    },
    {
      id: "eye_l_glint_primary",
      type: "ellipse",
      parent: "eye_l_group",
      x: -12,
      y: -10,
      width: 14,
      height: 14,
      fill: { color: "#FFFFFFFF" }
    },
    {
      id: "eye_l_glint_secondary",
      type: "ellipse",
      parent: "eye_l_group",
      x: 16,
      y: 0,
      width: 6,
      height: 6,
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
      fill: { color: "#FFFDF7" }
    },

    // 18 Right Eye
    {
      id: "eye_r_brow",
      type: "polygon",
      parent: "eye_r_group",
      x: 0,
      y: -2,
      points: browRPoints,
      fill: { color: "#C4B097" }
    },
    {
      id: "eye_r_socket",
      type: "ellipse",
      parent: "eye_r_group",
      x: 0,
      y: 0,
      width: 72,
      height: 72,
      fill: { color: "#1C0D05" }
    },
    {
      id: "eye_r_iris",
      type: "ellipse",
      parent: "eye_r_group",
      x: 0,
      y: 0,
      width: 68,
      height: 68,
      fill: {
        gradient: {
          type: "radial",
          start: { x: 0, y: 12 },
          end: { x: 28, y: -28 },
          stops: [
            { color: "#FFA61A", position: 0 },
            { color: "#EA8C00", position: 0.45 },
            { color: "#873B00", position: 0.8 },
            { color: "#1C0D05", position: 1 }
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
      width: 42,
      height: 42,
      fill: { color: "#0A0402" }
    },
    {
      id: "eye_r_glint_primary",
      type: "ellipse",
      parent: "eye_r_group",
      x: -12,
      y: -10,
      width: 14,
      height: 14,
      fill: { color: "#FFFFFFFF" }
    },
    {
      id: "eye_r_glint_secondary",
      type: "ellipse",
      parent: "eye_r_group",
      x: 16,
      y: 0,
      width: 6,
      height: 6,
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
      fill: { color: "#FFFDF7" }
    },

    // 19 Beak & Mouth (Warm Golden Orange with interior smile)
    {
      id: "beak_base",
      type: "polygon",
      parent: "beak_group",
      x: 0,
      y: 0,
      points: beakUpperPoints,
      fill: {
        gradient: {
          type: "linear",
          start: { x: 0, y: -16 },
          end: { x: 0, y: 15 },
          stops: [
            { color: "#FDBA74", position: 0 },
            { color: "#EA580C", position: 0.5 },
            { color: "#9A3412", position: 1 }
          ]
        }
      }
    },
    {
      id: "beak_smile_cavity",
      type: "polygon",
      parent: "beak_group",
      x: 0,
      y: 0,
      points: beakSmilePoints,
      fill: { color: "#7C2D12" }
    },
    {
      id: "beak_glint",
      type: "ellipse",
      parent: "beak_group",
      x: 0,
      y: -8,
      width: 8,
      height: 5,
      fill: { color: "#FED7AA" }
    }
  ];

  // 4. Animating Respiration, Ear Wiggle, Wing Harmonic Delay, and Blink
  const animations = [
    {
      name: "idle",
      fps: 60,
      duration: 120,
      loop: "loop",
      tracks: [
        // Body breathing
        {
          target: "body_group",
          property: "y",
          keyframes: [
            { frame: 0, value: -184, easing: "ease-in-out" },
            { frame: 60, value: -189, easing: "ease-in-out" },
            { frame: 120, value: -184, easing: "ease-in-out" }
          ]
        },
        {
          target: "body_group",
          property: "scaleY",
          keyframes: [
            { frame: 0, value: 1.0, easing: "ease-in-out" },
            { frame: 60, value: 1.03, easing: "ease-in-out" },
            { frame: 120, value: 1.0, easing: "ease-in-out" }
          ]
        },
        {
          target: "body_group",
          property: "scaleX",
          keyframes: [
            { frame: 0, value: 1.0, easing: "ease-in-out" },
            { frame: 60, value: 0.98, easing: "ease-in-out" },
            { frame: 120, value: 1.0, easing: "ease-in-out" }
          ]
        },
        // Wings breathing with harmonic phase shift
        {
          target: "wing_l_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0, easing: "ease-in-out" },
            { frame: 60, value: -3.0, easing: "ease-in-out" },
            { frame: 120, value: 0, easing: "ease-in-out" }
          ]
        },
        {
          target: "wing_r_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0, easing: "ease-in-out" },
            { frame: 60, value: 3.0, easing: "ease-in-out" },
            { frame: 120, value: 0, easing: "ease-in-out" }
          ]
        },
        // Ear tufts subtle organic twitch
        {
          target: "ear_tuft_l_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0, easing: "ease-in-out" },
            { frame: 55, value: 2.5, easing: "ease-in-out" },
            { frame: 120, value: 0, easing: "ease-in-out" }
          ]
        },
        {
          target: "ear_tuft_r_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0, easing: "ease-in-out" },
            { frame: 55, value: -2.5, easing: "ease-in-out" },
            { frame: 120, value: 0, easing: "ease-in-out" }
          ]
        },
        // Ground shadow breathing
        {
          target: "ground_shadow",
          property: "scaleX",
          keyframes: [
            { frame: 0, value: 1.0, easing: "ease-in-out" },
            { frame: 60, value: 0.95, easing: "ease-in-out" },
            { frame: 120, value: 1.0, easing: "ease-in-out" }
          ]
        },
        // Conscious blink
        {
          target: "eye_l_eyelid",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 69, value: 0 },
            { frame: 75, value: 1, easing: "ease-in" },
            { frame: 80, value: 1 },
            { frame: 85, value: 0, easing: "ease-out" },
            { frame: 120, value: 0 }
          ]
        },
        {
          target: "eye_r_eyelid",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 69, value: 0 },
            { frame: 75, value: 1, easing: "ease-in" },
            { frame: 80, value: 1 },
            { frame: 85, value: 0, easing: "ease-out" },
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
    artboard: { name: "Owluko_Fluffy", width: 512, height: 512 },
    backgroundColor: "#FAFAFA",
    groups,
    shapes,
    animations,
    stateMachine
  };

  const scenePath = "mascots/owluko/owluko_pure_vector.scene.json";
  fs.writeFileSync(scenePath, JSON.stringify(scene, null, 2));
  console.log("Updated " + scenePath);

  const outRivPath = "mascots/owluko/owluko_pure_vector.riv";
  console.log("Compiling to " + outRivPath + " via riv_create...");
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
    time: 1.3,
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

buildOwlukoPro().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
