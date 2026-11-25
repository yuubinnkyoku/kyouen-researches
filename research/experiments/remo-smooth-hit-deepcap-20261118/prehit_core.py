#!/usr/bin/env python3
"""K0956 core: the pre-tail mechanism of the sigma_Z value-one locus.

Published pinned inputs:
  composite_core.sigma_Z     the engine (K0948/K0949/K0950 pin)
  branch_density_core        K0954 branch structure / BH machinery
  hitpair_core               K0950 HIT-ARITH helpers (unused in the hot
                             loops; the raw window predicate is local)

Setting (K0950/K0952 notation).  Prime M, main regime
    K = (M+1) t + kappa,  t >= 1, 0 <= kappa <= M-2, (t,kappa) != (1,0),
    Y = K+1, k0 = M t + kappa - 1, N = M Y - 1,
    C = gcd(M+1, kappa+2), Q = N/C, live: gcd(kappa+1, M+1) = 1.

New machine-checkable claims (paper proofs in report.md):

  HIT-GAP   in the regime k0 >= sqrt(N) (M >= 3, t >= 2, with the single
            exception (M,t,kappa) = (3,2,0) where the statement survives;
            M = 2: t >= 3):
                sigma_Z(M,K) = 1
            <=> [Y prime or Y = M^2] and D*(N) < M,
            where D*(N) is the largest divisor of N not exceeding sqrt(N).
            (=> needs HIT-ARITH only; <= needs the complement-window
             bound N > (M+1) k0, i.e. 2M > kappa.)

  SPLIT     in the same regime every hit satisfies
            (i)  BRANCH: N has a divisor d with C | d, d <= M-1 and
                 N/d prime  (the K0952 branch form Ce < M, e | Q, Q/e
                 prime with d = Ce), or
            (ii) SMOOTH: N is (M-1)-smooth and N <= (M-1)^3.

  SEAM      hence the K0952 branch characterization of hits holds for
            t >= M-3 (M >= 7), t >= 3 (M = 5), and all t (M in {2,3});
            this sharpens the published seam t >= max(M, 3) to M-3.

Everything is deterministic.
"""
from __future__ import annotations

import math

from branch_density_core import (  # pinned K0954 core
    Branches, bh_class_expected, primes_upto, is_prime,
)


# --------------------------------------------------------------- sieving


def sieve_flags(n: int) -> bytearray:
    """bytearray f with f[i] = 1 iff i is prime, 0 <= i <= n."""
    f = bytearray(n + 1)
    f[0:2] = b"\x00\x00"
    for i in range(2, n + 1):
        f[i] = 1
    i = 2
    while i * i <= n:
        if f[i]:
            step = i
            start = i * i
            f[start:n + 1:step] = b"\x00" * (((n - start) // step) + 1)
        i += 1
    return f


# ----------------------------------------------------------- factorization


def factorize(n: int, plist) -> list:
    """Trial-division factorization of n >= 2 (plist sorted primes)."""
    fac = []
    m = n
    for p in plist:
        if p * p > m:
            break
        if m % p == 0:
            e = 0
            while m % p == 0:
                m //= p
                e += 1
            fac.append((p, e))
    if m > 1:
        fac.append((m, 1))
    return fac


def divisors_of(fac: list) -> list:
    """All divisors of n from its factorization (sorted)."""
    divs = [1]
    for (p, e) in fac:
        divs = [d * p ** i for d in divs for i in range(e + 1)]
    divs.sort()
    return divs


def dstar(n: int, divs) -> int:
    """Largest divisor of n that is <= sqrt(n) (1 if none)."""
    best = 1
    r = math.isqrt(n)
    for d in divs:
        if d <= r and d > best:
            best = d
    return best


# ------------------------------------------------------ hit predicates


def window_empty(N: int, M: int, k0: int, divs) -> bool:
    """HIT-ARITH condition (b): no divisor of N in [M, k0]."""
    for d in divs:
        if M <= d <= k0:
            return False
    return True


def hit_gap_pred(M: int, kappa: int, t: int, N: int, divs,
                 y_ok: bool) -> bool:
    """HIT-GAP right-hand side.  y_ok = [Y prime or Y = M^2]."""
    return y_ok and dstar(N, divs) < M


def branch_divisor(N: int, M: int, C: int, divs) -> int:
    """Some divisor d = C e of N with d <= M-1 and N/d prime, else 0."""
    for d in divs:
        if d >= M:
            break
        if d % C == 0 and is_prime(N // d):
            return d
    return 0


def is_smooth(fac: list, mcap: int) -> bool:
    return all(p <= mcap for (p, _e) in fac)


# ------------------------------------------------------ per-state analysis


def analyze_state(M: int, kappa: int, t: int, yflags, ycap: int,
                  plist) -> dict | None:
    """Full analysis of one main-regime state.

    Returns None when the state is not a hit; otherwise a dict with
        t, K, Y, N, k0, C, type ('branch' or 'smooth'), dstar,
        smooth (bool), n_le_cube (bool), plus the branch divisor.
    Only uses published theorems + local arithmetic (no engine call).
    """
    K = (M + 1) * t + kappa
    Y = K + 1
    y_ok = (Y == M * M) or (Y <= ycap and yflags[Y]) or \
        (Y > ycap and is_prime(Y))
    if not y_ok:
        return None
    N = M * Y - 1
    k0 = M * t + kappa - 1
    fac = factorize(N, plist)
    divs = divisors_of(fac)
    if not window_empty(N, M, k0, divs):
        return None
    C = math.gcd(M + 1, kappa + 2)
    d = branch_divisor(N, M, C, divs)
    out = {
        "M": M, "kappa": kappa, "t": t, "K": K, "Y": Y, "N": N,
        "k0": k0, "C": C, "dstar": dstar(N, divs),
        "smooth": is_smooth(fac, M - 1), "n_le_cube": N <= (M - 1) ** 3,
        "branch_d": d, "type": "branch" if d else "smooth",
    }
    return out


# ------------------------------------------------------ first-hit scan


def scan_first_hit(M: int, kappa: int, t_cap: int, yflags, ycap: int,
                   plist) -> tuple | None:
    """Smallest main-regime hit parameter t <= t_cap for the class
    (M, kappa), scanning t in increasing order.  Returns
    (t, K, type) or None.  (t,kappa) = (1,0) (the special K = M+1
    regime) is skipped for kappa = 0 by starting at t = 2."""
    t0 = 2 if kappa == 0 else 1
    C = math.gcd(M + 1, kappa + 2)
    for t in range(t0, t_cap + 1):
        Y = (M + 1) * t + kappa + 1
        if not ((Y == M * M) or (Y <= ycap and yflags[Y])
                or (Y > ycap and is_prime(Y))):
            continue
        N = M * Y - 1
        k0 = M * t + kappa - 1
        fac = factorize(N, plist)
        divs = divisors_of(fac)
        if not window_empty(N, M, k0, divs):
            continue
        d = branch_divisor(N, M, C, divs)
        return (t, Y - 1, ("branch" if d else "smooth"))
    return None


# ------------------------------------------------------ census scan


def census_pre_tail(M: int, t_hi: int, yflags, ycap: int, plist,
                    live_only: bool = True) -> list:
    """All hits with 1 <= t <= t_hi over classes of M (analysis dicts)."""
    out = []
    for kappa in range(0, M - 1):
        if live_only and math.gcd(kappa + 1, M + 1) != 1:
            continue
        t0 = 2 if kappa == 0 else 1
        for t in range(t0, t_hi + 1):
            r = analyze_state(M, kappa, t, yflags, ycap, plist)
            if r is not None:
                out.append(r)
    return out


# ---------------------------------------- corrected from-start BH model
#
# K0954's published t_hat integrated pair_integral from n = 0.  For
# branches with t_e = 0 the integrand 1/(ln(a1 n + c1) ln(a2 n + c2))
# diverges at n -> 0 (c1 = 1 for kappa = 0), so the Simpson value there
# is grid-dependent and the class expectation is not monotone in t.
# That artifact is why t_hat failed to order first hits (Spearman 0.095).
# The BH model is only meaningful on the admissible states: per branch e
# the parameter n corresponds to t = t_e + e n >= 1 with (t,kappa) != (1,0):
#     n_min(e) = 2   if e = 1, t_e = 0, kappa = 0   (t=1 excluded)
#              = 1   if t_e = 0 otherwise
#              = 0   if t_e >= 1
# On [n_min, (t - t_e)/e] both Y and Q exceed 1, the integrand is bounded,
# and the expectation is monotone in t.  first_hit_tstar below bisection-
# searches this corrected from-start expectation.


def _int_range(a1: int, c1: int, a2: int, c2: int, lo: float,
               hi: float, nodes: int = 128) -> float:
    """integral_{lo}^{hi} dn / (ln(a1 n + c1) ln(a2 n + c2)), 0 <= lo < hi,
    integrand bounded on the range (requires a1 lo + c1 >= 2)."""
    if hi <= lo:
        return 0.0
    total = 0.0
    u_hi = min(lo + 64.0, hi)
    # uniform Simpson on [lo, u_hi]
    if u_hi - lo >= 2.0:
        m = 64
        h = (u_hi - lo) / m
        s = 0.0
        for i in range(m + 1):
            f = 1.0 / (math.log(a1 * (lo + i * h) + c1)
                       * math.log(a2 * (lo + i * h) + c2))
            s += f if i in (0, m) else (4.0 * f if i % 2 else 2.0 * f)
        total += s * h / 3.0
    elif u_hi > lo:
        xm = 0.5 * (lo + u_hi)
        total += (1.0 / (math.log(a1 * xm + c1) * math.log(a2 * xm + c2))) \
            * (u_hi - lo)
    if hi > u_hi:
        prev = u_hi
        fprev = 1.0 / (math.log(a1 * prev + c1) * math.log(a2 * prev + c2))
        ratio = hi / u_hi
        for i in range(1, nodes):
            x = u_hi * ratio ** (i / (nodes - 1))
            fx = 1.0 / (math.log(a1 * x + c1) * math.log(a2 * x + c2))
            total += (x - prev) * 0.5 * (fx + fprev)
            prev, fprev = x, fx
    return total


_SS_CACHE = {}


def _ss_cached(br, e, prime_list):
    key = (br.M, br.kappa, e, len(prime_list))
    v = _SS_CACHE.get(key)
    if v is None:
        from branch_density_core import singular_series
        v = singular_series(br, e, prime_list)
        _SS_CACHE[key] = v
    return v


def branch_n_min(br, e: int) -> int:
    """Smallest admissible n on branch e (main regime, kappa class)."""
    if br.t_e[e] >= 1:
        return 0
    if e == 1 and br.kappa == 0:
        return 2
    return 1


def bh_expected_from_start(br, t: int, prime_list: list,
                           nodes: int = 128) -> float:
    """Corrected from-start BH expectation: sum over branches e of
    SS_e * integral over admissible integer candidates n, each counted
    over its unit bin [n, n+1), for n_min(e) <= n <= (t - t_e)/e.
    The published K0954 tail convention (bins [n, n+1), integral to
    n_hi) is kept; only the divergent n -> 0 artifact is removed by
    starting each branch at its admissible n_min."""
    tot = 0.0
    for e in br.e_list:
        te = br.t_e[e]
        if t < te:
            continue
        n_hi = (t - te) // e
        n_min = branch_n_min(br, e)
        if n_hi < n_min:
            continue
        ss = _ss_cached(br, e, prime_list)
        tot += ss * _int_range((br.M + 1) * e, br.c1[e], br.A, br.c2[e],
                               float(n_min), float(n_hi) + 1.0, nodes)
    return tot


def first_hit_tstar(br, prime_list: list, t_hi: int = 10 ** 6,
                    nodes: int = 128) -> float:
    """Smallest real t with corrected from-start expectation >= 1
    (bisection; the corrected expectation is monotone in t)."""
    lo, hi = 1.0, float(t_hi)
    if bh_expected_from_start(br, int(hi), prime_list, nodes) < 1.0:
        return float("inf")
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if bh_expected_from_start(br, int(mid), prime_list, nodes) >= 1.0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)
