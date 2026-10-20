#!/usr/bin/env python3
"""Independent 41-leaf minimum for four specified 8-stone LOSS roots.
Recomputes ALL 595 eligible S10 candidates to terminal in pure Python.
The half-integral dual and feasible cover are checked using integers.
No MILP or C++ verdict is trusted for this certificate.
"""
from pathlib import Path
from collections import Counter
from verify_core import canonical,legal,safe,next_player_wins_at_s10
import argparse
B=Path(__file__).resolve().parent

def check(dual_path=None, cover_path=None):
 dual_path=Path(dual_path or B/'loss4_dual_halves.tsv')
 cover_path=Path(cover_path or B/'loss4_cover_selected.txt')
 roots=[int(a[1],16) for line in (B/'proof24_optimized.tsv').read_text().splitlines() if (a:=line.split('\t'))[0]=='ROOT' and a[2]=='LOSS']
 assert len(roots)==4 and len(set(roots))==4
 assert all(r.bit_count()==8 and safe(r) and canonical(r)==r for r in roots)
 s9=sorted({canonical(r|1<<p) for r in roots for p in legal(r)})
 assert len(s9)==81
 edges={s:{canonical(s|1<<p) for p in legal(s)} for s in s9}
 candidates=sorted(set().union(*edges.values()))
 assert len(candidates)==595
 rows={}
 for line in (B/'loss4_all_s10_cpp.tsv').read_text().splitlines():
  a=line.split('\t');assert len(a)==5 and a[0] not in rows
  rows[a[0]]=a
 assert set(rows)=={f'{c:032x}' for c in candidates}
 loss=set();counts=Counter();states=0
 for c in candidates:
  assert c.bit_count()==10 and canonical(c)==c and safe(c)
  w,n=next_player_wins_at_s10(c)
  a=rows[f'{c:032x}']
  assert ('WIN' if w else 'LOSS')==a[1] and n==int(a[2]) and len(legal(c))==int(a[3])
  counts['WIN' if w else 'LOSS']+=1;states+=n
  if not w:loss.add(c)
 assert counts==Counter({'WIN':402,'LOSS':193}) and states==28278
 weights={}
 for line in dual_path.read_text().splitlines():
  a=line.split('\t');assert len(a)==2
  s=int(a[0],16);assert s not in weights and a[1] in ('0','1','2')
  weights[s]=int(a[1])
 assert set(weights)==set(s9) and sum(weights.values())==81
 for c in loss:
  assert sum(weights[s] for s in s9 if c in edges[s])<=2,('dual violation',f'{c:032x}')
 selected=[int(x,16) for x in cover_path.read_text().split()]
 assert len(selected)==len(set(selected))==41 and set(selected)<=loss
 assert all(edges[s]&set(selected) for s in s9)
 # Every possible 10-stone LOSS leaf covers at most one unit of dual weight;
 # total 40.5 units forces >=ceil(40.5)=41 leaves. 41 exist.
 print('PASS 4 S8 LOSS; 81 S9; 595 S10 (402 WIN,193 LOSS); 28,278 states; dual 81/2; 41-leaf global minimum')

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--dual');ap.add_argument('--cover')
 args=ap.parse_args();check(args.dual,args.cover)
