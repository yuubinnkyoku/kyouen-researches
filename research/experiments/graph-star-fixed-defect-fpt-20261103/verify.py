#!/usr/bin/env python3
"""FPT exact terminal coefficient via connected supports of log independence polynomial."""
from fractions import Fraction
from itertools import combinations
from collections import defaultdict
import random

def mul(a,b,d):
    z=[Fraction(0) for _ in range(d+1)]
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b[:d+1-i]):
                if y:z[i+j]+=x*y
    return z

def log_poly(p,d):
    t=p[:];t[0]-=1
    acc=[Fraction(0) for _ in range(d+1)]
    power=[Fraction(0) for _ in range(d+1)];power[0]=1
    for k in range(1,d+1):
        power=mul(power,t,d)
        if not any(power):break
        for j in range(1,d+1):acc[j]+=Fraction(1 if k%2 else -1,k)*power[j]
    return acc

def exp_poly(log,d):
    p=[Fraction(0) for _ in range(d+1)];p[0]=1
    for k in range(1,d+1):
        p[k]=sum(i*log[i]*p[k-i] for i in range(1,k+1))/k
    return p

def candidates(n,edges,d):
    adj=[set() for _ in range(n)]
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    H={v for v in range(n) if 2<=len(adj[v])<=d+1}
    seen,out=set(),[]
    for v in sorted(H):
        stack=[frozenset((v,))]
        while stack:
            B=stack.pop()
            if B in seen:continue
            seen.add(B)
            eb=sum(len(adj[v]&B) for v in B)//2
            defect=sum(len(adj[v])-1 for v in B)-eb
            if defect>d:continue
            if all(adj[v]-B for v in B):out.append((B,defect))
            if len(B)<2*d:
                nb=(set().union(*(adj[v] for v in B))&H)-B
                stack.extend(B|{v} for v in nb)
    return out,adj

def fpt_coeff(n,edges,q,d):
    r,e=q-3,len(edges)
    if e==0:return int(d==0)
    if d>e-1:return 0
    comps,adj=candidates(n,edges,d)
    L=sum(len(adj[v])==1 and len(adj[next(iter(adj[v]))])>=2 for v in range(n))
    h=sum(len(adj[v])==len(adj[w])==1 for v,w in edges)
    C=e-L-h
    base=(r+2)**h*r**C*(r+1)**L
    weights=[]
    for B,defect in comps:
        a=sum(sum(len(adj[v])==1 for v in adj[b]) for b in B)
        weights.append(Fraction(r**a,(r+1)**a)/r**(len(B)+defect))
    conflict=[set() for _ in comps]
    inverted=defaultdict(set)
    for i,(B,_) in enumerate(comps):
        for v in B:inverted[v].add(i)
    for i,(B,_) in enumerate(comps):
        near=B|set().union(*(adj[v] for v in B))
        for v in near:
            for j in inverted[v]:
                if i!=j:conflict[i].add(j);conflict[j].add(i)
    seen,connected=set(),[]
    for root in range(len(comps)):
        stack=[frozenset((root,))]
        while stack:
            S=stack.pop()
            if S in seen:continue
            seen.add(S)
            if sum(comps[i][1] for i in S)>d:continue
            connected.append(S)
            if len(S)<d:
                nb=set().union(*(conflict[i] for i in S))-S
                stack.extend(S|{v} for v in nb)
    total_log=[Fraction(0) for _ in range(d+1)]
    for S in connected:
        ids,k=sorted(S),len(S)
        contribution=[Fraction(0) for _ in range(d+1)]
        for mask in range(1<<k):
            T=[ids[j] for j in range(k) if mask>>j&1]
            poly=[Fraction(0) for _ in range(d+1)];poly[0]=1
            for mask2 in range(1,1<<len(T)):
                U=[T[j] for j in range(len(T)) if mask2>>j&1]
                if any(v in conflict[u] for u,v in combinations(U,2)):continue
                degree=sum(comps[u][1] for u in U)
                if degree<=d:
                    weight=Fraction(1)
                    for u in U:weight*=weights[u]
                    poly[degree]+=weight
            lp=log_poly(poly,d)
            sign=(-1)**(k-len(T))
            for j in range(1,d+1):contribution[j]+=sign*lp[j]
        for j in range(1,d+1):total_log[j]+=contribution[j]
    result=base*exp_poly(total_log,d)[d]+int(d==e-1)
    assert result.denominator==1,(n,edges,q,d,result)
    return int(result)

def direct_coeff(n,edges,q,d):
    r,e=q-3,len(edges)
    if e==0:return int(d==0)
    adj=[set() for _ in range(n)]
    for u,v in edges:adj[u].add(v);adj[v].add(u)
    result=int(d==e-1)
    for mask in range(1<<n):
        X={v for v in range(n) if mask>>v&1}
        if any(not adj[v]-X for v in X):continue
        R=set(range(n))-X
        er=sum(u in R and v in R for u,v in edges)
        if e-len(X)-er==d:result+=r**er
    return result

def test():
    total=0
    for n in range(1,6):
        pairs=list(combinations(range(n),2))
        for mask in range(1<<len(pairs)):
            edges=[p for i,p in enumerate(pairs) if mask>>i&1]
            if not edges:continue
            for q in (4,5,8):
                for d in range(min(3,len(edges)-1)+1):
                    a,b=fpt_coeff(n,edges,q,d),direct_coeff(n,edges,q,d)
                    assert a==b,(n,edges,q,d,a,b)
                    total+=1
    rng=random.Random(20261103)
    for n in (6,7,8):
        pairs=list(combinations(range(n),2))
        for _ in range(40):
            edges=[p for p in pairs if rng.random()<.3]
            if not edges:continue
            for q in (4,6):
                for d in range(min(3,len(edges)-1)+1):
                    a,b=fpt_coeff(n,edges,q,d),direct_coeff(n,edges,q,d)
                    assert a==b,(n,edges,q,d,a,b)
                    total+=1
    assert total==13047,total
    print("PASS",total,"exact coefficient comparisons")
if __name__=="__main__":test()
