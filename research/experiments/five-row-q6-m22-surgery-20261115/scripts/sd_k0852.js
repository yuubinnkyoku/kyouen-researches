#!/usr/bin/env node
// Post-hoc geometry: symmetric difference between the K0852 m=22 witness
// (five-row-q6-m22-witness-20261115, class {0} k=4 minpos=0, 24 stones) and
// every isometric column-offset embedding of the K0815 m=21 seed
// (seeds/seed_w56_21.json) on the 5x22 board.
// Pure computation; no solver. Usage: node sd_k0852.js

"use strict";
const W = [[0,0],[11,0],[15,0],[20,0],[3,1],[6,1],[10,1],[15,1],[18,1],[3,2],[6,2],[8,2],[10,2],[15,2],[4,3],[6,3],[9,3],[16,3],[17,3],[7,4],[9,4],[11,4],[12,4],[14,4]];
const S21 = require("../seeds/seed_w56_21.json").stones;
const key = (p) => p[0] + ',' + p[1];
const sd = (A, B) => {
  const sa = new Set(A.map(key)), sb = new Set(B.map(key));
  let d = 0;
  for (const k of sa) if (!sb.has(k)) d++;
  for (const k of sb) if (!sa.has(k)) d++;
  return d;
};
const h = 5, w = 21;
const iso = {
  id: (p) => [p[0], p[1]],
  H:  (p) => [w - 1 - p[0], p[1]],
  V:  (p) => [p[0], h - 1 - p[1]],
  HV: (p) => [w - 1 - p[0], h - 1 - p[1]],
};
const rows = [];
for (const [nm, f] of Object.entries(iso)) {
  for (const offX of [0, 1]) {
    const emb = S21.map((p) => { const q = f(p); return [q[0] + offX, q[1]]; });
    rows.push({ iso: nm, offX, sd: sd(emb, W) });
  }
}
rows.sort((a, b) => a.sd - b.sd);
const out = { witness: 'K0852 five-row-q6-m22-witness-20261115', seed: 'K0815 seeds_w56_21 (5x21, 24 stones)', embeddings: rows, minSd: rows[0].sd, note: 'min symmetric difference over all 4 isometries x 2 column offsets; both id@0 and H@0 attain the minimum 28' };
console.log(JSON.stringify(out, null, 1));
