#!/usr/bin/env python3
"""Independent finite audit for isotropic terminal triples of the quadratic-pencil game.

Proof of the unbounded statement is in README.md; this script checks finite cases.
No third-party dependencies, floating point, or randomness.
"""
from fractions import Fraction
from itertools import combinations, permutations
from math import comb, isqrt
import json

PERMS = [(p, (-1) ** sum(p[i] > p[j] for i in range(4) for j in range(i + 1, 4)))
         for p in permutations(range(4))]
LAMBDAS = [Fraction(n) for n in (-16, -9, -4, -2, -1, 0, 1, 2)] + [Fraction(-1, 4), Fraction(1, 2)]


def det3(a):
    return (a[0][0] * (a[1][1]*a[2][2]-a[1][2]*a[2][1])
            - a[0][1] * (a[1][0]*a[2][2]-a[1][2]*a[2][0])
            + a[0][2] * (a[1][0]*a[2][1]-a[1][1]*a[2][0]))


def det4_direct(points, lam):
    # Entirely separate 4x4 permutation expansion, rational arithmetic.
    rows = [(Fraction(x*x) + lam*y*y, Fraction(x), Fraction(y), Fraction(1)) for x, y in points]
    return sum(sign * rows[0][p[0]] * rows[1][p[1]] * rows[2][p[2]] * rows[3][p[3]]
               for p, sign in PERMS)


def det4_difference(points, lam):
    # 3x3 difference determinant with integer-scaled quadratic form.
    scale = lam.denominator
    def lift(p):
        x, y = p
        return (scale*x*x + lam.numerator*y*y, scale*x, scale*y)
    base = lift(points[0])
    mat = [tuple(a-b for a,b in zip(lift(p), base)) for p in points[1:]]
    return det3(mat)


def isotropic_triple(triple, lam):
    # Independent geometry: collinearity and vanishing Q(direction).
    (x0,y0),(x1,y1),(x2,y2)=triple
    u,v=x1-x0,y1-y0
    return (u*(y2-y0)-v*(x2-x0)==0 and
            Fraction(u*u)+lam*v*v==0)


def predicted(w, m, lam):
    if lam == 0:
        return m*comb(w,3)
    if lam > 0:
        return 0
    num, den = -lam.numerator, lam.denominator
    a,b = isqrt(num),isqrt(den)
    if a*a != num or b*b != den:
        return 0
    limit=min((m-1)//a,(w-1)//b)
    return 2*sum((h-1)*(m-a*h)*(w-b*h) for h in range(2,limit+1))


def check(w, m, lam, independent_full=False):
    board=[(x,y) for x in range(m) for y in range(w)]
    terminal=[]
    for indices in combinations(range(len(board)), 3):
        tri=tuple(board[i] for i in indices)
        geom=isotropic_triple(tri,lam)
        if geom:
            terminal.append(tri)
        # Exhaustive direct determinant test of maximality, independently of rank criterion.
        maximal=True
        for i,p in enumerate(board):
            if i in indices:
                continue
            d=det4_difference((*tri,p),lam)
            if independent_full:
                assert d == -det4_direct((*tri,p),lam)*lam.denominator**3, (w,m,lam,tri,p)
            if d != 0:
                maximal=False
                if not independent_full:
                    break
        assert maximal == geom, (w,m,str(lam),tri,maximal,geom)
    assert len(terminal)==predicted(w,m,lam), (w,m,str(lam),len(terminal),predicted(w,m,lam))
    return {'w':w,'m':m,'lambda':str(lam),'maximal_three':len(terminal), 'predicted':predicted(w,m,lam)}


def main():
    results=[]
    for m in range(4,11):
        for lam in LAMBDAS:
            # Full independent 4x4 audit for 4 and 5 columns, all triples, all fourth points.
            results.append(check(3,m,lam,independent_full=m<=5))
    extras=[(5,5,Fraction(-1,4)),(5,5,Fraction(-1)),(7,5,Fraction(-4,9)),
            (7,7,Fraction(-9,4)),(6,7,Fraction(-1,4)),(5,7,Fraction(-2)),
            (5,7,Fraction(0)),(4,7,Fraction(-1,4)),(6,6,Fraction(1))]
    for w,m,lam in extras:
        results.append(check(w,m,lam,independent_full=False))
    print(json.dumps({'method':'all 3-subsets; fourth points until legal; two determinants at w=3,m<=5',
                      'boards':len(results),'records':results},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
