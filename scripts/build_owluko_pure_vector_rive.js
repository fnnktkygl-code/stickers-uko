const { callMcpTool } = require("./rive_mcp_client.js");
const fs = require("fs");
const path = require("path");

async function buildOwlukoPureVectorRive() {
  console.log("==========================================================");
  console.log("  BUILDING OWLUKO 100% PURE NATIVE VECTOR RIVE MASCOT");
  console.log("  Ground Truth Reference: media_1788730079164.jpg");
  console.log("==========================================================");

  const kappa = 0.5522847498307936;

  // 1. Precise body egg contour (smooth organic bezier curves)
  // Measured from reference front view:
  // Center: (0, 0), Top at (0, -195), Bottom at (0, 185)
  // Left waist at (-132, 25), Right waist at (+132, 25)
  const bodyPoints = [
    // Top apex (0, -195)
    {
      x: 0,
      y: -195,
      cubic: {
        inRotation: 180,
        inDistance: 105 * kappa,
        rotation: 0,
        outDistance: 105 * kappa
      }
    },
    // Upper Right curve (98, -110)
    {
      x: 98,
      y: -110,
      cubic: {
        inRotation: 245,
        inDistance: 55,
        rotation: 65,
        outDistance: 55
      }
    },
    // Right waist (132, 25)
    {
      x: 132,
      y: 25,
      cubic: {
        inRotation: 270,
        inDistance: 70,
        rotation: 90,
        outDistance: 70
      }
    },
    // Lower Right belly (105, 140)
    {
      x: 105,
      y: 140,
      cubic: {
        inRotation: 295,
        inDistance: 55,
        rotation: 115,
        outDistance: 55
      }
    },
    // Bottom apex (0, 185)
    {
      x: 0,
      y: 185,
      cubic: {
        inRotation: 0,
        inDistance: 95 * kappa,
        rotation: 180,
        outDistance: 95 * kappa
      }
    },
    // Lower Left belly (-105, 140)
    {
      x: -105,
      y: 140,
      cubic: {
        inRotation: 65,
        inDistance: 55,
        rotation: 245,
        outDistance: 55
      }
    },
    // Left waist (-132, 25)
    {
      x: -132,
      y: 25,
      cubic: {
        inRotation: 90,
        inDistance: 70,
        rotation: 270,
        outDistance: 70
      }
    },
    // Upper Left curve (-98, -110)
    {
      x: -98,
      y: -110,
      cubic: {
        inRotation: 115,
        inDistance: 55,
        rotation: 295,
        outDistance: 55
      }
    }
  ];

  // 2. Left Wing contour (streamlined porcelain petal flush against flank)
  // Pivot at shoulder (0, 0), wing extends down to (x: -8, y: 195)
  const leftWingPoints = [
    // Top shoulder
    {
      x: 0,
      y: 0,
      cubic: {
        inRotation: 180,
        inDistance: 16 * kappa,
        rotation: 0,
        outDistance: 16 * kappa
      }
    },
    // Outer flank swell
    {
      x: -24,
      y: 95,
      cubic: {
        inRotation: 270,
        inDistance: 50,
        rotation: 90,
        outDistance: 50
      }
    },
    // Wing tip bottom
    {
      x: -8,
      y: 195,
      cubic: {
        inRotation: 290,
        inDistance: 18,
        rotation: 110,
        outDistance: 18
      }
    },
    // Inner contour tucking against body
    {
      x: 18,
      y: 100,
      cubic: {
        inRotation: 85,
        inDistance: 55,
        rotation: 265,
        outDistance: 55
      }
    }
  ];

  // 3. Right Wing contour (symmetrical to left wing)
  const rightWingPoints = [
    // Top shoulder
    {
      x: 0,
      y: 0,
      cubic: {
        inRotation: 0,
        inDistance: 16 * kappa,
        rotation: 180,
        outDistance: 16 * kappa
      }
    },
    // Outer flank swell
    {
      x: 24,
      y: 95,
      cubic: {
        inRotation: 270,
        inDistance: 50,
        rotation: 90,
        outDistance: 50
      }
    },
    // Wing tip bottom
    {
      x: 8,
      y: 195,
      cubic: {
        inRotation: 250,
        inDistance: 18,
        rotation: 70,
        outDistance: 18
      }
    },
    // Inner contour tucking against body
    {
      x: -18,
      y: 100,
      cubic: {
        inRotation: 95,
        inDistance: 55,
        rotation: 275,
        outDistance: 55
      }
    }
  ];

  // 4. Beak contour (smooth porcelain drop nestled between eyes)
  const beakPoints = [
    // Top bridge
    {
      x: 0,
      y: -22,
      cubic: {
        inRotation: 180,
        inDistance: 12 * kappa,
        rotation: 0,
        outDistance: 12 * kappa
      }
    },
    // Right cheek junction
    {
      x: 13,
      y: -10,
      cubic: {
        inRotation: 270,
        inDistance: 8,
        rotation: 90,
        outDistance: 12
      }
    },
    // Beak tip
    {
      x: 0,
      y: 24,
      cubic: {
        inRotation: 340,
        inDistance: 7,
        rotation: 200,
        outDistance: 7
      }
    },
    // Left cheek junction
    {
      x: -13,
      y: -10,
      cubic: {
        inRotation: 90,
        inDistance: 12,
        rotation: 270,
        outDistance: 8
      }
    }
  ];

  // 5. Avian 3-toed foot contour (rounded porcelain knuckles resting on ground)
  const leftFootPoints = [
    { x: 0, y: -28, radius: 4 },
    { x: 6, y: -16, radius: 3 },
    { x: 22, y: -2, radius: 6 },
    { x: 18, y: 3, radius: 6 },
    { x: 8, y: -5, radius: 3 },
    { x: 0, y: 5, radius: 7 },
    { x: -8, y: -4, radius: 3 },
    { x: -24, y: 1, radius: 6 },
    { x: -26, y: -5, radius: 6 },
    { x: -6, y: -16, radius: 3 }
  ];

  const rightFootPoints = [
    { x: 0, y: -28, radius: 4 },
    { x: -6, y: -16, radius: 3 },
    { x: -22, y: -2, radius: 6 },
    { x: -18, y: 3, radius: 6 },
    { x: -8, y: -5, radius: 3 },
    { x: 0, y: 5, radius: 7 },
    { x: 8, y: -4, radius: 3 },
    { x: 24, y: 1, radius: 6 },
    { x: 26, y: -5, radius: 6 },
    { x: 6, y: -16, radius: 3 }
  ];

  // 6. Porcelain eyelid hood contour (covers top 40% of eye in neutral expression)
  const leftEyelidPoints = [
    { x: -30, y: -14, radius: 6 },
    {
      x: 0,
      y: -29,
      cubic: {
        inRotation: 180,
        inDistance: 24 * kappa,
        rotation: 0,
        outDistance: 24 * kappa
      }
    },
    { x: 30, y: -14, radius: 6 },
    { x: 30, y: 2, radius: 4 },
    {
      x: 0,
      y: 6,
      cubic: {
        inRotation: 0,
        inDistance: 16 * kappa,
        rotation: 180,
        outDistance: 16 * kappa
      }
    },
    { x: -30, y: 2, radius: 4 }
  ];

  const rightEyelidPoints = [
    { x: -30, y: -14, radius: 6 },
    {
      x: 0,
      y: -29,
      cubic: {
        inRotation: 180,
        inDistance: 24 * kappa,
        rotation: 0,
        outDistance: 24 * kappa
      }
    },
    { x: 30, y: -14, radius: 6 },
    { x: 30, y: 2, radius: 4 },
    {
      x: 0,
      y: 6,
      cubic: {
        inRotation: 0,
        inDistance: 16 * kappa,
        rotation: 180,
        outDistance: 16 * kappa
      }
    },
    { x: -30, y: 2, radius: 4 }
  ];

  // Full native vector scene specification
  const scene = {
    artboard: { name: "Owluko_Master", width: 512, height: 512 },
    backgroundColor: "#18181B",
    groups: [
      { id: "root", x: 256, y: 485 },
      { id: "feet_group", parent: "root", x: 0, y: 0 },
      { id: "foot_l_group", parent: "feet_group", x: -62, y: 0 },
      { id: "foot_r_group", parent: "feet_group", x: +62, y: 0 },
      { id: "body_group", parent: "root", x: 0, y: -245 },
      { id: "wing_l_group", parent: "body_group", x: -128, y: -50 },
      { id: "wing_r_group", parent: "body_group", x: +128, y: -50 },
      { id: "head_group", parent: "body_group", x: 0, y: -80 },
      { id: "eye_l_group", parent: "head_group", x: -60, y: 0 },
      { id: "eye_r_group", parent: "head_group", x: +60, y: 0 },
      { id: "eyelid_l_group", parent: "eye_l_group", x: 0, y: 0 },
      { id: "eyelid_r_group", parent: "eye_r_group", x: 0, y: 0 }
    ],
    shapes: [
      // 01 Ground Contact Shadow
      {
        id: "ground_shadow",
        type: "ellipse",
        parent: "root",
        x: 0,
        y: 0,
        width: 230,
        height: 42,
        fill: {
          gradient: {
            type: "radial",
            stops: [
              { color: "#77000000", position: 0 },
              { color: "#33000000", position: 0.55 },
              { color: "#00000000", position: 1.0 }
            ]
          }
        }
      },
      // 02 Left Foot (porcelain avian claws)
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
            start: { x: 0, y: -28 },
            end: { x: 0, y: 5 },
            stops: [
              { color: "#D1C2B0", position: 0 },
              { color: "#A89480", position: 0.5 },
              { color: "#786552", position: 1.0 }
            ]
          }
        }
      },
      // 03 Right Foot
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
            start: { x: 0, y: -28 },
            end: { x: 0, y: 5 },
            stops: [
              { color: "#D1C2B0", position: 0 },
              { color: "#A89480", position: 0.5 },
              { color: "#786552", position: 1.0 }
            ]
          }
        }
      },
      // 04 Wings
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
            start: { x: 10, y: 0 },
            end: { x: -20, y: 190 },
            stops: [
              { color: "#FFFDF9", position: 0 },
              { color: "#F4ECE1", position: 0.3 },
              { color: "#DECFC0", position: 0.7 },
              { color: "#AD9B88", position: 1.0 }
            ]
          }
        }
      },
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
            start: { x: -10, y: 0 },
            end: { x: 20, y: 190 },
            stops: [
              { color: "#FFFDF9", position: 0 },
              { color: "#F4ECE1", position: 0.3 },
              { color: "#DECFC0", position: 0.7 },
              { color: "#AD9B88", position: 1.0 }
            ]
          }
        }
      },
      // 05 Continuous Porcelain Body Capsule
      {
        id: "body_capsule",
        type: "polygon",
        parent: "body_group",
        x: 0,
        y: 0,
        points: bodyPoints,
        fill: {
          gradient: {
            type: "linear",
            start: { x: -60, y: -195 },
            end: { x: 60, y: 185 },
            stops: [
              { color: "#FFFDF9", position: 0 },
              { color: "#F8F1E7", position: 0.25 },
              { color: "#E8DDCF", position: 0.6 },
              { color: "#CEBEAC", position: 0.85 },
              { color: "#9E8D7B", position: 1.0 }
            ]
          }
        }
      },
      // 06 Cranial Specular Glint
      {
        id: "cranial_specular",
        type: "ellipse",
        parent: "body_group",
        x: -36,
        y: -130,
        width: 130,
        height: 80,
        rotation: -18,
        fill: {
          gradient: {
            type: "radial",
            stops: [
              { color: "#66FFFFFF", position: 0 },
              { color: "#22FFFFFF", position: 0.5 },
              { color: "#00FFFFFF", position: 1.0 }
            ]
          }
        }
      },
      // 07 Belly Ambient Light
      {
        id: "belly_bounce",
        type: "ellipse",
        parent: "body_group",
        x: 0,
        y: 145,
        width: 170,
        height: 60,
        fill: {
          gradient: {
            type: "radial",
            stops: [
              { color: "#33FFF5E6", position: 0 },
              { color: "#00FFF5E6", position: 1.0 }
            ]
          }
        }
      },
      // 08 Eye Socket Soft Recesses
      {
        id: "eye_l_socket_shadow",
        type: "ellipse",
        parent: "head_group",
        x: -60,
        y: 0,
        width: 76,
        height: 76,
        fill: {
          gradient: {
            type: "radial",
            stops: [
              { color: "#44503C28", position: 0 },
              { color: "#22503C28", position: 0.65 },
              { color: "#00503C28", position: 1.0 }
            ]
          }
        }
      },
      {
        id: "eye_r_socket_shadow",
        type: "ellipse",
        parent: "head_group",
        x: +60,
        y: 0,
        width: 76,
        height: 76,
        fill: {
          gradient: {
            type: "radial",
            stops: [
              { color: "#44503C28", position: 0 },
              { color: "#22503C28", position: 0.65 },
              { color: "#00503C28", position: 1.0 }
            ]
          }
        }
      },
      // 09 Left Eye
      {
        id: "eye_l_rim",
        type: "ellipse",
        parent: "eye_l_group",
        x: 0,
        y: 0,
        width: 58,
        height: 58,
        fill: { color: "#301A0B" }
      },
      {
        id: "eye_l_iris",
        type: "ellipse",
        parent: "eye_l_group",
        x: 0,
        y: 0,
        width: 54,
        height: 54,
        fill: {
          gradient: {
            type: "radial",
            start: { x: -6, y: 6 },
            end: { x: 22, y: -22 },
            stops: [
              { color: "#FBBF24", position: 0 },
              { color: "#D97706", position: 0.4 },
              { color: "#92400E", position: 0.75 },
              { color: "#451A03", position: 1.0 }
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
        width: 28,
        height: 28,
        fill: { color: "#1C0A02" }
      },
      {
        id: "eye_l_glint_primary",
        type: "ellipse",
        parent: "eye_l_group",
        x: -9,
        y: -9,
        width: 11,
        height: 11,
        fill: { color: "#FFFFFF" }
      },
      {
        id: "eye_l_glint_secondary",
        type: "ellipse",
        parent: "eye_l_group",
        x: 8,
        y: 8,
        width: 5,
        height: 5,
        fill: { color: "#CCFFFFFF" }
      },
      // 10 Left Eyelid Hood
      {
        id: "eye_l_eyelid",
        type: "polygon",
        parent: "eyelid_l_group",
        x: 0,
        y: 0,
        points: leftEyelidPoints,
        fill: {
          gradient: {
            type: "linear",
            start: { x: 0, y: -28 },
            end: { x: 0, y: 6 },
            stops: [
              { color: "#FFFDF9", position: 0 },
              { color: "#F4ECE1", position: 0.5 },
              { color: "#D8C7B4", position: 0.85 },
              { color: "#78624E", position: 1.0 }
            ]
          }
        }
      },
      // 11 Right Eye
      {
        id: "eye_r_rim",
        type: "ellipse",
        parent: "eye_r_group",
        x: 0,
        y: 0,
        width: 58,
        height: 58,
        fill: { color: "#301A0B" }
      },
      {
        id: "eye_r_iris",
        type: "ellipse",
        parent: "eye_r_group",
        x: 0,
        y: 0,
        width: 54,
        height: 54,
        fill: {
          gradient: {
            type: "radial",
            start: { x: -6, y: 6 },
            end: { x: 22, y: -22 },
            stops: [
              { color: "#FBBF24", position: 0 },
              { color: "#D97706", position: 0.4 },
              { color: "#92400E", position: 0.75 },
              { color: "#451A03", position: 1.0 }
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
        width: 28,
        height: 28,
        fill: { color: "#1C0A02" }
      },
      {
        id: "eye_r_glint_primary",
        type: "ellipse",
        parent: "eye_r_group",
        x: -9,
        y: -9,
        width: 11,
        height: 11,
        fill: { color: "#FFFFFF" }
      },
      {
        id: "eye_r_glint_secondary",
        type: "ellipse",
        parent: "eye_r_group",
        x: 8,
        y: 8,
        width: 5,
        height: 5,
        fill: { color: "#CCFFFFFF" }
      },
      // 12 Right Eyelid Hood
      {
        id: "eye_r_eyelid",
        type: "polygon",
        parent: "eyelid_r_group",
        x: 0,
        y: 0,
        points: rightEyelidPoints,
        fill: {
          gradient: {
            type: "linear",
            start: { x: 0, y: -28 },
            end: { x: 0, y: 6 },
            stops: [
              { color: "#FFFDF9", position: 0 },
              { color: "#F4ECE1", position: 0.5 },
              { color: "#D8C7B4", position: 0.85 },
              { color: "#78624E", position: 1.0 }
            ]
          }
        }
      },
      // 13 Soft Beak Cast Shadow
      {
        id: "beak_shadow",
        type: "ellipse",
        parent: "head_group",
        x: 0,
        y: 52,
        width: 22,
        height: 10,
        fill: {
          gradient: {
            type: "radial",
            stops: [
              { color: "#553A2A1E", position: 0 },
              { color: "#003A2A1E", position: 1.0 }
            ]
          }
        }
      },
      // 14 Beak
      {
        id: "beak",
        type: "polygon",
        parent: "head_group",
        x: 0,
        y: 28,
        points: beakPoints,
        fill: {
          gradient: {
            type: "linear",
            start: { x: -6, y: -22 },
            end: { x: 6, y: 24 },
            stops: [
              { color: "#FFFDF9", position: 0 },
              { color: "#EFE5D6", position: 0.45 },
              { color: "#CBB9A5", position: 0.8 },
              { color: "#927F6C", position: 1.0 }
            ]
          }
        }
      }
    ],
    animations: [
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
              { frame: 30, value: 1.022, easing: "ease-in-out" },
              { frame: 60, value: 1.0, easing: "ease-in-out" },
              { frame: 90, value: 0.985, easing: "ease-in-out" },
              { frame: 120, value: 1.0, easing: "ease-in-out" }
            ]
          },
          {
            target: "body_group",
            property: "scaleX",
            keyframes: [
              { frame: 0, value: 1.0 },
              { frame: 30, value: 0.988, easing: "ease-in-out" },
              { frame: 60, value: 1.0, easing: "ease-in-out" },
              { frame: 90, value: 1.012, easing: "ease-in-out" },
              { frame: 120, value: 1.0, easing: "ease-in-out" }
            ]
          },
          {
            target: "body_group",
            property: "rotation",
            keyframes: [
              { frame: 0, value: 0 },
              { frame: 30, value: 1.2, easing: "ease-in-out" },
              { frame: 60, value: 0, easing: "ease-in-out" },
              { frame: 90, value: -1.2, easing: "ease-in-out" },
              { frame: 120, value: 0, easing: "ease-in-out" }
            ]
          },
          {
            target: "wing_l_group",
            property: "rotation",
            keyframes: [
              { frame: 0, value: 0 },
              { frame: 35, value: -2.2, easing: "ease-in-out" },
              { frame: 65, value: 0, easing: "ease-in-out" },
              { frame: 95, value: 2.2, easing: "ease-in-out" },
              { frame: 120, value: 0, easing: "ease-in-out" }
            ]
          },
          {
            target: "wing_r_group",
            property: "rotation",
            keyframes: [
              { frame: 0, value: 0 },
              { frame: 35, value: 2.2, easing: "ease-in-out" },
              { frame: 65, value: 0, easing: "ease-in-out" },
              { frame: 95, value: -2.2, easing: "ease-in-out" },
              { frame: 120, value: 0, easing: "ease-in-out" }
            ]
          },
          {
            target: "eyelid_l_group",
            property: "y",
            keyframes: [
              { frame: 0, value: 0 },
              { frame: 68, value: 0 },
              { frame: 73, value: 20, easing: "ease-in-out" },
              { frame: 77, value: 20, easing: "ease-in-out" },
              { frame: 82, value: 0, easing: "ease-in-out" },
              { frame: 120, value: 0 }
            ]
          },
          {
            target: "eyelid_l_group",
            property: "scaleY",
            keyframes: [
              { frame: 0, value: 1.0 },
              { frame: 68, value: 1.0 },
              { frame: 73, value: 1.25, easing: "ease-in-out" },
              { frame: 77, value: 1.25, easing: "ease-in-out" },
              { frame: 82, value: 1.0, easing: "ease-in-out" },
              { frame: 120, value: 1.0 }
            ]
          },
          {
            target: "eyelid_r_group",
            property: "y",
            keyframes: [
              { frame: 0, value: 0 },
              { frame: 68, value: 0 },
              { frame: 73, value: 20, easing: "ease-in-out" },
              { frame: 77, value: 20, easing: "ease-in-out" },
              { frame: 82, value: 0, easing: "ease-in-out" },
              { frame: 120, value: 0 }
            ]
          },
          {
            target: "eyelid_r_group",
            property: "scaleY",
            keyframes: [
              { frame: 0, value: 1.0 },
              { frame: 68, value: 1.0 },
              { frame: 73, value: 1.25, easing: "ease-in-out" },
              { frame: 77, value: 1.25, easing: "ease-in-out" },
              { frame: 82, value: 1.0, easing: "ease-in-out" },
              { frame: 120, value: 1.0 }
            ]
          },
          {
            target: "ground_shadow",
            property: "scaleX",
            keyframes: [
              { frame: 0, value: 1.0 },
              { frame: 30, value: 0.98, easing: "ease-in-out" },
              { frame: 60, value: 1.0, easing: "ease-in-out" },
              { frame: 90, value: 1.02, easing: "ease-in-out" },
              { frame: 120, value: 1.0, easing: "ease-in-out" }
            ]
          }
        ]
      },
      {
        name: "blink",
        fps: 60,
        duration: 20,
        loop: "oneShot",
        tracks: [
          {
            target: "eyelid_l_group",
            property: "y",
            keyframes: [
              { frame: 0, value: 0 },
              { frame: 6, value: 20, easing: "ease-out" },
              { frame: 11, value: 20 },
              { frame: 20, value: 0, easing: "ease-in-out" }
            ]
          },
          {
            target: "eyelid_l_group",
            property: "scaleY",
            keyframes: [
              { frame: 0, value: 1.0 },
              { frame: 6, value: 1.25, easing: "ease-out" },
              { frame: 11, value: 1.25 },
              { frame: 20, value: 1.0, easing: "ease-in-out" }
            ]
          },
          {
            target: "eyelid_r_group",
            property: "y",
            keyframes: [
              { frame: 0, value: 0 },
              { frame: 6, value: 20, easing: "ease-out" },
              { frame: 11, value: 20 },
              { frame: 20, value: 0, easing: "ease-in-out" }
            ]
          },
          {
            target: "eyelid_r_group",
            property: "scaleY",
            keyframes: [
              { frame: 0, value: 1.0 },
              { frame: 6, value: 1.25, easing: "ease-out" },
              { frame: 11, value: 1.25 },
              { frame: 20, value: 1.0, easing: "ease-in-out" }
            ]
          }
        ]
      }
    ],
    stateMachine: {
      name: "Owluko_SM",
      inputs: [
        { name: "isBreathing", type: "bool", initial: true },
        { name: "triggerBlink", type: "trigger" }
      ],
      states: [
        { name: "idle_state", animation: "idle" },
        { name: "blink_state", animation: "blink" }
      ],
      transitions: [
        { from: "entry", to: "idle_state" },
        { from: "idle_state", to: "blink_state", condition: { input: "triggerBlink" } },
        { from: "blink_state", to: "idle_state", exitTimeMs: 330 }
      ]
    }
  };

  const outRivPath = "mascots/owluko/owluko_pure_vector.riv";
  console.log("Compiling native vector scene to: " + outRivPath + "...");
  const createRes = await callMcpTool("riv_create", {
    outPath: outRivPath,
    scene: scene
  });

  if (createRes.isError) {
    console.error("FAILED to compile Rive file:", JSON.stringify(createRes, null, 2));
    process.exit(1);
  }

  const stat = fs.statSync(outRivPath);
  console.log("SUCCESS! Pure Vector .riv compiled: " + stat.size + " bytes (" + (stat.size / 1024).toFixed(1) + " KB)");

  console.log("\nInspecting .riv file via riv_inspect...");
  const inspectRes = await callMcpTool("riv_inspect", { path: outRivPath });
  console.log(inspectRes.content?.[0]?.text || "Inspection ok");

  console.log("\nRunning riv_lint...");
  const lintRes = await callMcpTool("riv_lint", { path: outRivPath });
  console.log(lintRes.content?.[0]?.text || "Lint ok");

  console.log("\nRendering preview frames...");
  const frame0Path = "mascots/owluko/owluko_pure_vector_frame0.png";
  await callMcpTool("riv_render_frame", {
    path: outRivPath,
    outPath: frame0Path,
    time: 0.4
  });
  console.log("Rendered frame 0 to " + frame0Path);

  const frameBlinkPath = "mascots/owluko/owluko_pure_vector_blink.png";
  await callMcpTool("riv_render_frame", {
    path: outRivPath,
    outPath: frameBlinkPath,
    time: 1.25
  });
  console.log("Rendered blink frame to " + frameBlinkPath);

  console.log("\nRendering animated GIF preview...");
  const gifPath = "mascots/owluko/owluko_pure_vector.gif";
  await callMcpTool("riv_render_gif", {
    path: outRivPath,
    outPath: gifPath,
    fps: 30,
    duration: 2.0
  });
  console.log("Rendered GIF to " + gifPath);
}

buildOwlukoPureVectorRive().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
