const path = require("path");
const fs = require("fs");
const { callMcpTool } = require("./rive_mcp_client.js");

async function testCompile() {
  const scene = {
    artboard: { name: "Owluko_HiFi", width: 1024, height: 1024 },
    backgroundColor: "#FFFFFF",
    groups: [
      { id: "root", x: 512, y: 876 },
      { id: "feet_group", parent: "root", x: 0, y: 0 },
      { id: "body_group", parent: "root", x: 0, y: -378 },
      { id: "head_group", parent: "body_group", x: 0, y: -126 },
      { id: "eye_l_group", parent: "head_group", x: -114, y: -10 },
      { id: "eye_r_group", parent: "head_group", x: 114, y: -10 },
      { id: "beak_group", parent: "head_group", x: 0, y: 44 }
    ],
    images: [
      {
        id: "body_img",
        pngPath: "mascots/owluko/components/hifi/base_body.png",
        x: 0,
        y: -25,
        parent: "body_group",
        scale: 1.0,
        z: 50
      },
      {
        id: "eye_l_img",
        pngPath: "mascots/owluko/components/hifi/eye_left.png",
        x: 0,
        y: 0,
        parent: "eye_l_group",
        scale: 1.0,
        z: 90
      },
      {
        id: "eye_r_img",
        pngPath: "mascots/owluko/components/hifi/eye_right.png",
        x: 0,
        y: 0,
        parent: "eye_r_group",
        scale: 1.0,
        z: 90
      },
      {
        id: "beak_img",
        pngPath: "mascots/owluko/components/hifi/beak.png",
        x: 0,
        y: 0,
        parent: "beak_group",
        scale: 1.0,
        z: 100
      },
      {
        id: "feet_img",
        pngPath: "mascots/owluko/components/hifi/feet.png",
        x: 0,
        y: -10,
        parent: "feet_group",
        scale: 1.0,
        z: 20
      }
    ],
    animations: [
      {
        name: "idle",
        fps: 60,
        duration: 60,
        loop: "loop",
        tracks: [
          {
            target: "body_group",
            property: "scaleY",
            keyframes: [
              { frame: 0, value: 1.0 },
              { frame: 30, value: 1.02, easing: "ease-in-out" },
              { frame: 60, value: 1.0, easing: "ease-in-out" }
            ]
          }
        ]
      }
    ]
  };

  const outPath = path.resolve(__dirname, "../mascots/owluko/test_hifi.riv");
  console.log("Compiling test Hi-Fi Rive to", outPath);
  const res = await callMcpTool("riv_create", {
    outPath: outPath,
    scene: scene
  });
  console.log("Result:", JSON.stringify(res, null, 2));

  if (fs.existsSync(outPath)) {
    const stat = fs.statSync(outPath);
    console.log(`Success! File size: ${stat.size} bytes (${(stat.size / 1024).toFixed(1)} KB)`);

    // Render frame 0
    const frame0 = path.resolve(__dirname, "../mascots/owluko/test_hifi_frame0.png");
    await callMcpTool("riv_render_frame", {
      path: outPath,
      outPath: frame0,
      animation: "idle",
      time: 0.0,
      background: "#FFFFFF"
    });
    console.log("Rendered frame 0 to", frame0);
  }
}

testCompile().catch(console.error);
