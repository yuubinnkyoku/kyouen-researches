// genfast3.js — chord-pair abstract-circle census for w×m q-point instances, q >= w+2.
//
// Replaces the O(w·m³) pair scan of genfast.js/genfast2.js with an O(C(w,2)·m²·w)
// enumeration, making m=612 generation ~seconds instead of ~minutes.
//
// Completeness argument (q >= w+2 forced):
//   A circle meets any horizontal row in <= 2 grid points. A q-point circle over w rows
//   with at most one double row (row containing 2 of its points) has at most
//   2 + (w-1) = w+1 < q points (q >= w+2). Hence EVERY q-point circle has >= 2
//   DOUBLE ROWS. For a double row y, the two points are symmetric about the center:
//   x = u ± ℓ/2 with ℓ = x2 - x1 ∈ Z>=1 and u = (x1+x2)/2. For two double rows
//   (ya, yb) of the SAME circle, the shared center u forces ℓ ≡ ℓ' (mod 2)
//   (both u ± ℓ/2 and u ± ℓ'/2 must be integers), and the center y-coordinate and
//   radius² are determined u-INDEPENDENTLY:
//     v   = [ℓ'² - ℓ² + 4δ(ya+yb)] / (8δ),   δ = yb - ya,
//     ρ²  = ℓ²/4 + (ya - v)².
//   So the abstract circle (v, ρ²) is determined by (ya, yb, ℓ, ℓ') alone; enumerate
//   all quadruples (with ℓ ≡ ℓ' mod 2). Exact integer arithmetic: with
//     P := 8δv = ℓ'² - ℓ² + 4δ(ya+yb) ∈ Z,
//     A := 64δ²ρ² = 16δ²ℓ² + (8δya - P)² ∈ Z,
//   row y contributes iff its offset t = sqrt(ρ² - (y-v)²) is a half-integer k/2:
//     64δ²t² = B := A - (8δy - P)² must be the perfect square (4δk)²,
//   and grid points x = u ± k/2 are integers iff k ≡ j (mod 2), u = j/2.
//   The two chord rows always contribute (k = ℓ, ℓ'). Remaining freedom: u = j/2 with
//   j ∈ [max(ℓ,ℓ'), 2(m-1)-max(ℓ,ℓ')], j ≡ ℓ (mod 2) (window keeps both chords
//   in [0, m-1]). Per candidate we scan the window and keep the circle iff the
//   in-window grid point count is >= q.
// Prefilter: with c extra matching rows beyond the 2 chord rows, points <= 4 + 2c,
//   so a candidate needs c >= ceil((q-4)/2) — cheap necessary condition before the scan.
//
// Lines: for q >= w+1 (implied by q >= w+2) the only lines carrying >= q grid
// points are the w horizontal rows (a non-horizontal line meets each row in <= 1
// point, hence <= w < q points), so the line census is built directly from the
// rows instead of the O(n²) pair scan — byte-identity with the pair-based
// census validated on all controls below.
//
// Curve ORDER replicates genfast.js/buildCensus EXACTLY (lines sorted by their two
// smallest point indices, circles by their three smallest, all lines before all
// circles), so the CNF is byte-identical given the same curve set (validated by cmp
// against genfast.js / genfast2.js on samples; see output/controls).
//
// Usage: node genfast3.js w m q [--deficient|--cap=K] [--counter=seq|tot]
//                            [--lex=H,V,HV] [--rowY=Y] out.cnf
// Requires q >= w+2 (asserts; at q = w+1 a q-point circle may have a single double
// row — use genfast.js/genfast2.js there).
'use strict';
const path = require('path');
const SEVEN = process.env.SEVEN_SCRIPTS || '/home/user/krwork/seven/scripts';
const S = require(path.join(SEVEN, 'sat.js'));
const S2 = require(path.join(SEVEN, 'sat2.js'));

function isqrt(n) { // exact floor sqrt for integer n < 2^53
  let s = Math.sqrt(n) | 0;
  while (s > 0 && s * s > n) s--;
  while ((s + 1) * (s + 1) <= n) s++;
  return s;
}

function fastCensus3(w, m, q) {
  if (q < w + 2) throw new Error('genfast3 requires q >= w+2 (w=' + w + ', q=' + q + '); single-double-row circles possible at q=w+1 — use genfast/genfast2');
  const P = S.pts(w, m), n = P.length;

  // ---- lines: for q >= w+1 (implied by the q >= w+2 requirement) the only lines with
  // >= q grid points are the w horizontal rows: any non-horizontal line meets each of
  // the w rows in <= 1 point, hence carries <= w < q points. So the line census is
  // exactly the rows with m >= q points, in row order (= the original pair-based
  // enumeration's result for these parameters; byte-identity validated on samples).
  const lines = [];
  if (m >= q) {
    for (let y = 0; y < w; y++) {
      const pts = new Array(m);
      for (let x = 0; x < m; x++) pts[x] = y * m + x;
      const lo = S.lineABC(P[pts[0]], P[pts[1]]);
      lines.push({ type: 'line', co: lo, pts: pts });
    }
  }

  // ---- circles: chord-pair abstract enumeration ----
  // Closed form used in the inner loop (identical B, algebraically expanded):
  //   B_y = A - (8δy-P)² = 16δ·E_y,  E_y = δℓ² + 4δ(ya-y)(y-yb) + (ya-y)(ℓ²-ℓ'²),
  // and the perfect-square test B_y = (4δk)² becomes E_y = δk².
  const found = new Map(); // canonical co key -> {type:'circle', co, pts}
  const needExtra = Math.ceil((q - 4) / 2); // necessary extras beyond the 2 chord rows
  const kbuf = new Int32Array(w); // per orow: k (>=0) or -1
  const obuf = new Int32Array(w); // orow y values
  const d1buf = new Int32Array(w); // ya - y
  const bbuf = new Int32Array(w);  // 4δ(ya-y)(y-yb)
  const cbuf = new Int32Array(w);  // per-l: 4δ(ya-y)(y-yb) + δℓ²

  for (let ya = 0; ya < w; ya++) {
    for (let yb = ya + 1; yb < w; yb++) {
      const dy = yb - ya;
      const d4 = 4 * dy;
      let no = 0;
      for (let y = 0; y < w; y++) if (y !== ya && y !== yb) {
        obuf[no] = y;
        d1buf[no] = ya - y;
        bbuf[no] = d4 * (ya - y) * (y - yb);
        no++;
      }
      for (let l = 1; l <= m - 1; l++) {
        const l2 = l * l;
        const lpar = l & 1;
        const dl2 = dy * l2;
        for (let oi = 0; oi < no; oi++) cbuf[oi] = bbuf[oi] + dl2; // E_y base = δℓ² + 4δ(ya-y)(y-yb)
        for (let lp = lpar ? 1 : 2; lp <= m - 1; lp += 2) { // lp ≡ l (mod 2)
          const mx = l > lp ? l : lp;
          const jlo = mx, jhi = 2 * (m - 1) - mx;
          if (jlo > jhi) continue;
          const Dl = l2 - lp * lp; // ℓ² - ℓ'²
          let nc = 0;
          for (let oi = 0; oi < no; oi++) {
            let k = -1;
            const E = cbuf[oi] + d1buf[oi] * Dl;
            if (E >= 0 && E % dy === 0) {
              const Q = E / dy; // must be k²
              const s = isqrt(Q);
              if (s * s === Q && (s & 1) === lpar) k = s;
            }
            kbuf[oi] = k;
            if (k >= 0) nc++;
          }
          if (nc < needExtra) continue;
          // window scan: u = j/2, j ≡ l (mod 2), j in [jlo, jhi]
          for (let j = jlo; j <= jhi; j += 2) {
            let cnt = 4; // two chord rows: both endpoints always in-window here
            for (let oi = 0; oi < no; oi++) {
              const k = kbuf[oi];
              if (k < 0) continue;
              if (k === 0) cnt++; // x = j/2, in-window by j <= 2m-2 (j even since lpar=0)
              else {
                const x1 = (j - k) >> 1, x2 = (j + k) >> 1;
                if (x1 >= 0) cnt++;
                if (x2 <= m - 1) cnt++;
              }
            }
            if (cnt < q) continue;
            // build pts (sorted ascending row-major indices)
            const pts = [];
            pts.push(ya * m + ((j - l) >> 1), ya * m + ((j + l) >> 1));
            pts.push(yb * m + ((j - lp) >> 1), yb * m + ((j + lp) >> 1));
            for (let oi = 0; oi < no; oi++) {
              const k = kbuf[oi];
              if (k < 0) continue;
              const y = obuf[oi];
              if (k === 0) pts.push(y * m + (j >> 1));
              else {
                const x1 = (j - k) >> 1, x2 = (j + k) >> 1;
                if (x1 >= 0) pts.push(y * m + x1);
                if (x2 <= m - 1) pts.push(y * m + x2);
              }
            }
            pts.sort((a, b) => a - b);
            const co = S.circleABC(P[pts[0]], P[pts[1]], P[pts[2]]);
            const ck = co.join(',');
            if (!found.has(ck)) found.set(ck, { type: 'circle', co: co, pts: pts });
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
S.buildCensus = fastCensus3;

if (require.main === module) {
  const t0 = Date.now();
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
  meta.generator = 'genfast3';
  meta.gen_sec = ((Date.now() - t0) / 1000).toFixed(1);
  console.log(JSON.stringify(meta));
}
module.exports = { fastCensus3 };
