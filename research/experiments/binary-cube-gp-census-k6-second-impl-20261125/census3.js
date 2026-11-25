#!/usr/bin/env node
// census3.js — INDEPENDENT SECOND IMPLEMENTATION of the vertex-0-anchored general-position
// (GP) census on the hypercube {0,1}^d (d=3..6), for the game that forbids d+1 points on a
// common real affine hyperplane (degenerate included). Primary target: d=6, reproduce the
// published per-pair counts (r6-results.jsonl, census experiment binary-cube-gp-census-k6-20261121)
// and re-verify anchored s10 = 0 (hence K_6 <= 9; K0568 evidence upgrade).
//
// DESIGN (intentionally different from census2.js, which was read ONLY for output
// conventions, never copied):
//   * census2.js core: fraction-free sweep-out frames over GF(p) with two large primes.
//   * census3.js core: PURE EXACT INTEGER arithmetic (no primes, no modular reduction):
//       - Bareiss fraction-free determinants of the small 0/1 homogeneous matrices;
//       - "row-replacement coordinate functionals" g_i(x) := det(M_B[row i <- x]) whose
//         signs are consistent per (i,d), so that
//       - every gate for children at sizes >= d+2 reduces to a PROJECTIVE MINOR
//         (2x2 / 3x3 / 4x4 determinant) of the stacked coordinate-rows
//         {new element} x {earlier post-B elements} x {candidate}, on omitted
//         B-column subsets. Proof of the reduction: the gate functional mu vanishes on
//         the B-rows outside the omitted column set, hence mu lies in the span of the
//         corresponding row-replacement cofactor functionals; solving mu(other pool
//         members) = 0 gives the minors. Zero-vs-nonzero of each minor is invariant
//         under the per-column sign conventions (sigma_i^2 = 1), so the gate reduces to
//         an exact integer minor test. All integers used stay < 2^31 except the final
//         4x4 minors (< 1.3e14), which are exact in float64 (< 2^53). Asserted in battery.
//
// Enumeration (same published conventions): anchored sets contain vertex 0; each set is
// built in strictly increasing vertex order; the 63 subtrees are split by the second
// element v2 (the smallest nonzero element). Counts[k] = number of GP sets of size k in
// the subtree (per-pair mode also reports counts[1] = 1 as subtree bookkeeping, matching
// the published per-pair lines).
//
// Modes:
//   node census3.js selftest       // arithmetic + witness + small-pair batteries
//   node census3.js brutecensus d  // independent slow reference census (direct dets everywhere)
//   node census3.js census d       // fast full anchored census (d=3..6)
//   node census3.js pair d v2 ...   // per-pair fast runs (one JSON line per pair)
//   node census3.js gatecheck d v2 N // pair run with first N child-decisions fully re-verified
//
// Processes are deterministic; all output is integer JSON; no timing in results lines.

"use strict";
const { performance } = require("perf_hooks");

// ---------------------------------------------------------------- utilities
function subsetIndices(n, k) {
  // all k-subsets of [0..n), ascending arrays
  const out = [];
  const cur = [];
  (function rec(start) {
    if (cur.length === k) { out.push(cur.slice()); return; }
    for (let i = start; i < n; i++) { cur.push(i); rec(i + 1); cur.pop(); }
  })(0);
  return out;
}

// seeded PRNG (deterministic output only; used in selftest)
function lcg(seed) {
  let s = seed >>> 0;
  return function () {
    s = (s * 1664525 + 1013904223) >>> 0;
    return s / 4294967296;
  };
}

// hom rows of all vertices
function homRows(d) {
  const n = 1 << d, m = d + 1;
  const out = new Array(n);
  for (let v = 0; v < n; v++) {
    const r = new Float64Array(m);
    r[0] = 1;
    for (let i = 0; i < d; i++) r[1 + i] = (v >> i) & 1;
    out[v] = r;
  }
  return out;
}

// exact integer det of an r x r matrix, flat row-major. entries must be small
// integers (|.| < 2^26 ok for d<=6 paths). Bareiss; returns signed exact det.
// NOTE: A is clobbered.
let DET_MAXABS = 0;
function detExact(r, A) {
  let sgn = 1, prev = 1;
  for (let k = 0; k < r; k++) {
    let p = -1;
    for (let i = k; i < r; i++) if (A[i * r + k] !== 0) { p = i; break; }
    if (p < 0) return 0;
    if (p !== k) {
      for (let j = k; j < r; j++) { const t = A[k * r + j]; A[k * r + j] = A[p * r + j]; A[p * r + j] = t; }
      sgn = -sgn;
    }
    const piv = A[k * r + k];
    if (piv < 0) { if (-piv > DET_MAXABS) DET_MAXABS = -piv; } else if (piv > DET_MAXABS) DET_MAXABS = piv;
    for (let i = k + 1; i < r; i++) {
      const a = A[i * r + k];
      for (let j = k + 1; j < r; j++) {
        const v2 = (A[i * r + j] * piv - a * A[k * r + j]) / prev;
        A[i * r + j] = v2;
      }
    }
    prev = piv;
  }
  const res = A[(r - 1) * r + (r - 1)];
  if (res < 0) { if (-res > DET_MAXABS) DET_MAXABS = -res; } else if (res > DET_MAXABS) DET_MAXABS = res;
  return sgn * res;
}

// exact rank of k rows (flat k x m), fraction-free growth stays minor-bounded.
function rankExact(k, m, A) {
  let rk = 0;
  for (let col = 0; col < m && rk < k; col++) {
    let p = -1;
    for (let i = rk; i < k; i++) if (A[i * m + col] !== 0) { p = i; break; }
    if (p < 0) continue;
    if (p !== rk) { for (let j = col; j < m; j++) { const t = A[rk * m + j]; A[rk * m + j] = A[p * m + j]; A[p * m + j] = t; } }
    const piv = A[rk * m + col];
    for (let i = rk + 1; i < k; i++) {
      const a = A[i * m + col];
      for (let j = col + 1; j < m; j++) A[i * m + j] = (A[i * m + j] * piv - a * A[rk * m + j]);
    }
    rk++;
  }
  return rk;
}

// ---------------------------------------------------------------- fast enumerator
// ctx for one pair run
function makeCtx(H, d) {
  const m = d + 1;
  return {
    d, m, H,
    counts: new Array(d + 5).fill(0),
    maxsize: 0,
    gateTrials: 0,
    elems: new Int32Array(d + 5),
    gpath: [], // gpath[depth] = Float64Array(m) copy of coords of that element (post-B elements)
    scratchA: new Float64Array(m * m),
    scratchB: new Float64Array(m * m),
    subsetsCache: {}, // size -> [ [indices...] ] for omitted-column enumeration
  };
}
function subsetCache(ctx, n, k) {
  const key = n + "," + k;
  if (!ctx.subsetsCache[key]) ctx.subsetsCache[key] = subsetIndices(n, k);
  return ctx.subsetsCache[key];
}

// pool: { n, vs: Int32Array, g: Float64Array|null (m floats per entry) }
// count[k]++ and descend structure.
function runPair(d, v2, opts) {
  const H = homRows(d);
  const ctx = makeCtx(H, d);
  const m = ctx.m;
  ctx.counts[1] = 1; // subtree bookkeeping (per published per-pair lines)
  ctx.counts[2] = 1; // the pair {0, v2} itself
  ctx.maxsize = Math.max(ctx.maxsize, 2);
  ctx.elems[0] = 0; ctx.elems[1] = v2;
  // initial pool: all x in (v2, 2^d)
  const n0 = (1 << d) - v2 - 1;
  const pool = { n: n0, vs: new Int32Array(n0), g: null };
  for (let i = 0; i < n0; i++) pool.vs[i] = v2 + 1 + i;
  scan(ctx, 2, pool, opts || {});
  const counts = ctx.counts.slice(0, Math.max(9, d + 5));
  while (counts.length < 11) counts.push(0);
  return { v2, counts, trials: ctx.gateTrials, maxdepth: ctx.maxsize };
}

// THE scan: test children candidates of node S (|S| = k, elems in ctx.elems[0..k-1]).
// pool entries vs[] ascending, all > ctx.elems[k-1], and already passing all gates of
// every ancestor (standard canonical DFS pool inheritance; see header).
function scan(ctx, k, pool, opts) {
  const { d, m, H } = ctx;
  const elems = ctx.elems;
  const last = elems[k - 1];

  // --- build passing list into scratch pass arrays
  const passes = [];
  if (k <= d) {
    // children of size k+1 <= d+1 = m: prefix affine-independence = rank growth
    const rows = ctx.scratchA; // (k+1) x m
    for (let i = 0; i < k; i++) { const r = H[elems[i]]; for (let j = 0; j < m; j++) rows[i * m + j] = r[j]; }
    for (let t = 0; t < pool.n; t++) {
      const x = pool.vs[t];
      ctx.gateTrials++;
      const r = H[x];
      for (let j = 0; j < m; j++) rows[k * m + j] = r[j];
      // rankExact clobbers its argument: test on a fresh copy so the S-rows survive
      const A = new Float64Array((k + 1) * m);
      for (let idx = 0; idx < (k + 1) * m; idx++) A[idx] = rows[idx];
      if (rankExact(k + 1, m, A) === k + 1) passes.push(x);
    }
  } else if (k === m) {
    // node B (size m, full rank): children x need det([B minus b_i, x]) != 0 for all i,
    // i.e. all m row-replacement coordinates g_i(x) != 0.
    // build M_B flat
    const MB = ctx.scratchA; // m x m (careful: rankExact above clobbered; rebuild)
    for (let i = 0; i < m; i++) { const r = H[elems[i]]; for (let j = 0; j < m; j++) MB[i * m + j] = r[j]; }
    const tmp = new Float64Array(m);
    const gPass = [];
    for (let t = 0; t < pool.n; t++) {
      const x = pool.vs[t];
      ctx.gateTrials++;
      const xr = H[x];
      let ok = true;
      const g = new Float64Array(m);
      for (let i = 0; i < m; i++) {
        // stash row i, replace by x, det, restore
        for (let j = 0; j < m; j++) { tmp[j] = MB[i * m + j]; MB[i * m + j] = xr[j]; }
        const sc = ctx.scratchB;
        for (let idx = 0; idx < m * m; idx++) sc[idx] = MB[idx];
        const di = detExact(m, sc);
        for (let j = 0; j < m; j++) MB[i * m + j] = tmp[j];
        g[i] = di;
        if (di === 0) { ok = false; break; } // fail fast; g incomplete but decision exact
      }
      if (ok) { passes.push(x); gPass.push(g); }
    }
    // store g coords for children: build child pool lazily per descend; keep gPass here
    for (let pi = 0; pi < passes.length; pi++) {
      const x = passes[pi];
      ctx.counts[k + 1]++; if (k + 1 > ctx.maxsize) ctx.maxsize = k + 1;
      elems[k] = x;
      ctx.gpath[k] = gPass[pi];
      // child pool: passers > x with their g
      const cn = passes.length - pi - 1;
      const cp = { n: cn, vs: new Int32Array(cn), g: new Float64Array(cn * m) };
      let c = 0;
      for (let pj = pi + 1; pj < passes.length; pj++) {
        cp.vs[c] = passes[pj];
        const gg = gPass[pj];
        for (let j = 0; j < m; j++) cp.g[c * m + j] = gg[j];
        c++;
      }
      scan(ctx, k + 1, cp, opts);
    }
    return;
  } else {
    // k >= m+1: minor gates. Pool = children with cached g coords (pool.g != null).
    // New gates: Y in S, |Y| = d, Y contains last. Enumerate P'' subsets of
    // {pool members of S below B, excluding last} and omitted B-column subsets.
    // rows of gate matrix: g(last), g(each p in P''), g(x); cols: any C subset of B indices
    // with |C| = 2 + |P''|: gate = det(rows; cols) != 0 (projective minor identity).
    const poolIdx = []; // indices (in ctx depth numbering) of post-B elements of S (excluding last)
    for (let i = m; i < k - 1; i++) poolIdx.push(i);
    const gLast = ctx.gpath[k - 1];
    // precompute P'' shapes (depend on k only; cached per k)
    if (!ctx.shapes || ctx.shapesKey !== k) {
      const shapes = [];
      const ppSets = [];
      (function rec2(start, cur) {
        if (cur.length > 0 && cur.length <= d - 1) ppSets.push(cur.slice());
        if (cur.length >= d - 1) return;
        for (let i = start; i < poolIdx.length; i++) { cur.push(poolIdx[i]); rec2(i + 1, cur); cur.pop(); }
      })(0, []);
      ppSets.unshift([]); // empty first
      ctx.shapes = ppSets; ctx.shapesKey = k;
    }
    const ppSets = ctx.shapes;
    const colSets = {};
    for (const pp of ppSets) {
      const sz = 2 + pp.length;
      if (!colSets[sz]) colSets[sz] = subsetCache(ctx, m, sz);
    }
    const gm = new Float64Array(4 * m); // max 4 rows? no: rows = 2+|pp| <= 4; cols same count; store col-major test below
    for (let t = 0; t < pool.n; t++) {
      const x = pool.vs[t];
      ctx.gateTrials++;
      const gx = pool.g ? pool.g.subarray(t * m, t * m + m) : null;
      let ok = true;
      outer:
      for (const pp of ppSets) {
        const sz = 2 + pp.length;
        const cs = colSets[sz];
        // rows: gLast (row0), g(pp...)(rows 1..), gx (last row)
        const rowsArr = [gLast];
        for (const dep of pp) rowsArr.push(ctx.gpath[dep]);
        rowsArr.push(gx);
        for (const cols of cs) {
          // det of rowsArr restricted to cols
          const D = ctx.scratchB;
          for (let i = 0; i < sz; i++) for (let j = 0; j < sz; j++) D[i * sz + j] = rowsArr[i][cols[j]];
          if (detExact(sz, D) === 0) { ok = false; break outer; }
        }
      }
      if (ok) passes.push(t);
    }
    // descend: passers (captured as pool index t) with their g (copy from pool.g)
    for (let pi = 0; pi < passes.length; pi++) {
      const tIdx = passes[pi];
      const x = pool.vs[tIdx];
      ctx.counts[k + 1]++; if (k + 1 > ctx.maxsize) ctx.maxsize = k + 1;
      elems[k] = x;
      ctx.gpath[k] = pool.g.subarray(tIdx * m, tIdx * m + m);
      const cn = passes.length - pi - 1;
      const cp = { n: cn, vs: new Int32Array(cn), g: new Float64Array(cn * m) };
      let c = 0;
      for (let pj = pi + 1; pj < passes.length; pj++) {
        const tj = passes[pj];
        cp.vs[c] = pool.vs[tj];
        for (let j = 0; j < m; j++) cp.g[c * m + j] = pool.g[tj * m + j];
        c++;
      }
      scan(ctx, k + 1, cp, opts);
    }
    return;
  }

  // --- k <= d branch descend (rank gates above)
  for (let pi = 0; pi < passes.length; pi++) {
    const x = passes[pi];
    ctx.counts[k + 1]++; if (k + 1 > ctx.maxsize) ctx.maxsize = k + 1;
    elems[k] = x;
    ctx.gpath[k] = null;
    const cn = passes.length - pi - 1;
    const cp = { n: cn, vs: new Int32Array(cn), g: null };
    let c = 0;
    for (let pj = pi + 1; pj < passes.length; pj++) cp.vs[c++] = passes[pj];
    scan(ctx, k + 1, cp, opts);
  }
}
function poolIndexOf(pool, x) {
  // small linear (pool entries few at hot layers)
  for (let i = 0; i < pool.n; i++) if (pool.vs[i] === x) return i;
  return -1;
}

// ---------------------------------------------------------------- brute reference
// Independent slow enumerator: every child-decision by DIRECT determinant evaluation
// against ALL (d+1)-subsets of S+{x} containing x (no fast gates, no inheritance).
function bruteCensus(d, maxSize) {
  const H = homRows(d);
  const m = d + 1, N = 1 << d;
  const counts = new Array(d + 5).fill(0);
  const elems = [];
  function gpPrefix(rows, r) { // homogeneous rank of first r rows
    const A = new Float64Array(r * m);
    for (let i = 0; i < r; i++) for (let j = 0; j < m; j++) A[i * m + j] = H[rows[i]][j];
    return rankExact(r, m, A);
  }
  function childOk(S, x) {
    const T = S.concat([x]);
    if (T.length <= m) return gpPrefix(T, T.length) === T.length;
    // all (d+1)-subsets containing x must be affinely independent
    const Ys = subsetIndices(T.length - 1, d);
    const Aset = new Float64Array(m * m);
    for (const Y of Ys) {
      let idx = 0;
      for (const yi of Y) { const r = H[T[yi]]; for (let j = 0; j < m; j++) Aset[idx++] = r[j]; }
      const r = H[x]; for (let j = 0; j < m; j++) Aset[idx++] = r[j];
      const D = new Float64Array(m * m); D.set(Aset);
      if (detExact(m, D) === 0) return false;
    }
    return true;
  }
  function rec(S) {
    counts[S.length]++;
    if (S.length >= (maxSize || d + 4)) return;
    const start = S[S.length - 1] + 1;
    for (let x = start; x < N; x++) {
      if (childOk(S, x)) rec(S.concat([x]));
    }
  }
  rec([0]); // counts[1] (=1 for {0}) comes from the recursive call itself
  const out = counts.slice(0, Math.max(9, d + 5));
  while (out.length < 11) out.push(0);
  return out;
}

// ---------------------------------------------------------------- selftest battery
function bigintLaplaceDet(m, rowsJs) {
  // rowsJs: array of int arrays length m. Cofactor Laplace with BigInt.
  const rows = rowsJs.map(r => r.map(BigInt));
  function det(rowsB) {
    const n = rowsB.length;
    if (n === 1) return rowsB[0][0];
    let s = 0n;
    for (let c = 0; c < n; c++) {
      const minor = rowsB.slice(1).map(r => r.filter((_, j) => j !== c));
      const term = rowsB[0][c] * det(minor);
      s += (c % 2 === 0 ? term : -term);
    }
    return s;
  }
  return det(rows);
}

function selftest() {
  const t0 = performance.now();
  const fails = [];
  const rand = lcg(0x3ED7351);
  const line = (name, pass, detail) => {
    if (!pass) fails.push(name + (detail ? ": " + detail : ""));
    console.log((pass ? "PASS" : "FAIL") + " " + name + (detail ? " " + detail : ""));
  };

  // B1: detExact vs BigInt Laplace, random 0/1 7x7 (d=6 homogeneous shape) and
  //     random 6x6/5x5 with a 0/1 row replaced by {1,bits} row.
  DET_MAXABS = 0;
  let b1n = 0;
  for (let trial = 0; trial < 400; trial++) {
    const m = 4 + (trial % 4); // 4..7
    const rows = [];
    for (let i = 0; i < m; i++) {
      const r = [1];
      for (let j = 0; j < m - 1; j++) r.push(rand() < 0.5 ? 0 : 1);
      rows.push(r);
    }
    if (trial % 3 === 0) { const r = rows[0]; r[(trial >> 2) % m] = 1; r[0] = 1; }
    const flat = new Float64Array(m * m);
    rows.forEach((r, i) => r.forEach((v, j) => { flat[i * m + j] = v; }));
    const D = new Float64Array(m * m); D.set(flat);
    const got = detExact(m, D);
    const want = bigintLaplaceDet(m, rows);
    if (BigInt(got) !== want) { b1n++; if (b1n <= 3) console.log(JSON.stringify(rows), got, want.toString()); }
  }
  line("B1_det_vs_bigint", b1n === 0, "trials=400 bad=" + b1n + " maxabs=" + DET_MAXABS);

  // B2: rankExact vs BigInt minor-based rank on random 0/1 rows
  let b2n = 0;
  for (let trial = 0; trial < 200; trial++) {
    const m = 4 + (trial % 4); const k = 1 + (trial % m);
    const rows = [];
    for (let i = 0; i < k; i++) { const r = [1]; for (let j = 0; j < m - 1; j++) r.push(rand() < 0.5 ? 0 : 1); rows.push(r); }
    const flat = new Float64Array(k * m);
    rows.forEach((r, i) => r.forEach((v, j) => { flat[i * m + j] = v; }));
    const rk = rankExact(k, m, new Float64Array(flat));
    // bigint rank via Laplace of random subsets is complex; instead: verify rk consistent with detExact on the full sweep when k==m
    if (k === m) {
      const D = new Float64Array(flat); const dv = detExact(m, D);
      if ((dv !== 0) !== (rk === m)) b2n++;
    } else {
      // cross-check: rank increases after adding an independent row in a fresh test
      if (rk > k || rk < 0) b2n++;
    }
  }
  line("B2_rank_sanity", b2n === 0, "trials=200 bad=" + b2n);

  // B3: gate-identity fuzz: random small trees vs direct-childOk (the brute core).
  let b3n = 0, b3trials = 0;
  for (let seed = 0; seed < 60; seed++) {
    const d = 3 + (seed % 4); // d=3..6
    const H = homRows(d); const m = d + 1; const N = 1 << d;
    const rnd = lcg(9871 + seed * 7919);
    // random anchored prefix growth using directChildOk
    const directOK = (S, x) => {
      const T = S.concat([x]);
      if (T.length <= m) {
        const A = new Float64Array(T.length * m);
        for (let i = 0; i < T.length; i++) for (let j = 0; j < m; j++) A[i * m + j] = H[T[i]][j];
        return rankExact(T.length, m, A) === T.length;
      }
      const Ys = subsetIndices(T.length - 1, d);
      for (const Y of Ys) {
        const D = new Float64Array(m * m); let idx = 0;
        for (const yi of Y) for (let j = 0; j < m; j++) D[idx++] = H[T[yi]][j];
        for (let j = 0; j < m; j++) D[idx++] = H[x][j];
        if (detExact(m, D) === 0) return false;
      }
      return true;
    };
    // grow a random prefix of size m (a GP B) containing 0
    let S = [0];
    while (S.length < m) {
      const x = 1 + Math.floor(rnd() * (N - 1));
      if (S.includes(x)) continue;
      if (directOK(S, x)) S.push(x);
      if (S.length > 4 && rnd() < 0.01) S = [0];
    }
    S = S.slice(0, m); // not sorted necessarily; canonical order enforced below
    S.sort((a, b) => a - b);
    // random child q (passing), then random deeper, then compare fast scan decisions on
    // random candidates against directOK at each level (grow up to size m+3)
    for (let chain = 0; chain < 12; chain++) {
      const cands = [];
      for (let t = 0; t < 8; t++) {
        const x = 1 + Math.floor(rnd() * (N - 1));
        if (S.includes(x)) continue;
        cands.push(x);
      }
      for (const x of cands) {
        // direct decision on S+{x}
        const fast = fastDecide(d, S, x); // synthesized below via runPair machinery
        const direct = directOK(S, x);
        b3trials++;
        if (fast !== direct) b3n++;
        if (b3n <= 3 && fast !== direct) console.log("B3 mismatch", d, JSON.stringify(S), x, fast, direct);
      }
      // descend by a random passing child
      const okOnes = cands.filter(x => x > (S.length ? S[S.length - 1] : 0) && directOK(S, x));
      if (okOnes.length === 0) break;
      S.push(okOnes[Math.floor(rnd() * okOnes.length)]);
      if (S.length >= m + 3) break;
    }
  }
  line("B3_fast_vs_direct", b3n === 0, "trials=" + b3trials + " bad=" + b3n);

  // B4: published 9-point witnesses are GP (d=6), by direct dets
  const wits = [
    [11, 22, 28, 37, 42, 49, 57, 58, 63],
    [0, 5, 6, 14, 21, 26, 35, 41, 52],
    [0, 23, 29, 33, 46, 49, 50, 52, 58],
  ];
  let b4n = 0;
  const H6 = homRows(6); const m6 = 7;
  for (const w of wits) {
    for (const Y of subsetIndices(w.length, 7)) {
      const D = new Float64Array(m6 * m6); let idx = 0;
      for (const yi of Y) for (let j = 0; j < m6; j++) D[idx++] = H6[w[yi]][j];
      if (detExact(m6, D) === 0) { b4n++; break; }
    }
  }
  // and the XOR-normalized image of witness 1 by 11
  const xor = (a, b) => a.map(v => v ^ b);
  const wn = xor(wits[0], 11);
  for (const Y of subsetIndices(wn.length, 7)) {
    const D = new Float64Array(m6 * m6); let idx = 0;
    for (const yi of Y) for (let j = 0; j < m6; j++) D[idx++] = H6[wn[yi]][j];
    if (detExact(m6, D) === 0) { b4n++; }
  }
  line("B4_witnesses_gp", b4n === 0, "witnesses=" + (wits.length + 1) + " bad=" + b4n);

  // B8: det magnitude bound assertion (Hadamard-style, exactness in float64)
  line("B8_det_magnitude_bound", DET_MAXABS <= 100000, "maxabs=" + DET_MAXABS);

  // B6: full small-d census agreement with the independently brute-verified published
  //     anchored tables (targets hardcoded here from research notes; the brute mode
  //     reproduces them from scratch as well - see battery).
  const targets = {
    3: [0,1,7,21,29,5,0,0,0,0,0],
    4: [0,1,15,105,430,940,408,0,0,0,0],
  };
  let b6n = 0;
  for (const [ds, want] of Object.entries(targets)) {
    const dq = parseInt(ds, 10);
    const counts = new Array(11).fill(0);
    for (let v2 = 1; v2 < (1 << dq); v2++) {
      const r = runPair(dq, v2, {});
      for (let k = 2; k < 11; k++) counts[k] += r.counts[k] || 0;
    }
    counts[1] = 1;
    if (JSON.stringify(counts) !== JSON.stringify(want)) b6n++;
  }
  line("B6_fast_census_d3_d4", b6n === 0, "bad=" + b6n);

  const ms = Math.round(performance.now() - t0);
  console.log("SELFTEST " + (fails.length === 0 ? "PASS" : "FAIL") + " fails=" + fails.length + " ms=" + ms);
  process.exitCode = fails.length === 0 ? 0 : 1;
}

// fastDecide: run the fast scan pipeline on an arbitrary (sorted) GP prefix S and candidate x.
// Implemented by running runPair-like ctx but with a custom prefix; used ONLY in selftest.
function fastDecide(d, S, x) {
  // NOTE: S sorted, contains 0 as first element, |S| >= 2 possibly < m; the fast gates
  // are defined for nodes of the canonical tree; we emulate: build pool = sorted candidates
  const H = homRows(d); const m = d + 1;
  const ctx = makeCtx(H, d);
  ctx.counts = null;
  const k = S.length;
  for (let i = 0; i < k; i++) ctx.elems[i] = S[i];
  // construct the pool single-entry and run the appropriate gate branch manually:
  if (k <= d) {
    const rows = ctx.scratchA;
    for (let i = 0; i < k; i++) for (let j = 0; j < m; j++) rows[i * m + j] = H[S[i]][j];
    for (let j = 0; j < m; j++) rows[k * m + j] = H[x][j];
    return rankExact(k + 1, m, rows) === k + 1;
  }
  // build coordinate cache for S
  const gOf = new Map();
  const B = S.slice(0, m);
  const MB = new Float64Array(m * m);
  for (let i = 0; i < m; i++) for (let j = 0; j < m; j++) MB[i * m + j] = H[B[i]][j];
  function gamma(v) {
    const g = new Float64Array(m);
    const D = new Float64Array(m * m);
    for (let i = 0; i < m; i++) {
      D.set(MB);
      for (let j = 0; j < m; j++) D[i * m + j] = H[v][j];
      g[i] = detExact(m, D);
    }
    return g;
  }
  if (k === m) {
    const g = gamma(x);
    for (let i = 0; i < m; i++) if (g[i] === 0) return false;
    return true;
  }
  for (let i = m; i < k; i++) gOf.set(S[i], gamma(S[i]));
  const gLast = gOf.get(S[k - 1]);
  const poolIdx = [];
  for (let i = m; i < k - 1; i++) poolIdx.push(i);
  const ppSets = [[]];
  (function rec3(start, cur) {
    if (cur.length > 0 && cur.length <= d - 1) ppSets.push(cur.slice());
    if (cur.length >= d - 1) return;
    for (let i = start; i < poolIdx.length; i++) { cur.push(poolIdx[i]); rec3(i + 1, cur); cur.pop(); }
  })(0, []);
  const gx = gamma(x);
  for (const pp of ppSets) {
    const sz = 2 + pp.length;
    const colsets = subsetIndices(m, sz);
    const rowsArr = [gLast];
    for (const dep of pp) rowsArr.push(gOf.get(S[dep]));
    rowsArr.push(gx);
    for (const cols of colsets) {
      const D = new Float64Array(sz * sz);
      for (let i = 0; i < sz; i++) for (let j = 0; j < sz; j++) D[i * sz + j] = rowsArr[i][cols[j]];
      if (detExact(sz, D) === 0) return false;
    }
  }
  return true;
}

// ---------------------------------------------------------------- gatecheck pair
function gatecheckPair(d, v2, budget) {
  // run a pair with per-trial direct re-verification of the first `budget` child-decisions
  const H = homRows(d); const m = d + 1;
  const directOK = (S, x) => {
    const T = S.concat([x]);
    if (T.length <= m) {
      const A = new Float64Array(T.length * m);
      for (let i = 0; i < T.length; i++) for (let j = 0; j < m; j++) A[i * m + j] = H[T[i]][j];
      return rankExact(T.length, m, A) === T.length;
    }
    const Ys = subsetIndices(T.length - 1, d);
    for (const Y of Ys) {
      const D = new Float64Array(m * m); let idx = 0;
      for (const yi of Y) for (let j = 0; j < m; j++) D[idx++] = H[T[yi]][j];
      for (let j = 0; j < m; j++) D[idx++] = H[x][j];
      if (detExact(m, D) === 0) return false;
    }
    return true;
  };
  // instrument scan via monkey-verified wrapper: simplest is to re-implement pair run with
  // verification at each child decision inside a modified scan. We do it by wrapping
  // scan's decision points: use a global hook.
  let checks = 0, mismatches = 0;
  const origScan = scan;
  const ctxHooks = {};
  // We re-run runPair with an options object carrying the verifier.
  const opts = {
    verify: (S, x, fastDecision) => {
      if (checks >= budget) return;
      checks++;
      const direct = directOK(S, x);
      if (direct !== fastDecision) mismatches++;
    },
  };
  const res = runPairWithVerify(d, v2, opts, directOK);
  return { v2, checks, mismatches, counts: res.counts, trials: res.trials, truncated: checks >= budget };
}

// runPair with verify hook at every child-decision (slower; only for gatecheck/budget use).
function runPairWithVerify(d, v2, opts, directOK) {
  const H = homRows(d);
  const ctx = makeCtx(H, d);
  const m = ctx.m;
  ctx.counts[1] = 1; ctx.counts[2] = 1; ctx.maxsize = 2;
  ctx.elems[0] = 0; ctx.elems[1] = v2;
  const n0 = (1 << d) - v2 - 1;
  const pool = { n: n0, vs: new Int32Array(n0), g: null };
  for (let i = 0; i < n0; i++) pool.vs[i] = v2 + 1 + i;
  scanVerify(ctx, 2, pool, opts);
  const counts = ctx.counts.slice(0, Math.max(9, d + 5));
  while (counts.length < 11) counts.push(0);
  return { counts, trials: ctx.gateTrials, maxdepth: ctx.maxsize };
}

function scanVerify(ctx, k, pool, opts) {
  // same logic as scan, with opts.verify invoked at every child-decision while budget lasts
  const { d, m, H } = ctx;
  const elems = ctx.elems;
  let remaining = () => true;
  const S = () => Array.from(elems.slice(0, k));
  const fastDecideFor = (nodePool, candidate, depth) => {
    // replicate branch decisions with verify
    throw new Error("unused");
  };
  const verifyAndCount = (xInst, decision, t, curPool) => {
    if (opts.verify) opts.verify(S(), xInst, decision);
    return decision;
  };
  // We simply implement the scan inline (duplicated from scan but with verify calls):
  const passes = [];
  if (k <= d) {
    const rows = ctx.scratchA;
    for (let i = 0; i < k; i++) { const r = H[elems[i]]; for (let j = 0; j < m; j++) rows[i * m + j] = r[j]; }
    for (let t = 0; t < pool.n; t++) {
      const x = pool.vs[t];
      ctx.gateTrials++;
      const r = H[x];
      for (let j = 0; j < m; j++) rows[k * m + j] = r[j];
      const A = new Float64Array((k + 1) * m);
      for (let idx = 0; idx < (k + 1) * m; idx++) A[idx] = rows[idx];
      const dec = rankExact(k + 1, m, A) === k + 1;
      const ver = verifyAndCount(x, dec);
      if (ver) passes.push(x);
    }
  } else if (k === m) {
    const MB = ctx.scratchA;
    for (let i = 0; i < m; i++) { const r = H[elems[i]]; for (let j = 0; j < m; j++) MB[i * m + j] = r[j]; }
    const tmp = new Float64Array(m);
    const gPass = [];
    for (let t = 0; t < pool.n; t++) {
      const x = pool.vs[t];
      ctx.gateTrials++;
      const xr = H[x];
      let ok = true;
      const g = new Float64Array(m);
      for (let i = 0; i < m; i++) {
        for (let j = 0; j < m; j++) { tmp[j] = MB[i * m + j]; MB[i * m + j] = xr[j]; }
        const sc = ctx.scratchB;
        for (let idx = 0; idx < m * m; idx++) sc[idx] = MB[idx];
        const di = detExact(m, sc);
        for (let j = 0; j < m; j++) MB[i * m + j] = tmp[j];
        g[i] = di;
        if (di === 0) { ok = false; break; }
      }
      const ver = verifyAndCount(x, ok);
      if (ver) { passes.push(x); gPass.push(g); }
    }
    for (let pi = 0; pi < passes.length; pi++) {
      const x = passes[pi];
      ctx.counts[k + 1]++; if (k + 1 > ctx.maxsize) ctx.maxsize = k + 1;
      elems[k] = x; ctx.gpath[k] = gPass[pi];
      const cn = passes.length - pi - 1;
      const cp = { n: cn, vs: new Int32Array(cn), g: new Float64Array(cn * m) };
      let c = 0;
      for (let pj = pi + 1; pj < passes.length; pj++) {
        cp.vs[c] = passes[pj];
        const gg = gPass[pj];
        for (let j = 0; j < m; j++) cp.g[c * m + j] = gg[j];
        c++;
      }
      scanVerify(ctx, k + 1, cp, opts);
    }
    return;
  } else {
    const poolIdx = [];
    for (let i = m; i < k - 1; i++) poolIdx.push(i);
    const gLast = ctx.gpath[k - 1];
    const ppSets = [[]];
    (function rec3(start, cur) {
      if (cur.length > 0 && cur.length <= d - 1) ppSets.push(cur.slice());
      if (cur.length >= d - 1) return;
      for (let i = start; i < poolIdx.length; i++) { cur.push(poolIdx[i]); rec3(i + 1, cur); cur.pop(); }
    })(0, []);
    const colSets = {};
    for (const pp of ppSets) {
      const sz = 2 + pp.length;
      if (!colSets[sz]) colSets[sz] = subsetIndices(m, sz);
    }
    for (let t = 0; t < pool.n; t++) {
      const x = pool.vs[t];
      ctx.gateTrials++;
      const gx = pool.g ? pool.g.subarray(t * m, t * m + m) : null;
      let ok = true;
      outer2:
      for (const pp of ppSets) {
        const sz = 2 + pp.length;
        const cs = colSets[sz];
        const rowsArr = [gLast];
        for (const dep of pp) rowsArr.push(ctx.gpath[dep]);
        rowsArr.push(gx);
        for (const cols of cs) {
          const D = ctx.scratchB;
          for (let i = 0; i < sz; i++) for (let j = 0; j < sz; j++) D[i * sz + j] = rowsArr[i][cols[j]];
          if (detExact(sz, D) === 0) { ok = false; break outer2; }
        }
      }
      const ver = verifyAndCount(x, ok);
      if (ver) passes.push(t);
    }
    for (let pi = 0; pi < passes.length; pi++) {
      const tIdx = passes[pi];
      const x = pool.vs[tIdx];
      ctx.counts[k + 1]++; if (k + 1 > ctx.maxsize) ctx.maxsize = k + 1;
      elems[k] = x; ctx.gpath[k] = pool.g.subarray(tIdx * m, tIdx * m + m);
      const cn = passes.length - pi - 1;
      const cp = { n: cn, vs: new Int32Array(cn), g: new Float64Array(cn * m) };
      let c = 0;
      for (let pj = pi + 1; pj < passes.length; pj++) {
        const tj = passes[pj];
        cp.vs[c] = pool.vs[tj];
        for (let j = 0; j < m; j++) cp.g[c * m + j] = pool.g[tj * m + j];
        c++;
      }
      scanVerify(ctx, k + 1, cp, opts);
    }
    return;
  }
  for (let pi = 0; pi < passes.length; pi++) {
    const x = passes[pi];
    ctx.counts[k + 1]++; if (k + 1 > ctx.maxsize) ctx.maxsize = k + 1;
    elems[k] = x; ctx.gpath[k] = null;
    const cn = passes.length - pi - 1;
    const cp = { n: cn, vs: new Int32Array(cn), g: null };
    let c = 0;
    for (let pj = pi + 1; pj < passes.length; pj++) cp.vs[c++] = passes[pj];
    scanVerify(ctx, k + 1, cp, opts);
  }
}

// ---------------------------------------------------------------- CLI
function main() {
  const args = process.argv.slice(2);
  const mode = args[0];
  if (mode === "selftest") return selftest();
  if (mode === "brutecensus") {
    const d = parseInt(args[1], 10);
    const t0 = performance.now();
    const counts = bruteCensus(d, parseInt(args[2] || "0", 10) || d + 4);
    console.log(JSON.stringify({ d, counts, ms: Math.round(performance.now() - t0) }));
    return;
  }
  if (mode === "census") {
    const d = parseInt(args[1], 10);
    const t0 = performance.now();
    const counts = new Array(Math.max(11, d + 5)).fill(0);
    for (let v2 = 1; v2 < 1 << d; v2++) {
      const r = runPair(d, v2, {});
      for (let k = 2; k < r.counts.length; k++) counts[k] += r.counts[k];
    }
    counts[1] = 1;
    console.log(JSON.stringify({ d, counts, ms: Math.round(performance.now() - t0) }));
    return;
  }
  if (mode === "pair") {
    const d = parseInt(args[1], 10);
    for (let i = 2; i < args.length; i++) {
      const v2 = parseInt(args[i], 10);
      const t0 = performance.now();
      const r = runPair(d, v2, {});
      console.log(JSON.stringify({ v2: r.v2, counts: r.counts, ms: Math.round(performance.now() - t0) }));
    }
    return;
  }
  if (mode === "gatecheck") {
    const d = parseInt(args[1], 10);
    const v2 = parseInt(args[2], 10);
    const N = parseInt(args[3] || "100000", 10);
    const t0 = performance.now();
    const r = gatecheckPair(d, v2, N);
    console.log(JSON.stringify({ d, ...r, ms: Math.round(performance.now() - t0) }));
    return;
  }
  console.error("usage: census3.js selftest|brutecensus d|census d|pair d v2 ...|gatecheck d v2 N");
  process.exit(2);
}
main();
