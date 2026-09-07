const { spawn } = require("child_process");

const proc = spawn("npx", ["-y", "rive-mcp-server"], {
  stdio: ["pipe", "pipe", "inherit"]
});

let buffer = "";
proc.stdout.on("data", (data) => {
  buffer += data.toString();
  const lines = buffer.split("\n");
  for (let i = 0; i < lines.length - 1; i++) {
    const line = lines[i].trim();
    if (!line) continue;
    try {
      const msg = JSON.parse(line);
      if (msg.id === 1) {
        const toolCall = JSON.stringify({
          jsonrpc: "2.0",
          id: 2,
          method: "tools/call",
          params: {
            name: "riv_studio",
            arguments: {
              path: "mascots/owluko/owluko_pure_vector.riv",
              scenePath: "mascots/owluko/owluko_pure_vector.scene.json",
              port: 8787
            }
          }
        }) + "\n";
        proc.stdin.write(toolCall);
      } else if (msg.id === 2) {
        console.log("Rive Studio started successfully! Running daemon...");
      }
    } catch (e) {}
  }
  buffer = lines[lines.length - 1];
});

const initReq = JSON.stringify({
  jsonrpc: "2.0",
  id: 1,
  method: "initialize",
  params: {
    protocolVersion: "2024-11-05",
    capabilities: {},
    clientInfo: { name: "rive-studio-daemon", version: "1.0.0" }
  }
}) + "\n";
proc.stdin.write(initReq);
