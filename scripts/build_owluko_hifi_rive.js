const path = require("path");
const fs = require("fs");
const { callMcpTool } = require("./rive_mcp_client.js");

async function buildHiFiRive() {
  console.log("===================================================================");
  console.log("  BUILDING OPTION A: OWLUKO HI-FI RIVE RIG (COMPONENT SHEET 3D)   ");
  console.log("===================================================================");

  const groups = [
    { id: "root", x: 512, y: 876 },
    { id: "shadow_group", parent: "root", x: 0, y: 0 },
    { id: "feet_group", parent: "root", x: 0, y: -24 },
    { id: "body_group", parent: "root", x: 0, y: -380 },
    { id: "wings_group", parent: "body_group", x: 0, y: 0 },
    { id: "wing_l_group", parent: "wings_group", x: -250, y: 30 },
    { id: "wing_r_rest_group", parent: "wings_group", x: 250, y: 30 },
    { id: "wing_r_wave_group", parent: "wings_group", x: 230, y: -40 }, // pivot at shoulder
    { id: "head_group", parent: "body_group", x: 0, y: -126 },
    { id: "eye_l_group", parent: "head_group", x: -114, y: -10 },
    { id: "eye_r_group", parent: "head_group", x: 114, y: -10 },
    { id: "beak_group", parent: "head_group", x: 0, y: 44 }
  ];

  const images = [
    // 1. Base Body (Panel 2)
    {
      id: "body_base_img",
      pngPath: "mascots/owluko/components/hifi/base_body.png",
      x: 0,
      y: -20,
      parent: "body_group",
      scale: 1.0,
      z: 50
    },
    // 2. Left Wing (tucked at flank)
    {
      id: "wing_left_img",
      pngPath: "mascots/owluko/components/hifi/wing.png",
      x: 0,
      y: 0,
      parent: "wing_l_group",
      scaleX: -0.9,
      scaleY: 0.9,
      rotation: -30,
      z: 30
    },
    // 3. Right Resting Wing
    {
      id: "wing_right_rest_img",
      pngPath: "mascots/owluko/components/hifi/wing.png",
      x: 0,
      y: 0,
      parent: "wing_r_rest_group",
      scaleX: 0.9,
      scaleY: 0.9,
      rotation: 30,
      z: 70
    },
    // 4. Right Waving Wing
    {
      id: "wing_right_wave_img",
      pngPath: "mascots/owluko/components/hifi/wing.png",
      x: 30,
      y: -30,
      parent: "wing_r_wave_group",
      scaleX: 1.05,
      scaleY: 1.05,
      rotation: 15,
      opacity: 0,
      z: 40
    },
    // 5. Left Eye
    {
      id: "eye_left_img",
      pngPath: "mascots/owluko/components/hifi/eye_left.png",
      x: 0,
      y: 0,
      parent: "eye_l_group",
      scale: 1.0,
      z: 90
    },
    // 6. Right Eye
    {
      id: "eye_right_img",
      pngPath: "mascots/owluko/components/hifi/eye_right.png",
      x: 0,
      y: 0,
      parent: "eye_r_group",
      scale: 1.0,
      z: 90
    },
    // 7. Beak
    {
      id: "beak_img",
      pngPath: "mascots/owluko/components/hifi/beak.png",
      x: 0,
      y: 0,
      parent: "beak_group",
      scale: 1.0,
      z: 100
    },
    // 8. Feet
    {
      id: "feet_img",
      pngPath: "mascots/owluko/components/hifi/feet.png",
      x: 0,
      y: 0,
      parent: "feet_group",
      scale: 1.0,
      z: 20
    }
  ];

  // Ground shadow vector shape
  const shapes = [
    {
      id: "ground_shadow",
      type: "ellipse",
      parent: "shadow_group",
      x: 0,
      y: 0,
      width: 440,
      height: 60,
      fill: { color: "#C8B29E", opacity: 0.35 },
      z: 10
    }
  ];

  // Animations
  const animations = [
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
            { frame: 60, value: 1.02, easing: "ease-in-out" },
            { frame: 120, value: 1.0, easing: "ease-in-out" }
          ]
        },
        {
          target: "wing_l_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0.0 },
            { frame: 60, value: -2.0, easing: "ease-in-out" },
            { frame: 120, value: 0.0, easing: "ease-in-out" }
          ]
        },
        {
          target: "wing_r_rest_group",
          property: "rotation",
          keyframes: [
            { frame: 0, value: 0.0 },
            { frame: 60, value: 2.0, easing: "ease-in-out" },
            { frame: 120, value: 0.0, easing: "ease-in-out" }
          ]
        }
      ]
    },
    {
      name: "waving",
      fps: 60,
      duration: 240,
      loop: "one-shot",
      tracks: [
        {
          target: "wing_right_rest_img",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 1 },
            { frame: 30, value: 1 },
            { frame: 45, value: 0, easing: "ease-out" },
            { frame: 205, value: 0 },
            { frame: 222, value: 1, easing: "ease-in" },
            { frame: 240, value: 1 }
          ]
        },
        {
          target: "wing_right_wave_img",
          property: "opacity",
          keyframes: [
            { frame: 0, value: 0 },
            { frame: 30, value: 0 },
            { frame: 45, value: 1, easing: "ease-in" },
            { frame: 205, value: 1 },
            { frame: 222, value: 0, easing: "ease-out" },
            { frame: 240, value: 0 }
          ]
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
        }
      ]
    }
  ];

  const stateMachine = {
    name: "SM_Owluko_HiFi",
    inputs: [
      { name: "triggerWave", type: "trigger" }
    ],
    states: [
      { name: "Idle", animation: "idle" },
      { name: "Waving", animation: "waving" }
    ],
    transitions: [
      { from: "entry", to: "Idle" },
      { from: "Idle", to: "Waving", condition: { input: "triggerWave" } },
      { from: "Waving", to: "Idle", exitTimeMs: 4000 }
    ]
  };

  const scene = {
    artboard: { name: "Owluko_HiFi", width: 1024, height: 1024 },
    backgroundColor: "#FFFFFF",
    groups,
    images,
    shapes,
    animations,
    stateMachine
  };

  const scenePath = path.resolve(__dirname, "../mascots/owluko/owluko_hifi.scene.json");
  fs.writeFileSync(scenePath, JSON.stringify(scene, null, 2));

  const outRiv = path.resolve(__dirname, "../mascots/owluko/owluko_hifi.riv");
  console.log("Compiling Hi-Fi .riv to", outRiv);
  await callMcpTool("riv_create", {
    outPath: outRiv,
    scene: scene
  });

  const stat = fs.statSync(outRiv);
  console.log(`Compiled Hi-Fi .riv: ${stat.size} bytes (${(stat.size / 1024).toFixed(1)} KB)`);

  // Render Frame 0
  const f0 = path.resolve(__dirname, "../mascots/owluko/owluko_hifi_frame0.png");
  await callMcpTool("riv_render_frame", {
    path: outRiv,
    outPath: f0,
    animation: "idle",
    time: 0.0,
    background: "#FFFFFF"
  });
  console.log("Rendered Hi-Fi Frame 0 to", f0);

  // Render Waving Frame
  const fWave = path.resolve(__dirname, "../mascots/owluko/owluko_hifi_wave_frame.png");
  await callMcpTool("riv_render_frame", {
    path: outRiv,
    outPath: fWave,
    animation: "waving",
    time: 1.42,
    background: "#FFFFFF"
  });
  console.log("Rendered Hi-Fi Waving Frame to", fWave);
}

buildHiFiRive().catch(console.error);
