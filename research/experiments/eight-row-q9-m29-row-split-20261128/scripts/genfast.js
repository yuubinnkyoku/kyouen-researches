// genfast.js — memory-bounded CNF generator for w×m q-point deficient/cap instances.
//
// Problem: sat2.js -> S.buildCensus enumerates ALL point triples to find circles
// (circMap of C(n,3) entries). For 7×52 (n=364) that is ~8.0M map entries and the
// node process is OOM-killed in this container at m=52 (m=51 with C(357,3)=7.5M
// still fits). The CNF itself is tiny (8k vars / 29k clauses) — only the census
// blows up.
//
// Fast census (this file) finds every circle with >= q points in O((2m)·n^2) time
// and O(n^2) memory, for q >= w+1:
//   A circle meets any row (horizontal line) in <= 2 grid points, so a circle with
//   q >= w+1 points has two points in the same row (pigeonhole over w rows). Its
//   center then lies on the vertical perpendicular bisector of that pair, i.e. the
//   center x-coordinate u = (x_a+x_b)/2 is a multiple of 1/2 in [0, m-1].
//   For fixed u, every distinct-row pair (p,q) of its grid points solves the
//   center y-coordinate v exactly (rational, denominator |8(y_p-y_q)| reduced), so
//   the true circle accumulates many pair-witnesses; candidates with >= PAIRTHRESH
//   witnesses get an exact integer point-set scan and are kept iff >= q points.
//   Minimum distinct-row pair witnesses of a q-point circle = C(q,2)-(q-w) >= 13
//   for all (w,q) used here, far above PAIRTHRESH=12. Line curves reuse the
//   original pair-based enumeration verbatim (O(n^2) map, fits comfortably).
//
// Curve order replicates buildCensus EXACTLY (verified byte-identical CNF against
// sat2.js for 12 (w,m,q) samples, see report.md): the original inserts a line at
// its first pair in lexicographic (i<j) pair order and a circle at its first
// triple in lexicographic (i<j<k) triple order — i.e. lines sorted by their two
// smallest point indices, circles by their three smallest; all lines before all
// circles. Everything downstream (encodeCore, sequential/totalizer counters,
// deficient clause, lex-leader, DIMACS writer) is reused VERBATIM from sat2.js by
// monkey-patching S.buildCensus — zero encoding drift.
//
// Usage: node genfast.js w m q [--deficient|--cap=K] [--counter=seq|tot]
//                        [--lex=H,V,HV] [--rowY=Y] out.cnf
// Requires q >= w+1 (asserts; below that the half-integer-center guarantee fails —
// use sat2.js). SAT models decode identically (cell var i+1 = cell[y*m+x]).
'use strict';
const path = require('path');
const SEVEN = process.env.SEVEN_SCRIPTS || '/home/user/krwork/seven/scripts';
const S = require(path.join(SEVEN, 'sat.js'));
const S2 = require(path.join(SEVEN, 'sat2.js'));

function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { const t = a % b; a = b; b = t; } return a; }
const PAIRTHRESH = 12; // << 13 = min distinct-row pair witnesses of any q-point circle (q>=w+1, w<=7)

function fastCensus(w, m, q) {
  if (q < w + 1) throw new Error('genfast requires q >= w+1 (w=' + w + ', q=' + q + '); use sat2.js');
  const P = S.pts(w, m), n = P.length;

  // ---- lines: original pair-based enumeration, verbatim ----
  const lineMap = new Map();
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
    const lo = S.lineABC(P[i], P[j]);
    const key = lo[0] + ',' + lo[1] + ',' + lo[2];
    if (!lineMap.has(key)) lineMap.set(key, lo);
  }
  const lines = [];
  for (const lo of lineMap.values()) {
    const set = [];
    for (let idx = 0; idx < n; idx++) if (S.onLine(lo, P[idx][0], P[idx][1])) set.push(idx);
    if (set.length >= q) lines.push({ type: 'line', co: lo, pts: set });
  }
  lines.sort((A, B) => (A.pts[0] - B.pts[0]) || (A.pts[1] - B.pts[1])); // = original insertion order

  // ---- circles: half-integer center-line census ----
  const found = new Map(); // canonical 'a,b,c,d' -> {type:'circle', co, pts}
  for (let U = 0; U <= 2 * m - 2; U++) { // center x u = U/2
    const A = new Array(n);
    for (let i = 0; i < n; i++) A[i] = (2 * P[i][0] - U) * (2 * P[i][0] - U);
    const cnt = new Map(); // 'n/d|p/r' (reduced v=n/d, rho=p/r) -> distinct-row pair witnesses
    for (let i = 0; i < n; i++) {
      const yi = P[i][1], Ai = A[i], yi2 = yi * yi;
      for (let j = i + 1; j < n; j++) {
        const yj = P[j][1];
        if (yi === yj) continue;
        // v = [ (Ai-Aj) + 4(yi^2-yj^2) ] / [ 8(yi-yj) ]
        let N = (Ai - A[j]) + 4 * (yi2 - yj * yj);
        let D = 8 * (yi - yj);
        let g = gcd(N, D); if (g === 0) g = 1;
        N /= g; D /= g; if (D < 0) { N = -N; D = -D; }
        // rho = Ai/4 + (yi - N/D)^2 = [ Ai D^2 + 4(yi D - N)^2 ] / (4 D^2)
        const yd = yi * D - N;
        let Rp = Ai * D * D + 4 * yd * yd;
        let Qp = 4 * D * D;
        let g2 = gcd(Rp, Qp); if (g2 === 0) g2 = 1;
        Rp /= g2; Qp /= g2;
        const key = N + '/' + D + '|' + Rp + '/' + Qp;
        cnt.set(key, (cnt.get(key) || 0) + 1);
      }
    }
    for (const [key, c] of cnt) {
      if (c < PAIRTHRESH) continue;
      const [vs, rs] = key.split('|');
      const [nv, dv] = vs.split('/').map(Number);
      const [pr, qr] = rs.split('/').map(Number);
      const set = [];
      for (let idx = 0; idx < n; idx++) {
        const x = P[idx][0], y = P[idx][1];
        const dx2 = 2 * x - U;
        const yd = y * dv - nv;
        // on circle <=> dx2^2/4 + yd^2/dv^2 = pr/qr <=> dx2^2 dv^2 qr + 4 yd^2 qr = 4 dv^2 pr
        if (dx2 * dx2 * dv * dv * qr + 4 * yd * yd * qr === 4 * dv * dv * pr) set.push(idx);
      }
      if (set.length >= q) {
        const co = S.circleABC(P[set[0]], P[set[1]], P[set[2]]);
        const ck = co.join(',');
        if (!found.has(ck)) found.set(ck, { type: 'circle', co: co, pts: set });
      }
    }
  }
  const circles = [...found.values()];
  circles.sort((A, B) => (A.pts[0] - B.pts[0]) || (A.pts[1] - B.pts[1]) || (A.pts[2] - B.pts[2]));
  return { P: P, n: n, curves: lines.concat(circles) };
}

// ---- patch and reuse sat2.js verbatim ----
S.buildCensus = fastCensus;

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
  meta.generator = 'genfast';
  console.log(JSON.stringify(meta));
}
