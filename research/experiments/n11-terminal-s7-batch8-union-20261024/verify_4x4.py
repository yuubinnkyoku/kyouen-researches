#!/usr/bin/env python3
"""Independent 4x4 Bareiss recheck of eight archived S9 WIN certificates."""
from pathlib import Path
from itertools import combinations
import sys
HERE = Path(__file__).resolve().parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / 'n11-s8-targeted-closure-20261015'))
import verify_terminal_independent as g
ROOTS = [
'00000000000000203802000000304020','00000000000000821080000002140024',
'00000000000000c21080040020100020','00000000000101001401010102000080',
'00000000021080401004041000000004','00000000100010841200000010050000',
'00000100100002001042100000800010','00000180100000001042100000004080']
COUNTS=[16,20,20,21,17,24,10,15]
STATES=[1410,2273,2095,2686,1520,5336,89,426]
def verify():
    union=set()
    total=0
    for root,count,expected in zip(ROOTS,COUNTS,STATES):
        p=EXP/'n11-s9-batch-terminal-20261018'/'certificates'/('s9-win-'+root+'.cert')
        lines=p.read_text(encoding='ascii').strip().splitlines()
        assert len(lines)==count+5
        assert lines[:4]==['# n11-S9-WIN-terminal-v1','BOARD 11',
                           'S9 '+root,'S10_WIN_LEAVES '+str(count)]
        assert lines[-1]=='END'
        assert all(x.startswith('LEAF ') and len(x)==37 for x in lines[4:-1])
        keys=[x[5:] for x in lines[4:-1]]
        assert len(keys)==len(set(keys))==count
        b=int(root,16)
        assert len(g.points(b))==9 and g.canonical(b)==b
        assert all(not g.forbidden(*q) for q in combinations(g.points(b),4))
        assert {int(h,16) for h in keys}==g.children(b)
        states=0
        for h in keys:
            m=int(h,16)
            assert len(g.points(m))==10 and g.canonical(m)==m
            assert all(not g.forbidden(*q) for q in combinations(g.points(m),4))
            outcome,visited,_=g.solve10(m)
            assert outcome, 'false WIN10 '+h
            states+=visited
            union.add(h)
        assert states==expected,(root,states,expected)
        total+=states
    assert len(union)==143 and total==15835
    print('PASS 8 S9 WIN; 143 S10 WIN; 4x4 states=15835; empty=UNKNOWN')
if __name__=='__main__':
    verify()
