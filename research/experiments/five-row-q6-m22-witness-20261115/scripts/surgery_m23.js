// surgery_m23.js — transplant the m=22 q=6 witness onto 5x23, analyze the blocking structure,
// and enumerate ALL 1-stone surgeries (remove 1, add 1).
// Soundness: a 1-stone witness needs U=(22,0) blocked or occupied, so the added
//   stone must lie on a T-curve (58 seed-empty candidate cells) or be U itself.
// (A 1-stone move cannot otherwise raise any T-curve to q-1=5 or occupy U.)
// 2-stone surgeries are covered by surgery2b_m23.js (heavy-T-curve sound filter).
'use strict';
const S = require('./sat.js');

const W = 5, M = 23, Q = 6;
// m=22 witness (rows [4,5,5,5,5], single deficient row 0)
const SEED = [[0,0],[11,0],[15,0],[20,0],[3,1],[6,1],[10,1],[15,1],[18,1],[3,2],[6,2],[8,2],[10,2],[15,2],[4,3],[6,3],[9,3],[16,3],[17,3],[7,4],[9,4],[11,4],[12,4],[14,4]];

const t0 = Date.now();
const { P, n, curves } = S.buildCensus(W, M, Q);
const idx = (x, y) => y * M + x;
const occ = new Uint8Array(n);
for (const [x, y] of SEED) occ[idx(x, y)] = 1;

// per-curve seed counts
const cnt = new Int32Array(curves.length);
for (let ci = 0; ci < curves.length; ci++) { let c = 0; for (const p of curves[ci].pts) c += occ[p]; cnt[ci] = c; }
// curves through each cell
const through = Array.from({ length: n }, () => []);
curves.forEach((cu, ci) => { for (const p of cu.pts) through[p].push(ci); });

// safety of transplanted seed
let unsafe = 0;
for (let ci = 0; ci < curves.length; ci++) if (cnt[ci] >= Q) unsafe++;
// maximality: per empty cell, max curve count
const emptyCells = [];
for (let i = 0; i < n; i++) if (!occ[i]) emptyCells.push(i);
const maxCnt = new Int32Array(n).fill(-1);
const unblocked = [];
for (const c of emptyCells) {
  let mx = 0;
  for (const ci of through[c]) if (cnt[ci] > mx) mx = cnt[ci];
  maxCnt[c] = mx;
  if (mx < Q - 1) unblocked.push(c);
}
const T = unblocked.length === 1 ? through[unblocked[0]] : null;
const U = unblocked[0];
const Tset = new Set();
for (const ci of T) for (const p of curves[ci].pts) if (p !== U) Tset.add(p);
const Tempty = [...Tset].filter(p => !occ[p]);
console.log(JSON.stringify({
  ms: Date.now() - t0, curves: curves.length, unsafeCurves: unsafe,
  emptyCells: emptyCells.length, unblocked: unblocked.map(p => [p % M, Math.floor(p / M)]),
  tCurves: T.length, tSet: Tset.size, tSetEmpty: Tempty.length,
  tCurveCounts: T.map(ci => cnt[ci]).sort((a, b) => b - a).join(',')
}));

// ---- helper: evaluate a final occupancy array ----
function evaluate(o) {
  // safety: any curve >= Q
  for (let ci = 0; ci < curves.length; ci++) { let c = 0; for (const p of curves[ci].pts) { c += o[p]; if (c >= Q) return { ok: false, why: 'unsafe' }; } }
  // maximality
  for (let c = 0; c < n; c++) {
    if (o[c]) continue;
    let blocked = false;
    for (const ci of through[c]) { let k = 0; for (const p of curves[ci].pts) k += o[p]; if (k >= Q - 1) { blocked = true; break; } }
    if (!blocked) return { ok: false, why: 'open', cell: c };
  }
  return { ok: true };
}

// ---- 1-stone surgery: remove s, add a (a in Tset ∪ {U}, vacant) ----
const stones = SEED.map(([x, y]) => idx(x, y));
const add1cand = [...Tempty, U];
let one = 0, oneConfigs = 0;
for (const s of stones) {
  for (const a of add1cand) {
    if (a === s) continue;
    if (occ[a]) continue;
    oneConfigs++;
    const o = occ.slice(); o[s] = 0; o[a] = 1;
    if (evaluate(o).ok) { one++; console.log('1STONE WITNESS', JSON.stringify({ s, a })); }
  }
}
console.log(JSON.stringify({ oneStoneConfigs: oneConfigs, oneStoneWitnesses: one }));
