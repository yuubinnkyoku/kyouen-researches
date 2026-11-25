// ts_verify_census5q7.js — third-system independent (5,m,7) forbidden-curve census.
// Method-disjoint from BOTH sat2.js (all-triples census) and genfast3.js (chord-pair
// abstract circles): enumerates every circle as circle(P1,P2,Q) with P1,P2 a horizontal
// chord of row ya and Q in a different row. Completeness: a >=7-point circle in a
// 5-row window has <=2 points per row, hence >=2 double rows (a horizontal chord);
// with >=7 points over <=2/row it touches >=4 rows, so a point Q outside the chord
// row exists and the circle through (P1,P2,Q) is unique and genuine (P1,P2,Q are
// never collinear). Lines: for q=7>=w+2 the only lines with >=7 window points are
// the 5 horizontal rows. Exact integer arithmetic via B = 4*del*b scaling.
// Usage: node ts_verify_census5q7.js M [M2]   (w=5, q=7 fixed)
'use strict';
function isqrt(n) { let s = Math.sqrt(n) | 0; while (s > 0 && s * s > n) s--; while ((s + 1) * (s + 1) <= n) s++; return s; }
function census(w, m, q) {
  const seen = new Set();
  let circles = 0;
  const lineCt = (m >= q) ? w : 0;
  for (let ya = 0; ya < w; ya++) {
    for (let x1 = 0; x1 < m; x1++) {
      for (let x2 = x1 + 1; x2 < m; x2++) {
        const a = x1 + x2;
        const dd = (x1 - x2) * (x1 - x2);
        for (let yb = 0; yb < w; yb++) {
          if (yb === ya) continue;
          const del = ya - yb;
          const D = 4 * del;
          const AD = Math.abs(D);
          for (let x3 = 0; x3 < m; x3++) {
            const t = 2 * x3 - a;
            const B = dd - t * t + 4 * (ya * ya - yb * yb);
            const RHS = D * D * dd + (2 * D * ya - B) * (2 * D * ya - B);
            const pts = [];
            for (let y = 0; y < w; y++) {
              const K = RHS - (2 * D * y - B) * (2 * D * y - B);
              if (K < 0) continue;
              const s = isqrt(K);
              if (s * s !== K) continue;
              if (s % AD !== 0) continue;
              const dvals = (s === 0) ? [0] : [s / D, -s / D];
              for (const dv of dvals) {
                const xx = (a + dv) / 2;
                if (Number.isInteger(xx) && xx >= 0 && xx < m) {
                  const idx = y * m + xx;
                  if (!pts.includes(idx)) pts.push(idx);
                }
              }
            }
            if (pts.length >= q) {
              pts.sort((p1, p2) => p1 - p2);
              const key = pts.join(',');
              if (!seen.has(key)) { seen.add(key); circles++; }
            }
          }
        }
      }
    }
  }
  return { m, lines: lineCt, circles, total: lineCt + circles };
}
const [M1, M2] = [Number(process.argv[2]), Number(process.argv[3] || process.argv[2])];
for (let m = M1; m <= M2; m++) console.log(JSON.stringify(census(5, m, 7)));
