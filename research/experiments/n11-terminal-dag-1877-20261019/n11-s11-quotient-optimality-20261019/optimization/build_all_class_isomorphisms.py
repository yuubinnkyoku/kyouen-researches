import sys,json
from pathlib import Path
import networkx as nx
from networkx.algorithms import isomorphism
sys.path.insert(0,str(Path(__file__).resolve().parent))
from hypergraph_signature import sig,v
base=Path(str(Path(__file__).resolve().parent))
classes=json.loads((base/'all_loss_isomorphism_classes.json').read_text())

def graph(key):
 n,bad=key;G=nx.Graph();G.add_nodes_from(range(n),kind='move')
 for j,mask in enumerate(bad):
  eid=n+j;G.add_node(eid,kind='edge'+str(mask.bit_count()))
  for i in range(n):
   if mask>>i&1:G.add_edge(eid,i)
 return G
cache={}
rows=[]
for idx,c in enumerate(classes):
 r=int(c['representative'],16);b=cache.setdefault(r,sig(r));rg=graph(b)
 for h in c['positions']:
  p=int(h,16);a=cache.setdefault(p,sig(p));n=a[0]
  if a==b:perm=list(range(n))
  else:
   gm=isomorphism.GraphMatcher(graph(a),rg,node_match=lambda x,y:x['kind']==y['kind'])
   assert gm.is_isomorphic()
   perm=[gm.mapping[i] for i in range(n)]
  assert sorted(perm)==list(range(n))
  assert {sum(1<<perm[i] for i in range(n) if mask>>i&1) for mask in a[1]}==set(b[1])
  rows.append([f'{p:032x}',idx,perm])
assert len(rows)==982 and len(set(r[0] for r in rows))==982
cert={'format':'n11-s11-terminal-hypergraph-quotient-v1','class_representatives':[c['representative'] for c in classes],'members':sorted(rows)}
path=base.parent/'s11_all_982_isomorphisms.json';path.write_text(json.dumps(cert,separators=(',',':')))
print('class count',len(classes),'candidate count',len(rows),'bytes',path.stat().st_size)
