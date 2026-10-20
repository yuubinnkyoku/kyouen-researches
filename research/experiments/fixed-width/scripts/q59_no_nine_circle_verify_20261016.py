#!/usr/bin/env python3
"""Independent finite audits for the 5-row q=9 theorem.

The proof itself is modular and covers every m.  The direct geometry audit
below uses integer determinants of triples, not the chord-square recurrence.
"""
from itertools import combinations
from math import gcd


def residue_audit():
    sq = {x*x % 9 for x in range(9)}
    triple = []
    quadruple = []
    quintuple = []
    for a in sq:
        for b in sq:
            x = [a, b]
            for _ in range(3):
                x.append((2*x[-1]-x[-2]-8) % 9)
            for length, out in ((3, triple), (4, quadruple), (5, quintuple)):
                if all(v in sq for v in x[:length]):
                    out.append(tuple(x[:length]))
    assert sorted(set(triple)) == [(0, 0, 1), (0, 4, 0), (1, 0, 0)]
    assert sorted(set(quadruple)) == [(1, 0, 0, 1)]
    assert not quintuple
    return len(triple), len(quadruple), len(quintuple)


def det3(a, b, c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
            -a[1]*(b[0]*c[2]-b[2]*c[0])
            +a[2]*(b[0]*c[1]-b[1]*c[0]))


def circle_from_triple(p, q, r):
    def t(z): return z[0]*z[0]+z[1]*z[1]
    x = [p[0], q[0], r[0]]
    y = [p[1], q[1], r[1]]
    z = [t(p), t(q), t(r)]
    one = [1, 1, 1]
    def d(a, b, c):
        return det3((a[0],b[0],c[0]), (a[1],b[1],c[1]), (a[2],b[2],c[2]))
    A = d(x,y,one)
    if A == 0:
        return None
    B, C, D = -d(z,y,one), -d(x,z,one), -d(x,y,z)
    if A < 0:
        A, B, C, D = -A, -B, -C, -D
    g = gcd(gcd(A,abs(B)), gcd(abs(C),abs(D)))
    return (A//g, B//g, C//g, D//g)


def direct_census(m):
    points = [(x,y) for y in range(5) for x in range(m)]
    circles = set()
    for p,q,r in combinations(points,3):
        c = circle_from_triple(p,q,r)
        if c is not None:
            circles.add(c)
    max_count = 0
    witness = None
    for A,B,C,D in circles:
        count = sum(A*(x*x+y*y)+B*x+C*y+D == 0 for x,y in points)
        if count > max_count:
            max_count = count
            witness = (A,B,C,D)
        assert count <= 8, (m,count,(A,B,C,D))
    return len(circles), max_count, witness


def main():
    print('mod9 triple/quadruple/quintuple patterns:', residue_audit())
    for m in (4, 5, 7, 9, 12, 14):
        n, maximum, witness = direct_census(m)
        print(f'm={m} circles={n} max_points={maximum} example={witness}')
        assert maximum == 8
    print('PASS: modular obstruction and independent finite determinant census')


if __name__ == '__main__':
    main()
