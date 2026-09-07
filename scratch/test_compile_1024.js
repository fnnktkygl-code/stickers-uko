const fs = require("fs");
const path = require("path");
const { callMcpTool } = require("../scripts/rive_mcp_client.js");

async function test() {
  const fragment = JSON.parse(fs.readFileSync("scratch/owluko_user_exact.scene.json", "utf8"));
  
  const scene = {
    artboard: {
      name: "Owluko_Canonical",
      width: 1024,
      height: 1024
    },
    backgroundColor: "#FFFFFF",
    shapes: fragment.shapes,
    animations: [
      {
        name: "idle",
        fps: 60,
        duration: 120,
        loop: "loop",
        tracks: []
      }
    ]
  };

  const outRiv = "scratch/test_1024.riv";
  await callMcpTool("riv_create", {
    outPath: path.resolve(outRiv),
    scene: scene
  });
  console.log("Compiled test_1024.riv successfully!");

  const outPng = "scratch/test_1024_frame.png";
  await callMcpTool("riv_render_frame", {
    path: path.resolve(outRiv),
    outPath: path.resolve(outPng),
    animation: "idle",
    time: 0,
    background: "#FFFFFF"
  });
  console.log("Rendered test_1024_frame.png successfully!");
}

test().catch(console.error);
