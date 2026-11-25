#!/usr/bin/env python3
"""Check constant-weight counts using midpoint enumeration and the formula."""
from itertools import combinations
from math import comb, factorial
import json


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def formula(d, k):
    count = 0
    for u in range(2, d + 1, 2):
        for v in range(2, d - u + 1, 2):
            count += (factorial(d) // (factorial(u) * factorial(v) * factorial(d-u-v))
                      * comb(u, u//2) * comb(v, v//2)
                      * choose(d-u-v, k-(u+v)//2))
    assert count % 8 == 0
    return count // 8


def midpoint(a, b, c, e, d):
    def sums(x, y):
        return tuple(((x >> i) & 1) + ((y >> i) & 1) for i in range(d))
    return (sums(a,b) == sums(c,e) or sums(a,c) == sums(b,e)
            or sums(a,e) == sums(b,c))


def main():
    results = []
    for d in range(2, 8):
        values = []
        for k in range(d+1):
            layer = [v for v in range(1 << d) if v.bit_count() == k]
            actual = sum(midpoint(*vertices, d) for vertices in combinations(layer, 4))
            assert actual == formula(d, k)
            values.append(actual)
        results.append({'dimension': d, 'counts_by_weight': values})
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
