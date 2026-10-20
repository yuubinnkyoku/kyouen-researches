#!/usr/bin/env python3
"""Exact-integer finite audit of a double-Pell family (not a proof of asymptotics).

Checks a fixed-slope Pell orbit, dual Pell orbit, pairwise disjoint
slope intervals, and all 70 4-point determinants of each sampled circle.
Uses only the standard library.
"""
from itertools import combinations, permutations
from math import gcd, isqrt

A0, B0, L0, M0 = 47, 6, 16097, 17283
P, Q = A0*A0-B0*B0, A0*A0-9*B0*B0
D = P*Q


def fundamental_unit(D):
    a0 = isqrt(D)
    assert a0*a0 != D
    m, d, a = 0, 1, a0
    pm, p, qm, q = 1, a0, 0, 1
    while p*p-D*q*q != 1:
        m = d*a-m
        d = (D-m*m)//d
        a = (a0+m)//d
        pm, p = p, a*p+pm
        qm, q = q, a*q+qm
    return p, q


def det4(rows):
    out = 0
    for p in permutations(range(4)):
        sign = -1 if sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2 else 1
        term = sign
        for i,j in enumerate(p):
            term *= rows[i][j]
        out += term
    return out


def verify_circle(A,B,L,M):
    a,b,c,d = A*L-3*B*M, A*M-B*L, A*M+B*L, A*L+3*B*M
    assert 0<a<b<c<d and all(v%2 for v in (a,b,c,d))
    assert a*a-2*b*b+c*c == -8
    assert b*b-2*c*c+d*d == -8
    pts = [((d+sign*ch)//2,y) for y,ch in enumerate((a,b,c,d)) for sign in (-1,1)]
    assert len(set(pts)) == 8
    # An independent circle equation check, plus all 4-point determinants.
    e=(a*a-b*b)//4-1
    f=(d*d-a*a)//4
    assert all(x*x+y*y-d*x+e*y+f==0 for x,y in pts)
    rows=[(x*x+y*y,x,y,1) for x,y in pts]
    for sub in combinations(rows,4):
        assert det4(sub)==0
    return 70


def main():
    assert Q*M0*M0-P*L0*L0 == 8
    u0,v0=fundamental_unit(D)
    assert u0*u0-D*v0*v0==1
    assert u0%2==1 and v0%2==0
    L,M=L0,M0
    samples=[]
    for n in range(4):
        assert Q*M*M-P*L*L==8 and L%2==M%2==1 and L<M
        assert 3*M<4*L
        U,V=M*M-L*L,9*M*M-L*L
        assert U%8==V%8==0 and U*A0*A0-V*B0*B0==8
        x=U*A0*A0-4
        y=A0*B0
        assert x%8==4 and x*y%8==0
        u=x*x//8-1
        v=x*y//8
        assert u*u-U*V*v*v==1
        assert u%6==1 and (U*v)%6==(V*v)%6==0
        assert L*L*V>9*M*M*U
        AA,BB=A0,B0
        determinants=0
        first_B=None
        for k in range(3):
            assert U*AA*AA-V*BB*BB==8
            assert gcd(AA,BB)==1 and AA%2==1 and BB%2==0 and AA%3!=0
            determinants+=verify_circle(AA,BB,L,M)
            AA2=u*AA+V*v*BB
            BB2=U*v*AA+u*BB
            assert AA2*BB<AA*BB2
            AA,BB=AA2,BB2
            if k==0:
                first_B=BB
        Ln=u0*L+Q*v0*M
        Mn=u0*M+P*v0*L
        Un=Mn*Mn-Ln*Ln
        assert Un>2*U and first_B>2*B0
        # r_(n,1) < alpha_(n+1), squared and cross-multiplied.
        # alpha_(n+1)^2-alpha_n^2 = 8/B0^2 (1/U-1/Un)
        assert B0*B0*Un < first_B*first_B*(Un-U)
        samples.append((n, len(str(L)),len(str(M)),len(str(first_B)),determinants))
        L,M=Ln,Mn
    print('P,Q,D:',P,Q,D)
    print('fundamental unit:',u0,v0)
    print('fundamental unit parity: odd/even PASS')
    print('fixed-slope seed:',A0,B0,L0,M0)
    for row in samples:
        print('n,L-digits,M-digits,dual-first-B-digits,determinants:',*row)
    print('total determinant checks:',sum(x[-1] for x in samples))
    print('dual interval disjointness: PASS')
    print('PASS')


if __name__=='__main__':
    main()
