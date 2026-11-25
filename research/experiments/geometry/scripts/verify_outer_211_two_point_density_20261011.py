#!/usr/bin/env python3
"""Independent integer checks for outer-row 2+1+1 thin-but-infinite theorem."""
from math import isqrt


def determinant(a):
    b = [[x*x+y*y, x, y, 1] for x,y in a]
    def det(m):
        if len(m)==1:
            return m[0][0]
        return sum((-1)**j * x * det([r[:j]+r[j+1:] for r in m[1:]]) for j,x in enumerate(m[0]))
    return det(b)


def norm_admissible(n):
    """Independent trial-factorization implementation of the norm criterion."""
    p=2
    while p*p<=n:
        e=0
        while n%p==0:
            n//=p
            e+=1
        if p%8 in (3,5) and e%2:
            return False
        p=3 if p==2 else p+2
    return n%8 not in (3,5)


def valuations(n,p):
    k=0
    while n%p==0:
        n//=p
        k+=1
    return k


def local_count(p,h):
    if h%p==0:
        return None
    return sum((d*d+8*h*h)%p==0 and (d*d+8*h*h)%(p*p)!=0 for d in range(p*p))


def pell_points(h, count):
    d,x=0,2*h
    out=[]
    for _ in range(count):
        d,x=3*d+4*x,2*d+3*x
        assert d%2==x%2==0 and 0<x<d
        points=((0,0),(d,0),((d+x)//2,h),(d//2,2*h))
        assert determinant(points)==0
        assert d*d+8*h*h==2*x*x
        out.append((d,x))
    return out


def run():
    primes=[3,11,19,43,59,67]
    for p in primes:
        assert p%8==3
        for h in range(1,15):
            if h%p:
                assert local_count(p,h)==2*(p-1), (p,h,local_count(p,h))
    cases=0
    local_obstructions=0
    for h in range(1,13):
        for d in range(1,1501):
            n=d*d+8*h*h
            good=norm_admissible(n)
            for p in primes:
                if h%p and valuations(n,p)%2:
                    local_obstructions+=1
                    assert not good, (h,d,p)
            cases+=1
    for h in range(1,11):
        assert pell_points(h,12)
    samples=[]
    for bound in [100,1000,10000,50000]:
        good=sum(norm_admissible(d*d+8) for d in range(1,bound+1))
        samples.append((bound,good,round(good/bound,6)))
    print('local_prime_tests',len(primes)*14-sum(14//p for p in primes))
    print('local_count_formula', '2*(p-1) residues mod p^2 for p=3 mod 8, p not dividing h')
    print('norm_vs_local_cases',cases,'local_obstructions_checked',local_obstructions)
    print('pell_d_h1',pell_points(1,5))
    print('pell_h_values',10,'pell_levels',12,'integer_determinants_checked',120)
    print('finite_counts_h1',samples)
    print('PASS')


if __name__=='__main__':
    run()
