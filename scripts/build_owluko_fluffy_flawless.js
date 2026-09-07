const fs = require("fs");
const path = require("path");
const { callMcpTool } = require("./rive_mcp_client.js");

const kappa = 0.5522847498307936;

async function buildOwlukoFluffyFlawless() {
  console.log("===============================================================");
  console.log("  BUILDING FLAWLESS FLUFFY BABY OWLUKO (100% REFERENCE CALQUE)");
  console.log("  Seamless Integrated Wings, Plump Bean Toes, Glassy Amber Eyes");
  console.log("===============================================================");

  // Artboard: 512x512
  // Center: x = 256, Ground baseline: y = 472
  const groups = [
    { id: "root", x: 256, y: 472 },
    { id: "shadow_group", parent: "root", x: 0, y: 0 },
    { id: "feet_group", parent: "root", x: 0, y: 0 },
    { id: "foot_l_group", parent: "feet_group", x: -62, y: 0 },
    { id: "foot_r_group", parent: "feet_group", x: 62, y: 0 },
    { id: "body_group", parent: "root", x: 0, y: -190 },
    { id: "wing_l_group", parent: "body_group", x: -145, y: 20 },
    { id: "wing_r_group", parent: "body_group", x: 145, y: 20 },
    { id: "head_group", parent: "body_group", x: 0, y: -80 },
    { id: "eye_l_group", parent: "head_group", x: -57, y: 0 },
    { id: "eye_r_group", parent: "head_group", x: 55, y: 0 },
    { id: "eyelid_l_group", parent: "eye_l_group", x: 0, y: 0 },
    { id: "eyelid_r_group", parent: "eye_r_group", x: 0, y: 0 },
    { id: "beak_group", parent: "head_group", x: 0, y: 28 }
  ];

  // 1. Plump Spherical Body (rx=170, ry=176)
  const rx_b = 170;
  const ry_b = 176;
  const bodyPoints = [
    { x: 0, y: -ry_b, cubic: { inRotation: 180, inDistance: rx_b * kappa, rotation: 0, outDistance: rx_b * kappa } },
    { x: rx_b, y: 15, cubic: { inRotation: 270, inDistance: ry_b * kappa, rotation: 90, outDistance: ry_b * kappa } },
    { x: 0, y: ry_b, cubic: { inRotation: 0, inDistance: rx_b * kappa, rotation: 180, outDistance: rx_b * kappa } },
    { x: -rx_b, y: 15, cubic: { inRotation: 90, inDistance: ry_b * kappa, rotation: 270, outDistance: ry_b * kappa } }
  ];

  // 2. Integrated Lateral Down Wings (Smooth lateral flank swells)
  // Left Wing:
  // Origin at shoulder (0, 0) in wing_l_group (x=-145, y=20 in body)
  // Curves smoothly along the spherical contour of the body
  const leftWingPoints = [
    // Shoulder junction (smooth transition from body)
    { x: 15, y: -15, cubic: { inRotation: 190, inDistance: 15, rotation: 10, outDistance: 15 } },
    // Outer flank swell (soft rounded curve)
    { x: -24, y: 40, cubic: { inRotation: 275, inDistance: 32, rotation: 95, outDistance: 32 } },
    // Lower rounded wing tip
    { x: -14, y: 105, cubic: { inRotation: 300, inDistance: 16, rotation: 120, outDistance: 14 } },
    { x: 2, y: 112, radius: 10 },
    // Inner contour tucking against the belly
    { x: 22, y: 95, cubic: { inRotation: 80, inDistance: 18, rotation: 260, outDistance: 18 } },
    { x: 25, y: 35, cubic: { inRotation: 85, inDistance: 35, rotation: 265, outDistance: 35 } }
  ];

  // Left Wing Crease Shadow (ambient occlusion between wing and belly)
  const leftWingCreasePoints = [
    { x: 25, y: 30, cubic: { inRotation: 85, inDistance: 35, rotation: 265, outDistance: 35 } },
    { x: 22, y: 95, cubic: { inRotation: 80, inDistance: 18, rotation: 260, outDistance: 18 } },
    { x: 2, y: 112, radius: 8 },
    { x: 8, y: 105, radius: 6 },
    { x: 16, y: 88, cubic: { inRotation: 80, inDistance: 14, rotation: 260, outDistance: 14 } },
    { x: 20, y: 32, cubic: { inRotation: 85, inDistance: 30, rotation: 265, outDistance: 30 } }
  ];

  // Right Wing (mirrored):
  const rightWingPoints = [
    { x: -15, y: -15, cubic: { inRotation: 350, inDistance: 15, rotation: 170, outDistance: 15 } },
    { x: 24, y: 40, cubic: { inRotation: 265, inDistance: 32, rotation: 85, outDistance: 32 } },
    { x: 14, y: 105, cubic: { inRotation: 240, inDistance: 16, rotation: 60, outDistance: 14 } },
    { x: -2, y: 112, radius: 10 },
    { x: -22, y: 95, cubic: { inRotation: 100, inDistance: 18, rotation: 280, outDistance: 18 } },
    { x: -25, y: 35, cubic: { inRotation: 95, inDistance: 35, rotation: 275, outDistance: 35 } }
  ];

  const rightWingCreasePoints = [
    { x: -25, y: 30, cubic: { inRotation: 95, inDistance: 35, rotation: 275, outDistance: 35 } },
    { x: -22, y: 95, cubic: { inRotation: 100, inDistance: 18, rotation: 280, outDistance: 18 } },
    { x: -2, y: 112, radius: 8 },
    { x: -8, y: 105, radius: 6 },
    { x: -16, y: 88, cubic: { inRotation: 100, inDistance: 14, rotation: 280, outDistance: 14 } },
    { x: -20, y: 32, cubic: { inRotation: 95, inDistance: 30, rotation: 275, outDistance: 30 } }
  ];

  // 3. Plump Rounded Bean Toes (3 distinct chubby bean toes per foot)
  // Left Foot:
  // Toe 1 (Outer left toe)
  const toeL1 = { x: -20, y: -8, width: 17, height: 26, rotation: -24 };
  // Toe 2 (Middle toe)
  const toeL2 = { x: 0, y: -6, width: 18, height: 28, rotation: -4 };
  // Toe 3 (Inner right toe)
  const toeL3 = { x: 18, y: -8, width: 17, height: 25, rotation: 16 };

  // Right Foot:
  // Toe 1 (Inner left toe)
  const toeR1 = { x: -18, y: -8, width: 17, height: 25, rotation: -16 };
  // Toe 2 (Middle toe)
  const toeR2 = { x: 0, y: -6, width: 18, height: 28, rotation: 4 };
  // Toe 3 (Outer right toe)
  const toeR3 = { x: 20, y: -8, width: 17, height: 26, rotation: 24 };

  // 4. Facial Disk (Barn owl soft heart / spectacles contour)
  const facialDiskPoints = [
    { x: 0, y: -28, cubic: { inRotation: 145, inDistance: 22, rotation: 35, outDistance: 22 } },
    { x: 56, y: -64, cubic: { inRotation: 180, inDistance: 24, rotation: 0, outDistance: 24 } },
    { x: 116, y: 6, cubic: { inRotation: 270, inDistance: 34, rotation: 90, outDistance: 34 } },
    { x: 0, y: 62, cubic: { inRotation: 0, inDistance: 40, rotation: 180, outDistance: 40 } },
    { x: -116, y: 6, cubic: { inRotation: 90, inDistance: 34, rotation: 270, outDistance: 34 } },
    { x: -56, y: -64, cubic: { inRotation: 180, inDistance: 24, rotation: 0, outDistance: 24 } }
  ];

  // 5. Beak (Cute warm orange cone nestled between eyes)
  const beakPoints = [
    { x: 0, y: -16, cubic: { inRotation: 180, inDistance: 13, rotation: 0, outDistance: 13 } },
    { x: 16, y: -5, cubic: { inRotation: 270, inDistance: 6, rotation: 90, outDistance: 8 } },
    { x: 0, y: 15, radius: 4 },
    { x: -16, y: -5, cubic: { inRotation: 90, inDistance: 8, rotation: 270, outDistance: 6 } }
  ];

  // 6. Eyelids (Circular domes for blink)
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

  // 7. Complete Shapes & Authentic Soft Down Shading
  const shapes = [
    // 01 Soft Ground Shadows
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
      width: 230,
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

    // 02 Plump Bean Toes (Left Foot)
    {
      id: "foot_l_toe1",
      type: "ellipse",
      parent: "foot_l_group",
      x: toeL1.x,
      y: toeL1.y,
      width: toeL1.width,
      height: toeL1.height,
      rotation: toeL1.rotation,
      fill: {
        gradient: {
          type: "linear",
          start: { x: 0, y: -13 },
          end: { x: 0, y: 13 },
          stops: [
            { color: "#FDBA74", position: 0 },
            { color: "#EA580C", position: 0.5 },
            { color: "#9A3412", position: 1 }
          ]
        }
      }
    },
    {
      id: "foot_l_toe3",
      type: "ellipse",
      parent: "foot_l_group",
      x: toeL3.x,
      y: toeL3.y,
      width: toeL3.width,
      height: toeL3.height,
      rotation: toeL3.rotation,
      fill: {
        gradient: {
          type: "linear",
          start: { x: 0, y: -13 },
          end: { x: 0, y: 13 },
          stops: [
            { color: "#FDBA74", position: 0 },
            { color: "#EA580C", position: 0.5 },
            { color: "#9A3412", position: 1 }
          ]
        }
      }
    },
    // Middle toe (on top of side toes)
    {
      id: "foot_l_toe2",
      type: "ellipse",
      parent: "foot_l_group",
      x: toeL2.x,
      y: toeL2.y,
      width: toeL2.width,
      height: toeL2.height,
      rotation: toeL2.rotation,
      fill: {
        gradient: {
          type: "linear",
          start: { x: 0, y: -14 },
          end: { x: 0, y: 14 },
          stops: [
            { color: "#FDBA74", position: 0 },
            { color: "#EA580C", position: 0.5 },
            { color: "#9A3412", position: 1 }
          ]
        }
      }
    },

    // 03 Plump Bean Toes (Right Foot)
    {
      id: "foot_r_toe1",
      type: "ellipse",
      parent: "foot_r_group",
      x: toeR1.x,
      y: toeR1.y,
      width: toeR1.width,
      height: toeR1.height,
      rotation: toeR1.rotation,
      fill: {
        gradient: {
          type: "linear",
          start: { x: 0, y: -13 },
          end: { x: 0, y: 13 },
          stops: [
            { color: "#FDBA74", position: 0 },
            { color: "#EA580C", position: 0.5 },
            { color: "#9A3412", position: 1 }
          ]
        }
      }
    },
    {
      id: "foot_r_toe3",
      type: "ellipse",
      parent: "foot_r_group",
      x: toeR3.x,
      y: toeR3.y,
      width: toeR3.width,
      height: toeR3.height,
      rotation: toeR3.rotation,
      fill: {
        gradient: {
          type: "linear",
          start: { x: 0, y: -13 },
          end: { x: 0, y: 13 },
          stops: [
            { color: "#FDBA74", position: 0 },
            { color: "#EA580C", position: 0.5 },
            { color: "#9A3412", position: 1 }
          ]
        }
      }
    },
    // Middle toe (on top)
    {
      id: "foot_r_toe2",
      type: "ellipse",
      parent: "foot_r_group",
      x: toeR2.x,
      y: toeR2.y,
      width: toeR2.width,
      height: toeR2.height,
      rotation: toeR2.rotation,
      fill: {
        gradient: {
          type: "linear",
          start: { x: 0, y: -14 },
          end: { x: 0, y: 14 },
          stops: [
            { color: "#FDBA74", position: 0 },
            { color: "#EA580C", position: 0.5 },
            { color: "#9A3412", position: 1 }
          ]
        }
      }
    },

    // 04 Body Sphere (Warm, soft, fluffy baby owl body ball)
    {
      id: "body_sphere",
      type: "polygon",
      parent: "body_group",
      x: 0,
      y: 0,
      points: bodyPoints,
      fill: {
        gradient: {
          type: "radial",
          start: { x: -30, y: -60 },
          end: { x: 60, y: 170 },
          stops: [
            { color: "#FFFDF7", position: 0 },
            { color: "#F5ECE0", position: 0.4 },
            { color: "#E5D6C1", position: 0.75 },
            { color: "#C8B59D", position: 1 }
          ]
        }
      }
    },

    // 05 Left Wing (Integrated side down flap)
    {
      id: "wing_left",
      type: "polygon",
      parent: "wing_l_group",
      x: 0,
      y: 0,
      points: leftWingPoints,
      fill: {
        gradient: {
          type: "linear",
          start: { x: -24, y: 20 },
          end: { x: 22, y: 95 },
          stops: [
            { color: "#F7EFE2", position: 0 },
            { color: "#EDE0CD", position: 0.5 },
            { color: "#D4C1A8", position: 1 }
          ]
        }
      }
    },
    // Left Wing Flank Crease Shadow (gives 3D depth against belly)
    {
      id: "wing_l_crease",
      type: "polygon",
      parent: "wing_l_group",
      x: 0,
      y: 0,
      points: leftWingCreasePoints,
      fill: { color: "#CBB69E" }
    },

    // 06 Right Wing (Integrated side down flap)
    {
      id: "wing_right",
      type: "polygon",
      parent: "wing_r_group",
      x: 0,
      y: 0,
      points: rightWingPoints,
      fill: {
        gradient: {
          type: "linear",
          start: { x: 24, y: 20 },
          end: { x: -22, y: 95 },
          stops: [
            { color: "#F7EFE2", position: 0 },
            { color: "#EDE0CD", position: 0.5 },
            { color: "#D4C1A8", position: 1 }
          ]
        }
      }
    },
    // Right Wing Flank Crease Shadow
    {
      id: "wing_r_crease",
      type: "polygon",
      parent: "wing_r_group",
      x: 0,
      y: 0,
      points: rightWingCreasePoints,
      fill: { color: "#CBB69E" }
    },

    // 07 Seamless Fluffy Belly Down (soft lighter down patch on front)
    {
      id: "fluffy_belly",
      type: "ellipse",
      parent: "body_group",
      x: 0,
      y: 65,
      width: 255,
      height: 190,
      fill: {
        gradient: {
          type: "radial",
          stops: [
            { color: "#FFFFFFFF", position: 0 },
            { color: "#FAF6ED", position: 0.65 },
            { color: "#EFE5D5", position: 0.88 },
            { color: "#DECDB5", position: 1 }
          ]
        }
      }
    },

    // 08 Facial Disk (Barn Owl Heart / Spectacles)
    {
      id: "facial_disk",
      type: "polygon",
      parent: "head_group",
      x: 0,
      y: 0,
      points: facialDiskPoints,
      fill: {
        gradient: {
          type: "radial",
          stops: [
            { color: "#FFFFFFFF", position: 0 },
            { color: "#FAF7EE", position: 0.65 },
            { color: "#EFE6D7", position: 0.88 },
            { color: "#DFCEB8", position: 1 }
          ]
        }
      }
    },

    // 09 Soft Cheek Blush
    {
      id: "blush_left",
      type: "ellipse",
      parent: "head_group",
      x: -88,
      y: 26,
      width: 36,
      height: 16,
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
      width: 36,
      height: 16,
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

    // 10 Left Eye (Soulful Glassy Radiant Amber Orb)
    {
      id: "eye_l_crease",
      type: "ellipse",
      parent: "eye_l_group",
      x: 0,
      y: -2,
      width: 76,
      height: 76,
      fill: {
        gradient: {
          type: "radial",
          stops: [
            { color: "#003A1F10", position: 0.7 },
            { color: "#443A1F10", position: 0.9 },
            { color: "#663A1F10", position: 1.0 }
          ]
        }
      }
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
    // Primary Glint (10:30 o'clock)
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
    // Secondary Glint (2:30 o'clock)
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
    // Retractable Eyelid
    {
      id: "eye_l_eyelid",
      type: "polygon",
      parent: "eyelid_l_group",
      x: 0,
      y: 0,
      opacity: 0,
      points: eyelidLPoints,
      fill: {
        gradient: {
          type: "linear",
          start: { x: 0, y: -36 },
          end: { x: 0, y: 20 },
          stops: [
            { color: "#FAF5EA", position: 0 },
            { color: "#EFE5D5", position: 0.8 },
            { color: "#DECDB5", position: 1 }
          ]
        }
      }
    },

    // 11 Right Eye
    {
      id: "eye_r_crease",
      type: "ellipse",
      parent: "eye_r_group",
      x: 0,
      y: -2,
      width: 76,
      height: 76,
      fill: {
        gradient: {
          type: "radial",
          stops: [
            { color: "#003A1F10", position: 0.7 },
            { color: "#443A1F10", position: 0.9 },
            { color: "#663A1F10", position: 1.0 }
          ]
        }
      }
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
      fill: {
        gradient: {
          type: "linear",
          start: { x: 0, y: -36 },
          end: { x: 0, y: 20 },
          stops: [
            { color: "#FAF5EA", position: 0 },
            { color: "#EFE5D5", position: 0.8 },
            { color: "#DECDB5", position: 1 }
          ]
        }
      }
    },

    // 12 Beak (Warm orange cone nestled between eyes)
    {
      id: "beak",
      type: "polygon",
      parent: "beak_group",
      x: 0,
      y: 0,
      points: beakPoints,
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

  // 8. Organic 60 FPS Respiration Loop
  const animations = [
    {
      name: "idle",
      fps: 60,
      duration: 120,
      loop: "loop",
      tracks: [
        // Gentle spherical body breathing
        {
          target: "body_group",
          property: "y",
          keyframes: [
            { frame: 0, value: -190, easing: "ease-in-out" },
            { frame: 60, value: -195, easing: "ease-in-out" },
            { frame: 120, value: -190, easing: "ease-in-out" }
          ]
        },
        {
          target: "body_group",
          property: "scaleY",
          keyframes: [
            { frame: 0, value: 1.0, easing: "ease-in-out" },
            { frame: 60, value: 1.025, easing: "ease-in-out" },
            { frame: 120, value: 1.0, easing: "ease-in-out" }
          ]
        },
        {
          target: "body_group",
          property: "scaleX",
          keyframes: [
            { frame: 0, value: 1.0, easing: "ease-in-out" },
            { frame: 60, value: 0.985, easing: "ease-in-out" },
            { frame: 120, value: 1.0, easing: "ease-in-out" }
          ]
        },
        // Subtle organic wing breathing
        {
          target: "wing_l_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0, easing: "ease-in-out" },
            { frame: 60, value: -2.0, easing: "ease-in-out" },
            { frame: 120, value: 0, easing: "ease-in-out" }
          ]
        },
        {
          target: "wing_r_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0, easing: "ease-in-out" },
            { frame: 60, value: 2.0, easing: "ease-in-out" },
            { frame: 120, value: 0, easing: "ease-in-out" }
          ]
        },
        // Ground shadow breathing
        {
          target: "shadow_group",
          property: "scaleX",
          keyframes: [
            { frame: 0, value: 1.0, easing: "ease-in-out" },
            { frame: 60, value: 0.95, easing: "ease-in-out" },
            { frame: 120, value: 1.0, easing: "ease-in-out" }
          ]
        },
        // Conscious blink at frame 70..85
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
  console.log("Written updated scene to " + scenePath);

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

buildOwlukoFluffyFlawless().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
