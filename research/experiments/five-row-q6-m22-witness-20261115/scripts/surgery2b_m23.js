// surgery2b_m23.js — complete 2-stone surgery enumeration from the m=22 witness seed on 5x23.
// Sound: final maximal config => U=(22,0) blocked or occupied => some T-curve with
// seed count >= 3 gains a net stone, or an add sits at U itself. Only T-curves with
// seed >= 3 can reach Q-1=5 with at most 2 adds (max 2+2-0=4 < 5 for seed<=2).
// So: >=1 add in HT = empty cells on heavy T-curves (seed>=3) ∪ {U}; other add: any vacant cell.
// Checks: blockU -> safety (curves through adds) -> full maximality (blocker-avoidance fast path).
'use strict';
const S = require('./sat.js');

const W = 5, M = 23, Q = 6;
const SEED = [[0,0],[11,0],[15,0],[20,0],[3,1],[6,1],[10,1],[15,1],[18,1],[3,2],[6,2],[8,2],[10,2],[15,2],[4,3],[6,3],[9,3],[16,3],[17,3],[7,4],[9,4],[11,4],[12,4],[14,4]];

const t0 = Date.now();
const { P, n, curves } = S.buildCensus(W, M, Q);
const idx = (x, y) => y * M + x;
const occ = new Uint8Array(n);
for (const [x, y] of SEED) occ[idx(x, y)] = 1;
const NC = curves.length;
const seedCnt = new Int32Array(NC);
for (let ci = 0; ci < NC; ci++) { let c = 0; for (const p of curves[ci].pts) c += occ[p]; seedCnt[ci] = c; }
const through = Array.from({ length: n }, () => []);
curves.forEach((cu, ci) => { for (const p of cu.pts) through[p].push(ci); });
// membership matrix for O(1) curve-membership lookups
const mem = [];
for (let ci = 0; ci < NC; ci++) { const a = new Uint8Array(n); for (const p of curves[ci].pts) a[p] = 1; mem.push(a); }

// U and T-curves
let U = -1;
const emptyCells = [];
for (let i = 0; i < n; i++) { if (!occ[i]) emptyCells.push(i); else occ[i] = 1; }
for (const c of emptyCells) { let mx = 0; for (const ci of through[c]) if (seedCnt[ci] > mx) mx = seedCnt[ci]; if (mx < Q - 1) { if (U !== -1) throw new Error('two unblocked'); U = c; } }
if (U !== idx(22, 0)) throw new Error('U mismatch ' + U);
const Tcurves = through[U];
const heavy = Tcurves.filter(ci => seedCnt[ci] >= 3);
const HTset = new Set([U]);
for (const ci of heavy) for (const p of curves[ci].pts) if (!occ[p]) HTset.add(p);
const blockers = Array.from({ length: n }, () => []);
for (const c of emptyCells) for (const ci of through[c]) if (seedCnt[ci] >= Q - 1) blockers[c].push(ci);

const stones = SEED.map(([x, y]) => idx(x, y));
const HT = [...HTset];
console.log(JSON.stringify({ U: [U % M, Math.floor(U / M)], heavyT: heavy.length, heavyCounts: heavy.map(ci => seedCnt[ci]), htCandidates: HT.length }));

// full final-state check (used only for survivors of cheap filters)
function fullMaximal(o) {
  for (let c = 0; c < n; c++) {
    if (o[c]) continue;
    let blocked = false;
    for (const ci of through[c]) { let k = 0; for (const p of curves[ci].pts) k += o[p]; if (k >= Q - 1) { blocked = true; break; } }
    if (!blocked) return false;
  }
  return true;
}

let configs = 0, passedBlockU = 0, passedSafety = 0, witnesses = [];
for (let i1 = 0; i1 < stones.length; i1++) for (let i2 = i1 + 1; i2 < stones.length; i2++) {
  const s1 = stones[i1], s2 = stones[i2];
  // vacancy mask: cells addable = empty ∪ {s1,s2}
  const vacant = new Uint8Array(n);
  for (const c of emptyCells) vacant[c] = 1;
  vacant[s1] = 1; vacant[s2] = 1;
  for (const a1 of HT) {
    if (!vacant[a1]) continue;
    for (let a2 = 0; a2 < n; a2++) {
      if (a2 === a1 || !vacant[a2]) continue;
      // avoid double counting when both adds in HT: require a2 not in HT or a2 > a1
      if (HTset.has(a2) && a2 < a1) continue;
      configs++;
      // --- filter 1: U blocked or occupied ---
      const uOcc = (a1 === U || a2 === U);
      if (!uOcc) {
        let okU = false;
        for (const ci of Tcurves) {
          const c = seedCnt[ci] + mem[ci][a1] + mem[ci][a2] - mem[ci][s1] - mem[ci][s2];
          if (c >= Q - 1) { okU = true; break; }
        }
        if (!okU) continue;
      }
      passedBlockU++;
      // --- filter 2: safety (curves through adds) ---
      let safe = true;
      outer:
      for (const a of [a1, a2]) {
        for (const ci of through[a]) {
          const c = seedCnt[ci] + mem[ci][a1] + mem[ci][a2] - mem[ci][s1] - mem[ci][s2];
          if (c >= Q) { safe = false; break outer; }
        }
      }
      if (!safe) continue;
      passedSafety++;
      // --- filter 3: maximality ---
      const o = occ.slice(); o[s1] = 0; o[s2] = 0; o[a1] = 1; o[a2] = 1;
      if (fullMaximal(o)) {
        witnesses.push({ s1, s2, a1, a2 });
        console.log('2STONE WITNESS', JSON.stringify(witnesses[witnesses.length - 1]));
      }
    }
  }
}
console.log(JSON.stringify({ configs, passedBlockU, passedSafety, witnesses: witnesses.length, ms: Date.now() - t0 }));
