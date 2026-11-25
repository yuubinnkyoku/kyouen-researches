#!/usr/bin/env python3
"""Check every selected terminal leaf with a separate Python minimax implementation."""
from pathlib import Path
from verify_core import canonical,safe,legal,next_player_wins_at_s10
B=Path(__file__).resolve().parent
rows=[line.split('\t') for line in (B/'round9_opt_cpp.tsv').read_text().splitlines()]
assert len(rows)==336
assert len(set(r[0] for r in rows))==len(rows)
for row in rows:
 h,verdict,states,moves,_=row
 b=int(h,16)
 assert b.bit_count()==10 and canonical(b)==b and safe(b)
 v,n=next_player_wins_at_s10(b)
 assert ('WIN' if v else 'LOSS')==verdict and n==int(states)
 assert len(legal(b))==int(moves)
print('PASS independent C++ vs Python',len(rows),'WIN',sum(r[1]=='WIN' for r in rows),'LOSS',sum(r[1]=='LOSS' for r in rows),'states',sum(int(r[2]) for r in rows))
