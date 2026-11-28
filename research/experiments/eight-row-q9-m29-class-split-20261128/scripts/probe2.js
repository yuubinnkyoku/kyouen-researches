// probe2.js — complete transplant / add-one / swap(1,1) enumeration at 8x29 for the (8,9) family.
// Deterministic; census-based screening with O(1) curve membership; every hit confirmed by sat.js verifyConfig.
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
  for (const [x, y] of stones) { const i = idxOf.get(x + ',' + y); if (i === undefined) throw new Error('off board ' + x + ',' + y); stoneSet[i] = 1; }
  const cnt = new Int32Array(NC);
  for (let ci = 0; ci < NC; ci++) { const base = ci * n; let c = 0; for (const p of curvePts[ci]) if (stoneSet[p]) c++; cnt[ci] = c; }
  return { stoneSet, cnt };
}
function baseUnblocked(stoneSet, cnt) {
  const un = [];
  for (let i = 0; i < n; i++) {
    if (stoneSet[i]) continue;
    let b = false;
    for (const ci of through[i]) if (cnt[ci] >= Q - 1) { b = true; break; }
    if (!b) un.push(i);
  }
  return un;
}

const seeds = [loadStones('probe/s8x28q9_rowY3.witness.json'), loadStones('probe/witness_c3k37p1_28.json')];
const images = { id: (x, y) => [x, y], H: (x, y) => [M1 - 1 - x, y], V: (x, y) => [x, W - 1 - y], HV: (x, y) => [M1 - 1 - x, W - 1 - y] };

const placements = [];
const hits = [];
for (let si = 0; si < seeds.length; si++) {
  for (const [iname, img] of Object.entries(images)) {
    const mapped = seeds[si].map(([x, y]) => img(x, y));
    const xs = mapped.map(p => p[0]);
    const maxx = Math.max(...xs), minx = Math.min(...xs);
    for (let t = 0; maxx + t <= M2 - 1; t++) {
      const stones = mapped.map(([x, y]) => [x + t, y]);
      const pl = mkPlacement(stones);
      let unsafe = 0; for (let ci = 0; ci < NC; ci++) if (pl.cnt[ci] >= Q) unsafe++;
      const un = baseUnblocked(pl.stoneSet, pl.cnt);
      const rec = { seed: si, image: iname, shift: t, span: [minx + t, maxx + t], unsafe, nUnblocked: un.length, unblocked: un.map(i => P[i]) };
      placements.push(rec);
      if (unsafe > 0) continue;
      const stoneIdx = []; for (let i = 0; i < n; i++) if (pl.stoneSet[i]) stoneIdx.push(i);
      const freeIdx = []; for (let i = 0; i < n; i++) if (!pl.stoneSet[i]) freeIdx.push(i);
      // ---- add-one (full completion): 64 stones ----
      let addOneCands = 0;
      for (const z of freeIdx) {
        let zsafe = true;
        for (const ci of through[z]) if (pl.cnt[ci] >= Q - 1) { zsafe = false; break; }
        if (!zsafe) continue;
        let ok = true;
        for (const p of un) {
          if (p === z) continue;
          let b = false;
          for (const ci of through[p]) { const c = pl.cnt[ci] + (onCurve[ci * n + z] ? 1 : 0); if (c >= Q - 1) { b = true; break; } }
          if (!b) { ok = false; break; }
        }
        if (!ok) continue;
        addOneCands++;
        const cand = stones.concat([P[z]]);
        const v = S.verifyConfig(W, M2, Q, cand);
        if (v.ok) hits.push({ kind: 'add-one-full', seed: si, image: iname, shift: t, added: P[z], size: cand.length, rows: v.rows });
        else throw new Error('screening false positive add-one ' + JSON.stringify({ si, iname, t, z }));
      }
      rec.addOneCands = addOneCands;
      // ---- swap(1,1): remove s, add z; 63 stones ----
      let swapSafeChecked = 0, swapMaxChecked = 0;
      for (const s of stoneIdx) {
        for (const z of freeIdx) {
          let zsafe = true;
          for (const ci of through[z]) { const c = pl.cnt[ci] - (onCurve[ci * n + s] ? 1 : 0); if (c >= Q - 1) { zsafe = false; break; } }
          if (!zsafe) continue;
          swapSafeChecked++;
          let maximal = true;
          for (const p of freeIdx) {
            if (p === z) continue;
            let b = false;
            for (const ci of through[p]) {
              const base = ci * n;
              const c = pl.cnt[ci] - (onCurve[base + s] ? 1 : 0) + (onCurve[base + z] ? 1 : 0);
              if (c >= Q - 1) { b = true; break; }
            }
            if (!b) { maximal = false; break; }
          }
          if (maximal) {
            let b = false;
            for (const ci of through[s]) {
              const base = ci * n;
              const c = pl.cnt[ci] - 1 + (onCurve[base + z] ? 1 : 0);
              if (c >= Q - 1) { b = true; break; }
            }
            if (!b) maximal = false;
          }
          if (!maximal) continue;
          swapMaxChecked++;
          const cand = stones.filter(([x, y]) => !(x === P[s][0] && y === P[s][1])).concat([P[z]]);
          const v = S.verifyConfig(W, M2, Q, cand);
          if (v.ok) hits.push({ kind: 'swap-1-1', seed: si, image: iname, shift: t, removed: P[s], added: P[z], size: cand.length, rows: v.rows, minRow: v.minRow, stones: cand });
          else throw new Error('screening false positive swap ' + JSON.stringify({ si, iname, t, s, z }));
        }
      }
      rec.swapSafeChecked = swapSafeChecked; rec.swapMaxChecked = swapMaxChecked;
    }
  }
}

fs.writeFileSync('probe/probe2_result.json', JSON.stringify({ board: [W, M2, Q], nCurves: NC, placements, hits, ms: Date.now() - t0 }, null, 1));
console.log(JSON.stringify({ nCurves: NC, placements: placements.map(p => ({ seed: p.seed, image: p.image, shift: p.shift, unsafe: p.unsafe, nUnblocked: p.nUnblocked, addOneCands: p.addOneCands, swapSafeChecked: p.swapSafeChecked, swapMaxChecked: p.swapMaxChecked })), addOneHits: hits.filter(h => h.kind === 'add-one-full').length, swapHits: hits.filter(h => h.kind === 'swap-1-1').length, ms: Date.now() - t0 }, null, 1));
