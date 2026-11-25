#!/usr/bin/env python3
"""Exact finite certificates for the q=5 section 37/47-adic theorem."""
from math import comb, factorial

C = {32: 1, 24: -30, 20: 140, 18: 135, 16: -1215,
     14: 2205, 12: -1977, 10: 780, 8: 250,
     6: -495, 4: 255, 2: -49}
PRIMES = (37, 47)
LIMIT = 10**18


def exp_exact(d):
    n = sum(c * a**d for a, c in C.items())
    assert n % 120 == 0
    return n // 120


def exp_mod(d, p, t):
    m = p**t
    return sum(c * pow(a, d, m) for a, c in C.items()) * pow(120, -1, m) % m


def stirling_values(max_d):
    # Identity a**d = sum_k comb(a,k) k! S(d,k).
    g = [sum(c * comb(a, k) for a, c in C.items() if a >= k)
         for k in range(33)]
    row = [1] + [0] * 32
    out = []
    for d in range(max_d + 1):
        n = sum(g[k] * factorial(k) * row[k] for k in range(33))
        assert n % 120 == 0
        out.append(n // 120)
        row = [0] + [row[k - 1] + k * row[k] for k in range(1, 33)]
    return out


def valuation(n, p):
    assert n > 0
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def predicted(d, p):
    k, j = divmod(d, p - 1)
    return 1 + valuation(k, p) if j < 5 else 0


def verify():
    exact = stirling_values(2 * max(PRIMES) - 3)
    assert all(exact[d] == exp_exact(d) for d in range(len(exact)))
    assert exact[:5] == [0] * 5
    for p in PRIMES:
        assert p > 32 and 120 % p != 0
        roots = [j for j in range(p - 1) if exp_mod(j, p, 1) == 0]
        assert roots == list(range(5))
        slopes = []
        for j in range(p - 1):
            delta = (exp_mod(j + p - 1, p, 2) - exp_mod(j, p, 2)) % p**2
            assert delta % p == 0
            slope = delta // p
            assert (exact[j + p - 1] - exact[j]) // p % p == slope
            assert slope != 0, (p, j)
            slopes.append(slope)
        for d in range(5, 300):
            for t in range(1, 5):
                period = (p - 1) * p**(t - 1)
                assert exp_mod(d + period, p, t) == exp_mod(d, p, t)
                delta = (exp_mod(d + period, p, t + 1)
                         - exp_mod(d, p, t + 1)) % p**(t + 1)
                assert delta == p**t * slopes[d % (p-1)] % p**(t + 1)
            v = predicted(d, p)
            assert exp_mod(d, p, v + 1) % p**v == 0
            assert exp_mod(d, p, v + 1) != 0
        k = 0
        while (p-1) * p**(k+1) <= LIMIT:
            k += 1
        step = (p-1) * p**k
        winners = [(u, j) for u in range(1, LIMIT // step + 1)
                   for j in range(5) if step*u + j <= LIMIT]
        assert winners and step*p > LIMIT
        assert all(u % p != 0 and predicted(step*u+j, p) == k+1
                   for u,j in winners)
        print(f"p={p}: root residues={roots}; slopes={slopes}")
        print(f"p={p}: max valuation={k+1}; step={step}; "
              f"u=1..{max(u for u,_ in winners)}; count={len(winners)}")
    print("PASS: two exact integer methods, complete residue checks, regressions")


if __name__ == "__main__":
    verify()
