// Restricted 3-for-3 replacement enumeration for 7-row q=4 deficient-maximal witnesses.
// Exactly 3 removals + 3 additions, final shape exactly [3,3,3,3,3,3,2],
// addition cells confined to window columns x >= xMin. Complete within (base, window).
// Modes:
//   fresh (default): additions must be cells not occupied by the base (hole refills forbidden).
//   holes (control): additions may additionally reuse the cells of the 3 removed stones
//                    (per removal triple), enabling known-answer controls.
// Safety (complete case split for additions A within window):
//   {1 add + 3 kept}: badT with removal skip mask
//   {2 add + 2 kept}: badP (fresh-only records in fresh mode; all-cell records in holes mode)
//   {3 add + 1 kept}: direct 4x4 determinant (no unbounded curve cache growth)
//   {4 kept}: base safety precondition (thrown on unsafe base)
// Maximality (complete case split for deficient-row empty cell u; coverage targets include
//   removed base cells - coverBy records ALL u targets, unlike pinned fresh-mode enum_two):
//   {3 kept}: remBlocked    {1 add + 2 kept}: coverBy with skip
//   {2 add + 1 kept}: key3 query    {3 add}: direct determinant
// Exact integer geometry only (Board reused verbatim from pinned enum_two.js).
'use strict';
const { Board } = require('./enum_two.js');

function f4(ax, ay, bx2, by2, cx, cy, dx, dy) {
  const ux = bx2 - ax, uy = by2 - ay;
  const az = bx2 * bx2 + by2 * by2 - ax * ax - ay * ay;
  const vx = cx - ax, vy = cy - ay, vz = cx * cx + cy * cy - ax * ax - ay * ay;
  const wx = dx - ax, wy = dy - ay, wz = dx * dx + dy * dy - ax * ax - ay * ay;
  return ux * (vy * wz - vz * wy) - uy * (vx * wz - vz * wx) + az * (vx * wy - vy * wx) === 0;
}

function runThree(board, base, opts) {
  opts = opts || {};
  const W = board.W, N = board.N, C = N, n = 20;
  const holes = !!opts.holes, xMin = opts.xMin | 0;
  const maxWit = (opts.maxWitnesses | 0) || 256;
  const budgetMs = Math.max(0, opts.budgetMs | 0);
  const startTs = Date.now();
  const occ = new Uint8Array(C), baseRows = new Int32Array(8);
  for (const [x, y] of base) { if (x < 0 || x >= W || y < 0 || y >= 7 || occ[x + W * y]) throw new Error('invalid base'); occ[x + W * y] = 1; baseRows[y]++; }
  for (let y = 0; y < 7; y++) if (baseRows[y] > 3) throw new Error('row capacity');
  const bx = new Int32Array(n), by = new Int32Array(n);
  base.forEach((p, i) => { bx[i] = p[0]; by[i] = p[1]; });
  for (let a = 0; a < n; a++) for (let b = a + 1; b < n; b++) for (let c = b + 1; c < n; c++) for (let d = c + 1; d < n; d++)
    if (f4(bx[a], by[a], bx[b], by[b], bx[c], by[c], bx[d], by[d])) throw new Error('unsafe base');
  // badT: for every cell, base triples whose curve passes it (needed fresh AND holes).
  const badT = new Array(C); for (let i = 0; i < C; i++) badT[i] = [];
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) for (let k = j + 1; k < n; k++) {
    const pts = board.key3(bx[i], by[i], bx[j], by[j], bx[k], by[k]);
    const pk = i * 400 + j * 20 + k;
    for (const u of pts) badT[u].push(pk);
  }
  // badP: pair safety records. coverBy: coverage records (u0 -> any target u, always).
  const badP = new Map(), coverBy = new Map();
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
    const pk = i * 20 + j;
    for (let u0 = 0; u0 < C; u0++) {
      if (occ[u0] && !holes) continue; // u0 must be a possible addition (fresh, or any cell in holes mode)
      const px = u0 % W, py = (u0 / W) | 0;
      const pts = board.key3(px, py, bx[i], by[i], bx[j], by[j]);
      for (const u of pts) {
        if (u === u0) continue;
        const ck = u0 * 1024 + u;
        let ca = coverBy.get(ck); if (!ca) { ca = []; coverBy.set(ck, ca); } ca.push(pk);
        if (occ[u] && !holes) continue; // badP partner must be fresh in fresh mode
        const kk = u0 < u ? u0 * 1024 + u : u * 1024 + u0;
        let arr = badP.get(kk); if (!arr) { arr = []; badP.set(kk, arr); } arr.push(pk);
      }
    }
  }
  const skip = new Uint8Array(n);
  const single = (u) => { const L = badT[u]; for (let t = 0; t < L.length; t++) { const pk = L[t], i = (pk / 400) | 0, rest = pk % 400, j = (rest / 20) | 0, k = rest % 20; if (!skip[i] && !skip[j] && !skip[k]) return false; } return true; };
  const pairOK = (u, v) => { const kk = u < v ? u * 1024 + v : v * 1024 + u; const L = badP.get(kk); if (!L) return true; for (let t = 0; t < L.length; t++) { const pk = L[t], i = (pk / 20) | 0, j = pk % 20; if (!skip[i] && !skip[j]) return false; } return true; };
  const covU = (p, u) => { const L = coverBy.get(p * 1024 + u); if (!L) return false; for (let t = 0; t < L.length; t++) { const pk = L[t], i = (pk / 20) | 0, j = pk % 20; if (!skip[i] && !skip[j]) return true; } return false; };
  let triplesExamined = 0, safeTriples = 0, shapeFails = 0, maximal = 0, removalsProcessed = 0, genCounter = 0;
  const witnesses = [];
  const stamp = new Int32Array(N + W); // [0..N): curve coverage per gen; [N..N+W): deficient-row stone columns
  const ord = []; for (let x = W - 1; x >= 0; x--) ord.push(x);
  const kept = [];
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) for (let k = j + 1; k < n; k++) {
    if (budgetMs && Date.now() - startTs > budgetMs) return { timed_out: true, removal_triples_processed: removalsProcessed };
    skip.fill(0); skip[i] = 1; skip[j] = 1; skip[k] = 1;
    kept.length = 0; for (let z = 0; z < n; z++) if (!skip[z]) kept.push(z);
    const rc2 = new Int32Array(8); for (let y = 0; y < 8; y++) rc2[y] = baseRows[y]; rc2[by[i]]--; rc2[by[j]]--; rc2[by[k]]--;
    const rowsAvail = []; for (let y = 0; y < 7; y++) if (rc2[y] < 3) rowsAvail.push(y);
    if (rowsAvail.length === 0) { removalsProcessed++; continue; }
    const remBlocked = new Uint8Array(N);
    for (let a = 0; a < 17; a++) for (let b = a + 1; b < 17; b++) for (let c = b + 1; c < 17; c++) {
      const pts = board.key3(bx[kept[a]], by[kept[a]], bx[kept[b]], by[kept[b]], bx[kept[c]], by[kept[c]]);
      for (const u of pts) remBlocked[u] = 1;
    }
    const avail = [];
    for (const y of rowsAvail) { for (let x = xMin; x < W; x++) { const u = x + W * y; if (!occ[u]) avail.push(u); } }
    if (holes) { for (const t of [i, j, k]) { if (bx[t] >= xMin) avail.push(bx[t] + W * by[t]); } }
    const sA = []; for (const u of avail) if (single(u)) sA.push(u);
    const ax = sA.map(u => u % W), ay = sA.map(u => (u / W) | 0);
    const pairs = [];
    for (let a = 0; a < sA.length; a++) for (let b = a + 1; b < sA.length; b++) {
      if (ay[a] === ay[b] && rc2[ay[a]] > 1) continue;
      if (pairOK(sA[a], sA[b])) pairs.push(a * 1024 + b);
    }
    for (const ab of pairs) {
      const a = (ab / 1024) | 0, b = ab % 1024;
      const u1 = sA[a], u2 = sA[b];
      for (let c = b + 1; c < sA.length; c++) {
        const cyr = ay[c];
        if (cyr === ay[a] && rc2[cyr] > 1) continue;
        if (cyr === ay[b] && rc2[cyr] > 1) continue;
        triplesExamined++;
        const u3 = sA[c];
        if (!pairOK(u1, u3)) continue;
        if (!pairOK(u2, u3)) continue;
        const x1 = ax[a], y1 = ay[a], x2 = ax[b], y2 = ay[b], x3 = ax[c], y3 = cyr;
        let bad = false;
        for (const z of kept) { if (f4(x1, y1, x2, y2, x3, y3, bx[z], by[z])) { bad = true; break; } }
        if (bad) continue;
        safeTriples++;
        const counts = new Int32Array(8);
        for (const z of kept) counts[by[z]]++;
        counts[y1]++; counts[y2]++; counts[y3]++;
        let y0 = -1, shape = true;
        for (let y = 0; y < 7; y++) { if (counts[y] > 3 || counts[y] < 2) shape = false; if (counts[y] === 2) { if (y0 !== -1) { shape = false; break; } y0 = y; } }
        if (!shape || y0 < 0 || counts[y0] !== 2) { shapeFails++; continue; }
        // maximality over deficient row y0 (kept 17 + 3 additions = 20 stones).
        // Mark each covering curve exactly once per candidate, then scan the row.
        genCounter++;
        const g = genCounter;
        if (y1 === y0) stamp[N + x1] = g;
        if (y2 === y0) stamp[N + x2] = g;
        if (y3 === y0) stamp[N + x3] = g;
        for (const z of kept) if (by[z] === y0) stamp[N + bx[z]] = g;
        const ax2 = [x1, x2, x3], ay2 = [y1, y2, y3];
        const mark = (pts) => { for (let t = 0; t < pts.length; t++) stamp[pts[t]] = g; };
        // {3 additions} curve (circle or line) through all three additions
        mark(board.key3(ax2[0], ay2[0], ax2[1], ay2[1], ax2[2], ay2[2]));
        // {2 additions + 1 kept}: three addition pairs x each kept stone
        for (let e = 0; e < 3; e++) for (let f = e + 1; f < 3; f++) {
          for (const z of kept) mark(board.key3(ax2[e], ay2[e], ax2[f], ay2[f], bx[z], by[z]));
        }
        const addU1 = u1, addU2 = u2, addU3 = u3;
        let failX = -1;
        for (const x of ord) {
          const u = x + W * y0;
          if (stamp[N + x] === g) continue;
          if (remBlocked[u] || stamp[u] === g) continue;
          // {1 addition + 2 kept} coverage records
          if (covU(addU1, u) || covU(addU2, u) || covU(addU3, u)) continue;
          failX = x; break;
        }
        if (failX === -1) {
          maximal++;
          if (witnesses.length < maxWit) {
            const cand = kept.map(z => [bx[z], by[z]]);
            cand.push([x1, y1], [x2, y2], [x3, y3]);
            cand.sort((p, q) => p[0] - q[0] || p[1] - q[1]);
            witnesses.push(cand);
          }
        }
      }
    }
    removalsProcessed++;
  }
  return {
    width: W, xMin, mode: holes ? 'holes' : 'fresh',
    removal_triples_total: (n * (n - 1) * (n - 2)) / 6, removal_triples_processed: removalsProcessed,
    triples_examined: triplesExamined, safe_triples: safeTriples, shape_fails: shapeFails,
    safe_maximal_row_deficient: maximal, witnesses, ms: Date.now() - startTs, timed_out: false
  };
}

// Independent brute-force verifier (no skip masks, no incremental caches).
// Re-checks: board bounds, row shape [3,3,3,3,3,3,2], 4-point safety by direct determinant,
// and deficient-row maximality by enumerating all C(20,3) stone triples' curves.
function bruteVerify(board, stones) {
  const W = board.W, N = board.N, n = stones.length;
  const occ = new Uint8Array(N); const rows = new Int32Array(8);
  const out = { n, safe: true, shape_ok: false, maximal: false, deficient_rows: [], issues: [] };
  for (const [x, y] of stones) {
    if (x < 0 || x >= W || y < 0 || y >= 7) { out.issues.push('out of board: ' + x + ',' + y); out.safe = false; return out; }
    if (occ[x + W * y]) { out.issues.push('duplicate: ' + x + ',' + y); out.safe = false; return out; }
    occ[x + W * y] = 1; rows[y]++;
  }
  if (n !== 20) { out.issues.push('n=' + n + ' != 20'); out.safe = false; return out; }
  for (let a = 0; a < n; a++) for (let b = a + 1; b < n; b++) for (let c = b + 1; c < n; c++) for (let d = c + 1; d < n; d++)
    if (f4(stones[a][0], stones[a][1], stones[b][0], stones[b][1], stones[c][0], stones[c][1], stones[d][0], stones[d][1])) {
      out.safe = false; out.issues.push('concyclic4: ' + JSON.stringify([stones[a], stones[b], stones[c], stones[d]])); return out;
    }
  let y0 = -1, shape = true;
  for (let y = 0; y < 7; y++) { if (rows[y] > 3) shape = false; if (rows[y] === 2) { if (y0 !== -1) shape = false; else y0 = y; } else if (rows[y] !== 3) shape = false; }
  out.shape_ok = shape && countsAllRows(rows);
  if (!out.shape_ok) { out.issues.push('bad shape'); return out; }
  out.deficient_rows = [y0];
  const covered = new Uint8Array(N);
  for (let a = 0; a < n; a++) for (let b = a + 1; b < n; b++) for (let c = b + 1; c < n; c++) {
    const pts = board.key3(stones[a][0], stones[a][1], stones[b][0], stones[b][1], stones[c][0], stones[c][1]);
    for (const u of pts) covered[u] = 1;
  }
  for (let x = 0; x < W; x++) { const u = x + W * y0; if (!occ[u] && !covered[u]) { out.issues.push('uncovered deficient-cell x=' + x + ' row=' + y0); return out; } }
  out.maximal = true;
  return out;
}
function countsAllRows(rows) { for (let y = 0; y < 7; y++) if (rows[y] !== 2 && rows[y] !== 3) return false; return true; }

module.exports = { Board, runThree, f4, bruteVerify };
