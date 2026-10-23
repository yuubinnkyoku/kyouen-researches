#!/usr/bin/env python3
"""Independent Python 3x3 determinant shared-D4 52-leaf terminal verifier."""
import sys
from pathlib import Path
from itertools import combinations
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'n11-four-s8-joint-terminal52-20261023'))
from terminal_geometry import circle, points, legal, safe
from fastgeom import canonical

def prep(m):
    if not (m.bit_count()==10 and safe(m) and canonical(m)==m):raise ValueError("invalid S10 key")
    base=points(m)
    moves=legal(m)
    n=len(moves)
    bad=[]
    for i,j in combinations(range(n),2):
        if any(circle(a,b,moves[i],moves[j]) for a,b in combinations(base,2)):
            bad.append((1<<i)|(1<<j))
    for i,j,k in combinations(range(n),3):
        mask=(1<<i)|(1<<j)|(1<<k)
        if any(mask & b == b for b in bad): continue
        if any(circle(a,moves[i],moves[j],moves[k]) for a in base): bad.append(mask)
    for ids in combinations(range(n),4):
        mask=sum(1<<i for i in ids)
        if any(mask & b == b for b in bad):continue
        if circle(*(moves[i] for i in ids)):bad.append(mask)
    ban_by=[[] for _ in range(n)]
    for b in bad:
        for i in range(n):
            if b>>i&1:ban_by[i].append(b^(1<<i))
    pair=[sum(sub.bit_count()==1 for sub in ban_by[i]) for i in range(n)]
    triple=[sum(sub.bit_count()==2 for sub in ban_by[i]) for i in range(n)]
    quad=[sum(sub.bit_count()==3 for sub in ban_by[i]) for i in range(n)]
    order=sorted(range(n),key=lambda i:(-(100000*pair[i]+1000*triple[i]+quad[i]),moves[i]))
    return moves,ban_by,order

def run(path):
    keys=[int(s,16) for s in Path(path).read_text().splitlines()]
    if not (len(keys)==52 and len(set(keys))==52):raise ValueError("52 distinct keys required")
    if len(sys.argv)>2 and sys.argv[2]=="reverse":keys.reverse()
    memo={};lookups=0;hits=0;edges=0;total_separate=0
    separate="separate" in sys.argv[2:]
    for m in keys:
        moves,ban_by,order=prep(m)
        def solve(state,board):
            nonlocal lookups,hits,edges
            key=canonical(board)
            lookups+=1
            if key in memo:
                hits+=1
                return memo[key]
            for i in order:
                bit=1<<i
                if state&bit or any(state&sub==sub for sub in ban_by[i]):continue
                edges+=1
                if not solve(state|bit,board|(1<<moves[i])):
                    memo[key]=True
                    return True
            memo[key]=False
            return False
        if solve(0,m):raise ValueError(f'LOSS conflict at {m:032x}')
        if separate:
            total_separate+=len(memo)
            memo.clear()
    print(dict(result='PASS',roots=len(keys),states=(total_separate if separate else len(memo)),lookups=lookups,hits=hits,edges=edges))
if __name__=='__main__':run(sys.argv[1])
