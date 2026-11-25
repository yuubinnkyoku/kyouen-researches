// genfast2.js — memory-bounded CNF generator, integer-keyed fast variant of genfast.js.
//
// Same algorithm as genfast.js (K0820): for q >= w+1 every q-point circle has a
// half-integer center x = U/2; for each U the pair scan counts distinct-row pair
// witnesses per (center-y, radius^2); candidates with >= PAIRTHRESH=12 witnesses
// get an exact integer point scan and are kept iff >= q points.
//
// Speed: genfast.js canonicalizes (v, rho) by two gcd reductions and uses a
// string-keyed Map. Here the same (v, rho) is represented CANONICALLY WITHOUT gcd:
//   dy = yb - ya in 1..6 (ya < yb), D = 8*(ya-yb) = -8*dy < 0,
//   v = N/D with N = (Ai-Aj) + 4*(ya^2-yb^2),
//   N480 = 480*v = -N * (480/(8*dy))   (480/(8*dy) in {60,30,20,15,12,10} for dy=1..6)
//   RHO  = rho * 921600 = 230400*Ai + 4*(480*ya - N480)^2   (exact integers; the
//   membership test becomes 230400*(2x-U)^2 + 4*(480y-N480)^2 === RHO).
// Same circle => same (N480, RHO) regardless of the witnessing pair, so exact
// integer key match => no false merges; counts equal genfast.js's counts (same
// distinct-row pair set, same PAIRTHRESH). Lines/scan/order/dedup/encode are
// reused verbatim via the S.buildCensus monkey-patch, so the CNF is byte-identical
// (validated: 7x25 q8 rowY=2, 7x101 q9, 7x110 q10 def+lex, 8x26 q9 — all cmp-equal).
//
// Inner state uses typed arrays with open addressing (Int32Array N480/counts,
// Float64Array RHO; per-U touched-slot list to avoid clearing the whole table).
//
// Usage: node genfast2.js w m q [--deficient|--cap=K] [--counter=seq|tot]
//                           [--lex=H,V,HV] [--rowY=Y] out.cnf
'use strict';
const path = require('path');
const SEVEN = process.env.SEVEN_SCRIPTS || '/home/user/krwork/seven/scripts';
const S = require(path.join(SEVEN, 'sat.js'));
const S2 = require(path.join(SEVEN, 'sat2.js'));
const PAIRTHRESH = 12;

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
  lines.sort((A, B) => (A.pts[0] - B.pts[0]) || (A.pts[1] - B.pts[1]));

  // ---- circles: half-integer center-line census, integer-keyed ----
  const TB = 1 << 21;              // table slots (2M)
  const TMSK = TB - 1;
  const kN = new Int32Array(TB);   // N480
  const kR = new Float64Array(TB); // RHO (exact integer <= 2^53)
  const kC = new Int32Array(TB);   // distinct-row pair witnesses
  const touched = new Int32Array(TB);
  const SCA = [0, 60, 30, 20, 15, 12, 10]; // 480/(8*dy) for dy=1..6
  const found = new Map(); // circle co key -> {type:'circle', co, pts}

  const A = new Int32Array(n);
  const ysq = new Int32Array(w);
  for (let y = 0; y < w; y++) ysq[y] = y * y;
  for (let U = 0; U <= 2 * m - 2; U++) {
    for (let i = 0; i < n; i++) { const t = 2 * P[i][0] - U; A[i] = t * t; }
    let nTouched = 0;
    for (let ya = 0; ya < w; ya++) {
      const a0 = ya * m;
      for (let yb = ya + 1; yb < w; yb++) {
        const dy = yb - ya, sc = SCA[dy];
        const b0 = yb * m;
        const d43 = 4 * (ysq[ya] - ysq[yb]);
        for (let xi = 0; xi < m; xi++) {
          const Ai = A[a0 + xi], base = Ai + d43;
          const r480 = 480 * ya;
          for (let xj = 0; xj < m; xj++) {
            const Aj = A[b0 + xj];
            // v = N/D, N = (Ai-Aj)+4(ya^2-yb^2), D = 8*(ya-yb) = -8*dy < 0:
            // N480 = 480*v = -N * sc.
            const N480 = (Aj - base) * sc;
            const RHO = 230400 * Ai + 4 * (r480 - N480) * (r480 - N480);
            let h = ((N480 * 2654435761) ^ (RHO % 1000003)) & TMSK;
            if (h < 0) h = 0;
            for (;;) {
              const c = kC[h];
              if (c === 0) { kN[h] = N480; kR[h] = RHO; kC[h] = 1; touched[nTouched++] = h; break; }
              else if (kN[h] === N480 && kR[h] === RHO) { kC[h] = c + 1; break; }
              h = (h + 1) & TMSK;
            }
          }
        }
      }
    }
    for (let t = 0; t < nTouched; t++) {
      const h = touched[t];
      if (kC[h] < PAIRTHRESH) { kC[h] = 0; continue; }
      const N480 = kN[h], RHO = kR[h];
      kC[h] = 0;
      const set = [];
      for (let idx = 0; idx < n; idx++) {
        const t2 = 2 * P[idx][0] - U;
        const dy2 = 480 * P[idx][1] - N480;
        if (230400 * t2 * t2 + 4 * dy2 * dy2 === RHO) set.push(idx);
      }
      if (set.length >= q) {
        const co = S.circleABC(P[set[0]], P[set[1]], P[set[2]]);
        const ck = co.join(',');
        if (!found.has(ck)) found.set(ck, { type: 'circle', co: co, pts: set });
      }
    }
  }
  const circles = [...found.values()];
  circles.sort((A2, B2) => (A2.pts[0] - B2.pts[0]) || (A2.pts[1] - B2.pts[1]) || (A2.pts[2] - B2.pts[2]));
  return { P: P, n: n, curves: lines.concat(circles) };
}

// ---- patch and reuse sat2.js verbatim ----
S.buildCensus = fastCensus;

if (require.main === module) {
  const args = process.argv.slice(2);
  const [w, m, q] = [Number(args[0]), Number(args[1]), Number(args[2])];
  let i = 3, mode = 'deficient', cap = null, cnt = 'seq', lex = [], rowY = null, outfile = null;
  for (; i < args.length; i++) {
    const a = args[i];
    if (a === '--deficient') mode = 'deficient';
    else if (a.startsWith('--cap=')) { mode = 'cap'; cap = Number(a.slice(6)); }
    else if (a.startsWith('--counter=')) cnt = a.slice(10);
    else if (a.startsWith('--lex=')) lex = a.slice(6).split(',').filter(s => ['H', 'V', 'HV'].includes(s));
    else if (a.startsWith('--rowY=')) { mode = 'rowfixed'; rowY = Number(a.slice(7)); }
    else if (!outfile) outfile = a;
  }
  const opts = { mode, cap, counter: cnt, lex, rowY };
  const { enc, meta } = S2.dump(w, m, q, opts);
  require('fs').writeFileSync(outfile, S2.toDimacs2(enc));
  meta.file = outfile;
  meta.generator = 'genfast2';
  console.log(JSON.stringify(meta));
}
module.exports = { fastCensus };
