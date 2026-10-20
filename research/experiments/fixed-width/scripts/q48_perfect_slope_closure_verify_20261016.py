#!/usr/bin/env python3
"""Finite exact-integer audit of the dense-in-itself slope construction.

The infinite/perfect-set claim is established by the accompanying proof,
not by these finitely many samples.
"""
from itertools import combinations
from math import gcd, isqrt

SEEDS = [(47, 6, 16097, 17283), (53, 12, 18791, 24939)]


def pell_unit(d):
    a0 = isqrt(d)
    assert a0 * a0 != d
    m, den, a = 0, 1, a0
    p0, p1, q0, q1 = 1, a0, 0, 1
    while p1*p1-d*q1*q1 != 1:
        m = den*a-m
        den = (d-m*m)//den
        a = (a0+m)//den
        p0, p1 = p1, a*p1+p0
        q0, q1 = q1, a*q1+q0
    if p1%2 != 1 or q1%2 != 0:
        p1, q1 = p1*p1+d*q1*q1, 2*p1*q1
    assert p1*p1-d*q1*q1 == 1 and p1%2==1 and q1%2==0
    return p1,q1


def mul(a,b):
    return (a[0]*b[0]+a[1]*b[2],a[0]*b[1]+a[1]*b[3],
            a[2]*b[0]+a[3]*b[2],a[2]*b[1]+a[3]*b[3])


def pow_mat(a,n):
    r=(1,0,0,1)
    while n:
        if n&1:r=mul(r,a)
        a=mul(a,a)
        n//=2
    return r


def det4(m):
    # Independent fraction-free Bareiss determinant, unlike circle equation check.
    m=[list(row) for row in m]
    sign=1
    prev=1
    for k in range(3):
        if not m[k][k]:
            for j in range(k+1,4):
                if m[j][k]:m[k],m[j]=m[j],m[k];sign=-sign;break
            else:return 0
        pivot=m[k][k]
        for i in range(k+1,4):
            for j in range(k+1,4):
                num=m[i][j]*pivot-m[i][k]*m[k][j]
                assert num%prev==0
                m[i][j]=num//prev
        for i in range(k+1,4):m[i][k]=0
        prev=pivot
    return sign*m[3][3]


def circle_check(A,B,L,M):
    a,b,c,d=A*L-3*B*M,A*M-B*L,A*M+B*L,A*L+3*B*M
    assert 0<a<b<c<d and all(x%2 for x in (a,b,c,d))
    assert a*a-2*b*b+c*c == b*b-2*c*c+d*d == -8
    pts=[((d+sign*ch)//2,y) for y,ch in enumerate((a,b,c,d)) for sign in (-1,1)]
    assert len(set(pts))==8
    e=(a*a-b*b)//4-1
    f=(d*d-a*a)//4
    assert all(x*x+y*y-d*x+e*y+f==0 for x,y in pts)
    rows=[(x*x+y*y,x,y,1) for x,y in pts]
    for ids in combinations(range(8),4):
        assert det4([rows[i] for i in ids])==0
    return 70


def main():
    checks=0
    for A,B,L,M in SEEDS:
        assert gcd(A,B)==1 and A%2==1 and B%2==0 and A%3!=0
        P,Q=A*A-B*B,A*A-9*B*B
        assert Q*M*M-P*L*L==8
        u0,v0=pell_unit(P*Q)
        initial_A,initial_B=A,B
        for n in range(2):
            assert L%2==M%2==1 and Q*M*M-P*L*L==8
            U,V=M*M-L*L,9*M*M-L*L
            assert U%8==V%8==0 and U*A*A-V*B*B==8
            assert L*L*V>9*M*M*U
            x,y=U*A*A-4,A*B
            assert x%8==4 and y%2==0
            u,v=x*x//8-1,x*y//8
            assert u*u-U*V*v*v==1
            S=(u,V*v,U*v,u)
            assert S[0]*S[3]-S[1]*S[2]==1
            W=pow_mat(S,24)
            assert W[0]%6==W[3]%6==1 and W[1]%6==W[2]%6==0
            AA,BB=A,B
            for k in range(2):
                assert gcd(AA,BB)==1 and AA%2==1 and BB%2==0 and AA%3!=0
                assert U*AA*AA-V*BB*BB==8
                checks+=circle_check(AA,BB,L,M)
                AA2=W[0]*AA+W[1]*BB
                BB2=W[2]*AA+W[3]*BB
                assert AA2*BB<AA*BB2
                AA,BB=AA2,BB2
            Ln=u0*L+Q*v0*M
            Mn=u0*M+P*v0*L
            assert Mn*Mn-Ln*Ln>2*U
            L,M=Ln,Mn
            print(f'PASS seed={initial_A}/{initial_B} n={n} k=0,1 (140 determinants)')
    print('PASS total independent 4-point determinants:',checks)
    print('PASS congruence-preserving 24th-power dual Pell maps and strict slope decrease')

if __name__=='__main__':main()
