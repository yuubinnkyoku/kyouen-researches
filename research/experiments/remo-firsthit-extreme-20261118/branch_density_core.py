#!/usr/bin/env python3
"""K0953 core: admissible-branch structure, singular series, and exact
value-one tail counting for sigma_Z(M,(M+1)t+kappa).

Builds on K0952 (HIT-TAIL-SMOOTH exact reduction of the tail to a finite
union of prime pairs) and K0950 (HIT-ARITH).  For prime M, live kappa
(gcd(kappa+1,M+1)=1) define

    C = gcd(M+1, kappa+2),  A = M(M+1)/C,  B = (M(kappa+1)-1)/C,
    Q(t) = A t + B,  Y(t) = (M+1)t + kappa+1,

and the branch set
    E(M,kappa) = { e : 1 <= e <= (M-1)//C, gcd(e,A)=1 }.

Branch e contributes the prime pair
    Y_e(n) = (M+1)(t_e + e n) + kappa + 1,
    P_e(n) = (A(t_e + e n) + B)/e,     t_e = (-B) * A^{-1} mod e.

New machine-checkable claims (paper proofs in report.md):

  ALL-ADM     every branch pair (Y_e, P_e) is locally admissible at every
              prime (generalizes K0952's e=1 result to all e in E).
  SS-STRUCT   the Bateman-Horn singular series of branch e is
                  SS_e = G(M,C) * prod_{q|e, q !| M(M+1)} (q-1)/(q-2),
              a function of (M, C) and e alone; in particular the HL
              density of a live class depends on kappa only through C.
"""
from __future__ import annotations

import math

# ---------------------------------------------------------------- primes


def primes_upto(n: int) -> list[int]:
    b = bytearray(b"\x01") * (n + 1)
    if n >= 0:
        b[0] = 0
    if n >= 1:
        b[1] = 0
    for p in range(2, math.isqrt(n) + 1):
        if b[p]:
            b[p * p:n + 1:p] = b"\x00" * (((n - p * p) // p) + 1)
    return [i for i, v in enumerate(b) if v]


def sieve_set(n: int) -> bytearray:
    b = bytearray(b"\x01") * (n + 1)
    b[0:2] = b"\x00\x00"
    for p in range(2, math.isqrt(n) + 1):
        if b[p]:
            b[p * p:n + 1:p] = b"\x00" * (((n - p * p) // p) + 1)
    return b


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


# ------------------------------------------------------------- branches


class Branches:
    __slots__ = ("M", "kappa", "C", "A", "B", "live", "e_list",
                 "t_e", "c1", "c2")

    def __init__(self, M: int, kappa: int):
        self.M = M
        self.kappa = kappa
        self.live = math.gcd(kappa + 1, M + 1) == 1
        self.C = math.gcd(M + 1, kappa + 2)
        self.A = M * (M + 1) // self.C
        self.B = (M * (kappa + 1) - 1) // self.C
        emax = (M - 1) // self.C
        self.e_list = []
        self.t_e = {}
        self.c1 = {}
        self.c2 = {}
        for e in range(1, emax + 1):
            if math.gcd(e, self.A) != 1:
                continue
            te = (-self.B * pow(self.A, -1, e)) % e if e > 1 else 0
            self.e_list.append(e)
            self.t_e[e] = te
            self.c1[e] = (M + 1) * te + kappa + 1
            self.c2[e] = (self.A * te + self.B) // e

    def __len__(self) -> int:
        return len(self.e_list)


def _v(q: int, n: int) -> int:
    v = 0
    while n % q == 0:
        n //= q
        v += 1
    return v


def nu_pair(q: int, a1: int, c1: int, a2: int, c2: int) -> int:
    """#residues n mod q with q | (a1 n + c1) or q | (a2 n + c2).
    O(q) brute force; use only for validation batteries."""
    cnt = 0
    for n in range(q):
        if (a1 * n + c1) % q == 0 or (a2 * n + c2) % q == 0:
            cnt += 1
    return cnt


def obstructed(q: int, a1: int, c1: int, a2: int, c2: int) -> bool:
    """True iff the pair has a fixed prime divisor at q:
    every n mod q satisfies q | (a1 n + c1) or q | (a2 n + c2)."""
    if (a1 % q == 0) and (c1 % q == 0):
        return True
    if (a2 % q == 0) and (c2 % q == 0):
        return True
    if a1 % q and a2 % q:
        # each form has exactly one root mod q; full coverage happens
        # only when q = 2 and the two roots are DISTINCT
        if q == 2 and (a2 * c1 - a1 * c2) % 2:
            return True
    return False


def nu_case(q: int, M: int, kappa: int, e: int, C: int, A: int) -> int:
    """Closed-form nu(q) for the branch pair (report.md SS-STRUCT):
      0 iff q | M+1 and v_q(kappa+2) < v_q(M+1)
      1 iff q | M, or q | e with q !| M+1, or q | M+1 with
          v_q(kappa+2) >= v_q(M+1)
      2 otherwise.
    (For q | M+1 the test is v_q(C) = v_q(M+1), equivalent because
     v_q(C) = min(v_q(M+1), v_q(kappa+2)).)"""
    if q == 2:
        if M == 2:
            return 1
        return 1 if _v(2, C) >= _v(2, M + 1) else 0
    if q % M == 0:
        return 1
    if (M + 1) % q == 0:
        return 1 if _v(q, C) >= _v(q, M + 1) else 0
    if e % q == 0:
        return 1
    return 2


def singular_series(br: "Branches", e: int, prime_list: list[int]) -> float:
    """SS_e via the closed form SS-STRUCT (primes in prime_list)."""
    M, C = br.M, br.C
    ss = 1.0
    for q in prime_list:
        nu = nu_case(q, M, br.kappa, e, C, br.A)
        ss *= (1 - nu / q) / (1 - 1.0 / q) ** 2
    return ss


# ------------------------------------------------------- exact tail hits


def tail_hits(br: "Branches", t_lo: int, t_hi: int, y_is_prime) -> int:
    """Exact number of value-one positions with t_lo <= t <= t_hi in the
    class (M,kappa), via the K0952 branch union.  t_lo >= max(M,3)."""
    if not br.live:
        return 0
    n_hits = 0
    for e in br.e_list:
        te = br.t_e[e]
        n_lo = max(0, -((te - t_lo) // e))     # ceil((t_lo - te)/e), >= 0
        for n in range(n_lo, (t_hi - te) // e + 1):
            t = te + e * n
            Y = (br.M + 1) * t + br.kappa + 1
            if not y_is_prime(Y):
                continue
            P = (br.A * t + br.B) // e
            if is_prime(P):
                n_hits += 1
    return n_hits


def branch_of(br: "Branches", t: int):
    """The (unique) branch e of a hit at parameter t, or None.
    Uniqueness: e = D/C with D the M-smooth part of N (K0952)."""
    for e in br.e_list:
        if (t - br.t_e[e]) % e == 0:
            P = (br.A * t + br.B) // e
            if P * e == br.A * t + br.B and is_prime(P):
                return e
    return None


# --------------------------------------------------------- BH integral


def _integrand(x: float, a1: int, c1: int, a2: int, c2: int) -> float:
    v1 = a1 * x + c1
    v2 = a2 * x + c2
    if v1 <= 1 or v2 <= 1:
        return 0.0
    return 1.0 / (math.log(v1) * math.log(v2))


def pair_integral(a1: int, c1: int, a2: int, c2: int, n_hi: int,
                  nodes: int = 128) -> float:
    """integral_0^{n_hi} dn / (ln(a1 n + c1) * ln(a2 n + c2)).
    Hybrid grid: uniform Simpson on [0, min(64, n_hi)], log-spaced
    trapezoid on [64, n_hi]."""
    if n_hi <= 0:
        return 0.0
    total = 0.0
    u_hi = min(64, n_hi)
    if u_hi >= 2:
        m = 64
        h = u_hi / m
        s = _integrand(0.0, a1, c1, a2, c2) + _integrand(u_hi, a1, c1, a2, c2)
        for i in range(1, m):
            s += (4.0 if i % 2 else 2.0) * _integrand(i * h, a1, c1, a2, c2)
        total += s * h / 3.0
    else:
        total += _integrand(n_hi / 2.0, a1, c1, a2, c2) * n_hi
    if n_hi > 64:
        prev = 64.0
        fprev = _integrand(prev, a1, c1, a2, c2)
        ratio = n_hi / 64.0
        for i in range(1, nodes):
            x = 64.0 * ratio ** (i / (nodes - 1))
            fx = _integrand(x, a1, c1, a2, c2)
            total += (x - prev) * 0.5 * (fx + fprev)
            prev, fprev = x, fx
    return total


def bh_expected_hits(br: "Branches", e: int, t: int,
                     prime_list: list[int], nodes: int = 128) -> float:
    """BH-expected number of branch-e hits with parameter <= t.

    Bateman-Horn for the pair (Y_e(n), P_e(n)) counts n <= (t-t_e)/e
    directly; the 1/e of the t-density is the Jacobian dn = dt/e and
    must NOT be applied again."""
    ss = singular_series(br, e, prime_list)
    te = br.t_e[e]
    n_hi = (t - te) // e
    if n_hi < 0:
        return 0.0
    return ss * pair_integral((br.M + 1) * e, br.c1[e],
                              br.A, br.c2[e], n_hi, nodes)


def bh_class_expected(br: "Branches", t: int, prime_list: list[int],
                      nodes: int = 128) -> float:
    return sum(bh_expected_hits(br, e, t, prime_list, nodes)
               for e in br.e_list)


def first_hit_t(br: "Branches", prime_list: list[int],
                t_hi: int = 10 ** 9, nodes: int = 128) -> float:
    """Predicted first-hit parameter: smallest t with BH expected
    class hits >= 1 (bisection on ln t)."""
    lo, hi = 1.0, float(t_hi)
    if bh_class_expected(br, int(hi), prime_list, nodes) < 1.0:
        return float("inf")
    for _ in range(40):
        mid = math.sqrt(lo * hi)
        if bh_class_expected(br, int(mid), prime_list, nodes) >= 1.0:
            hi = mid
        else:
            lo = mid
    return math.sqrt(lo * hi)
