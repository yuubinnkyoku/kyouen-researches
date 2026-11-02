#!/usr/bin/env python3
"""Independent audit of vertex-cover inclusion-exclusion terminal polynomials."""
from collections import defaultdict
from itertools import combinations

def add(a,b,sign=1):
    c=defaultdict(int,a)
    for e,x in b.items(): c[e]+=sign*x
    return {e:x for e,x in c.items() if x}

def mul(a,b):
    c=defaultdict(int)
    for i,x in a.items():
        for j,y in b.items(): c[i+j]+=x*y
    return {e:x for e,x in c.items() if x}

def vertex_cover_poly(n,edges,r,cover):
    assert r>=1 and edges
    C=set(cover)
    assert len(C)==len(cover) and all(a in C or b in C for a,b in edges)
    adj=[set() for _ in range(n)]
    for a,b in edges:
        adj[a].add(b); adj[b].add(a)
    I=[v for v in range(n) if v not in C]
    C=sorted(C)
    total={}
    for bits in range(1<<len(C)):
        A={C[i] for i in range(len(C)) if bits>>i&1}
        D=set(C)-A
        U=[v for v in D if not(adj[v]&A)]
        eA=sum(a in A and b in A for a,b in edges)
        pref={-(len(D)+eA):r**eA}
        for bitsS in range(1<<len(U)):
            S={U[i] for i in range(len(U)) if bitsS>>i&1}
            part={0:1}
            for v in I:
                d=len(adj[v]&A)
                f={-d:r**d} if not(adj[v]&S) else {}
                if d>0: f=add(f,{-1:1})
                part=mul(part,f)
                if not part: break
            total=add(total,mul(pref,part),-1 if len(S)%2 else 1)
    N=1+n+r*len(edges)
    return dict(sorted(add({N-1:1},{N+e:x for e,x in total.items()}).items()))

def direct_graph(n,edges,r):
    adj=[0]*n
    for a,b in edges:
        adj[a]|=1<<b; adj[b]|=1<<a
    N=1+n+r*len(edges)
    out=defaultdict(int); out[N-1]+=1
    for X in range(1<<n):
        kept=((1<<n)-1)^X
        if any(not(adj[v]&kept) for v in range(n) if X>>v&1): continue
        e0=sum(not(X>>a&1) and not(X>>b&1) for a,b in edges)
        out[N-X.bit_count()-e0]+=r**e0
    return dict(sorted(out.items()))

def direct_hyperedges(n,edges,r):
    N=1+n+r*len(edges)
    assert N<=17
    forbidden=[]
    for j,(a,b) in enumerate(edges):
        f=1|(1<<(1+a))|(1<<(1+b))
        for t in range(r): f|=1<<(1+n+r*j+t)
        forbidden.append(f)
    out=defaultdict(int)
    for X in range(1<<N):
        if any(X&f==f for f in forbidden): continue
        if all(any(((X|(1<<i))&f)==f for f in forbidden)
               for i in range(N) if not(X>>i&1)):
            out[X.bit_count()]+=1
    return dict(sorted(out.items()))

def minimum_cover(n,edges):
    for k in range(n+1):
        for C in combinations(range(n),k):
            if all(a in C or b in C for a,b in edges): return C
    raise AssertionError

def bipartite_formula(m,r):
    from math import comb
    N=3+m+2*r*m
    out=defaultdict(int)
    out[N-1]+=1
    for j in range(m+1):
        out[N-2*m+j]+=comb(m,j)*r**(2*(m-j))
    out[N-m-1]+=2*((r+1)**m-1)
    out[N-2]+=1
    return dict(sorted(out.items()))

def main():
    graphs=multi=alt_count=hyp_count=hyp_masks=0
    for n in range(2,7):
        pairs=list(combinations(range(n),2))
        for mask in range(1,1<<len(pairs)):
            if n==6 and mask%17: continue
            edges=[p for j,p in enumerate(pairs) if mask>>j&1]
            C=minimum_cover(n,edges)
            if len(C)>3: continue
            for r in (1,2,3):
                got=vertex_cover_poly(n,edges,r,C)
                expected=direct_graph(n,edges,r)
                assert got==expected,(n,edges,r,C,got,expected)
                graphs+=1
                if len(edges)>n: multi+=1
                if n<=4 and r<=2:
                    for k in range(n+1):
                        for other in combinations(range(n),k):
                            if other==C or not all(a in other or b in other for a,b in edges): continue
                            assert vertex_cover_poly(n,edges,r,other)==expected
                            alt_count+=1
                N=1+n+r*len(edges)
                if n<=5 and N<=17 and hyp_count<100:
                    assert got==direct_hyperedges(n,edges,r)
                    hyp_count+=1; hyp_masks+=1<<N
    for m in range(1,21):
        edges=[(0,v) for v in range(2,m+2)]+[(1,v) for v in range(2,m+2)]
        for r in (1,2,3,4):
            got=vertex_cover_poly(m+2,edges,r,(0,1))
            assert got==bipartite_formula(m,r),(m,r,got)
            if m<=9: assert got==direct_graph(m+2,edges,r)
    print(f"PASS graph cases={graphs}, multicycle={multi}, alternative covers={alt_count}, "
          f"hypergraph cases={hyp_count}, hypergraph masks={hyp_masks}, K_2,m formula cases=80")
    print("K_2,3 q=4:",bipartite_formula(3,1))
    print("K_2,3 q=5:",bipartite_formula(3,2))

if __name__=="__main__": main()
