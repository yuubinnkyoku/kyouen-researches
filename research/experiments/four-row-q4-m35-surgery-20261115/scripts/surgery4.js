#!/usr/bin/env node
// surgery4.js — bounded-edit witness surgery machine v2 (fast lane), with a census
// completeness fix for q <= w boards.
//
// Derived from eight-row-q9-m29-surgery-20261115/scripts/surgery.js (md5
// 94baa517b788efa02dc761b892fc8440, reused verbatim by five-row-q6-m22-surgery-20261115):
// the enumeration core (enumP/processP/dfs/finalCheck/emitWitness and the exact pruning
// lemmas L1/L2/L3) is byte-identical. ONLY buildCensus is replaced, because the original
// chord-pair census enumerates (i) only ROW lines and (ii) only circles having a 2-point
// chord on each of two distinct rows. That is complete when q > w (a non-row line and a
// <=1-point-per-row circle then have < q window points), but INCOMPLETE for q <= w:
//   - non-row lines with >= q window points exist (e.g. diagonals at q = w),
//   - circles with window distribution (1,1,...,1) or (2,1,1,...,1) exist.
// buildCensus4 adds, on top of the verbatim chord-pair port:
//   (L) all lines via sat.js lineABC over all point pairs (superset of row lines),
//   (E-a) all circles through one point on each of three rows (covers every circle
//         whose window rows all carry <= 1 point),
//   (E-b) all circles through a pair on one row plus one point on another row
//         (covers every circle with exactly one 2-point row).
// Completeness argument (any w, q): a circle has <= 2 window points per row; if >= 2 rows
// carry a pair it is found by the chord-pair port; if exactly 1 row carries a pair by
// (E-b); if no row carries a pair (all singles) by (E-a), since >= q >= 4 points force
// >= 3 occupied rows. Dedup is by the exact window point set: two distinct circles share
// <= 2 points, so >= 4-point sets are in bijection with circles.
// Census equality vs sat.js all-triples buildCensus is machine-checked by
// census4_check.js at several (w,m,q) before any surgery run (C4-style control).
//
// Usage: node surgery4.js <w> <q> <m> <seed.json> <maxP> <maxRm> <targetMax> [offX]
"use strict";
const fs = require("fs");
const S = require("./sat.js");


function gcdN(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { const t = a % b; a = b; b = t; } return a || 1; }
function isqrt(n) { if (n < 0) return -1; let r = Math.floor(Math.sqrt(n)); while (r * r > n) r--; while ((r + 1) * (r + 1) <= n) r++; return r; }

// pts on circle co=[A,B,C,D] (A>0): per row y solve A x^2 + B x + (A y^2 + C y + D) = 0
// exactly over the integers (verbatim logic of sat3.js circlePts).
function circlePts(co, w, m) {
  const A = co[0], B = co[1], C = co[2], D = co[3];
  const twoA = 2 * A;
  const set = [];
  for (let y = 0; y < w; y++) {
    const t = A * y * y + C * y + D;
    const disc = B * B - 4 * A * t;
    if (disc < 0) continue;
    let r = Math.round(Math.sqrt(disc));
    while (r > 0 && r * r > disc) r--;
    while ((r + 1) * (r + 1) <= disc) r++;
    if (r * r !== disc) continue;
    const n1 = -B - r, n2 = -B + r;
    if (n1 % twoA === 0) { const x = n1 / twoA; if (x >= 0 && x < m) set.push(y * m + x); }
    if (r > 0 && n2 % twoA === 0) { const x = n2 / twoA; if (x >= 0 && x < m) set.push(y * m + x); }
  }
  set.sort((a, b) => a - b);
  return set;
}

function buildCensus4(w, m, q) {
  const N = w * m;
  // ---- (L) all lines via sat.js lineABC over all pairs (superset of the row lines) ----
  const lineMap = new Map();
  const P = [];
  for (let y = 0; y < w; y++) for (let x = 0; x < m; x++) P.push([x, y]);
  for (let i = 0; i < P.length; i++) for (let j = i + 1; j < P.length; j++) {
    const lo = S.lineABC(P[i], P[j]);
    const key = lo.join(",");
    if (!lineMap.has(key)) lineMap.set(key, lo);
  }
  const curves = [];
  for (const lo of lineMap.values()) {
    const pts = [];
    for (let idx = 0; idx < P.length; idx++) if (S.onLine(lo, P[idx][0], P[idx][1])) pts.push(idx);
    if (pts.length >= q) curves.push(Int32Array.from(pts));
  }
  // ---- chord-pair circle port (verbatim from surgery.js buildCensus) ----
  const found = new Map(); // chord-pair internal key -> pts
  const needExtra = Math.ceil((q - 4) / 2);
  const kbuf = new Int32Array(w), obuf = new Int32Array(w), d1buf = new Int32Array(w), bbuf = new Int32Array(w), cbuf = new Int32Array(w);
  const px = (i) => i % m, py = (i) => Math.floor(i / m);
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
          const key = dd + "," + uu + "," + vv + "," + (rr0 / (g * g));
          if (!found.has(key)) found.set(key, pts);
        }
      }
    }
  }
  // ---- dedup layer: exact window point-set keys ----
  const circByPts = new Map();
  for (const pts of found.values()) if (pts.length >= q) circByPts.set(pts.join(","), pts);
  // ---- (E-a) all-single-row circles: one point on each of three rows ----
  let nEa = 0;
  for (let r1 = 0; r1 < w; r1++) for (let r2 = r1 + 1; r2 < w; r2++) for (let r3 = r2 + 1; r3 < w; r3++) {
    for (let xa = 0; xa < m; xa++) for (let xb = 0; xb < m; xb++) {
      const p1 = [xa, r1], p2 = [xb, r2];
      for (let xc = 0; xc < m; xc++) {
        const co = S.circleABC(p1, p2, [xc, r3]);
        if (co === null) continue;
        const pts = circlePts(co, w, m);
        if (pts.length < q) continue;
        nEa++;
        const key = pts.join(",");
        if (!circByPts.has(key)) circByPts.set(key, pts);
      }
    }
  }
  // ---- (E-b) exactly-one-pair-row circles: a pair on row ya plus a point on row yb ----
  let nEb = 0;
  for (let ya = 0; ya < w; ya++) {
    for (let x1 = 0; x1 < m; x1++) for (let x2 = x1 + 1; x2 < m; x2++) {
      for (let yb = 0; yb < w; yb++) {
        if (yb === ya) continue;
        for (let xb = 0; xb < m; xb++) {
          const co = S.circleABC([x1, ya], [x2, ya], [xb, yb]);
          if (co === null) continue;
          const pts = circlePts(co, w, m);
          if (pts.length < q) continue;
          nEb++;
          const key = pts.join(",");
          if (!circByPts.has(key)) circByPts.set(key, pts);
        }
      }
    }
  }
  for (const pts of circByPts.values()) curves.push(Int32Array.from(pts));
  const nCirc = circByPts.size;
  const pcCount = new Int32Array(N);
  for (const c of curves) for (const p of c) pcCount[p]++;
  const pcOff = new Int32Array(N + 1); for (let p = 0; p < N; p++) pcOff[p + 1] = pcOff[p] + pcCount[p];
  const pcArr = new Int32Array(pcOff[N]);
  { let t = 0; const fl = new Int32Array(N); for (let ci = 0; ci < curves.length; ci++) for (const p of curves[ci]) { pcArr[pcOff[p] + fl[p]] = ci; fl[p]++; } }
  return { N, nC: curves.length, nCirc, nEa, nEb, curves, pcOff, pcArr };
}

if (require.main === module) {
const [W, Q, M] = [Number(process.argv[2]), Number(process.argv[3]), Number(process.argv[4])];
  const SEEDF = process.argv[5];
  const [MAXP, MAXRM, TARGETMAX] = [Number(process.argv[6]), Number(process.argv[7]), Number(process.argv[8])];
  const OFFX = Number(process.argv[9] || 0);
  const seed = JSON.parse(fs.readFileSync(SEEDF, "utf8"));
  const t0 = Date.now();
  const Ctx = buildCensus4(W, M, Q);
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
    census: { curves: nC, circles: Ctx.nCirc, nEa: Ctx.nEa, nEb: Ctx.nEb },
    nEmpty: empties.length, nTprime: Tprime.length,
    Tprime: Tprime.map(p => [p % M, Math.floor(p / M)]),
    nP, nPpruned, nRmLeaves, nSafe, nMaximal, nWitness, failStats,
    elapsedMs: Date.now() - t0,
  };
  console.log(JSON.stringify(summary));

}
module.exports = { buildCensus4, circlePts, isqrt, gcdN };
