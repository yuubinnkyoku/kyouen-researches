#!/usr/bin/env python3
"""Optimize shared S10 WIN leaves for 20 S8 WIN roots.
No optimizer result is treated as proof; the output is verified independently.
"""
from pathlib import Path
from verify_core import canonical,legal
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
import numpy as np
B=Path(__file__).resolve().parent
roots=[int(a[1],16) for line in (B/'proof24.tsv').read_text().splitlines() if (a:=line.split('\t'))[0]=='ROOT' and a[2]=='WIN']
assert len(roots)==20
verdict={int(a[0],16):(a[1],int(a[2])) for line in (B/'all_s10_cpp.tsv').read_text().splitlines() if (a:=line.split('\t'))}
opts=[]
for ri,r in enumerate(roots):
 for p in legal(r):
  s9=canonical(r|1<<p)
  ch={canonical(s9|1<<q) for q in legal(s9)}
  if all(verdict[c][0]=='WIN' for c in ch):opts.append((ri,s9,ch))
assert len({ri for ri,_,_ in opts})==20
leaves=sorted({c for _,_,ch in opts for c in ch});leaf_ix={c:i for i,c in enumerate(leaves)}
no=len(opts);nl=len(leaves)
# Each root selects exactly one S9 witness; selected S9 forces all S10 WIN children.
A=lil_matrix((20+sum(len(ch) for _,_,ch in opts),no+nl),dtype=float)
lb=np.zeros(A.shape[0]);ub=np.full(A.shape[0],np.inf)
for ri in range(20):
 for j,(r,_,_) in enumerate(opts):
  if ri==r:A[ri,j]=1
 lb[ri]=1;ub[ri]=1
row=20
for j,(_,_,ch) in enumerate(opts):
 for c in ch:
  A[row,no+leaf_ix[c]]=1;A[row,j]=-1;row+=1
assert row==A.shape[0]
A=A.tocsr();integrality=np.ones(no+nl);bounds=Bounds(0,1)
objective=np.r_[np.zeros(no),np.ones(nl)]
res=milp(c=objective,integrality=integrality,bounds=bounds,constraints=LinearConstraint(A,lb,ub),options={'time_limit':120,'mip_rel_gap':0})
print('options',no,'potential leaves',nl,'min count',res.message,'objective',res.fun,'bound',res.mip_dual_bound)
assert res.x is not None
min_n=round(res.fun)
card=np.r_[np.zeros(no),np.ones(nl)]
# Second stage minimizes summed independently re-solved states, fixing minimal leaf count.
A2=lil_matrix((1,no+nl));A2[0,no:]=1
from scipy.sparse import vstack
cost=np.r_[np.zeros(no),np.array([verdict[c][1] for c in leaves])]
res2=milp(c=cost,integrality=integrality,bounds=bounds,constraints=[LinearConstraint(A,lb,ub),LinearConstraint(A2.tocsr(),min_n,min_n)],options={'time_limit':120,'mip_rel_gap':0})
print('min cost at count',res2.message,'cost',res2.fun,'bound',res2.mip_dual_bound)
if res2.x is None:res2=res
chosen=[(ri,s9,ch) for j,(ri,s9,ch) in enumerate(opts) if res2.x[j]>0.5]
assert len(chosen)==20 and len({ri for ri,_,_ in chosen})==20
selected=set().union(*(ch for _,_,ch in chosen))
assert len(selected)==min_n
print('selected leaves',len(selected),'states',sum(verdict[c][1] for c in selected))
(B/'win20_s9_selected.tsv').write_text(''.join(f'{roots[ri]:032x}\t{s9:032x}\n' for ri,s9,ch in sorted(chosen)))
