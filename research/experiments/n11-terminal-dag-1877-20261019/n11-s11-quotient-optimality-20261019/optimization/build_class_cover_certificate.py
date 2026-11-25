import sys,json,collections
from pathlib import Path
import networkx as nx
from networkx.algorithms import isomorphism
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix
sys.path.insert(0,str(Path(__file__).resolve().parent))
from hypergraph_signature import sig,v
BASE=Path(str(Path(__file__).resolve().parents[1]/'n11-s11-dual-branch-optimality-20261019'))
sys.path.insert(0,str(BASE))
from verify_full_s11 import candidates
high,parents=candidates()
classes=json.loads((Path(__file__).resolve().parent/'all_loss_isomorphism_classes.json').read_text())
sol=json.loads((Path(__file__).resolve().parent/'class_cover_lex.json').read_text())
selected_classes=[classes[j] for j in sol['selected_class_indices']]
position_to_rep={int(p,16):int(c['representative'],16) for c in selected_classes for p in c['positions']}
positions=sorted(position_to_rep)
A=lil_matrix((672,len(positions)),dtype=float)
for j,p in enumerate(positions):
 for i in parents[p]:A[i,j]=1
A=A.tocsc()
res=milp(c=np.ones(len(positions)),integrality=np.ones(len(positions)),bounds=Bounds(np.zeros(len(positions)),np.ones(len(positions))),constraints=LinearConstraint(A,np.ones(672),np.full(672,np.inf)),options={'time_limit':60,'mip_rel_gap':0})
print('selected classes',len(selected_classes),'available witnesses',len(positions),'witness minimum',res.fun,'status',res.status,'bound',res.mip_dual_bound,flush=True)
selected_w=[p for p,x in zip(positions,res.x) if x>.5]
assert set().union(*(parents[p] for p in selected_w))==set(range(672))
print('selected witness positions',len(selected_w),flush=True)
# Encode exact move-index permutations from each witness to its cheapest representative.
def make_graph(key):
 n,bad=key;G=nx.Graph()
 G.add_nodes_from(range(n),kind='move')
 for j,mask in enumerate(bad):
  eid=n+j;G.add_node(eid,kind='edge'+str(mask.bit_count()))
  for i in range(n):
   if mask>>i&1:G.add_edge(eid,i)
 return G
cache={}
cert=[]
for p in selected_w:
 r=position_to_rep[p];a=cache.setdefault(p,sig(p));b=cache.setdefault(r,sig(r))
 if a==b:perm=list(range(a[0]))
 else:
  gm=isomorphism.GraphMatcher(make_graph(a),make_graph(b),node_match=lambda x,y:x['kind']==y['kind'])
  assert gm.is_isomorphic()
  perm=[gm.mapping[i] for i in range(a[0])]
 assert sorted(perm)==list(range(a[0]))
 assert {sum(1<<perm[i] for i in range(a[0]) if mask>>i&1) for mask in a[1]}==set(b[1])
 cert.append([f'{p:032x}',f'{r:032x}',perm])
reps=sorted({position_to_rep[p] for p in positions if position_to_rep[p] in [int(c['representative'],16) for c in selected_classes]})
# A selected class might have no selected witness? It would be redundant in the class cover.
used_reps={position_to_rep[p] for p in selected_w}
assert len(used_reps)==len(selected_classes),('unused class',len(used_reps),len(selected_classes))
cert_path=Path(str(Path(__file__).resolve().parents[1]/'s11_class_cover_189_certificate.json'))
cert_path.write_text(json.dumps({'format':'n11-s11-hypergraph-class-cover-v1','witnesses':cert,'representatives':[f'{r:032x}' for r in sorted(used_reps)]},separators=(',',':')))
print('certificate bytes',cert_path.stat().st_size,'unique reps',len(used_reps),flush=True)
