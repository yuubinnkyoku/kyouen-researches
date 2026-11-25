#!/usr/bin/env node
// surgery_verify5.js — INDEPENDENT re-implementation of the bounded-edit surgery
// machine (verification tool for four-row-q5-m21-surgery-20261115 / surgery4.js).
//
// Verified on 2026-11-15 in a TS sandbox (second implementation), then ported to
// Node verbatim. Reproduces ALL counters of surgery4.js exactly on the (4,5) m=21
// instances ((2,2)/(3,3) x offX in {0,1}); see the experiment README verification
// section. Differences from surgery4.js are intentional (independence):
//   - census: all-triples counting (normalize circle coefficients per non-collinear
//     triple, group, keep point sets with k>=q window points; rows added separately;
//     sanity check C(k,3) == triples per circle). No chord-pair port, no lineABC.
//   - enumeration: own DFS with incremental deficit tracking; leaves are the same
//     set: (P, Rm) with |P|<=maxP (pAddOK relaxed-safety prune, identical formula),
//     Rm a subset of deficit-curve stones (justified by lemma L2: each removed
//     stone's hole must be re-blocked in F by a curve c' with exactly q-1 F-stones,
//     forcing cnt(c')+|c'∩P| >= q, i.e. c' deficit-positive pre-removal),
//     |Rm| <= maxRm, |Rm| >= max(countMin, maxNeed), all deficits covered.
//   - finalCheck: early-exit maximality scan (holes first, then T', then other
//     empties) — verdict-identical to a full scan; witnesses re-verified from
//     scratch (safety + maximality + deficiency + count bound) before emission.
// Positive control: on (4,5) m=20 with seed = known witness minus two stones,
// (2,2)/15 rediscovers the known witness (nMaximal = nWitness = 1).
// Deterministic: no RNG, pure integer arithmetic.
//
// Usage: node surgery_verify5.js <w> <q> <m> <seed.json> <maxP> <maxRm> <targetMax> [offX]
'use strict';
const fs = require('fs');

function buildCensusTriples(w, m, q) {
  const N = w * m;
  const gcd2 = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) { const t = a % b; a = b; b = t; } return a; };
  let nonCollinear = 0;
  let cap = 200000;
  let A = new Int32Array(cap), B = new Int32Array(cap), C = new Int32Array(cap), D = new Int32Array(cap);
  let T = 0;
  for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++) for (let k = j + 1; k < N; k++) {
    const x1 = i % m, y1 = (i - (i % m)) / m, x2 = j % m, y2 = (j - (j % m)) / m, x3 = k % m, y3 = (k - (k % m)) / m;
    const Dd = x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2);
    if (Dd === 0) continue;
    nonCollinear++;
    if (T === cap) {
      cap *= 2;
      const A2 = new Int32Array(cap); A2.set(A); A = A2;
      const B2 = new Int32Array(cap); B2.set(B); B = B2;
      const C2 = new Int32Array(cap); C2.set(C); C = C2;
      const D2 = new Int32Array(cap); D2.set(D); D = D2;
    }
    const r1 = -(x1 * x1 + y1 * y1), r2 = -(x2 * x2 + y2 * y2), r3 = -(x3 * x3 + y3 * y3);
    let Uu = r1 * (y2 - y3) - y1 * (r2 - r3) + (r2 * y3 - r3 * y2);
    let Vv = x1 * (r2 - r3) - r1 * (x2 - x3) + (x2 * r3 - x3 * r2);
    let Ww = x1 * (y2 * r3 - y3 * r2) - y1 * (x2 * r3 - x3 * r2) + r1 * (x2 * y3 - x3 * y2);
    let Dn = Dd;
    const g0 = gcd2(gcd2(Dn, Uu), gcd2(Vv, Ww)) || 1;
    Dn /= g0; Uu /= g0; Vv /= g0; Ww /= g0;
    if (Dn < 0) { Dn = -Dn; Uu = -Uu; Vv = -Vv; Ww = -Ww; }
    A[T] = Dn; B[T] = Uu; C[T] = Vv; D[T] = Ww; T++;
  }
  const As = A.subarray(0, T), Bs = B.subarray(0, T), Cs = C.subarray(0, T), Ds = D.subarray(0, T);
  const order = new Int32Array(T);
  for (let i = 0; i < T; i++) order[i] = i;
  order.sort((p, r) => As[p] - As[r] || Bs[p] - Bs[r] || Cs[p] - Cs[r] || Ds[p] - Ds[r]);
  const circlePtsList = [];
  const byPts = {};
  let t = 0;
  while (t < T) {
    const i0 = order[t];
    const a0 = As[i0], b0 = Bs[i0], c0 = Cs[i0], d0 = Ds[i0];
    let u = t;
    while (u < T) { const i = order[u]; if (As[i] !== a0 || Bs[i] !== b0 || Cs[i] !== c0 || Ds[i] !== d0) break; u++; }
    const nTrip = u - t;
    if (nTrip >= 10) {
      const pts = [];
      for (let c = 0; c < N; c++) {
        const x = c % m, y = (c - (c % m)) / m;
        if (a0 * (x * x + y * y) + b0 * x + c0 * y + d0 === 0) pts.push(c);
      }
      const kk = pts.length;
      if (kk * (kk - 1) * (kk - 2) / 6 !== nTrip) throw new Error('census sanity failure');
      circlePtsList.push(pts);
      byPts[kk] = (byPts[kk] || 0) + 1;
    }
    t = u;
  }
  const curves = circlePtsList.slice();
  for (let y = 0; y < w; y++) { const pts = []; for (let x = 0; x < m; x++) pts.push(y * m + x); curves.push(pts); }
  const nC = curves.length;
  const pcCount = new Int32Array(N);
  for (const c of curves) for (const p of c) pcCount[p]++;
  const pcOff = new Int32Array(N + 1);
  for (let p = 0; p < N; p++) pcOff[p + 1] = pcOff[p] + pcCount[p];
  const pcArr = new Int32Array(pcOff[N]);
  { const fl = new Int32Array(N); for (let ci = 0; ci < nC; ci++) for (const p of curves[ci]) { pcArr[pcOff[p] + fl[p]] = ci; fl[p]++; } }
  return { N, nC, nCirc: circlePtsList.length, byPts, nonCollinear, curves, pcOff, pcArr };
}

function runSurgery(cen, seedXY, maxP, maxRm, targetMax, offX, w, m, q) {
  const { N, nC, curves, pcOff, pcArr } = cen;
  const QM1 = q - 1;
  const stone = new Uint8Array(N);
  for (const s of seedXY) {
    const x = s[0] + offX, y = s[1];
    if (x < 0 || x >= m || y < 0 || y >= w) throw new Error('seed stone off board');
    const p = y * m + x;
    if (stone[p]) throw new Error('duplicate seed stone');
    stone[p] = 1;
  }
  const n0 = seedXY.length;
  const cnt = new Int32Array(nC);
  for (let ci = 0; ci < nC; ci++) { let c = 0; for (const p of curves[ci]) c += stone[p]; cnt[ci] = c; }
  for (let ci = 0; ci < nC; ci++) if (cnt[ci] > QM1) throw new Error('seed unsafe: curve ' + ci + ' cnt ' + cnt[ci]);
  const empties = [];
  for (let p = 0; p < N; p++) if (!stone[p]) empties.push(p);
  const Tprime = [];
  for (const p of empties) {
    let b = false;
    for (let oi = pcOff[p]; oi < pcOff[p + 1]; oi++) if (cnt[pcArr[oi]] === QM1) { b = true; break; }
    if (!b) Tprime.push(p);
  }
  let nP = 0, nPpruned = 0, leaves = 0, nMaximal = 0, nWitness = 0;
  const witnesses = [];
  const addCnt = new Int32Array(nC);
  const isDef = new Uint8Array(nC);
  const defList = [];
  const P = [];
  const inP = new Uint8Array(N);
  const rmMask = new Uint8Array(N);
  const rOn = new Int32Array(nC);
  const touched = [];
  const staticScan = [];
  const cands = [];
  const need = [];
  const candDefOff = [];
  const candDefFlat = [];
  const got = [];
  const rm = [];
  const candSeen = new Uint8Array(N);

  function fullVerify(rmList) {
    const inF = new Uint8Array(N);
    inF.set(stone);
    for (const p of P) inF[p] = 1;
    for (const r of rmList) inF[r] = 0;
    const fc = new Int32Array(nC);
    for (let ci = 0; ci < nC; ci++) { let c = 0; for (const p of curves[ci]) c += inF[p]; fc[ci] = c; }
    let safe = true;
    for (let ci = 0; ci < nC; ci++) if (fc[ci] > QM1) { safe = false; break; }
    let maximal = true;
    if (safe) {
      for (let p = 0; p < N; p++) {
        if (inF[p]) continue;
        let b = false;
        for (let oi = pcOff[p]; oi < pcOff[p + 1]; oi++) if (fc[pcArr[oi]] === QM1) { b = true; break; }
        if (!b) { maximal = false; break; }
      }
    }
    const stones = [];
    const rows = new Array(w).fill(0);
    for (let p = 0; p < N; p++) if (inF[p]) { stones.push([p % m, (p - (p % m)) / m]); rows[(p - (p % m)) / m]++; }
    return { safe, maximal, n: stones.length, rows, minRow: Math.min.apply(null, rows), stones };
  }

  function finalCheck(rmList) {
    for (const r of rmList) {
      rmMask[r] = 1;
      for (let oi = pcOff[r]; oi < pcOff[r + 1]; oi++) { const g = pcArr[oi]; if (rOn[g] === 0) touched.push(g); rOn[g]++; }
    }
    let maximal = true;
    const nRm = rmList.length;
    for (let si = 0; si < nRm + staticScan.length; si++) {
      const c = si < nRm ? rmList[si] : staticScan[si - nRm];
      let b = false;
      for (let oi = pcOff[c]; oi < pcOff[c + 1]; oi++) { const g = pcArr[oi]; if (cnt[g] + addCnt[g] - rOn[g] === QM1) { b = true; break; } }
      if (!b) { maximal = false; break; }
    }
    if (maximal) {
      nMaximal++;
      const v = fullVerify(rmList);
      if (v.safe && v.maximal && v.n <= targetMax && v.minRow <= q - 2) {
        nWitness++;
        witnesses.push({ n: v.n, rows: v.rows, stones: v.stones });
      } else {
        throw new Error('maximal leaf failed full verify');
      }
    }
    for (const g of touched) rOn[g] = 0;
    touched.length = 0;
    for (const r of rmList) rmMask[r] = 0;
  }

  function processP() {
    nP++;
    if (Tprime.length > 0 && P.length === maxP) {
      for (const t of Tprime) {
        if (inP[t]) continue;
        let ok = false;
        for (let oi = pcOff[t]; oi < pcOff[t + 1]; oi++) { const g = pcArr[oi]; if (cnt[g] + addCnt[g] >= QM1) { ok = true; break; } }
        if (!ok) { nPpruned++; return; }
      }
    }
    const countMin = Math.max(0, n0 + P.length - targetMax);
    const nDef = defList.length;
    let maxNeed = 0;
    need.length = 0;
    for (let di = 0; di < nDef; di++) { const g = defList[di]; const nd = cnt[g] + addCnt[g] - QM1; need.push(nd); if (nd > maxNeed) maxNeed = nd; }
    const minRm = Math.max(countMin, maxNeed);
    if (minRm > maxRm) { nPpruned++; return; }
    cands.length = 0;
    for (let di = 0; di < nDef; di++) {
      const g = defList[di];
      for (const p of curves[g]) if (stone[p] && !candSeen[p]) { candSeen[p] = 1; cands.push(p); }
    }
    for (const c of cands) candSeen[c] = 0;
    if (cands.length < minRm) { nPpruned++; return; }
    staticScan.length = 0;
    for (const t of Tprime) if (!inP[t]) staticScan.push(t);
    for (const e of empties) if (!inP[e]) staticScan.push(e);
    candDefOff.length = 0; candDefFlat.length = 0;
    const dIdx = new Map();
    for (let di = 0; di < nDef; di++) dIdx.set(defList[di], di);
    for (let ci = 0; ci < cands.length; ci++) {
      candDefOff.push(candDefFlat.length);
      const r = cands[ci];
      for (let oi = pcOff[r]; oi < pcOff[r + 1]; oi++) { const di = dIdx.get(pcArr[oi]); if (di !== undefined) candDefFlat.push(di); }
    }
    candDefOff.push(candDefFlat.length);
    got.length = 0;
    for (let di = 0; di < nDef; di++) got.push(0);
    const nCands = cands.length;
    const dfs = (startIdx) => {
      const size = rm.length;
      if (size >= minRm) {
        let cov = true;
        for (let di = 0; di < nDef; di++) if (got[di] < need[di]) { cov = false; break; }
        if (cov) { leaves++; finalCheck(rm.slice()); }
      }
      if (size >= maxRm) return;
      const slots = maxRm - size;
      for (let di = 0; di < nDef; di++) if (need[di] - got[di] > slots) return;
      for (let i = startIdx; i < nCands; i++) {
        rm.push(cands[i]);
        const o1 = candDefOff[i], o2 = candDefOff[i + 1];
        for (let o = o1; o < o2; o++) got[candDefFlat[o]]++;
        dfs(i + 1);
        for (let o = o1; o < o2; o++) got[candDefFlat[o]]--;
        rm.pop();
      }
    };
    dfs(0);
  }

  const pAddOK = (p) => {
    for (let oi = pcOff[p]; oi < pcOff[p + 1]; oi++) { const g = pcArr[oi]; if (cnt[g] + addCnt[g] + 1 - maxRm > QM1) return false; }
    return true;
  };
  const dfsP = (startIdx) => {
    if (P.length > 0) processP();
    if (P.length === maxP) return;
    for (let i = startIdx; i < empties.length; i++) {
      const p = empties[i];
      if (!pAddOK(p)) continue;
      P.push(p); inP[p] = 1;
      const newlyDef = [];
      for (let oi = pcOff[p]; oi < pcOff[p + 1]; oi++) { const g = pcArr[oi]; addCnt[g]++; if (!isDef[g] && cnt[g] + addCnt[g] > QM1) { isDef[g] = 1; defList.push(g); newlyDef.push(g); } }
      dfsP(i + 1);
      for (let oi = pcOff[p]; oi < pcOff[p + 1]; oi++) { const g = pcArr[oi]; addCnt[g]--; }
      for (const g of newlyDef) { isDef[g] = 0; defList.pop(); }
      P.pop(); inP[p] = 0;
    }
  };
  dfsP(0);
  return { nP, nPpruned, leaves, nMaximal, nWitness, witnesses, Tprime: Tprime.map((p) => [p % m, (p - (p % m)) / m]), nEmpty: empties.length, n0 };
}

if (require.main === module) {
  const w = Number(process.argv[2]), q = Number(process.argv[3]), m = Number(process.argv[4]);
  const seedFile = process.argv[5];
  const maxP = Number(process.argv[6]), maxRm = Number(process.argv[7]), targetMax = Number(process.argv[8]);
  const offX = Number(process.argv[9] || 0);
  const seed = JSON.parse(fs.readFileSync(seedFile, 'utf8'));
  const t0 = Date.now();
  const cen = buildCensusTriples(w, m, q);
  const r = runSurgery(cen, seed.stones, maxP, maxRm, targetMax, offX, w, m, q);
  console.log(JSON.stringify({
    board: w + 'x' + m, q, seedFile, offX, n0: r.n0, maxP, maxRm, targetMax,
    census: { curves: cen.nC, circles: cen.nCirc, byPts: cen.byPts, nonCollinear: cen.nonCollinear },
    nEmpty: r.nEmpty, Tprime: r.Tprime,
    nP: r.nP, nPpruned: r.nPpruned, nRmLeaves: r.leaves, nMaximal: r.nMaximal, nWitness: r.nWitness,
    witnesses: r.witnesses,
    elapsedMs: Date.now() - t0,
  }));
}
module.exports = { buildCensusTriples, runSurgery };
