#!/usr/bin/env python3
"""Exact degree-bound audit and independent priority-permutation check."""
from fractions import Fraction
from itertools import product, permutations
from math import factorial, prod

def no_center_probability(ns):
    k = len(ns)
    union = [0] * (1 << k)
    h = [Fraction(0)] * (1 << k)
    h[0] = Fraction(1)
    for s in range(1, 1 << k):
        bit = s & -s
        union[s] = union[s ^ bit] | ns[bit.bit_length() - 1]
        h[s] = sum((h[s ^ (1 << c)] for c in range(k) if s >> c & 1),
                   Fraction(0)) / (s.bit_count() + union[s].bit_count())
    return sum(((-1 if s.bit_count() % 2 else 1) * h[s]
                for s in range(1 << k)), Fraction(0))

def bounds(ns):
    ds = [n.bit_count() for n in ns]
    if 0 in ds:
        return Fraction(0), Fraction(0)
    lo = prod((Fraction(d, d + 1) for d in ds), start=Fraction(1))
    hi = 1 / (1 + sum((Fraction(1, d) for d in ds), Fraction(0)))
    return lo, hi

def no_center_by_permutations(ns, m):
    k = len(ns)
    count = 0
    for order in permutations(range(k + m)):
        chosen = []
        for v in order:
            if v < k:
                blocked = any(u < k or (u >= k and ns[v] & (1 << (u-k)))
                              for u in chosen)
            else:
                blocked = any(u < k and (ns[u] & (1 << (v-k)))
                              for u in chosen)
            if not blocked:
                chosen.append(v)
        count += all(v >= k for v in chosen)
    return Fraction(count, factorial(k + m))

def main():
    total = 0
    for k, m in [(1, 0), (1, 5), (2, 5), (3, 4), (4, 3)]:
        for ns in product(range(1 << m), repeat=k):
            p = no_center_probability(ns)
            lo, hi = bounds(ns)
            assert lo <= p <= hi, (k, m, ns, lo, p, hi)
            total += 1
        print("bounds:", k, m, (1 << m) ** k, "passed")
    print("total bounds:", total)
    independent = 0
    for k, m in [(1, 3), (2, 4), (3, 3)]:
        for ns in product(range(1 << m), repeat=k):
            assert no_center_probability(ns) == no_center_by_permutations(ns, m)
            independent += 1
    print("independent permutations:", independent, "passed")
    for k, d in [(2, 2), (3, 2), (4, 3)]:
        identical = [(1 << d) - 1] * k
        disjoint = [((1 << d) - 1) << (i * d) for i in range(k)]
        assert no_center_probability(identical) == Fraction(d, d + k)
        assert no_center_probability(disjoint) == Fraction(d, d + 1) ** k
        print("sharp:", k, d, no_center_probability(disjoint),
              no_center_probability(identical))

if __name__ == "__main__":
    main()
