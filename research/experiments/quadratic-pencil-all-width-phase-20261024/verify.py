#!/usr/bin/env python3
"""Finite independent check of the all-width quadratic-pencil phase theorem.

The theorem is algebraic; this script checks all 3-stone configurations on
small rectangles by directly testing every possible fourth stone.
"""
from fractions import Fraction
from itertools import combinations
from math import comb, gcd, isqrt
import json


def det3(a, b, c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
            - a[1]*(b[0]*c[2]-b[2]*c[0])
            + a[2]*(b[0]*c[1]-b[1]*c[0]))


def forbidden(triple, point, lam):
    p, q = lam.numerator, lam.denominator
    x0, y0 = triple[0]

    def row(t):
        x, y = t
        return (q*(x*x-x0*x0)+p*(y*y-y0*y0),
                q*(x-x0), q*(y-y0))

    return det3(row(triple[1]), row(triple[2]), row(point)) == 0


def isotropic(triple, lam):
    (x0,y0),(x1,y1),(x2,y2) = triple
    dx,dy = x1-x0,y1-y0
    return (dx*(y2-y0)-dy*(x2-x0) == 0
            and lam.denominator*dx*dx+lam.numerator*dy*dy == 0)


def expected_count(w, m, lam):
    if lam == 0:
        return m*comb(w,3)
    if lam >= 0:
        return 0
    p,q = -lam.numerator,lam.denominator
    a,b = isqrt(p),isqrt(q)
    if a*a != p or b*b != q:
        return 0
    d = gcd(a,b)
    a //= d
    b //= d
    H = min((m-1)//a,(w-1)//b)
    return 2*sum((h-1)*(m-a*h)*(w-b*h) for h in range(2,H+1))


def main():
    rows = []
    coeffs = [Fraction(-4), Fraction(-1), Fraction(-1,4),
              Fraction(-2), Fraction(0), Fraction(1,2),
              Fraction(1), Fraction(3,2)]
    total = 0
    for w in (3,4,5):
        for m in (4,5,6):
            board = [(x,y) for y in range(w) for x in range(m)]
            for lam in coeffs:
                maximal = 0
                for triple in combinations(board,3):
                    deg = isotropic(triple,lam)
                    is_max = all(forbidden(triple,p,lam)
                                 for p in board if p not in triple)
                    assert deg == is_max, (w,m,str(lam),triple,deg,is_max)
                    maximal += is_max
                    total += 1
                predicted = expected_count(w,m,lam)
                assert maximal == predicted, (w,m,str(lam),maximal,predicted)
                rows.append({'w':w,'m':m,'lambda':str(lam),
                             'maximal_triples':maximal})
    print(json.dumps({'cases':len(rows),'triples_checked':total,
                      'all_match':True,
                      'sample':[r for r in rows
                                if r['m']==6 and r['w'] in (3,5)]},
                     ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
