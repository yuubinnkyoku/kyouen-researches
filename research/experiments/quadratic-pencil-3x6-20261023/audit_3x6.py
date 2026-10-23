#!/usr/bin/env python3
"""Independent exact 4x4 Leibniz determinants and memoized recursive mex.

Reads results.tsv emitted by quadratic_3x6.cpp. No reuse of its geometric
coefficient computation, forbidden masks, or bottom-up DP.
"""
from fractions import Fraction
from itertools import combinations, permutations
from functools import lru_cache
import csv, sys, json

def det4(a):
    total=0
    for p in permutations(range(4)):
        sign=(-1)**sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
        prod=1
        for i in range(4):prod*=a[i][p[i]]
        total+=sign*prod
    return total

def audit(path):
    with open(path,encoding='utf-8') as f:
        metadata=f.readline().strip()
        rows=list(csv.DictReader(f,delimiter='\t'))
    assert 'width=6 height=3 exceptions=53' in metadata
    pts=[(x,y) for x in range(6) for y in range(3)]
    exceptions={Fraction(r['lambda']) for r in rows if r['lambda']!='generic'}
    assert len(rows)==54 and len(exceptions)==53
    total=0
    for r in rows:
        lam=Fraction(1000003) if r['lambda']=='generic' else Fraction(r['lambda'])
        assert r['lambda']!='generic' or lam not in exceptions
        d=lam.denominator;n=lam.numerator
        triples=[[] for _ in pts]
        forbidden=0
        for ids in combinations(range(len(pts)),4):
            mat=[[d*x*x+n*y*y,d*x,d*y,d] for x,y in (pts[i] for i in ids)]
            if det4(mat)!=0:continue
            forbidden+=1
            for i in ids:triples[i].append(sum(1<<j for j in ids if j!=i))
        @lru_cache(None)
        def grundy(mask):
            options=set()
            for i in range(len(pts)):
                if mask>>i&1 or any((mask&t)==t for t in triples[i]):continue
                options.add(grundy(mask|(1<<i)))
            g=0
            while g in options:g+=1
            return g
        assert grundy(0)==int(r['grundy']),r['lambda']
        wins=','.join(str(i) for i in range(18) if grundy(1<<i)==0) or '-'
        assert wins==r['wins'],r['lambda']
        assert grundy.cache_info().currsize==int(r['safe']),r['lambda']
        assert forbidden==int(r['forbidden']),r['lambda']
        total+=grundy.cache_info().currsize
    return {'cases':len(rows),'exceptions':len(exceptions),'total_safe_positions':total,'independent_4x4_topdown':'PASS'}

if __name__=='__main__':
    print(json.dumps(audit(sys.argv[1]),indent=2))
