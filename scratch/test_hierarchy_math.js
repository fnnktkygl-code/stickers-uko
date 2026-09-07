// Hierarchy definitions:
// Artboard: 1024 x 1024
const groups = {
  root: { id: "root", x: 512, y: 876 },
  shadow_group: { id: "shadow_group", parent: "root", x: 0, y: 0 },
  feet_group: { id: "feet_group", parent: "root", x: 0, y: 0 },
  body_group: { id: "body_group", parent: "root", x: 0, y: -378 }, // global: (512, 498)
  wings_group: { id: "wings_group", parent: "body_group", x: 0, y: 0 }, // global: (512, 498)
  wing_l_group: { id: "wing_l_group", parent: "wings_group", x: -294, y: 0 }, // global: (218, 498)
  wing_r_group: { id: "wing_r_group", parent: "wings_group", x: 294, y: 0 }, // global: (806, 498)
  chest_group: { id: "chest_group", parent: "body_group", x: 0, y: 0 }, // global: (512, 498)
  head_group: { id: "head_group", parent: "body_group", x: 0, y: -126 }, // global: (512, 372)
  eye_l_group: { id: "eye_l_group", parent: "head_group", x: -114.5, y: -10.5 }, // global: (397.5, 361.5)
  eye_r_group: { id: "eye_r_group", parent: "head_group", x: 120, y: -16 }, // global: (632, 356)
  beak_group: { id: "beak_group", parent: "head_group", x: 0, y: 44 } // global: (512, 416)
};

// Calculate global offset for any group
function getGlobalOffset(groupId) {
  let gx = 0, gy = 0;
  let curr = groups[groupId];
  while (curr) {
    gx += curr.x;
    gy += curr.y;
    curr = curr.parent ? groups[curr.parent] : null;
  }
  return { gx, gy };
}

for (const gid of Object.keys(groups)) {
  const { gx, gy } = getGlobalOffset(gid);
  console.log(`Group ${gid.padEnd(16)}: global = (${gx}, ${gy})`);
}
