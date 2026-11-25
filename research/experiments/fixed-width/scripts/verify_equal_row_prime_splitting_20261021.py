#!/usr/bin/env python3
"""Independent finite-field audits; mathematical proof is in the report."""
from math import isqrt

def primes(n):
    return [p for p in range(2,n+1) if all(p%d for d in range(2,isqrt(p)+1))]

def recurrence(p,n):
    qr={x*x%p for x in range(p)}
    ans=set()
    for a in qr:
        for b in qr:
            v=[a,b]
            for j in range(2,n):
                v.append((2*v[-1]-v[-2]-2)%p)
            if all(x in qr for x in v):
                ans.add(tuple(v))
    return ans

def center_radius(p,n):
    qr={x*x%p for x in range(p)}
    return {tuple((v-(j-u)**2)%p for j in range(n))
            for u in range(p) for v in range(p)
            if all((v-(j-u)**2)%p in qr for j in range(n))}

def main():
    for p in primes(43):
        if p<5: continue
        a,b=recurrence(p,p),center_radius(p,p)
        assert a==b
        assert len(a)==(p if p%4==1 else 0)
        if p%4==1:
            assert all(x.count(0)==1 for x in a)
        print("p",p,"full_period",len(a))
    for p,yes,no in [(7,5,6),(11,6,7),(19,9,10),(23,8,9),(31,10,11)]:
        a=recurrence(p,yes)
        assert a==center_radius(p,yes) and a
        assert not recurrence(p,no) and not center_radius(p,no)
        print("p",p,"allowed",yes,len(a),"forbidden",no,0)
    qr9={x*x%9 for x in range(9)}
    for d in (1,2,4,5,7,8):
        assert not [(A,L) for A in range(9) for L in range(9)
                    if all((A+L*j-4*d*d*j*j)%9 in qr9 for j in range(5))]
    print("mod9 six units: 0/81 each; PASS")

if __name__=="__main__":
    main()
