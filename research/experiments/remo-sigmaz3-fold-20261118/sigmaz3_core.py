#!/usr/bin/env python3
"""K0944 core: structure of sigma_Z(3,K) — fold decomposition, ONE-CHAR,
fast run-bump survivor computation.

Composition of PUBLISHED theorems only:
  K0941 THM-C (E-game phase rule + sigma fold; pinned byte-identical in
  composite_core.py sha256 3990d67f...), K0941 sigma_Z wrapper.

New here (paper proofs in report.md, machine-verified in sigmaz3_verify.py):
  RUN-3     the E(3;K-4,3) prefix is a run of s=u-1 simple phases at pot 3
            (r=3, alpha-=4, beta+=3, k-=1), leaving the TAIL E(3; a, 3u)
            for K = 4u+a, K >= 4.
  FOLD      sigma_Z(3,K) = Phi_K(sigma_E(3; a, 3u)): a fold through levels
            K-s..K each with c=4, governed by an explicit trichotomy on
            D = sigma_tail + 4u  (quiet / single bite at K / cascade).
  ONE-CHAR  sigma_Z(3,K) = 1  <=>  sigma_E(3; K%4, 3*(K//4)) = K%4 + 1.
            The alternative (last bite below K then quiet) requires a bite
            at level 3u, 3u+1 or 3u+2, all below the fold range start
            3u+a+1 -> impossible.
  A2-NEVER  K = 4u+2 (K>=6): sigma_Z(3,K) <> 1 always
            (wrap and no-wrap cases for sigma_tail = 3 are both empty).
  FAST      sigma_E computed in O(#segments) via run-bump phase batching
            + batched constant-c folds (empirically O(sqrt(k)) segments).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from composite_core import sigma_E as _sigma_E_pinned
from composite_core import sigma_Z as _sigma_Z_pinned


# ---------- FAST E-game survivor (run-bump segments + batched folds) ----
def _fold_const(v, m0, m1, c):
    """Fold sig = (sig + c) mod m through levels m0..m1 ASCENDING,
    starting from input v at level m0. Requires c >= 2."""
    m = m0
    while m <= m1:
        if v + c < m:
            # no bite at m; first biting level offset j0 >= 1:
            # bite at level m+j (quiet below) <=>
            #   input v + j*c to m+j satisfies v + j*c + c >= m+j
            #   <=>  j*(c-1) >= m - v - c
            j0 = -(-(m - v - c) // (c - 1))
            if j0 < 1:
                j0 = 1
            if m + j0 > m1:
                return v + c * (m1 - m + 1)     # no bite in the whole range
            v += c * j0                          # quiet through m..m+j0-1
            v = v + c - (m + j0)                # bite at level m+j0
            m = m + j0 + 1
        else:
            v = v + c - m                       # bite at level m
            m += 1
    return v

def sigma_E_fast(P, alpha, beta):
    """Same value as pinned composite_core.sigma_E(P,alpha,beta)."""
    k = alpha + beta
    if k <= 1:
        return 0
    segs = []   # (c, m0, m1): fold levels m0..m1 ascending with const c
    while k > 1:
        if P < k:
            if alpha >= P + 1:
                # RUN: t phases at pot P, r=P, c=P+1, levels k-t+1..k
                t = alpha // (P + 1)
                segs.append((P + 1, k - t + 1, k))
                alpha -= t * (P + 1)
                beta += t * P
                k -= t
            else:
                # BUMP: one phase, r=P, c=P+1, level k
                segs.append((P + 1, k, k))
                P, alpha, beta = P + 1, beta + 2 * alpha - P - 1, P - alpha
                k -= 1
        else:
            # ENDGAME phase: r = P mod k
            q, r = divmod(P, k)
            segs.append((r + 1, k, k))
            if r < alpha:
                P, alpha, beta = P + q, alpha - r - 1, beta + r
            else:
                P, alpha, beta = P + q + 1, beta + 2 * alpha - r - 1, r - alpha
            k -= 1
    sig = 0
    for (c, m0, m1) in reversed(segs):        # ascending levels
        if m0 == m1:
            sig = (sig + c) % m0
        else:
            sig = _fold_const(sig, m0, m1, c) if c >= 2 else \
                _fold_const_slow(sig, m0, m1, c)
    return sig

def _fold_const_slow(v, m0, m1, c):
    for m in range(m0, m1 + 1):
        v = (v + c) % m
    return v

def sigma_Z_fast(M, K):
    """Same value as pinned composite_core.sigma_Z(M,K), fast path."""
    if K <= 1:
        return 0
    q, r = divmod(M, K)
    return (r + 1 + sigma_E_fast(M + q, K - 1 - r, r)) % K

# ---------- FOLD decomposition for sigma_Z(3,K) --------------------------
def tail_params(K):
    """K >= 4 -> (u, a, s) with K = 4u+a, s = u-1 run phases,
    TAIL = E(3; a, 3u) of entry size 3u+a."""
    if K < 4:
        raise ValueError("K >= 4 required")
    u, a = divmod(K, 4)
    return u, a, u - 1

def fold4(K, stail):
    """Predicted sigma_Z(3,K) from stail = sigma_E(3; a, 3u)  (K >= 4).
    Trichotomy on D = stail + 4u:
      D <= K-1        -> quiet: value D
      K <= D <= K+2   -> single bite at level K: value D-K
      D >= K+3        -> first bite at L0=ceil((4K-D)/3), cascade.
    """
    u, a, s = tail_params(K)
    D = stail + 4 * u
    if D <= K - 1:
        return D
    if D <= K + 2:
        return D - K
    L0 = -(-(4 * K - D) // 3)
    v = D + 3 * L0 - 4 * K
    assert 0 <= v <= 2, (K, D, L0, v)
    L = L0
    while L < K:
        m = -(-(4 * L - v) // 3)
        if m > K:
            break
        v = v + 4 * (m - 1 - L) + 4 - m
        assert 0 <= v <= 2, (K, D, L, m, v)
        L = m
    return v + 4 * (K - L)

def sigma_Z3(K):
    """sigma_Z(3,K) via decomposition: tail (fast) + fold4.
    K in [2,3]: direct (no run structure)."""
    if K <= 3:
        return _sigma_Z_pinned(3, K)
    u, a, _s = tail_params(K)
    return fold4(K, sigma_E_fast(3, a, 3 * u))

# ---------- censuses -------------------------------------------------------
def ones_upto(Kmax):
    """Value-1 positions of sigma_Z(3,.) for 4 <= K <= Kmax (fast path)."""
    return [K for K in range(4, Kmax + 1) if sigma_Z3(K) == 1]

def tail_census(a, umax):
    """For side a: dict of interesting tail-value counts for u <= umax."""
    res = {"a": a, "umax": umax, "hits_a_plus_1": 0, "hits_examples": []}
    for u in range(1, umax + 1):
        v = sigma_E_fast(3, a, 3 * u)
        if v == a + 1:
            res["hits_a_plus_1"] += 1
            if len(res["hits_examples"]) < 8:
                res["hits_examples"].append(u)
    return res

def U_set(umax):
    """U = {u <= umax : sigma_E(3; 0, 3u) = 1} (fast path)."""
    return [u for u in range(1, umax + 1) if sigma_E_fast(3, 0, 3 * u) == 1]

def is_one_char(K):
    """The ONE-CHAR witness: (sigma_Z(3,K) == 1) vs (tail == a+1)."""
    u, a, _s = tail_params(K)
    stail = sigma_E_fast(3, a, 3 * u)
    return _sigma_Z_pinned(3, K) == 1, stail == a + 1
