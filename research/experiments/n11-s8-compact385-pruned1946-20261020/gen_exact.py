#!/usr/bin/env python3
"""Regenerate dual-tight exact-cover matrices from exact geometry and dual weights.
No verdict cache, MILP solver, or precomputed incidence matrix is trusted.
Usage: python3 gen_exact.py 0 > component0.matrix
"""
import sys,json
from pathlib import Path
from collections import defaultdict
from fractions import Fraction
from verify_core import children
from verify_compact385 import connected_components
B=Path(__file__).resolve().parent
assert len(sys.argv)==2
id=int(sys.argv[1]);assert id in (0,6)
keep=set()
for line in (B/'win_witnesses1561.tsv').read_text().splitlines():
    h,p=line.split('\t');assert h not in keep and 0<=int(p)<121
    keep.add(h)
assert len(keep)==1561
s9={f'{c:032x}' for h in (B/'loss_roots35.txt').read_text().split() for c in children(int(h,16))}
cov=defaultdict(set)
for h in s9:
    for c in children(int(h,16)):cov[f'{c:032x}'].add(h)
assert len(s9)==782 and len(cov)==6446
D=json.loads((B/'dual_components.json').read_text())
W={h:Fraction(v) for d in D for h,v in d['weights'].items()}
weight=lambda ss:sum((W.get(s,0) for s in ss),Fraction(0))
high={h for h,ss in cov.items() if weight(ss)>1}
assert len(high)==1346 and high<=keep
possible={h:ss for h,ss in cov.items() if h not in high}
comps=connected_components(s9,possible)
assert len(comps)==12
comp=next(c for c in comps if set(D[id]['weights'])<=c)
pos=sorted(s for s in comp if W.get(s,0)>0)
zero=sorted(comp-set(pos))
pi={s:i for i,s in enumerate(pos)};zi={s:i for i,s in enumerate(zero)}
cols=sorted((h,ss) for h,ss in possible.items() if h not in keep and ss<=comp and weight(ss)==1)
print(len(pos),len(zero),len(cols))
for h,ss in cols:
    p=[pi[s] for s in sorted(ss) if s in pi]
    z=[zi[s] for s in sorted(ss) if s in zi]
    assert p and len(p)+len(z)==len(ss)
    print(len(p),len(z),*p,*z)
