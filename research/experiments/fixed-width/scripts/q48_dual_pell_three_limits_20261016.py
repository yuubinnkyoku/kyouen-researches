#!/usr/bin/env python3
"""Independent exact-integer audit of three disjoint infinite-slope families.

The two new families use fixed (L,M) and variable (A,B); the older
family uses fixed (L,M) and variable (C,B) with A=3C.
"""
from itertools import combinations, permutations
from math import gcd, isqrt


def det4(rows):
    total = 0
    for p in permutations(range(4)):
        inv = sum(p[i] > p[j] for i in range(4) for j in range(i+1,4))
        product = 1
        for i, j in enumerate(p):
            product *= rows[i][j]
        total += (-1 if inv % 2 else 1) * product
    return total


def pell_unit_from_seed(A, B, L, M):
    U = M*M-L*L
    V = 9*M*M-L*L
    X = U*A*A-4
    Y = A*B
    assert X % 4 == 0 and Y % 2 == 0 and X*Y % 8 == 0
    u = X*X//8-1
    v = X*Y//8
    assert u*u-U*V*v*v == 1
    assert u % 6 == 1 and (U*v) % 6 == 0 and (V*v) % 6 == 0
    return U, V, u, v


def circle_points(chords):
    d = chords[-1]
    return [((d+sgn*ch)//2, y) for y, ch in enumerate(chords) for sgn in (-1, 1)]


def audit_chords(chords):
    a,b,c,d=chords
    assert 0<a<b<c<d and all(t%2 for t in chords)
    assert a*a-2*b*b+c*c == -8
    assert b*b-2*c*c+d*d == -8
    points = circle_points(chords)
    assert len(set(points)) == 8
    # Direct circle equation independent of the two second-difference tests.
    E=(a*a-b*b)//4-1
    F=(d*d-a*a)//4
    assert all(x*x+y*y-d*x+E*y+F == 0 for x,y in points)
    lifted=[(x*x+y*y,x,y,1) for x,y in points]
    for subset in combinations(lifted,4):
        assert det4(subset) == 0
    return 70


def audit_new(A,B,L,M):
    U,V,u,v=pell_unit_from_seed(A,B,L,M)
    assert U*A*A-V*B*B == 8
    assert gcd(A,B)==1 and A%2==1 and B%2==0 and A%3!=0
    assert L*L*V > 9*M*M*U # limiting chord a remains positive
    first_ratio=(A,B)
    checked=0
    for n in range(5):
        assert U*A*A-V*B*B == 8
        assert gcd(A,B)==1 and A%2==1 and B%2==0 and A%3!=0
        assert A>3*B and L*A>3*M*B
        assert A*first_ratio[1] <= first_ratio[0]*B
        chords=(A*L-3*B*M,A*M-B*L,A*M+B*L,A*L+3*B*M)
        checked += audit_chords(chords)
        A2=u*A+V*v*B
        B2=U*v*A+u*B
        assert A2*B<A*B2 # strict decrease
        A,B=A2,B2
    return {'seed':str(first_ratio[0])+'/'+str(first_ratio[1]),'U':U,'V':V,
            'u':u,'v':v,'determinants':checked,
            'last_A_digits':len(str(A)),'last_B_digits':len(str(B))}


def audit_old():
    U=1859131879201
    v=16953823416
    assert U*U-12025*v*v == 1 and U%6==1 and v%6==0
    C,B=3,1
    checked=0
    for n in range(5):
        assert 37*C*C-325*B*B == 8
        assert gcd(C,B)==1 and C%2==B%2==1 and C%3==0 and B%3==1
        chords=(18*C-19*B,19*C-6*B,19*C+6*B,18*C+19*B)
        checked += audit_chords(chords)
        C2=U*C+325*v*B
        B2=37*v*C+U*B
        assert C2*B<C*B2
        C,B=C2,B2
    return {'seed':'9/1','determinants':checked,'last_A_digits':len(str(3*C)),
            'last_B_digits':len(str(B))}


if __name__=='__main__':
    old=audit_old()
    new1=audit_new(47,6,16097,17283)
    new2=audit_new(53,12,18791,24939)
    print('old',old)
    print('new1',new1)
    print('new2',new2)
    print('TOTAL_DETERMINANTS',sum(x['determinants'] for x in (old,new1,new2)))
    print('PASS')
