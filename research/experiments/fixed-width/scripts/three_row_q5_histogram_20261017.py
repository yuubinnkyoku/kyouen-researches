#!/usr/bin/env python3
"""Exact three-column/three-row q=5 audit, independent circle determinant and mex."""
from collections import Counter
from functools import lru_cache
from itertools import combinations
from math import comb


def circles(a, b, d):
    points = [(x, d*y) for x in (0, a, a+b) for y in range(3)]
    edges = set()
    for p, q, r in combinations(range(9), 3):
        x, y = points[p]
        u, v = points[q]
        s, t = points[r]
        D = (u-x)*(t-y)-(s-x)*(v-y)
        if not D:
            continue
        E = (u*u+v*v)-(x*x+y*y)
        F = (s*s+t*t)-(x*x+y*y)
        A = -E*(t-y)+F*(v-y)
        B = -(u-x)*F+(s-x)*E
        C = -D*(x*x+y*y)-A*x-B*y
        mask = sum(1 << i for i, (xx, yy) in enumerate(points)
                   if D*(xx*xx+yy*yy)+A*xx+B*yy+C == 0)
        if mask.bit_count() >= 5:
            edges.add(mask)
    return tuple(sorted(edges))


def predicted(a, b, d):
    return (int(a*(a+b)==d*d)+int(b*(a+b)==d*d)
            +2*int(a*b==2*d*d))


def game(edges):
    @lru_cache(None)
    def g(mask):
        options = set()
        for j in range(9):
            nxt = mask | (1 << j)
            if nxt != mask and all(nxt & e != e for e in edges):
                options.add(g(nxt))
        n = 0
        while n in options:
            n += 1
        return n
    safe = [mask for mask in range(512) if all(mask&e != e for e in edges)]
    hist = Counter(g(mask) for mask in safe)
    terminal = Counter(mask.bit_count() for mask in safe if not any(
        mask & (1<<j) == 0 and all((mask | (1<<j)) & e != e for e in edges)
        for j in range(9)))
    return g(0), hist, terminal, len(safe)


def reduced_histogram():
    @lru_cache(None)
    def g(i, u, v, f):
        options = set()
        for x in ((i+1,u,v,f),(i,u+1,v,f),(i,u,v+1,f),(i,u,v,f+1)):
            j, a, b, h = x
            if j>2 or a>3 or b>3 or h>1 or (j==2 and (a==3 or b==3)):
                continue
            options.add(g(*x))
        n = 0
        while n in options:
            n += 1
        return n
    hist = Counter()
    for i in range(3):
        for u in range(4):
            for v in range(4):
                for f in range(2):
                    if i==2 and (u==3 or v==3):
                        continue
                    hist[g(i,u,v,f)] += comb(2,i)*comb(3,u)*comb(3,v)
    return hist


def main():
    seen = Counter()
    for a in range(1,17):
        for b in range(1,17):
            for d in range(1,17):
                edges = circles(a,b,d)
                assert len(edges) == predicted(a,b,d), (a,b,d,edges)
                assert all(e.bit_count() == 5 for e in edges)
                seen[len(edges)] += 1
    assert seen == {0:4048,1:24,2:24}, seen
    print('4096 exact determinant boards:', dict(sorted(seen.items())))
    cases = ((2,3,1),(1,3,2),(1,2,1))
    expected = ((1,{0:256,1:256},{9:1},512),
                (0,{0:248,1:248},{8:5},496),
                (1,{0:160,1:160,2:81,3:81},{7:9,8:2},482))
    for abc, target in zip(cases, expected):
        result = game(circles(*abc))
        assert result == target, (abc,result,target)
        print(abc, result)
    assert reduced_histogram() == expected[2][1]
    print('Reduced weighted mex and independent 9-bit enumeration agree.')

if __name__ == '__main__':
    main()
