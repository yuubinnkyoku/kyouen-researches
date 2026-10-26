#!/usr/bin/env python3
"""Exact small-prime q=5 period certificate; Python standard library only."""
from math import comb, factorial

TERMS = ((32, 1), (24, -30), (20, 140), (18, 135), (16, -1215),
         (14, 2205), (12, -1977), (10, 780), (8, 250), (6, -495),
         (4, 255), (2, -49))
PRIMES = (7, 11, 13, 17, 19, 23, 29, 31)


def e_mod(d, modulus):
    assert modulus % 2 and modulus % 3 and modulus % 5
    return (sum(c * pow(a, d, modulus) for a, c in TERMS)
            * pow(120, -1, modulus)) % modulus


def prime_factors(n):
    out = []
    q = 2
    while q * q <= n:
        if n % q == 0:
            out.append(q)
            while n % q == 0:
                n //= q
        q += 1
    if n > 1:
        out.append(n)
    return out


def stirling_check():
    # Power-sum coefficients -> falling-factorial/Stirling coefficients.
    g = [sum(c * comb(a, k) for a, c in TERMS if a >= k)
         for k in range(33)]
    assert all(v >= 0 for v in g)
    s = [0] * 33
    s[0] = 1
    for d in range(1, 66):
        s = [0] + [k * s[k] + s[k - 1] for k in range(1, 33)]
        if d >= 5:
            v = sum(g[k] * factorial(k) * s[k] for k in range(33))
            assert v % 120 == 0
            direct = sum(c * a ** d for a, c in TERMS)
            assert v == direct, (d, v, direct)
    print("Stirling/falling-factorial cross-check: d=5..65 PASS")


def check():
    stirling_check()
    print("p | P | differences for P/ell | slope witness d | slope | periods t=1..3")
    for p in PRIMES:
        P = p - 1
        fac = prime_factors(P)
        differences = [(e_mod(5 + P // ell, p) - e_mod(5, p)) % p
                       for ell in fac]
        assert all(differences), (p, differences)
        d_slope = 5 if ((e_mod(5 + P, p * p)
                         - e_mod(5, p * p)) % (p * p)) else 6
        slope = ((e_mod(d_slope + P, p * p)
                  - e_mod(d_slope, p * p)) % (p * p)) // p
        assert slope != 0
        periods = []
        for t in (1, 2, 3):
            modulus = p ** t
            T = P * p ** (t - 1)
            start = max(5, t)
            vals = [e_mod(d, modulus)
                    for d in range(start, start + 2 * T)]
            assert all(vals[i] == vals[i + T] for i in range(T))
            for ell in prime_factors(T):
                shorter = T // ell
                assert any(vals[i] != vals[i + shorter]
                           for i in range(T))
            periods.append(T)
        print(f"{p} | {P} | {dict(zip(fac, differences))} | "
              f"{d_slope} | {slope} | {periods}")
    print("PASS")


if __name__ == "__main__":
    check()
