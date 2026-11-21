// extract_witness.js — parse kissat model (v-lines) from the def-mode CNF run,
// map positive cell vars (1..n, row-major i = y*m + x) to stone points, print
// "x1:y1,x2:y2,..." and run the lane's own sat.js verifyConfig (same-implementation
// check; independent geometry check is verify34.py).
'use strict';
const fs = require('fs');
const S = require('./sat.js');

const outFile = process.argv[2];   // kissat output with v-lines
const w = Number(process.argv[3]);
const m = Number(process.argv[4]);
const q = Number(process.argv[5]);
const n = w * m;
const txt = fs.readFileSync(outFile, 'utf8');
let pos = new Set();
for (const line of txt.split('\n')) {
  if (!line.startsWith('v ')) continue;
  for (const tok of line.slice(2).trim().split(/\s+/)) {
    const v = Number(tok);
    if (v > 0 && v <= n) pos.add(v);
    if (v === 0) break;
  }
}
const stones = [];
for (let i = 0; i < n; i++) if (pos.has(i + 1)) stones.push([i % m, Math.floor(i / m)]);
const coord = stones.map(p => p[0] + ':' + p[1]).join(',');
const verify = S.verifyConfig(w, m, q, stones);
console.log(JSON.stringify({ w, m, q, stones: stones.length, coord, verify }));
