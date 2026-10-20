#!/usr/bin/env python3
from pathlib import Path
import sys
from verify_core import canonical,safe,legal,next_player_wins_at_s10
B=Path(__file__).resolve().parent
rows=[line.split('\t') for line in (B/'round8_s10_3975.tsv').read_text().splitlines()]
assert len(rows)==3975
start=int(sys.argv[1]);end=int(sys.argv[2]);assert 0<=start<end<=len(rows)
for h,v,n,m,_ in rows[start:end]:
 p=int(h,16);assert p.bit_count()==10 and canonical(p)==p and safe(p)
 w,states=next_player_wins_at_s10(p)
 assert ('WIN' if w else 'LOSS')==v and states==int(n) and len(legal(p))==int(m)
print('PASS prior S10',start,end)
