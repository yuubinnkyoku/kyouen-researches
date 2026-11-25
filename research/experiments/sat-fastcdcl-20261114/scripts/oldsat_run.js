// run the repo's verbatim CDCL on a DIMACS file (same parse as fastsat)
const fs = require('fs');
const mod = require('./row_deficient_sat.js');
const raw = fs.readFileSync(process.argv[2], 'utf8');
const clauses = [];
let nv = 0;
for (const line of raw.split('\n')) {
  const t = line.trim();
  if (!t || t[0] === 'p' || t[0] === 'c') continue;
  const cur = [];
  for (const s of t.split(/\s+/)) { const n = parseInt(s, 10); if (isNaN(n) || n === 0) continue; cur.push(n); }
  if (cur.length) { clauses.push(cur); for (const l of cur) { const v = Math.abs(l); if (v > nv) nv = v; } }
}
const t0 = Date.now();
const res = mod.cdcl(nv, clauses, parseInt(process.argv[3] || '3000000'));
const out = { sat: !!res.sat, timeout: !!res.timeout, conflicts: res.conflicts, ms: Date.now() - t0 };
if (res.sat) {
  const stones = [];
  const pts = []; for (let y = 0; y < 6; y++) for (let x = 0; x < 22; x++) pts.push([x, y]);
  for (let i = 0; i < 132; i++) if (res.model[i + 1]) stones.push(pts[i]);
  out.stones = stones.length;
}
console.log(JSON.stringify(out));
