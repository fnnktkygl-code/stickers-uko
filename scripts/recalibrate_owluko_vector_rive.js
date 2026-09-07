const fs = require("fs");
const path = require("path");
const { callMcpTool } = require("./rive_mcp_client.js");

const kappa = 0.5522847498307936;

async function run() {
  console.log("=== Recalibrating Owluko Vector Scene from Reference Calque ===");

  const groups = [
    { id: "root", x: 256, y: 472 },
    { id: "feet_group", parent: "root", x: 0, y: 0 },
    { id: "foot_l_group", parent: "feet_group", x: -56, y: 0 },
    { id: "foot_r_group", parent: "feet_group", x: 54, y: 0 },
    { id: "body_group", parent: "root", x: 0, y: -184 },
    { id: "wing_l_group", parent: "body_group", x: -140, y: 32 },
    { id: "wing_r_group", parent: "body_group", x: 140, y: 32 },
    { id: "head_group", parent: "body_group", x: 0, y: -82 },
    { id: "eye_l_group", parent: "head_group", x: -57, y: 0 },
    { id: "eye_r_group", parent: "head_group", x: 55, y: 0 },
    { id: "eyelid_l_group", parent: "eye_l_group", x: 0, y: 0 },
    { id: "eyelid_r_group", parent: "eye_r_group", x: 0, y: 0 }
  ];

  // Plump, chubby ball body (rx=168, ry=174)
  const rx_b = 168;
  const ry_b = 174;
  const bodyPoints = [
    {
      x: 0,
      y: -ry_b,
      cubic: {
        inRotation: 180,
        inDistance: rx_b * kappa,
        rotation: 0,
        outDistance: rx_b * kappa
      }
    },
    {
      x: rx_b,
      y: 10,
      cubic: {
        inRotation: 270,
        inDistance: ry_b * kappa,
        rotation: 90,
        outDistance: ry_b * kappa
      }
    },
    {
      x: 0,
      y: ry_b,
      cubic: {
        inRotation: 0,
        inDistance: rx_b * kappa,
        rotation: 180,
        outDistance: rx_b * kappa
      }
    },
    {
      x: -rx_b,
      y: 10,
      cubic: {
        inRotation: 90,
        inDistance: ry_b * kappa,
        rotation: 270,
        outDistance: ry_b * kappa
      }
    }
  ];

  // Facial Disk: Flawless smooth spectacle/heart contour around eyes
  const facialDiskPoints = [
    {
      x: 0,
      y: -30,
      cubic: {
        inRotation: 145,
        inDistance: 20,
        rotation: 35,
        outDistance: 20
      }
    },
    {
      x: 56,
      y: -64,
      cubic: {
        inRotation: 180,
        inDistance: 24,
        rotation: 0,
        outDistance: 24
      }
    },
    {
      x: 118,
      y: 6,
      cubic: {
        inRotation: 270,
        inDistance: 34,
        rotation: 90,
        outDistance: 34
      }
    },
    {
      x: 0,
      y: 62,
      cubic: {
        inRotation: 0,
        inDistance: 40,
        rotation: 180,
        outDistance: 40
      }
    },
    {
      x: -118,
      y: 6,
      cubic: {
        inRotation: 90,
        inDistance: 34,
        rotation: 270,
        outDistance: 34
      }
    },
    {
      x: -56,
      y: -64,
      cubic: {
        inRotation: 180,
        inDistance: 24,
        rotation: 0,
        outDistance: 24
      }
    }
  ];

  const leftWingPoints = [
    {
      x: 0,
      y: 0,
      cubic: { inRotation: 180, inDistance: 12, rotation: 0, outDistance: 12 }
    },
    {
      x: -26,
      y: 45,
      cubic: { inRotation: 270, inDistance: 30, rotation: 90, outDistance: 30 }
    },
    { x: -12, y: 92, radius: 12 },
    { x: 4, y: 95, radius: 10 },
    {
      x: 18,
      y: 50,
      cubic: { inRotation: 85, inDistance: 32, rotation: 265, outDistance: 32 }
    }
  ];

  const rightWingPoints = [
    {
      x: 0,
      y: 0,
      cubic: { inRotation: 0, inDistance: 12, rotation: 180, outDistance: 12 }
    },
    {
      x: 26,
      y: 45,
      cubic: { inRotation: 270, inDistance: 30, rotation: 90, outDistance: 30 }
    },
    { x: 12, y: 92, radius: 12 },
    { x: -4, y: 95, radius: 10 },
    {
      x: -18,
      y: 50,
      cubic: { inRotation: 95, inDistance: 32, rotation: 275, outDistance: 32 }
    }
  ];

  const beakPoints = [
    {
      x: 0,
      y: -15,
      cubic: { inRotation: 180, inDistance: 12, rotation: 0, outDistance: 12 }
    },
    {
      x: 15,
      y: -5,
      cubic: { inRotation: 270, inDistance: 7, rotation: 90, outDistance: 10 }
    },
    { x: 0, y: 18, radius: 4 },
    {
      x: -15,
      y: -5,
      cubic: { inRotation: 90, inDistance: 10, rotation: 270, outDistance: 7 }
    }
  ];

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

  // Smooth circular dome eyelid matching eye socket
  const eyelidLPoints = [
    {
      x: -36,
      y: 0,
      cubic: { inRotation: 90, inDistance: 36 * kappa, rotation: 270, outDistance: 36 * kappa }
    },
    {
      x: 0,
      y: -36,
      cubic: { inRotation: 180, inDistance: 36 * kappa, rotation: 0, outDistance: 36 * kappa }
    },
    {
      x: 36,
      y: 0,
      cubic: { inRotation: 270, inDistance: 36 * kappa, rotation: 90, outDistance: 36 * kappa }
    },
    {
      x: 0,
      y: 20,
      cubic: { inRotation: 0, inDistance: 24, rotation: 180, outDistance: 24 }
    }
  ];

  const eyelidRPoints = [
    {
      x: -36,
      y: 0,
      cubic: { inRotation: 90, inDistance: 36 * kappa, rotation: 270, outDistance: 36 * kappa }
    },
    {
      x: 0,
      y: -36,
      cubic: { inRotation: 180, inDistance: 36 * kappa, rotation: 0, outDistance: 36 * kappa }
    },
    {
      x: 36,
      y: 0,
      cubic: { inRotation: 270, inDistance: 36 * kappa, rotation: 90, outDistance: 36 * kappa }
    },
    {
      x: 0,
      y: 20,
      cubic: { inRotation: 0, inDistance: 24, rotation: 180, outDistance: 24 }
    }
  ];

  const shapes = [
    {
      id: "ground_shadow",
      type: "ellipse",
      parent: "root",
      x: 0,
      y: 0,
      width: 290,
      height: 40,
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
          start: { x: 15, y: 0 },
          end: { x: -25, y: 95 },
          stops: [
            { color: "#FAF5E5", position: 0 },
            { color: "#EDE2CF", position: 0.4 },
            { color: "#DFCDB5", position: 0.8 },
            { color: "#BEAC94", position: 1 }
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
          start: { x: -15, y: 0 },
          end: { x: 25, y: 95 },
          stops: [
            { color: "#FAF5E5", position: 0 },
            { color: "#EDE2CF", position: 0.4 },
            { color: "#DFCDB5", position: 0.8 },
            { color: "#BEAC94", position: 1 }
          ]
        }
      }
    },
    {
      id: "body_sphere",
      type: "polygon",
      parent: "body_group",
      x: 0,
      y: 0,
      points: bodyPoints,
      fill: {
        gradient: {
          type: "linear",
          start: { x: -40, y: -174 },
          end: { x: 40, y: 174 },
          stops: [
            { color: "#FFFDF5", position: 0 },
            { color: "#F7EFE1", position: 0.25 },
            { color: "#EBDEC9", position: 0.6 },
            { color: "#D6C3A8", position: 0.85 },
            { color: "#B8A387", position: 1 }
          ]
        }
      }
    },
    {
      id: "fluffy_belly",
      type: "ellipse",
      parent: "body_group",
      x: 0,
      y: 65,
      width: 265,
      height: 195,
      fill: {
        gradient: {
          type: "radial",
          stops: [
            { color: "#FFFFFFFF", position: 0 },
            { color: "#FAF6ED", position: 0.6 },
            { color: "#EFE5D5", position: 0.85 },
            { color: "#DECDB5", position: 1 }
          ]
        }
      }
    },
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
            { color: "#FAF6EC", position: 0.65 },
            { color: "#EFE5D6", position: 0.88 },
            { color: "#DECDB5", position: 1 }
          ]
        }
      }
    },
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
            { color: "#2FED7855", position: 0 },
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
            { color: "#2FED7855", position: 0 },
            { color: "#00ED7855", position: 1 }
          ]
        }
      }
    },
    // Left Eye
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
      id: "eye_l_rim",
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
    // Right Eye
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
      id: "eye_r_rim",
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
    // Beak
    {
      id: "beak",
      type: "polygon",
      parent: "head_group",
      x: 0,
      y: 30,
      points: beakPoints,
      fill: {
        gradient: {
          type: "linear",
          start: { x: 0, y: -15 },
          end: { x: 0, y: 18 },
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
      parent: "head_group",
      x: 0,
      y: 22,
      width: 8,
      height: 5,
      fill: { color: "#FED7AA" }
    }
  ];

  const animations = [
    {
      name: "idle",
      fps: 60,
      duration: 120,
      loop: "loop",
      tracks: [
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
        {
          target: "wing_l_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0, easing: "ease-in-out" },
            { frame: 60, value: -1.8, easing: "ease-in-out" },
            { frame: 120, value: 0, easing: "ease-in-out" }
          ]
        },
        {
          target: "wing_r_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0, easing: "ease-in-out" },
            { frame: 60, value: 1.8, easing: "ease-in-out" },
            { frame: 120, value: 0, easing: "ease-in-out" }
          ]
        },
        {
          target: "ground_shadow",
          property: "scaleX",
          keyframes: [
            { frame: 0, value: 1.0, easing: "ease-in-out" },
            { frame: 60, value: 0.96, easing: "ease-in-out" },
            { frame: 120, value: 1.0, easing: "ease-in-out" }
          ]
        },
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

  console.log("=== ALL DELIVERABLES GENERATED SUCCESSFULLY ===");
}

run().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
