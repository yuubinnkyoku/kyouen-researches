// probe3.js — bounded-edit classes (1,0),(2,0),(2,1) around every placement of the two
// published 8x28 witnesses on 8x29 (deficient-maximal search; (0,0),(1,1) covered by probe2).
// Deterministic; census screening; every hit confirmed by sat.js verifyConfig.
'use strict';
const fs = require('fs');
const S = require('../scripts/sat.js');

const W = 8, M1 = 28, M2 = 29, Q = 9;
const t0 = Date.now();
function loadStones(p) { const j = JSON.parse(fs.readFileSync(p, 'utf8')); return j.stones.map(([x, y]) => [x, y]); }
const { P, n, curves } = S.buildCensus(W, M2, Q);
const NC = curves.length;
const idxOf = new Map();
P.forEach((p, i) => idxOf.set(p[0] + ',' + p[1], i));
const curvePts = curves.map(c => c.pts);
const onCurve = new Uint8Array(NC * n);
for (let ci = 0; ci < NC; ci++) for (const p of curvePts[ci]) onCurve[ci * n + p] = 1;
const through = Array.from({ length: n }, () => []);
for (let ci = 0; ci < NC; ci++) for (const p of curvePts[ci]) through[p].push(ci);

function mkPlacement(stones) {
  const stoneSet = new Uint8Array(n);
  for (const [x, y] of stones) { const i = idxOf.get(x + ',' + y); stoneSet[i] = 1; }
  const cnt = new Int32Array(NC);
  for (let ci = 0; ci < NC; ci++) { let c = 0; for (const p of curvePts[ci]) if (stoneSet[p]) c++; cnt[ci] = c; }
  return { stoneSet, cnt };
}

const seeds = [loadStones('probe/s8x28q9_rowY3.witness.json'), loadStones('probe/witness_c3k37p1_28.json')];
const images = { id: (x, y) => [x, y], H: (x, y) => [M1 - 1 - x, y], V: (x, y) => [x, W - 1 - y], HV: (x, y) => [M1 - 1 - x, W - 1 - y] };

const placements = [];
const hits = [];
for (let si = 0; si < seeds.length; si++) {
  for (const [iname, img] of Object.entries(images)) {
    const mapped = seeds[si].map(([x, y]) => img(x, y));
    const maxx = Math.max(...mapped.map(p => p[0]));
    for (let t = 0; maxx + t <= M2 - 1; t++) {
      const stones = mapped.map(([x, y]) => [x + t, y]);
      const pl = mkPlacement(stones);
      let unsafe = 0; for (let ci = 0; ci < NC; ci++) if (pl.cnt[ci] >= Q) unsafe++;
      const rec = { seed: si, image: iname, shift: t, unsafe };
      placements.push(rec);
      if (unsafe > 0) continue;
      const stoneIdx = []; for (let i = 0; i < n; i++) if (pl.stoneSet[i]) stoneIdx.push(i);
      const freeIdx = []; for (let i = 0; i < n; i++) if (!pl.stoneSet[i]) freeIdx.push(i);
      const cntFull = (ci, s1, s2, z) => {
        const base = ci * n;
        let c = pl.cnt[ci];
        if (s1 >= 0 && onCurve[base + s1]) c--;
        if (s2 >= 0 && onCurve[base + s2]) c--;
        if (z >= 0 && onCurve[base + z]) c++;
        return c;
      };
      const checkConfig = (rmArr, z, kind) => {
        const s1 = rmArr[0], s2 = rmArr.length > 1 ? rmArr[1] : -1;
        for (let ci = 0; ci < NC; ci++) if (cntFull(ci, s1, s2, z) >= Q) return false;
        const occ = new Uint8Array(n);
        for (const i of stoneIdx) occ[i] = 1;
        for (const i of rmArr) occ[i] = 0;
        if (z >= 0) occ[z] = 1;
        for (let p = 0; p < n; p++) {
          if (occ[p]) continue;
          let b = false;
          for (const ci of through[p]) if (cntFull(ci, s1, s2, z) >= Q - 1) { b = true; break; }
          if (!b) return false;
        }
        const cand = stones.filter(([x, y]) => !rmArr.some(i => P[i][0] === x && P[i][1] === y)).concat(z >= 0 ? [P[z]] : []);
        const v = S.verifyConfig(W, M2, Q, cand);
        if (v.ok) hits.push({ kind, seed: si, image: iname, shift: t, removed: rmArr.map(i => P[i]), added: z >= 0 ? P[z] : null, size: cand.length, rows: v.rows, minRow: v.minRow, stones: cand });
        else throw new Error('screening false positive ' + kind + ' ' + JSON.stringify({ si, iname, t, rmArr, z }));
        return true;
      };
      for (const s of stoneIdx) checkConfig([s], -1, '(1,0)');
      rec.checked10 = stoneIdx.length;
      for (let a = 0; a < stoneIdx.length; a++) for (let b2 = a + 1; b2 < stoneIdx.length; b2++) checkConfig([stoneIdx[a], stoneIdx[b2]], -1, '(2,0)');
      rec.checked20 = stoneIdx.length * (stoneIdx.length - 1) / 2;
      let c21safe = 0;
      for (let a = 0; a < stoneIdx.length; a++) for (let b2 = a + 1; b2 < stoneIdx.length; b2++) {
        const s1 = stoneIdx[a], s2 = stoneIdx[b2];
        for (const z of freeIdx) {
          let zsafe = true;
          for (const ci of through[z]) if (cntFull(ci, s1, s2, z) >= Q) { zsafe = false; break; }
          if (!zsafe) continue;
          c21safe++;
          checkConfig([s1, s2], z, '(2,1)');
        }
      }
      rec.checked21safe = c21safe;
    }
  }
}
fs.writeFileSync('probe/probe3_result.json', JSON.stringify({ board: [W, M2, Q], placements, hits, ms: Date.now() - t0 }, null, 1));
console.log(JSON.stringify({ placements: placements.map(p => ({ seed: p.seed, image: p.image, shift: p.shift, unsafe: p.unsafe, checked10: p.checked10, checked20: p.checked20, checked21safe: p.checked21safe })), hits: hits.length, deficientHits: hits.filter(h => h.minRow <= Q - 2).length, ms: Date.now() - t0 }, null, 1));
