#!/usr/bin/env python3
"""K0958 core: complete census of (M-1)-smooth hits of the sigma_Z
value-one locus (prime M, main regime), plus the paper lemmas
SMOOTH-LOW-OMEGA (S3) and S3' machine-checked.

Setting (K0950/K0956 notation).  Prime M, main regime
    K = (M+1) t + kappa,  t >= 1, 0 <= kappa <= M-2, (t,kappa) != (1,0),
    Y = K+1, k0 = M t + kappa - 1, N = M Y - 1,
    C = gcd(M+1, kappa+2), live: gcd(kappa+1, M+1) = 1.

Census candidate set (completeness argument in report.md):
  every smooth hit with prime M >= 5 satisfies
    Y prime,  Y <= (M-1)^3 / M,  kappa = (Y-1) mod (M+1) in [0, M-2],
    (t, kappa) != (1, 0).
  Within the candidate set, HIT-ARITH (K0950) gives
    hit  <=>  window [M, k0] empty.

Census algorithm (deterministic sieve-walk): for each small prime
p <= M-1 the candidates divisible by p are exactly the Y with
Y = M^{-1} (mod p); walk that residue class and divide out all
powers of p, recording the factorization.  A candidate is
(M-1)-smooth iff its leftover reaches 1.

Lemma S3 (universal, proved in report.md):
  N (M-1)-smooth with Omega(N) <= 3  =>  every divisor d <= sqrt(N)
  of N satisfies d <= M-1.
Lemma S3' (universal, proved):
  main-regime state, prime M, [Y ok], N (M-1)-smooth, Omega(N) <= 3
    =>  sigma_Z(M,K) = 1  (no window test needed).
Machine check: among census candidates, no Omega<=3 candidate is
window-blocked (equivalent: every blocked candidate has Omega >= 4).

Everything is deterministic.
"""
from __future__ import annotations

import math

from branch_density_core import primes_upto, is_prime  # pinned K0954 core
from prehit_core import divisors_of, dstar, branch_divisor, \
    window_empty, factorize  # pinned K0956 core


# ------------------------------------------------------------- sieving


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


# -------------------------------------------------------- window test


def window_blocked(N: int, M: int, k0: int, fac: list) -> bool:
    """True iff some divisor of N lies in [M, k0] (fac = factorization
    of N as a list of (p, e)).  DFS over divisor products with the
    prune prod > k0; explores exactly the divisors <= k0."""
    found = False
    nf = len(fac)

    def rec(i: int, prod: int) -> None:
        nonlocal found
        if prod > k0:
            return
        if prod >= M:
            found = True
            return
        if i == nf:
            return
        p, e = fac[i]
        pe = 1
        for _ in range(e + 1):
            if found:
                return
            rec(i + 1, prod * pe)
            pe *= p

    rec(0, 1)
    return found


# ------------------------------------------------------ census walk


def census_walk(M: int, ymax: int, yflags: bytearray, small: list):
    """Deterministic census of the candidate set for one M.

    Returns (cand, stats) where cand maps Y -> [leftover, fac] for the
    (M-1)-smooth candidates (leftover == 1) and stats carries counts.
    fac is a list of [p, e].  small = primes <= M-1 (sorted)."""
    Mp1 = M + 1
    cand = {}
    n_cand = 0
    for Y in range(M + 2, ymax + 1):
        if not yflags[Y]:
            continue
        kap = (Y - 1) % Mp1
        if kap > M - 2:
            continue
        if kap == 0 and (Y - 1) // Mp1 == 1:
            continue  # special state (t,kappa) = (1,0)
        cand[Y] = [M * Y - 1, []]
        n_cand += 1
    dead = 0
    for Y in cand:
        kap = (Y - 1) % Mp1
        if math.gcd(kap + 1, Mp1) != 1:
            dead += 1
    n_steps = 0
    for p in small:
        r = pow(M, -1, p)
        start = r + ((M + 2 - r + p - 1) // p) * p
        for Y in range(start, ymax + 1, p):
            v = cand.get(Y)
            if v is None:
                continue
            n_steps += 1
            lv, fac = v
            e = 0
            while lv % p == 0:
                lv //= p
                e += 1
            if e:
                fac.append([p, e])
                v[0] = lv
    smooth = {Y: v for Y, v in cand.items() if v[0] == 1}
    stats = {"n_cand": n_cand, "n_steps": n_steps, "dead_cand": dead}
    return smooth, cand, stats


def classify_candidates(M: int, smooth: dict):
    """Split smooth candidates into hits / blocked; per-candidate
    Omega and window status.  Returns (hits, blocked) lists of dicts."""
    Mp1 = M + 1
    hits = []
    blocked = []
    for Y in sorted(smooth):
        v = smooth[Y]
        fac = [(p, e) for (p, e) in v[1]]
        kap = (Y - 1) % Mp1
        t = (Y - 1 - kap) // Mp1
        K = Mp1 * t + kap
        N = M * Y - 1
        k0 = M * t + kap - 1
        Om = sum(e for (_p, e) in fac)
        blk = window_blocked(N, M, k0, fac)
        row = {
            "M": M, "kappa": kap, "t": t, "K": K, "Y": Y, "N": N,
            "k0": k0, "C": math.gcd(Mp1, kap + 2), "Omega": Om,
            "omega": len(fac),
        }
        if blk:
            blocked.append(row)
        else:
            hits.append(row)
    return hits, blocked


def enrich_hits(M: int, hits: list, plist_big: list) -> None:
    """In place: factorization string, dstar, branch type for hits."""
    for h in hits:
        fac = factorize(h["N"], plist_big)
        divs = divisors_of(fac)
        h["dstar"] = dstar(h["N"], divs)
        d = branch_divisor(h["N"], M, h["C"], divs)
        h["branch_d"] = d
        h["type"] = "branch" if d else "smooth-only"
        h["fac"] = "*".join("%d^%d" % (p, e) if e > 1 else "%d" % p
                            for (p, e) in fac)
