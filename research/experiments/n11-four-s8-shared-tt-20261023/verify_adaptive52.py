#!/usr/bin/env python3
"""Independent Python/3x3-integer-geometry check of per-leaf ordered S10 LOSS certificate."""
import sys
from pathlib import Path
from verify_shared52 import prep
from fastgeom import canonical

def run(keys_file, schedule_file):
    keys=[int(s,16) for s in Path(keys_file).read_text().split()]
    assert len(keys)==len(set(keys))==52
    rows=[]
    for line in Path(schedule_file).read_text().splitlines():
        key,*w=line.split()
        assert len(w)==4
        rows.append((int(key,16),tuple(map(int,w))))
    assert len(rows)==52 and [x for x,_ in rows]==keys[::-1], 'schedule must match 52 leaves in reverse order'
    memo={};lookups=hits=edges=0
    for m,weight in rows:
        moves,ban_by,_=prep(m)
        def priority(i):
            pair=sum(sub.bit_count()==1 for sub in ban_by[i])
            triple=sum(sub.bit_count()==2 for sub in ban_by[i])
            quad=sum(sub.bit_count()==3 for sub in ban_by[i])
            dist=abs(moves[i]%11-5)+abs(moves[i]//11-5)
            return weight[0]*pair+weight[1]*triple+weight[2]*quad+weight[3]*dist
        order=sorted(range(len(moves)),key=lambda i:(-priority(i),moves[i]))
        def solve(mask,board):
            nonlocal lookups,hits,edges
            key=canonical(board)
            lookups+=1
            if key in memo:
                hits+=1
                return memo[key]
            for i in order:
                bit=1<<i
                if mask&bit or any(mask&sub==sub for sub in ban_by[i]):
                    continue
                edges+=1
                if not solve(mask|bit,board|(1<<moves[i])):
                    memo[key]=True
                    return True
            memo[key]=False
            return False
        assert not solve(0,m),f'LOSS conflict at {m:032x}'
    assert (len(memo),lookups,hits,edges)==(6563,10944,4381,10892), (len(memo),lookups,hits,edges)
    print('PASS',{'roots':52,'states':len(memo),'lookups':lookups,'hits':hits,'edges':edges})
if __name__=='__main__':
    assert len(sys.argv)==3
    run(sys.argv[1],sys.argv[2])
