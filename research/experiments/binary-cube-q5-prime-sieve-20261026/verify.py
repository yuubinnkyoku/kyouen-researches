#!/usr/bin/env python3
"""Exact finite certificate for q=5 regular prime residues 32<p<1000.

The all-dimensional implication is the proved lemma in
research/experiments/binary-cube-q5-prime-regular-20261026/README.md.
"""
from math import comb, factorial, isqrt

COEFF = {32: 1, 24: -30, 20: 140, 18: 135, 16: -1215,
         14: 2205, 12: -1977, 10: 780, 8: 250,
         6: -495, 4: 255, 2: -49}
BOUND = 1000
LIMIT = 10**18
REGULAR = [37, 47, 59, 67, 79, 101, 193, 233, 271, 313,
           379, 439, 503, 547, 557, 601, 607, 857, 947, 967, 991]


def primes_below(bound):
    return [p for p in range(37, bound)
            if all(p % a for a in range(2, isqrt(p) + 1))]


def exp_mod(d, mod):
    return sum(c * pow(a, d, mod) for a, c in COEFF.items()) * pow(120, -1, mod) % mod


def stirling_mod_values(end, mod):
    """Independent arithmetic route: Stirling recurrence, not power sums."""
    g = [sum(c * comb(a, k) for a, c in COEFF.items() if a >= k)
         for k in range(33)]
    weights = [g[k] * factorial(k) % mod for k in range(33)]
    row = [1] + [0] * 32
    inv = pow(120, -1, mod)
    for d in range(end + 1):
        yield sum(weights[k] * row[k] for k in range(33)) * inv % mod
        row = [0] + [(row[k-1] + k * row[k]) % mod for k in range(1, 33)]


def main():
    regular = []
    fail_extra_root = []
    fail_zero_slope = []
    for p in primes_below(BOUND):
        mod = p * p
        # Two arithmetically distinct algorithms check every d=0..2p-3.
        values = list(stirling_mod_values(2 * p - 3, mod))
        assert len(values) == 2 * p - 2
        for d, v in enumerate(values):
            assert v == exp_mod(d, mod), (p, d)
        roots = [j for j in range(p - 1) if values[j] % p == 0]
        slopes = [((values[j+p-1]-values[j]) % mod) // p
                  for j in range(p-1)]
        assert all((values[j+p-1]-values[j]) % p == 0 for j in range(p-1))
        extra = [j for j in roots if j >= 5]
        zeros = [j for j, v in enumerate(slopes) if v == 0]
        assert roots[:5] == list(range(5))
        if extra:
            fail_extra_root.append(p)
        if zeros:
            fail_zero_slope.append(p)
        if not extra and not zeros:
            regular.append(p)
            period = p - 1
            t = 1
            while period * p <= LIMIT:
                period *= p
                t += 1
            count = sum((LIMIT-j) // period for j in range(5))
            assert period * p > LIMIT
            assert count > 0
            print(f"p={p}: max v_p={t}, step={period}, maximizers={count}")
    assert regular == REGULAR
    allp = primes_below(BOUND)
    assert set(allp) == set(regular) | set(fail_extra_root) | set(fail_zero_slope)
    print(f"PASS: {len(allp)} primes 32<p<1000; "
          f"regular={len(regular)}, extra roots={len(fail_extra_root)}, "
          f"zero slopes={len(fail_zero_slope)} (failure types can overlap)")


if __name__ == '__main__':
    main()
