#!/usr/bin/env python3
"""All-dimensional exact q=5 binary-cube section count.

Compile q5_complete_masks.cpp, save its output to masks.txt, then run
python q5_complete.py masks.txt. No floating-point operations.
"""
from collections import Counter
from itertools import combinations, product
from math import comb, factorial
import sys
P=1009

def rank_with_ones(patterns):
    pivots={}
    for v in [31]+list(patterns):
        row=[(v>>i)&1 for i in range(5)]
        for col,basis in sorted(pivots.items()):
            if row[col]:
                t=row[col]
                row=[(a-t*b)%P for a,b in zip(row,basis)]
        col=next((j for j,x in enumerate(row) if x),None)
        if col is not None:
            t=pow(row[col],-1,P)
            pivots[col]=[(a*t)%P for a in row]
    return len(pivots)

def independent_weight_audit(masks):
    # Independent comparison, not a proof that bounded weights suffice.
    found=set()
    for w in product(range(-3,4),repeat=5):
        s=sum(w)
        if not s or any(w[i]==s and all(w[j]==0 for j in range(5) if j!=i)
                        for i in range(5)):
            continue
        m=0
        for v in range(32):
            t=sum(w[i] for i in range(5) if v>>i&1)
            if t in (0,s):m|=1<<v
        if m.bit_count()>=9 and rank_with_ones(
                v for v in range(32) if m>>v&1)==5:
            found.add(m)
    assert found==set(masks)
    print("independent integer-weight audit: 510 masks")

def uncovered(masks,k):
    # Exact inclusion-exclusion, retaining intersections of size >= k.
    coef={(1<<32)-1:1}
    for a in masks:
        if a.bit_count()<k:continue
        nxt=coef.copy()
        for old,v in coef.items():
            meet=old&a
            if meet.bit_count()>=k:
                nxt[meet]=nxt.get(meet,0)-v
        coef={m:v for m,v in nxt.items() if v}
    return sum(v*comb(m.bit_count(),k) for m,v in coef.items()),len(coef)

def good_rank_deficient(patterns):
    # Direct affine-span check on the canonical 12-pattern relation.
    k=len(patterns)
    rows=[[(v>>i)&1 for v in patterns]+[1] for i in range(5)]
    if len({tuple(r) for r in rows})!=5:return False
    piv=[];rank=0
    for col in range(k+1):
        i=next((i for i in range(rank,5) if rows[i][col]),None)
        if i is None:continue
        rows[rank],rows[i]=rows[i],rows[rank]
        t=pow(rows[rank][col],-1,P)
        rows[rank]=[x*t%P for x in rows[rank]]
        for j in range(5):
            if j!=rank:
                t=rows[j][col]
                rows[j]=[(a-t*b)%P for a,b in zip(rows[j],rows[rank])]
        piv.append(col);rank+=1
        if rank==5:break
    null=[]
    for f in range(k+1):
        if f in piv:continue
        vec=[0]*(k+1);vec[f]=1
        for i,col in enumerate(piv):vec[col]=-rows[i][f]
        null.append(vec)
    count=0
    for z in range(1<<k):
        if all((sum(x for j,x in enumerate(vec[:k]) if z>>j&1)
                +vec[k])%P==0 for vec in null):
            count+=1
            if count>5:return False
    return count==5

def deficient_correction(k):
    if k>12:return 0
    pat=[v for v in range(32) if (v&1)+((v>>1)&1)==
         ((v>>2)&1)+((v>>3)&1)]
    assert len(pat)==12
    return 15*sum(good_rank_deficient(T) for T in combinations(pat,k))

def main():
    if len(sys.argv)!=2:raise SystemExit("usage: q5_complete.py masks.txt")
    with open(sys.argv[1],encoding="ascii") as f:
        masks=[int(line) for line in f if line.strip()]
    assert len(masks)==len(set(masks))==510
    assert Counter(m.bit_count() for m in masks)=={10:280,14:105,16:85,20:10,24:30}
    independent_weight_audit(masks)
    # Audit the 15 exceptional rank-deficient containers and their overlaps.
    exceptional=[]
    for four in combinations(range(5),4):
        for plus in combinations(four,2):
            minus=tuple(i for i in four if i not in plus)
            if plus>minus:continue
            b=sum(1<<v for v in range(32)
                  if sum((v>>i)&1 for i in plus)==
                     sum((v>>i)&1 for i in minus))
            exceptional.append(b)
    assert len(set(exceptional))==15
    assert Counter((a&b).bit_count() for a,b in combinations(exceptional,2))=={
        4:60,6:30,8:15}
    for b in exceptional:
        assert any((b&~a)==0 for a in masks if a.bit_count()==24)
    for i,j in combinations(range(5),2):
        eq=sum(1<<v for v in range(32) if ((v>>i)&1)==((v>>j)&1))
        assert any((eq&~a)==0 for a in masks if a.bit_count()==24)
    print("rank-deficiency audit: 15 disjoint-at-k>=9 containers, all covered")
    g={k:0 for k in range(5)}
    g.update({5:2592,6:36304,7:329552,8:2038600})
    print("k full-rank-good deficient-good g(5,k) DP-states")
    for k in range(9,17):
        full,states=uncovered(masks,k)
        correction=deficient_correction(k)
        g[k]=full+correction
        print(k,full,correction,g[k],states)
    for k in range(17,33):
        c=lambda n:comb(n,k) if k<=n else 0
        g[k]=c(32)-30*c(24)+140*c(20)+135*c(18)
    a={j:sum((-1)**(k-j)*comb(k,j)*g[k] for k in range(j,33))
       for j in range(33)}
    expected={2:-49,4:255,6:-495,8:250,10:780,12:-1977,
              14:2205,16:-1215,18:135,20:140,24:-30,32:1}
    assert {j:v for j,v in a.items() if v}==expected
    print("exponential numerator coefficients:",expected)
    for d in range(5,16):
        n=sum(v*j**d for j,v in a.items())
        assert n%factorial(5)==0
        E=n//factorial(5)
        if d<=8:
            assert E=={5:2592,6:256704,7:18778368,8:1133185536}[d]
        print(f"E_{{{d},5}}={E}")

if __name__=="__main__":
    main()
