#!/usr/bin/env python3
"""Direct hypergraph maximal-state checks for critical Poisson terminal defects."""
from collections import Counter
from math import comb, exp

def bip_edges(a,b,r):
    n=1+a+b+r*a*b
    edges=[]
    pos=1+a+b
    for i in range(a):
        for j in range(b):
            e=1|(1<<(1+i))|(1<<(1+a+j))
            for z in range(r): e|=1<<(pos+z)
            pos+=r
            edges.append(e)
    assert pos==n
    return n,edges

def clique_edges(h,L,r):
    n=1+L*h+r*L*comb(h,2)
    edges=[]
    pos=1+L*h
    for c in range(L):
        for i in range(h):
            for j in range(i+1,h):
                e=1|(1<<(1+c*h+i))|(1<<(1+c*h+j))
                for z in range(r): e|=1<<(pos+z)
                pos+=r
                edges.append(e)
    assert pos==n
    return n,edges

def maximal_masks(n,edges):
    full=(1<<n)-1
    for mask in range(1<<n):
        if any((mask&e)==e for e in edges): continue
        missing=full^mask
        ok=True
        while missing:
            bit=missing&-missing
            missing-=bit
            if not any(((mask|bit)&e)==e for e in edges):
                ok=False
                break
        if ok: yield mask

def check_bip(a,b,r):
    n,edges=bip_edges(a,b,r)
    s=n-a*b
    hist=Counter()
    total=0
    for mask in maximal_masks(n,edges):
        total+=1
        if (mask&1) and all(mask&(1<<(1+i)) for i in range(a)):
            k=sum(not bool(mask&(1<<(1+a+j))) for j in range(b))
            if k<b:
                assert mask.bit_count()==s+(a-1)*k
                hist[k]+=1
    expected={k:comb(b,k)*r**(a*(b-k)) for k in range(b)}
    assert hist==expected,(a,b,r,hist,expected)
    assert total==3+sum(comb(a,i)*comb(b,j)*r**(i*j)
                        for i in range(1,a+1) for j in range(1,b+1))
    return n,total,sum(hist.values())

def check_clique(h,L,r):
    n,edges=clique_edges(h,L,r)
    E=comb(h,2)
    s=n-L*E
    hist=Counter()
    total=0
    for mask in maximal_masks(n,edges):
        total+=1
        if mask&1:
            k=0
            ok=True
            for c in range(L):
                count=sum(bool(mask&(1<<(1+c*h+i))) for i in range(h))
                if count<h-1:
                    ok=False
                    break
                k+=h-count
            if ok:
                assert mask.bit_count()==s+(h-2)*k
                hist[k]+=1
    expected={k:comb(L,k)*h**k*r**(L*E-k*(h-1)) for k in range(L+1)}
    assert hist==expected,(h,L,r,hist,expected)
    W=sum(comb(h,j)*r**comb(j,2) for j in range(1,h+1))
    assert total==1+W**L
    return n,total,sum(hist.values())

def bip_counts(a,b,r):
    T=3+sum(comb(a,i)*comb(b,j)*r**(i*j)
            for i in range(1,a+1) for j in range(1,b+1))
    D=sum(comb(b,k)*r**(a*(b-k)) for k in range(b))
    assert 0<=D<=T
    return T,D

def clique_counts(h,L,r):
    E=comb(h,2)
    W=sum(comb(h,j)*r**comb(j,2) for j in range(1,h+1))
    D=sum(comb(L,k)*h**k*r**(L*E-k*(h-1)) for k in range(L+1))
    T=1+W**L
    assert 0<=D<=T
    return T,D

def main():
    cases=0
    masks=0
    for a,b,r in ((2,2,1),(2,3,1),(2,2,2),(2,3,2)):
        n,T,D=check_bip(a,b,r)
        cases+=1; masks+=1<<n
        print("bip direct",a,b,r,n,T,D)
    for h,L,r in ((3,1,1),(3,2,1),(3,1,2),(3,2,2),(4,1,1)):
        n,T,D=check_clique(h,L,r)
        cases+=1; masks+=1<<n
        print("clique direct",h,L,r,n,T,D)
    print("direct exhaustive:",cases,"cases,",masks,"masks")
    for a in range(2,9):
        for b in range(a,20):
            for r in (1,2,3): bip_counts(a,b,r)
    for h in range(3,10):
        for L in range(1,9):
            for r in (1,2,3): clique_counts(h,L,r)
    print("independent integer checks: 315 bipartite + 168 clique")
    for a,b in ((5,32),(6,64),(7,128),(8,256)):
        T,D=bip_counts(a,b,2)
        print("bip critical",a,b,"dominant",D/T,"minimum",2**(a*b)/T)
    for h,L in ((6,5),(7,9),(8,16),(9,28)):
        T,D=clique_counts(h,L,2)
        print("clique critical",h,L,"dominant",D/T,"minimum",2**(L*comb(h,2))/T)

if __name__=="__main__": main()
