#!/usr/bin/env python3
"""Independent exact arithmetic + determinant checks for outer-row 2+1+1 circles.
Run: python research/experiments/geometry/scripts/verify_outer_211_norm.py
Uses only the Python standard library. No floating point is used.
"""
from fractions import Fraction
from itertools import combinations
from math import isqrt


def mul(z, w):
    a, b = z
    c, d = w
    return a*c + 2*b*d, a*d + b*c


def norm(z):
    a, b = z
    return a*a - 2*b*b


def div_round(z, w):
    a, b = z
    c, d = w
    n = norm(w)
    assert n
    return (round(Fraction(a*c-2*b*d, n)),
            round(Fraction(b*c-a*d, n)))


def sub(z, w):
    return z[0]-w[0], z[1]-w[1]


def euclidean_gcd(z, w):
    while w != (0, 0):
        q = div_round(z, w)
        z, w = w, sub(z, mul(q, w))
    return z


def factor(n):
    f = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            f[p] = f.get(p, 0)+1
            n //= p
        p += 1 if p == 2 else 2
    if n > 1:
        f[n] = f.get(n, 0)+1
    return f


def admissible(n):
    return all(e % 2 == 0 for p, e in factor(n).items()
               if p % 8 in (3, 5))


def split_prime_element(p):
    assert p % 8 in (1, 7)
    t = next(x for x in range(p) if x*x % p == 2)
    z = euclidean_gcd((p, 0), (t, 1))
    assert abs(norm(z)) == p, (p, z, norm(z))
    return z


def witness(n):
    """Find integers X,Y satisfying 2X^2-Y^2=n, iff inert valuations even."""
    if not admissible(n):
        return None
    z = (1, 0)
    for p, e in factor(n).items():
        if p == 2:
            base = (0, 1)
            power = e
        elif p % 8 in (3, 5):
            base = (p, 0)
            power = e // 2
        else:
            base = split_prime_element(p)
            power = e
        for _ in range(power):
            z = mul(z, base)
    assert abs(norm(z)) == n
    if norm(z) > 0:
        z = mul(z, (1, 1))  # norm(1+sqrt(2)) = -1
    assert norm(z) == -n
    Y, X = z
    assert 2*X*X-Y*Y == n
    return X, Y


def determinant4(points):
    rows = [[x*x+y*y, x, y, 1] for x,y in points]
    def det(a):
        if len(a) == 1:
            return a[0][0]
        return sum((-1)**j * a[0][j] * det([row[:j]+row[j+1:] for row in a[1:]])
                   for j in range(len(a)))
    return det(rows)


def run():
    checked = 0
    solvable = 0
    no_mod8 = 0
    max_abs_coordinate = 0
    for h in range(1, 31):
        for d in range(1, 101):
            n = d*d + 8*h*h
            xy = witness(n)
            assert (xy is not None) == admissible(n)
            if xy is not None:
                X, Y = xy
                assert (X-d)%2 == (Y-d)%2 == 0
                # Translate the chord to x=0,d, with the other rows h,2h.
                u, v = (d+X)//2, (d+Y)//2
                assert determinant4([(0,0),(d,0),(u,h),(v,2*h)]) == 0
                solvable += 1
                max_abs_coordinate = max(max_abs_coordinate, abs(u), abs(v))
            if h%2 and d%2==0 and d%8:
                assert xy is None, (h,d,n)
                no_mod8 += 1
            checked += 1

    # Independent bounded search: direct determinant, no norm arithmetic.
    direct = 0
    direct_concyclic = 0
    for h in range(1, 5):
        for d in range(1, 9):
            for u in range(-7, 15):
                for v in range(-7, 15):
                    det = determinant4([(0,0),(d,0),(u,h),(v,2*h)])
                    # Re-express by the algebraic equation, as an independent audit.
                    X,Y = 2*u-d,2*v-d
                    eq = 2*X*X-Y*Y == d*d+8*h*h
                    assert (det == 0) == eq, (h,d,u,v,det)
                    if det == 0:
                        assert admissible(d*d+8*h*h)
                        direct_concyclic += 1
                    direct += 1
    print('arithmetic_cases:', checked)
    print('constructed_witnesses:', solvable)
    print('mod8_obstructed_cases:', no_mod8)
    print('direct_determinant_candidates:', direct)
    print('direct_determinant_circles:', direct_concyclic)
    print('max_abs_constructed_x:', max_abs_coordinate)
    print('status: PASS')


if __name__ == '__main__':
    run()
