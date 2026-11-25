// extend5.js: pruned removal+addition column-extension enumeration for q=5, targets M>=30.
// Prune: a new-column cell blocked by >=4 kept stones must NOT be filled (unsafe);
// additions may only use unblocked cells; remaining unblocked cells must become blocked by additions.
const S = require('./scripts/sat.js');
const fs = require('fs');
const R = Number(process.argv[2] || 2);
const MINM = Number(process.argv[3] || 30);
const MAXM = Number(process.argv[4] || 32);
const BF = process.argv[5] || '';

function subsetsAtMost(arr, cap) {
  const out = [];
  const stack = (i, cur) => { out.push(cur.slice()); if (cur.length === cap) return; for (let j = i; j < arr.length; j++) { cur.push(arr[j]); stack(j + 1, cur); cur.pop(); } };
  stack(0, []);
  return out;
}

let pool = [];
for (const f of ['wits/sa3.jsonl', 'wits/sae.jsonl']) {
  for (const line of fs.readFileSync(f, 'utf8').split('\n')) {
    if (!line.trim()) continue;
    let d; try { d = JSON.parse(line); } catch (e) { continue; }
    const st = d.stones || d.witness; if (!st || !d.witness) continue;
    if (d.w === 6 && d.q === 5) pool.push({ m: d.m, st });
  }
}
for (const d of JSON.parse(fs.readFileSync('wits/extended.json', 'utf8'))) {
  if (d.w === 6 && d.q === 5) pool.push({ m: d.toM, st: d.stones });
}
const seen = new Set();
pool = pool.filter(p => { const k = p.m + '|' + p.st.map(s => s.join(',')).sort().join(';'); if (seen.has(k)) return false; seen.add(k); return true; });
console.error('bases:', pool.map(p => p.m + 'x' + p.st.length).join(' '));

const capDef = 23;
const found = [];
let stats = { remsets: 0, candidateAdds: 0, fullVerify: 0 };

for (const p of pool) {
  if (BF && (p.m + 'x' + p.st.length) !== BF) continue;
  const spare = capDef - p.st.length;
  for (let M = Math.max(MINM, p.m + 1); M <= Math.min(MAXM, p.m + 3); M++) {
    // board census for 6xM with >=4-point curves (blocking needs >=4 stones)
    const cen = buildBlockCensus(6, M, 4);
    for (let off = 0; off + p.m <= M; off++) {
      const shifted = p.st.map(([x, y]) => [x + off, y]);
      const newCells = [];
      for (let x = 0; x < M; x++) for (let y = 0; y < 6; y++) if (!(x >= off && x < off + p.m)) newCells.push([x, y]);
      const rems = [[]];
      if (R >= 1) for (let i = 0; i < p.st.length; i++) rems.push([i]);
      if (R >= 2) for (let i = 0; i < p.st.length; i++) for (let j = i + 1; j < p.st.length; j++) rems.push([i, j]);
      if (R >= 3) for (let i = 0; i < p.st.length; i++) for (let j = i + 1; j < p.st.length; j++) for (let k3 = j + 1; k3 < p.st.length; k3++) rems.push([i, j, k3]);
      for (const rem of rems) {
        stats.remsets++;
        const rs = new Set(rem.map(i => shifted[i][0] + ',' + shifted[i][1]));
        const kept = shifted.filter(s => !rs.has(s[0] + ',' + s[1]));
        const budget = spare + rem.length;
        // blocked-by-kept among new cells
        const keptSet = new Set(kept.map(s => s[0] + ',' + s[1]));
        const unblocked = [];
        for (const c of newCells) {
          let bl = false;
          const key = c[0] + ',' + c[1];
          for (const cu of cen.through[key] || []) {
            let cnt = 0;
            for (const pt of cu.pts) { if (keptSet.has(pt)) cnt++; }
            if (cnt >= 4) { bl = true; break; }
          }
          if (!bl) unblocked.push(c);
        }
        if (unblocked.length > 12) continue; // cannot cover with <=budget additions blocking-wise (heuristic skip)
        const addSets = subsetsAtMost(unblocked, Math.min(budget, unblocked.length));
        for (const A of addSets) {
          if (A.length > budget) continue;
          stats.candidateAdds++;
          const cand = kept.concat(A);
          if (cand.length > capDef) continue;
          // quick necessary check: safety of A relative to kept (no curve with kept+A >=5) then full verify
          const v = S.verifyConfig(6, M, 5, cand);
          stats.fullVerify++;
          if (v.ok) {
            found.push({ M, size: cand.length, base: p.m + 'x' + p.st.length, off, rem: rem.length, add: A.length, rows: v.rows, stones: cand });
            console.error('FOUND', JSON.stringify({ M, size: cand.length, rows: v.rows, rem: rem.length, add: A.length }));
          }
        }
      }
    }
    console.error('progress', JSON.stringify({ base: p.m + 'x' + p.st.length, M, ...stats, found: found.length }));
  }
}
console.log(JSON.stringify({ stats, found: found.length, witnesses: found }, null, 1));

function buildBlockCensus(w, m, minPts) {
  const P = []; for (let y = 0; y < w; y++) for (let x = 0; x < m; x++) P.push([x, y]);
  const n = P.length;
  const curves = [];
  const lineMap = new Map();
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
    const lo = S.lineABC ? null : null;
  }
  // use internal functions from sat.js via re-implementation
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
    const a = P[i], b = P[j];
    let l = a[1] - b[1], k = b[0] - a[0], c = a[0] * b[1] - b[0] * a[1];
    const g = (function gg(x, y) { x = Math.abs(x); y = Math.abs(y); while (y) { const t = x % y; x = y; y = t; } return x; })(l, k) || 1;
    l /= g; k /= g; c /= g;
    if (l < 0 || (l === 0 && k < 0)) { l = -l; k = -k; c = -c; }
    const key = l + ',' + k + ',' + c;
    if (!lineMap.has(key)) lineMap.set(key, [l, k, c]);
  }
  for (const [key, lo] of lineMap) {
    const set = [];
    for (let idx = 0; idx < n; idx++) if (lo[0] * P[idx][0] + lo[1] * P[idx][1] + lo[2] === 0) set.push(P[idx][0] + ',' + P[idx][1]);
    if (set.length >= minPts) curves.push({ pts: set });
  }
  // circles: reuse sat.js circleABC through triples
  const circMap = new Map();
  const Smod = require('./scripts/sat.js');
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) for (let k2 = j + 1; k2 < n; k2++) {
    const co = circleABCPub(P[i], P[j], P[k2]);
    if (!co) continue;
    const key = co.join(',');
    if (!circMap.has(key)) circMap.set(key, co);
  }
  for (const [key, co] of circMap) {
    const set = [];
    for (let idx = 0; idx < n; idx++) if (co[0] * (P[idx][0] * P[idx][0] + P[idx][1] * P[idx][1]) + co[1] * P[idx][0] + co[2] * P[idx][1] + co[3] === 0) set.push(P[idx][0] + ',' + P[idx][1]);
    if (set.length >= minPts) curves.push({ pts: set });
  }
  const through = {};
  for (const cu of curves) for (const key of cu.pts) (through[key] = through[key] || []).push(cu);
  return { curves, through };
}
function circleABCPub(p1, p2, p3) {
  const [x1, y1] = p1, [x2, y2] = p2, [x3, y3] = p3;
  const s1 = x1 * x1 + y1 * y1, s2 = x2 * x2 + y2 * y2, s3 = x3 * x3 + y3 * y3;
  const det = x1 * (y2 - y3) - y1 * (x2 - x3) + (x2 * y3 - x3 * y2);
  if (det === 0) return null;
  const B = s1 * (y2 - y3) - y1 * (s2 - s3) + (s2 * y3 - s3 * y2);
  const C = x1 * (s2 - s3) - s1 * (x2 - x3) + (x2 * s3 - x3 * s2);
  const D = x1 * (y2 * s3 - y3 * s2) - y1 * (x2 * s3 - x3 * s2) + s1 * (x2 * y3 - x3 * y2);
  let a = det, b = -B, c = -C, d = -D;
  const g = (function gg(x, y) { x = Math.abs(x); y = Math.abs(y); while (y) { const t = x % y; x = y; y = t; } return x; })(g0(g0(a, b), c), d) || 1;
  function g0(x, y) { x = Math.abs(x); y = Math.abs(y); while (y) { const t = x % y; x = y; y = t; } return x; }
  a /= g; b /= g; c /= g; d /= g;
  if (a < 0 || (a === 0 && (b < 0 || (b === 0 && (c < 0 || (c === 0 && d < 0)))))) { a = -a; b = -b; c = -c; d = -d; }
  return [a, b, c, d];
}
