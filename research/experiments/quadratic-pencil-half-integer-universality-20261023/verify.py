#!/usr/bin/env python3
"""Independent exact 4x4 determinant check for the 3-row quadratic pencil."""
from fractions import Fraction
from itertools import combinations, permutations
from math import comb

PERMS = [(p, (-1) ** sum(p[i] > p[j] for i in range(4) for j in range(i+1,4))) for p in permutations(range(4))]

def det4(rows):
    return sum(sign * rows[0][p[0]] * rows[1][p[1]] * rows[2][p[2]] * rows[3][p[3]] for p,sign in PERMS)

def coefficients(pts):
    a = det4([(x*x,x,y,1) for x,y in pts])
    b = det4([(y*y,x,y,1) for x,y in pts])
    return a,b

def generic_forbidden(pts):
    ys = {y for x,y in pts}
    if len(ys) == 1:
        return True
    if len(ys) != 2:
        return False
    row = [[x for x,y in pts if y==j] for j in sorted(ys)]
    return len(row[0]) == len(row[1]) == 2 and sum(row[0]) == sum(row[1])

def witness(k):
    if k >= 0:
        pts = ((0,0),(k+1,0),(0,1),(1,2))
    else:
        pts = ((0,0),(1-k,0),(1,1),(1,2))
    return pts

def main():
    for m in range(2,9):
        pts = [(x,y) for x in range(m) for y in range(3)]
        exceptions = set()
        b_nonzero = 0
        for quad in combinations(pts,4):
            a,b = coefficients(quad)
            assert (a == 0 and b == 0) == generic_forbidden(quad), (m,quad,a,b)
            if b:
                b_nonzero += 1
                lam = Fraction(-a,b)
                assert lam.denominator in (1,2), (quad,lam)
                exceptions.add(lam)
        assert all(Fraction(k,2) in exceptions for k in range(-(m-2),m-1)), (m,exceptions)
        print('m=',m,'four_points=',comb(3*m,4),'B_nonzero=',b_nonzero,
              'exception_count=',len(exceptions),'min=',min(exceptions),'max=',max(exceptions))
    for k in range(-20,21):
        a,b = coefficients(witness(k))
        assert b and Fraction(-a,b) == Fraction(k,2), (k,a,b)
        assert not generic_forbidden(witness(k))
    print('explicit witnesses k=-20..20: PASS')
    print('all tested classifications: PASS')

if __name__ == '__main__':
    main()
