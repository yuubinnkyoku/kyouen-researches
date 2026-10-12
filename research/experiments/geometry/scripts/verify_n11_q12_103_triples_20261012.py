#!/usr/bin/env python3
"""Exact 103-stone terminal configurations and 3-first-move obstruction, 11x11 q=12.

Only Python standard library; independent full enumeration and private-circle DP.
"""
from collections import defaultdict
from itertools import combinations, product
from math import gcd
from functools import reduce

N=11
POINTS=[(x,y) for y in range(N) for x in range(N)]
FULL21=(1<<21)-1

def center_circles():
    result=set()
    for cx in range(2*N-1):
        for cy in range(2*N-1):
            by_radius=defaultdict(int)
            for p,(x,y) in enumerate(POINTS):
                by_radius[(2*x-cx)**2+(2*y-cy)**2] |= 1<<p
            result.update(mask for mask in by_radius.values() if mask.bit_count()>=12)
    return sorted(result)

def triple_circles():
    groups=defaultdict(int)
    for i,j,k in combinations(range(N*N),3):
        ax,ay=POINTS[i];bx,by=POINTS[j];cx,cy=POINTS[k]
        ux,uy,vx,vy=bx-ax,by-ay,cx-ax,cy-ay
        det=ux*vy-vx*uy
        if not det:continue
        p=bx*bx+by*by-ax*ax-ay*ay
        q=cx*cx+cy*cy-ax*ax-ay*ay
        b=uy*q-p*vy;c=vx*p-ux*q
        d=-det*(ax*ax+ay*ay)-b*ax-c*ay
        vals=(det,b,c,d)
        g=reduce(gcd,map(abs,vals))
        vals=tuple(v//g for v in vals)
        if vals[0]<0:vals=tuple(-v for v in vals)
        groups[vals] |= (1<<i)|(1<<j)|(1<<k)
    return set(m for m in groups.values() if m.bit_count()>=12)

def private_subsets(circles):
    inc=[sum(1<<e for e,c in enumerate(circles) if c>>p&1) for p in range(N*N)]
    candidates=[]
    for omitted in combinations(range(21),3):
        selected=FULL21^sum(1<<e for e in omitted)
        exclusive={e:[] for e in range(21) if selected>>e&1}
        for p,mask in enumerate(inc):
            hit=mask&selected
            if hit and hit.bit_count()==1:
                exclusive[hit.bit_length()-1].append(p)
        if all(exclusive.values()):
            candidates.append((omitted,tuple(tuple(v) for v in exclusive.values())))
    return inc,candidates

def enumerate_covers(inc,candidates):
    covers=set();assignments=0
    for omitted,groups in candidates:
        for chosen in product(*groups):
            assignments+=1
            mask=0;hits=0
            for p in chosen:
                mask|=1<<p;hits|=inc[p]
            if hits==FULL21:covers.add(mask)
    return covers,assignments

def all_triple_obstructions(covers):
    n=len(covers)
    removed=[bytearray((n+7)//8) for _ in range(N*N)]
    for i,mask in enumerate(covers):
        while mask:
            bit=mask&-mask; p=bit.bit_length()-1;mask-=bit
            removed[p][i>>3] |=1<<(i&7)
    removed=[int.from_bytes(row,'little') for row in removed]
    all_configs=(1<<n)-1
    return {(i,j,k) for i in range(N*N) for j in range(i+1,N*N)
            for k in range(j+1,N*N)
            if removed[i]|removed[j]|removed[k]==all_configs}

def possible_dp(triple,inc,candidates):
    excluded=set(triple)
    for omitted,groups in candidates:
        reachable={0}
        for group in groups:
            masks={sum(1<<t for t,e in enumerate(omitted) if inc[p]>>e&1)
                   for p in group if p not in excluded}
            if not masks:break
            reachable={a|b for a in reachable for b in masks}
        else:
            if 7 in reachable:return True
    return False

def orbit(triple):
    coords=[POINTS[p] for p in triple]
    images=set()
    for t in range(8):
        transformed=[((x,y),(10-x,y),(x,10-y),(10-x,10-y),
                      (y,x),(10-y,x),(y,10-x),(10-y,10-x))[t]
                     for x,y in coords]
        images.add(tuple(sorted(N*y+x for x,y in transformed)))
    return images

def main():
    circles=center_circles()
    assert len(circles)==21 and all(c.bit_count()==12 for c in circles)
    assert set(circles)==triple_circles()
    inc,candidates=private_subsets(circles)
    assert len(candidates)==20
    covers,assignments=enumerate_covers(inc,candidates)
    assert assignments==189440
    assert len(covers)==171008
    for d in covers:
        assert d.bit_count()==18
        assert all(d&c for c in circles)
        assert all(any(d&c==1<<p for c in circles) for p in range(121) if d>>p&1)
    bad=all_triple_obstructions(covers)
    assert len(bad)==96
    seen=set();bad_orbits=[]
    for t in sorted(bad):
        if t in seen:continue
        o=orbit(t)
        assert o<=bad
        seen |=o
        bad_orbits.append((t,len(o)))
    assert len(bad_orbits)==15 and len(seen)==96
    # Independent algorithm: DP on the three non-private circles, using
    # D4 orbits of all 287,980 triples, without using the enumerated covers.
    seen=set();dp_bad=set();reps=0
    for t in combinations(range(121),3):
        if t in seen:continue
        o=orbit(t);seen|=o;reps+=1
        if not possible_dp(t,inc,candidates):dp_bad |=o
    assert len(seen)==287980 and dp_bad==bad
    print('circles=21; independent center/triple enumerations agree')
    print('private-circle subsets=20 / 1330; assignments=',assignments)
    print('103-stone maximal-safe configurations=',len(covers))
    print('three-point prefixes impossible at 103 stones=',len(bad),'/',287980)
    print('D4 orbits of impossible triples=',len(bad_orbits),'DP triple-orbit checks=',reps)
    for t,size in bad_orbits:
        print('obstruction',tuple(POINTS[p] for p in t),'orbit_size',size)
    print('PASS: exhaustive cover enumeration agrees with independent private-circle DP')
if __name__=='__main__':main()
