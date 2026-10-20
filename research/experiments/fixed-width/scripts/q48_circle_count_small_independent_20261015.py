#!/usr/bin/env python3
"""Independent complete integer-chord enumeration on small widths."""
from math import isqrt


def count(m):
    total, types = 0, []
    for a in range(1,m):
        for b in range(1,m):
            c2=2*b*b-a*a-8
            if c2<=0: continue
            c=isqrt(c2)
            if c*c!=c2 or c>=m: continue
            d2=2*c*c-b*b-8
            if d2<=0: continue
            d=isqrt(d2)
            if d*d!=d2 or d>=m: continue
            if len({a%2,b%2,c%2,d%2})!=1: continue
            span=max(a,b,c,d)
            total+=m-span
            types.append((a,b,c,d))
    return total, types


def main():
    for m in (4,20,73,74,75,100,120,200):
        c,ts=count(m)
        expect=max(0,m-3)+2*max(0,m-73)
        assert c==expect, (m,c,expect)
        print(f'm={m}: total={c}, types={len(ts)} PASS')

if __name__ == '__main__':
    main()
