#!/usr/bin/env node
// K0946 sigma_locus_core.js
// Three independent implementations of the K0941 sigma recursions:
//   naiveE/naiveZ : direct JS port of composite_core.py sigma_E/sigma_Z
//                   (pinned copy, sha256 3990d67f...; K0941 definitions)
//   literalZ/literalE : literal chip-distribution state engine
//                   (K0928 Lemma P phase rule on explicit holdings)
//   fastE/fastZ : run-carry level engine with no-wrap batched backward
//                   pass (the K0945 FAST algorithm, independent
//                   implementation used for large sweeps)
// Modes:
//   audit        : full deterministic audit JSON on stdout (one line)
//   div3 M kmin kmax : sweep Z(M,K)=1 hits, residue spectrum mod M+1
//   locus M kmin kmax: list all hits
// Everything is deterministic (fixed LCG seed, no clock, no Map iteration
// order dependence).
'use strict';

// ---------- naive port of the pinned composite_core.py ----------
function naiveE(P, alpha, beta) {
  if (alpha + beta <= 1) return 0;
  const frames = [];
  let k = alpha + beta;
  while (k > 1) {
    const q = Math.floor(P / k), r = P % k;
    frames.push([k, r]);
    if (r < alpha) { P = P + q; alpha = alpha - r - 1; beta = beta + r; }
    else { P = P + q + 1; const na = beta + 2 * alpha - r - 1; beta = r - alpha; alpha = na; }
    k -= 1;
  }
  let sig = 0;
  for (let i = frames.length - 1; i >= 0; i--) sig = (frames[i][1] + 1 + sig) % frames[i][0];
  return sig;
}
function naiveZ(M, K) {
  if (K <= 1) return 0;
  const q = Math.floor(M / K), r = M % K;
  return (r + 1 + naiveE(M + q, K - 1 - r, r)) % K;
}

// ---------- literal chip-distribution state engine ----------
function literalSurvivor(holdings, pot, ptr) {
  const H = holdings.slice();
  let p = ptr, P = pot;
  let k = H.length;
  const alive = Array.from({ length: H.length }, (_, i) => i);
  while (k > 1) {
    const q = Math.floor(P / k), r = P % k;
    for (let i = 0; i < k; i++) H[alive[i]] += q;
    for (let i = 0; i < r; i++) H[alive[(p + i) % k]] += 1;
    const L = (p + P) % k;
    const newpot = H[alive[L]];
    alive.splice(L, 1);
    P = newpot; p = L % (k - 1); k -= 1;
  }
  return alive[0];
}
function literalZ(M, K) { return literalSurvivor(new Array(K).fill(M), M, 0); }
function literalE(P, alpha, beta) {
  const h = new Array(alpha + beta).fill(P);
  for (let i = alpha; i < alpha + beta; i++) h[i] = P + 1;
  return literalSurvivor(h, P, 0);
}

// ---------- run-carry fast engine (K0945 FAST, independent impl) ----------
function runcarryLevels(P, alpha, beta) {
  const out = [];
  let k = alpha + beta, p = P, al = alpha, be = beta;
  while (k > 1) {
    if (p < k && al >= p + 1) {                 // type-A run batch
      const L = Math.floor(al / (p + 1));
      const batch = Math.min(L, k - p);
      if (batch > 0) out.push([k, k - batch + 1, p]);
      k -= batch; al -= batch * (p + 1); be += batch * p;
    } else if (p < k) {                          // bump / carry
      out.push([k, k, p]);
      const nal = be + 2 * al - p - 1, nbe = p - al;
      al = nal; be = nbe; p = p + 1; k -= 1;
    } else {                                     // endgame P >= k
      const q = Math.floor(p / k), r = p % k;
      out.push([k, k, r]);
      if (r < al) { p = p + q; al = al - r - 1; be = be + r; }
      else { const np = p + q + 1, nal = be + 2 * al - r - 1, nbe = r - al;
             p = np; al = nal; be = nbe; }
      k -= 1;
    }
  }
  return out;
}
function fastE(P, alpha, beta) {
  const lv = runcarryLevels(P, alpha, beta);
  let sig = 0;
  for (let i = lv.length - 1; i >= 0; i--) {
    const khi = lv[i][0], klo = lv[i][1], s = lv[i][2] + 1;
    let k = klo;
    while (k <= khi) {
      if (s >= 2) {
        const j = Math.floor((k - 2 - sig) / (s - 1));
        if (j > 0) { const m = Math.min(j, khi - k + 1); sig += m * s; k += m; if (k > khi) break; }
      }
      sig = (sig + s) % k; k += 1;
    }
  }
  return sig;
}
function fastZ(M, K) {
  if (K <= 1) return 0;
  const q = Math.floor(M / K), r = M % K;
  return (r + 1 + fastE(M + q, K - 1 - r, r)) % K;
}

// ---------- deterministic LCG ----------
let _seed = 123456789;
function rnd() { _seed = (_seed * 1103515245 + 12345) % 2147483648; return _seed / 2147483648; }

// ---------- audit ----------
function audit() {
  const rep = { impl: 'sigma_locus_core.js', cross: {}, classify: {}, sweep: {}, excl1: {} };
  // cross: fast vs naive, literal vs naive
  let n = 0, fails = 0;
  for (let P = 0; P <= 16; P++)
    for (let k = 2; k <= 100; k++)
      for (let alpha = 0; alpha <= k; alpha++) {
        n++;
        if (fastE(P, alpha, k - alpha) !== naiveE(P, alpha, k - alpha)) fails++;
      }
  rep.cross.egrid_fast_naive = { states: n, fails };
  n = 0; fails = 0;
  for (let M = 1; M <= 12; M++)
    for (let K = 2; K <= 1200; K++) {
      n++;
      if (fastZ(M, K) !== naiveZ(M, K)) fails++;
    }
  rep.cross.zgrid_fast_naive = { states: n, fails };
  n = 0; fails = 0;
  for (let M = 1; M <= 8; M++)
    for (let K = 2; K <= 60; K++) {
      n++;
      if (literalZ(M, K) !== naiveZ(M, K)) fails++;
    }
  rep.cross.literal_z = { states: n, fails };
  n = 0; fails = 0;
  for (let P = 0; P <= 8; P++)
    for (let k = 2; k <= 30; k++)
      for (let alpha = 0; alpha <= k; alpha++) {
        n++;
        if (literalE(P, alpha, k - alpha) !== naiveE(P, alpha, k - alpha)) fails++;
      }
  rep.cross.literal_e = { states: n, fails };
  n = 0; fails = 0;
  for (let i = 0; i < 500; i++) {
    const P = Math.floor(rnd() * 150) + 1;
    const k = Math.floor(rnd() * 4000) + 2;
    const alpha = Math.floor(rnd() * (k + 1));
    n++;
    if (fastE(P, alpha, k - alpha) !== naiveE(P, alpha, k - alpha)) fails++;
  }
  rep.cross.random_large = { states: n, fails };
  // naive grids exported for the Python pinned-core cross-language check
  rep.zgrid_py = {};
  for (let M = 1; M <= 12; M++) {
    const vals = [];
    for (let K = 2; K <= 1200; K++) vals.push(naiveZ(M, K));
    rep.zgrid_py[String(M)] = vals;
  }
  rep.egrid_py = {};
  for (let P = 0; P <= 8; P++) {
    const byp = [];
    for (let k = 2; k <= 40; k++) {
      const vals = [];
      for (let alpha = 0; alpha <= k; alpha++) vals.push(naiveE(P, alpha, k - alpha));
      byp.push(vals);
    }
    rep.egrid_py[String(P)] = byp;
  }
  // classify: every value-1 hit is case-(i) silent (ONE-CHAR-GENERAL)
  const cMs = [2, 3, 5, 7, 11, 13, 17, 19, 23];
  for (const M of cMs) {
    const g = M + 1;
    let hits = 0, silent = 0, cascade = 0, navbad = 0, runfail = 0;
    const byk = {};
    for (let K = M + 1; K <= 6000; K++) {
      if (fastZ(M, K) !== 1) continue;
      hits++;
      if (naiveZ(M, K) !== 1) { navbad++; continue; }
      const kappa = K % g, s = Math.floor((K - M - 1) / g);
      if ((K - M - 1) - s * g !== kappa) runfail++;
      const tail = naiveE(M, kappa, M * (s + 1));
      if (tail === kappa + 1) {
        silent++;
        byk[String(kappa)] = (byk[String(kappa)] || 0) + 1;
      } else cascade++;
    }
    rep.classify[String(M)] = { hits, silent, cascade, naive_mismatch: navbad, run_identity_fail: runfail, silent_by_kappa: byk };
  }
  // sweep: residue spectra of the value-1 locus, M = 1..40, K <= 10000
  for (let M = 1; M <= 40; M++) {
    const g = M + 1;
    const res = new Array(g).fill(0);
    let deg = 0, nondeg = 0, nondiv = 0, odd = 0, firstND = -1;
    for (let K = 2; K <= 10000; K++) {
      if (fastZ(M, K) !== 1) continue;
      res[K % g]++;
      if (K > M) {
        nondeg++;
        if (K % 2 === 1) odd++;
        if (K % g !== 0) { nondiv++; if (firstND < 0) firstND = K; }
      } else deg++;
    }
    rep.sweep[String(M)] = { deg, nondeg, nondiv, odd, firstND, res };
  }
  // hits_small: hit lists for the Python pinned-core full-set comparison
  rep.hits_small = {};
  for (let M = 1; M <= 40; M++) {
    const out = [];
    for (let K = 2; K <= 1200; K++) if (fastZ(M, K) === 1) out.push(K);
    rep.hits_small[String(M)] = out;
  }
  // excl1 reduced form: sigma_E(M+1; M(s+2)-1, 0) != 0 (U0-NEVER)
  let u0tot = 0, u0zero = 0;
  for (let M = 2; M <= 30; M++)
    for (let s = 0; s <= 60; s++) {
      u0tot++;
      if (naiveE(M + 1, M * (s + 2) - 1, 0) === 0) u0zero++;
    }
  rep.excl1 = { states: u0tot, zeros: u0zero };
  process.stdout.write(JSON.stringify(rep) + '\n');
}

// ---------- CLI ----------
const mode = process.argv[2];
if (mode === 'audit') {
  audit();
} else if (mode === 'div3') {
  const M = Number(process.argv[3]), Kmin = Number(process.argv[4]), Kmax = Number(process.argv[5]);
  const g = M + 1;
  const res = new Array(g).fill(0);
  let deg = 0, nondeg = 0, nondiv = 0, odd = 0, firstND = -1;
  for (let K = Kmin; K <= Kmax; K++) {
    if (fastZ(M, K) === 1) {
      res[K % g]++;
      if (K > M) {
        nondeg++;
        if (K % 2 === 1) odd++;
        if (K % g !== 0) { nondiv++; if (firstND < 0) firstND = K; }
      } else deg++;
    }
  }
  console.log(`M=${M} Kmin=${Kmin} Kmax=${Kmax} deg=${deg} nondeg=${nondeg} nondiv=${nondiv} odd=${odd} firstND=${firstND} res=[${res.join(',')}]`);
} else if (mode === 'locus') {
  const M = Number(process.argv[3]), Kmin = Number(process.argv[4]), Kmax = Number(process.argv[5]);
  const out = [];
  for (let K = Kmin; K <= Kmax; K++) if (fastZ(M, K) === 1) out.push(K);
  console.log(JSON.stringify({ M, Kmin, Kmax, count: out.length, locus: out }));
} else {
  console.error('modes: audit | div3 M kmin kmax | locus M kmin kmax');
  process.exit(2);
}
