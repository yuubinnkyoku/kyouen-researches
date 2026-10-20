#!/usr/bin/env python3
"""Check every S10 child of four S8 LOSS roots, independently of C++."""
from pathlib import Path
from verify_core import canonical,safe,legal,next_player_wins_at_s10
B=Path(__file__).resolve().parent
roots=[int(a[1],16) for line in (B/'proof24_optimized.tsv').read_text().splitlines() if (a:=line.split('\t'))[0]=='ROOT' and a[2]=='LOSS']
assert len(roots)==4
s9={canonical(r|1<<p) for r in roots for p in legal(r)}
s10={canonical(s|1<<p) for s in s9 for p in legal(s)}
assert len(s9)==81 and len(s10)==595
rows=[line.split('\t') for line in (B/'loss4_all_s10_cpp.tsv').read_text().splitlines()]
assert len(rows)==595 and set(a[0] for a in rows)=={f'{x:032x}' for x in s10}
w=l=states=0
for a in rows:
 assert len(a)==5
 p=int(a[0],16)
 assert p.bit_count()==10 and canonical(p)==p and safe(p)
 win,n=next_player_wins_at_s10(p)
 assert ('WIN' if win else 'LOSS')==a[1] and n==int(a[2]),('mismatch',a)
 assert len(legal(p))==int(a[3]),('legal count mismatch',a)
 w+=win;l+=not win;states+=n
assert (w,l,states)==(402,193,28278)
print('PASS loss4 full independent S10 boundary: roots=595 WIN=402 LOSS=193 states=28278; 0 conflicts')
