#!/usr/bin/env python3
"""Independent cache-free S8 LOSS certificate verifier for standard 11x11."""
import sys
from pathlib import Path
import fifth_verify_standalone as geo

def verify(path):
    lines=Path(path).read_text(encoding='ascii').splitlines()
    assert lines[:3]==['# n11-S8-LOSS-batch-terminal-v1','BOARD 11','ROOTS 3']
    assert lines[-1]=='END'
    roots=set();edges={}
    for line in lines[3:-1]:
        a=line.split()
        if a[0]=='ROOT':
            assert len(a)==2 and len(a[1])==32
            m=int(a[1],16)
            assert m not in roots
            assert m.bit_count()==8 and geo.canonical(m)==m and geo.safe(m)
            roots.add(m)
        elif a[0]=='WITNESS':
            assert len(a)==3 and len(a[1])==len(a[2])==32
            s9,s10=map(lambda x:int(x,16),a[1:])
            assert s9 not in edges
            edges[s9]=s10
        else:raise AssertionError('bad record')
    assert len(roots)==3
    required=set.union(*(geo.children(s8) for s8 in roots))
    assert edges.keys()==required
    leaves={}
    for s9,s10 in edges.items():
        assert s9.bit_count()==9 and geo.canonical(s9)==s9 and geo.safe(s9)
        assert s10.bit_count()==10 and geo.canonical(s10)==s10 and geo.safe(s10)
        assert s10 in geo.children(s9)
        if s10 not in leaves:
            is_loss,states,moves=geo.terminal_s10(s10)
            assert is_loss,f'S10 WIN {s10:032x}'
            leaves[s10]=(states,moves)
    print('PASS S8 LOSS',len(roots),'S9 obligations',len(edges),'S10 LOSS',len(leaves),'states',sum(s for s,m in leaves.values()))
    return leaves

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: verify_s8_loss_batch_python.py certificate')
    verify(sys.argv[1])
