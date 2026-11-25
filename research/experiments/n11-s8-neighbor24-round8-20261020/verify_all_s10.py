#!/usr/bin/env python3
"""Independently check every S10 terminal result using Python integer geometry.
No solver result is used to shortcut a position's search.
"""
from pathlib import Path
import sys
from verify_core import canonical,safe,legal,next_player_wins_at_s10
B=Path(__file__).resolve().parent
rows=[line.split('\t') for line in (B/'all_s10_cpp.tsv').read_text().splitlines()]
assert len(rows)==3975
assert len({a[0] for a in rows})==len(rows)
start=int(sys.argv[1]) if len(sys.argv)>1 else 0
end=int(sys.argv[2]) if len(sys.argv)>2 else len(rows)
assert 0<=start<end<=len(rows)
for i in range(start,end):
 a=rows[i];assert len(a)==5
 p=int(a[0],16)
 assert p.bit_count()==10 and canonical(p)==p and safe(p)
 w,n=next_player_wins_at_s10(p)
 assert ('WIN' if w else 'LOSS')==a[1] and n==int(a[2]),('mismatch',i,a,w,n)
 assert len(legal(p))==int(a[3]),('legal count mismatch',i,a)
print('PASS independent Python S10',start,end,'roots',end-start,'states',sum(int(a[2]) for a in rows[start:end]))
