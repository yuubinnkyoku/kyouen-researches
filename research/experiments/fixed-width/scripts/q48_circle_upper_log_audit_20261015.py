#!/usr/bin/env python3
"""Independent finite audit for the elementary O(m^2 log m) circle bound."""
from math import gcd, isqrt

def r2_direct(n):
    if n < 1: return 0
    count = 0
    for x in range(-isqrt(n), isqrt(n) + 1):
        y2 = n-x*x
        y = isqrt(y2)
        if y*y == y2:
            count += 1 if y == 0 else 2
    return count

def r2_divisors(n):
    return 4*sum((1 if d%4==1 else -1 if d%4==3 else 0)
                 for d in range(1,n+1) if n%d==0)

def chord_patterns(m):
    patterns=[]
    for b in range(3,m,2):
        for a in range(1,m,2):
            c2=2*b*b-a*a-8
            if c2<=0: continue
            c=isqrt(c2)
            if c*c!=c2 or c>=m or c%2==0: continue
            d2=2*c*c-b*b-8
            if d2<=0: continue
            d=isqrt(d2)
            if d*d==d2 and 0<d<m and d%2==1:
                patterns.append((a,b,c,d))
    return patterns

def main():
    for n in range(1,301):
        assert r2_direct(n)==r2_divisors(n), n
    for b in range(3,301,2):
        x,y=b-2,b+2
        assert gcd(x,y)==1
        assert 4*r2_direct(2*x*y)==r2_direct(x)*r2_direct(y), b
    expected={4:1,73:1,74:3,100:3,200:3,300:3}
    for m in (4,73,74,100,200,300):
        patterns=chord_patterns(m)
        assert len(patterns)==expected[m], (m,patterns)
        for a,b,c,d in patterns:
            S=max(a,b,c,d)
            F=(S*S-a*a)//4
            E=(S*S-b*b)//4-1-F
            points=[]
            for row,span in enumerate((a,b,c,d)):
                for x in ((S-span)//2,(S+span)//2):
                    assert x*x+row*row-S*x+E*row+F==0
                    points.append((x,row))
            assert len(set(points))==8
        count=sum(m-max(p) for p in patterns)
        known=max(0,m-3)+2*max(0,m-73)
        assert count==known, (m,count,known)
        upper=sum(r2_direct(2*(b*b-4)) for b in range(3,m,2))
        assert len(patterns)<=upper
        moment=sum(r2_direct(n)**2 for n in range(1,m+2))
        assert 4*upper<=moment
        print(f"m={m}: patterns={len(patterns)} circles={count} "
              f"sum_r2={upper} second_moment={moment} PASS")
    print("r2 direct/divisor identities: 300 PASS")
    print("coprime shifted-norm identity: 149 PASS")
    print("AUDIT PASS (finite only)")

if __name__=="__main__":
    main()
