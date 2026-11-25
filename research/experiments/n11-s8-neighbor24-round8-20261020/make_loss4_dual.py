#!/usr/bin/env python3
"""Generate half-integral LP dual weights (construction only)."""
from pathlib import Path
from verify_core import canonical,legal
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
import numpy as np
B=Path(__file__).resolve().parent
roots=[int(a[1],16) for line in (B/'proof24_optimized.tsv').read_text().splitlines() if (a:=line.split('\t'))[0]=='ROOT' and a[2]=='LOSS']
s9=sorted({canonical(r|1<<p) for r in roots for p in legal(r)})
verdict={int(a[0],16):a[1] for line in (B/'loss4_all_s10_cpp.tsv').read_text().splitlines() if (a:=line.split('\t'))}
loss=sorted(k for k,v in verdict.items() if v=='LOSS');ix={v:i for i,v in enumerate(loss)}
A=lil_matrix((len(s9),len(loss)),dtype=float)
for i,s in enumerate(s9):
 for p in legal(s):
  q=canonical(s|1<<p)
  if q in ix:A[i,ix[q]]=1
A=A.tocsr()
res=linprog(-np.ones(len(s9)),A_ub=A.T,b_ub=np.ones(len(loss)),bounds=(0,None),method='highs')
assert res.success
weights=[round(2*x) for x in res.x]
assert max(abs(2*x-w) for x,w in zip(res.x,weights))<1e-6
assert sum(weights)==81 and all(w>=0 for w in weights)
assert (A.T@np.array(weights)<=2).all()
(B/'loss4_dual_halves.tsv').write_text(''.join(f'{s:032x}\t{w}\n' for s,w in zip(s9,weights)))
print('dual objective',sum(weights),'/2 =',sum(weights)/2,'=> >=41 leaves')
