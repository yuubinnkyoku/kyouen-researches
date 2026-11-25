#!/usr/bin/env python3
"""Exact finite-bound 5-adic extrema for five-point binary-cube sections.

Uses K0567's proved all-t lifting theorem and K0561's exponential formula.
No hyperplane census is performed.
"""
from math import comb, factorial

COEFF = {
    32: 1, 24: -30, 20: 140, 18: 135, 16: -1215, 14: 2205,
    12: -1977, 10: 780, 8: 250, 6: -495, 4: 255, 2: -49,
}


def residue_composite(d, t):
    assert d >= 5 and t >= 1
    m = 120 * 5**t
    n = sum(c * pow(a, d, m) for a, c in COEFF.items()) % m
    assert n % 120 == 0
    return n // 120


def residue_five_adic(d, t):
    assert d >= 5 and t >= 1
    m = 5**t
    n = sum(c * pow(a, d, 5*m) for a, c in COEFF.items()) % (5*m)
    assert n % 5 == 0
    return (n // 5 * pow(24, -1, m)) % m


def direct_small(d):
    assert d >= 5
    n = sum(c * a**d for a, c in COEFF.items())
    assert n % 120 == 0
    return n // 120


def direct_stirling(d):
    """Stirling recurrence and binomial inversion of K0561 coefficients."""
    assert d >= 5
    g = [sum(comb(a, k)*c for a, c in COEFF.items() if a >= k)
         for k in range(33)]
    assert g[:5] == [0]*5
    row = [1] + [0]*32
    for _ in range(d):
        row = [0] + [row[k-1] + k*row[k] for k in range(1, 33)]
    n = sum(g[k]*factorial(k)*row[k] for k in range(33))
    assert n % 120 == 0
    return n // 120


def roots_through(max_t):
    roots = (1, 2, 3, 4)
    out = {}
    for t in range(1, max_t+1):
        period = 4*5**t
        assert len(roots) == len(set(roots)) == 4
        for r in roots:
            d = r if r >= max(5, t) else r + (
                (max(5, t)-r+period-1)//period)*period
            assert residue_composite(d, t) == residue_five_adic(d, t) == 0
        out[t] = (period, roots)
        if t == max_t:
            break
        children = []
        for r in roots:
            good = []
            for j in range(5):
                candidate = r + j*period
                new_period = 5*period
                d = candidate if candidate >= max(5, t+1) else candidate + (
                    (max(5, t+1)-candidate+new_period-1)//new_period)*new_period
                a = residue_composite(d, t+1)
                b = residue_five_adic(d, t+1)
                assert a == b, (t, candidate, a, b)
                if a == 0:
                    good.append(candidate)
            assert len(good) == 1, (t, r, good)
            children.extend(good)
        roots = tuple(sorted(children))
    return out


def hits(bound, period, roots):
    count, values = 0, []
    for r in roots:
        first = r if r >= 5 else r + ((5-r+period-1)//period)*period
        if first > bound:
            continue
        c = 1 + (bound-first)//period
        count += c
        if c <= 20:
            values.extend(first+i*period for i in range(c))
    return count, sorted(values)


def verify():
    table = roots_through(32)
    expected = {
        1: (1, 2, 3, 4),
        2: (2, 3, 4, 61),
        3: (3, 4, 202, 261),
        4: (3, 4, 202, 1761),
        5: (2504, 6761, 10003, 10202),
        25: (805442412107522702, 973649720776606761,
             1107905929047210003, 1114261673894590004),
        26: (973649720776606761, 1114261673894590004,
             4381721098630960202, 4684184615570647503),
        27: (10644649093109710003, 18995655106511777504,
             22263114531248147702, 24815507630932856761),
    }
    for t, roots in expected.items():
        assert table[t][1] == roots, t
    for d in range(5, 65):
        assert direct_stirling(d) == direct_small(d)
        for t in (1, 3, 6, 15, 32):
            assert direct_small(d) % 5**t == residue_composite(d, t)
            assert residue_composite(d, t) == residue_five_adic(d, t)
    targets = [
        (10**5, 8, [44261]),
        (10**6, 9, [335003]),
        (10**12, 17, [809636777504]),
        (10**18, 26, [973649720776606761]),
    ]
    for bound, t, expected_hits in targets:
        count, values = hits(bound, *table[t])
        assert count == len(expected_hits) and values == expected_hits
        assert hits(bound, *table[t+1])[0] == 0
        # Do not apply an eventual-period theorem before its onset.
        for d in range(5, max(5, t+1)):
            assert direct_small(d) % 5**(t+1) != 0
        for d in values:
            assert residue_composite(d, t) == 0
            assert residue_five_adic(d, t+1) != 0
        print(f'5<=d<={bound}: max v5(E_d5)={t}, attained at {values}')
    print('All four branches checked through t=32 by two modular routes.')
    print('Small d=5..64 independently checked by Stirling recurrence.')


if __name__ == '__main__':
    verify()
