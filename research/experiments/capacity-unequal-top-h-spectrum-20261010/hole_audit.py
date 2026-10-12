#!/usr/bin/env python3
"""Independent brute-force audit of terminal-length gap formula for top-h capacity games.
No terminal-spectrum formula is used in the brute-force side.
"""
from itertools import combinations_with_replacement, product

def brute_lengths(c,h,r):
    lengths=set()
    nstates=0
    for x in product(*(range(v+1) for v in c)):
        if sum(sorted(x,reverse=True)[:h])>r:
            continue
        nstates+=1
        if not any(x[i]<c[i] and sum(sorted(x[:i]+(x[i]+1,)+x[i+1:],reverse=True)[:h])<=r for i in range(len(c))):
            lengths.add(sum(x))
    return lengths,nstates

def predicted_holes(c,h,r):
    if sum(c[:h])<=r:
        return 0,1,0,0
    L=max(0,r-sum(c[:h-1]))
    U=min(c[h-1],r//h)
    gap_count=sum(max(0,min(ci,U)-L) for ci in c[h+1:])
    distinct=1+max(0,min(c[h],U)-L) if h<len(c) else 1
    span=sum(max(0,min(ci,U)-L) for ci in c[h:])
    return gap_count,distinct,span,U-L

def main():
    cases=states=holes=nontrivial=0
    for w in range(1,7):
        for asc in combinations_with_replacement(range(5),w):
            c=tuple(reversed(asc))
            for h in range(1,w+1):
                for r in range(sum(c[:h])+2):
                    lengths,ns=brute_lengths(c,h,r)
                    actual_holes=max(lengths)-min(lengths)+1-len(lengths)
                    expected,n_distinct,span,interval=predicted_holes(c,h,r)
                    assert (actual_holes,len(lengths),max(lengths)-min(lengths))==(expected,n_distinct,span),(c,h,r,lengths,expected,n_distinct,span)
                    cases+=1; states+=ns; holes+=actual_holes
                    nontrivial+=bool(actual_holes)
    print(f'PASS cases={cases} safe_states={states} cases_with_holes={nontrivial} total_missing_lengths={holes}')
    for c,h,r in [((5,4,3,2,1),2,5),((5,4,3,2,1),3,7),((5,4,3,2,1),4,8)]:
        lengths,_=brute_lengths(c,h,r)
        print(f'example c={c} h={h} r={r}: lengths={sorted(lengths)} missing={sorted(set(range(min(lengths),max(lengths)+1))-lengths)}')
if __name__=='__main__':main()
