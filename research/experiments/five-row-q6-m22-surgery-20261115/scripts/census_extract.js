function gcdN(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { const t = a % b; a = b; b = t; } return a || 1; }
function isqrt(n) { if (n < 0) return -1; let r = Math.floor(Math.sqrt(n)); while (r * r > n) r--; while ((r + 1) * (r + 1) <= n) r++; return r; }

// Exact chord-pair census port (genfast3 / sa_machine_incremental.js lineage).
function buildCensus(w, m, q) {
  const curves = [];
  if (m >= q) for (let y = 0; y < w; y++) { const pts = []; for (let x = 0; x < m; x++) pts.push(y * m + x); curves.push(Int32Array.from(pts)); }
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
        for (let oi = 0; oi < no; oi++) {
          let k = -1;
          const E = cbuf[oi] + d1buf[oi] * Dl;
          if (E >= 0 && E % dy === 0) { const Q0 = E / dy, s = isqrt(Q0); if (s * s === Q0 && (s & 1) === lpar) k = s; }
          kbuf[oi] = k; if (k >= 0) nc++;
        }
        if (nc < needExtra) continue;
        for (let j = jlo; j <= jhi; j += 2) {
          let cnt = 4;
          for (let oi = 0; oi < no; oi++) { const k = kbuf[oi]; if (k < 0) continue; if (k === 0) cnt++; else { const x1 = (j - k) >> 1, x2 = (j + k) >> 1; if (x1 >= 0) cnt++; if (x2 <= m - 1) cnt++; } }
          if (cnt < q) continue;
          const pts = [];
          pts.push(ya * m + ((j - l) >> 1), ya * m + ((j + l) >> 1));
          pts.push(yb * m + ((j - lp) >> 1), yb * m + ((j + lp) >> 1));
          for (let oi = 0; oi < no; oi++) {
            const k = kbuf[oi]; if (k < 0) continue; const y = obuf[oi];
            if (k === 0) pts.push(y * m + (j >> 1));
            else { const x1 = (j - k) >> 1, x2 = (j + k) >> 1; if (x1 >= 0) pts.push(y * m + x1); if (x2 <= m - 1) pts.push(y * m + x2); }
          }
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
  for (const pts of found.values()) curves.push(Int32Array.from(pts));
  const N = w * m;
  const pcCount = new Int32Array(N);
  for (const c of curves) for (const p of c) pcCount[p]++;
  const pcOff = new Int32Array(N + 1); for (let p = 0; p < N; p++) pcOff[p + 1] = pcOff[p] + pcCount[p];
  const pcArr = new Int32Array(pcOff[N]);
  { let t = 0; const fl = new Int32Array(N); for (let ci = 0; ci < curves.length; ci++) for (const p of curves[ci]) { pcArr[pcOff[p] + fl[p]] = ci; fl[p]++; } }
  return { N, nC: curves.length, nCirc: found.size, curves, pcOff, pcArr };
}
module.exports = { buildCensus, gcdN, isqrt };
