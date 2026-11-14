// genff.js — ultra-fast census CNF generator for w×m q-point deficient/cap instances.
//
// genfast.js reduced the census to O((2m)·n^2) via half-integer center columns; for
// m in the hundreds that is still minutes per instance. This generator replaces the
// per-point-pair witness counting with direct SAME-ROW-PAIR-PAIR enumeration:
//
//   A circle with q >= w+2 grid points has, by pigeonhole, >= 2 same-row pairs
//   (rows hold <= 2 circle points each, so #pairs = sum C(n_y,2) >= q-w-1 >= 1...
//    precisely: minimizing sum C(n_y,2) subject to sum n_y = q over w rows with n_y<=2
//    gives 2 pairs at q = w+2, more for larger q).
//   A same-row pair on a circle with center x u = U/2 is symmetric: points
//   (u±e/2, y), characterized by (row y, offset e) with e ≡ U (mod 2), 1 <= e <=
//   min(U, 2m-2-U). TWO same-row pairs (y1,e1),(y2,e2), y1≠y2, determine the circle:
//     v = [4(y1^2-y2^2) + e1^2 - e2^2] / [8(y1-y2)]   (center y, exact rational)
//   Each candidate is pre-filtered (pure integer arithmetic, no gcd/Map in the hot
//   loop) by requiring >= EXTRA_ROWS_MIN further rows carrying an in-grid circle
//   point; candidates passing get the exact genfast-identical point-set scan.
//   The filter has no false negatives: a true q-point circle has q-4 points outside
//   rows y1,y2, occupying >= ceil((q-4)/2) rows, and EXTRA_ROWS_MIN caps that below.
//   Equal-offset rectangles (e1 = e2, i2 == i1 in the loop) ARE enumerated: a
//   circle whose same-row pairs all share one offset is only reachable there.
//
//   Lines: for q > w every line with >= q grid points is horizontal (a non-horizontal
//   line meets each of the w rows in <= 1 point), so exactly the w rows survive —
//   built with the same lineABC/scan/sort calls genfast uses, byte-identical output.
//   For q <= w the full genfast pair enumeration is used as fallback.
//
// Output verified byte-identical to genfast.js / sat2.js on 14 samples (see
// output/verif notes committed alongside): the curve list (order included) and the
// whole downstream sat2.js encoding (counters, deficient/cap/rowfixed, lex-leader,
// DIMACS) are identical, so kissat results transfer bit-exactly.
//
// Usage: node genff.js w m q [--deficient|--cap=K] [--counter=seq|tot]
//                        [--lex=H,V,HV] [--rowY=Y] out.cnf
// Requires q >= w+2 and w <= 7 (asserts; below that use genfast.js/sat2.js).
// SAT models decode identically (cell var i+1 = cell[y*m+x]).
'use strict';
const path = require('path');
const SEVEN = process.env.SEVEN_SCRIPTS || '/home/user/krwork/seven/scripts';
const S = require(path.join(SEVEN, 'sat.js'));
const S2 = require(path.join(SEVEN, 'sat2.js'));

function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { const t = a % b; a = b; b = t; } return a; }

function fastCensusFF(w, m, q) {
  if (q < w + 1) throw new Error('genff requires q >= w+1 (w=' + w + ', q=' + q + '); use sat2.js');
  if (w > 7) throw new Error('genff requires w <= 7 (w=' + w + ')');
  if (q - w < 2) throw new Error('genff requires q >= w+2 (two same-row pairs); use genfast.js');
  const EXTRA_ROWS_MIN = Math.min(3, w - 2, Math.ceil((q - 4) / 2)); // <= ceil((q-4)/2) => no false negatives
  const P = S.pts(w, m), n = P.length;

  // ---- lines ----
  const lines = [];
  if (q > w) {
    // only the w horizontal rows can hold >= q points
    for (let y = 0; y < w; y++) {
      const i0 = y * m, i1 = i0 + 1;
      const lo = S.lineABC(P[i0], P[i1]);
      const set = [];
      for (let idx = 0; idx < n; idx++) if (S.onLine(lo, P[idx][0], P[idx][1])) set.push(idx);
      if (set.length >= q) lines.push({ type: 'line', co: lo, pts: set });
    }
  } else {
    // fallback: genfast's full pair enumeration (small instances only)
    const lineMap = new Map();
    for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
      const lo = S.lineABC(P[i], P[j]);
      const key = lo[0] + ',' + lo[1] + ',' + lo[2];
      if (!lineMap.has(key)) lineMap.set(key, lo);
    }
    for (const lo of lineMap.values()) {
      const set = [];
      for (let idx = 0; idx < n; idx++) if (S.onLine(lo, P[idx][0], P[idx][1])) set.push(idx);
      if (set.length >= q) lines.push({ type: 'line', co: lo, pts: set });
    }
  }
  lines.sort((A, B) => (A.pts[0] - B.pts[0]) || (A.pts[1] - B.pts[1])); // = original insertion order

  // ---- squares table: sqTab[par][s^2] = s for s ≡ par (mod 2); sqTab[1][0] stays -1
  // (odd U has no in-grid tangent point x=U/2) ----
  const T2 = 2 * m - 2;
  const T2sq = T2 * T2;
  const sqTab = [new Int32Array(T2sq + 1).fill(-1), new Int32Array(T2sq + 1).fill(-1)];
  for (let s = 0; s <= T2; s++) sqTab[s & 1][s * s] = s;

  // ---- circles: same-row-pair-pair enumeration ----
  const found = new Map(); // canonical 'a,b,c,d' -> {type:'circle', co, pts}
  const rowPairs = [];
  for (let y1 = 0; y1 < w; y1++) for (let y2 = y1 + 1; y2 < w; y2++) rowPairs.push([y1, y2]);
  for (let U = 0; U <= T2; U++) { // center x u = U/2
    const limMin = Math.min(U, T2 - U), limMax = Math.max(U, T2 - U);
    const start = (U & 1) ? 1 : 2;
    const ne = Math.floor((limMin - start) / 2) + 1;
    if (ne < 2) continue;
    const A = new Int32Array(ne);
    for (let i = 0; i < ne; i++) { const e = start + 2 * i; A[i] = e * e; }
    const par = U & 1;
    for (let rp = 0; rp < rowPairs.length; rp++) {
      const y1 = rowPairs[rp][0], y2 = rowPairs[rp][1];
      const D0 = 8 * (y1 - y2), D02 = D0 * D0, C0 = 4 * (y1 * y1 - y2 * y2), y1D0 = y1 * D0;
      const oth = [];
      for (let y3 = 0; y3 < w; y3++) if (y3 !== y1 && y3 !== y2) oth.push(y3);
      const no = oth.length;
      const P3b = new Int32Array(w), S3b = new Int32Array(w);
      for (let i1 = 0; i1 < ne; i1++) {
        const A1 = A[i1], K1base = y1D0 - A1 - C0, Wbase = A1 * D02;
        for (let oi = 0; oi < no; oi++) {
          const y3 = oth[oi];
          const G3 = y3 * D0 - A1 - C0;
          P3b[oi] = 4 * (K1base - G3);
          S3b[oi] = K1base + G3;
        }
        for (let i2 = 0; i2 < ne; i2++) { // ORDERED e pairs (both (e1,e2),(e2,e1) are
          // distinct circles for fixed rows y1<y2); i2 == i1 covers equal-offset rectangles
          const A2 = A[i2], N0 = A1 - A2 + C0, twoA2 = 2 * A2;
          let rows = 0;
          for (let oi = 0; oi < no; oi++) {
            const W = Wbase + P3b[oi] * (S3b[oi] + twoA2);
            if (W < 0 || W % D02 !== 0) continue;
            const s2 = W / D02;
            if (s2 > T2sq) continue;
            const s = sqTab[par][s2];
            if (s < 0 || s > limMax) continue;
            if (++rows >= EXTRA_ROWS_MIN) break;
          }
          if (rows < EXTRA_ROWS_MIN) continue;
          // exact scan — identical arithmetic to genfast.js
          let Nn = N0, Dd = D0;
          let g = gcd(Nn, Dd); if (g === 0) g = 1;
          Nn /= g; Dd /= g; if (Dd < 0) { Nn = -Nn; Dd = -Dd; }
          const yd1 = y1 * Dd - Nn;
          let Rp = A1 * Dd * Dd + 4 * yd1 * yd1;
          let Qp = 4 * Dd * Dd;
          let g2 = gcd(Rp, Qp); if (g2 === 0) g2 = 1;
          Rp /= g2; Qp /= g2;
          const set = [];
          for (let idx = 0; idx < n; idx++) {
            const dx2 = 2 * P[idx][0] - U;
            const yd = P[idx][1] * Dd - Nn;
            if (dx2 * dx2 * Dd * Dd * Qp + 4 * yd * yd * Qp === 4 * Dd * Dd * Rp) set.push(idx);
          }
          if (set.length >= q) {
            const co = S.circleABC(P[set[0]], P[set[1]], P[set[2]]);
            const ck = co.join(',');
            if (!found.has(ck)) found.set(ck, { type: 'circle', co: co, pts: set });
          }
        }
      }
    }
  }
  const circles = [...found.values()];
  circles.sort((A, B) => (A.pts[0] - B.pts[0]) || (A.pts[1] - B.pts[1]) || (A.pts[2] - B.pts[2]));
  return { P: P, n: n, curves: lines.concat(circles) };
}

// ---- patch and reuse sat2.js verbatim ----
S.buildCensus = fastCensusFF;

if (require.main === module) {
  const args = process.argv.slice(2);
  const [w, m, q] = [Number(args[0]), Number(args[1]), Number(args[2])];
  let i = 3, mode = 'deficient', cap = null, cnt = 'seq', lex = [], rowY = null, out = null;
  for (; i < args.length; i++) {
    const a = args[i];
    if (a === '--deficient') mode = 'deficient';
    else if (a.startsWith('--cap=')) { mode = 'cap'; cap = Number(a.slice(6)); }
    else if (a.startsWith('--counter=')) cnt = a.slice(10);
    else if (a.startsWith('--lex=')) lex = a.slice(6).split(',').filter(s => S2.S === S && ['H', 'V', 'HV'].includes(s));
    else if (a.startsWith('--rowY=')) { mode = 'rowfixed'; rowY = Number(a.slice(7)); }
    else if (!out) out = a;
  }
  const opts = { mode, cap, counter: cnt, lex, rowY };
  const { enc, meta } = S2.dump(w, m, q, opts);
  require('fs').writeFileSync(out, S2.toDimacs2(enc));
  meta.file = out;
  meta.generator = 'genff';
  console.log(JSON.stringify(meta));
}
