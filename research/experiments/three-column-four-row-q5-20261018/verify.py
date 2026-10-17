#!/usr/bin/env python3
"""Exact arithmetic and independent geometric audit of 3x4 q=5."""
import argparse
import itertools as it
import json
from collections import Counter, defaultdict
from functools import lru_cache

R = range(4)
FIVE = tuple(it.combinations(range(12), 5))

def symbolic():
    """All (2,2,1) candidate circles and chord-equation coefficients."""
    out = defaultdict(set)
    for lone in range(3):
        paircols = [i for i in range(3) if i != lone]
        for p, q in it.product(it.combinations(R, 2), repeat=2):
            if sum(p) != sum(q):
                continue
            t = sum(p)
            for y in R:
                prod = [0, 0, 0]
                prod[paircols[0]] = p[0]*p[1]
                prod[paircols[1]] = q[0]*q[1]
                prod[lone] = y*(t-y)
                mask = sum(1 << (4*paircols[0]+z) for z in p)
                mask |= sum(1 << (4*paircols[1]+z) for z in q)
                mask |= 1 << (4*lone+y)
                out[(prod[2]-prod[1], prod[0]-prod[1])].add(mask)
    return {key: frozenset(value) for key, value in out.items()}

PAT = symbolic()
COEFFS = {(-6,0),(-3,0),(-2,-2),(-2,0),(-1,-1),
          (0,-6),(0,-3),(0,-2),(0,0),(0,1),(0,2),
          (1,0),(2,0),(2,2),(3,3),(6,6)}
POS = {(0,1),(0,2),(1,0),(2,0),(2,2),(3,3),(6,6)}

def predicted(a,b,d):
    return frozenset(e for (alpha,beta),edges in PAT.items()
                     if a*b*(a+b) == d*d*(alpha*a+beta*b)
                     for e in edges)

def det3(v):
    (a,b,c),(d,e,f),(g,h,i) = v
    return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)

def independent(a,b,d):
    """Cramer-based exact circle test; no chord products or row sums."""
    points = [(x,d*y) for x in (0,a,a+b) for y in R]
    result = set()
    for indices in FIVE:
        p = [points[i] for i in indices]
        counts = Counter(x for x,y in p)
        if len(counts) != 3 or max(counts.values()) > 2:
            continue
        triple = next((t for t in it.combinations(p,3)
                       if det3([(x,y,1) for x,y in t])),None)
        if triple is None:
            continue
        D = det3([(x,y,1) for x,y in triple])
        U = -det3([(x*x+y*y,y,1) for x,y in triple])
        V = -det3([(x,x*x+y*y,1) for x,y in triple])
        W = -det3([(x,y,x*x+y*y) for x,y in triple])
        if all(D*(x*x+y*y)+U*x+V*y+W == 0 for x,y in p):
            result.add(sum(1 << i for i in indices))
    return frozenset(result)

def category(a,b,d):
    aa,bb,ab,dd = a*(a+b),b*(a+b),a*b,d*d
    if aa == bb == 2*dd:
        return 'two_six_circles'
    if ab == 2*dd:
        return 'six_plus_two_fives'
    if aa == 2*dd or bb == 2*dd:
        return 'one_six_circle'
    if aa == dd or bb == dd or ab in (3*dd,6*dd):
        return 'two_disjoint_fives'
    return 'none'

def five_subsets(mask):
    return {sum(1 << i for i in sub)
            for sub in it.combinations([i for i in range(12) if mask >> i & 1],5)}

def check_structure():
    assert set(PAT) == COEFFS
    assert {k for k in PAT if k[0]>0 or k[1]>0} == POS
    assert sum(map(len,PAT.values())) == 96
    for k in ((0,1),(1,0),(3,3),(6,6)):
        a,b = tuple(PAT[k])
        assert a & b == 0
    for k in ((0,2),(2,0)):
        u = 0
        for edge in PAT[k]:
            u |= edge
        assert u.bit_count() == 6 and PAT[k] == five_subsets(u)
    # ab=2d²: six-circle plus two disjoint five-circles.
    E = PAT[(2,2)]
    six = next(mask for mask in range(1<<12)
               if mask.bit_count()==6 and five_subsets(mask) <= E)
    p,q = tuple(E-five_subsets(six))
    assert p&q == 0 and (p&six).bit_count()==2 and (q&six).bit_count()==2
    s = []
    for k in ((0,2),(2,0)):
        union = 0
        for edge in PAT[k]:
            union |= edge
        s.append(union)
    assert (s[0]&s[1]).bit_count() == 2

def game(edges):
    ok = [all(mask&e != e for e in edges) for mask in range(4096)]
    g = [0]*4096
    for mask in range(4095,-1,-1):
        if not ok[mask]:
            continue
        children = {g[mask|(1<<i)] for i in range(12)
                    if not mask>>i&1 and ok[mask|(1<<i)]}
        while g[mask] in children:
            g[mask] += 1
    @lru_cache(None)
    def recursive(mask):
        values = {recursive(mask|(1<<i)) for i in range(12)
                  if not mask>>i&1 and ok[mask|(1<<i)]}
        z = 0
        while z in values:
            z += 1
        return z
    assert all(recursive(mask)==g[mask] for mask in range(4096) if ok[mask])
    maximal = Counter()
    for mask in range(4096):
        if ok[mask] and not any(not mask>>i&1 and ok[mask|(1<<i)]
                                for i in range(12)):
            maximal[mask.bit_count()] += 1
    return {'forbidden_fives':len(edges),'safe':sum(ok),'root':g[0],
            'first_values':sorted({g[1<<i] for i in range(12)}),
            'grundy_histogram':dict(sorted(Counter(g[i] for i in range(4096)
                                                 if ok[i]).items())),
            'maximal':dict(sorted(maximal.items()))}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bound',type=int,default=16)
    parser.add_argument('--output',default=None)
    args = parser.parse_args()
    assert args.bound >= 1
    check_structure()
    representatives = {'none':(1,10,1),'two_disjoint_fives':(1,3,2),
                       'one_six_circle':(1,7,2),
                       'six_plus_two_fives':(1,2,1),
                       'two_six_circles':(1,1,1)}
    profiles = {}
    for kind,params in representatives.items():
        assert predicted(*params) == independent(*params)
        profiles[kind] = game(predicted(*params))
        assert profiles[kind]['root'] == 0
    seen = Counter()
    for a,b,d in it.product(range(1,args.bound+1),repeat=3):
        p = predicted(a,b,d)
        assert p == independent(a,b,d), (a,b,d)
        typ = category(a,b,d)
        seen[typ] += 1
        assert len(p) == profiles[typ]['forbidden_fives'], (a,b,d,typ)
    result = {'bound':args.bound,'audited_boards':args.bound**3,
              'symbolic_candidates':sum(map(len,PAT.values())),
              'coefficient_pairs':[list(x) for x in sorted(PAT)],
              'class_counts':dict(sorted(seen.items())),
              'profiles':profiles}
    if args.output:
        with open(args.output,'w',encoding='utf-8') as f:
            json.dump(result,f,indent=2,ensure_ascii=False)
            f.write('\n')
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__ == '__main__':
    main()
