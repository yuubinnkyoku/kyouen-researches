#!/usr/bin/env python3
"""Optional SciPy audit of the 143-candidate, 104-obligation minimum S10 LOSS leaf cover."""
from pathlib import Path
import sys
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix
from fifth_verify_standalone import children
p=Path(__file__).resolve().parent.parent/'data'
s9=[int(x,16) for x in (p/'s8_loss_obligations.txt').read_text().split()]
leaves=[int(x,16) for x in (p/'s8_loss_candidate_leaves.txt').read_text().split()]
receipts={int(a,16):(b,int(s),int(m)) for a,b,s,m in (x.split() for x in (p/'s8_loss_candidate_leaves_cpp.tsv').read_text().splitlines())}
assert len(s9)==104 and len(leaves)==143
assert all(receipts[x][0]=='LOSS' for x in leaves)
A=lil_matrix((len(s9),len(leaves)),dtype=np.float64)
for i,s in enumerate(s9):
 ch=children(s)
 for j,x in enumerate(leaves):
  if x in ch:A[i,j]=1
A=A.tocsr();integ=np.ones(len(leaves),dtype=int);bounds=Bounds(0,1)
r=milp(np.ones(len(leaves)),integrality=integ,bounds=bounds,constraints=LinearConstraint(A,1,np.inf),options={'time_limit':30,'mip_rel_gap':0})
assert r.success and abs(r.fun-r.mip_dual_bound)<1e-6 and r.fun==63
C=np.vstack((A.toarray(),np.ones((1,len(leaves)))))
lo=np.r_[np.ones(len(s9)),63];hi=np.r_[np.full(len(s9),np.inf),63]
r2=milp(np.array([receipts[x][1] for x in leaves],dtype=float),integrality=integ,bounds=bounds,constraints=LinearConstraint(C,lo,hi),options={'time_limit':30,'mip_rel_gap':0})
assert r2.success and abs(r2.fun-r2.mip_dual_bound)<1e-6 and r2.fun==85676
chosen={int(x,16) for x in (p/'s8_loss_selected_leaves.txt').read_text().split()}
assert len(chosen)==63 and sum(receipts[x][1] for x in chosen)==85676
assert all(any(x in chosen for x in children(s)) for s in s9)
print('PASS candidate-restricted ILP minimum 63 S10 leaves, states 85676, both dual gaps 0')
