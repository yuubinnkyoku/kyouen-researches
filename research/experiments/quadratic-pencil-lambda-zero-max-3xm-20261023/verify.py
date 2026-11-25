#!/usr/bin/env python3
"""Exact audit of maximum safe sets for the 3-row lambda=0 quadratic pencil."""
from itertools import combinations

WITNESS = ((0, 1, 3), (2, 4, 6), (2, 5, 7))


def det(a):
    """Independent 4x4 integer determinant via fraction-free Bareiss elimination."""
    a = [list(row) for row in a]
    n = len(a)
    sign, denom = 1, 1
    for k in range(n - 1):
        if a[k][k] == 0:
            swap = next((i for i in range(k + 1, n) if a[i][k]), None)
            if swap is None:
                return 0
            a[k], a[swap] = a[swap], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                v = a[i][j] * pivot - a[i][k] * a[k][j]
                assert v % denom == 0
                a[i][j] = v // denom
            a[i][k] = 0
        denom = pivot
    return sign * a[-1][-1]


def forbidden_direct(q):
    return det([[x*x, x, y, 1] for x, y in q]) == 0


def forbidden_formula(q):
    rows = [[x for x, y in q if y == r] for r in range(3)]
    sizes = tuple(map(len, rows))
    if max(sizes) == 4:
        return True
    if sorted(sizes) == [0, 1, 3]:
        return False
    if sorted(sizes) == [0, 2, 2]:
        two = [row for row in rows if len(row) == 2]
        return sum(two[0]) == sum(two[1])
    assert sorted(sizes) == [1, 1, 2], sizes
    r = sizes.index(2)
    a, b = rows[r]
    if r == 0:
        c, d = rows[1][0], rows[2][0]
        return -a*b + 2*(a+b)*c-(a+b)*d-2*c*c+d*d == 0
    if r == 1:
        c, d = rows[0][0], rows[2][0]
        return -2*a*b+(a+b)*(c+d)-c*c-d*d == 0
    c, d = rows[0][0], rows[1][0]
    return -a*b-(a+b)*c+2*(a+b)*d+c*c-2*d*d == 0


def safe_triples(a, b, c):
    """Complete four-point test specialized to exactly three stones in each row."""
    pair_sums = lambda row: {u+v for u, v in combinations(row, 2)}
    sa, sb, sc = map(pair_sums, (a, b, c))
    if sa & sb or sa & sc or sb & sc:
        return False
    for u, v in combinations(a, 2):
        for x in b:
            for z in c:
                if -u*v+2*(u+v)*x-(u+v)*z-2*x*x+z*z == 0:
                    return False
    for u, v in combinations(b, 2):
        for x in a:
            for z in c:
                if -2*u*v+(u+v)*(x+z)-x*x-z*z == 0:
                    return False
    for u, v in combinations(c, 2):
        for x in a:
            for z in b:
                if -u*v-(u+v)*x+2*(u+v)*z+x*x-2*z*z == 0:
                    return False
    return True


def main():
    checked = 0
    for m in range(2, 6):
        points = [(x, y) for x in range(m) for y in range(3)]
        for q in combinations(points, 4):
            assert forbidden_direct(q) == forbidden_formula(q), (m, q)
            checked += 1
    assert checked == 2001
    print("independent determinant/formula comparison: 2001 quadruples agree")

    for m, expected in ((7, 0), (8, 68)):
        triples = list(combinations(range(m), 3))
        count = sum(safe_triples(a, b, c)
                    for a in triples for b in triples for c in triples)
        assert count == expected, (m, count)
        print(f"m={m}: checked {len(triples)**3} row-triple patterns; safe 9-sets={count}")

    points = [(x, y) for y, row in enumerate(WITNESS) for x in row]
    assert len(points) == 9
    assert all(not forbidden_direct(q) for q in combinations(points, 4))
    assert all(not forbidden_direct(q) for q in combinations(points[:-1], 4))
    print("m=8 9-point witness: 126/126 quadruples nonzero (Bareiss)")
    print("m=7 8-point witness: 70/70 quadruples nonzero (Bareiss)")


if __name__ == "__main__":
    main()
