#!/usr/bin/env python3
"""K0950 core: arithmetic reduction of the sigma_Z value-1 locus.

Composition of PUBLISHED universal theorems only:
  K0946 RUN-UNIV / ONE-CHAR-GENERAL (main-regime residue decomposition),
  K0946 EXCL-2 / EXCL-1 (kappa = M-1, M residues are never hits),
  K0948 U0-CLASSIFY (special K = M+1 case),
  K0949 PRIME-M / VALUE-ONE-CHAR / SIMPLE-CHAR
    (hit <=> M prime, k_T = M, k_{T-1} < M, spf(Y) >= M).

New here (paper proofs in report.md; every predicate below is machine
anchored against the composite_core engine by audit_build.py):
  LEMMA SQ         k0 >= sqrt(Y) in the whole main regime
  LEMMA Y-FACTOR   given spf(Y)>=M: (no MY-divisor in (M,k0])
                   <=> [Y prime or Y = M^2]
  THEOREM HIT-ARITH  main-regime hit <=> [Y prime or Y=M^2] and
                   M(M^2... (MY-1) has no divisor in [M,k0]
  LEMMA P-KILL     prime p | M+1  =>  kappa = p-1 (mod p) never hits
  THEOREM Y-PRIME  K+1 < M^2 => hit <=> K+1 prime and (b)
  THEOREM K0-FAMILY  prime M, u >= 2:
                   sigma_Z(M,(M+1)u)=1 <=> [(M+1)u+1 prime or u = M-1]
                   and rho(M,u) := [M((M+1)u+1)-1 has no divisor
                   in [M, Mu-1]]
  THEOREM M-SQ     prime M >= 3: sigma_Z(M,M^2-1)=1 <=> M^2+M+1 prime
  THEOREM PAIR-2   sigma_Z(2,3u)=1 (u>=2) <=> 3u+1 and 6u+1 both prime;
                   with the special K=3:  the full M=2 locus (K>2) is
                   {3} U {3u: u>=2, 3u+1 and 6u+1 both prime}
  THEOREM PAIR-3   sigma_Z(3,4u)=1 (u>=1) <=> (4u+1 and 6u+1 both prime)
                   or u = 2

Nothing in this file is stochastic; all sweeps are deterministic.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sievegen_core import isprime, spf


# ---------- optional fast prime flags (semantics-preserving) -------------

_FLAGS = None
_FLAGS_N = 0


def set_prime_flags(n):
    """Build a primality bytearray for [0..n]; _isp() uses it when large
    enough.  Pure speed device - does not change any predicate."""
    global _FLAGS, _FLAGS_N
    if n <= _FLAGS_N:
        return
    b = bytearray(n + 1)
    for i in range(2, n + 1):
        b[i] = 1
    i = 2
    while i * i <= n:
        if b[i]:
            b[i * i::i] = bytearray(len(range(i * i, n + 1, i)))
        i += 1
    _FLAGS = b
    _FLAGS_N = n


def _isp(n):
    if _FLAGS is not None and n <= _FLAGS_N:
        return bool(_FLAGS[n])
    return isprime(n)


# ---------- small primes / factorization machinery ----------------------

_P = []          # primes up to _P_CAP (for trial division / AP sieves)
_P_CAP = 0


def _ensure_primes(cap):
    global _P, _P_CAP
    if cap <= _P_CAP:
        return
    b = bytearray(cap + 1)
    for i in range(2, cap + 1):
        b[i] = 1
    i = 2
    while i * i <= cap:
        if b[i]:
            b[i * i::i] = bytearray(len(range(i * i, cap + 1, i)))
        i += 1
    _P = [i for i in range(2, cap + 1) if b[i]]
    _P_CAP = cap


def has_divisor_in(g, lo, hi):
    """True iff g has a divisor d with lo <= d <= hi (g >= 1)."""
    if g < 1 or hi < lo or hi < 2:
        return False
    if lo < 2:
        lo = 2
    if lo > g:
        return False
    _ensure_primes(int(g ** 0.5) + 2)
    m = g
    fac = []
    for p in _P:
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
    divs = [1]
    for (p, e) in fac:
        divs = [d * p ** i for d in divs for i in range(e + 1)]
    for d in divs:
        if lo <= d <= hi:
            return True
    return False


# ---------- THEOREM HIT-ARITH predicate ----------------------------------

def hit_special(M):
    """K = M+1 case (published K0948): sigma_Z(M,M+1)=1
    <=> M prime and spf(M+2) >= M."""
    return _isp(M) and spf(M + 2) >= M


def arith_hit(M, K):
    """Decision predicate for sigma_Z(M,K)=1 with M >= 2, K > M.

    Implements HIT-ARITH + published EXCL / PRIME-M / special case.
    K <= M is the DEG regime (K0946) and is NOT decided here."""
    if M < 2 or K <= M:
        raise ValueError("arith_hit requires M>=2, K>M")
    kap = K % (M + 1)
    if kap == M - 1 or kap == M:        # EXCL-2 / EXCL-1
        return False
    if K == M + 1:                      # special regime
        return hit_special(M)
    if not _isp(M):                      # PRIME-M
        return False
    # main regime:  kappa in [0,M-2], (s,kappa) != (0,0)
    s = (K - M - 1) // (M + 1)
    k0 = M * (s + 1) + kap - 1
    Y = K + 1
    if not (_isp(Y) or Y == M * M):      # (c)+(a) via LEMMA Y-FACTOR
        return False
    return not has_divisor_in(M * Y - 1, M, k0)   # (b)


# ---------- census over a K-range (candidates from primes) --------------

def census_hits(M, Kmax):
    """All K in (M, Kmax] with sigma_Z(M,K)=1, via HIT-ARITH.
    Enumerates Y=K+1 over primes (+ the single Y=M^2 candidate):
    by Y-FACTOR no other Y can hit, so this is an exhaustive sweep."""
    hits = []
    if M < 2 or Kmax <= M:
        raise ValueError
    if hit_special(M) and M + 1 <= Kmax:
        hits.append(M + 1)
    if not _isp(M):
        return hits
    _ensure_primes(Kmax + 2)
    Ystart = M + 3                       # skip Y = M+2 (special regime)
    for Y in _P:                         # primes up to Kmax+1
        if Y < Ystart:
            continue
        if Y > Kmax + 1:
            break
        K = Y - 1
        kap = K % (M + 1)
        if kap == M - 1 or kap == M:
            continue
        s = (K - M - 1) // (M + 1)
        k0 = M * (s + 1) + kap - 1
        if not has_divisor_in(M * Y - 1, M, k0):
            hits.append(K)
    K = M * M - 1                        # Y = M^2 candidate
    if M >= 3 and K <= Kmax:
        k0 = M * (M - 1) - 1
        if not has_divisor_in(M ** 3 - 1, M, k0):
            hits.append(K)
    return sorted(hits)


# ---------- family / pair predicates (THEOREM K0-FAMILY etc.) ------------

def rho(M, u):
    """rho(M,u) <=> M((M+1)u+1)-1 has no divisor in [M, Mu-1] (u>=2)."""
    Y = (M + 1) * u + 1
    return not has_divisor_in(M * Y - 1, M, M * u - 1)


def k0_family_hit(M, u):
    """THEOREM K0-FAMILY: sigma_Z(M,(M+1)u)=1 (prime M, u>=2)
    <=> [(M+1)u+1 prime or u = M-1] and rho(M,u)."""
    if not _isp(M) or u < 2:
        raise ValueError
    Y = (M + 1) * u + 1
    return (_isp(Y) or u == M - 1) and rho(M, u)


def msq_hit(M):
    """THEOREM M-SQ: prime M >= 3: sigma_Z(M,M^2-1)=1 <=> M^2+M+1 prime."""
    return _isp(M * M + M + 1)


def pair2_hit(u):
    """THEOREM PAIR-2: sigma_Z(2,3u)=1 (u>=2) <=> 3u+1 and 6u+1 both prime."""
    return _isp(3 * u + 1) and _isp(6 * u + 1)


def pair3_hit(u):
    """THEOREM PAIR-3: sigma_Z(3,4u)=1 (u>=1)
    <=> (4u+1 and 6u+1 both prime) or u == 2."""
    return u == 2 or (_isp(4 * u + 1) and _isp(6 * u + 1))


# ---------- AP sieves for deep pair sweeps ------------------------------

def ap_composite(a, N):
    """bytearray comp[u]=1 iff a*u+1 composite, for 0 <= u <= N."""
    lim = a * N + 1
    _ensure_primes(int(lim ** 0.5) + 2)
    comp = bytearray(N + 1)
    for p in _P:
        if p * p > lim:
            break
        if a % p == 0:
            continue                    # a*u+1 = 1 (mod p): never 0
        r = (-pow(a, -1, p)) % p
        cnt = len(range(r, N + 1, p))
        comp[r::p] = b"\x01" * cnt
        if (p - 1) % a == 0:            # a*u+1 == p is PRIME: unmark it
            u0 = (p - 1) // a
            if u0 <= N:
                comp[u0] = 0
    return comp


def pair_deep(a1, a2, N, extra=()):
    """u in [1..N] with a1*u+1 and a2*u+1 both prime, plus extra u's
    (family exceptions like u=2 for M=3), sorted."""
    c1 = ap_composite(a1, N)
    c2 = ap_composite(a2, N)
    out = [u for u in range(1, N + 1) if not c1[u] and not c2[u]]
    for u in extra:
        if 1 <= u <= N and u not in out:
            out.append(u)
    return sorted(out)


# ---------- Hardy-Littlewood machinery (conjecture-level) --------------

def singular_series(a1, a2, pmax):
    """HL singular series for the pair (a1*u+1, a2*u+1), primes <= pmax:
    prod_p (1 - nu_p/p) / (1 - 1/p)^2,  nu_p = #roots of (a1*u+1)(a2*u+1)
    = 0 mod p.  E.g. SS(3,6) = 3.96097..., SS(4,6) = 5.28128..."""
    _ensure_primes(pmax)
    prod = 1.0
    for p in _P:
        if p > pmax:
            break
        roots = set()
        if a1 % p:
            roots.add((-pow(a1, -1, p)) % p)
        if a2 % p:
            roots.add((-pow(a2, -1, p)) % p)
        nu = len(roots)
        prod *= (1.0 - nu / p) / (1.0 - 1.0 / p) ** 2
    return prod


def hl_integral(a1, a2, N):
    """sum_{u=2}^{N} 1/(ln(a1*u)*ln(a2*u))  (HL predicted pair count)."""
    import math
    tot = 0.0
    for u in range(2, N + 1):
        tot += 1.0 / (math.log(a1 * u) * math.log(a2 * u))
    return tot
