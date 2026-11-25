#!/usr/bin/env python3
"""Exhaustive finite check for Grundy values at capacity slack exactly 2.

Abstract game: sorted occupancy vector x_1>=...>=x_w, 0<=x_i<=m,
safe iff sum(x[:h])<=r. A move increments one coordinate and resorts.
"""
from functools import lru_cache
from itertools import combinations_with_replacement
import json

def solve(w,h,m,r):
    @lru_cache(None)
    def grundy(x):
        child=set()
        for i,a in enumerate(x):
            if a==m:
                continue
            y=list(x); y[i]+=1; y=tuple(sorted(y, reverse=True))
            if sum(y[:h])<=r:
                child.add(grundy(y))
        g=0
        while g in child:
            g+=1
        return g
    count=0; hist={}
    for asc in combinations_with_replacement(range(m+1),w):
        x=tuple(reversed(asc))
        if sum(x[:h])<=r and r-sum(x[:h])==2:
            g=grundy(x)
            count+=1
            hist[str(g)]=hist.get(str(g),0)+1
    return count,hist

def main():
    total=0; hist={}
    rows=[]
    # New extension beyond the earlier w<=8 checks: full w=9,m=9 sweep.
    for h in range(2,9):
        for r in range(2,9*h):
            n,hh=solve(9,h,9,r)
            total+=n
            for g,c in hh.items(): hist[g]=hist.get(g,0)+c
            rows.append({"h":h,"r":r,"states":n,"grundy_histogram":hh})
    out={"game":"sorted capacity game","w":9,"m":9,"h_range":[2,8],
         "r_range":"all integers 2 <= r < 9h","capacity_slack":2,
         "states_checked":total,"grundy_histogram":hist,
         "max_grundy":max(map(int,hist)) if hist else None,
         "counterexamples_g_ge_2":sum(c for g,c in hist.items() if int(g)>=2),
         "rows":rows}
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
