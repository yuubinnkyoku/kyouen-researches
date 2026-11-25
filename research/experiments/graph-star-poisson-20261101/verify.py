#!/usr/bin/env python3
"""Direct hypergraph maximal-state checks for critical Poisson terminal defects."""
from collections import Counter
from math import comb, exp
from fractions import Fraction

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


def finite_bip_hist(a, b, r):
    """Independent coefficient extraction from the complete terminal polynomial."""
    n = 1+a+b+r*a*b
    s = n-a*b
    hist = Counter()
    for h in (n-1, n-a, n-b):
        hist[Fraction(h-s, a-1)] += 1
    for i in range(1, a+1):
        for j in range(1, b+1):
            h = n-a-b+i+j-i*j
            hist[Fraction(h-s, a-1)] += comb(a, i)*comb(b, j)*r**(i*j)
    return hist


def finite_clique_hist(h, L, r):
    """Independent polynomial convolution, not a dominant-family formula."""
    e = comb(h, 2)
    n = 1+L*h+r*L*e
    s = n-L*e
    terms = {0: 1}
    for _ in range(L):
        nxt = Counter()
        for degree, weight in terms.items():
            for j in range(1, h+1):
                nxt[degree+j-comb(j, 2)] += (
                    weight*comb(h, j)*r**comb(j, 2))
        terms = nxt
    hist = Counter({Fraction(n-1-s, h-2): 1})
    for degree, weight in terms.items():
        hist[Fraction(n-L*h+degree-s, h-2)] += weight
    return hist


def tv_binomial(hist, n, p):
    """Exact rational total-variation distance, including nonintegral defects."""
    total = sum(hist.values())
    binomial = {Fraction(k): Fraction(comb(n, k))*p**k*(1-p)**(n-k)
                for k in range(n+1)}
    return sum(abs(Fraction(hist.get(k, 0), total)-binomial.get(k, 0))
               for k in set(hist) | set(binomial))/2


def check_finite_error_bounds():
    """Check the new bounds without using Poisson floating-point approximations."""
    checked_bip = checked_clique = 0
    for a in range(2, 8):
        for b in range(a, 26):
            for r in (2, 3, 4):
                T, D = bip_counts(a, b, r)
                x = Fraction(1, r**a)
                A = (1+x)**b
                E = Fraction(b+2)*(Fraction(3, 4)**b)
                delta = Fraction(T-D, T)
                assert delta <= (E+x**b)/(A-x**b)
                checked_bip += 1
    for h in range(3, 11):
        for L in range(1, 12):
            for r in (2, 3, 4):
                T, D = clique_counts(h, L, r)
                e = comb(h, 2)
                a = Fraction(h, r**(h-1))
                eta_star = Fraction(2**h, r**(2*h-3))
                delta = Fraction(T-D, T)
                bound = Fraction(1, r**(L*e)) + (
                    1+eta_star/(1+a))**L-1
                assert delta <= bound
                checked_clique += 1
    tv_bip = tv_clique = 0
    for a in range(2, 6):
        for b in range(a, 10):
            for r in (2, 3):
                hist = finite_bip_hist(a, b, r)
                T, D = bip_counts(a, b, r)
                assert sum(hist.values()) == T
                x = Fraction(1, r**a)
                p = x/(1+x)
                assert tv_binomial(hist, b, p) <= Fraction(T-D, T)+p**b
                tv_bip += 1
    for h in range(3, 8):
        for L in range(1, 6):
            for r in (2, 3):
                hist = finite_clique_hist(h, L, r)
                T, D = clique_counts(h, L, r)
                assert sum(hist.values()) == T
                a = Fraction(h, r**(h-1))
                p = a/(1+a)
                assert tv_binomial(hist, L, p) <= Fraction(T-D, T)
                tv_clique += 1
    print("finite TV bounds:", checked_bip, "bip inequalities,",
          checked_clique, "clique inequalities,",
          tv_bip, "bip exact distributions,",
          tv_clique, "clique exact distributions")

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
    check_finite_error_bounds()
    for a,b in ((5,32),(6,64),(7,128),(8,256)):
        T,D=bip_counts(a,b,2)
        print("bip critical",a,b,"dominant",D/T,"minimum",2**(a*b)/T)
    for h,L in ((6,5),(7,9),(8,16),(9,28)):
        T,D=clique_counts(h,L,2)
        print("clique critical",h,L,"dominant",D/T,"minimum",2**(L*comb(h,2))/T)

if __name__=="__main__": main()
