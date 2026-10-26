#!/usr/bin/env python3
"""Exact six-branch p-adic certificates for q=5 and p=41,43,53."""
from math import comb, factorial

COEFF = {32: 1, 24: -30, 20: 140, 18: 135, 16: -1215,
         14: 2205, 12: -1977, 10: 780, 8: 250,
         6: -495, 4: 255, 2: -49}
PRIMES = {41: 19, 43: 8, 53: 27}
LIMIT = 10**18
EXPECTED = {41: (11, 7), 43: (11, 6), 53: (10, 31)}


def exp_mod(d, mod):
    return (sum(c * pow(a, d, mod) for a, c in COEFF.items())
            * pow(120, -1, mod)) % mod


def stirling_values(end, mod):
    """Independent arithmetic route via Stirling numbers of the second kind."""
    g = [sum(c * comb(a, k) for a, c in COEFF.items() if a >= k)
         for k in range(33)]
    weights = [g[k] * factorial(k) % mod for k in range(33)]
    row = [1] + [0] * 32
    inv = pow(120, -1, mod)
    for _ in range(end + 1):
        yield sum(weights[k] * row[k] for k in range(33)) * inv % mod
        row = [0] + [(row[k-1] + k * row[k]) % mod
                     for k in range(1, 33)]


def binomial_mod(j, k, p, t):
    """For d=j+(p-1)k, expand (a^(p-1))^k in powers of p."""
    mod = p**t
    total = 0
    for a, c in COEFF.items():
        b = (pow(a, p-1) - 1) // p
        value = sum(comb(k, h) * (p*b)**h
                    for h in range(min(k, t-1) + 1))
        total += c * pow(a, j, mod) * (value % mod)
    return total * pow(120, -1, mod) % mod


def lift(p, j, slope, max_t):
    k = 0
    roots = {1: k}
    for t in range(1, max_t):
        mod = p**(t+1)
        base = exp_mod(j+(p-1)*k, mod)
        assert base % p**t == 0
        digit = -(base//p**t) * pow(slope, -1, p) % p
        k += p**(t-1)*digit
        assert exp_mod(j+(p-1)*k, mod) == 0
        assert binomial_mod(j, k, p, t+1) == 0
        roots[t+1] = k
    return roots


def count_roots(p, root_lifts, t):
    step = (p-1)*p**(t-1)
    progressions = []
    for j, lifts in root_lifts.items():
        first = j+(p-1)*lifts[t]
        if first < 5:
            first += step
        if first <= LIMIT:
            count = 1+(LIMIT-first)//step
            progressions.append((j, first, count))
    return progressions


def main():
    for p, extra in PRIMES.items():
        mod = p*p
        vals = list(stirling_values(2*p-3, mod))
        assert all(v == exp_mod(d, mod) for d, v in enumerate(vals))
        roots = [j for j in range(p-1) if vals[j] % p == 0]
        assert roots == [0, 1, 2, 3, 4, extra], (p, roots)
        slopes = {j: ((vals[j+p-1]-vals[j]) % mod)//p
                  for j in range(p-1)}
        assert all(slopes[j] != 0 for j in roots)
        zeros = [j for j in slopes if slopes[j] == 0]
        assert zeros == {41: [], 43: [12], 53: []}[p], (p, zeros)
        assert all({(j+h)%(p-1) for j in roots} != set(roots)
                   for h in range(1, p-1))
        root_lifts = {j: lift(p, j, slopes[j], 13) for j in roots}
        assert all(all(v == 0 for v in root_lifts[j].values())
                   for j in range(5))
        for t in range(1, 4):
            for j in range(p-1):
                for k in range(p**(t-1)):
                    if t == 3 and p > 43 and j not in roots:
                        continue  # Eliminated by reduction modulo p.
                    d = j+(p-1)*k
                    expected = j in roots and k == root_lifts[j][t]
                    assert (exp_mod(d, p**t) == 0) == expected
        counts = {t: count_roots(p, root_lifts, t)
                  for t in range(1, 14)}
        max_t = max(t for t, rows in counts.items() if rows)
        total = sum(c for _, _, c in counts[max_t])
        assert (max_t, total) == EXPECTED[p], (p, max_t, total)
        assert not counts[max_t+1]
        print(f'p={p}: roots={roots}; slopes={[slopes[j] for j in roots]}; '
              f'zero slopes={zeros}')
        print(f'  extra branch k_t (t=2..5)='
              f'{[root_lifts[extra][t] for t in range(2, 6)]}')
        print(f'  maximum={max_t}; count={total}; '
              f'progressions={counts[max_t]}')
    print('PASS: exact finite certificates and two arithmetic routes')


if __name__ == '__main__':
    main()
