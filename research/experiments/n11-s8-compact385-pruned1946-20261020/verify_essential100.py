#!/usr/bin/env python3
"""Check 100 explicit 384-leaf adversarial covers, independent of cover search.

A 384-leaf cover here is a combinatorial *counterfactual*, NOT a game
certificate: each has a previously excluded (actual WIN) S10 state.
"""
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
import json
from verify_core import canonical,children,safe,legal,next_player_wins_at_s10
B=Path(__file__).resolve().parent
D=json.loads((B/'dual_components.json').read_text())
W={h:Fraction(v) for d in D for h,v in d['weights'].items()}
roots=(B/'loss_roots35.txt').read_text().split()
assert len(roots)==len(set(roots))==35
assert all(int(h,16).bit_count()==8 and canonical(int(h,16))==int(h,16) and safe(int(h,16)) for h in roots)
s9={f'{b:032x}' for h in roots for b in children(int(h,16))}
assert len(s9)==782
cov=defaultdict(set)
for h in s9:
 for b in children(int(h,16)):cov[f'{b:032x}'].add(h)
assert len(cov)==6446
witness={}
for line in (B/'win_witnesses1591.tsv').read_text().splitlines():
 h,p=line.split('\t');assert h not in witness;witness[h]=int(p)
assert len(witness)==1591
weight=lambda ss:sum((W.get(s,0) for s in ss),Fraction(0))
high={h for h,ss in cov.items() if weight(ss)>1}
assert len(high)==1346 and high<=witness.keys()
# Compute components by ordinary graph traversal, independently of the DFS solver.
adj={s:set() for s in s9}
for h,ss in cov.items():
 if h in high:continue
 for s in ss:adj[s].update(ss)
remaining=set(s9);components=[]
while remaining:
 start=min(remaining);stack=[start];cc={start};remaining.remove(start)
 while stack:
  for t in adj[stack.pop()]&remaining:
   remaining.remove(t);cc.add(t);stack.append(t)
 components.append(cc)
assert len(components)==12
comp=next(c for c in components if set(D[6]['weights'])<=c)
assert len(comp)==87
pos={s for s in comp if W.get(s,0)>0};zero=comp-pos
assert len(pos)==74 and len(zero)==13 and sum((W.get(s,0) for s in comp),Fraction(0))==41
optional={h for h in witness if h not in high and cov[h]<=comp}
assert len(optional)==100
chosen=(B/'selected385.txt').read_text().split()
assert len(chosen)==len(set(chosen))==385
assert set(chosen)<=cov.keys() and not set(chosen)&witness.keys()
assert set().union(*(cov[h] for h in chosen))==s9
base_comp={h for h in chosen if cov[h]<=comp}
assert len(base_comp)==42
outside=set(chosen)-base_comp
assert len(outside)==343

proof=json.loads((B/'component6_essential100.json').read_text())
assert proof['component_id']==6 and proof['base_witness_count']==1591
assert set(proof['obligations'])==comp
assert set(proof['positive'])==pos and set(proof['zero'])==zero
assert set(proof['optional_exclusions'])==optional
assert set(proof['selected41_by_restored_exclusion'])==optional
@lru_cache(None)
def check_state(h):
 b=int(h,16)
 assert b.bit_count()==10 and canonical(b)==b and safe(b)
 return True
for h,leaf_list in sorted(proof['selected41_by_restored_exclusion'].items()):
 assert len(leaf_list)==len(set(leaf_list))==41
 leaves=set(leaf_list)
 assert h in leaves and leaves<=cov.keys()
 assert all(check_state(x) and cov[x]<=comp and weight(cov[x])==1 for x in leaves)
 assert leaves&witness.keys()=={h}
 # Positive obligations are covered exactly once, zero-weight ones at least once.
 assert all(sum(s in cov[x] for x in leaves)==1 for s in pos)
 assert all(any(s in cov[x] for x in leaves) for s in zero)
 assert set().union(*(cov[x] for x in leaves))==comp
 global384=outside|leaves
 assert len(global384)==384
 assert set().union(*(cov[x] for x in global384))==s9
 # Check that the *one* reinstated column is actually WIN, so it must
 # not be interpreted as a legitimate LOSS proof leaf.
 b=int(h,16);p=witness[h]
 assert p in legal(b)
 child_win,_=next_player_wins_at_s10(b|(1<<p))
 assert child_win is False,('WIN exclusion witness failed',h)
print('PASS 100/100 independently verified 41-leaf component covers')
print('PASS 100/100 counterfactual 384-leaf global covers (343 unchanged + 41)')
print('PASS 100/100 excluded S10 states independently WIN, each with an S11 LOSS child')
print('PASS all 100 baseline optional exclusions are individually necessary to rule out these covers')
print('IMPORTANT: this does NOT prove minimum number of exclusions under alternative choices')
