#!/usr/bin/env node
'use strict';
/*
 * K0964 sweep engine (Node.js; all integers < 2^53, exact in doubles).
 *
 * Modes:
 *   A  reproduce the published K0963 band t in [4, T5(M)] (validation)
 *   B  new kodd=4 census band:
 *        part 1: t in [2, T36=(M-2)//36], all kappa (prime Y candidates)
 *        part 2: t in (T36, T12=(M-2)//12], kappa=0 only (Y=(M+1)t+1)
 *
 * Method (identical to the published K0963 sweep): for each small prime
 * p <= M-1 walk the AP  Y = M^{-1} (mod p)  inside the band and divide
 * p-powers out of the cofactor N = M*Y-1.  Cofactor 1 at the end
 * <=> N is (M-1)-smooth.  Prime-Y candidates only ([Y ok] classes;
 * Y=M^2 is outside both bands: t=M-1 > T12 for M>13).
 *
 * Accounting follows the published semantics: n_cand counts all prime Y
 * (dead kappa=M-1 included), n_smooth counts all smooth rows (dead
 * included), hits/blocked count live rows only (kappa <= M-2).
 *
 * Checkpointed per M: state.json (next index); outputs appended as JSONL
 * after each M.  Deterministic: byte-identical on re-run.
 */
const fs = require('fs');
const path = require('path');

const mode = process.argv[2];           // 'A' | 'B'
const budgetMs = process.argv[3] ? Number(process.argv[3]) : 200000;
if (mode !== 'A' && mode !== 'B') throw new Error('mode A|B required');

const here = __dirname;
const work = path.join(here, 'mode' + mode);
fs.mkdirSync(work, {recursive: true});
const meta = JSON.parse(fs.readFileSync(path.join(here, 'bounds_meta.json'), 'utf8'));
const bounds = JSON.parse(fs.readFileSync(path.join(here, 'bounds_band' + mode + '.json'), 'utf8'));

const ymax = mode === 'A' ? meta.ymaxA : meta.ymaxB;

// ---- global prime sieve up to ymax -------------------------------------
function sieveUpTo(n) {
  const f = new Uint8Array(n + 1).fill(1);
  f[0] = 0; if (n >= 1) f[1] = 0;
  for (let i = 2; i * i <= n; i++)
    if (f[i]) for (let j = i * i; j <= n; j += i) f[j] = 0;
  return f;
}
const pflag = sieveUpTo(ymax);
// prime list up to 10000 (small primes for AP walk / trial division)
const SMALL_MAX = meta.Ms[meta.Ms.length - 1] - 1;
const smallPrimes = [];
for (let i = 2; i <= SMALL_MAX; i++) if (pflag[i]) smallPrimes.push(i);

// ---- helpers -------------------------------------------------------------
function invMod(a, p) {
  let or_ = a % p, r = p, os = 1, s = 0;
  while (r !== 0) {
    const q = Math.floor(or_ / r);
    const tr = or_ - q * r; or_ = r; r = tr;
    const ts = os - q * s; os = s; s = ts;
  }
  return ((os % p) + p) % p;
}

// enumerate all divisors from flat facs [p,e,p,e,...]; early exit if a
// divisor falls in [lo, hi] (window)
function windowEmpty(facs, lo, hi) {
  let divs = [1];
  for (let j = 0; j < facs.length; j += 2) {
    const p = facs[j], e = facs[j + 1];
    let pe = 1;
    const nd = [];
    for (let k = 1; k <= e; k++) {
      pe *= p;
      for (let d = 0; d < divs.length; d++) {
        const v = divs[d] * pe;
        if (v >= lo && v <= hi) return false;
        nd.push(v);
      }
    }
    divs = divs.concat(nd);
  }
  return true;
}

// ---- state ---------------------------------------------------------------
const stateFile = path.join(work, 'state.json');
let next = 0;
if (fs.existsSync(stateFile)) next = JSON.parse(fs.readFileSync(stateFile, 'utf8')).next;

const acctFile = path.join(work, 'acct.jsonl');
const rowsK4 = path.join(work, 'rows_k4.jsonl');
const rowsK5p = path.join(work, 'rows_k5p.jsonl');
const rowsK3deep = path.join(work, 'rows_k3deep.jsonl');

const t0 = Date.now();
let totCand = 0, totSmooth = 0, totHits = 0, totBlocked = 0, totDead = 0;

// prime list for candidate slicing (all primes up to ymax)
// build lazily: index of first prime >= ylo via linear scan of smallPrimes
// is not possible (primes up to 8.3M) -> build full list once.
const allPrimes = [];
for (let i = 2; i <= ymax; i++) if (pflag[i]) allPrimes.push(i);

function firstIdxAtLeast(x) {
  // binary search in allPrimes
  let lo = 0, hi = allPrimes.length - 1;
  if (allPrimes[hi] < x) return allPrimes.length;
  while (lo < hi) { const mid = (lo + hi) >> 1; if (allPrimes[mid] < x) lo = mid + 1; else hi = mid; }
  return lo;
}

function appendRow(file, obj) { fs.appendFileSync(file, JSON.stringify(obj) + '\n'); }

function processM(rowB) {
  const M = rowB.M;
  const out = {M: M};
  if (mode === 'A') {
    const T = rowB.T, ylo = rowB.ylo, yhi = rowB.yhi;
    const L = yhi - ylo + 1;
    const flag = new Uint8Array(L);
    const cof = new Float64Array(L);
    const facsArr = new Array(L);
    let lo = firstIdxAtLeast(ylo);
    let nCand = 0;
    for (let pi = lo; pi < allPrimes.length && allPrimes[pi] <= yhi; pi++) {
      const Y = allPrimes[pi];
      const idx = Y - ylo;
      flag[idx] = 1;
      cof[idx] = M * Y - 1;
      nCand++;
    }
    for (let si = 0; si < smallPrimes.length; si++) {
      const p = smallPrimes[si];
      if (p > M - 1) break;
      const minv = invMod(M % p, p);
      let i0 = (minv - (ylo % p) + p) % p;
      for (let i = i0; i < L; i += p) {
        if (!flag[i]) continue;
        let c = cof[i];
        let e = 0;
        do { c /= p; e++; } while (c % p === 0);
        cof[i] = c;
        let f = facsArr[i];
        if (f === undefined) facsArr[i] = [p, e];
        else { f.push(p); f.push(e); }
      }
    }
    let nSmooth = 0, nDead = 0, nBlocked = 0, nHits = 0;
    const kdHist = {};
    const tmax = {};   // kodd -> {t, kap}
    for (let pi = lo; pi < allPrimes.length && allPrimes[pi] <= yhi; pi++) {
      const i = allPrimes[pi] - ylo;
      if (cof[i] !== 1) continue;
      nSmooth++;
      const Y = allPrimes[pi];
      const kap = (Y - 1) % (M + 1);
      if (kap > M - 2) { nDead++; continue; }
      const t = (Y - 1 - kap) / (M + 1);
      const k0 = M * t + kap - 1;
      const facs = facsArr[i];
      if (!windowEmpty(facs, M, k0)) { nBlocked++; continue; }
      nHits++;
      // kodd
      let kodd = 0;
      const odd = [];
      for (let j = 0; j < facs.length; j += 2) {
        const p = facs[j], e = facs[j + 1];
        if (p > 2) { kodd += e; for (let k = 0; k < e; k++) odd.push(p); }
      }
      kdHist[kodd] = (kdHist[kodd] || 0) + 1;
      const prev = tmax[kodd];
      if (!prev || t > prev.t) tmax[kodd] = {t: t, kap: kap};
      if (kodd === 5 || kodd >= 6) {
        appendRow(rowsK5p, {M: M, t: t, kap: kap, Y: Y, N: M * Y - 1,
          a: facs[1], k0: k0, kodd: kodd, odd: odd});
      }
      if (kodd <= 2) throw new Error('kodd<=2 hit at M=' + M);
    }
    Object.assign(out, {T: T, n_cand: nCand, n_smooth: nSmooth,
      n_dead_smooth: nDead, n_blocked: nBlocked, n_hits: nHits,
      kd_hist: kdHist, tmax: tmax});
    totCand += nCand; totSmooth += nSmooth; totHits += nHits;
    totBlocked += nBlocked; totDead += nDead;
  } else {
    // ---- mode B ----
    const T36 = rowB.T36, T12 = rowB.T12, cs = rowB.csqrt;
    const ylo = rowB.ylo1, yhi = rowB.yhi1;
    const L = yhi - ylo + 1;
    const flag = new Uint8Array(L);
    const cof = new Float64Array(L);
    const facsArr = new Array(L);
    let lo = firstIdxAtLeast(ylo);
    let nCand = 0;
    for (let pi = lo; pi < allPrimes.length && allPrimes[pi] <= yhi; pi++) {
      const Y = allPrimes[pi];
      const idx = Y - ylo;
      flag[idx] = 1;
      cof[idx] = M * Y - 1;
      nCand++;
    }
    for (let si = 0; si < smallPrimes.length; si++) {
      const p = smallPrimes[si];
      if (p > M - 1) break;
      const minv = invMod(M % p, p);
      let i0 = (minv - (ylo % p) + p) % p;
      for (let i = i0; i < L; i += p) {
        if (!flag[i]) continue;
        let c = cof[i];
        let e = 0;
        do { c /= p; e++; } while (c % p === 0);
        cof[i] = c;
        let f = facsArr[i];
        if (f === undefined) facsArr[i] = [p, e];
        else { f.push(p); f.push(e); }
      }
    }
    let nSmooth = 0, nDead = 0, nBlocked = 0, nHits = 0;
    const kdHist = {};
    const tmax = {};
    for (let pi = lo; pi < allPrimes.length && allPrimes[pi] <= yhi; pi++) {
      const i = allPrimes[pi] - ylo;
      if (cof[i] !== 1) continue;
      nSmooth++;
      const Y = allPrimes[pi];
      const kap = (Y - 1) % (M + 1);
      if (kap > M - 2) { nDead++; continue; }
      const t = (Y - 1 - kap) / (M + 1);
      const k0 = M * t + kap - 1;
      const facs = facsArr[i];
      if (!windowEmpty(facs, M, k0)) { nBlocked++; continue; }
      nHits++;
      let kodd = 0;
      const odd = [];
      for (let j = 0; j < facs.length; j += 2) {
        const p = facs[j], e = facs[j + 1];
        if (p > 2) { kodd += e; for (let k = 0; k < e; k++) odd.push(p); }
      }
      kdHist[kodd] = (kdHist[kodd] || 0) + 1;
      const prev = tmax[kodd];
      if (!prev || t > prev.t) tmax[kodd] = {t: t, kap: kap};
      if (kodd === 4) {
        appendRow(rowsK4, {M: M, t: t, kap: kap, Y: Y, N: M * Y - 1,
          a: facs[1], k0: k0, odd: odd, part: 1});
      } else if (kodd >= 5) {
        appendRow(rowsK5p, {M: M, t: t, kap: kap, Y: Y, N: M * Y - 1,
          a: facs[1], k0: k0, kodd: kodd, odd: odd, part: 1});
      } else if (kodd === 3 && t >= cs) {
        appendRow(rowsK3deep, {M: M, t: t, kap: kap, Y: Y, N: M * Y - 1,
          a: facs[1], k0: k0, odd: odd, part: 1});
      }
      if (kodd <= 2) throw new Error('kodd<=2 hit at M=' + M);
    }
    // ---- part 2: kappa=0, t in (T36, T12] ----
    let nCand2 = 0, nSmooth2 = 0, nBlocked2 = 0, nHits2 = 0;
    const kdHist2 = {};
    const tmax2 = {};
    for (let t = rowB.p2tlo; t <= rowB.p2thi; t++) {
      const Y = (M + 1) * t + 1;
      if (!pflag[Y]) continue;
      nCand2++;
      const N = M * Y - 1;
      // trial division by all primes <= M-1
      const facs = [];
      let c = N;
      for (let si = 0; si < smallPrimes.length; si++) {
        const p = smallPrimes[si];
        if (p > M - 1) break;
        if (c % p === 0) {
          let e = 0;
          do { c /= p; e++; } while (c % p === 0);
          facs.push(p, e);
        }
      }
      if (c !== 1) continue;   // not (M-1)-smooth
      nSmooth2++;
      const k0 = M * t - 1;    // kappa = 0
      if (!windowEmpty(facs, M, k0)) { nBlocked2++; continue; }
      nHits2++;
      let kodd = 0;
      const odd = [];
      for (let j = 0; j < facs.length; j += 2) {
        const p = facs[j], e = facs[j + 1];
        if (p > 2) { kodd += e; for (let k = 0; k < e; k++) odd.push(p); }
      }
      kdHist2[kodd] = (kdHist2[kodd] || 0) + 1;
      const prev = tmax2[kodd];
      if (!prev || t > prev.t) tmax2[kodd] = {t: t};
      if (kodd === 4) {
        appendRow(rowsK4, {M: M, t: t, kap: 0, Y: Y, N: N,
          a: facs[1], k0: k0, odd: odd, part: 2});
      } else if (kodd >= 5) {
        appendRow(rowsK5p, {M: M, t: t, kap: 0, Y: Y, N: N,
          a: facs[1], k0: k0, kodd: kodd, odd: odd, part: 2});
      } else if (kodd === 3 && t >= cs) {
        appendRow(rowsK3deep, {M: M, t: t, kap: 0, Y: Y, N: N,
          a: facs[1], k0: k0, odd: odd, part: 2});
      }
      if (kodd <= 2) throw new Error('kodd<=2 p2 hit at M=' + M);
    }
    Object.assign(out, {T36: T36, T12: T12,
      p1: {n_cand: nCand, n_smooth: nSmooth, n_dead_smooth: nDead,
           n_blocked: nBlocked, n_hits: nHits, kd_hist: kdHist, tmax: tmax},
      p2: {n_cand: nCand2, n_smooth: nSmooth2, n_blocked: nBlocked2,
           n_hits: nHits2, kd_hist: kdHist2, tmax: tmax2}});
    totCand += nCand + nCand2; totSmooth += nSmooth + nSmooth2;
    totHits += nHits + nHits2; totBlocked += nBlocked + nBlocked2;
    totDead += nDead;
  }
  appendRow(acctFile, out);
  fs.writeFileSync(stateFile, JSON.stringify({next: next + 1}));
}

while (next < bounds.length && Date.now() - t0 < budgetMs) {
  processM(bounds[next]);
  next++;
  if (next % 50 === 0)
    console.error('progress', next, '/', bounds.length,
      'cand', totCand, 'smooth', totSmooth, 'hits', totHits);
}

const done = next >= bounds.length;
console.log(JSON.stringify({mode: mode, done: next, left: bounds.length - next,
  tot_cand: totCand, tot_smooth: totSmooth, tot_dead: totDead,
  tot_blocked: totBlocked, tot_hits: totHits,
  runtime_s: (Date.now() - t0) / 1000}));
