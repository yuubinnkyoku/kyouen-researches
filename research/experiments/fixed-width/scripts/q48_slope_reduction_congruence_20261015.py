#!/usr/bin/env python3
"""Finite checks for q=8, four-row slope gap, Pell reduction and congruence orbits.

The unbounded theorems are proved in the accompanying report, not by this script.
Only standard-library exact integer arithmetic is used.
"""
from math import gcd, isqrt

CHORDS = [
    (35, 51, 63, 73),
    (1331, 1935, 2391, 2773),
    (50543, 73479, 90795, 105301),
    (445465, 715719, 908883, 1067653),
    (98119, 1096275, 1547259, 1893727),
]


def parameters(ch):
    a,b,c,d=ch
    s,t,u,v=(d+a)//2,(d-a)//2,(c+b)//2,(c-b)//2
    assert s*t==3*u*v
    L=gcd(s,v)
    A,B=s//L,v//L
    g=gcd(A,3)
    assert (u*g)%A==0
    M=u*g//A
    P=A*A-B*B
    Q=(A*A-9*B*B)//(g*g)
    assert Q*M*M-P*L*L==8
    return A,B,g,P,Q,L,M


def pell(D):
    """Least U,V>0 satisfying U^2-D V^2=1, by continued fractions."""
    r=isqrt(D)
    assert r*r!=D
    m=0; den=1; a=r
    p0,p1=1,a; q0,q1=0,1
    while p1*p1-D*q1*q1!=1:
        m=den*a-m
        den=(D-m*m)//den
        a=(r+m)//den
        p0,p1=p1,a*p1+p0
        q0,q1=q1,a*q1+q0
    return p1,q1


def chord(A,B,g,L,M):
    return (A*L-(3*B//g)*M,(A//g)*M-B*L,
            (A//g)*M+B*L,A*L+(3*B//g)*M)


def coordinates(ds):
    d=ds[-1]
    assert all(0<t<=d and t%2 for t in ds)
    pts=[((d-t)//2,y) for y,t in enumerate(ds)] + [((d+t)//2,y) for y,t in enumerate(ds)]
    assert len(set(pts))==8
    return pts


def det3(rows):
    (a,b,c),(d,e,f),(g,h,i)=rows
    return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)


def check_circle(ds):
    assert ds[0]<ds[1]<ds[2]<ds[3]
    assert ds[0]**2-2*ds[1]**2+ds[2]**2==-8
    assert ds[1]**2-2*ds[2]**2+ds[3]**2==-8
    pts=coordinates(ds)
    # Independent lifted-determinant test, avoiding the chord recurrence.
    p0,p1,p2=pts[0],pts[1],pts[2]
    def lift(p):
        x,y=p;u,v=p0
        return x-u,y-v,x*x+y*y-u*u-v*v
    for p in pts[3:]:
        assert det3([lift(p1),lift(p2),lift(p)])==0
    return pts


def advance(L,M,P,Q,U,V):
    return U*L+Q*V*M,U*M+P*V*L


def backwards(L,M,P,Q,U,V):
    return U*L-Q*V*M,U*M-P*V*L


def modular_order(U,V,P,Q,N):
    """Order of the Pell matrix mod N; identity rather than seed orbit."""
    a,b,c,d=1,0,0,1
    u,v,w,z=U%N,(Q*V)%N,(P*V)%N,U%N
    k=0
    while True:
        a,b,c,d=(a*u+b*w)%N,(a*v+b*z)%N,(c*u+d*w)%N,(c*v+d*z)%N
        k+=1
        if (a,b,c,d)==(1%N,0,0,1%N):return k
        assert k<=10000,('unexpectedly long modular order',N)


def audit():
    # Exact residue proof checks for oddness of every chord.
    from itertools import product
    parity_patterns = [r for r in product((0,1),repeat=4)
                       if (r[0]-2*r[1]+r[2])%4==0
                       and (r[1]-2*r[2]+r[3])%4==0]
    assert parity_patterns == [(0,0,0,0),(1,1,1,1)]
    assert not [r for r in product((0,1,4),repeat=4)
                if (r[0]-2*r[1]+r[2]+2)%8==0
                and (r[1]-2*r[2]+r[3]+2)%8==0]
    tests=0
    for ds in CHORDS:
        A,B,g,P,Q,L,M=parameters(ds)
        assert A>3*B
        # Exact integer version of A/B > sqrt(9+6 sqrt(2)).
        assert A**4-18*A*A*B*B+9*B**4>0
        assert chord(A,B,g,L,M)==ds
        D=P*Q
        u,v=pell(D)
        U,V=u*u+D*v*v,2*u*v
        assert U%2==1 and V%2==0 and U*U-D*V*V==1
        for mod in (3,5,9,27,100):
            k=modular_order(U,V,P,Q,2*mod)
            l,m=L,M
            for _ in range(k):l,m=advance(l,m,P,Q,U,V)
            new_ds=chord(A,B,g,l,m)
            assert all(new_ds[i]% (2*mod)==ds[i]%(2*mod) for i in range(4))
            old_pts=coordinates(ds)
            new_pts=check_circle(new_ds)
            assert all((x1-x0)%mod==0 and y1==y0
                       for (x0,y0),(x1,y1) in zip(old_pts,new_pts))
            assert new_ds[-1]>ds[-1]
            assert Q*m*m-P*l*l==8
            tests+=1
        # Reduction check on two forward iterates, including positivity and strict decrease.
        for _ in range(2):
            L2,M2=advance(L,M,P,Q,U,V)
            assert L2*L2>8*Q*V*V
            assert backwards(L2,M2,P,Q,U,V)==(L,M)
            L,M=L2,M2
        print('slope=%d/%d initial_span=%d modular_orders(3,5,9,27,100)=%s' %
              (A,B,ds[-1], [modular_order(U,V,P,Q,2*mod) for mod in (3,5,9,27,100)]))
    # Independent small-coefficient norm-equation reduction audit.
    generic=0
    for P in range(2,21):
        for Q in range(1,21):
            D=P*Q
            if isqrt(D)**2==D:continue
            u,v=pell(D)
            U,V=u*u+D*v*v,2*u*v
            for L in range(1,1001):
                numerator=P*L*L+8
                if numerator%Q:continue
                M=isqrt(numerator//Q)
                if Q*M*M!=numerator:continue
                if L*L>8*Q*V*V:
                    l,m=backwards(L,M,P,Q,U,V)
                    assert 0<l<L and m>0 and Q*m*m-P*l*l==8
                    assert advance(l,m,P,Q,U,V)==(L,M)
                    generic+=1
    print('PASS: %d residue-preserving circles (five seeds x five moduli), %d small-norm reductions' % (tests,generic))

if __name__=='__main__':audit()
