const { callMcpTool } = require("./rive_mcp_client.js");
const fs = require("fs");

async function buildMasterRive() {
  console.log("Building Owluko Master Rive scene via Rive MCP...");

  // Relative to pelvis group at (256, 435):
  // Center of 512x512 canvas is at (256, 256), so offset is (0, -179)
  // Left shoulder pivot is at (128, 192), offset from pelvis is (-128, -243)
  // Right shoulder pivot is at (384, 192), offset from pelvis is (+128, -243)

  const scene = {
    artboard: { name: "Owluko", width: 512, height: 512 },
    backgroundColor: "#18181b",
    groups: [
      // Root anchor at ground level [256, 489]
      { id: "root", x: 256, y: 489 },
      // Pelvis anchor at [256, 435] (offset from root: y = -54)
      { id: "body_group", parent: "root", x: 0, y: -54 },
      // Left shoulder group at [128, 192] (offset from pelvis: x = -128, y = -243)
      { id: "wing_l_group", parent: "body_group", x: -128, y: -243 },
      // Right shoulder group at [384, 192] (offset from pelvis: x = 128, y = -243)
      { id: "wing_r_group", parent: "body_group", x: 128, y: -243 },
      // Closed eyes overlay group parented to body
      { id: "eyes_group", parent: "body_group", x: 0, y: -179 }
    ],
    images: [
      // 00 Shadow at ground plane
      { id: "shadow", pngPath: "mascots/owluko/rig_layers/00_shadow.png", parent: "root", x: 0, y: 0 },
      // 01 & 02 Feet stationary on ground (emerging from under belly)
      { id: "foot_l", pngPath: "mascots/owluko/rig_layers/01_foot_left.png", parent: "root", x: 0, y: -233 },
      { id: "foot_r", pngPath: "mascots/owluko/rig_layers/02_foot_right.png", parent: "root", x: 0, y: -233 },
      // 03 Porcelain continuous egg body (flawless, no green, no cut seams)
      { id: "body", pngPath: "mascots/owluko/rig_layers/03_body_porcelain.png", parent: "body_group", x: 0, y: -179 },
      // 04 & 05 Wings parented to shoulder pivots
      { id: "wing_l", pngPath: "mascots/owluko/rig_layers/04_wing_left.png", parent: "wing_l_group", x: 128, y: 64 },
      { id: "wing_r", pngPath: "mascots/owluko/rig_layers/05_wing_right.png", parent: "wing_r_group", x: -128, y: 64 },
      // 06 Closed eyes overlay for realistic eyelid blink
      { id: "closed_eyes", pngPath: "mascots/owluko/rig_layers/08_closed_eyes_aligned.png", parent: "eyes_group", x: 0, y: 0, opacity: 0 }
    ],
    animations: [
      {
        name: "idle",
        fps: 60,
        duration: 120, // 2.0s loop
        loop: "loop",
        tracks: [
          // Body organic respiration (Squash & Stretch)
          {
            target: "body_group",
            property: "scaleY",
            keyframes: [
              { frame: 0, value: 1.0 },
              { frame: 30, value: 1.018, easing: "ease-in-out" },
              { frame: 60, value: 1.0, easing: "ease-in-out" },
              { frame: 90, value: 0.986, easing: "ease-in-out" },
              { frame: 120, value: 1.0, easing: "ease-in-out" }
            ]
          },
          {
            target: "body_group",
            property: "scaleX",
            keyframes: [
              { frame: 0, value: 1.0 },
              { frame: 30, value: 0.991, easing: "ease-in-out" },
              { frame: 60, value: 1.0, easing: "ease-in-out" },
              { frame: 90, value: 1.008, easing: "ease-in-out" },
              { frame: 120, value: 1.0, easing: "ease-in-out" }
            ]
          },
          // Subtle head / torso tilt
          {
            target: "body_group",
            property: "rotation",
            keyframes: [
              { frame: 0, value: 0 },
              { frame: 30, value: 1.5, easing: "ease-in-out" },
              { frame: 60, value: 0, easing: "ease-in-out" },
              { frame: 90, value: -1.5, easing: "ease-in-out" },
              { frame: 120, value: 0, easing: "ease-in-out" }
            ]
          },
          // Left wing secondary harmonic hover
          {
            target: "wing_l_group",
            property: "rotation",
            keyframes: [
              { frame: 0, value: 0 },
              { frame: 35, value: -2.4, easing: "ease-in-out" },
              { frame: 65, value: 0, easing: "ease-in-out" },
              { frame: 95, value: 2.4, easing: "ease-in-out" },
              { frame: 120, value: 0, easing: "ease-in-out" }
            ]
          },
          // Right wing secondary harmonic hover
          {
            target: "wing_r_group",
            property: "rotation",
            keyframes: [
              { frame: 0, value: 0 },
              { frame: 35, value: 2.4, easing: "ease-in-out" },
              { frame: 65, value: 0, easing: "ease-in-out" },
              { frame: 95, value: -2.4, easing: "ease-in-out" },
              { frame: 120, value: 0, easing: "ease-in-out" }
            ]
          },
          // Periodic blink at frame 70..80
          {
            target: "closed_eyes",
            property: "opacity",
            keyframes: [
              { frame: 0, value: 0 },
              { frame: 68, value: 0 },
              { frame: 72, value: 1.0, easing: "ease-in-out" },
              { frame: 78, value: 1.0, easing: "ease-in-out" },
              { frame: 82, value: 0, easing: "ease-in-out" },
              { frame: 120, value: 0 }
            ]
          },
          // Shadow expansion matching breathing squash
          {
            target: "shadow",
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
      // Standalone Blink Animation
      {
        name: "blink",
        fps: 60,
        duration: 24,
        loop: "oneShot",
        tracks: [
          {
            target: "closed_eyes",
            property: "opacity",
            keyframes: [
              { frame: 0, value: 0 },
              { frame: 5, value: 1.0, easing: "ease-in-out" },
              { frame: 18, value: 1.0, easing: "ease-in-out" },
              { frame: 24, value: 0, easing: "ease-in-out" }
            ]
          }
        ]
      }
    ],
    stateMachine: {
      name: "Owluko_SM",
      inputs: [
        { name: "triggerBlink", type: "trigger" },
        { name: "isBreathing", type: "bool", default: true }
      ],
      states: [
        { name: "Idle_Breathing", animation: "idle" },
        { name: "Triggered_Blink", animation: "blink" }
      ],
      transitions: [
        { from: "entry", to: "Idle_Breathing" },
        { from: "Idle_Breathing", to: "Triggered_Blink", condition: { input: "triggerBlink" } },
        { from: "Triggered_Blink", to: "Idle_Breathing", exitTimeMs: 400 }
      ]
    }
  };

  const outPath = "mascots/owluko/owluko_mcp_master.riv";
  console.log("Calling riv_create to compile binary .riv...");
  const res = await callMcpTool("riv_create", { outPath, scene });
  console.log("riv_create result:", res.content ? res.content[0].text : res);

  console.log("Inspecting compiled .riv via riv_inspect...");
  const inspectRes = await callMcpTool("riv_inspect", { path: outPath });
  console.log("riv_inspect:", inspectRes.content[0].text);

  console.log("Rendering 60fps animated preview GIF via riv_render_gif...");
  const gifRes = await callMcpTool("riv_render_gif", {
    path: outPath,
    animation: "idle",
    fps: 30,
    out: "mascots/owluko/owluko_mcp_master.gif"
  });
  console.log("riv_render_gif:", gifRes.content[0].text);

  console.log("Rendering transparent APNG via riv_render_apng...");
  const apngRes = await callMcpTool("riv_render_apng", {
    path: outPath,
    animation: "idle",
    fps: 30,
    background: "transparent",
    out: "mascots/owluko/owluko_mcp_master.png"
  });
  console.log("riv_render_apng:", apngRes.content[0].text);

  console.log("All Rive MCP assets compiled successfully!");
}

buildMasterRive().catch(console.error);
