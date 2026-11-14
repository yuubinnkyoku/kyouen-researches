// sa_machine.js — SA(シミュレーテッド・アニーリング)版 欠損極大witness探索機
// 由来: research/experiments/six-row-deficient-witnesses-20261113/scripts/deficient_maximal_machine.ts
//       (K0808) の buildCurves / verifyIndependent を機械的移植し、探索部を SA に置換した。
// census・独立検証器のロジックは verbatim 移植(バグ修正済み版: 接線二重追加防止・r^2/g^2)。
'use strict';
function gcdN(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { const t = a % b; a = b; b = t; } return a || 1; }
function isqrt(n) { if (n < 0) return -1; let r = Math.floor(Math.sqrt(n)); while (r * r > n) r--; while ((r + 1) * (r + 1) <= n) r++; return r; }

function buildCurves(w, m, q) {
  const N = w * m; const px = new Int32Array(N), py = new Int32Array(N);
  for (let y = 0; y < w; y++) for (let x = 0; x < m; x++) { px[x + m * y] = x; py[x + m * y] = y; }
  const lineKeys = new Set();
  for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++) {
    let dx = px[j] - px[i], dy = py[j] - py[i];
    const g = gcdN(dx, dy); dx /= g; dy /= g;
    if (dy < 0 || (dy === 0 && dx < 0)) { dx = -dx; dy = -dy; }
    lineKeys.add(`L${dx},${dy},${px[i] * dy - py[i] * dx}`);
  }
  const lines = [];
  for (const key of lineKeys) {
    const p = key.slice(1).split(',').map(Number);
    const dx = p[0], dyy = p[1], c = p[2];
    const pts = [];
    for (let i = 0; i < N; i++) { if (px[i] * dyy - py[i] * dx === c) pts.push(i); }
    if (pts.length >= q) lines.push(Int32Array.from(pts));
  }
  const keptC = new Map();
  for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++) for (let k = j + 1; k < N; k++) {
    const x1 = px[i], y1 = py[i], x2 = px[j], y2 = py[j], x3 = px[k], y3 = py[k];
    const d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)); if (d === 0) continue;
    const s1 = x1 * x1 + y1 * y1, s2 = x2 * x2 + y2 * y2, s3 = x3 * x3 + y3 * y3;
    const ux = s1 * (y2 - y3) + s2 * (y3 - y1) + s3 * (y1 - y2), uy = s1 * (x3 - x2) + s2 * (x1 - x3) + s3 * (x2 - x1);
    const qx = x1 * d - ux, qy = y1 * d - uy; const r2 = qx * qx + qy * qy;
    let dd = d, uu = ux, vv = uy, rr = r2;
    const g = gcdN(gcdN(Math.abs(dd), Math.abs(uu)), Math.abs(vv));
    dd /= g; uu /= g; vv /= g; rr /= (g * g);
    if (dd < 0) { dd = -dd; uu = -uu; vv = -vv; }
    const key = `${dd},${uu},${vv},${rr}`;
    if (keptC.has(key)) continue;
    const pts = [];
    for (let y = 0; y < w; y++) {
      const dy = y * dd - vv; const rem = rr - dy * dy; if (rem < 0) continue;
      const r = isqrt(rem);
      if (r * r === rem) {
        const dxs = r === 0 ? [0] : [r, -r];
        for (const dx of dxs) {
          const num = dx + uu; if (num % dd !== 0) continue;
          const x = num / dd; if (x >= 0 && x < m) pts.push(x + m * y);
        }
      }
    }
    if (pts.length >= q) keptC.set(key, Int32Array.from(pts));
  }
  const curves = lines.concat([...keptC.values()]);
  const pcCount = new Int32Array(N);
  for (const c of curves) for (const p of c) pcCount[p]++;
  const pcOff = new Int32Array(N + 1); for (let p = 0; p < N; p++) pcOff[p + 1] = pcOff[p] + pcCount[p];
  const pcArr = new Int32Array(pcOff[N]); { let t = 0; const fl = new Int32Array(N);
    for (let ci = 0; ci < curves.length; ci++) for (const p of curves[ci]) { pcArr[pcOff[p] + fl[p]] = ci; fl[p]++; } }
  return { N, px, py, nC: curves.length, nLines: lines.length, nCirc: keptC.size, curves, pcOff, pcArr };
}

function makeSearch(Ctx, q, seed0, sampleK = 24) {
  const { N, curves, pcOff, pcArr } = Ctx; const nC = curves.length;
  const cnt = new Int32Array(nC), stone = new Uint8Array(N), unsafe = new Uint8Array(N);
  let seed = seed0 >>> 0 || 1;
  function rnd() { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x80000000; }
  function addStone(p) {
    stone[p] = 1;
    for (let oi = pcOff[p]; oi < pcOff[p + 1]; oi++) { const ci = pcArr[oi]; cnt[ci]++;
      if (cnt[ci] === q - 1) { const c = curves[ci]; for (let t = 0; t < c.length; t++) unsafe[c[t]] = 1; } }
  }
  const free = [];
  function maximalize() {
    free.length = 0; for (let p = 0; p < N; p++) if (!stone[p] && !unsafe[p]) free.push(p);
    while (free.length > 0) {
      if (free.length === 1) { addStone(free[0]); free.length = 0; break; }
      const k = Math.min(sampleK, free.length);
      let bestP = -1, bestSc = -1;
      for (let t = 0; t < k; t++) {
        const i = Math.floor(rnd() * free.length); const p = free[i];
        let sc = 0;
        for (let oi = pcOff[p]; oi < pcOff[p + 1]; oi++) if (cnt[pcArr[oi]] === q - 2) sc++;
        sc += rnd() * 0.5;
        if (sc > bestSc) { bestSc = sc; bestP = p; }
      }
      addStone(bestP);
      let w2 = 0;
      for (let t = 0; t < free.length; t++) { const f = free[t];
        if (f === bestP) continue;
        if (!stone[f] && !unsafe[f]) free[w2++] = f; }
      free.length = w2;
    }
  }
  function rebuildFromMask() {
    cnt.fill(0); unsafe.fill(0);
    for (let p = 0; p < N; p++) if (stone[p]) {
      for (let oi = pcOff[p]; oi < pcOff[p + 1]; oi++) { const ci = pcArr[oi]; cnt[ci]++;
        if (cnt[ci] === q - 1) { const c = curves[ci]; for (let t = 0; t < c.length; t++) unsafe[c[t]] = 1; } } }
  }
  function countStones() { let s = 0; for (let p = 0; p < N; p++) if (stone[p]) s++; return s; }
  function stoneList() { const st = []; for (let p = 0; p < N; p++) if (stone[p]) st.push(p); return st; }
  return { rnd, addStone, maximalize, rebuildFromMask, countStones, stoneList, stone, N };
}

function minimizeSA(Ctx, q, seed0, budgetMs, opts = {}) {
  const S = makeSearch(Ctx, q, seed0, opts.sampleK || 24);
  const { N } = S;
  const full = opts.fullCapacity;
  const t0 = Date.now();
  S.stone.fill(0); S.rebuildFromMask(); S.maximalize();
  let cur = S.stoneList().length;
  let best = Int32Array.from(S.stoneList());
  let bestN = cur;
  let T = opts.T0 || 2.5;
  const TMin = 0.02, alpha = 0.99985;
  let iters = 0, accepts = 0, rejects = 0, lastImprove = 0;
  const maxRemoveFrac = opts.maxRemoveFrac || 0.30;
  const prevMask = new Uint8Array(N);
  while (Date.now() - t0 < budgetMs) {
    iters++;
    const st = S.stoneList();
    const rmax = Math.max(2, Math.floor(st.length * maxRemoveFrac));
    let r = 1 + Math.floor(S.rnd() * rmax);
    if (r > st.length) r = st.length;
    const idxs = new Set();
    while (idxs.size < r) idxs.add(Math.floor(S.rnd() * st.length));
    prevMask.set(S.stone);
    for (const i of idxs) S.stone[st[i]] = 0;
    S.rebuildFromMask(); S.maximalize();
    const cand = S.stoneList().length;
    const d = cand - cur;
    if (d <= 0 || S.rnd() < Math.exp(-d / T)) { cur = cand; accepts++; }
    else {
      S.stone.set(prevMask); S.rebuildFromMask(); cur = S.countStones();
      rejects++;
      if (iters - lastImprove > 300000) {
        S.stone.fill(0); for (const p of best) S.stone[p] = 1;
        S.rebuildFromMask(); cur = bestN; lastImprove = iters;
      }
    }
    if (cur < bestN) { bestN = cur; best = Int32Array.from(S.stoneList()); lastImprove = iters; }
    if (bestN < full) break;
    T *= alpha;
    if (T < TMin) { T = opts.T0 || 2.5; }
  }
  return { best, bestN, iters, accepts, rejects, ms: Date.now() - t0 };
}

function verifyIndependent(w, m, q, W) {
  const n = W.length; const xs = W.map(s => s[0]), ys = W.map(s => s[1]);
  let worstLine = 0, worstCirc = 0;
  const lineSeen = new Set();
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
    let dx = xs[j] - xs[i], dy = ys[j] - ys[i];
    const g = gcdN(dx, dy); dx /= g; dy /= g;
    if (dy < 0 || (dy === 0 && dx < 0)) { dx = -dx; dy = -dy; }
    const c0 = xs[i] * dy - ys[i] * dx;
    const key = `${dx},${dy},${c0}`;
    if (lineSeen.has(key)) continue; lineSeen.add(key);
    let c = 0; for (let t = 0; t < n; t++) { if (xs[t] * dy - ys[t] * dx === c0) c++; }
    if (c > worstLine) worstLine = c;
  }
  const circSeen = new Set();
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) for (let k2 = j + 1; k2 < n; k2++) {
    const x1 = xs[i], y1 = ys[i], x2 = xs[j], y2 = ys[j], x3 = xs[k2], y3 = ys[k2];
    const d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)); if (d === 0) continue;
    const s1 = x1 * x1 + y1 * y1, s2 = x2 * x2 + y2 * y2, s3 = x3 * x3 + y3 * y3;
    const ux = s1 * (y2 - y3) + s2 * (y3 - y1) + s3 * (y1 - y2), uy = s1 * (x3 - x2) + s2 * (x1 - x3) + s3 * (x2 - x1);
    let dd = d, uu = ux, vv = uy;
    const g = gcdN(gcdN(Math.abs(dd), Math.abs(uu)), Math.abs(vv));
    dd /= g; uu /= g; vv /= g;
    if (dd < 0) { dd = -dd; uu = -uu; vv = -vv; }
    const key = `${dd},${uu},${vv}`;
    if (circSeen.has(key)) continue; circSeen.add(key);
    const qx = x1 * dd - uu, qy = y1 * dd - vv, rr = qx * qx + qy * qy;
    let c = 0; for (let t = 0; t < n; t++) { const dx = xs[t] * dd - uu, dy = ys[t] * dd - vv; if (dx * dx + dy * dy === rr) c++; }
    if (c > worstCirc) worstCirc = c;
  }
  const safe = (worstLine < q) && (worstCirc < q);
  const stoneSet = new Set(); for (let i = 0; i < n; i++) stoneSet.add(xs[i] + "," + ys[i]);
  const unblocked = [];
  for (let x = 0; x < m; x++) for (let y = 0; y < w; y++) {
    if (stoneSet.has(x + "," + y)) continue;
    let blocked = false;
    for (let i = 0; i < n && !blocked; i++) {
      let dx = xs[i] - x, dy = ys[i] - y;
      const g = gcdN(dx, dy); dx /= g; dy /= g;
      if (dy < 0 || (dy === 0 && dx < 0)) { dx = -dx; dy = -dy; }
      const c0 = x * dy - y * dx;
      let c = 0; for (let t = 0; t < n; t++) { if (xs[t] * dy - ys[t] * dx === c0) c++; }
      if (c >= q - 1) blocked = true;
    }
    for (let i = 0; i < n && !blocked; i++) for (let j = i + 1; j < n && !blocked; j++) {
      const x1 = x, y1 = y, x2 = xs[i], y2 = ys[i], x3 = xs[j], y3 = ys[j];
      const d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)); if (d === 0) continue;
      const s1 = x1 * x1 + y1 * y1, s2 = x2 * x2 + y2 * y2, s3 = x3 * x3 + y3 * y3;
      const ux = s1 * (y2 - y3) + s2 * (y3 - y1) + s3 * (y1 - y2), uy = s1 * (x3 - x2) + s2 * (x1 - x3) + s3 * (x2 - x1);
      const qx = x1 * d - ux, qy = y1 * d - uy, r2 = qx * qx + qy * qy;
      let c = 0; for (let t = 0; t < n; t++) { const dx = xs[t] * d - ux, dy = ys[t] * d - uy; if (dx * dx + dy * dy === r2) c++; }
      if (c >= q - 1) blocked = true;
    }
    if (!blocked) unblocked.push([x, y]);
  }
  return { n, worstLine, worstCirc, safe, maximal: unblocked.length === 0, unblockedCount: unblocked.length, unblocked: unblocked.slice(0, 3) };
}

module.exports = { buildCurves, minimizeSA, verifyIndependent };

if (require.main === module) {
  const [w, m, q, budget, seed] = process.argv.slice(2).map(Number);
  const ctx = buildCurves(w, m, q);
  const full = w * (q - 1);
  const r = minimizeSA(ctx, q, seed, budget, { fullCapacity: full });
  const witness = [...r.best].map(p => [p % m, Math.floor(p / m)]);
  const out = { w, m, q, full, min: r.bestN, nC: ctx.nC, nCirc: ctx.nCirc, nLines: ctx.nLines,
    iters: r.iters, accepts: r.accepts, rejects: r.rejects, ms: r.ms, seed };
  if (r.bestN < full) {
    out.witness = witness;
    out.independent = verifyIndependent(w, m, q, witness);
  }
  console.log(JSON.stringify(out));
}
