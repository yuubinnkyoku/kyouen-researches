// (4,4) four-row q=4 bounded-neighborhood witness engine, part 2 of the
// four-row q4 m35 witness-hunt-counting lane (see the part-1 experiment dir).
//
// Board: w=4 rows (y=0..3), m columns (x=0..m-1), q=4. Cells indexed
// idx = y*m + x. Curves = lines and circles through >= q grid cells, in the
// canonical exact-integer conventions validated by the part-1 fail-closed
// verifier (verify_counting_wq4_20261121.py):
//   - lines: primitive direction (a,b), b>0 or (a>0,b==0), each counted once;
//   - circles: rational circumcenter (na/d, nb/d) reduced with sign d>0,
//     membership rx=d*x-na, ry=d*y-nb, r2=rx^2+ry^2 (a circle = (na,nb,d,r2)).
//
// explorePlacement searches, per placement of a published witness base
// (m'-witness embedding: 4 reflections x all translations inside the board),
// all R-configs S-R with |R| <= 2 (DFS over base stones, each removal set
// visited exactly once) and ALL addition sets A with |A| <= 2 whose config
// S-R+A is a witness (safe, maximal, row-deficient, capped class alive) --
// including non-essential extensions of A0 witnesses, since maximality is
// preserved when adding safe stones. The brute battery in hunt_driver.js
// enumerates the same target set without pruning; the two must agree.
//
// Coverage completeness theorem (|A| <= 2; U = uncovered free cells of S-R,
// i.e. free cells not on any cnt==q-1 curve; n3[p]>0 means covered). A cell
// u in U ends up blocked in S-R+A iff
//   (a) a stone lands on u (self-cover / hole-filling), or
//   (b) some added stone lies on a cnt==q-2 curve through u (2+1 = q), or
//   (c) both added stones lie on a cnt==q-1 curve through u (1+2 = q).
// cnt==q-2 with both stones would make 4 on one curve (unsafe), cnt==q-1
// curves through u are excluded (u would be covered), cnt>=3 case needs no
// stone. Hence enumerating, per anchor u* with the smallest helper pool:
//   pool(u*) = A1(u*) (cells on cnt==q-2 curves through u*) 
//            + cells on cnt==q-1 curves through u* (pair partners)
//            + {u*} (self-cover)
// and iterating a1 over pool(u*), a2 over the per-u allowed-set
// intersection  A1(u) u partners(a1,u) u {u}  over u not already covered by
// a1 (or equal to a1), is complete: every witness pair has an element in
// pool(u*).
//
// Completeness target (supersedes any subsumption-based pruning). For one
// R-config the engine enumerates ALL witnesses S-R+A with |A| <= 2 (the
// battery's brute-force mode enumerates the same set without the helper
// machinery and the two witness SETS must be equal). The only prunes are
// provably-witness-impossible cases:
//   - a stone on a cnt==q-1 curve is unsafe in every extension (solo gate);
//   - a pair sharing a cnt==q-2 curve is unsafe (pair gate);
//   - if S-R+a1 has all rows >= 3, no further stone can re-deficient a row,
//     so pairs containing a cover-AlONE witness single a1 are only explored
//     with a2 arbitrary, and pairs containing a nondef single are skipped;
//   - U==empty R-configs are themselves maximal: singles/pairs enumerated
//     over all free cells (maximality is preserved by adding safe stones),
//     so that extended witnesses (supersets of an A0 witness) are found.
// The dead-R-config prune (some u uncoverable by any |A| <= 2) is also
// sound: u uncoverable now stays uncoverable in no deeper layer reached from
// the same R-config.
//
// Since a witness candidate must be safe, maximal, def, class-alive, and
// |stones| <= 13 (11-stone bases + 2 additions), every witness found is
// pushed only after full verifyConfig. Nothing here claims absence at any m:
// the output records which finite bounded neighborhoods were enumerated.

'use strict';

function gcd(a, b) {
  a = Math.abs(a); b = Math.abs(b);
  while (b) { const t = b; b = a % b; a = t; }
  return a;
}

// ----- census ---------------------------------------------------------

// returns { N, m, w, q, pts, curves (array of Int32Array cell idx lists),
//            cellCurves (per cell: Int32Array of curve indices, possibly
//            absent if a cell lies on no >=q curve), curveHas (per curve
//            Uint8Array cell membership), nTotal, nLines, nCircles }
function buildCensus(w, m, q) {
  const N = w * m;
  const pts = new Array(N);
  for (let y = 0; y < w; y++) for (let x = 0; x < m; x++) pts[y * m + x] = [x, y];
  const curves = [];
  // lines: canonical primitive direction, minimal board point first.
  // horizontals
  for (let y = 0; y < w; y++) {
    if (m >= q) { const arr = []; for (let x = 0; x < m; x++) arr.push(y * m + x); curves.push(arr); }
  }
  // verticals
  for (let x = 0; x < m; x++) {
    if (w >= q) { const arr = []; for (let y = 0; y < w; y++) arr.push(y * m + x); curves.push(arr); }
  }
  // slanted: direction (a,b), b>=1, gcd(|a|,b)=1, a != 0
  const countLine = (a, b) => {
    // lines with >= q points
    let n = 0;
    for (let x = 0; x < m; x++) for (let y = 0; y < w; y++) {
      if ((x - a >= 0 && x - a < m) && (y - b >= 0 && y - b < w)) continue; // not minimal
      const arr = [];
      let cx = x, cy = y;
      while (cx >= 0 && cx < m && cy >= 0 && cy < w) { arr.push(cy * m + cx); cx += a; cy += b; }
      if (arr.length >= q) { curves.push(arr); n++; }
    }
    return n;
  };
  for (let a = -(m - 1); a < m; a++) {
    if (a === 0) continue;
    for (let b = 1; b < w; b++) {
      if (gcd(Math.abs(a), b) !== 1) continue;
      if ((q - 1) * Math.abs(a) > m - 1 || (q - 1) * b > w - 1) continue;
      countLine(a, b);
    }
  }
  const nLines = curves.length;
  // circles: circumcenter (na/d, nb/d) from any point triple; reduced, sign d>0.
  // For each distinct center, bucket cells by scaled squared radius; each bucket
  // with >= q cells is one circle curve.
  const ssq = new Int32Array(N);
  for (let i = 0; i < N; i++) { const [x, y] = pts[i]; ssq[i] = x * x + y * y; }
  const centerMap = new Map(); // key na|nb|d -> { na, nb, d }
  for (let i = 0; i < N; i++) {
    const x1 = pts[i][0], y1 = pts[i][1], s1 = ssq[i];
    for (let j = i + 1; j < N; j++) {
      const x2 = pts[j][0], y2 = pts[j][1], s2 = ssq[j];
      for (let k = j + 1; k < N; k++) {
        const x3 = pts[k][0], y3 = pts[k][1], s3 = ssq[k];
        let d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2));
        if (d === 0) continue; // collinear
        let na = s1 * (y2 - y3) + s2 * (y3 - y1) + s3 * (y1 - y2);
        let nb = s1 * (x3 - x2) + s2 * (x1 - x3) + s3 * (x2 - x1);
        const g = gcd(gcd(na, nb), d) || 1;
        na = na / g; nb = nb / g; d = d / g; // exact: g divides each
        if (d < 0) { na = -na; nb = -nb; d = -d; }
        const key = na + '|' + nb + '|' + d;
        if (!centerMap.has(key)) centerMap.set(key, [na, nb, d]);
      }
    }
  }
  let nCircles = 0;
  for (const [key, c] of centerMap) {
    const [na, nb, dd] = c;
    const hist = new Map();
    for (let i = 0; i < N; i++) {
      const rx = dd * pts[i][0] - na, ry = dd * pts[i][1] - nb;
      const r2 = rx * rx + ry * ry;
      let bucket = hist.get(r2);
      if (!bucket) { bucket = []; hist.set(r2, bucket); }
      bucket.push(i);
    }
    for (const [r2, bucket] of hist) {
      if (bucket.length >= q) { curves.push(bucket); nCircles++; }
    }
  }
  // per-cell curve index lists (Int32Array), per-curve membership bitsets
  const perCell = new Array(N).fill(null);
  const counts = new Int32Array(N);
  for (let ci = 0; ci < curves.length; ci++) for (const p of curves[ci]) counts[p]++;
  for (let p = 0; p < N; p++) { if (counts[p] > 0) perCell[p] = new Int32Array(counts[p]); }
  const fill = new Int32Array(N);
  for (let ci = 0; ci < curves.length; ci++) for (const p of curves[ci]) perCell[p][fill[p]++] = ci;
  const curveHas = curves.map(arr => {
    const u = new Uint8Array(N);
    for (const p of arr) u[p] = 1;
    return u;
  });
  const curvesArr = curves.map(arr => Int32Array.from(arr));
  return {
    N, m, w, q, pts, curves: curvesArr, cellCurves: perCell, curveHas,
    nTotal: curves.length, nLines, nCircles
  };
}

// ----- full verification (independent of SearchState) -------------------

// verify a stone cell-index list against the census. Returns
// { ok, n, safe, maximal, deficient, rows, capped, any } where any is the
// conjunction safe & maximal & deficient (class filtering remains with the
// caller, who applied the alive-class gate on capped rows beforehand).
function verifyConfig(cens, stones) {
  const { N, w, m, q, cellCurves, nTotal, curves } = cens;
  const res = { ok: true, n: stones.length, safe: false, maximal: false, deficient: false, rows: [], capped: [], any: false };
  if (stones.length === 0) { res.ok = false; return res; }
  const occ = new Uint8Array(N);
  for (const p of stones) {
    if (p < 0 || p >= N || occ[p]) { res.ok = false; return res; }
    occ[p] = 1;
  }
  const rows = new Int32Array(w);
  for (const p of stones) rows[(p / m) | 0]++;
  res.rows = Array.from(rows);
  res.capped = Array.from(rows).map(r => Math.min(3, r)).sort((a, b) => a - b);
  // safety + coverage in one pass over the stones' curves
  const cnt = new Int32Array(nTotal);
  for (const p of stones) {
    const ccs = cellCurves[p];
    if (ccs) for (const c of ccs) cnt[c]++;
  }
  let safe = true;
  for (let c = 0; c < nTotal; c++) if (cnt[c] >= q) { safe = false; break; }
  res.safe = safe;
  if (!safe) return res;
  let maximal = true;
  for (let p = 0; p < N; p++) {
    if (occ[p]) continue;
    const ccs = cellCurves[p];
    let covered = false;
    if (ccs) for (const c of ccs) if (cnt[c] === q - 1) { covered = true; break; }
    if (!covered) { maximal = false; break; }
  }
  res.maximal = maximal;
  res.deficient = Array.from(rows).some(r => r <= 2);
  res.any = safe && maximal && res.deficient;
  return res;
}

// ----- placements -------------------------------------------------------

// the 4 reflections (w x m slab widths differ, rotations are not symmetries
// unless w == m; reflections suffice for embeddings used here)
const D4 = [
  ([x, y]) => [x, y],
  ([x, y]) => [-x, y],
  ([x, y]) => [x, -y],
  ([x, y]) => [-x, -y],
];

// all placements of a stone [[x,y],...] pattern into the w x m board:
// normalize the reflected pattern to its bounding box, then slide it.
// Returns [{ g, tx, ty, idxs, key }] with key a canonical string of sorted
// cell indices (dedup across g modes that coincide).
function placementsOfBase(cens, stonesXY) {
  const { m, w } = cens;
  const out = [];
  const seen = new Set();
  D4.forEach((f, gi) => {
    const pts = stonesXY.map(f);
    let minx = Infinity, maxx = -Infinity, miny = Infinity, maxy = -Infinity;
    for (const [x, y] of pts) {
      if (x < minx) minx = x; if (x > maxx) maxx = x;
      if (y < miny) miny = y; if (y > maxy) maxy = y;
    }
    const norm = pts.map(([x, y]) => [x - minx, y - miny]);
    const W = maxx - minx, H = maxy - miny;
    if (W >= m || H >= w) return;
    for (let ty = 0; ty + H < w; ty++) {
      for (let tx = 0; tx + W < m; tx++) {
        const idxs = norm.map(([x, y]) => ((y + ty) * m) + (x + tx));
        idxs.sort((a, b) => a - b);
        const key = idxs.join(',');
        if (seen.has(key)) continue;
        seen.add(key);
        out.push({ g: gi, tx, ty, idxs, key });
      }
    }
  });
  return out;
}

// ----- incremental search state ------------------------------------------

// maintained invariants: freeMask, rows, cnt (per-curve stone count), n3 (per
// free cell: number of curves through the cell with cnt == q-1), rLabel
// (cells removed so far in DFS order).
class SearchState {
  constructor(cens) {
    this.census = cens;
    this.reset();
  }
  reset() {
    const { N, w, nTotal } = this.census;
    this.freeMask = new Uint8Array(N); this.freeMask.fill(1);
    this.rows = new Int32Array(w);
    this.cnt = new Int32Array(nTotal);
    this.n3 = new Int32Array(N);
    this.stones = [];
    this.rLabel = [];
  }
  addStone(p) {
    const { cellCurves, curves, m } = this.census;
    this.freeMask[p] = 0; this.rows[(p / m) | 0]++;
    for (const c of cellCurves[p] || []) {
      if (++this.cnt[c] === this.census.q - 1) {
        for (const u of curves[c]) this.n3[u]++;
      }
    }
    this.stones.push(p);
  }
  removeStoneByValue(p) {
    const { cellCurves, curves, m } = this.census;
    // find the stone index in this.stones and splice it out
    const i = this.stones.indexOf(p);
    if (i < 0) throw new Error('removing non-stone cell');
    this.stones.splice(i, 1);
    this.freeMask[p] = 1; this.rows[(p / m) | 0]--;
    for (const c of cellCurves[p] || []) {
      if (this.cnt[c]-- === this.census.q - 1) {
        for (const u of curves[c]) this.n3[u]--;
      }
    }
  }
  addStoneUntracked(p) { this.addStone(p); }
}
// convenience alias used by benchmarks
function materialize(cens, cells) {
  const st = new SearchState(cens);
  for (const p of cells) st.addStone(p);
  return st;
}

// ----- the layered bounded-neighborhood enumeration -----------------------

// alive = { m: board m, alive: { '(..., ...)': B } } from the verified
// q=4 class table (part 1 captable_q4.json): class alive at threshold t
// iff B >= t (K1202 demand/supply inequality, proven input).
function explorePlacement(census, alive, st, cfg) {
  const { N, nTotal, curves, cellCurves, curveHas, q, m } = census;
  const res = {
    rConfigs: 0, d0Candidates: 0, singleCandidates: 0, pairCandidates: 0,
    d1Dead: 0, d2Dead: 0, prunedDef: 0, prunedClass: 0, prunedUnsafeSingle: 0,
    a0Singles: 0, maxU: 0, sumU: 0, selfSingles: 0, selfPairs: 0,
    witnesses: []
  };
  const Umark0 = new Uint8Array(N); // filled per R-config

  // class alive at this board's m iff B(class) >= m (sound prune: every
  // maximal safe row-deficient config on w x m satisfies m <= B(class))
  const classAlive = (cappedKey) => {
    const B = alive.alive[cappedKey];
    return B !== undefined && B >= alive.m;
  };
  const cappedKeyOf = (rowsNow) =>
    '(' + rowsNow.map(r => Math.min(3, r)).sort((a, b) => a - b).join(', ') + ')';
  // def && class-alive gate (cheap, pre-verify)
  const defClassOK = (rowsNow) => {
    let def = false;
    for (const r of rowsNow) if (r <= 2) { def = true; break; }
    if (!def) return false;
    return classAlive(cappedKeyOf(rowsNow));
  };
  const rowOf = (p) => (p / m) | 0;

  function exploreR(depth) {
    res.rConfigs++;
    const Umark = Umark0.fill(0);
    const U = [];
    for (let p = 0; p < N; p++) if (st.freeMask[p]) {
      if (st.n3[p] === 0) { U.push(p); Umark[p] = 1; }
    }
    const uSize = U.length;
    if (uSize > res.maxU) res.maxU = uSize;
    if (uSize > 0) res.sumU += uSize;
    res.d0Candidates += (uSize === 0 ? 1 : 0);
    const R = st.rLabel.slice();

    // solo safety memo for this R-config: a stone at a is unsafe in EVERY
    // extension of S-R by further stones containing it, iff a lies on a
    // cnt==q-1 curve of S-R.
    const soloSafeMemo = new Map();
    const isSoloSafe = (a) => {
      let v = soloSafeMemo.get(a);
      if (v === undefined) {
        v = true;
        const ccs = cellCurves[a];
        if (ccs) for (const c of ccs) if (st.cnt[c] === q - 1) { v = false; break; }
        soloSafeMemo.set(a, v);
      }
      return v;
    };
    // joint pair safety given both solo-safe: the only new danger is both
    // stones on one cnt==q-2 curve (cnt would reach q).
    const pairSafe = (a1, a2) => {
      const ccs = cellCurves[a1];
      if (ccs) for (const c of ccs) {
        if (st.cnt[c] === q - 2 && curveHas[c][a2]) return false;
      }
      return true;
    };
    const rowsWith = (...cells) => {
      const rn = st.rows.slice();
      for (const c of cells) rn[rowOf(c)]++;
      return rn;
    };
    const trySingle = (a, layerTag) => {
      res.singleCandidates++;
      const final = st.stones.slice(); final.push(a); final.sort((x, y) => x - y);
      const v = verifyConfig(census, final);
      if (v.any) res.witnesses.push({ layer: layerTag, R, A: [a], stones: final, v });
    };
    const tryPair = (a1, a2, layerTag) => {
      res.pairCandidates++;
      const final = st.stones.slice(); final.push(a1, a2); final.sort((x, y) => x - y);
      const v = verifyConfig(census, final);
      if (v.any) res.witnesses.push({ layer: layerTag, R, A: [a1, a2], stones: final, v });
    };

    if (uSize === 0) {
      // S-R is already maximal: A0 witness check, then singles/pairs over
      // all free cells (adding safe stones preserves maximality). This
      // catches extended witnesses (supersets of an A0 witness).
      if (defClassOK(st.rows)) {
        const v = verifyConfig(census, st.stones.slice());
        if (v.any) res.witnesses.push({ layer: 'A0', R, A: [], stones: st.stones.slice(), v });
      }
      const maxAdd = (cfg && cfg.maxAdd !== undefined) ? cfg.maxAdd : 2;
      if (maxAdd === 0) return;
      const freeCells = [];
      for (let p = 0; p < N; p++) if (st.freeMask[p] && isSoloSafe(p)) freeCells.push(p);
      for (const a of freeCells) {
        if (!defClassOK(rowsWith(a))) { res.prunedDef++; continue; }
        trySingle(a, 'A0+1');
      }
      if (maxAdd < 2) return;
      for (let i = 0; i < freeCells.length; i++) {
        const a1 = freeCells[i];
        for (let j = i + 1; j < freeCells.length; j++) {
          const a2 = freeCells[j];
          if (!pairSafe(a1, a2)) continue;
          if (!defClassOK(rowsWith(a1, a2))) { res.prunedDef++; continue; }
          tryPair(a1, a2, 'A0+2');
        }
      }
      return;
    }

    // ---- U != empty: helper sets from one pass over curves ----
    // A1: u -> free cells on cnt==q-2 curves through u (one such stone
    // covers u); P1: u -> cnt==1 (q-3) curves through u (both stones on one
    // such curve cover u).
    const UidxOf = new Int32Array(N).fill(-1);
    for (let i = 0; i < U.length; i++) UidxOf[U[i]] = i;
    const A1mark = new Map(), A1list = new Map(), P1 = new Map();
    for (let c = 0; c < nTotal; c++) {
      const k = st.cnt[c];
      const kind = (k === q - 2) ? 2 : (k === q - 3) ? 1 : 0;
      if (!kind) continue;
      const arr = curves[c];
      const us = [];
      for (const p of arr) { const ui = UidxOf[p]; if (ui >= 0) us.push(ui); }
      if (us.length === 0) continue;
      if (kind === 2) {
        for (const ui of us) if (!A1mark.has(ui)) { A1mark.set(ui, new Uint8Array(N)); A1list.set(ui, new Set()); }
        for (const p of arr) {
          if (!st.freeMask[p]) continue;
          for (const ui of us) { A1mark.get(ui)[p] = 1; A1list.get(ui).add(p); }
        }
      } else {
        for (const ui of us) { if (!P1.has(ui)) P1.set(ui, []); P1.get(ui).push(c); }
      }
    }
    // vote[p] = #{u in U : a stone at p covers u via a cnt==q-2 curve}
    const vote = new Int32Array(N);
    for (const [ui, mk] of A1mark) { for (let p = 0; p < N; p++) if (mk[p]) vote[p]++; }
    // coverExtra[u] = 1 iff a stone at u covers u itself and that was not
    // already counted in vote[u] (u on a cnt==q-2 curve through itself).
    const coverExtra = new Uint8Array(N);
    for (const u of U) {
      const mk = A1mark.get(UidxOf[u]);
      if (!mk || !mk[u]) coverExtra[u] = 1;
    }
    const coverAll = (a) => vote[a] + coverExtra[a] >= uSize;

    // dead-R-config prune: some u uncoverable by any |A| <= 2 (no A1, no P1,
    // self not even solo-safe).
    for (let i = 0; i < U.length; i++) {
      if (!A1mark.has(i) && !P1.has(i) && !isSoloSafe(U[i])) {
        if (depth === 0) res.d1Dead++; else res.d2Dead++;
        return;
      }
    }

    // ---- |A| = 1 ----
    for (let a = 0; a < N; a++) {
      if (!st.freeMask[a]) continue;
      if (!coverAll(a)) continue;
      res.selfSingles += Umark[a] ? 1 : 0;
      if (!isSoloSafe(a)) { res.prunedUnsafeSingle++; continue; }
      if (!defClassOK(rowsWith(a))) { res.prunedDef++; continue; }
      trySingle(a, 'A1');
    }

    // ---- |A| = 2 ----
    // anchor: u* = min pool size; pool(u*) = A1(u*) free cells + free cells
    // of P1(u*) curves + {u*}. Every witness pair has an element in it.
    let ustar = -1;
    {
      let best = Infinity;
      for (let i = 0; i < U.length; i++) {
        let sz = A1mark.has(i) ? A1list.get(i).size : 0;
        if (P1.has(i)) for (const c of P1.get(i)) for (const p of curves[c]) if (st.freeMask[p]) sz++;
        if (sz + 1 < best) { best = sz + 1; ustar = i; }
      }
    }
    const ustarPool = new Set();
    if (A1mark.has(ustar)) for (const p of A1list.get(ustar)) ustarPool.add(p);
    if (P1.has(ustar)) for (const c of P1.get(ustar)) for (const p of curves[c]) if (st.freeMask[p]) ustarPool.add(p);
    ustarPool.add(U[ustar]);

    const pairSeen = new Set();
    const maybePair = (a1, a2) => {
      if (a1 === a2) return;
      const lo = Math.min(a1, a2), hi = Math.max(a1, a2);
      const pk = lo * 8192 + hi;
      if (pairSeen.has(pk)) return;
      pairSeen.add(pk);
      res.selfPairs += (Umark[a1] || Umark[a2]) ? 1 : 0;
      if (!isSoloSafe(a2)) return;
      if (!pairSafe(a1, a2)) return;
      if (!defClassOK(rowsWith(a1, a2))) { res.prunedDef++; return; }
      tryPair(a1, a2, 'A2');
    };

    for (const a1 of ustarPool) {
      if (!isSoloSafe(a1)) continue;
      if (coverAll(a1)) {
        if (rowsWith(a1).every(r => r >= 3)) continue; // nondef single: pairs cannot witness
        if (defClassOK(rowsWith(a1))) {
          // single already a witness (or verifies to one); pairs containing
          // it may still be extended witnesses with a2 anywhere (complete:
          // maximality is preserved when adding safe stones).
          for (let a2 = 0; a2 < N; a2++) {
            if (!st.freeMask[a2] || a2 === a1) continue;
            maybePair(a1, a2);
          }
        } else {
          // capped(R)+capped(a1) class dead: adding a2 to a saturated row
          // keeps the capped profile dead; a2 confined to deficient rows.
          const rn = rowsWith(a1);
          for (let a2 = 0; a2 < N; a2++) {
            if (!st.freeMask[a2] || a2 === a1) continue;
            if (rn[rowOf(a2)] > 2) continue;
            maybePair(a1, a2);
          }
        }
      } else {
        // a1 does not cover U alone: a2 restricted per-u to
        // A1(u) u {u} u {free cells on P1(u) curves through a1}, for u not
        // already covered by a1 alone (or equal to a1).
        const allow = new Set();
        let feasible = true;
        for (const u of U) {
          if (u === a1) continue;
          const mk = A1mark.get(UidxOf[u]);
          if (mk && mk[a1]) continue;
          const here = new Set();
          if (mk) for (const p of A1list.get(UidxOf[u])) here.add(p);
          here.add(u);
          if (P1.has(UidxOf[u])) {
            for (const c of P1.get(UidxOf[u])) {
              if (!curveHas[c][a1]) continue;
              for (const p of curves[c]) if (st.freeMask[p] && p !== a1) here.add(p);
            }
          }
          here.delete(a1);
          if (here.size === 0) { feasible = false; break; }
          if (allow.size === 0) { for (const p of here) allow.add(p); }
          else { for (const p of [...allow]) if (!here.has(p)) allow.delete(p); }
          if (allow.size === 0) { feasible = false; break; }
        }
        if (!feasible) continue;
        for (const a2 of allow) maybePair(a1, a2);
      }
    }
  }

  const baseSorted = st.stones.slice().sort((a, b) => a - b);
  const nBase = baseSorted.length;
  const dfsR = (depth, minOi) => {
    exploreR(depth);
    if (depth === 2) return;
    for (let oi = minOi; oi < nBase; oi++) {
      const p = baseSorted[oi];
      st.removeStoneByValue(p);
      st.rLabel.push(p);
      dfsR(depth + 1, oi + 1);
      st.rLabel.pop();
      st.addStone(p);
    }
  };
  dfsR(0, 0);
  return res;
}
module.exports = { buildCensus, verifyConfig, placementsOfBase, SearchState, explorePlacement, materialize, D4, gcd };
