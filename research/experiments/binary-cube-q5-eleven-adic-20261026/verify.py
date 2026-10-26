#!/usr/bin/env python3
"""Independent arithmetic checks for K0561's q=5 formula, 11-adic valuation.

The universal proof is in README.md; these tests do not replace it.
"""
from math import comb, factorial
from random import Random

COEFF = {32: 1, 24: -30, 20: 140, 18: 135, 16: -1215, 14: 2205,
         12: -1977, 10: 780, 8: 250, 6: -495, 4: 255, 2: -49}
BASE_RESIDUES = (0, 0, 0, 0, 0, 7, 8, 4, 10, 7)
DERIVATIVES = (8, 4, 10, 8, 1, 3, 10, 9, 9, 1)


def exact_exp(d):
    numerator = sum(c * a**d for a, c in COEFF.items())
    assert numerator % 120 == 0
    return numerator // 120


def mod_exp(d, t):
    """Modulo 11**t, with denominator 120 inverted as an 11-adic unit."""
    modulus = 11**t
    numerator = sum(c * pow(a, d, modulus) for a, c in COEFF.items()) % modulus
    return numerator * pow(120, -1, modulus) % modulus


def exact_stirling(d):
    """Second, structurally different, exact evaluation for small d."""
    g = [sum(c * comb(a, k) for a, c in COEFF.items() if a >= k)
         for k in range(33)]
    row = [1] + [0] * 32
    for _ in range(d):
        row = [0] + [row[k - 1] + k * row[k] for k in range(1, 33)]
    numerator = sum(g[k] * factorial(k) * row[k] for k in range(33))
    assert numerator % 120 == 0
    return numerator // 120


def valuation(n, p=11):
    assert n > 0
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def expected_valuation(d):
    assert d >= 5
    k, j = divmod(d, 10)
    return 1 + valuation(k) if j < 5 else 0


def verify():
    assert all(a % 11 != 0 for a in COEFF)
    assert tuple(exact_exp(j) % 11 for j in range(10)) == BASE_RESIDUES
    assert all(exact_exp(j) == 0 for j in range(5))
    assert tuple(((exact_exp(j + 10) - exact_exp(j)) // 11) % 11
                 for j in range(10)) == DERIVATIVES
    assert all((exact_exp(j + 10) - exact_exp(j)) % 11 == 0
               for j in range(10))
    assert all(x % 11 != 0 for x in DERIVATIVES)

    # Independent integer method: Stirling support counts, no modular exponent.
    for d in range(5, 61):
        v = exact_stirling(d)
        assert v == exact_exp(d)
        assert v % 11**5 == mod_exp(d, 5)
        assert valuation(v) == expected_valuation(d)

    # Direct modular tests at the smallest period and at nontrivial lifts.
    for t in range(1, 7):
        period = 10 * 11**(t - 1)
        for d in range(5, 125):
            assert mod_exp(d + period, t) == mod_exp(d, t)
            delta = (mod_exp(d + period, t + 1) - mod_exp(d, t + 1)) % 11**(t + 1)
            assert delta == (11**t * DERIVATIVES[d % 10]) % 11**(t + 1)

    # Finite exhaustive root classification for the first four levels.
    for t in range(1, 5):
        period = 10 * 11**(t - 1)
        roots = {d % period for d in range(5, 5 + period) if mod_exp(d, t) == 0}
        assert roots == set(range(5))

    # Very large d and arbitrary shift k: exact valuation of the difference.
    rng = Random(20261026)
    for _ in range(300):
        d = rng.randrange(5, 10**18)
        s = rng.randrange(0, 18)
        k = (11**s) * rng.randrange(1, 11)
        if k % 11 == 0:
            k //= 11
            s -= 1
        mod = 11**(s + 2)
        delta = (mod_exp(d + 10*k, s + 2) - mod_exp(d, s + 2)) % mod
        assert delta == (11*k*DERIVATIVES[d % 10]) % mod
        assert delta % 11**(s + 1) == 0 and delta != 0
        # Cross-check the explicit valuation at huge d.
        v = expected_valuation(d)
        assert mod_exp(d, v + 1) % 11**v == 0
        assert mod_exp(d, v + 1) != 0

    N = 10**18
    scale = 11**16
    achievers = tuple(10*scale*u + j for u in (1, 2) for j in range(5))
    assert len(achievers) == 10 and achievers[-1] <= N
    assert 10*11**17 > N
    assert all(expected_valuation(d) == 17 for d in achievers)
    print('base residues:', BASE_RESIDUES)
    print('11-adic shift slopes:', DERIVATIVES)
    print('verified: d=5..60 via independent Stirling integer evaluation')
    print('verified: periods and slopes t=1..6, d=5..124')
    print('verified: complete residue roots t=1..4')
    print('verified: 300 deterministic large-d difference tests')
    print('max v11 for 5 <= d <= 10^18: 17, exactly 10 achievers')
    print('achievers:', achievers)


if __name__ == '__main__':
    verify()
