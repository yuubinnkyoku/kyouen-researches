// decode a SAT model (cell vars are 1..n in pts order) and verify with census-free verifier
const fs = require('fs');
const mod = require('./row_deficient_sat.js');
const [w, m, q] = process.argv.slice(2, 5).map(Number);
const modelFile = process.argv[5];
const lits = fs.readFileSync(modelFile, 'utf8').trim().split(/\s+/).map(Number);
const nv = lits.length;
const { P } = mod.pts(w, m) ? {} : {};
const pts = []; for (let y = 0; y < w; y++) for (let x = 0; x < m; x++) pts.push([x, y]);
const stones = [];
for (let i = 0; i < pts.length; i++) if (lits[i] > 0) stones.push(pts[i]);
const verify = mod.verifyConfig(w, m, q, stones);
const rows = {};
for (const s of stones) rows[s[1]] = (rows[s[1]] || 0) + 1;
console.log(JSON.stringify({ w, m, q, stones: stones.length, rows, verify }));
