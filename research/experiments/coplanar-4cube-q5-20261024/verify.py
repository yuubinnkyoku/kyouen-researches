#!/usr/bin/env python3
"""Exact 4D binary-cube hyperplane game enumeration."""
from collections import Counter
from itertools import combinations, permutations, product
def det4(a):
    z=0
    for p in permutations(range(4)):
        inv=sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
        v=(-1)**inv
        for i in range(4): v*=a[i][p[i]]
        z+=v
    return z
def independent5(ids,pts):
    b=pts[ids[0]]
    return det4([[pts[ids[j]][i]-b[i] for j in range(1,5)] for i in range(4)])!=0
def bits(m):
    while m:
        b=m&-m
        yield b
        m^=b
def main():
    pts=list(product(range(2),repeat=4))
    bad={sum(1<<x for x in ids) for ids in combinations(range(16),5)
         if not independent5(ids,pts)}
    N=1<<16
    safe=bytearray(N)
    for m in range(N):
        n=m.bit_count()
        if n<5: safe[m]=1
        elif n==5: safe[m]=int(m not in bad)
        else: safe[m]=int(all(safe[m^b] for b in bits(m)))
    g=[0]*N;h=[0]*N;terminal=Counter();four=[];hist=Counter()
    for m in sorted((i for i in range(N) if safe[i]),key=int.bit_count,reverse=True):
        ch=[m|(1<<i) for i in range(16) if not (m>>i)&1 and safe[m|(1<<i)]]
        if not ch:
            terminal[m.bit_count()]+=1;h[m]=1
            if m.bit_count()==4: four.append(m)
        else:
            a={g[t] for t in ch}
            while g[m] in a:g[m]+=1
            a={h[t] for t in ch}
            while h[m] in a:h[m]+=1
        hist[g[m]]+=1
    rect=set();support=Counter()
    for a in range(16):
        for A in range(1,16):
            for B in range(1,16):
                if A&B:continue
                rect.add(sum(1<<x for x in (a,a^A,a^B,a^A^B)))
                support[tuple(sorted((A.bit_count(),B.bit_count())))]+=1
    support={k:v//8 for k,v in support.items()}
    assert len(bad)==1360 and sum(safe)==6613
    assert terminal==Counter({4:100,6:1088})
    assert set(four)==rect and len(rect)==100
    assert support=={(1,1):24,(1,2):48,(1,3):16,(2,2):12}
    assert all(g[m]==m.bit_count()%2 and h[m]==1-m.bit_count()%2
               for m in range(N) if safe[m])
    print("forbidden_5",len(bad),"safe",sum(safe))
    print("maximal",sorted(terminal.items()),"root",g[0],h[0])
    print("grundy_histogram",sorted(hist.items()))
    print("first_move_gh",sorted(Counter((g[1<<i],h[1<<i])
                                        for i in range(16)).items()))
    print("rectangles_by_support",sorted(support.items()))
if __name__=="__main__":main()
