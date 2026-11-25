#!/usr/bin/env node
// Complete chord-pair census of forbidden curves (rows when m >= q, plus all circles with
// >= q grid points), with per-circle row-coverage analysis and optional full 3-point-group
// brute-force cross-check. Used to establish the twelve-point family characterization
// (see report.md and output/census_structure.json).
// Usage: node census_family_check.js <w> <q> <m...> [--bf]
"use strict";
const args = process.argv.slice(2).filter(a => a !== '--bf');
const bf = process.argv.includes('--bf');
const w = Number(args[0]), q = Number(args[1]);
function gcdN(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { const t = a % b; a = b; b = t; } return a || 1; }
function isqrt(n) { if (n < 0) return -1; let r = Math.floor(Math.sqrt(n)); while (r * r > n) r--; while ((r + 1) * (r + 1) <= n) r++; return r; }
function chordCensus(m) { /* same chord-pair enumeration as sa_machine_incremental.js; returns Map key->pts */
  const needExtra = Math.ceil((q - 4) / 2);
  const kbuf = new Int32Array(w), obuf = new Int32Array(w), d1buf = new Int32Array(w), bbuf = new Int32Array(w), cbuf = new Int32Array(w);
  const px = (i) => i % m, py = (i) => Math.floor(i / m);
  const found = new Map();
  for (let ya = 0; ya < w; ya++) for (let yb = ya + 1; yb < w; yb++) {
    const dy = yb - ya, d4 = 4 * dy;
    let no = 0;
    for (let y = 0; y < w; y++) if (y !== ya && y !== yb) { obuf[no] = y; d1buf[no] = ya - y; bbuf[no] = d4 * (ya - y) * (y - yb); no++; }
    for (let l = 1; l <= m - 1; l++) {
      const l2 = l * l, lpar = l & 1, dl2 = dy * l2;
      for (let oi = 0; oi < no; oi++) cbuf[oi] = bbuf[oi] + dl2;
      for (let lp = lpar ? 1 : 2; lp <= m - 1; lp += 2) {
        const mx = l > lp ? l : lp, jlo = mx, jhi = 2 * (m - 1) - mx;
        if (jlo > jhi) continue;
        const Dl = l2 - lp * lp;
        let nc = 0;
        for (let oi = 0; oi < no; oi++) { let k = -1; const E = cbuf[oi] + d1buf[oi] * Dl; if (E >= 0 && E % dy === 0) { const Q0 = E / dy, s = isqrt(Q0); if (s * s === Q0 && (s & 1) === lpar) k = s; } kbuf[oi] = k; if (k >= 0) nc++; }
        if (nc < needExtra) continue;
        for (let j = jlo; j <= jhi; j += 2) {
          let cnt = 4;
          for (let oi = 0; oi < no; oi++) { const k = kbuf[oi]; if (k < 0) continue; if (k === 0) cnt++; else { const x1 = (j - k) >> 1, x2 = (j + k) >> 1; if (x1 >= 0) cnt++; if (x2 <= m - 1) cnt++; } }
          if (cnt < q) continue;
          const pts = [];
          pts.push(ya * m + ((j - l) >> 1), ya * m + ((j + l) >> 1));
          pts.push(yb * m + ((j - lp) >> 1), yb * m + ((j + lp) >> 1));
          for (let oi = 0; oi < no; oi++) { const k = kbuf[oi]; if (k < 0) continue; const y = obuf[oi]; if (k === 0) pts.push(y * m + (j >> 1)); else { const x1 = (j - k) >> 1, x2 = (j + k) >> 1; if (x1 >= 0) pts.push(y * m + x1); if (x2 <= m - 1) pts.push(y * m + x2); } }
          pts.sort((a, b) => a - b);
          const x1 = px(pts[0]), y1 = py(pts[0]), x2 = px(pts[1]), y2 = py(pts[1]), x3 = px(pts[2]), y3 = py(pts[2]);
          const d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2));
          const s1 = x1 * x1 + y1 * y1, s2 = x2 * x2 + y2 * y2, s3 = x3 * x3 + y3 * y3;
          const ux = s1 * (y2 - y3) + s2 * (y3 - y1) + s3 * (y1 - y2), uy = s1 * (x3 - x2) + s2 * (x1 - x3) + s3 * (x2 - x1);
          const qx = x1 * d - ux, qy = y1 * d - uy, rr0 = qx * qx + qy * qy;
          let dd = d, uu = ux, vv = uy;
          const g = gcdN(gcdN(Math.abs(dd), Math.abs(uu)), Math.abs(vv));
          dd /= g; uu /= g; vv /= g;
          if (dd < 0) { dd = -dd; uu = -uu; vv = -vv; }
          const key = dd + ',' + uu + ',' + vv + ',' + (rr0 / (g * g));
          if (!found.has(key)) found.set(key, pts);
        }
      }
    }
  }
  return found;
}
function bruteForce(m) { /* all C(N,3) triples; stores only circles with >= q grid points */
  const N = w * m;
  const X = new Int32Array(N), Y = new Int32Array(N);
  for (let p = 0; p < N; p++) { X[p] = p % m; Y[p] = Math.floor(p / m); }
  const found = new Map();
  for (let a = 0; a < N; a++) { const x1 = X[a], y1 = Y[a], s1 = x1 * x1 + y1 * y1;
    for (let b = a + 1; b < N; b++) { const x2 = X[b], y2 = Y[b], s2 = x2 * x2 + y2 * y2;
      for (let c = b + 1; c < N; c++) { const x3 = X[c], y3 = Y[c];
        if ((y2 - y1) * (x3 - x1) === (y3 - y1) * (x2 - x1)) continue;
        const d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2));
        if (d === 0) continue;
        const s3 = x3 * x3 + y3 * y3;
        const ux = s1 * (y2 - y3) + s2 * (y3 - y1) + s3 * (y1 - y2);
        const uy = s1 * (x3 - x2) + s2 * (x1 - x3) + s3 * (x2 - x1);
        const qx = x1 * d - ux, qy = y1 * d - uy, r2 = qx * qx + qy * qy;
        if (r2 <= 0) continue;
        let dd = d, uu = ux, vv = uy, rr = r2;
        const g = gcdN(gcdN(Math.abs(dd), Math.abs(uu)), Math.abs(vv));
        dd /= g; uu /= g; vv /= g; rr /= g * g;
        if (dd < 0) { dd = -dd; uu = -uu; vv = -vv; }
        const key = dd + ',' + uu + ',' + vv + ',' + rr;
        if (found.has(key)) continue;
        let cnt = 0;
        for (let p = 0; p < N; p++) { const xx = X[p] * dd - uu, yy = Y[p] * dd - vv; if (xx * xx + yy * yy === rr) cnt++; }
        if (cnt >= q) found.set(key, cnt);
      }
    }
  }
  return found;
}
for (const argM of args.slice(2)) {
  const m = Number(argM);
  const cc = chordCensus(m);
  const rowsets = {}, sizes = {};
  for (const pts of cc.values()) {
    const rs = Array.from(new Set(pts.map(p => Math.floor(p / m)))).sort((a, b) => a - b).join('');
    rowsets[rs] = (rowsets[rs] || 0) + 1;
    sizes[pts.length] = (sizes[pts.length] || 0) + 1;
  }
  const rec = { w, q, m, circles: cc.size, expect_family: m - 7, sizes, rowsets };
  if (bf) {
    const b = bruteForce(m);
    const a1 = Array.from(cc.keys()).sort(), a2 = Array.from(b.keys()).sort();
    rec.brute_force = { circles: b.size, key_identical: JSON.stringify(a1) === JSON.stringify(a2) };
  }
  console.log(JSON.stringify(rec));
}
