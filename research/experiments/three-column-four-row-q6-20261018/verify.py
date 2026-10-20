#!/usr/bin/env python3
"""Independent exact geometry and complete Grundy audit for anisotropic 3x4 q=6."""
from collections import Counter
from itertools import combinations, product

ALL=(1<<12)-1
SIX=tuple(combinations(range(12),6))

def determinant(m):
    n=len(m)
    if n==1:return m[0][0]
    # Bareiss exact determinant
    a=[list(r) for r in m]
    sign=1; prev=1
    for k in range(n-1):
        if a[k][k]==0:
            i=next((i for i in range(k+1,n) if a[i][k]),None)
            if i is None:return 0
            a[k],a[i]=a[i],a[k];sign=-sign
        piv=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                v=a[i][j]*piv-a[i][k]*a[k][j]
                assert v%prev==0
                a[i][j]=v//prev
            a[i][k]=0
        prev=piv
    return sign*a[-1][-1]

def direct(a,b,d):
    pts=[(x,d*y) for x in (0,a,a+b) for y in range(4)]
    edges=set()
    for ids in SIX:
        p=[pts[i] for i in ids]
        if sorted(Counter(x for x,y in p).values()) != [2,2,2]:continue
        if determinant([[x*x+y*y,x,y,1] for x,y in p[:4]])==0:
            # test rank of all 4x4 minors = 0. Note first 4 could be collinear, but
            # all minors vanishing suffices, and for 2/column there are noncollinear triples.
            if all(determinant([[x*x+y*y,x,y,1] for x,y in (p[i] for i in ix)])==0
                   for ix in combinations(range(6),4)):
                edges.add(sum(1<<i for i in ids))
    return frozenset(edges)

def symbolic(a,b,d):
    # All 6-point circles must have pairs summing to 3: (0,3) with product 0,
    # or (1,2) with product 2. The other sums have only one pair each.
    pairs=((0,3),(1,2))
    out=set()
    for p0,p1,p2 in product(pairs,repeat=3):
        P0,P1,P2=(p[0]*p[1] for p in (p0,p1,p2))
        if a*b*(a+b)!=d*d*(a*(P2-P1)+b*(P0-P1)):continue
        out.add(sum(1<<(4*i+y) for i,p in enumerate((p0,p1,p2)) for y in p))
    return frozenset(out)

def classify(a,b,d):
    aa=a*(a+b)==2*d*d
    bb=b*(a+b)==2*d*d
    ab=a*b==2*d*d
    if aa and bb:return 'two_overlapping_sixes'
    if aa or bb or ab:return 'one_six'
    return 'none'

def game(edges):
    ok=bytearray(1 if all(mask&e!=e for e in edges) else 0 for mask in range(4096))
    g=bytearray(4096)
    for mask in range(4095,-1,-1):
        if not ok[mask]:continue
        nxt={g[mask|1<<i] for i in range(12) if not (mask>>i)&1 and ok[mask|1<<i]}
        while g[mask] in nxt:g[mask]+=1
    maximal=Counter()
    for mask in range(4096):
        if ok[mask] and not any(not mask>>i&1 and ok[mask|1<<i] for i in range(12)):
            maximal[mask.bit_count()]+=1
    return {'edges':len(edges),'safe':sum(ok),'root':g[0],
            'first_values':dict(sorted(Counter(g[1<<i] for i in range(12)).items())),
            'histogram':dict(sorted(Counter(g[mask] for mask in range(4096) if ok[mask]).items())),
            'maximal':dict(sorted(maximal.items())),'max_grundy':max(g)}

def audit(bound=16):
    reps={'none':(1,10,1),'one_six':(1,7,2),'two_overlapping_sixes':(1,1,1)}
    result={}
    for name,(a,b,d) in reps.items():
        e=symbolic(a,b,d)
        assert e==direct(a,b,d),(name,e,direct(a,b,d))
        result[name]=game(e)
        if name=='two_overlapping_sixes':
            u,v=tuple(e)
            assert (u&v).bit_count()==2
    seen=Counter()
    for a,b,d in product(range(1,bound+1),repeat=3):
        sym=symbolic(a,b,d)
        geom=direct(a,b,d)
        assert sym==geom,(a,b,d,sym,geom)
        name=classify(a,b,d)
        seen[name]+=1
        assert len(sym)==result[name]['edges'],(a,b,d,name)
        if len(sym)==2:
            u,v=tuple(sym)
            assert (u&v).bit_count()==2,(a,b,d)
    return {'bound':bound,'audited':bound**3,'types':dict(seen),'profiles':result}

if __name__=='__main__':
    import json,sys
    n=int(sys.argv[1]) if len(sys.argv)>1 else 16
    print(json.dumps(audit(n),ensure_ascii=False,indent=2))
