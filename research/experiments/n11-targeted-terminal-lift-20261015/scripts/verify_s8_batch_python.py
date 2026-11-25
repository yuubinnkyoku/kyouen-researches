#!/usr/bin/env python3
"""Cache-free independent 11x11 S8 WIN batch terminal verifier."""
import sys
from pathlib import Path
from functools import lru_cache
import fifth_verify_standalone as geo

def verify(path):
    lines=Path(path).read_text(encoding='ascii').splitlines()
    assert lines[:2]==['# n11-S8-WIN-batch-terminal-v1','BOARD 11']
    assert lines[2].startswith('ROOTS ')
    expected=int(lines[2].split()[1])
    assert 0<expected<=10000
    assert lines[-1]=='END'
    edges={}
    for line in lines[3:-1]:
        tag,s8,s9=line.split()
        assert tag=='EDGE' and len(s8)==len(s9)==32
        a,b=int(s8,16),int(s9,16)
        assert a not in edges
        edges[a]=b
    assert len(edges)==expected
    terminal={}
    for a,b in edges.items():
        assert a.bit_count()==8 and geo.canonical(a)==a and geo.safe(a)
        assert b.bit_count()==9 and geo.canonical(b)==b and geo.safe(b)
        assert b in geo.children(a)
        leaves=geo.children(b)
        assert leaves
        for leaf in leaves:
            if leaf not in terminal:
                is_loss,states,moves=geo.terminal_s10(leaf)
                assert not is_loss, f'LOSS leaf {leaf:032x}'
                terminal[leaf]=(states,moves)
    assert len(set(edges.values()))>0
    print(f'PASS S8 WIN {len(edges)} S9 witnesses {len(set(edges.values()))} S10 WIN {len(terminal)} states {sum(s for s,m in terminal.values())}')
    return terminal

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: verify_s8_batch_python.py certificate')
    verify(sys.argv[1])
