#!/usr/bin/env python3
"""Integer audit: explicit slope-9 Pell-circle counts on four rows.

Mathematical asymptotics are proved in the accompanying report, not by this test.
"""
import json

def by_pell(m):
    u, v = 1, 0
    count = 0
    terms = 0
    while True:
        u, v = 19*u+60*v, 6*u+19*v
        d = u+9*v
        if d >= m:
            break
        assert u*u-10*v*v == 1
        chords = (9*v-u, 3*u-v, 3*u+v, u+9*v)
        assert 0 < chords[0] < chords[1] < chords[2] < chords[3]
        points = [(u,0),(9*v,0),(5*v-u,1),(2*u+4*v,1),
                  (4*v-u,2),(2*u+5*v,2),(0,3),(u+9*v,3)]
        assert len(set(points)) == 8
        assert min(x for x,y in points) == 0
        assert max(x for x,y in points) == d
        for x,y in points:
            assert x*x+y*y-d*x-3*(u*v+1)*y+9*u*v == 0
        pairs = [sorted(x for x,y in points if y==i) for i in range(4)]
        assert len({sum(pair) for pair in pairs}) == 1
        products = [pair[0]*pair[1]-i*i for i,pair in enumerate(pairs)]
        assert products[0]-2*products[1]+products[2] == 0
        assert products[1]-2*products[2]+products[3] == 0
        count += 2*(m-d)
        terms += 1
    return count, terms

def by_recurrence(m):
    prev, curr, total = 1, 73, 0
    while curr < m:
        total += 2*(m-curr)
        prev, curr = curr, 38*curr-prev
    return total

def main():
    samples = (1,4,73,74,2773,2774,105301,105302,
               1000000,1000001,2000001,3000001,10**12,10**30)
    output = []
    for m in samples:
        count, terms = by_pell(m)
        assert count == by_recurrence(m)
        if m <= 1000001:
            assert count == 2*sum(max(0,m-d) for d in (73,2773,105301))
        output.append({"m":m,"slope9_circle_sets":count,"terms":terms})
    print(json.dumps({"audit":"PASS","samples":output},ensure_ascii=False,indent=2))

if __name__ == "__main__":
    main()
