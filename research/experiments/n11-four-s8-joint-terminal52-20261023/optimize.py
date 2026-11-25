#!/usr/bin/env python3
"""Optional SciPy/HiGHS search; NOT needed to independently verify the proof."""
from pathlib import Path
import numpy as np
from scipy.optimize import Bounds,LinearConstraint,milp
from scipy.sparse import lil_matrix,vstack,csr_matrix
from terminal_geometry import canonical,children
from verify_global import read_keys,read_s10
H=Path(__file__).resolve().parent
roots=read_keys(H/'roots4.keys',8)
obligations=sorted(set().union(*(children(x) for x in roots)))
verdicts=read_s10(H/'s10-all1017.tsv')
keys=sorted(k for k,v in verdicts.items() if v[0]=='LOSS')
A=lil_matrix((len(obligations),len(keys)),dtype=float)
idx={x:i for i,x in enumerate(obligations)}
for j,k in enumerate(keys):
    for p in range(121):
        if (k>>p)&1:
            child=canonical(k^(1<<p))
            if child in idx:A[idx[child],j]=1
A=A.tocsr();N=len(keys)
first=milp(np.ones(N),integrality=np.ones(N),bounds=Bounds(0,1),
           constraints=LinearConstraint(A,np.ones(len(obligations)),np.inf),
           options={'mip_rel_gap':0})
assert first.success and first.fun==52 and first.mip_gap==0
B=vstack([A,csr_matrix(np.ones((1,N)))]).tocsr()
second=milp(np.array([verdicts[k][1] for k in keys],dtype=float),
            integrality=np.ones(N),bounds=Bounds(0,1),
            constraints=LinearConstraint(B,np.r_[np.ones(len(obligations)),52],
                                         np.r_[np.full(len(obligations),np.inf),52]),
            options={'mip_rel_gap':0})
assert second.success and second.fun==12280 and second.mip_gap==0
chosen={keys[j] for j,x in enumerate(second.x) if x>0.5}
assert chosen==read_keys(H/'selected52.keys',10)
print('PASS ILP: 52 leaves, min individual terminal states 12280 (HiGHS optimum)')
