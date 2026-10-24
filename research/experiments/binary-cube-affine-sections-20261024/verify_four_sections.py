#!/usr/bin/env python3
"""Independent integer-rank census of 4-point real 3-flat sections of {0,1}^d.

Run: python verify_four_sections.py --max-d 5
No floating-point ranks and no third-party packages.
"""
import argparse
from collections import Counter
from itertools import combinations
from math import comb, factorial
import json


def stirling(n, k):
    return sum((-1)**j * comb(k, j) * (k-j)**n for j in range(k+1)) // factorial(k)


def expected(d):
    h8 = 2**(d-3) * stirling(d+1, 4)
    h6 = 5 * (10**d - 4*8**d + 6*6**d - 4*4**d + 2**d) // 48
    h5 = 15 * 2**d * stirling(d+1, 6)
    h4 = (16**d - 12*12**d + 30*10**d - 35*8**d + 24*6**d - 10*4**d + 2*2**d) // 24
    dep4 = (6**d - 2*4**d + 2**d) // 8
    return {"dependent_four_sets": dep4, "H4": h4, "H5": h5, "H6": h6, "H8": h8}


def det3(a, b, c):
    return a[0]*(b[1]*c[2]-b[2]*c[1])-b[0]*(a[1]*c[2]-a[2]*c[1])+c[0]*(a[1]*b[2]-a[2]*b[1])


def census(d):
    points = [tuple((x >> j) & 1 for j in range(d)) for x in range(1 << d)]
    generators = Counter()
    dependent = 0
    for a,b,c,e in combinations(range(1 << d), 4):
        pa,pb,pc,pe = (points[x] for x in (a,b,c,e))
        v = [tuple(p[j]-pa[j] for j in range(d)) for p in (pb,pc,pe)]
        pivot = None
        for ijk in combinations(range(d), 3):
            rows = [tuple(v[col][j] for col in range(3)) for j in ijk]
            dt = det3(*rows)
            if dt:
                pivot = (ijk, rows, dt)
                break
        if pivot is None:
            dependent += 1
            continue
        ijk, rows, dt = pivot
        lambdas = {}
        for proj in range(8):
            rhs = tuple(((proj >> t)&1) - pa[j] for t,j in enumerate(ijk))
            lam = []
            for col in range(3):
                changed = [tuple(rhs[row] if k==col else rows[row][k] for k in range(3)) for row in range(3)]
                lam.append(det3(*changed))
            lambdas[proj] = tuple(lam)
        n = 0
        for p in points:
            proj = sum(p[j] << t for t,j in enumerate(ijk))
            lam = lambdas[proj]
            if all(dt*(p[j]-pa[j]) == sum(lam[k]*v[k][j] for k in range(3)) for j in range(d)):
                n += 1
        generators[n] += 1
    assert all(n in (4,5,6,8) for n in generators), generators
    mult = {4:1, 5:4, 6:12, 8:58}
    assert all(generators[n] % mult[n] == 0 for n in generators)
    result = {"dependent_four_sets": dependent, **{f"H{n}":generators[n]//mult[n] for n in (4,5,6,8)}}
    assert dependent + sum(generators.values()) == comb(1 << d, 4)
    assert result == expected(d), (d, result, expected(d))
    return result


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--max-d', type=int, default=5)
    args=ap.parse_args()
    for d in range(3, args.max_d+1):
        print(json.dumps({"d":d, **census(d)}, sort_keys=True))


if __name__ == '__main__':
    main()
