#!/usr/bin/env python3
"""Exact arithmetic audit for the 5-adic q=5 binary-cube section theorem.

All large-dimensional checks are congruences derived from the proved
K0561 exponential formula; they are not a hyperplane census.
"""
from math import comb, factorial

# 120 E_{d,5} = sum COEFF[a] a**d for d>=5 (K0561).
COEFF = {
    32: 1, 24: -30, 20: 140, 18: 135, 16: -1215, 14: 2205,
    12: -1977, 10: 780, 8: 250, 6: -495, 4: 255, 2: -49,
}


def residue_composite(d: int, t: int) -> int:
    """Divide the whole numerator by 120 before reducing modulo 5**t."""
    assert d >= 5 and t >= 1
    mod = 120 * 5**t
    n = sum(c * pow(a, d, mod) for a, c in COEFF.items()) % mod
    assert n % 120 == 0
    return n // 120


def residue_five_adic(d: int, t: int) -> int:
    """Different modulus and division: divide by 5, invert 24."""
    assert d >= 5 and t >= 1
    mod = 5**t
    n = sum(c * pow(a, d, 5 * mod) for a, c in COEFF.items()) % (5 * mod)
    assert n % 5 == 0
    return (n // 5 * pow(24, -1, mod)) % mod


def exact_stirling(d: int) -> int:
    """Reconstruct support counts by binomial inversion, then use Stirling DP."""
    assert d >= 5
    g = [sum(comb(a, k) * c for a, c in COEFF.items() if a >= k)
         for k in range(33)]
    assert g[:5] == [0] * 5
    assert g[5:9] == [2592, 36304, 329552, 2038600]
    row = [1] + [0] * 32
    for _ in range(d):
        row = [0] + [row[k - 1] + k * row[k] for k in range(1, 33)]
    numerator = sum(g[k] * factorial(k) * row[k] for k in range(33))
    assert numerator % 120 == 0
    return numerator // 120


def lift_roots(max_t: int = 12):
    """One root per class modulo 20; five candidate lifts at each level."""
    roots = (1, 2, 3, 4)
    table = {}
    for t in range(1, max_t + 1):
        period = 4 * 5**t
        assert len(roots) == len(set(roots)) == 4
        for r in roots:
            d = r
            if d < max(5, t):
                d += ((max(5, t) - d + period - 1) // period) * period
            assert residue_composite(d, t) == 0
            assert residue_five_adic(d, t) == 0
        table[t] = (period, roots)
        if t == max_t:
            break
        children = []
        for r in roots:
            good = []
            for j in range(5):
                candidate = r + j * period
                d = candidate
                if d < max(5, t + 1):
                    d += ((max(5, t + 1) - d + 5*period - 1)//(5*period))*(5*period)
                a = residue_composite(d, t + 1)
                b = residue_five_adic(d, t + 1)
                assert a == b
                if a == 0:
                    good.append(candidate)
            assert len(good) == 1, (t, r, good)
            children.extend(good)
        roots = tuple(sorted(children))
    return table


def verify():
    assert [(d % 20, residue_composite(d, 1)) for d in range(20, 40)] == [
        (r, v) for r, v in enumerate(
            [4, 0, 0, 0, 0, 2, 4, 3, 1, 4, 3, 1, 2, 1, 2, 4, 3, 3, 1, 2])]
    # 20 is the least period modulo 5: neither maximal proper divisor works.
    for p in (4, 10):
        assert any(residue_composite(d, 1) != residue_composite(d+p, 1)
                   for d in range(20, 40))

    # Independent arithmetic via Stirling support counts for small dimensions.
    for d in range(5, 37):
        exact = exact_stirling(d)
        assert exact == sum(c * a**d for a, c in COEFF.items()) // 120
        for t in (1, 2, 3, 6):
            assert exact % 5**t == residue_composite(d, t)
            assert exact % 5**t == residue_five_adic(d, t)

    # The all-t mathematical congruence is proved in README; these are regressions.
    for t in range(13):
        p = 4 * 5**t
        mod = 5**(t+1)
        for d in range(max(5, t+1), max(5, t+1) + 60):
            a = residue_composite(d+p, t+1)
            b = residue_five_adic(d, t+1)
            assert (a-b) % mod == (pow(2, d, 5)*5**t) % mod, (t,d)
            assert a == residue_five_adic(d+p, t+1)

    table = lift_roots(12)
    expected = {
        1: (1, 2, 3, 4),
        2: (2, 3, 4, 61),
        3: (3, 4, 202, 261),
        4: (3, 4, 202, 1761),
        5: (2504, 6761, 10003, 10202),
    }
    for t, roots in expected.items():
        assert table[t][1] == roots, (t, table[t])
    for t in range(1, 6):
        p, roots = table[t]
        # Complete finite check of all residues in one period.
        observed = tuple(d % p for d in range(max(5,t), max(5,t)+p)
                         if residue_composite(d, t) == 0)
        assert tuple(sorted(observed)) == roots
    print('q=5: exact 5-adic increment checked t=0..12 (60 d each)')
    print('q=5: four unique 5-adic root branches checked through t=12')
    for t in range(1, 6):
        print('5^%d: period=%d, roots=%s' % (t, *table[t]))
    print('Stirling support-count and two modular divisions agree, d=5..36')


if __name__ == '__main__':
    verify()
