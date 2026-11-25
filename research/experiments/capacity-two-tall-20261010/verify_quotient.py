#!/usr/bin/env python3
"""Independent bottom-up quotient-state audit (a,b,t) for two-tall capacities."""
from collections import Counter


def solve(r, s, k):
    def safe(a,b,t):
        z = [a,b]
        if t:
            z.append(1)
        if t>1:
            z.append(1)
        z.sort(reverse=True)
        return sum(z[:2]) <= r

    values = {}
    terminals = set()
    for total in range(r+s+k, -1, -1):
        for a in range(r+1):
            for b in range(s+1):
                t=total-a-b
                if t<0 or t>k or not safe(a,b,t):
                    continue
                children = []
                for da,db,dt,allowed in [(1,0,0,a<r),(0,1,0,b<s),(0,0,1,t<k)]:
                    if allowed and safe(a+da,b+db,t+dt):
                        children.append(values[(a+da,b+db,t+dt)])
                if not children:
                    terminals.add(total)
                mex=0
                while mex in children:
                    mex+=1
                values[(a,b,t)] = mex
                formula=(r+k-total)%2
                if (a,b,t)==(r,0,0) or (s==r and (a,b,t)==(0,r,0)):
                    formula=0
                if k%2 and ((a,b,t)==(r-1,0,0) or (s==r and (a,b,t)==(0,r-1,0))):
                    formula=2
                assert mex==formula, (r,s,k,(a,b,t),mex,formula)
    assert terminals == {r,r+k}, (r,s,k,terminals)
    return len(values), max(values.values())

if __name__=='__main__':
    tally=Counter()
    for r in range(2,21):
        for s in range(1,r+1):
            for k in range(1,17):
                n,g=solve(r,s,k)
                tally[g]+=1
                tally['states']+=n
    print('parameter_triples=',sum(tally[i] for i in (1,2)),
          'quotient_safe_states=',tally['states'],
          'max_grundy_histogram=',{i:tally[i] for i in (1,2)})
