'use strict';
const fs = require('fs');
const path = require('path');
const [w, m, q] = [Number(process.argv[2]), Number(process.argv[3]), Number(process.argv[4])];
const modelFile = process.argv[5];
const txt = fs.readFileSync(modelFile, 'utf8');
const lits = [];
for (const line of txt.split('\n')) {
  const t = line.trim();
  if (t.startsWith('v ')) for (const tok of t.slice(2).trim().split(/\s+/)) { const v = Number(tok); if (Number.isFinite(v) && v !== 0) lits.push(v); }
}
const val = new Map();
for (const l of lits) val.set(Math.abs(l), l > 0);
const stones = [];
for (let y = 0; y < w; y++) for (let x = 0; x < m; x++) if (val.get(y * m + x + 1)) stones.push([x, y]);
const S = require(path.join(__dirname, 'sat.js'));
const verify = S.verifyConfig(w, m, q, stones);
const rows = Array.from({ length: w }, (_, y) => stones.filter(s => s[1] === y).length);
console.log(JSON.stringify({ w, m, q, nStones: stones.length, rows, stones, jsVerify: verify }));
