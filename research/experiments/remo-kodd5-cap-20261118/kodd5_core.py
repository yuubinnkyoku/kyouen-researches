#!/usr/bin/env python3
"""K0963 core: COPRIME-KILL zone machinery and kodd=5 caps.

Independent implementation (no imports from earlier experiment modules)
of the main-regime arithmetic and the zone predicates used by the
K0963 audit and sweep:

  * regime: K=(M+1)t+kappa, Y=K+1, N=MY-1, k0=Mt+kappa-1,
    N=(M+1)k0+2M-kappa, 0<=kappa<=M-2, (t,kappa)!=(1,0), a=v2(N)>=1;
  * XBAR = (M+1)k0/(M-1), compared in exact integer arithmetic
    (d >= XBAR  <=>  d*(M-1) >= (M+1)*k0);
  * EW (EFFECTIVE-WINDOW, K0961 T3, t>=1): no divisor of N in [M, XBAR);
  * CK (COPRIME-KILL, new, t>=1): no two coprime divisors of N are both
    >= XBAR.  Proof: coprime d,e | N give de | N, but
    de >= XBAR^2 > N (identity check in the report), contradiction.
  * TZ (TWO-ZONE, K0961 T1, t>=2): every odd divisor q<=M-1 of N has
    2^a*q <= M-1;
  * CS (COMPLEMENT-SMALL, new, t>=2): every squarefree product Q_S of
    distinct odd primes with Q_S >= XBAR has 2^a*Q_{S^c} <= M-1, where
    Q_{S^c} is the complementary squarefree product;
  * kodd=5 (r=5) config classification of the zone-2 pair family F and
    the per-config caps proved in the K0963 report:

      CAP-73:  k0^3 * 2^{4a} * (M+1)^3 < (M-1)^7          (F subsets of
               {45},{45,14},{45,24},{45,15},{45,25})
      CAP-27:  27 * k0 * 2^{2a} * (M+1) <= (M-1)^3       ({45,34},{45,35}
               via XBAR*p1*p2^2 <= sigma^2 (123/34/24 resp. 123/35/25
               route); and the exceptional {45,34,35} branch with all of
               134,135,234,235 >= XBAR via XBAR*p1*p2^2 <= sigma^2
               (125/45/14 route))
      CAP-52:  k0^2 * 2^{3a} * (M+1)^2 <= (M-1)^5        (Case A and the
               quad-route Case-B configs)

    Universal corollary: kodd=5 & t>=2 implies
    k0 <= max(CAP-52, CAP-27) bound, in particular t < sqrt(M) + slack;
    with the census (M<=2000) this decides t<=3 there.
"""
from __future__ import annotations

import math

_MR_BASES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for p in _MR_BASES:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in _MR_BASES:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        ok = False
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                ok = True
                break
        if not ok:
            return False
    return True


def primes_upto(n: int) -> list[int]:
    b = bytearray(b"\x01") * (n + 1)
    b[0:2] = b"\x00\x00"
    for p in range(2, math.isqrt(n) + 1):
        if b[p]:
            b[p * p:n + 1:p] = b"\x00" * (((n - p * p) // p) + 1)
    return [i for i, v in enumerate(b) if v]


# --------------------------------------------------------------- regime

class Regime:
    """Main-regime state for prime M, live (t, kappa)."""

    def __init__(self, M: int, kap: int, t: int):
        assert is_prime(M) and M >= 5
        assert 0 <= kap <= M - 2 and (t, kap) != (1, 0) and t >= 1
        self.M, self.kap, self.t = M, kap, t
        self.K = (M + 1) * t + kap
        self.Y = self.K + 1
        self.N = M * self.Y - 1
        self.k0 = M * t + kap - 1
        assert self.N == (M + 1) * self.k0 + 2 * M - kap
        self.a = (self.N & -self.N).bit_length() - 1
        # sigma = (M-1)/2^a  (real); integer test: q <= sigma <=> 2^a*q <= M-1
        self.p2a = 1 << self.a

    # XBAR = (M+1)*k0/(M-1); exact comparisons
    def ge_xbar(self, d: int) -> bool:
        return d * (self.M - 1) >= (self.M + 1) * self.k0

    def le_sigma(self, q: int) -> bool:
        return self.p2a * q <= self.M - 1

    def factor(self, small_primes: list[int]) -> tuple[list[tuple[int, int]], int]:
        """Factor N by ALL primes <= M-1; return (facs, leftover).
        leftover == 1  <=>  N is (M-1)-smooth."""
        facs = []
        m = self.N
        for p in small_primes:
            if p > self.M - 1:
                break
            if m % p == 0:
                e = 0
                while m % p == 0:
                    m //= p
                    e += 1
                facs.append((p, e))
        return facs, m

    def full_factor(self, small_primes: list[int]) -> list[tuple[int, int]]:
        """Complete factorization; for non-smooth N the leftover (>1)
        has all prime factors > M-1 and is factored by trial division."""
        facs, left = self.factor(small_primes)
        if left > 1:
            if is_prime(left):
                facs.append((left, 1))
            else:
                m = left
                p = 2
                while p * p <= m:
                    while m % p == 0:
                        facs.append((p, 1))
                        m //= p
                    p += 1 if p == 2 else 2
                if m > 1:
                    facs.append((m, 1))
        return _merge(facs)


def _merge(facs: list[tuple[int, int]]) -> list[tuple[int, int]]:
    d: dict[int, int] = {}
    for p, e in facs:
        d[p] = d.get(p, 0) + e
    return sorted(d.items())


def divisors(facs: list[tuple[int, int]]) -> list[int]:
    divs = [1]
    for p, e in facs:
        pe = 1
        new = []
        for _ in range(e):
            pe *= p
            new.extend(d * pe for d in divs)
        divs += new
    divs.sort()
    return divs


# ------------------------------------------------------------ predicates

def check_ew(reg: Regime, divs: list[int]) -> bool:
    """EFFECTIVE-WINDOW: no divisor of N in [M, XBAR)."""
    for d in divs:
        if d >= reg.M and not reg.ge_xbar(d):
            return False
    return True


def check_ck(reg: Regime, divs: list[int], facs: list[tuple[int, int]]) -> bool:
    """COPRIME-KILL: no two coprime divisors both >= XBAR.

    A coprime pair (d, e) with both >= XBAR would give de | N and
    de >= XBAR^2 > N.  It suffices to test, for every divisor d >= XBAR,
    whether the full product of the prime powers of the primes NOT in
    supp(d) is >= XBAR (that product is a divisor coprime to d).
    """
    # full-power product over primes not dividing d
    full = {p: p ** e for p, e in facs}
    for d in divs:
        if not reg.ge_xbar(d):
            continue
        rest = 1
        for p, pw in full.items():
            if d % p:
                rest *= pw
        if reg.ge_xbar(rest):
            return False
    return True


def check_tz(reg: Regime, divs: list[int]) -> bool:
    """TWO-ZONE (t>=2): odd divisor q<=M-1 => 2^a*q <= M-1."""
    for d in divs:
        if d % 2 == 1 and d <= reg.M - 1:
            if reg.p2a * d > reg.M - 1:
                return False
    return True


def check_cs(reg: Regime, odd_primes: list[int]) -> bool:
    """COMPLEMENT-SMALL / PARTITION-KILL (t>=2), multiplicity-safe.

    odd_primes = the odd primes of N WITH multiplicity (sorted).  For
    every index subset S of the multiset with prod(S) >= XBAR, the
    partition complement prod(S^c) = (N/2^a)/prod(S) satisfies
        prod(S^c) < XBAR   (since prod(S)*prod(S^c) = N/2^a < XBAR^2)
    hence by EW prod(S^c) <= M-1 and by TZ 2^a*prod(S^c) <= M-1.

    No coprimality is used: S and S^c partition the prime MULTISET,
    so their product is exactly N/2^a.  In this form the K0963 proofs
    apply with kodd counted WITH multiplicity (published convention
    kodd = Omega(N/2^a))."""
    r = len(odd_primes)
    for mask in range(1, 1 << r):
        qs = 1
        for i in range(r):
            if mask >> i & 1:
                qs *= odd_primes[i]
        if reg.ge_xbar(qs):
            qc = 1
            for i in range(r):
                if not (mask >> i & 1):
                    qc *= odd_primes[i]
            if reg.p2a * qc > reg.M - 1:
                return False
    return True


def check_pair_intersect(reg: Regime, odd: list[int]) -> bool:
    """PAIR-INTERSECT (multiplicity-safe): no two index-disjoint pairs
    both have product >= XBAR (their product is a sub-multiset product
    dividing N, hence <= N/2^a < XBAR^2)."""
    r = len(odd)
    big = [(i, j) for i in range(r) for j in range(i + 1, r)
           if reg.ge_xbar(odd[i] * odd[j])]
    for x in range(len(big)):
        for y in range(x + 1, len(big)):
            a1, a2 = big[x]
            b1, b2 = big[y]
            if len({a1, a2, b1, b2}) == 4:
                return False
    return True


def check_general_facts(reg: Regime, odd: list[int]) -> dict:
    """For kodd>=5, t>=2: p1p2<=sigma, p2p3<=sigma, p1<=sqrt(sigma),
    p2<=sqrt(sigma); for r>=6 also p3p4<=sigma, p3<=sqrt(sigma)."""
    out = {"p1p2": reg.le_sigma(odd[0] * odd[1]),
           "p2p3": reg.le_sigma(odd[1] * odd[2]),
           "p1_sqrt": reg.p2a * odd[0] * odd[0] <= reg.M - 1,
           "p2_sqrt": reg.p2a * odd[1] * odd[1] <= reg.M - 1}
    if len(odd) >= 6:
        out["p3p4"] = reg.le_sigma(odd[2] * odd[3])
        out["p3_sqrt"] = reg.p2a * odd[2] * odd[2] <= reg.M - 1
    return out


# --------------------------------------------------------- kodd=5 configs

# zone-2 pair family F for r=5 (pairs "ij", i<j, product >= XBAR).
# CK forces: F pairwise intersecting; if F nonempty then 45 in F and
# 12,13,23 not in F.  Config -> cap predicate name.
K5_ROUTE = {
    frozenset(): ("A", "cap52"),
    frozenset({"45"}): ("B1", "cap73"),
    frozenset({"45", "14"}): ("B2-14", "cap73"),
    frozenset({"45", "24"}): ("B2-24", "cap73"),
    frozenset({"45", "15"}): ("B3-15", "cap73"),
    frozenset({"45", "25"}): ("B3-25", "cap73"),
    frozenset({"45", "34"}): ("B2-34", "cap27"),
    frozenset({"45", "35"}): ("B3-35", "cap27"),
    frozenset({"45", "14", "15"}): ("B4-1", "cap52"),
    frozenset({"45", "24", "25"}): ("B4-2", "cap52"),
    frozenset({"45", "14", "24"}): ("B5-1424", "cap52"),
    frozenset({"45", "14", "34"}): ("B5-1434", "cap52"),
    frozenset({"45", "24", "34"}): ("B5-2434", "cap52"),
    frozenset({"45", "14", "24", "34"}): ("B5-max", "cap52"),
    frozenset({"45", "15", "25"}): ("B6-1525", "cap52"),
    frozenset({"45", "15", "35"}): ("B6-1535", "cap52"),
    frozenset({"45", "25", "35"}): ("B6-2535", "cap52"),
    frozenset({"45", "15", "25", "35"}): ("B6-max", "cap52"),
    frozenset({"45", "34", "35"}): ("B4-3", "cap52_or_27"),  # split below
}


def k5_config(reg: Regime, odd: list[int]) -> dict:
    """Classify an r=5, t>=2 row.  Returns config label, route, and the
    triple-zone data for the exceptional {45,34,35} split."""
    assert len(odd) == 5
    p = odd
    pairs = [("12", 0, 1), ("13", 0, 2), ("14", 0, 3), ("15", 0, 4),
             ("23", 1, 2), ("24", 1, 3), ("25", 1, 4),
             ("34", 2, 3), ("35", 2, 4), ("45", 3, 4)]
    F = frozenset(lab for lab, i, j in pairs if reg.ge_xbar(p[i] * p[j]))
    cfg, route = K5_ROUTE[F]
    out = {"F": sorted(F), "config": cfg, "route": route}
    if F == frozenset({"45", "34", "35"}):
        trip = {"134": p[0] * p[2] * p[3], "135": p[0] * p[2] * p[4],
                "234": p[1] * p[2] * p[3], "235": p[1] * p[2] * p[4]}
        big = {k: reg.ge_xbar(v) for k, v in trip.items()}
        out["exc_all_big"] = all(big.values())
        out["route"] = "cap27" if out["exc_all_big"] else "cap52"
    return out


def cap_check(reg: Regime, route: str) -> dict:
    """Check the per-config cap (integer form)."""
    k0, M, a = reg.k0, reg.M, reg.a
    res = {}
    res["cap52"] = k0 * k0 * (1 << (3 * a)) * (M + 1) ** 2 <= (M - 1) ** 5
    res["cap73"] = k0 ** 3 * (1 << (4 * a)) * (M + 1) ** 3 < (M - 1) ** 7
    res["cap27"] = 27 * k0 * (1 << (2 * a)) * (M + 1) <= (M - 1) ** 3
    ok = {"cap52": res["cap52"], "cap73": res["cap73"],
          "cap27": res["cap27"],
          "cap52_or_27": res["cap52"] or res["cap27"]}
    return {"holds": ok[route], "detail": res, "route": route}


def k0_caps(M: int, a: int = 1) -> dict:
    """Largest k0 allowed by CAP-52 / CAP-27 / CAP-73 / SQRT3 (real caps
    floor'd), for band planning."""
    k52 = math.isqrt((M - 1) ** 5 // ((1 << (3 * a)) * (M + 1) ** 2))
    k27 = (M - 1) ** 3 // (27 * (1 << (2 * a)) * (M + 1))
    c7 = (M - 1) ** 7 // ((1 << (4 * a)) * (M + 1) ** 3)
    k73 = round(c7 ** (1 / 3))
    while k73 ** 3 * (1 << (4 * a)) * (M + 1) ** 3 >= (M - 1) ** 7:
        k73 -= 1
    while (k73 + 1) ** 3 * (1 << (4 * a)) * (M + 1) ** 3 < (M - 1) ** 7:
        k73 += 1
    return {"cap52": k52, "cap27": k27, "cap73": k73}


def band_tmax(M: int) -> int:
    """Largest t for which a kodd=5 hit could exist (a=1 worst case),
    i.e. the search band [4, band_tmax(M)] is complete for kodd=5."""
    c = k0_caps(M, 1)
    t52 = (c["cap52"] + 1) // M
    t27 = (c["cap27"] + 1) // M
    return max(t52, t27)


# --------------------------------------------------- kodd>=6 case labels

def k6plus_case(reg: Regime, odd: list[int]) -> dict:
    """Case label for r>=6, t>=2:
       PS       all pairs < XBAR  -> CAP-52 holds (prefix route)
       LG-PF    largest pair >= XBAR and some prefix P_j (3<=j<=r-3)
                >= XBAR -> CAP-52 holds
       LG-OPEN  largest pair >= XBAR and all prefixes <= sigma (open)
    """
    r = len(odd)
    p = odd
    L = p[-2] * p[-1]
    if not reg.ge_xbar(L):
        case = "PS"
    else:
        # all pairs within first r-2 primes must be <= sigma (CK vs L)
        for i in range(r - 2):
            for j in range(i + 1, r - 2):
                assert reg.le_sigma(p[i] * p[j]), "CK violation (r>=6)"
        # P_{r-2} <= sigma (complement of {r-1,r})
        pref = 1
        for x in p[:r - 2]:
            pref *= x
        assert reg.le_sigma(pref), "CS violation (r>=6)"
        case = "LG-OPEN"
        pref = 1
        for j in range(3, r - 2):          # prefixes P_3..P_{r-3}
            pref *= p[j - 1]
            if reg.ge_xbar(pref):
                case = "LG-PF"
                break
    return {"case": case}
