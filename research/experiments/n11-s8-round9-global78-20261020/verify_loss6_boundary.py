#!/usr/bin/env python3
from pathlib import Path
import sys
from verify_core import canonical,safe,legal,next_player_wins_at_s10
B=Path(__file__).resolve().parent
rows=[line.split('\t') for line in (B/'loss6_all_s10_cpp.tsv').read_text().splitlines()]
assert len(rows)==1461
start=int(sys.argv[1]) if len(sys.argv)>1 else 0
end=int(sys.argv[2]) if len(sys.argv)>2 else len(rows)
assert 0<=start<end<=len(rows)
for i in range(start,end):
 h,v,n,m,_=rows[i]
 p=int(h,16)
 assert p.bit_count()==10 and canonical(p)==p and safe(p)
 win,states=next_player_wins_at_s10(p)
 assert ('WIN' if win else 'LOSS')==v and states==int(n),('mismatch',i,h)
 assert len(legal(p))==int(m),('move mismatch',i,h)
print('PASS full boundary',start,end,'states',sum(int(r[2]) for r in rows[start:end]),flush=True)
