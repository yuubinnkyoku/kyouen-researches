#!/usr/bin/env python3
"""Exact audit of generalized Pell families for 4-row 8-point lattice circles.

No floating point, no external dependencies. Two independent checks:
  (1) two quadratic second-difference identities;
  (2) all 70 lifted 4-point cocircular determinants.
"""
from math import gcd, isqrt
from itertools import combinations

SEEDS = [
    (445465, 715719, 908883, 1067653),
    (98119, 1096275, 1547259, 1893727),
]

def pell_unit(D):
    a0 = isqrt(D)
    assert a0*a0 != D
    m, den, a = 0, 1, a0
    pprev, p = 1, a
    qprev, q = 0, 1
    while p*p-D*q*q != 1:
        m = den*a-m
        den = (D-m*m)//den
        a = (a0+m)//den
        pprev, p = p, a*p+pprev
        qprev, q = q, a*q+qprev
    return p, q

def normalize(ds):
    a,b,c,d = ds
    assert a < b < c < d and all(x>0 and x%2 for x in ds)
    s,v = (d+a)//2,(c-b)//2
    L = gcd(s,v)
    A,B = s//L,v//L
    g = gcd(A,3)
    t,u = (d-a)//2,(c+b)//2
    assert (t*g)%(3*B)==0 and (u*g)%A==0
    M = t*g//(3*B)
    assert M==u*g//A
    P,Q = A*A-B*B,(A*A-9*B*B)//(g*g)
    assert A>3*B and P>0 and Q>0 and Q*M*M-P*L*L==8
    return A,B,g,L,M,P,Q

def chord(A,B,g,L,M):
    return (A*L-3*B*M//g, A*M//g-B*L, A*M//g+B*L, A*L+3*B*M//g)

def det(mat):
    # Exact fraction-free determinant using permutations (n=4).
    ans=0
    from itertools import permutations
    for perm in permutations(range(4)):
        inv=sum(perm[i]>perm[j] for i in range(4) for j in range(i+1,4))
        prod=1
        for i in range(4):prod*=mat[i][perm[i]]
        ans+=(-1 if inv&1 else 1)*prod
    return ans

def audit(ds):
    a,b,c,d=ds
    assert 0<a<b<c<d and all(x&1 for x in ds)
    assert a*a-2*b*b+c*c==-8
    assert b*b-2*c*c+d*d==-8
    pts=[((d+sign*di)//2,i) for i,di in enumerate(ds) for sign in (-1,1)]
    assert len(set(pts))==8 and min(x for x,y in pts)==0
    assert max(x for x,y in pts)==d
    for four in combinations(pts,4):
        rows=[[x,y,x*x+y*y,1] for x,y in four]
        assert det(rows)==0
    return pts

def run():
    for seed in SEEDS:
        A,B,g,L,M,P,Q=normalize(seed)
        D=P*Q
        U,V=pell_unit(D)
        assert U*U-D*V*V==1
        assert U&1 and not V&1
        assert isqrt(D)**2!=D
        print(f'seed={seed}')
        print(f'slope={A}/{B} g={g} P={P} Q={Q} D={D} initial=(L={L},M={M})')
        print(f'pell_unit=(U={U},V={V}) digits=({len(str(U))},{len(str(V))})')
        for k in range(3):
            ds=chord(A,B,g,L,M)
            audit(ds)
            print(f'  generation={k} max_chord_digits={len(str(ds[-1]))} chord_sha256=',end='')
            import hashlib
            print(hashlib.sha256(','.join(map(str,ds)).encode()).hexdigest())
            if k==0:assert ds==seed
            L,M=U*L+Q*V*M, U*M+P*V*L
            assert Q*M*M-P*L*L==8
    print('PASS: 2 seeds x 3 generations x 70 lifted determinants, exact Pell recurrence')

if __name__=='__main__':run()
