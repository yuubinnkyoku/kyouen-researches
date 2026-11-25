// extend6.js: deep-removal column-extension enumeration for deficient-maximal witnesses.
//
// Setting: known deficient-maximal safe witnesses ("bases") on w x baseM boards for a
// fixed (w,q). Target board w x targetM (targetM > baseM). A target witness W is searched
// among configurations of the form: (base shifted by off columns) minus (removal set R,
// |R| = r) plus (additions A among unblocked empty cells, |kept|+|A| <= w(q-1)-1).
//
// Completeness within this sub-space (proof sketch):
//  - Any config C on the target board whose symmetric difference with a shifted base B is
//    (R out, A in) with |R| <= rmax has: kept = B\R safe (subset of safe B), and every
//    stone of A lies on NO curve carrying q-1 kept stones (else C unsafe); so A can only
//    use cells that are empty and unblocked w.r.t. kept. Conversely every A over those
//    cells is enumerated, and each candidate is fully verified (safe+maximal) by the
//    census-free verifier. Additions inside the base footprint equal smaller removals
//    (covered by smaller r), so restricting A to unblocked cells loses nothing.
//  - off ranges over 0..targetM-baseM (all horizontal placements).
//
// Efficiency: blocking/safety both use the >= q-point curve census of the target board.
// Removal DFS maintains per-curve kept counts and per-cell blocked-counts incrementally.
// Per removal leaf, cells in U (empty, unblocked) get bucket lists Mk = curves with
// kept-count q-1-k; A is enumerated as a combination DFS over U and blocked(u) is checked
// with precomputed U-masks of curves (popcount of AND). Candidates passing the fast
// filters get a full census-free verifyConfig. Witnesses print to stdout and append to OUT.
//
// Usage: node extend6.js w q baseM targetM rmin rmax [offmin offmax]
// Output: one JSON line per (base,off): {task, stats, witnesses}; found witnesses on stdout.
'use strict';
const fs = require('fs');
const path = require('path');
// Configurable paths (repo layout defaults):
//   EXT6_ROOT  experiment root (default: parent of this scripts/ dir)
//   EXT6_SATJS row_deficient_sat.js (K0810) providing pts/buildCensus/verifyConfig
//   EXT6_WITS  witness-pool dir with base witnesses
//   EXT6_OUT   output dir for raw task/witness JSONL
const ROOT = process.env.EXT6_ROOT || path.resolve(__dirname, '..');
const SATJS = process.env.EXT6_SATJS || path.resolve(ROOT, '../row-deficient-sat-witnesses-20261114/scripts/row_deficient_sat.js');
const WITDIR = process.env.EXT6_WITS || path.join(ROOT, 'witness-pool');
const OUTDIR = process.env.EXT6_OUT || path.join(ROOT, 'output');
const { pts, buildCensus, verifyConfig } = require(SATJS);

const [w, q, baseM, targetM, rmin, rmax, offminArg, offmaxArg] = process.argv.slice(2).map(Number);
const offmin = offminArg || 0, offmax = (offmaxArg != null ? offmaxArg : targetM - baseM);
const capDef = w * (q - 1) - 1; // deficient at targetM <=> |S| <= capDef

// ---- pool ----
const pool = [];
function addBase(m, st, src) {
  const key = m + '|' + st.map(s => s.join(',')).sort().join(';');
  for (const p of pool) if (p.key === key) return;
  pool.push({ m, st, key, src });
}
for (const f of ['sa3', 'sae', 'found']) {
  let txt; try { txt = fs.readFileSync(WITDIR + '/' + f + '.jsonl', 'utf8'); } catch (e) { continue; }
  for (const line of txt.split('\n')) {
    if (!line.trim()) continue;
    let d; try { d = JSON.parse(line); } catch (e) { continue; }
    const st = d.witness || d.stones;
    if (!st || !d.witness) continue;
    if (d.w === w && d.q === q && d.m === baseM) addBase(d.m, st, f);
  }
}
for (const d of JSON.parse(fs.readFileSync(WITDIR + '/extended.json', 'utf8'))) {
  if (d.w === w && d.q === q && d.toM === baseM) addBase(d.toM, d.stones, 'extended');
}
for (const f of ['w67_20', 'w68_18', 'w56_20', 'w56_21']) {
  try {
    const d = JSON.parse(fs.readFileSync(WITDIR + '/' + f + '.json', 'utf8'));
    if (d.w === w && d.q === q && d.m === baseM) addBase(d.m, d.stones, f);
  } catch (e) {}
}
if (!pool.length) { console.error('no bases for ' + w + 'x' + baseM + ' q=' + q); process.exit(1); }
console.error('bases: ' + pool.map(p => p.m + 'x' + p.st.length + '(' + p.src + ')').join(' '));

// ---- target census (curves with >= q points) ----
const P = pts(w, targetM); const N = P.length;
const { curves } = buildCensus(w, targetM, q);
const NC = curves.length;
const cuPts = curves.map(c => c.pts);
const cellThrough = Array.from({ length: N }, () => []);
for (let ci = 0; ci < NC; ci++) for (const p of cuPts[ci]) cellThrough[p].push(ci);

const OUT = path.join(OUTDIR, 'extend6_' + w + 'x' + targetM + 'q' + q + '_from' + baseM + '.jsonl');
const results = [];
let globalStats = { leaves: 0, subsets: 0, candPass: 0, verifyPass: 0, witnesses: 0 };

for (const base of pool) {
  const nSt = base.st.length;
  for (let off = offmin; off <= offmax; off++) {
    const stoneCells = base.st.map(([x, y]) => y * targetM + (x + off));
    const keptMask = new Uint8Array(N);
    for (const c of stoneCells) keptMask[c] = 1;
    const curveCnt = new Int32Array(NC);
    const blockedCnt = new Int32Array(N);
    for (let ci = 0; ci < NC; ci++) {
      let cnt = 0; for (const p of cuPts[ci]) if (keptMask[p]) cnt++;
      curveCnt[ci] = cnt;
      if (cnt >= q - 1) for (const p of cuPts[ci]) blockedCnt[p]++;
    }
    const task = { w, q, baseM, targetM, off, rmin, rmax, base: baseM + 'x' + nSt, capDef };
    let taskStats = { leaves: 0, subsets: 0, candPass: 0, verifyPass: 0, uOverflow: 0 };
    const witnesses = [];

    function emitCandidate(keptCells, A) {
      globalStats.candPass++;
      taskStats.candPass++;
      const cells = keptCells.concat(A);
      const stones = cells.map(c => [c % targetM, Math.floor(c / targetM)]);
      const v = verifyConfig(w, targetM, q, stones);
      if (v.ok && stones.length <= capDef) {
        taskStats.verifyPass++; globalStats.verifyPass++;
        const rec = { w, q, m: targetM, size: stones.length, rows: v.rows, base: base.m + 'x' + base.st.length, off, rem: nSt - keptCells.length, add: A.length, stones, verify: 'js-censusfree-PASS' };
        witnesses.push(rec); globalStats.witnesses++;
        fs.appendFileSync(OUT, JSON.stringify({ witness: rec }) + '\n');
        console.log('WITNESS ' + JSON.stringify(rec));
      }
    }

    function leaf() {
      taskStats.leaves++;
      const keptCells = [];
      for (let i = 0; i < nSt; i++) if (keptMask[stoneCells[i]]) keptCells.push(stoneCells[i]);
      const budget = capDef - keptCells.length;
      if (budget < 0) return;
      const U = [];
      for (let c = 0; c < N; c++) if (!keptMask[c] && blockedCnt[c] === 0) U.push(c);
      const u = U.length;
      if (u === 0) { emitCandidate(keptCells, []); return; }
      // buckets per U cell: Mk = curves needing k adds to block (cnt == q-1-k), k=1..6
      const M1 = [], M2 = [], M3 = [], M4 = [], M5 = [], M6 = [];
      const uIdx = new Int32Array(N).fill(-1);
      for (let i = 0; i < u; i++) uIdx[U[i]] = i;
      const pop16 = new Uint8Array(1 << 16);
      for (let x = 1; x < (1 << 16); x++) pop16[x] = pop16[x >> 1] + (x & 1);
      const popc = (x) => pop16[x & 0xFFFF] + pop16[(x >> 16) & 0xFFFF];
      const maskCache = new Map();
      const umaskOf = (ci) => { let m = maskCache.get(ci); if (m === undefined) { m = 0; for (const p of cuPts[ci]) { const ui = uIdx[p]; if (ui >= 0) m |= (1 << ui); } maskCache.set(ci, m); } return m; };
      for (let i = 0; i < u; i++) {
        const c = U[i]; M1.push([]); M2.push([]); M3.push([]); M4.push([]); M5.push([]); M6.push([]);
        for (const ci of cellThrough[c]) {
          const k = q - 1 - curveCnt[ci];
          if (k === 1) M1[i].push(ci);
          else if (k === 2) M2[i].push(ci);
          else if (k === 3) M3[i].push(ci);
          else if (k === 4) M4[i].push(ci);
          else if (k === 5) M5[i].push(ci);
          else if (k === 6) M6[i].push(ci);
        }
      }
      // danger curves per U cell for safety: cnt >= q-2
      const D = [];
      for (let i = 0; i < u; i++) {
        const c = U[i]; const dl = [];
        for (const ci of cellThrough[c]) if (curveCnt[ci] >= q - 2) dl.push(ci);
        D.push(dl);
      }
      const maxA = Math.min(budget, u);
      if (maxA > 6 || u > 24) { taskStats.uOverflow++; return; } // documented incomplete skip
      const chosen = [];
      let am = 0;
      function cand() {
        taskStats.subsets++;
        for (let ii = 0; ii < chosen.length; ii++) {
          const i = chosen[ii];
          for (const ci of D[i]) {
            if (curveCnt[ci] + popc(umaskOf(ci) & am) >= q) return;
          }
        }
        for (let i = 0; i < u; i++) {
          if ((am >> i) & 1) continue;
          let blocked = false;
          for (const ci of M1[i]) { if (umaskOf(ci) & am) { blocked = true; break; } }
          if (!blocked) for (const ci of M2[i]) { if (popc(umaskOf(ci) & am) >= 2) { blocked = true; break; } }
          if (!blocked) for (const ci of M3[i]) { if (popc(umaskOf(ci) & am) >= 3) { blocked = true; break; } }
          if (!blocked) for (const ci of M4[i]) { if (popc(umaskOf(ci) & am) >= 4) { blocked = true; break; } }
          if (!blocked) for (const ci of M5[i]) { if (popc(umaskOf(ci) & am) >= 5) { blocked = true; break; } }
          if (!blocked) for (const ci of M6[i]) { if (popc(umaskOf(ci) & am) >= 6) { blocked = true; break; } }
          if (!blocked) return;
        }
        const A = []; for (let i = 0; i < u; i++) if ((am >> i) & 1) A.push(U[i]);
        emitCandidate(keptCells, A);
      }
      function combos(start) {
        cand();
        if (chosen.length === maxA) return;
        for (let i = start; i < u; i++) {
          chosen.push(i); am |= (1 << i);
          combos(i + 1);
          chosen.pop(); am &= ~(1 << i);
        }
      }
      combos(0);
    }

    // removal DFS
    function dfs(startIdx, depth) {
      if (depth >= rmin && depth <= rmax) leaf();
      if (depth === rmax) return;
      for (let i = startIdx; i < nSt; i++) {
        const s = stoneCells[i];
        keptMask[s] = 0;
        const touched = cellThrough[s];
        for (const ci of touched) { if (--curveCnt[ci] === q - 2) for (const p of cuPts[ci]) blockedCnt[p]--; }
        dfs(i + 1, depth + 1);
        keptMask[s] = 1;
        for (const ci of touched) { if (++curveCnt[ci] === q - 1) for (const p of cuPts[ci]) blockedCnt[p]++; }
      }
    }
    dfs(0, 0);
    const line = { task, stats: taskStats, witnesses: witnesses.length };
    results.push(line);
    fs.appendFileSync(OUT, JSON.stringify({ taskLine: line }) + '\n');
    console.log(JSON.stringify(line));
  }
}
console.log(JSON.stringify({ global: globalStats }));
