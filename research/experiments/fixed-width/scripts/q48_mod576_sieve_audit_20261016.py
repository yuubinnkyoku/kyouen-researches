#!/usr/bin/env python3
"""Independent finite checks for the 4-row/8-point-circle modulus-576 sieve.

Pure stdlib; no unbounded result is inferred from these checks.
"""
from __future__ import annotations
from fractions import Fraction
from math import gcd, isqrt, log, pi, sqrt
from collections import defaultdict

RESIDUES = (9, 23, 41, 55)


def prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


def primes_for_sieve(z: int) -> list[int]:
    return [p for p in range(7, z + 1) if p % 4 == 3 and prime(p)]


def kappa(B: int) -> int:
    return (4 if B % 2 else 32) * (6 if B % 3 == 0 else 1)


def allowed_mod576(A: int, B: int) -> bool:
    if B % 3:
        if A % 9 != 0:
            return False
    elif A % 3 == 0:
        return False
    if B % 2:
        return A % 2 == 1 and (A * pow(B, -1, 64)) % 64 in RESIDUES
    return A % 2 == 1


def feasible_lower_bound(A: int, B: int) -> bool:
    # Exact comparison A/B > sqrt(9+6 sqrt(2)), no floats.
    u = A * A - 9 * B * B
    return u > 0 and u * u > 72 * B**4


def local_sieve(A: int, B: int, z: int) -> bool:
    return all(B % p == 0 or A % p not in {B % p, -B % p, 3*B % p, -3*B % p}
               for p in primes_for_sieve(z))


def f(n: int) -> Fraction:
    if n == 1:
        return Fraction(1)
    value = Fraction(1)
    d = 2
    while d*d <= n:
        if n % d == 0:
            power = 0
            while n % d == 0:
                n //= d
                power += 1
            if power != 1 or d < 7 or d % 4 != 3 or not prime(d):
                return Fraction(0)
            value *= Fraction(4, d-4)
        d += 1
    if n > 1:
        if n < 7 or n % 4 != 3 or not prime(n):
            return Fraction(0)
        value *= Fraction(4, n-4)
    return value


def G(z: int, B: int = 1) -> Fraction:
    return sum((f(q) for q in range(1, z+1) if gcd(q, B) == 1), Fraction(0))


def F(B: int) -> Fraction:
    return sum((f(d) for d in range(1, B+1) if B % d == 0), Fraction(0))


def chord_slope(chords: tuple[int,int,int,int]) -> tuple[int,int]:
    a,b,c,d = chords
    s=(a+d)//2
    v=(c-b)//2
    g=gcd(s,v)
    return s//g,v//g


def main():
    # Every B has precisely the claimed number of residue classes modulo 576.
    for B in range(1, 577):
        actual = [A for A in range(576) if allowed_mod576(A,B)]
        assert len(actual) == kappa(B), (B, len(actual), kappa(B))
        assert all(A%2 == 1 for A in actual)
    print('CRT audit: 576 B residues, all exact; kappa(B) in {4,24,32,192}')

    # Reconstruct known increasing nonlocal 8-point circles, check the 576 classes.
    known = [(35,51,63,73), (1331,1935,2391,2773),
             (50543,73479,90795,105301),
             (98119,1096275,1547259,1893727),
             (445465,715719,908883,1067653),
             (1919303,2790267,3447819,3998665),
             (5371183,43796547,61704339,75476575)]
    for chords in known:
        A,B=chord_slope(chords)
        assert allowed_mod576(A,B) and feasible_lower_bound(A,B)
        assert all(x%2 for x in chords)
        assert chords[0]**2 - 2*chords[1]**2 + chords[2]**2 == -8
        assert chords[1]**2 - 2*chords[2]**2 + chords[3]**2 == -8
    print('Known nonlocal chord types: 7 increasing examples satisfy all restrictions')

    # Two independent computations of a finite G(z) and F(B) identity.
    for z in (11, 23, 47):
        gz=G(z)
        for B in range(1,101):
            assert gz <= F(B)*G(z,B)
    print('Sieve denominator inequality: 3 z values × 100 B values, exact rationals')

    # Check the actual one-dimensional large sieve bound on each nonempty progression.
    # It is deliberately checked *before* imposing coprimality or slope threshold.
    for H,z in ((80,11),(160,13),(300,19)):
        ps=primes_for_sieve(z)
        checked=0
        survivors=0
        for B in range(1, H+1):
            gb=G(z,B)
            classes=[a for a in range(576) if allowed_mod576(a,B)]
            for a in classes:
                # Parameterize A=a+576k in [1,H].
                ks=[k for k in range(0,(H+575)//576+2) if 1 <= a+576*k <= H]
                n=len(ks)
                if not n:
                    continue
                actual=sum(all(B%p==0 or (a+576*k)%p not in {(t*B)%p for t in (-3,-1,1,3)} for p in ps) for k in ks)
                assert actual*gb <= n+z*z, (H,B,a,actual,gb)
                checked+=1
                survivors+=actual
        print(f'Large-sieve finite audit: H={H}, z={z}, progressions={checked}, surviving integers={survivors}')

    for H in (200, 400, 800):
        z=isqrt(H)
        counts=defaultdict(int)
        for B in range(1,H+1):
            for A in range(1,H+1):
                if not feasible_lower_bound(A,B) or gcd(A,B)!=1:
                    continue
                counts['primitive_above_alpha']+=1
                if allowed_mod576(A,B):
                    counts['mod576']+=1
                    if local_sieve(A,B,z):
                        counts['mod576_and_sieved']+=1
        print(f'Finite primitive candidates H={H}, z={z}: {dict(counts)}')

    # Truncated Euler products are numerical diagnostics, NOT rigorous constants.
    E=1.; FF=1.
    for p in primes_for_sieve(100000):
        E*=p*(p-1)**2/((p-4)*(p+1)**2)
        FF*=1+4/(p*(p-4))
    alpha=sqrt(9+6*sqrt(2))
    print(f'Truncated products p<=100000: E={E:.12f}, F={FF:.12f}, alpha={alpha:.12f}')
    print(f'New limsup upper constant (truncated): {pi*pi*FF/(3*alpha*E):.9f}')
    print('PASS: finite audits only; analytic asymptotics require cited theorems')


if __name__=='__main__':
    main()
