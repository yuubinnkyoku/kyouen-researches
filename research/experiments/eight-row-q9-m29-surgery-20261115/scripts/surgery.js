#!/usr/bin/env node
// Bounded-edit witness surgery machine v2 (fast lane). Given a SAFE seed config on the
// w x m board (typically a known witness embedded at a column offset, possibly with a
// few stones removed for controls), enumerate ALL final configurations
//   F = seed + P - Rm,  P subset of seed-empty cells, Rm subset of seed stones,
//   |P| <= maxP, |Rm| <= maxRm, |F| <= targetMax,
// that are (a) safe (every census curve holds <= q-1 stones) and (b) maximal (every
// empty cell of F lies on a census curve holding exactly q-1 stones).
// Such F with |F| <= w*(q-1)-1 is a stabilization witness (deficiency is implied by
// pigeonhole). Enumeration is complete within the stated bounds; nothing else claimed.
//
// Exact pruning lemmas (L1/L2/L3) are proved in the experiment README:
//  L1: F safe <=> for every census curve c, |c∩Rm| >= cnt(c) + |c∩P| - (q-1).
//  L2: every r∈Rm must be re-blocked by some curve c'∋r with final count exactly q-1,
//      which forces cnt(c') + |c'∩P| > q-1 (deficit-positive); hence
//      Rm ⊆ stones lying on deficit-positive curves.
//  L3: every unblocked seed cell t (T') needs a curve c∋t with cnt(c)+|c∩P| >= q-1.
//
// Usage: node surgery.js <w> <q> <m> <seed.json> <maxP> <maxRm> <targetMax> [offX]
//   seed.json: {"stones": [[x,y],...]} placed at (x+offX, y).
// Output: JSONL; witness events carry stones for verify_witness.py; final summary.

"use strict";
const fs = require("fs");
const [W, Q, M] = [Number(process.argv[2]), Number(process.argv[3]), Number(process.argv[4])];
const SEEDF = process.argv[5];
const [MAXP, MAXRM, TARGETMAX] = [Number(process.argv[6]), Number(process.argv[7]), Number(process.argv[8])];
const OFFX = Number(process.argv[9] || 0);
const seed = JSON.parse(fs.readFileSync(SEEDF, "utf8"));

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

const t0 = Date.now();
const Ctx = buildCensus(W, M, Q);
const { N, nC, curves, pcOff, pcArr } = Ctx;
const QM1 = Q - 1;

const stone = new Uint8Array(N);
for (const [x, y] of seed.stones) {
  const X = x + OFFX;
  if (X < 0 || X >= M || y < 0 || y >= W) { console.error("seed stone off board"); process.exit(1); }
  const p = y * M + X;
  if (stone[p]) { console.error("duplicate seed stone"); process.exit(1); }
  stone[p] = 1;
}
const n0 = seed.stones.length;

const cnt = new Int32Array(nC);
for (let ci = 0; ci < nC; ci++) { let c = 0; for (const p of curves[ci]) c += stone[p]; cnt[ci] = c; }
for (let ci = 0; ci < nC; ci++) if (cnt[ci] > QM1) { console.error("seed unsafe: curve " + ci + " cnt " + cnt[ci]); process.exit(1); }

const empties = [];
for (let p = 0; p < N; p++) if (!stone[p]) empties.push(p);
const Tprime = [];
for (const p of empties) { let b = false; for (let oi = pcOff[p]; oi < pcOff[p + 1]; oi++) if (cnt[pcArr[oi]] === QM1) { b = true; break; } if (!b) Tprime.push(p); }
const Tset = new Set(Tprime);

let nP = 0, nPpruned = 0, nRmLeaves = 0, nSafe = 0, nMaximal = 0, nWitness = 0;
const witnesses = [];
const failStats = { unblocked_Tprime: 0, unblocked_hole: 0, unblocked_exposed: 0, unsafe: 0 };

function finalCheck(Plist, Rmlist) {
  const fc = Int32Array.from(cnt);
  for (const p of Plist) for (let oi = pcOff[p]; oi < pcOff[p + 1]; oi++) fc[pcArr[oi]]++;
  for (const r of Rmlist) for (let oi = pcOff[r]; oi < pcOff[r + 1]; oi++) fc[pcArr[oi]]--;
  for (let ci = 0; ci < nC; ci++) if (fc[ci] > QM1) { failStats.unsafe++; return { ok: false, why: "unsafe" }; }
  nSafe++;
  const inF = new Uint8Array(N);
  inF.set(stone);
  for (const p of Plist) inF[p] = 1;
  for (const r of Rmlist) inF[r] = 0;
  const Rset = new Set(Rmlist);
  let ok = true;
  const unb = [];
  for (let p = 0; p < N; p++) {
    if (inF[p]) continue;
    let b = false;
    for (let oi = pcOff[p]; oi < pcOff[p + 1]; oi++) if (fc[pcArr[oi]] === QM1) { b = true; break; }
    if (!b) { ok = false; unb.push(p); if (unb.length >= 8) break; }
  }
  if (!ok) {
    for (const u of unb) {
      if (Tset.has(u)) failStats.unblocked_Tprime++;
      else if (Rset.has(u)) failStats.unblocked_hole++;
      else failStats.unblocked_exposed++;
    }
    return { ok: false, why: "maximal", cells: unb };
  }
  nMaximal++;
  return { ok: true };
}

function emitWitness(Plist, Rmlist) {
  const inF = new Uint8Array(N);
  inF.set(stone);
  for (const p of Plist) inF[p] = 1;
  for (const r of Rmlist) inF[r] = 0;
  const stonesOut = [];
  for (let p = 0; p < N; p++) if (inF[p]) stonesOut.push([p % M, Math.floor(p / M)]);
  if (stonesOut.length > TARGETMAX) { console.error("BUG: count bound violated"); process.exit(2); }
  nWitness++;
  witnesses.push(stonesOut);
  console.log(JSON.stringify({ event: "witness", n: stonesOut.length, stones: stonesOut }));
}

function processP(Plist, addCnt) {
  nP++;
  const remaining = MAXP - Plist.length;
  if (Tprime.length > 0 && remaining === 0) {
    const Pset = new Set(Plist);
    for (const t of Tprime) {
      if (Pset.has(t)) continue; // occupied by an add: maximality does not require blocking
      let ok = false;
      for (let oi = pcOff[t]; oi < pcOff[t + 1]; oi++) { const ci = pcArr[oi]; if (cnt[ci] + addCnt[ci] >= QM1) { ok = true; break; } }
      if (!ok) { nPpruned++; return; }
    }
  }
  const countMin = Math.max(0, n0 + Plist.length - TARGETMAX);
  if (countMin > MAXRM) { nPpruned++; return; }
  const deficits = [];
  let maxNeed = 0;
  for (let ci = 0; ci < nC; ci++) { const need = cnt[ci] + addCnt[ci] - QM1; if (need > 0) { deficits.push({ ci, need }); if (need > maxNeed) maxNeed = need; } }
  const minRm = Math.max(countMin, maxNeed);
  if (minRm > MAXRM) { nPpruned++; return; }
  const candSet = new Set();
  for (const d of deficits) for (const p of curves[d.ci]) if (stone[p]) candSet.add(p);
  const cands = [...candSet];
  if (cands.length < minRm) { nPpruned++; return; }

  const dIdx = new Map(); deficits.forEach((d, i) => dIdx.set(d.ci, i));
  const candD = cands.map(r => {
    let mask = 0;
    for (let oi = pcOff[r]; oi < pcOff[r + 1]; oi++) { const di = dIdx.get(pcArr[oi]); if (di !== undefined) mask |= (1 << di); }
    return mask;
  });
  const nDef = deficits.length;
  const got = new Int32Array(nDef);
  const rm = [];
  const seen = new Set();
  function coverOK() { for (let i = 0; i < nDef; i++) if (got[i] < deficits[i].need) return false; return true; }
  function dfs(startIdx) {
    const size = rm.length;
    if (size >= minRm && coverOK()) {
      const key = rm.slice().sort((a, b) => a - b).join(",");
      if (!seen.has(key)) {
        seen.add(key);
        nRmLeaves++;
        const res = finalCheck(Plist, rm);
        if (res.ok) emitWitness(Plist, rm);
        // fall through: supersets of a covering Rm are distinct final configs and
        // may still be maximal (extra removals re-blocked per L2); keep exploring.
      }
    }
    if (size >= MAXRM) return;
    const slots = MAXRM - size;
    for (let i = 0; i < nDef; i++) if (deficits[i].need - got[i] > slots) return;
    for (let i = startIdx; i < cands.length; i++) {
      rm.push(cands[i]);
      const m = candD[i];
      for (let b = 0; b < nDef; b++) if (m & (1 << b)) got[b]++;
      dfs(i + 1);
      for (let b = 0; b < nDef; b++) if (m & (1 << b)) got[b]--;
      rm.pop();
    }
  }
  dfs(0);
}

(function enumP() {
  const P = [];
  const addCnt = new Int32Array(nC);
  function pAddOK(p) {
    for (let oi = pcOff[p]; oi < pcOff[p + 1]; oi++) { const ci = pcArr[oi]; if (cnt[ci] + addCnt[ci] + 1 - MAXRM > QM1) return false; }
    return true;
  }
  function rec(startIdx) {
    if (P.length > 0) processP(P.slice(), addCnt);
    if (P.length === MAXP) return;
    for (let i = startIdx; i < empties.length; i++) {
      const p = empties[i];
      if (!pAddOK(p)) continue;
      P.push(p);
      for (let oi = pcOff[p]; oi < pcOff[p + 1]; oi++) addCnt[pcArr[oi]]++;
      rec(i + 1);
      for (let oi = pcOff[p]; oi < pcOff[p + 1]; oi++) addCnt[pcArr[oi]]--;
      P.pop();
    }
  }
  rec(0);
})();

const summary = {
  event: "summary", board: W + "x" + M, q: Q, seedFile: SEEDF, offX: OFFX, n0,
  targetMax: TARGETMAX, maxP: MAXP, maxRm: MAXRM,
  census: { curves: nC, circles: Ctx.nCirc },
  nEmpty: empties.length, nTprime: Tprime.length,
  Tprime: Tprime.map(p => [p % M, Math.floor(p / M)]),
  nP, nPpruned, nRmLeaves, nSafe, nMaximal, nWitness, failStats,
  elapsedMs: Date.now() - t0,
};
console.log(JSON.stringify(summary));
