#!/usr/bin/env python3
"""Independent finite audit of heterogeneous top-h terminal spectrum.

Brute enumerator uses only the legal-move rule; predictor uses the theorem's
threshold formula and a bivariate generating-function coefficient DP.
"""
from itertools import combinations_with_replacement, product
from math import comb
from collections import defaultdict


def predicted(c, h, r):
    w = len(c)
    if sum(c[:h]) <= r:
        return {sum(c): (1, 1)}, [(sum(c), 1, 1)]
    L = max(0, r - sum(c[:h-1]))
    U = min(c[h-1], r//h)
    out = defaultdict(lambda: [0, 0])
    by_b = []
    for b in range(L, U+1):
        # coefficient y^j z^t for 0 <= j < h, t = r-h*b.
        # For physical subsets, use binomial coefficients instead of 1.
        target = r - h*b
        occ = {(0, 0): 1}
        phys = {(0, 0): 1}
        for ci in c:
            nxt, nxtphys = defaultdict(int), defaultdict(int)
            base = min(ci, b)
            for (j, t), v in occ.items():
                nxt[j, t] += v
                if ci > b and j+1 < h:
                    for delta in range(1, min(ci-b, target-t)+1):
                        nxt[j+1, t+delta] += v
            for (j, t), v in phys.items():
                nxtphys[j, t] += v * comb(ci, base)
                if ci > b and j+1 < h:
                    for delta in range(1, min(ci-b, target-t)+1):
                        nxtphys[j+1, t+delta] += v * comb(ci, b+delta)
            occ, phys = nxt, nxtphys
        n_occ = sum(v for (j,t),v in occ.items() if t == target)
        n_phys = sum(v for (j,t),v in phys.items() if t == target)
        T = r-h*b+sum(min(ci,b) for ci in c)
        out[T][0] += n_occ
        out[T][1] += n_phys
        by_b.append((T, n_occ, n_phys))
    return {k: tuple(v) for k,v in out.items()}, by_b


def brute(c,h,r):
    w = len(c)
    tally = defaultdict(lambda: [0,0])
    safe = 0
    for x in product(*(range(ci+1) for ci in c)):
        if sum(sorted(x, reverse=True)[:h]) > r:
            continue
        safe += 1
        terminal = True
        for i in range(w):
            if x[i] == c[i]:
                continue
            y = x[:i] + (x[i]+1,) + x[i+1:]
            if sum(sorted(y, reverse=True)[:h]) <= r:
                terminal = False
                break
        if terminal:
            T = sum(x)
            count = 1
            for ci,xi in zip(c,x):
                count *= comb(ci,xi)
            tally[T][0] += 1
            tally[T][1] += count
    return {k:tuple(v) for k,v in tally.items()},safe


def run():
    cases=states=terminals=physical=nontrivial=0
    examples=[]
    for w in range(1,6):
        for asc in combinations_with_replacement(range(5),w):
            c=tuple(reversed(asc))
            for h in range(1,w+1):
                for r in range(sum(c[:h])+2):
                    expected, per_b=predicted(c,h,r)
                    actual,n_safe=brute(c,h,r)
                    assert expected == actual, (c,h,r,expected,actual)
                    if sum(c[:h])>r:
                        L=max(0,r-sum(c[:h-1]))
                        U=min(c[h-1],r//h)
                        assert len(per_b)==U-L+1
                        for i in range(len(per_b)-1):
                            diff=per_b[i+1][0]-per_b[i][0]
                            assert diff==sum(ci>=L+i+1 for ci in c)-h
                        nontrivial+=1
                    cases+=1
                    states+=n_safe
                    terminals+=sum(n for n,_ in actual.values())
                    physical+=sum(n for _,n in actual.values())
    print(f'PASS cases={cases} safe_states={states} maximal_vectors={terminals} physical_maximal_sets={physical} nontrivial_cases={nontrivial}')
    for c,h,r in [((5,4,3,2,1),3,7),((5,4,3,2,1),4,8),((5,4,3,2,1),2,5)]:
        e,per_b=predicted(c,h,r)
        a,n=brute(c,h,r)
        assert e==a
        print(f'example c={c} h={h} r={r}: {per_b}; aggregated={e}')

if __name__=='__main__':
    run()

# Separate direct mex check of the all-position binary-Grundy corollary.
def audit_grundy():
    from functools import lru_cache
    checked=nonbinary=0
    for w in range(1,5):
        for asc in combinations_with_replacement(range(4),w):
            c=tuple(reversed(asc))
            for h in range(1,w+1):
                for r in range(sum(c[:h])+2):
                    spec,_=predicted(c,h,r)
                    parity={T%2 for T in spec}
                    @lru_cache(None)
                    def grundy(x):
                        children=set()
                        for i in range(w):
                            if x[i]<c[i]:
                                y=x[:i]+(x[i]+1,)+x[i+1:]
                                if sum(sorted(y,reverse=True)[:h])<=r:
                                    children.add(grundy(y))
                        g=0
                        while g in children:
                            g+=1
                        return g
                    gs=[]
                    for x in product(*(range(ci+1) for ci in c)):
                        if sum(sorted(x,reverse=True)[:h])<=r:
                            g=grundy(x)
                            gs.append(g)
                            if len(parity)==1:
                                assert g==(next(iter(parity))-sum(x))%2,(c,h,r,x,g)
                    if len(parity)>1:
                        assert max(gs)>=2,(c,h,r)
                        nonbinary+=1
                    else:
                        assert max(gs)<=1,(c,h,r)
                    checked+=1
    print(f'PASS direct_mex_conditions={checked} mixed_parity_nonbinary={nonbinary}')

if __name__=='__main__':
    audit_grundy()
