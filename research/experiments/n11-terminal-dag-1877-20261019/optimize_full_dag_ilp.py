import json,time,collections
from pathlib import Path
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix
from build_joint_dag import DAG,restrict
import networkx as nx
P=Path(__file__).resolve().parent
D=json.loads((P/'joint_class_search_state.json').read_text());nodes=D['nodes'];N=len(nodes);t=time.time()
match=DAG()
for i,node in enumerate(nodes):
 n=node['n'];b=node['bad'];g=match.graph(n,b);h=nx.weisfeiler_lehman_graph_hash(g,node_attr='typ',iterations=4)
 match.buckets[(n,h)].append((i,g))
opts=[]
for i,node in enumerate(nodes):
 n,b=node['n'],tuple(node['bad']);edges=[]
 for move in range(n):
  nn,bb=restrict(n,b,1<<move)
  j,perm,_,_=match.locate(nn,bb)
  if j is not None and nodes[j]['win']!=node['win']:edges.append([move,j,perm])
 if not node['win'] and len(edges)!=n:raise ValueError(f'LOSS child missing {i} {len(edges)}/{n}')
 if node['win'] and not edges:raise ValueError(f'WIN child missing {i}')
 opts.append(edges)
print('nodes',N,'edges',sum(map(len,opts)),'elapsed',round(time.time()-t,1),flush=True)
# constraint y_i - y_j <=0 for LOSS, y_i - sum_j y_j <=0 for WIN
rows=[];cols=[];vals=[];lb=[];ub=[]
def add(coeff,lo=-np.inf,hi=0):
 r=len(lb)
 for c,v in coeff:
  rows.append(r);cols.append(c);vals.append(v)
 lb.append(lo);ub.append(hi)
for i,node in enumerate(nodes):
 if node['win']:
  children=sorted({j for _,j,_ in opts[i]})
  add([(i,1)]+[(j,-1) for j in children])
 else:
  for j in sorted({j for _,j,_ in opts[i]}):add([(i,1),(j,-1)])
for _,j,_ in D['leaf_roots']:add([(j,1)],lo=1,hi=np.inf)
for k in range(672):
 classes=[c for c,cover in enumerate(D['class_cover']) if k in cover]
 ids=sorted({D['class_roots'][c][1] for c in classes})
 add([(j,1) for j in ids],lo=1,hi=np.inf)
A=coo_matrix((np.array(vals,dtype=float),(rows,cols)),shape=(len(lb),N)).tocsr()
print('MILP constraints',len(lb),'nonzero',A.nnz,'elapsed',round(time.time()-t,1),flush=True)
res=milp(np.ones(N),integrality=np.ones(N),bounds=Bounds(np.zeros(N),np.ones(N)),constraints=LinearConstraint(A,lb,ub),options={'time_limit':100,'mip_rel_gap':0.005,'disp':True})
print('RESULT',res.status,res.message,'objective',res.fun,'bound',getattr(res,'mip_dual_bound',None),'gap',getattr(res,'mip_gap',None),'elapsed',round(time.time()-t,1),flush=True)
if res.x is not None:
 active={i for i,x in enumerate(res.x) if x>.5}
 assert all(j in active for _,j,_ in D['leaf_roots'])
 assert all(any(D['class_roots'][c][1] in active for c,cover in enumerate(D['class_cover']) if k in cover) for k in range(672))
 assert all((any(j in active for _,j,_ in opts[i]) if nodes[i]['win'] else all(j in active for _,j,_ in opts[i])) for i in active)
 print('active',len(active),'active class roots',sum(D['class_roots'][c][1] in active for c in range(606)),flush=True)
 (P/'joint_full_dag_ilp.json').write_text(json.dumps({'active':sorted(active),'status':res.status,'bound':getattr(res,'mip_dual_bound',None),'gap':getattr(res,'mip_gap',None)},indent=2))
 (P/'joint_full_dag_options.json').write_text(json.dumps(opts,separators=(',',':')))
