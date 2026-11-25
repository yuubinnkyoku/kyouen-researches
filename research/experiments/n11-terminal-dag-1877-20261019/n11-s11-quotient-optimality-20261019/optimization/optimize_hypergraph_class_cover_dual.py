#!/usr/bin/env python3
import sys,collections,json,time
from pathlib import Path
import networkx as nx
from networkx.algorithms import isomorphism
from scipy.optimize import milp,LinearConstraint,Bounds,linprog
from scipy.sparse import lil_matrix
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from hypergraph_signature import sig,v
BASE=Path(str(Path(__file__).resolve().parents[1]/'n11-s11-dual-branch-optimality-20261019'))
sys.path.insert(0,str(BASE))
from verify_full_s11 import candidates

def make_graph(key):
 n,bad=key;G=nx.Graph()
 G.add_nodes_from(range(n),kind='move')
 for j,mask in enumerate(bad):
  eid=n+j;G.add_node(eid,kind='edge'+str(mask.bit_count()))
  for i in range(n):
   if mask>>i&1:G.add_edge(eid,i)
 return G

high,parents=candidates()
rows={int(s,16):(res,int(states),int(moves)) for s,res,states,moves,_ in (line.split() for line in (BASE/'all_s11_cpp.tsv').read_text().splitlines())}
loss=sorted(p for p in parents if rows[p][0]=='LOSS')
assert len(loss)==982
print('geometry high',len(high),'loss',len(loss),flush=True)
by_sig=collections.defaultdict(list)
for p in loss:by_sig[sig(p)].append(p)
print('exact signatures',len(by_sig),flush=True)
by_wl=collections.defaultdict(list)
for key in by_sig:
 G=make_graph(key)
 h=nx.weisfeiler_lehman_graph_hash(G,node_attr='kind')
 by_wl[h].append((key,G))
classes=[];isotests=0
for entries in by_wl.values():
 local=[]
 for key,G in entries:
  for grp in local:
   rep,RG=grp[0]
   isotests+=1
   if nx.is_isomorphic(G,RG,node_match=lambda a,b:a['kind']==b['kind']):
    grp.append((key,G));break
  else:local.append([(key,G)])
 for grp in local:
  pp=[p for key,G in grp for p in by_sig[key]]
  r=min(pp,key=lambda p:(rows[p][1],p))
  classes.append({'representative':r,'positions':pp,'signatures':[key for key,G in grp]})
print('iso classes',len(classes),'iso tests',isotests,'group sizes',collections.Counter(len(x['positions']) for x in classes).most_common(12),flush=True)
N=len(classes)
A=lil_matrix((672,N),dtype=float)
for j,c in enumerate(classes):
 for p in c['positions']:
  for i in parents[p]:A[i,j]=1
A=A.tocsc()
print('nonzeros',A.nnz,flush=True)
lp=linprog(np.array([rows[x['representative']][1] for x in classes],dtype=float),A_ub=-A,b_ub=-np.ones(672),bounds=(0,None),method='highs')
from fractions import Fraction
weights=[Fraction(float(-x)).limit_denominator(10000) for x in lp.ineqlin.marginals]
assert all(x>=0 for x in weights)
assert sum(weights)==Fraction(11609,2)
for j,c in enumerate(classes):
 covered=set().union(*(parents[p] for p in c['positions']))
 assert sum(weights[i] for i in covered)<=rows[c['representative']][1],j
print('dual support',sum(x>0 for x in weights),'denominators',collections.Counter(x.denominator for x in weights if x),'objective',sum(weights),flush=True)
(Path(__file__).resolve().parents[1]/'s11_class_cover_dual.json').write_text(json.dumps([[i,str(x)] for i,x in enumerate(weights) if x],separators=(',',':')))

opts={'time_limit':45,'mip_rel_gap':0.0}
for name,cost in [('count',np.ones(N)),('states',np.array([rows[x['representative']][1] for x in classes],dtype=float)),('lex',np.array([1000*rows[x['representative']][1]+1 for x in classes],dtype=float))]:
 t=time.time();res=milp(c=cost,integrality=np.ones(N),bounds=Bounds(np.zeros(N),np.ones(N)),constraints=LinearConstraint(A,np.ones(672),np.full(672,np.inf)),options=opts)
 print(name,'status',res.status,'message',res.message,'value',res.fun,'bound',res.mip_dual_bound,'gap',res.mip_gap,'time',round(time.time()-t,2),flush=True)
 if res.x is None:continue
 selected=[j for j,x in enumerate(res.x) if x>0.5]
 assert all(any(A[i,j] for j in selected) for i in range(672))
 output={'metric':name,'selected_class_indices':selected,'selected_representatives':[f'{classes[j]["representative"]:032x}' for j in selected], 'terminal_states':sum(rows[classes[j]['representative']][1] for j in selected), 'num_classes':len(selected), 'optimization':{'status':res.status,'dual_bound':res.mip_dual_bound,'gap':res.mip_gap}}
 (Path(str(Path(__file__).resolve().parent))/('class_cover_'+name+'.json')).write_text(json.dumps(output,indent=2))
print('saving classes',flush=True)
(Path(str(Path(__file__).resolve().parent))/'all_loss_isomorphism_classes.json').write_text(json.dumps([{'representative':f'{x["representative"]:032x}','positions':[f'{p:032x}' for p in x['positions']]} for x in classes]))
