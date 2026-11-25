'use strict';
// dx34.js — exhaustive enumeration of deficient maximal-safe configs on 3 x m, q=4,
// for arbitrary row profiles (r0,r1,r2), 0<=ri<=3, min<=2.
// Semantics (matches sat.js verifyConfig / sat2.js def-mode encode):
//   SAFE: no 4 concyclic stones (4 collinear impossible: rows <=3 stones, transversal
//         lines carry <=3 grid points).
//   MAXIMAL: an empty cell u is blocked iff its row line carries 3 stones (full row),
//         or some circle through u carries 3 stones (exactly 3 in a safe config).
//         Crossing lemma: a non-horizontal line meets each row once, so a line through
//         an empty cell of row y carries <=2 stones -> lines never block empty cells
//         of deficient rows; full rows are blocked by their row line.
//   DEFICIENT: profile has min row count <= 2.
// Paths:
//   direct: per-config exact computation (ground truth engine, any profile)
//   fast  : precomputed per-(pair) mask tables; supports exactly-one-full-row (3,a,b),
//           a,b in {1,2}; and (2,2,2). Must agree with direct on all small boards.
// Usage:
//   node dx34.js direct <m> <r0,r1,r2> [--examples=N]
//   node dx34.js fast   <m> <r0,r1,r2> [--examples=N]
//   node dx34.js selftest <m>

function isqrt(n) { if (n < 0) return -1; let r = Math.floor(Math.sqrt(n)); while (r > 0 && r * r > n) r--; while ((r + 1) * (r + 1) <= n) r++; return r; }
function circle3(x1, y1, x2, y2, x3, y3) {
  const s1 = x1 * x1 + y1 * y1, s2 = x2 * x2 + y2 * y2, s3 = x3 * x3 + y3 * y3;
  const dx2 = x2 - x1, dy2 = y2 - y1, dx3 = x3 - x1, dy3 = y3 - y1;
  const det = dx2 * dy3 - dx3 * dy2; if (det === 0) return null;
  let A = det, Bu = -(s2 - s1) * dy3 + (s3 - s1) * dy2, Bv = -dx2 * (s3 - s1) + dx3 * (s2 - s1), D = -(A * s1 + Bu * x1 + Bv * y1);
  if (A < 0) { A = -A; Bu = -Bu; Bv = -Bv; D = -D; }
  return [A, Bu, Bv, D];
}
function onC(c, x, y) { return c[0] * (x * x + y * y) + c[1] * x + c[2] * y + c[3] === 0; }
const ROOTS = [0, 0, 0];
function rowRoots(c, y) {
  const A = c[0], Bu = c[1];
  const K = A * y * y + c[2] * y + c[3];
  const disc = Bu * Bu - 4 * A * K;
  if (disc < 0) return 0;
  const r = isqrt(disc);
  if (r * r !== disc) return 0;
  const d2 = 2 * A; const n1 = -Bu + r, n2 = -Bu - r; let cnt = 0;
  if (n1 % d2 === 0) ROOTS[cnt++] = n1 / d2;
  if (r !== 0 && n2 % d2 === 0) ROOTS[cnt++] = n2 / d2;
  return cnt;
}
function combos(m, k) {
  const res = []; const cur = [];
  (function rec(start, left) { if (left === 0) { res.push(cur.slice()); return; } for (let x = start; x <= m - left; x++) { cur.push(x); rec(x + 1, left - 1); cur.pop(); } })(0, k);
  return res;
}

function direct(m, prof, examples) {
  const [r0, r1, r2] = prof;
  const rows = [combos(m, r0), combos(m, r1), combos(m, r2)];
  const full = (1 << m) - 1;
  let count = 0; const ex = [];
  const pts = []; const blocked = [0, 0, 0];
  function check(A, B, C) {
    pts.length = 0;
    const sets = [A, B, C];
    for (let i = 0; i < 3; i++) for (const x of sets[i]) pts.push(x, i);
    const k = pts.length / 2;
    blocked[0] = r0 === 3 ? full : 0; blocked[1] = r1 === 3 ? full : 0; blocked[2] = r2 === 3 ? full : 0;
    for (let i = 0; i < k; i++) for (let j = i + 1; j < k; j++) for (let l = j + 1; l < k; l++) {
      const c = circle3(pts[2*i], pts[2*i+1], pts[2*j], pts[2*j+1], pts[2*l], pts[2*l+1]);
      if (!c) continue;
      let cnt = 0;
      for (let t = 0; t < k; t++) if (onC(c, pts[2*t], pts[2*t+1])) cnt++;
      if (cnt >= 4) return;
      for (let y = 0; y < 3; y++) { const n = rowRoots(c, y); for (let t = 0; t < n; t++) { const x = ROOTS[t]; if (x >= 0 && x < m) blocked[y] |= (1 << x); } }
    }
    for (let y = 0; y < 3; y++) {
      let stones = 0; for (const x of sets[y]) stones |= (1 << x);
      const need = full & ~stones;
      if ((blocked[y] & need) !== need) return;
    }
    count++;
    if (ex.length < examples) ex.push([...A.map(x => [x, 0]), ...B.map(x => [x, 1]), ...C.map(x => [x, 2])]);
  }
  for (const A of rows[0]) {
    if (r1 === 0) { if (r2 === 0) check(A, [], []); else for (const C of rows[2]) check(A, [], C); }
    else for (const B of rows[1]) { if (r2 === 0) check(A, B, []); else for (const C of rows[2]) check(A, B, C); }
  }
  return { count, examples: ex };
}

// ============ fast path: exactly one full row ============
// Rows: F=full(3), B=rb stones, C=rc stones, rb,rc in {1,2}. Optionally chunk over triples of F.
//
// Circle classes (stones A=[a1,a2,a3]@yF, Bs@yB, Cs@yC) and their uses:
//  (2F,1B) circles(a_i,a_j,b): rowB(b+<=1 other)->covBAB; rowC(<=2)->covCAB; quad{a_i,a_j,b,b'}->unsafeAB
//  (2F,1C) circles(a_i,a_j,c): rowC(c+<=1)->covCAC; rowB(<=2)->covBAC; quad{a_i,a_j,c,c'}->unsafeAC
//  (2B,1F) circles(b1,b2,a): rowC(<=2)->covCBB
//  (2C,1F) circles(c1,c2,a): rowB(<=2)->covBCC
//  (2B,1C) circles(b1,b2,c): rowC(c+<=1)->gC2   [iff bIsPair]
//  (2C,1B) circles(c1,c2,b): rowB(b+<=1)->gB2   [iff cIsPair]
//  quad{b1,b2,c1,c2}->uBC [iff both pairs]
//  (1F,1B,1C) circles(a,b,c): rowB other->cacheBC_B, rowC other->cacheBC_C (per A, indexed b*m+c, folded over a)
//  quad{a_i,a_j,b,c}->Q[b] bits over c (roots of circles(a_i,a_j,b) at rowC)
//  quad{a_i,b1,b2,c}->R2[bi] bits over c (roots of circles(a_i,b1,b2) at rowC) [iff bIsPair]
//  quad{a_i,c1,c2,b}->S2[ci] bits over b (roots of circles(a_i,c1,c2) at rowB) [iff cIsPair]
// coverage rowB = covBAB | covBAC | covBCC | gB2 | cacheBC_B(b1|b2 x c1|c2)
// coverage rowC = covCAB | covCAC | covCBB | gC2 | cacheBC_C(...)
function fastFull(m, prof, examples, astart, acount) {
  const [r0, r1, r2] = prof;
  const F = r0 === 3 ? 0 : (r1 === 3 ? 1 : 2);
  const rows = [0, 1, 2].filter(y => y !== F);
  const B = rows[0], C = rows[1];
  const rb = prof[B], rc = prof[C];
  const yF = F, yB = B, yC = C;
  const full = (1 << m) - 1;
  const singles = []; for (let x = 0; x < m; x++) singles.push([x]);
  const pairsB = rb === 2 ? combos(m, 2) : singles;
  const setsC = rc === 2 ? combos(m, 2) : singles;
  const nB = pairsB.length, nC = setsC.length;
  const Asets = combos(m, 3);
  let count = 0; const ex = [];
  const bIsPair = rb === 2, cIsPair = rc === 2;
  const gC2 = new Int32Array(nB * nC), gB2 = new Int32Array(nB * nC), uBC = new Uint8Array(nB * nC);
  if (bIsPair) {
    for (let bi = 0; bi < nB; bi++) { const b1 = pairsB[bi][0], b2 = pairsB[bi][1];
      for (let ci = 0; ci < nC; ci++) { const Cs = setsC[ci];
        for (const c of Cs) { const cir = circle3(b1, yB, b2, yB, c, yC); if (!cir) continue;
          const n = rowRoots(cir, yC); for (let t = 0; t < n; t++) { const x = ROOTS[t]; if (x >= 0 && x < m) gC2[bi * nC + ci] |= (1 << x); } }
      } }
  }
  if (cIsPair) {
    for (let bi = 0; bi < nB; bi++) {
      for (let ci = 0; ci < nC; ci++) { const c1 = setsC[ci][0], c2 = setsC[ci][1];
        for (const b of pairsB[bi]) { const cir = circle3(c1, yC, c2, yC, b, yB); if (!cir) continue;
          const n = rowRoots(cir, yB); for (let t = 0; t < n; t++) { const x = ROOTS[t]; if (x >= 0 && x < m) gB2[bi * nC + ci] |= (1 << x); } }
      } }
  }
  if (bIsPair && cIsPair) {
    for (let bi = 0; bi < nB; bi++) { const b1 = pairsB[bi][0], b2 = pairsB[bi][1];
      for (let ci = 0; ci < nC; ci++) { const Cs = setsC[ci];
        const cir = circle3(b1, yB, b2, yB, Cs[0], yC);
        if (cir && onC(cir, Cs[1], yC)) uBC[bi * nC + ci] = 1;
      } }
  }
  const aLo = astart || 0, aHi = Math.min(Asets.length, astart != null && acount != null ? astart + acount : Asets.length);
  const cacheBC_B = new Int32Array(m * m), cacheBC_C = new Int32Array(m * m);
  for (let ai = aLo; ai < aHi; ai++) {
    const A = Asets[ai];
    const apairs = [[A[0], A[1]], [A[1], A[2]], [A[2], A[0]]];
    cacheBC_B.fill(0); cacheBC_C.fill(0);
    for (const a of A) for (let b = 0; b < m; b++) for (let c = 0; c < m; c++) {
      const cir = circle3(a, yF, b, yB, c, yC); if (!cir) continue;
      let n = rowRoots(cir, yB); for (let t = 0; t < n; t++) { const x = ROOTS[t]; if (x >= 0 && x < m) cacheBC_B[b * m + c] |= (1 << x); }
      n = rowRoots(cir, yC); for (let t = 0; t < n; t++) { const x = ROOTS[t]; if (x >= 0 && x < m) cacheBC_C[b * m + c] |= (1 << x); }
    }
    const Q = new Int32Array(m);
    for (let b = 0; b < m; b++) for (const ap of apairs) { const cir = circle3(ap[0], yF, ap[1], yF, b, yB); if (!cir) continue;
      const n = rowRoots(cir, yC); for (let t = 0; t < n; t++) { const x = ROOTS[t]; if (x >= 0 && x < m) Q[b] |= (1 << x); } }
    const unsafeAB = new Uint8Array(nB), covBAB = new Int32Array(nB), covCAB = new Int32Array(nB), covCBB = new Int32Array(nB), R2 = new Int32Array(nB);
    for (let bi = 0; bi < nB; bi++) {
      const Bs = pairsB[bi];
      for (const ap of apairs) {
        for (const b of Bs) {
          const cir = circle3(ap[0], yF, ap[1], yF, b, yB); if (!cir) continue;
          if (bIsPair && onC(cir, Bs[0] === b ? Bs[1] : Bs[0], yB)) unsafeAB[bi] = 1;
          let n = rowRoots(cir, yB); for (let t = 0; t < n; t++) { const x = ROOTS[t]; if (x >= 0 && x < m) covBAB[bi] |= (1 << x); }
          n = rowRoots(cir, yC); for (let t = 0; t < n; t++) { const x = ROOTS[t]; if (x >= 0 && x < m) covCAB[bi] |= (1 << x); }
        }
      }
      if (bIsPair) {
        for (const a of A) { const cir = circle3(Bs[0], yB, Bs[1], yB, a, yF); if (!cir) continue;
          const n = rowRoots(cir, yC); for (let t = 0; t < n; t++) { const x = ROOTS[t]; if (x >= 0 && x < m) covCBB[bi] |= (1 << x); } }
        for (const a of A) { const cir = circle3(a, yF, Bs[0], yB, Bs[1], yB); if (!cir) continue;
          const n = rowRoots(cir, yC); for (let t = 0; t < n; t++) { const x = ROOTS[t]; if (x >= 0 && x < m) R2[bi] |= (1 << x); } }
      }
    }
    const unsafeAC = new Uint8Array(nC), covBAC = new Int32Array(nC), covCAC = new Int32Array(nC), covBCC = new Int32Array(nC), S2 = new Int32Array(nC);
    for (let ci = 0; ci < nC; ci++) {
      const Cs = setsC[ci];
      for (const ap of apairs) {
        for (const c of Cs) {
          const cir = circle3(ap[0], yF, ap[1], yF, c, yC); if (!cir) continue;
          if (cIsPair && onC(cir, Cs[0] === c ? Cs[1] : Cs[0], yC)) unsafeAC[ci] = 1;
          let n = rowRoots(cir, yB); for (let t = 0; t < n; t++) { const x = ROOTS[t]; if (x >= 0 && x < m) covBAC[ci] |= (1 << x); }
          n = rowRoots(cir, yC); for (let t = 0; t < n; t++) { const x = ROOTS[t]; if (x >= 0 && x < m) covCAC[ci] |= (1 << x); }
        }
      }
      if (cIsPair) {
        for (const a of A) { const cir = circle3(Cs[0], yC, Cs[1], yC, a, yF); if (!cir) continue;
          const n = rowRoots(cir, yB); for (let t = 0; t < n; t++) { const x = ROOTS[t]; if (x >= 0 && x < m) covBCC[ci] |= (1 << x); } }
        for (const a of A) { const cir = circle3(a, yF, Cs[0], yC, Cs[1], yC); if (!cir) continue;
          const n = rowRoots(cir, yB); for (let t = 0; t < n; t++) { const x = ROOTS[t]; if (x >= 0 && x < m) S2[ci] |= (1 << x); } }
      }
    }
    for (let bi = 0; bi < nB; bi++) {
      if (unsafeAB[bi]) continue;
      const Bs = pairsB[bi];
      let bbits = 0; for (const b of Bs) bbits |= (1 << b);
      const needB = full & ~bbits;
      const R2bi = R2[bi];
      const b1 = Bs[0], b2 = Bs.length > 1 ? Bs[1] : -1;
      const q = Q[b1] | (b2 >= 0 ? Q[b2] : 0);
      const covBaseB = covBAB[bi] | covCBB[bi] * 0;
      const baseBRowB = covBAB[bi];
      for (let ci = 0; ci < nC; ci++) {
        if (unsafeAC[ci]) continue;
        const Cs = setsC[ci];
        let cbits = 0; for (const c of Cs) cbits |= (1 << c);
        if (bIsPair && cIsPair) {
          if (uBC[bi * nC + ci]) continue;
          if ((R2bi & cbits)) continue;
          if ((S2[ci] & bbits)) continue;
        } else if (bIsPair && !cIsPair) {
          if ((R2bi & cbits)) continue;
        } else if (!bIsPair && cIsPair) {
          if ((S2[ci] & bbits)) continue;
        }
        if (q & cbits) continue;
        const c1 = Cs[0], c2 = Cs.length > 1 ? Cs[1] : -1;
        const covB = baseBRowB | covBAC[ci] | covBCC[ci] | (cIsPair ? gB2[bi * nC + ci] : 0)
          | cacheBC_B[b1 * m + c1] | (c2 >= 0 ? cacheBC_B[b1 * m + c2] : 0) | (b2 >= 0 ? cacheBC_B[b2 * m + c1] : 0) | (b2 >= 0 && c2 >= 0 ? cacheBC_B[b2 * m + c2] : 0);
        if ((covB & needB) !== needB) continue;
        const needC = full & ~cbits;
        const covC = covCAB[bi] | covCAC[ci] | covCBB[bi] | (bIsPair ? gC2[bi * nC + ci] : 0)
          | cacheBC_C[b1 * m + c1] | (c2 >= 0 ? cacheBC_C[b1 * m + c2] : 0) | (b2 >= 0 ? cacheBC_C[b2 * m + c1] : 0) | (b2 >= 0 && c2 >= 0 ? cacheBC_C[b2 * m + c2] : 0);
        if ((covC & needC) !== needC) continue;
        count++;
        if (ex.length < examples) ex.push([...A.map(x => [x, F]), ...Bs.map(x => [x, B]), ...Cs.map(x => [x, C])]);
      }
    }
  }
  return { count, examples: ex };
}
// ============ fast path: (2,2,2) ============
function fast222(m, examples) {
  const P = combos(m, 2); const n = P.length;
  const full = (1 << m) - 1;
  // t[X][Y] = Int32Array(n*n): bits for row Y of circles(P[xi]@X, sy@Y), sy in P[yi]
  // tr[X][Y] = Int32Array(n*n): bits for row R=3-X-Y of the same circles
  const t = {}, tr = {};
  for (let X = 0; X < 3; X++) for (let Y = 0; Y < 3; Y++) { if (X === Y) continue; const R = 3 - X - Y;
    const ty = new Int32Array(n * n), tR = new Int32Array(n * n);
    for (let xi = 0; xi < n; xi++) { const p1 = P[xi];
      for (let yi = 0; yi < n; yi++) {
        for (const sy of P[yi]) {
          const cir = circle3(p1[0], X, p1[1], X, sy, Y); if (!cir) continue;
          let nr = rowRoots(cir, Y); for (let t2 = 0; t2 < nr; t2++) { const x = ROOTS[t2]; if (x >= 0 && x < m) ty[xi * n + yi] |= (1 << x); }
          nr = rowRoots(cir, R); for (let t2 = 0; t2 < nr; t2++) { const x = ROOTS[t2]; if (x >= 0 && x < m) tR[xi * n + yi] |= (1 << x); }
        }
      } }
    t[X + '' + Y] = ty; tr[X + '' + Y] = tR;
  }
  const t7 = [new Int32Array(n * n * m), new Int32Array(n * n * m), new Int32Array(n * n * m)];
  for (let ai = 0; ai < n; ai++) for (let bi = 0; bi < n; bi++) {
    const Ap = P[ai], Bp = P[bi];
    for (let c = 0; c < m; c++) { let mA = 0, mB = 0, mC = 0;
      for (const a of Ap) for (const b of Bp) { const cir = circle3(a, 0, b, 1, c, 2); if (!cir) continue;
        let nr = rowRoots(cir, 0); for (let t2 = 0; t2 < nr; t2++) { const x = ROOTS[t2]; if (x >= 0 && x < m) mA |= (1 << x); }
        nr = rowRoots(cir, 1); for (let t2 = 0; t2 < nr; t2++) { const x = ROOTS[t2]; if (x >= 0 && x < m) mB |= (1 << x); }
        nr = rowRoots(cir, 2); for (let t2 = 0; t2 < nr; t2++) { const x = ROOTS[t2]; if (x >= 0 && x < m) mC |= (1 << x); }
      }
      const base = (ai * n + bi) * m + c; t7[0][base] = mA; t7[1][base] = mB; t7[2][base] = mC;
    }
  }
  const u = {};
  for (const [X, Y] of [[0, 1], [0, 2], [1, 2]]) { const arr = new Uint8Array(n * n);
    for (let xi = 0; xi < n; xi++) for (let yi = 0; yi < n; yi++) { const p = P[xi], q = P[yi];
      const cir = circle3(p[0], X, p[1], X, q[0], Y); if (cir && onC(cir, q[1], Y)) arr[xi * n + yi] = 1; }
    u[X + '' + Y] = arr; }
  // v[X][Y]: quads {2 of X, 1 of Y, 1 of Z}, Z=3-X-Y: per (X-pair xi, Y-pair yi): bits over Z stone x
  const v = {};
  for (let X = 0; X < 3; X++) for (let Y = 0; Y < 3; Y++) { if (X === Y) continue; const Z = 3 - X - Y;
    const arr = new Int32Array(n * n);
    for (let xi = 0; xi < n; xi++) { const p = P[xi];
      for (let yi = 0; yi < n; yi++) { const q = P[yi]; let bits = 0;
        for (let z = 0; z < m; z++) { for (const py of q) { const cir = circle3(p[0], X, p[1], X, py, Y); if (cir && onC(cir, z, Z)) { bits |= (1 << z); break; } } }
        arr[xi * n + yi] = bits; } }
    v[X + '' + Y] = arr; }
  let count = 0; const ex = [];
  for (let ai = 0; ai < n; ai++) { const Ap = P[ai];
    const abits = (1 << Ap[0]) | (1 << Ap[1]);
    const needA = full & ~abits;
    for (let bi = 0; bi < n; bi++) {
      if (u['01'][ai * n + bi]) continue;
      const Bp = P[bi]; const bbits = (1 << Bp[0]) | (1 << Bp[1]);
      const needB = full & ~bbits;
      for (let ci = 0; ci < n; ci++) {
        if (u['02'][ai * n + ci] || u['12'][bi * n + ci]) continue;
        const Cp = P[ci]; const c1 = Cp[0], c2 = Cp[1]; const cbits = (1 << c1) | (1 << c2);
        if ((v['01'][ai * n + bi] & cbits)) continue;   // {a1,a2,b,z2}
        if ((v['10'][bi * n + ai] & cbits)) continue;   // {b1,b2,a,z2}
        if ((v['02'][ai * n + ci] & bbits)) continue;   // {a1,a2,c,z1}
        if ((v['20'][ci * n + ai] & bbits)) continue;   // {c1,c2,a,z1}
        if ((v['12'][bi * n + ci] & abits)) continue;   // {b1,b2,c,z0}
        if ((v['21'][ci * n + bi] & abits)) continue;   // {c1,c2,b,z0}
        const baseAB = (ai * n + bi) * m;
        let covA = t['10'][bi * n + ai] | t['20'][ci * n + ai] | tr['12'][bi * n + ci] | tr['21'][ci * n + bi] | t7[0][baseAB + c1] | t7[0][baseAB + c2];
        if ((covA & needA) !== needA) continue;
        let covB = t['01'][ai * n + bi] | t['21'][ci * n + bi] | tr['02'][ai * n + ci] | tr['20'][ci * n + ai] | t7[1][baseAB + c1] | t7[1][baseAB + c2];
        if ((covB & needB) !== needB) continue;
        const needC = full & ~cbits;
        let covC = t['02'][ai * n + ci] | t['12'][bi * n + ci] | tr['01'][ai * n + bi] | tr['10'][bi * n + ai] | t7[2][baseAB + c1] | t7[2][baseAB + c2];
        if ((covC & needC) !== needC) continue;
        count++;
        if (ex.length < examples) ex.push([[Ap[0], 0], [Ap[1], 0], [Bp[0], 1], [Bp[1], 1], [c1, 2], [c2, 2]]);
      } } }
  return { count, examples: ex };
}

function fast(m, prof, examples, astart, acount) {
  const [r0, r1, r2] = prof;
  const nFull = (r0 === 3) + (r1 === 3) + (r2 === 3);
  if (nFull === 1 && r0 !== 0 && r1 !== 0 && r2 !== 0) return fastFull(m, prof, examples, astart, acount);
  if (nFull === 0 && r0 === 2 && r1 === 2 && r2 === 2) return fast222(m, examples);
  throw new Error('fast supports (3,a,b) a,b in {1,2} and (2,2,2); got ' + prof);
}

function profilesDef() { const res = []; for (let a = 0; a <= 3; a++) for (let b = 0; b <= 3; b++) for (let c = 0; c <= 3; c++) if (Math.min(a, b, c) <= 2) res.push([a, b, c]); return res; }

const argv = process.argv.slice(2);
const cmd = argv[0];
const m = Number(argv[1]);
if (cmd === 'direct' || cmd === 'fast') {
  const prof = argv[2].split(',').map(Number);
  const exArg = argv.find(a => a.startsWith('--examples='));
  const stArg = argv.find(a => a.startsWith('--astart='));
  const ctArg = argv.find(a => a.startsWith('--acount='));
  const t0 = Date.now();
  const r = cmd === 'direct' ? direct(m, prof, exArg ? Number(exArg.slice(11)) : 0) : fast(m, prof, exArg ? Number(exArg.slice(11)) : 0, stArg ? Number(stArg.slice(9)) : null, ctArg ? Number(ctArg.slice(9)) : null);
  console.log(JSON.stringify({ mode: cmd, m, prof: prof.join(','), count: r.count, ms: Date.now() - t0, astart: stArg ? Number(stArg.slice(9)) : null, acount: ctArg ? Number(ctArg.slice(9)) : null }));
  for (const e of r.examples) console.log(JSON.stringify(e));
} else if (cmd === 'selftest') {
  const profiles = profilesDef();
  const out = { m, direct: {}, fastDiff: 0 };
  let mismatches = 0;
  for (const prof of profiles) {
    const d = direct(m, prof, 0).count;
    out.direct[prof.join(',')] = d;
    const [a, b, c] = prof;
    const nFull = (a === 3) + (b === 3) + (c === 3);
    if ((nFull === 1 && a !== 0 && b !== 0 && c !== 0) || (nFull === 0 && a === 2 && b === 2 && c === 2)) {
      const f = fast(m, prof, 0).count;
      if (f !== d) { mismatches++; console.log('MISMATCH prof=' + prof.join(',') + ' direct=' + d + ' fast=' + f); }
    }
  }
  out.fastMismatch = mismatches;
  out.defTotal = Object.values(out.direct).reduce((s, v) => s + v, 0);
  console.log(JSON.stringify(out));
} else { console.log('cmds: direct|fast|selftest'); }
