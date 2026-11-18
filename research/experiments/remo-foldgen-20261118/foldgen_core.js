'use strict';
/* K0951 pinned core (remo-foldgen-20261118).
 *
 * Pure-JS transcription of the sigma_E / sigma_Z recursion pinned in
 * composite_core.py (sha256
 * 3990d67ff3a89f480bd92ae784a9efa763d76264e2b8e4a2d1752507a4740f40),
 * with the per-level fold evaluation replaced by the closed-form
 * trichotomy FOLD-GEN (K0951). Statements, proofs and the machine
 * evidence: report.md in this directory.
 *
 * Frame convention (identical to composite_core.py):
 *   decomposeE(P, alpha, beta) emits flat quads:
 *     [0, r+1, k, 0]    plain level k, addend r+1
 *     [1, c, k, kTop]   bump: fold over levels [k, kTop], addend c = P+1
 *   Evaluation composes frames from the LAST quad to the FIRST (the
 *   first quad is the entry frame of the chain).
 */

function ceilDiv(n, d) {
  return Math.floor((n + d - 1) / d);
}

function decomposeE(P0, alpha0, beta0) {
  const ph = [];
  let P = P0, a = alpha0, b = beta0, k = a + b;
  while (k > 1) {
    if (P < k && P < a) {
      let t = ceilDiv(a - P, P + 1);
      if (t > k - P) t = k - P;
      if (t > k - 1) t = k - 1;
      const kTop = k, c = P + 1;
      a -= t * (P + 1);
      b += t * P;
      k -= t;
      if (k > 1 && P < k) {
        ph.push(1, c, k, kTop);
        const na = b + 2 * a - P - 1, nb = P - a;
        P = P + 1; a = na; b = nb; k -= 1;
      } else {
        ph.push(1, c, k + 1, kTop);
      }
    } else {
      const q = Math.floor(P / k), r = P % k;
      ph.push(0, r + 1, k, 0);
      if (r < a) {
        const na = a - r - 1, nb = b + r;
        P = P + q; a = na; b = nb;
      } else {
        const na = b + 2 * a - r - 1, nb = r - a;
        P = P + q + 1; a = na; b = nb;
      }
      k -= 1;
    }
  }
  return ph;
}

/* Direct fold: sigma_l = (sigma_{l-1} + c) mod l for l in [a, b],
 * entry x = sigma_{a-1}. Reference implementation. */
function foldDirect(c, a, b, x) {
  let s = x;
  for (let l = a; l <= b; l++) s = (s + c) % l;
  return s;
}

/* FOLD-GEN closed-form trichotomy (K0951 Theorem). Valid when
 * a >= c - 1 and x <= a - 2; outside that boundary callers must use
 * foldDirect (see foldGenChecked). With D = x + c*(b - a + 1):
 *   (i)   D <= b - 1          -> sigma_b = D          (fully quiet)
 *   (ii)  b <= D <= b + c - 2 -> sigma_b = D - b      (single wrap at b)
 *   (iii) D >= b + c - 1      -> cascade:
 *         L0 = max(a, ceil((c*b - D)/(c-1))),
 *         v0 = D + (c-1)*L0 - c*b  in [0, c-2];
 *         each bite at level L with value v:
 *           m = max(L + 1, ceil((c*L - v)/(c-1))),
 *           v <- v + (c-1)*m - c*L,  L <- m;
 *         when m > b: sigma_b = v + c*(b - L).
 * Proof: the quiet-chain slack f(l) = l - x - c*(l - a + 1) is
 * strictly decreasing for c >= 2, so the first bite level is
 * L0 = max(a, ceil((c*b - D)/(c-1))) and at most one wrap occurs per
 * level when L0 >= c - 1 (u <= L0 + c - 2 < 2*L0). x <= a - 2 is the
 * quiet-at-(a-1) condition needed when L0 = a. Sharp counterexample
 * outside the boundary: c=5, a=2, b=2, x=0 -> direct 1, trichotomy 3.
 */
function foldGen(c, a, b, x) {
  const D = x + c * (b - a + 1);
  if (D <= b - 1) return D;
  if (D <= b + c - 2) return D - b;
  let L = Math.max(a, ceilDiv(c * b - D, c - 1));
  let v = D + (c - 1) * L - c * b;
  for (;;) {
    const m = Math.max(L + 1, ceilDiv(c * L - v, c - 1));
    if (m > b) return v + c * (b - L);
    v = v + (c - 1) * m - c * L;
    L = m;
  }
}

function foldGenChecked(c, a, b, x) {
  if (a < c - 1 || x > a - 2) return foldDirect(c, a, b, x);
  return foldGen(c, a, b, x);
}

/* Fast sigma_E: decomposeE + closed-form fold composition. */
function sigmaEFast(P, alpha, beta) {
  if (alpha + beta <= 1) return 0;
  const ph = decomposeE(P, alpha, beta);
  let sig = 0;
  for (let i = ph.length - 4; i >= 0; i -= 4) {
    if (ph[i] === 0) sig = (ph[i + 1] + sig) % ph[i + 2];
    else sig = foldGen(ph[i + 1], ph[i + 2], ph[i + 3], sig);
  }
  return sig;
}

/* Reference sigma_E (frame-by-frame, composite_core.py verbatim). */
function sigmaENaive(P, alpha, beta) {
  if (alpha + beta <= 1) return 0;
  const frames = [];
  let k = alpha + beta, a = alpha, b = beta;
  while (k > 1) {
    const q = Math.floor(P / k), r = P % k;
    frames.push(k, r);
    if (r < a) {
      P = P + q;
      const na = a - r - 1;
      b = b + r;
      a = na;
    } else {
      P = P + q + 1;
      const na = b + 2 * a - r - 1;
      b = r - a;
      a = na;
    }
    k -= 1;
  }
  let sig = 0;
  for (let i = frames.length - 2; i >= 0; i -= 2) {
    sig = (frames[i + 1] + 1 + sig) % frames[i];
  }
  return sig;
}

/* Reference sigma_Z (composite_core.py verbatim). */
function sigmaZNaive(M, K) {
  if (K <= 1) return 0;
  const q = Math.floor(M / K), r = M % K;
  return (r + 1 + sigmaENaive(M + q, K - 1 - r, r)) % K;
}

/* U-RUNG2-FINAL residue equations (K0951). For u >= 2:
 *   u in U  iff  u mod 5 in {0, 2, 3} and (r = u mod 5, j = floor(u/5)):
 *     r = 0: sigma_E(5; 12j - 4, 3) = 12j - 3
 *     r = 2: sigma_E(5; 12j + 2, 2) = 12j + 3
 *     r = 3: sigma_E(5; 12j + 2, 4) = 12j + 3
 * (r = 1 only u = 1; r = 4 never; see report.md EXCL-U-MOD5.) */
function rhsOk(u) {
  const r = u % 5, j = (u - r) / 5;
  if (r === 0) return sigmaEFast(5, 12 * j - 4, 3) === 12 * j - 3;
  if (r === 2) return sigmaEFast(5, 12 * j + 2, 2) === 12 * j + 3;
  if (r === 3) return sigmaEFast(5, 12 * j + 2, 4) === 12 * j + 3;
  return false;
}

/* Terminal-fold bite counters for the entry (i = 0) frame of
 * decomposeE(P, alpha, beta), evaluated with entry sig:
 *   bites: -2 boundary violation (a < c-1 or sig > a-2; use foldDirect),
 *          -1 first frame is a plain level (no bump),
 *           0 no cascade (quiet or single wrap at b),
 *           k >= 1 cascade with k bites;
 *   l0IsA: whether the first bite is at the interval bottom a
 *          (the rung-2 k1). THEOREM (K0951 terminal bite): for every
 *          u in U with u >= 3 the answer is {bites: 1, l0IsA: true}.
 */
function sigmaETail(P, alpha, beta) {
  const ph = decomposeE(P, alpha, beta);
  let sig = 0;
  for (let i = ph.length - 4; i >= 4; i -= 4) {
    if (ph[i] === 0) sig = (ph[i + 1] + sig) % ph[i + 2];
    else sig = foldGen(ph[i + 1], ph[i + 2], ph[i + 3], sig);
  }
  if (ph[0] === 1) {
    const c = ph[1], a = ph[2], b = ph[3];
    if (a < c - 1 || sig > a - 2) return { bites: -2, l0IsA: false };
    const D = sig + c * (b - a + 1);
    if (D <= b + c - 2) return { bites: 0, l0IsA: false };
    let L = Math.max(a, ceilDiv(c * b - D, c - 1));
    const l0IsA = (L === a);
    let bites = 1;
    let v = D + (c - 1) * L - c * b;
    for (;;) {
      const m = Math.max(L + 1, ceilDiv(c * L - v, c - 1));
      if (m > b) return { bites, l0IsA };
      v = v + (c - 1) * m - c * L;
      L = m;
      bites++;
    }
  }
  return { bites: -1, l0IsA: false };
}

module.exports = {
  ceilDiv, decomposeE, foldDirect, foldGen, foldGenChecked,
  sigmaEFast, sigmaENaive, sigmaZNaive, rhsOk, sigmaETail,
};
