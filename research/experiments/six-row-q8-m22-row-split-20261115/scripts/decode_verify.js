// decode_verify.js — decode a kissat SAT log into stones and run both verifiers.
// Usage: node decode_verify.js w m q <kissat_log> <out_json>
// Cell variables are the first w*m variables of the sat2.js encoding (cell[i] = var i+1, i = y*m + x).
'use strict';
const S = require('./sat.js');
const fs = require('fs');
const [w, m, q] = [Number(process.argv[2]), Number(process.argv[3]), Number(process.argv[4])];
const log = fs.readFileSync(process.argv[5], 'utf8');
const outPath = process.argv[6];
const n = w * m;
// collect v-lines (kissat prints model in multiple v lines, signs are + for true)
const pos = new Set();
for (const line of log.split('\n')) {
  if (!line.startsWith('v ')) continue;
  for (const tok of line.slice(2).trim().split(/\s+/)) {
    const v = Number(tok);
    if (!v) continue;
    if (v > 0 && v <= n) pos.add(v);
  }
}
if (pos.size === 0) throw new Error('no model found');
const P = S.pts(w, m);
const stones = [];
for (let i = 0; i < n; i++) if (pos.has(i + 1)) stones.push(P[i]);
const verify = S.verifyConfig(w, m, q, stones);
const rows = new Array(w).fill(0);
for (const [x, y] of stones) rows[y]++;
const out = { w, m, q, nStones: stones.length, rows, stones, jsVerify: verify };
fs.writeFileSync(outPath, JSON.stringify(out) + '\n');
fs.writeFileSync(outPath + '.stones.json', JSON.stringify(stones));
console.log(JSON.stringify({ nStones: stones.length, rows, jsVerify: verify }));
