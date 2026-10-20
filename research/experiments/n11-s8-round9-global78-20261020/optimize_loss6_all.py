from pathlib import Path
from collections import defaultdict
import numpy as np
from scipy.optimize import milp,LinearConstraint,Bounds,linprog
from scipy.sparse import lil_matrix
from verify_core import canonical,points,children
B=Path(__file__).resolve().parent
roots=[x.split('\t') for x in (B/'round9_proof.tsv').read_text().splitlines() if x.startswith('ROOT')]
loss=[int(r[1],16) for r in roots if r[2]=='LOSS']
obs=set().union(*(children(r) for r in loss))
rows=(B/'loss6_all_s10_cpp.tsv').read_text().splitlines()
loss10=[int(r.split('\t')[0],16) for r in rows if r.split('\t')[1]=='LOSS']
coverage={x:{canonical(x^(1<<p)) for p in points(x)}&obs for x in loss10}
coverage={x:v for x,v in coverage.items() if v}
obs=sorted(obs); cand=sorted(coverage)
index={x:i for i,x in enumerate(obs)}
A=lil_matrix((len(obs),len(cand)),dtype=float)
for j,x in enumerate(cand):
 for s in coverage[x]:A[index[s],j]=1
A=A.tocsr()
print('obligations',len(obs),'candidates',len(cand),flush=True)
res=milp(np.ones(len(cand)),integrality=np.ones(len(cand)),bounds=Bounds(0,1),constraints=LinearConstraint(A,1,np.inf),options={'time_limit':60})
print('milp',res.message,res.fun,flush=True)
assert res.x is not None
sel=[x for j,x in enumerate(cand) if res.x[j]>0.5]
assert len(sel)==round(res.fun) and set().union(*(coverage[x] for x in sel))==set(obs)
(B/'loss6_all_cover_selected.txt').write_text(''.join(f'{x:032x}\n' for x in sel))
# save certificate mapping chosen candidate per obligation
mp={s:min((x for x in sel if s in coverage[x])) for s in obs}
(B/'loss6_all_cover_mapping.tsv').write_text(''.join(f'{s:032x}\t{mp[s]:032x}\n' for s in obs))
# dual LP floating lower bound exploratory
lp=linprog(-np.ones(len(obs)),A_ub=A.T,b_ub=np.ones(len(cand)),bounds=(0,None),method='highs')
print('LP dual',-lp.fun, 'integer',res.fun,'gap',res.fun+lp.fun,flush=True)
