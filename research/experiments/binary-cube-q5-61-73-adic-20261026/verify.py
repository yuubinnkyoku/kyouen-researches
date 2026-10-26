#!/usr/bin/env python3
"""Exact p=61,73 congruence certificates for binary-cube 5-point sections.

All unbounded claims require K0561's proved exponential identity and the
p-adic lifting lemma in README.md. This script verifies finite hypotheses.
"""
from math import comb, factorial

COEFF = {32: 1, 24: -30, 20: 140, 18: 135, 16: -1215,
         14: 2205, 12: -1977, 10: 780, 8: 250,
         6: -495, 4: 255, 2: -49}
LIMIT = 10**18
DATA = {
    61: {"roots": [0, 1, 2, 3, 4, 13, 20, 23, 29],
         "singular": 13, "dead_unit": 28,
         "slope": {0: 43, 1: 40, 2: 29, 3: 1, 4: 53,
                   13: 0, 20: 32, 23: 13, 29: 2},
         "max_t": 10, "max_count": 9},
    73: {"roots": [0, 1, 2, 3, 4, 59],
         "singular": 59, "dead_unit": 13,
         "slope": {0: 48, 1: 8, 2: 6, 3: 43, 4: 41, 59: 0},
         "max_t": 9, "max_count": 85},
}

def exponential(d, mod):
    return sum(c * pow(a, d, mod) for a, c in COEFF.items()) * pow(120, -1, mod) % mod

def stirling_values(end, mod):
    """Second-kind Stirling recurrence, independent modular arithmetic path."""
    weights = [factorial(k) * sum(c * comb(a, k) for a, c in COEFF.items() if a >= k)
               % mod for k in range(33)]
    row = [1] + [0] * 32
    inv = pow(120, -1, mod)
    for _ in range(end + 1):
        yield sum(w * s for w, s in zip(weights, row)) * inv % mod
        row = [0] + [(row[k-1] + k*row[k]) % mod for k in range(1, 33)]

def lift(p, j, slope, last_t):
    """Unique simple zero k mod p^(t-1), t=1,...,last_t."""
    P = p-1
    k = 0
    out = {1: 0}
    for t in range(1, last_t):
        modulus = p**(t+1)
        f = exponential(j+P*k, modulus)
        assert f % p**t == 0
        digit = (- (f // p**t) * pow(slope, -1, p)) % p
        k += p**(t-1)*digit
        assert exponential(j+P*k, modulus) == 0
        out[t+1] = k
    return out

def progression(p, j, k, t):
    period = (p-1)*p**(t-1)
    start = j+(p-1)*k
    if start < 5:
        start += period
    if start > LIMIT:
        return None
    return (j, start, period, 1+(LIMIT-start)//period)

def main():
    for p, expected in DATA.items():
        P = p-1
        values = list(stirling_values(2*P+4, p**3))
        assert all(exponential(d, p**3) == v for d, v in enumerate(values))
        assert values[:5] == [0]*5
        roots = [j for j in range(P) if values[j] % p == 0]
        assert roots == expected['roots']
        slopes = {j: ((values[j+P]-values[j]) % p**2)//p for j in roots}
        assert slopes == expected['slope']
        dead = expected['singular']
        assert [j for j in roots if slopes[j] == 0] == [dead]
        assert values[dead] % p**2 == p*expected['dead_unit']
        simple = {j: lift(p, j, slopes[j], 13) for j in roots if j != dead}
        for j in range(P):
            for k in range(p):
                predicted = (j in simple and k == simple[j][2])
                assert (exponential(j+P*k, p**2) == 0) == predicted
        assert all(all(k == 0 for k in simple[j].values()) for j in range(5))
        assert all({(j+h) % P for j in roots} != set(roots) for h in range(1, P))
        def rows(t):
            return [r for j in simple if (r := progression(p, j, simple[j][t], t))]
        max_t = max(t for t in range(2, 14) if rows(t))
        assert max_t == expected['max_t']
        assert not rows(max_t+1)
        maximizers = rows(max_t)
        assert sum(r[3] for r in maximizers) == expected['max_count']
        assert all(exponential(dead+P*k, p**2) == p*expected['dead_unit']
                   for k in range(p))
        print('p', p, 'mod-p roots', roots, 'singular', dead)
        print('slopes', slopes, 'simple roots k mod p',
              {j: simple[j][2] for j in simple})
        print('maximum v_p for 5<=d<=10^18:', max_t)
        print('maximizers (j, first, period, count):', maximizers)
        print('total maximizers:', sum(r[3] for r in maximizers))
    print('PASS: exact finite hypotheses, two arithmetic methods, lifts to 13')

if __name__ == '__main__':
    main()
