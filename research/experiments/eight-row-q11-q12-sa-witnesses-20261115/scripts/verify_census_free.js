#!/usr/bin/env node
// Census-free, integer-only verifier for (safe, maximal) claims on w x m boards.
// safety  : every row holds <= q-1 stones; every non-horizontal line holds <= q-1 stones
//           (at w=8 lines hold <= 8 grid points, vacuous for q>=11 but checked anyway);
//           every circle through >= 3 stones holds <= q-1 stones (all stone triples,
//           exact cross-multiplied circle equation, no census consulted).
// maximality: every non-stone point f is blocked: rowCount(f.row) == q-1, or some circle
//           through f (enumerated via f + stone pairs) already holds q-1 stones.
// Circle identity: (d, ux, uy, r^2) normalized by gcd, sign of d > 0.
// Usage: node verify_census_free.js <w> <m> <q> <p1,p2,...>   (0-indexed row-major points)
"use strict";
const [W, M, Q, PTS] = process.argv.slice(2);
const w = Number(W), m = Number(M), q = Number(Q);
const S = String(PTS).split(',').map(Number);
function gcdN(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { const t = a % b; a = b; b = t; } return a || 1; }
const N = w * m, nS = S.length;
const stone = new Uint8Array(N); for (const p of S) stone[p] = 1;
const X = new Int32Array(nS), Y = new Int32Array(nS);
for (let i = 0; i < nS; i++) { X[i] = S[i] % m; Y[i] = Math.floor(S[i] / m); }
const rowCount = new Int32Array(w); for (let i = 0; i < nS; i++) rowCount[Y[i]]++;
const rowsOK = Array.from(rowCount).every(c => c <= q - 1);
let maxCirc = 0, unsafeCirc = 0;
for (let a = 0; a < nS; a++) {
  const x1 = X[a], y1 = Y[a], s1 = x1 * x1 + y1 * y1;
  for (let b = a + 1; b < nS; b++) {
    const x2 = X[b], y2 = Y[b], s2 = x2 * x2 + y2 * y2;
    for (let c = b + 1; c < nS; c++) {
      const x3 = X[c], y3 = Y[c];
      if ((y2 - y1) * (x3 - x1) === (y3 - y1) * (x2 - x1)) continue;
      const d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2));
      const s3 = x3 * x3 + y3 * y3;
      const ux = s1 * (y2 - y3) + s2 * (y3 - y1) + s3 * (y1 - y2);
      const uy = s1 * (x3 - x2) + s2 * (x1 - x3) + s3 * (x2 - x1);
      const qx = x1 * d - ux, qy = y1 * d - uy, r2 = qx * qx + qy * qy;
      let dd = d, uu = ux, vv = uy, rr = r2;
      const g = gcdN(gcdN(Math.abs(dd), Math.abs(uu)), Math.abs(vv));
      dd /= g; uu /= g; vv /= g; rr /= g * g;
      if (dd < 0) { dd = -dd; uu = -uu; vv = -vv; }
      let cnt = 0;
      for (let t = 0; t < nS; t++) { const xx = X[t] * dd - uu, yy = Y[t] * dd - vv; if (xx * xx + yy * yy === rr) cnt++; }
      if (cnt > maxCirc) maxCirc = cnt;
      if (cnt >= q) unsafeCirc++;
    }
  }
}
let maxLine = 0, unsafeLine = 0;
for (let a = 0; a < nS; a++) for (let b = a + 1; b < nS; b++) {
  let dx = X[b] - X[a], dy = Y[b] - Y[a];
  if (dx === 0 && dy === 0) continue;
  const g = gcdN(dx, dy); dx /= g; dy /= g;
  if (dx < 0 || (dx === 0 && dy < 0)) { dx = -dx; dy = -dy; }
  if (dy === 0) continue; // horizontal rows are covered by rowCount
  let cnt = 0;
  for (let t = 0; t < nS; t++) { const tx = X[t] - X[a], ty = Y[t] - Y[a]; if (tx * dy - ty * dx === 0) cnt++; }
  if (cnt > maxLine) maxLine = cnt;
  if (cnt >= q) unsafeLine++;
}
const unblocked = [];
for (let f = 0; f < N; f++) {
  if (stone[f]) continue;
  const fx = f % m, fy = Math.floor(f / m);
  let blocked = rowCount[fy] === q - 1;
  if (!blocked) {
    const sf = fx * fx + fy * fy;
    outer: for (let a = 0; a < nS; a++) {
      const x1 = X[a], y1 = Y[a], s1 = x1 * x1 + y1 * y1;
      for (let b = a + 1; b < nS; b++) {
        const x2 = X[b], y2 = Y[b];
        if ((y2 - y1) * (fx - x1) === (fy - y1) * (x2 - x1)) continue;
        const s2 = x2 * x2 + y2 * y2;
        const d = 2 * (x1 * (y2 - fy) + x2 * (fy - y1) + fx * (y1 - y2));
        const ux = s1 * (y2 - fy) + s2 * (fy - y1) + sf * (y1 - y2);
        const uy = s1 * (fx - x2) + s2 * (x1 - fx) + sf * (x2 - x1);
        const qx = x1 * d - ux, qy = y1 * d - uy, r2 = qx * qx + qy * qy;
        let dd = d, uu = ux, vv = uy, rr = r2;
        const g = gcdN(gcdN(Math.abs(dd), Math.abs(uu)), Math.abs(vv));
        dd /= g; uu /= g; vv /= g; rr /= g * g;
        if (dd < 0) { dd = -dd; uu = -uu; vv = -vv; }
        let cnt = 0;
        for (let t = 0; t < nS; t++) { const xx = X[t] * dd - uu, yy = Y[t] * dd - vv; if (xx * xx + yy * yy === rr) cnt++; }
        if (cnt >= q - 1) { blocked = true; break outer; }
      }
    }
  }
  if (!blocked) unblocked.push(f);
}
const full = w * Math.min(m, q - 1);
console.log(JSON.stringify({
  w, m, q, stones: nS, full, deficient: full - nS, row_counts: Array.from(rowCount),
  safe: rowsOK && unsafeCirc === 0 && unsafeLine === 0,
  rows_ok: rowsOK, max_circle_stones: maxCirc, unsafe_circle_triples: unsafeCirc,
  max_line_nonh: maxLine, unsafe_line_pairs: unsafeLine,
  maximal: unblocked.length === 0, unblocked_sample: unblocked.slice(0, 8)
}));
if (!(rowsOK && unsafeCirc === 0 && unsafeLine === 0 && unblocked.length === 0)) process.exit(1);
