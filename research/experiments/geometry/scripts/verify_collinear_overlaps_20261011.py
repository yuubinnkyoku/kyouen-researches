#!/usr/bin/env python3
"""Exact line-hyperedge overlap identities, independently checked by hyperedge pairs."""
from itertools import combinations, product
from collections import Counter, defaultdict
from math import comb, gcd


def hist_formula(shape):
    hist=Counter()
    bounds=[range(1-n,n) for n in shape]
    for v in product(*bounds):
        if not any(v) or next(x for x in v if x)<0:continue
        g=0
        for x in v:g=gcd(g,abs(x))
        if g!=1:continue
        def A(k):
            out=1
            for n,x in zip(shape,v):out*=max(0,n-(k-1)*abs(x))
            return out
        for k in range(2,max(shape)+1):
            count=A(k)-2*A(k+1)+A(k+2)
            assert count>=0
            hist[k]+=count
    return +hist


def predicted(shape,q):
    hist=hist_formula(shape)
    h=sum(lines*comb(k,q) for k,lines in hist.items() if k>=q)
    overlaps={j:sum(lines*comb(k,q)*comb(q,j)*comb(k-q,q-j)//2
                    for k,lines in hist.items() if k>=2*q-j)
              for j in range(2,q)}
    # Caution: per-line term product is always even when j<q.
    return h,overlaps




def histogram_from_pairs(shape):
    """Independent exact line-length census without generating q-subsets."""
    pts=list(product(*(range(n) for n in shape)))
    lines=defaultdict(set)
    for i,j in combinations(range(len(pts)),2):
        delta=tuple(y-x for x,y in zip(pts[i],pts[j]))
        g=0
        for x in delta:g=gcd(g,abs(x))
        v=tuple(x//g for x in delta)
        if next(x for x in v if x)<0:v=tuple(-x for x in v)
        start=pts[i]
        while all(0<=a-b<n for a,b,n in zip(start,v,shape)):
            start=tuple(a-b for a,b in zip(start,v))
        lines[v,start].update((i,j))
    return dict(Counter(map(len,lines.values())))

def direct(shape,q):
    pts=list(product(*(range(n) for n in shape)))
    lines=defaultdict(set)
    for i,j in combinations(range(len(pts)),2):
        delta=tuple(y-x for x,y in zip(pts[i],pts[j]))
        g=0
        for x in delta:g=gcd(g,abs(x))
        v=tuple(x//g for x in delta)
        if next(x for x in v if x)<0:v=tuple(-x for x in v)
        start=pts[i]
        while all(0<=a-b<n for a,b,n in zip(start,v,shape)):
            start=tuple(a-b for a,b in zip(start,v))
        lines[v,start].update((i,j))
    edges=[frozenset(t) for ids in lines.values() if len(ids)>=q
           for t in combinations(sorted(ids),q)]
    assert len(edges)==len(set(edges))
    overlaps=Counter()
    for a,b in combinations(edges,2):
        j=len(a&b)
        if j>=2:overlaps[j]+=1
    return len(edges),{j:overlaps[j] for j in range(2,q)}


def main():
    cases=[((n,n),q) for n in range(2,8) for q in (3,4,5)]
    cases += [((2,3,4),q) for q in (3,4)]
    cases += [((3,3,3),q) for q in (3,4)]
    for shape,q in cases:
        a=predicted(shape,q)
        b=direct(shape,q)
        assert a==b,(shape,q,a,b)
        print('OK',shape,q,'H',a[0],'overlaps',a[1])
    print('ALL',len(cases),'cases matched')
    for q in (3,4,5,8):
        print('11x11',q,predicted((11,11),q))

if __name__=='__main__':main()

# Extra independent determinant-style audit: enumerate q-subsets rather than lines.
def direct_by_minors(shape,q):
    pts=list(product(*(range(n) for n in shape)))
    edges=[]
    for t in combinations(range(len(pts)),q):
        base=pts[t[0]]
        diff=[tuple(pts[i][c]-base[c] for c in range(len(shape))) for i in t[1:]]
        if all(a[c]*b[d]==a[d]*b[c]
               for a,b in combinations(diff,2)
               for c,d in combinations(range(len(shape)),2)):
            edges.append(set(t))
    counter=Counter(len(a&b) for a,b in combinations(edges,2))
    return len(edges),{j:counter[j] for j in range(2,q)}

if __name__=='__main__':
    independent=histogram_from_pairs((11,11))
    assert independent==dict(hist_formula((11,11)))
    assert independent=={2:2668,3:396,4:124,5:40,6:28,7:4,8:4,9:4,10:4,11:24}
    print('11x11 independent line histogram OK',dict(sorted(independent.items())))
    for shape,q in [((4,4),3),((4,4),4),((5,5),4),((6,6),4),((2,3,4),3)]:
        assert predicted(shape,q)==direct_by_minors(shape,q)
        print('minor audit OK',shape,q)
