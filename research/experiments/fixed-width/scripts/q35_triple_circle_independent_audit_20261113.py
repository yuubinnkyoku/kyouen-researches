#!/usr/bin/env python3
"""Independent exact triple-generated circle audit for 3 x m, q=5.

Uses only integer determinants; no Pell-family or chord parameterization.
"""
from itertools import combinations
from math import gcd
from functools import reduce
import sys


def exact_five_circles(m):
    points = [(x, y) for x in range(m) for y in range(3)]
    circles = set()
    for (x1, y1), (x2, y2), (x3, y3) in combinations(points, 3):
        A, B = 2 * (x2 - x1), 2 * (y2 - y1)
        C = x2*x2 + y2*y2 - x1*x1 - y1*y1
        D, E = 2 * (x3 - x1), 2 * (y3 - y1)
        F = x3*x3 + y3*y3 - x1*x1 - y1*y1
        det = A*E - B*D
        if not det:
            continue
        u = -2 * (C*E - B*F)
        v = -2 * (A*F - C*D)
        w = -(det*(x1*x1 + y1*y1) + u*x1 + v*y1)
        coeff = (det, u, v, w)
        g = reduce(gcd, coeff)
        coeff = tuple(z // g for z in coeff)
        if coeff[0] < 0:
            coeff = tuple(-z for z in coeff)
        circles.add(coeff)
    return sum(
        sum(a*(x*x+y*y) + b*x + c*y + d == 0 for x, y in points) == 5
        for a, b, c, d in circles
    )


def main():
    upper = int(sys.argv[1]) if len(sys.argv) > 1 else 22
    counts = [0] + [exact_five_circles(m) for m in range(1, upper + 1)]
    for m in range(1, upper + 1):
        second = counts[m] - 2*counts[m-1] + counts[m-2] if m >= 2 else 0
        print(f"{m},{counts[m]},{second}")
    assert counts[9] == 6 and counts[10] == 8
    if upper >= 22:
        assert counts[22] == 64
        assert counts[18] == 36
        assert counts[19] == 46


if __name__ == "__main__":
    main()
