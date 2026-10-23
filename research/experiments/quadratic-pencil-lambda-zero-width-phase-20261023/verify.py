#!/usr/bin/env python3
"""Exact audits for lambda=0 width phase transition (not the unbounded proof)."""
from itertools import combinations, permutations


def determinant(points, lam=0):
    a = [(x*x + lam*y*y, x, y, 1) for x, y in points]
    total = 0
    for p in permutations(range(4)):
        sign = (-1) ** sum(p[i] > p[j] for i in range(4) for j in range(i+1, 4))
        prod = 1
        for i in range(4):
            prod *= a[i][p[i]]
        total += sign * prod
    return total


def det_difference(points, lam=0):
    x0, y0 = points[0]
    a = [[x*x + lam*y*y - x0*x0 - lam*y0*y0, x-x0, y-y0]
         for x, y in points[1:]]
    return -(a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
             - a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
             + a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))


def maximal(w, m, selected, lam=0):
    s = set(selected)
    assert len(s) == len(selected)
    for four in combinations(selected, 4):
        assert determinant(four, lam) == det_difference(four, lam) != 0, four
    for y in range(w):
        for x in range(m):
            p = (x, y)
            if p in s:
                continue
            assert any(determinant((*three, p), lam) ==
                       det_difference((*three, p), lam) == 0
                       for three in combinations(selected, 3)), (w, m, p)


def main():
    for w in (3, 4, 6):
        for m in (1, 2, 3, 8, 23, 40):
            maximal(w, m, ((0, 0), (0, 1), (0, 2)))
    print('vertical triple: 18 finite boards checked')

    five = ((0, 0), (2, 0), (1, 1), (2, 1), (5, 1))
    for lam in (-7, 0, 1, 9):
        maximal(2, 8, five, lam)
    print('2x8 five-stone maximal: four lambda values checked')

    four = ((0, 0), (0, 1), (1, 0), (2, 0))
    assert determinant(four) == det_difference(four) != 0
    print('safe four-point configuration: two determinants agree')

    for m in range(2, 8):
        pts = [(x, y) for y in range(2) for x in range(m)]
        for q in combinations(pts, 4):
            rows = [[x for x, y in q if y == r] for r in (0, 1)]
            forbidden = (max(map(len, rows)) == 4 or
                         (len(rows[0]) == len(rows[1]) == 2 and
                          sum(rows[0]) == sum(rows[1])))
            assert (determinant(q) == 0) == forbidden
            assert determinant(q) == det_difference(q)
    print('2-row pair-sum criterion: m=2..7 exhaustive audit passed')


if __name__ == '__main__':
    main()
