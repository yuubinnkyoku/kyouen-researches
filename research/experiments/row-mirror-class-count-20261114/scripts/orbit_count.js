// orbit_count.js — row-mirror-canonical deficiency class count: brute force vs closed form.
// A deficiency class of the class-split machinery (sat3.js --class=D) is a non-empty
// subset D of rows {0..w-1}; the row mirror V: y -> w-1-y acts on subsets, and a complete
// sweep covers one canonical representative per V-orbit (a board reflection is an
// isometry, so SAT(D) <=> SAT(V(D))). This script brute-forces the orbit count for
// w = 1..W and compares with the Burnside closed form
//   C(w) = 2^(w-1) + 2^(ceil(w/2)-1) - 1 = (2^w + 2^ceil(w/2) - 2) / 2.
// Usage: node orbit_count.js [W]   (default W = 14)
'use strict';
const W = Number(process.argv[2] || 14);
const rows = [];
for (let w = 1; w <= W; w++) {
  const mirror = (mask) => { let r = 0; for (let i = 0; i < w; i++) if (mask >> i & 1) r |= 1 << (w - 1 - i); return r; };
  const seen = new Set(); let orbits = 0;
  for (let mask = 1; mask < (1 << w); mask++) {
    if (seen.has(mask)) continue;
    orbits++; seen.add(mask); seen.add(mirror(mask));
  }
  const formula = 2 ** (w - 1) + 2 ** (Math.ceil(w / 2) - 1) - 1;
  rows.push({ w, orbits, formula, match: orbits === formula });
}
console.log(JSON.stringify({ generated: new Date().toISOString(), w_max: W, rows }, null, 1));
if (rows.some(r => !r.match)) { process.exitCode = 1; }
