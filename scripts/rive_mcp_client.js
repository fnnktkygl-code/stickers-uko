const { spawn } = require("child_process");

function callMcpTool(toolName, args) {
  return new Promise((resolve, reject) => {
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
            // Handshake complete, send tool call
            const toolCall = JSON.stringify({
              jsonrpc: "2.0",
              id: 2,
              method: "tools/call",
              params: {
                name: toolName,
                arguments: args
              }
            }) + "\n";
            proc.stdin.write(toolCall);
          } else if (msg.id === 2) {
            proc.kill();
            if (msg.error) {
              reject(new Error(JSON.stringify(msg.error)));
            } else {
              resolve(msg.result);
            }
          }
        } catch (e) {
          // not JSON line
        }
      }
      buffer = lines[lines.length - 1];
    });

    proc.on("error", (err) => reject(err));

    // Send initialize
    const initReq = JSON.stringify({
      jsonrpc: "2.0",
      id: 1,
      method: "initialize",
      params: {
        protocolVersion: "2024-11-05",
        capabilities: {},
        clientInfo: { name: "antigravity-rive-client", version: "1.0.0" }
      }
    }) + "\n";
    proc.stdin.write(initReq);
  });
}

if (require.main === module) {
  const toolName = process.argv[2];
  const argsJson = process.argv[3] ? JSON.parse(process.argv[3]) : {};
  if (!toolName) {
    console.error("Usage: node scripts/rive_mcp_client.js <toolName> '<argsJson>'");
    process.exit(1);
  }
  callMcpTool(toolName, argsJson)
    .then((res) => {
      console.log(JSON.stringify(res, null, 2));
    })
    .catch((err) => {
      console.error("Tool call failed:", err);
      process.exit(1);
    });
}

module.exports = { callMcpTool };
