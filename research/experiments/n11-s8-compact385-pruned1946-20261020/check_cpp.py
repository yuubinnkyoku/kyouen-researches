#!/usr/bin/env python3
"""Compare C++ terminal minimax against the 1,946 required proof positions."""
from pathlib import Path
import sys
B=Path(__file__).resolve().parent
assert len(sys.argv)==2
sel=set((B/'selected385.txt').read_text().split())
win={line.split('\t')[0] for line in (B/'win_witnesses1561.tsv').read_text().splitlines()}
assert len(sel)==385 and len(win)==1561 and not sel&win
expected=(B/'terminal1946_cpp.tsv').read_bytes()
actual=Path(sys.argv[1]).read_bytes()
assert actual==expected,'C++ terminal table mismatch'
lines=actual.decode().splitlines();assert len(lines)==1946
states=0
for line in lines:
    h,v,n,m,p=line.split('\t')
    assert h in sel|win and v==('LOSS' if h in sel else 'WIN')
    if h in sel:states+=int(n)
assert states==34709
print('PASS C++ independent 1946 terminal results; 385 LOSS cost=34709 states')
