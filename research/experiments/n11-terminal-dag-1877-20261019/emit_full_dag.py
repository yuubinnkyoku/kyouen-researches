import json,time,collections,sys
from pathlib import Path
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix
P=Path(__file__).resolve().parent;Q=P/'n11-s11-quotient-optimality-20261019'
D=json.loads((P/'joint_class_search_state.json').read_text());opt=json.loads((P/'joint_full_dag_ilp.json').read_text());options=json.loads((P/'joint_full_dag_options.json').read_text());nodes=D['nodes'];active=set(opt['active'])
q=json.loads((Q/'s11_all_982_isomorphisms.json').read_text());H={p:i for i,p in enumerate(D['high_positions'])};allowed_classes={i for i,r in enumerate(D['class_roots']) if r[1] in active}
# reconstruct incidence from geometry (do not trust precomputed class_cover)
sys.path.insert(0,str(Q/'n11-s11-dual-branch-optimality-20261019'))
import compact_proof184_342 as v
witness=[]
for phex,cid,perm in q['members']:
 if cid not in allowed_classes:continue
 p=int(phex,16);cover=set()
 for j in v.points(p):
  par=f'{v.canonical(p^(1<<j)):032x}'
  if par in H:cover.add(H[par])
 if cover:witness.append((phex,cid,perm,cover))
print('allowed classes',len(allowed_classes),'candidate witness positions',len(witness))
# solve min cardinality witness cover
row=[];col=[];val=[]
for i,(_,_,_,cover) in enumerate(witness):
 for k in cover:row.append(k);col.append(i);val.append(1)
A=coo_matrix((np.array(val,dtype=float),(row,col)),shape=(len(H),len(witness))).tocsr()
res=milp(np.ones(len(witness)),integrality=np.ones(len(witness)),bounds=Bounds(np.zeros(len(witness)),np.ones(len(witness))),constraints=LinearConstraint(A,np.ones(len(H)),np.full(len(H),np.inf)),options={'time_limit':60,'mip_rel_gap':0.005})
if res.x is None:raise ValueError('witness cover failed')
selected=[witness[i] for i,x in enumerate(res.x) if x>.5]
assert len(set().union(*(e[3] for e in selected)))==len(H)
print('selected witness positions',len(selected),'classes',len({e[1] for e in selected}),'status',res.status,'bound',getattr(res,'mip_dual_bound',None))
selected_classes={e[1] for e in selected}
roots=D['leaf_roots']+[D['class_roots'][c] for c in sorted(selected_classes)]
# prune reachability. Choose any active LOSS child for WIN; prefer existing original edge when possible.
chosen={}
for i in active:
 if nodes[i]['win']:
  legal=[e for e in options[i] if e[1] in active]
  assert legal
  original=nodes[i]['edges'][0]
  chosen[i]=next((e for e in legal if e[:2]==original[:2]),legal[0])
 else:
  chosen[i]=options[i]
reached={r[1] for r in roots};todo=list(reached)
while todo:
 i=todo.pop();edges=[chosen[i]] if nodes[i]['win'] else chosen[i]
 for _,j,_ in edges:
  if j not in reached:reached.add(j);todo.append(j)
print('active',len(active),'reachable',len(reached),'roots',len(roots))
remap={j:i for i,j in enumerate(sorted(reached))};newnodes=[]
for i in sorted(reached):
 node=dict(nodes[i]);edges=[chosen[i]] if node['win'] else chosen[i]
 node['edges']=[[move,remap[j],perm] for move,j,perm in edges]
 newnodes.append(node)
newroots=[[p,remap[j],perm] for p,j,perm in roots]
cert={'format':'n11-s11-shared-residual-hypergraph-dag-v1','roots':newroots,'nodes':newnodes}
(P/'joint_dag_optimized_final.json').write_text(json.dumps(cert,separators=(',',':'))+'\n')
cover={'format':'n11-s11-hypergraph-class-cover-v1','witnesses':[[p,q['class_representatives'][cid],perm] for p,cid,perm,_ in selected],'representatives':sorted({q['class_representatives'][cid] for _,cid,_,_ in selected})}
(P/'joint_cover_optimized_final.json').write_text(json.dumps(cover,separators=(',',':'))+'\n')
print('FINAL nodes',len(newnodes),'edges',sum(len(n['edges']) for n in newnodes),'rootcount',len(newroots),'witnesses',len(selected),'classreps',len(selected_classes))
