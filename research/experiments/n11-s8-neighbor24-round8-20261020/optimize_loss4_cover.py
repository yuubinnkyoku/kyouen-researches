#!/usr/bin/env python3
"""Construct a shared S10 LOSS witness cover for four S8 LOSS roots.
SciPy MILP is only used to propose a certificate, never to verify it.
"""
from pathlib import Path
from verify_core import canonical,legal
from scipy.optimize import milp,LinearConstraint,Bounds
from scipy.sparse import lil_matrix
import numpy as np
B=Path(__file__).resolve().parent
roots=[int(a[1],16) for line in (B/'proof24.tsv').read_text().splitlines() if (a:=line.split('\t'))[0]=='ROOT' and a[2]=='LOSS']
assert len(roots)==4
s9=sorted({canonical(r|1<<p) for r in roots for p in legal(r)})
verdict={int(a[0],16):(a[1],int(a[2])) for line in (B/'loss4_all_s10_cpp.tsv').read_text().splitlines() if (a:=line.split('\t'))}
cands=sorted(k for k,v in verdict.items() if v[0]=='LOSS')
ix={v:i for i,v in enumerate(cands)}
A=lil_matrix((len(s9),len(cands)),dtype=float)
for i,s in enumerate(s9):
 for p in legal(s):
  q=canonical(s|1<<p)
  if q in ix:A[i,ix[q]]=1
 assert A.getrow(i).nnz
A=A.tocsr()
res=milp(c=np.ones(len(cands)),integrality=np.ones(len(cands)),bounds=Bounds(0,1),constraints=LinearConstraint(A,1,np.inf),options={'time_limit':60,'mip_rel_gap':0})
print('MILP',res.message,'nodes',getattr(res,'mip_node_count',None),'bound',getattr(res,'mip_dual_bound',None),'objective',res.fun)
assert res.x is not None and (A@np.round(res.x)>=1).all()
min_n=int(np.round(res.x).sum())
res2=milp(c=np.array([verdict[k][1] for k in cands],dtype=float),integrality=np.ones(len(cands)),bounds=Bounds(0,1),constraints=[LinearConstraint(A,1,np.inf),LinearConstraint(np.ones((1,len(cands))),min_n,min_n)],options={'time_limit':60,'mip_rel_gap':0})
print('secondary',res2.message,'cost',res2.fun)
if res2.x is None:res2=res
chosen={cands[i] for i,x in enumerate(res2.x) if x>0.5}
assert len(chosen)==min_n
print('cover',len(chosen),'states',sum(verdict[k][1] for k in chosen),'obligations',len(s9),'candidates',len(cands))
(B/'loss4_cover_selected.txt').write_text('\n'.join(f'{x:032x}' for x in sorted(chosen))+'\n')
