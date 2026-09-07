const fs = require("fs");
const path = require("path");

const fragment = JSON.parse(fs.readFileSync("scratch/owluko_user_exact.scene.json", "utf8"));
console.log("Shapes count:", fragment.shapes.length);

// Check if any shape has undefined x or y
for (const s of fragment.shapes) {
  if (typeof s.x !== "number" || typeof s.y !== "number") {
    console.error("Shape missing x or y:", s.id);
  }
}
console.log("All shapes have valid x, y!");
