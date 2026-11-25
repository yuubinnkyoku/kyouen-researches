#!/usr/bin/env node
// Incremental simulated-annealing machine for row-deficient maximal safe witnesses
// on w x m grid boards (fixed-width stabilization lane).
//
// Derived from K0811 (research/experiments/sa-row-deficient-witnesses-20261114/scripts/sa_machine.js);
// census is the genfast3 chord-pair port. The SA hot loop is rewritten with incremental
// updates: per-curve stone counters cnt[], per-point block counters blocked[] (number of
// curves through the point already holding q-1 stones), a stone stack with positions, and
// fixed iteration budgets. The RNG is a deterministic LCG, so (board, seed, maxIters)
// runs are bit-reproducible. Executed in the Vibe TS sandbox on 2026-11-15;
// output/results.jsonl records the actual runs. This CLI packages the executed logic.
//
// Usage: node sa_machine_incremental.js <w> <q> <mFrom> <mTo> <seedFrom> <seedTo> <maxIters>

"use strict";
const [W, Q, MFROM, MTO, SFROM, STO, MAXIT] = process.argv.slice(2).map(Number);

function gcdN(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { const t = a % b; a = b; b = t; } return a || 1; }
function isqrt(n) { if (n < 0) return -1; let r = Math.floor(Math.sqrt(n)); while (r * r > n) r--; while ((r + 1) * (r + 1) <= n) r++; return r; }

// Complete chord-pair census: rows (if m >= q) + all circles with >= q grid points.
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

// Incremental SA. State is always a maximal safe configuration.
function minimizeSA3(Ctx, q, seed0, maxIters, opts) {
  const { N, curves, pcOff, pcArr } = Ctx, nC = Ctx.nC;
  const cnt = new Int32Array(nC);
  const blocked = new Int32Array(N);
  const stone = new Uint8Array(N);
  const stones = [];
  const sPos = new Int32Array(N).fill(-1);
  let seed = seed0 >>> 0 || 1;
  function rnd() { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x80000000; }
  function addStone(p) {
    stone[p] = 1; stones.push(p); sPos[p] = stones.length - 1;
    for (let oi = pcOff[p]; oi < pcOff[p + 1]; oi++) { const ci = pcArr[oi]; if (++cnt[ci] === q - 1) { const c = curves[ci]; for (let t = 0; t < c.length; t++) blocked[c[t]]++; } }
  }
  function removeStone(p) {
    stone[p] = 0;
    const last = stones.pop(), ip = sPos[p];
    if (stones.length > ip) { stones[ip] = last; sPos[last] = ip; }
    sPos[p] = -1;
    for (let oi = pcOff[p]; oi < pcOff[p + 1]; oi++) { const ci = pcArr[oi]; if (--cnt[ci] === q - 2) { const c = curves[ci]; for (let t = 0; t < c.length; t++) blocked[c[t]]--; } }
  }
  const free = [];
  function maximalize() {
    free.length = 0; for (let p = 0; p < N; p++) if (!stone[p] && blocked[p] === 0) free.push(p);
    const sampleK = opts.sampleK || 24;
    while (free.length > 0) {
      if (free.length === 1) { addStone(free[0]); free.length = 0; break; }
      const k = Math.min(sampleK, free.length);
      let bestP = -1, bestSc = -1;
      for (let t = 0; t < k; t++) {
        const i = Math.floor(rnd() * free.length), p = free[i];
        let sc = 0;
        for (let oi = pcOff[p]; oi < pcOff[p + 1]; oi++) if (cnt[pcArr[oi]] === q - 2) sc++;
        sc += rnd() * 0.5;
        if (sc > bestSc) { bestSc = sc; bestP = p; }
      }
      addStone(bestP);
      let w2 = 0;
      for (let t = 0; t < free.length; t++) { const f = free[t]; if (f === bestP) continue; if (!stone[f] && blocked[f] === 0) free[w2++] = f; }
      free.length = w2;
    }
  }
  const full = opts.fullCapacity;
  maximalize();
  let cur = stones.length;
  const bestMask = new Uint8Array(N);
  bestMask.set(stone);
  let bestN = cur, T = opts.T0 || 2.5;
  const TMin = 0.02, alpha = 0.99985;
  let iters = 0, lastImprove = 0;
  const maxRemoveFrac = opts.maxRemoveFrac || 0.30;
  const prevStones = [];
  while (iters < maxIters) {
    iters++;
    const ns = stones.length;
    const rmax = Math.max(2, Math.floor(ns * maxRemoveFrac));
    let r = 1 + Math.floor(rnd() * rmax);
    if (r > ns) r = ns;
    prevStones.length = 0; for (const s of stones) prevStones.push(s);
    for (let t = 0; t < r; t++) removeStone(stones[Math.floor(rnd() * stones.length)]);
    maximalize();
    const cand = stones.length, d = cand - cur;
    if (d <= 0 || rnd() < Math.exp(-d / T)) cur = cand;
    else {
      for (const s of stones) { stone[s] = 0; sPos[s] = -1; }
      cnt.fill(0); blocked.fill(0); stones.length = 0;
      for (const s of prevStones) { stone[s] = 1; stones.push(s); sPos[s] = stones.length - 1; for (let oi = pcOff[s]; oi < pcOff[s + 1]; oi++) { const ci = pcArr[oi]; if (++cnt[ci] === q - 1) { const c = curves[ci]; for (let t = 0; t < c.length; t++) blocked[c[t]]++; } } }
      cur = prevStones.length;
      if (iters - lastImprove > 300000) {
        for (const s of stones) { stone[s] = 0; sPos[s] = -1; }
        cnt.fill(0); blocked.fill(0); stones.length = 0;
        for (let p = 0; p < N; p++) if (bestMask[p]) { stone[p] = 1; stones.push(p); sPos[p] = stones.length - 1; for (let oi = pcOff[p]; oi < pcOff[p + 1]; oi++) { const ci = pcArr[oi]; if (++cnt[ci] === q - 1) { const c = curves[ci]; for (let t = 0; t < c.length; t++) blocked[c[t]]++; } } }
        cur = bestN; lastImprove = iters;
      }
    }
    if (cur < bestN) { bestN = cur; bestMask.set(stone); lastImprove = iters; }
    if (bestN < full) break;
    T *= alpha; if (T < TMin) T = opts.T0 || 2.5;
  }
  const bestPts = []; for (let p = 0; p < N; p++) if (bestMask[p]) bestPts.push(p);
  return { best: bestPts, bestN, iters };
}

for (let m = MFROM; m <= MTO; m++) {
  const Ctx = buildCensus(W, m, Q);
  const full = W * Math.min(m, Q - 1);
  for (let seed = SFROM; seed <= STO; seed++) {
    const r = minimizeSA3(Ctx, Q, seed, MAXIT, { fullCapacity: full });
    console.log(JSON.stringify({ board: W + 'x' + m, q: Q, m, full, census: { curves: Ctx.nC, circles: Ctx.nCirc }, seed, iters: r.iters, best_n: r.bestN, witness: r.bestN < full, pts: r.bestN < full ? r.best : null }));
  }
}
