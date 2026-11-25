#!/usr/bin/env python3
"""Exact independent checks for identical-hub split graph extremal theorem."""
from fractions import Fraction
from functools import lru_cache
from itertools import permutations
from math import factorial

def allocations(m, L):
    if m == 1:
        yield (L,)
        return
    for x in range(L + 1):
        for rest in allocations(m - 1, L - x):
            yield (x,) + rest

def balanced_product(n, total):
    if n == 0:
        return 1 if total == 0 else None
    a, r = divmod(total, n)
    return (a + 1) ** (n - r) * (a + 2) ** r

def formula(t, d, c):
    W = d + sum(t[:d])
    p = Fraction(W, W + c)
    for x in t:
        p /= x + 1
    return p

def compressed_independent_recursion(t, d, c):
    """Independent-point-first Markov recursion; no priority formula used."""
    m = len(t)
    A = (1 << d) - 1
    @lru_cache(None)
    def f(S):
        if not S:
            return Fraction(1)
        remaining = [j for j in range(m) if S >> j & 1]
        alive_hubs = c if (S & A) == A else 0
        denom = len(remaining) + sum(t[j] for j in remaining) + alive_hubs
        return sum((f(S ^ (1 << j)) for j in remaining), Fraction()) / denom
    return f((1 << m) - 1)

def explicit_graph_recursion(t, d, c):
    """Fully labelled closed-neighborhood recursion."""
    m = len(t)
    nbr = [0] * (m + sum(t) + c)
    def edge(a, b):
        nbr[a] |= 1 << b
        nbr[b] |= 1 << a
    centers = list(range(m, len(nbr)))
    for i, a in enumerate(centers):
        for b in centers[i + 1:]:
            edge(a, b)
    pos = m
    for j, num in enumerate(t):
        for _ in range(num):
            edge(j, pos)
            pos += 1
    for h in range(pos, len(nbr)):
        for j in range(d):
            edge(j, h)
    @lru_cache(None)
    def f(S):
        if S == 0:
            return Fraction(1)
        n = S.bit_count()
        return sum((f(S & ~(nbr[v] | (1 << v))) if v < m else Fraction(0)
                    for v in range(len(nbr)) if S >> v & 1), Fraction()) / n
    return f((1 << len(nbr)) - 1)

def priority_permutations(t, d, c):
    """Direct greedy scan of all labelled priority orders."""
    m = len(t)
    n = m + sum(t) + c
    nbr = [0] * n
    centers = list(range(m, n))
    for i, a in enumerate(centers):
        for b in centers[i + 1:]:
            nbr[a] |= 1 << b
            nbr[b] |= 1 << a
    pos = m
    for j, num in enumerate(t):
        for _ in range(num):
            nbr[j] |= 1 << pos
            nbr[pos] |= 1 << j
            pos += 1
    for h in range(pos, n):
        for j in range(d):
            nbr[j] |= 1 << h
            nbr[h] |= 1 << j
    good = 0
    for order in permutations(range(n)):
        chosen = 0
        for v in order:
            if not chosen & (nbr[v] | (1 << v)):
                chosen |= 1 << v
        if chosen == (1 << m) - 1:
            good += 1
    return Fraction(good, factorial(n))

def predicted_min(m, d, L, c):
    vals = []
    for T in range(L + 1):
        inside = balanced_product(d, T)
        outside = balanced_product(m - d, L - T)
        if outside is not None:
            vals.append((T, Fraction(d + T, (d + T + c) * inside * outside)))
    low = min(v for _, v in vals)
    return low, [T for T, v in vals if v == low]

def main():
    total = small = orders = extrema = 0
    for m in range(1, 6):
        for d in range(1, m + 1):
            for L in range(0, 7):
                tt = list(allocations(m, L))
                for c in range(1, 9):
                    vals = []
                    for t in tt:
                        p = formula(t, d, c)
                        assert p == compressed_independent_recursion(t, d, c), (m,d,L,c,t)
                        total += 1
                        if m + L + c <= 9 and m <= 3 and L <= 3 and c <= 2:
                            assert p == explicit_graph_recursion(t, d, c)
                            small += 1
                        if m + L + c <= 7 and m <= 3 and L <= 2 and c <= 2:
                            assert p == priority_permutations(t, d, c)
                            orders += 1
                        vals.append(p)
                    low, Ts = predicted_min(m, d, L, c)
                    high = Fraction(d + L, (d + L + c) * (L + 1))
                    assert min(vals) == low, (m,d,L,c,'min')
                    assert max(vals) == high, (m,d,L,c,'max')
                    extrema += 1
    for c in range(1, 21):
        _, Ts = predicted_min(3, 2, 5, c)
        expected = [3] if c < 5 else [2,3] if c == 5 else [2]
        assert Ts == expected, (c,Ts)
    print(f'PASS: {total} allocation cases; {small} labelled graph recursions; '
          f'{orders} full priority permutations; {extrema} sharp-bound classes; '
          'phase transition c=5 checked for c=1..20.')

if __name__ == '__main__':
    main()
