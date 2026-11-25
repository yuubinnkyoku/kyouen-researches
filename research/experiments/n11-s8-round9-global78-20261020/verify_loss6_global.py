#!/usr/bin/env python3
"""Independent 78-leaf global minimum proof over all legal S10 replies.

The C++ boundary TSV is checked against fresh Python minimax when FULL=1.
With FULL=0 only the finite covering arithmetic is checked, not the game verdicts.
"""
from pathlib import Path
from collections import Counter
import os
from verify_core import canonical,children,points,safe,next_player_wins_at_s10,legal
from verify_proof import parse
B=Path(__file__).resolve().parent

def check(c,why):
 if not c:raise ValueError(why)

def run(dual='loss6_dual.tsv',selection='loss6_all_cover_selected.txt',full=True):
 roots=parse(B/'round9_proof_optimized.tsv')
 lossroots=[int(b['root'],16) for b in roots if b['result']=='LOSS']
 check(len(lossroots)==6,'wrong number of LOSS roots')
 obligations=set().union(*(children(r) for r in lossroots))
 check(len(obligations)==158,'wrong S9 obligation count')
 dual_rows=[line.split('\t') for line in (B/dual).read_text().splitlines()]
 check(len(dual_rows)==158,'dual count')
 dual_weights={int(k,16):int(w) for k,w in dual_rows}
 check(len(dual_weights)==158 and set(dual_weights)==obligations,'dual keys')
 check(all(w>=0 for w in dual_weights.values()),'negative dual weight')
 check(sum(dual_weights.values())==156,'dual objective is not 78')
 all10=set().union(*(children(s9) for s9 in obligations))
 check(len(all10)==1461,'wrong boundary size')
 rows=[line.split('\t') for line in (B/'loss6_all_s10_cpp.tsv').read_text().splitlines()]
 check(len(rows)==1461 and len(set(r[0] for r in rows))==1461,'boundary rows')
 table={int(r[0],16):r for r in rows}
 check(set(table)==all10,'incomplete or extra S10 boundary')
 loss10={k for k,r in table.items() if r[1]=='LOSS'}
 check(len(loss10)==331 and len(all10-loss10)==1130,'boundary verdict count')
 for k,row in table.items():
  check(len(row)==5 and row[1] in ('WIN','LOSS'),'malformed verdict row')
  check(k.bit_count()==10 and canonical(k)==k and safe(k),'invalid S10 position')
  if full:
   w,n=next_player_wins_at_s10(k)
   check(('WIN' if w else 'LOSS')==row[1] and n==int(row[2]),'terminal mismatch')
   check(len(legal(k))==int(row[3]),'legal count mismatch')
 sel=[int(x,16) for x in (B/selection).read_text().split()]
 check(len(sel)==len(set(sel))==78,'not 78 distinct leaves')
 check(set(sel)<=loss10,'selected leaf not LOSS')
 cover={x:{canonical(x^(1<<p)) for p in points(x)}&obligations for x in loss10}
 check(set().union(*(cover[x] for x in sel))==obligations,'incomplete cover')
 for x,c in cover.items():
  check(sum(dual_weights[s] for s in c)<=2,'dual inequality violated')
 print('PASS global 78-leaf optimality: 6 S8 LOSS, 158 S9 obligations, 1461 S10 states, 331 LOSS candidates, dual sum 78, full',full)
 return True
if __name__=='__main__':run(full=os.environ.get('FULL','1')=='1')
