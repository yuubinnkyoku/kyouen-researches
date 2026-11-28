// probe_ctrl.js — controls for the transplant/add-one/swap surgery screening pipeline.
// C1/C2: census screening on the unmodified 8x28 seeds must reproduce safe+maximal.
// C3: deterministic sample of rejected candidates at 8x29 (seed0/id/t0) dumped for pyVerify.
'use strict';
const fs = require('fs');
const S = require('../scripts/sat.js');
const W = 8, M1 = 28, M2 = 29, Q = 9;

function loadStones(p) { const j = JSON.parse(fs.readFileSync(p, 'utf8')); return j.stones.map(([x, y]) => [x, y]); }
function mkBoard(m) {
  const { P, n, curves } = S.buildCensus(W, m, Q);
  const NC = curves.length;
  const idxOf = new Map(); P.forEach((p, i) => idxOf.set(p[0] + ',' + p[1], i));
  const curvePts = curves.map(c => c.pts);
  const through = Array.from({ length: n }, () => []);
  for (let ci = 0; ci < NC; ci++) for (const p of curvePts[ci]) through[p].push(ci);
  return { P, n, NC, idxOf, curvePts, through };
}
function analyzeBoard(B, stones) {
  const stoneSet = new Uint8Array(B.n);
  for (const [x, y] of stones) { const i = B.idxOf.get(x + ',' + y); if (i === undefined) throw new Error('off board'); stoneSet[i] = 1; }
  const cnt = new Int32Array(B.NC);
  let unsafe = 0;
  for (let ci = 0; ci < B.NC; ci++) { let c = 0; for (const p of B.curvePts[ci]) if (stoneSet[p]) c++; cnt[ci] = c; if (c >= Q) unsafe++; }
  const unblocked = [];
  for (let i = 0; i < B.n; i++) {
    if (stoneSet[i]) continue;
    let b = false;
    for (const ci of B.through[i]) if (cnt[ci] >= Q - 1) { b = true; break; }
    if (!b) unblocked.push(i);
  }
  return { unsafe, unblocked: unblocked.map(i => B.P[i]) };
}

const seeds = [loadStones('probe/s8x28q9_rowY3.witness.json'), loadStones('probe/witness_c3k37p1_28.json')];
const B28 = mkBoard(M1);
const ctrl = seeds.map((st, i) => {
  const a = analyzeBoard(B28, st);
  const v = S.verifyConfig(W, M1, Q, st);
  return { seed: i, unsafe: a.unsafe, nUnblocked: a.unblocked.length, verifyOk: v.ok, size: v.size, rows: v.rows };
});

const B29 = mkBoard(M2);
const st29 = seeds[0];
const a29 = analyzeBoard(B29, st29);
const stoneSet = new Uint8Array(B29.n);
for (const [x, y] of st29) stoneSet[B29.idxOf.get(x + ',' + y)] = 1;
const cnt = new Int32Array(B29.NC);
for (let ci = 0; ci < B29.NC; ci++) { let c = 0; for (const p of B29.curvePts[ci]) if (stoneSet[p]) c++; cnt[ci] = c; }
const onCurve = new Uint8Array(B29.NC * B29.n);
for (let ci = 0; ci < B29.NC; ci++) for (const p of B29.curvePts[ci]) onCurve[ci * B29.n + p] = 1;
const stoneIdx = []; for (let i = 0; i < B29.n; i++) if (stoneSet[i]) stoneIdx.push(i);
const freeIdx = []; for (let i = 0; i < B29.n; i++) if (!stoneSet[i]) freeIdx.push(i);
const sample = [];
let got = 0;
outer11:
for (const s of stoneIdx) for (const z of freeIdx) {
  let zsafe = true;
  for (const ci of B29.through[z]) { const c = cnt[ci] - (onCurve[ci * B29.n + s] ? 1 : 0); if (c >= Q - 1) { zsafe = false; break; } }
  if (!zsafe) continue;
  let maximal = true;
  for (const p of freeIdx) {
    if (p === z) continue;
    let b = false;
    for (const ci of B29.through[p]) { const base = ci * B29.n; const c = cnt[ci] - (onCurve[base + s] ? 1 : 0) + (onCurve[base + z] ? 1 : 0); if (c >= Q - 1) { b = true; break; } }
    if (!b) { maximal = false; break; }
  }
  if (maximal) { let b = false; for (const ci of B29.through[s]) { const c = cnt[ci] - 1 + (onCurve[ci * B29.n + z] ? 1 : 0); if (c >= Q - 1) { b = true; break; } } if (!b) maximal = false; }
  if (!maximal) { sample.push({ kind: 'swap-1-1', rm: [s], z }); got++; if (got >= 6) break outer11; }
}
let got21 = 0;
outer21:
for (let a = 0; a < stoneIdx.length; a++) for (let b2 = a + 1; b2 < stoneIdx.length; b2++) {
  const s1 = stoneIdx[a], s2 = stoneIdx[b2];
  for (const z of freeIdx) {
    let zsafe = true;
    for (const ci of B29.through[z]) { const base = ci * B29.n; const c = cnt[ci] - (onCurve[base + s1] ? 1 : 0) - (onCurve[base + s2] ? 1 : 0) + (onCurve[base + z] ? 1 : 0); if (c >= Q) { zsafe = false; break; } }
    if (!zsafe) continue;
    const occ = new Uint8Array(B29.n);
    for (const i of stoneIdx) occ[i] = 1;
    occ[s1] = 0; occ[s2] = 0; occ[z] = 1;
    let maximal = true;
    for (let p = 0; p < B29.n; p++) {
      if (occ[p]) continue;
      let b = false;
      for (const ci of B29.through[p]) { const base = ci * B29.n; const c = cnt[ci] - (onCurve[base + s1] ? 1 : 0) - (onCurve[base + s2] ? 1 : 0) + (onCurve[base + z] ? 1 : 0); if (c >= Q - 1) { b = true; break; } }
      if (!b) { maximal = false; break; }
    }
    if (!maximal) { sample.push({ kind: '(2,1)', rm: [s1, s2], z }); got21++; if (got21 >= 6) break outer21; }
  }
}
const dumps = sample.map((sm, k) => {
  const cand = st29.filter(([x, y]) => !sm.rm.some(i => x === B29.P[i][0] && y === B29.P[i][1])).concat([B29.P[sm.z]]);
  const f = 'probe/ctrl_sample_' + k + '.json';
  fs.writeFileSync(f, JSON.stringify(cand));
  return { file: f, kind: sm.kind, removed: sm.rm.map(i => B29.P[i]), added: B29.P[sm.z], size: cand.length };
});
fs.writeFileSync('probe/ctrl_result.json', JSON.stringify({ ctrl28: ctrl, a29: { unsafe: a29.unsafe, nUnblocked: a29.unblocked.length, unblocked: a29.unblocked }, sample: dumps }, null, 1));
console.log(JSON.stringify({ ctrl28: ctrl, a29: { unsafe: a29.unsafe, nUnblocked: a29.unblocked.length }, nSample: dumps.length }));
