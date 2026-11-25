#!/usr/bin/env python3
"""Independent exact determinant audit of the three-row, three-column 5-circle theorem."""
from itertools import combinations
from math import gcd
from functools import reduce, lru_cache
from collections import Counter
from math import comb


def circles_on_board(a, b, d):
    xs = (0, a, a + b)
    pts = tuple((x, d * r) for x in xs for r in range(3))
    seen = {}
    for p, q, r in combinations(pts, 3):
        x1, y1 = p
        x2, y2 = q
        x3, y3 = r
        u, v = x2 - x1, y2 - y1
        s, t = x3 - x1, y3 - y1
        det = u * t - s * v
        if det == 0:
            continue
        norm = lambda x, y: x*x+y*y
        z1, z2, z3 = norm(*p), norm(*q), norm(*r)
        A = -(z2-z1)*t+(z3-z1)*v
        B = -u*(z3-z1)+s*(z2-z1)
        C = -det*z1-A*x1-B*y1
        common = reduce(gcd, (abs(det), abs(A), abs(B), abs(C)))
        key = tuple((z//common)*(1 if det > 0 else -1) for z in (det, A, B, C))
        if key not in seen:
            support = frozenset((x,y) for x,y in pts if det*(x*x+y*y)+A*x+B*y+C == 0)
            seen[key] = support
    return {key: supp for key,supp in seen.items() if len(supp) >= 5}


def predicted_circles(a,b,d):
    xs=(0,a,a+b)
    candidates=[]
    if a*(a+b)==d*d:
        candidates.append((1,2,(0,2)))
    if b*(a+b)==d*d:
        candidates.append((0,1,(0,2)))
    if a*b==2*d*d:
        candidates.extend([(0,2,(0,1)),(0,2,(1,2))])
    result={}
    pts={(x,d*r) for x in xs for r in range(3)}
    for i,j,(r,s) in candidates:
        # Circle through (xi,dr),(xi,ds),(xj,dr),(xj,ds).
        A=-(xs[i]+xs[j]); B=-d*(r+s); C=xs[i]*xs[j]+d*d*r*s
        support=frozenset((x,y) for x,y in pts if x*x+y*y+A*x+B*y+C==0)
        assert len(support)==5, (a,b,d,i,j,r,s,support)
        result[(1,A,B,C)]=support
    return result


def main():
    total=0
    counts={0:0,1:0,2:0}
    for a in range(1,17):
        for b in range(1,17):
            for d in range(1,17):
                actual=circles_on_board(a,b,d)
                expected=predicted_circles(a,b,d)
                assert actual==expected, (a,b,d,actual,expected)
                assert all(len(s)==5 for s in actual.values())
                counts[len(actual)]+=1
                total+=1
    print(f'Exact determinant enumeration: {total} boards (a,b,d in 1..16)')
    print(f'Five-point circle counts: {counts}')
    print('All circle coefficients and their complete supports agree with the formula.')
    print('No six-point circle exists on any audited three-row board.')
    for a,b,d in ((1,3,2),(3,1,2),(1,2,1),(1,8,3)):
        print(f'(a,b,d)=({a},{b},{d}): {len(circles_on_board(a,b,d))} five-point circles')

if __name__=='__main__':
    main()

# Full 9-bit game verification, independent of the four-class recurrence.
def full_grundy(a,b,d):
    pts=tuple((x,d*r) for x in (0,a,a+b) for r in range(3))
    index={p:i for i,p in enumerate(pts)}
    forbidden=tuple(sum(1<<index[p] for p in support) for support in circles_on_board(a,b,d).values())
    @lru_cache(None)
    def grundy(mask):
        nxt=set()
        for j in range(9):
            if (mask>>j)&1: continue
            new=mask|(1<<j)
            if all(new&edge != edge for edge in forbidden):
                nxt.add(grundy(new))
        k=0
        while k in nxt:k+=1
        return k
    for mask in range(512):
        if all(mask&edge != edge for edge in forbidden):
            grundy(mask)
    return pts,forbidden,grundy


def reduced_two_circle(i,a,b,f):
    @lru_cache(None)
    def rec(i,a,b,f):
        nxt=set()
        for j,k,l,h in ((i+1,a,b,f),(i,a+1,b,f),(i,a,b+1,f),(i,a,b,f+1)):
            if j>2 or k>3 or l>3 or h>1 or (j==2 and (k==3 or l==3)):
                continue
            nxt.add(rec(j,k,l,h))
        g=0
        while g in nxt:g+=1
        return g
    return rec(i,a,b,f)


def verify_game():
    cases=((2,3,1), (1,3,2), (1,2,1))  # 0, 1, 2 forbidden circles
    for a,b,d in cases:
        pts,edges,grundy=full_grundy(a,b,d)
        edge_count=len(edges)
        assert edge_count in (0,1,2)
        count=0
        vals=set()
        for mask in range(512):
            if any(mask&e==e for e in edges):continue
            count+=1
            val=grundy(mask)
            vals.add(val)
            if edge_count<2:
                cap=9-edge_count
                assert val==(cap-mask.bit_count())%2
            else:
                intersection=edges[0]&edges[1]
                a_only=edges[0]&~edges[1]
                b_only=edges[1]&~edges[0]
                outside=((1<<9)-1)&~(edges[0]|edges[1])
                counts=((mask&intersection).bit_count(),(mask&a_only).bit_count(),
                        (mask&b_only).bit_count(),(mask&outside).bit_count())
                assert val==reduced_two_circle(*counts), (mask,counts,val)
        # Independent histogram via multiplicities of the reduced state classes.
        histogram=Counter()
        if edge_count==0:
            for stones in range(10):
                histogram[(9-stones)%2]+=comb(9,stones)
        elif edge_count==1:
            for inside in range(5):
                for outside_count in range(5):
                    histogram[(8-inside-outside_count)%2]+=comb(5,inside)*comb(4,outside_count)
        else:
            for i in range(3):
                for u in range(4):
                    for v in range(4):
                        for f in range(2):
                            if i==2 and (u==3 or v==3):
                                continue
                            histogram[reduced_two_circle(i,u,v,f)]+=comb(2,i)*comb(3,u)*comb(3,v)
        brute_histogram=Counter(grundy(mask) for mask in range(512) if all(mask&e!=e for e in edges))
        assert histogram==brute_histogram, (histogram,brute_histogram)
        expected_histograms={0:{0:256,1:256},1:{0:248,1:248},2:{0:160,1:160,2:81,3:81}}
        assert dict(histogram)==expected_histograms[edge_count]
        # A terminal safe set has no legal one-point extension.
        terminal=Counter()
        for mask in range(512):
            if any(mask&e==e for e in edges):
                continue
            if not any(not(mask>>j&1) and all((mask|(1<<j))&e!=e for e in edges) for j in range(9)):
                terminal[mask.bit_count()]+=1
        expected_terminal={0:{9:1},1:{8:5},2:{7:9,8:2}}
        assert dict(terminal)==expected_terminal[edge_count]
        expected_counts={0:512,1:496,2:482}
        assert count==expected_counts[edge_count]
        assert grundy(0)==(1 if edge_count in (0,2) else 0)
        print(f'Game (a,b,d)=({a},{b},{d}), forbidden={edge_count}, safe={count}, root={grundy(0)}, nimbers={sorted(vals)}, histogram={dict(sorted(histogram.items()))}, terminal={dict(sorted(terminal.items()))}')
    print('All safe subsets match the independent reduced recursion / parity theorem.')

if __name__=='__main__':
    verify_game()
