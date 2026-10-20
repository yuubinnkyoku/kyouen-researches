#!/usr/bin/env python3
"""Independent exact-integer audit of the 4-row 8-point infinite-slope family.

All arithmetic is integer; finite verification supports, but does not replace,
the symbolic Pell-automorphism proof in the paired report.
"""
from itertools import combinations
from math import gcd, isqrt

U = 1859131879201
V = 16953823416
D = 12025


def determinant(rows):
    """Bareiss fraction-free determinant; independent of the circle equation."""
    a = [list(row) for row in rows]
    n = len(a)
    prev = 1
    sign = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            pivot = next((i for i in range(k + 1, n) if a[i][k]), None)
            if pivot is None:
                return 0
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        p = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * p - a[i][k] * a[k][j]
                assert numerator % prev == 0
                a[i][j] = numerator // prev
            a[i][k] = 0
        prev = p
    return sign * a[-1][-1]


def next_pair(c, b):
    return U*c + 325*V*b, 37*V*c + U*b


def chords(c, b):
    return 18*c - 19*b, 19*c - 6*b, 19*c + 6*b, 18*c + 19*b


def audit(generations=5):
    assert U*U - D*V*V == 1
    assert U % 2 == 1 and V % 2 == 0
    assert U % 3 == 1 and V % 3 == 0
    assert 109*V < U < 110*V
    c,b = 3,1
    old = None
    slopes = set()
    output=[]
    for n in range(generations):
        assert 37*c*c - 325*b*b == 8
        assert gcd(c,b) == 1 and c % 3 == 0 and b % 3 == 1
        assert c % 2 == b % 2 == 1
        assert 2*b < c <= 3*b
        a0,a1,a2,a3=chords(c,b)
        assert 0 < a0 < a1 < a2 < a3
        assert all(a%2 for a in (a0,a1,a2,a3))
        assert a0*a0-2*a1*a1+a2*a2 == -8
        assert a1*a1-2*a2*a2+a3*a3 == -8
        assert gcd(3*c,b) == 1
        if old is not None:
            assert c*old[1] < old[0]*b  # strictly decreasing c/b
        old=(c,b)
        assert (3*c,b) not in slopes
        slopes.add((3*c,b))
        assert 3*c*pow(b,-1,576) % 576 == 9
        S=a3
        Bcircle=(a0*a0-a1*a1)//4-1
        Ccircle=(S*S-a0*a0)//4
        points=[]
        for y,di in enumerate((a0,a1,a2,a3)):
            assert (S-di)%2==0
            left,right=(S-di)//2,(S+di)//2
            assert left>=0 and right<=S
            assert left != right
            for x in (left,right):
                assert x*x+y*y-S*x+Bcircle*y+Ccircle==0
                points.append((x,y))
        assert len(points)==len(set(points))==8
        assert len({x for x,y in points})==8
        for subset in combinations(points,4):
            assert determinant([(x,y,x*x+y*y,1) for x,y in subset]) == 0
        output.append((n,3*c,b,a3))
        c,b=next_pair(c,b)
    return output


def modular_recurrence_orders():
    """Independently check the finite-group congruence step for sample moduli."""
    result = {}
    for N in (2, 3, 5, 7, 27, 64, 100, 576):
        mod = 2 * N
        t = ((U % mod, (325*V) % mod), ((37*V) % mod, U % mod))
        p = ((1, 0), (0, 1))
        for h in range(1, 200000):
            p = tuple(tuple(sum(p[i][k] * t[k][j] for k in range(2)) % mod
                            for j in range(2)) for i in range(2))
            if p == ((1, 0), (0, 1)):
                break
        else:
            raise AssertionError(f"no modular return found for {N}")
        c = (p[0][0]*3 + p[0][1]) % mod
        b = (p[1][0]*3 + p[1][1]) % mod
        assert (c,b) == (3 % mod, 1 % mod)
        initial = chords(3,1)
        returned = chords(c,b)
        assert all((x-y)%mod == 0 for x,y in zip(initial,returned))
        for x,y in zip(initial,returned):
            assert ((returned[-1]+y)//2 - (initial[-1]+x)//2) % N == 0
        result[N] = h
    return result


if __name__ == '__main__':
    out=audit()
    orders=modular_recurrence_orders()
    print('unit_identity=PASS; primitive_parity=PASS; strict_slopes=PASS')
    print('norm=PASS; chord_equations=PASS; 8_point_circle=PASS')
    print('independent_lifted_determinants=PASS (70 per generation)')
    print('mod576_residue_9=PASS')
    print('modular_return_orders=' + str(orders))
    print('generation,A,B,max_chord')
    for row in out:
        print(','.join(map(str,row)))
