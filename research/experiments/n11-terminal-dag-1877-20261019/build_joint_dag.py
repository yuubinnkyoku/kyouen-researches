#!/usr/bin/env python3
"""Generate a shared terminal-game proof DAG using exact incidence-graph isomorphism.
Generator uses networkx; the verifier uses only Python standard library.
"""
import sys,json,collections,time,os
from pathlib import Path
import networkx as nx
from networkx.algorithms import isomorphism as iso
P=Path(__file__).resolve().parent/'n11-s11-quotient-optimality-20261019'
sys.path.insert(0,str(P))
from verify_class_cover_189 import minimal_forbidden
from itertools import combinations
sys.path.insert(0,str(P/"n11-s11-dual-branch-optimality-20261019"))
import compact_proof184_342 as v

def signature_any(m):
    if m.bit_count()==11:return minimal_forbidden(m)
    assert m.bit_count()==10 and v.safe(m) and v.canonical(m)==m
    base=v.points(m);moves=v.legal(m);n=len(moves)
    bad=[]
    for i,j in combinations(range(n),2):
        if any(v.circle(a,b,moves[i],moves[j]) for a,b in combinations(base,2)):
            bad.append((1<<i)|(1<<j))
    for i,j,k in combinations(range(n),3):
        e=(1<<i)|(1<<j)|(1<<k)
        if any(e&b==b for b in bad):continue
        if any(v.circle(a,moves[i],moves[j],moves[k]) for a in base):bad.append(e)
    for ids in combinations(range(n),4):
        e=sum(1<<i for i in ids)
        if any(e&b==b for b in bad):continue
        if v.circle(*(moves[i] for i in ids)):bad.append(e)
    return n,set(bad)
def restrict(n,bad,played):
 rest=((1<<n)-1)^played
 blocked=0
 for e in bad:
  r=e&rest
  if r.bit_count()==1:blocked|=r
 rest&=~blocked
 idx=[i for i in range(n) if rest>>i&1]
 ren={i:j for j,i in enumerate(idx)}
 b=[]
 for e in bad:
  r=e&rest
  if r==0:continue
  if (e&~(rest|played))!=0:continue
  if r.bit_count()<2:raise AssertionError('bad residual singleton')
  mask=sum(1<<ren[i] for i in idx if r>>i&1)
  b.append(mask)
 b.sort(key=lambda x:(x.bit_count(),x))
 minimal=[]
 for e in b:
  if not any(e&f==f for f in minimal):minimal.append(e)
 return len(idx),tuple(sorted(minimal))

class DAG:
 def __init__(self):
  self.nodes=[];self.buckets=collections.defaultdict(list)
  self.hits=0;self.exact=0
 def graph(self,n,bad):
  g=nx.Graph()
  g.add_nodes_from(range(n),typ='v')
  for k,e in enumerate(bad):
   j=n+k;g.add_node(j,typ=f'e{e.bit_count()}')
   g.add_edges_from((j,i) for i in range(n) if e>>i&1)
  return g
 def locate(self,n,bad):
  g=self.graph(n,bad)
  h=nx.weisfeiler_lehman_graph_hash(g,node_attr='typ',iterations=4)
  for id,old in self.buckets[(n,h)]:
   self.exact+=1
   matcher=iso.GraphMatcher(g,old,node_match=iso.categorical_node_match('typ',''))
   if matcher.is_isomorphic():
    self.hits+=1
    return id,[matcher.mapping[i] for i in range(n)],g,h
  return None,None,g,h
 def solve(self,n,bad):
  id,perm,g,h=self.locate(n,bad)
  if id is not None:
   return self.nodes[id]['win'],id,perm
  id=len(self.nodes)
  node={'n':n,'bad':list(bad),'win':None,'edges':[]}
  self.nodes.append(node)
  self.buckets[(n,h)].append((id,g))
  win=False
  order=os.environ.get('ORDER','weighted_desc')
  degrees=[sum(1 for e in bad if e>>i&1) for i in range(n)]
  weighted=[sum(1/(e.bit_count()-1) for e in bad if e>>i&1) for i in range(n)]
  if order=='desc':moves=range(n-1,-1,-1)
  elif order=='degree_asc':moves=sorted(range(n),key=lambda i:(degrees[i],i))
  elif order=='degree_desc':moves=sorted(range(n),key=lambda i:(-degrees[i],i))
  elif order=='weighted_asc':moves=sorted(range(n),key=lambda i:(weighted[i],i))
  elif order=='weighted_desc':moves=sorted(range(n),key=lambda i:(-weighted[i],i))
  else:moves=range(n)
  for i in moves:
   n2,b2=restrict(n,bad,1<<i)
   childwin,childid,perm=self.solve(n2,b2)
   node['edges'].append([i,childid,perm])
   if not childwin:
    win=True;break
  node['win']=win
  return win,id,list(range(n))

def run():
 cert=json.loads((P/'s11_class_cover_189_certificate.json').read_text())
 roots=sorted(int(x,16) for x in cert['representatives'])+sorted(v.decode_positions(v.LEAVES_B85))
 dag=DAG();root_entries=[];t=time.time()
 for p in roots:
  n,bad=signature_any(p)
  win,id,perm=dag.solve(n,tuple(sorted(bad)))
  if win:raise ValueError(f'root unexpectedly WIN: {p:032x}')
  root_entries.append([f'{p:032x}',id,perm])
 print("initial",len(dag.nodes),dag.hits)
 # Keep only one LOSS child for each WIN node; LOSS nodes require every child.
 for node in dag.nodes:
  if node['win']:
   node['edges']=[next(edge for edge in node['edges'] if not dag.nodes[edge[1]]['win'])]
 reachable={entry[1] for entry in root_entries}
 todo=list(reachable)
 while todo:
  for _,child,_ in dag.nodes[todo.pop()]['edges']:
   if child not in reachable:
    reachable.add(child);todo.append(child)
 oldids=sorted(reachable)
 rename={old:new for new,old in enumerate(oldids)}
 nodes=[dag.nodes[i] for i in oldids]
 for node in nodes:
  node['edges']=[[move,rename[child],perm] for move,child,perm in node['edges']]
 root_entries=[[key,rename[child],perm] for key,child,perm in root_entries]
 print('pruned',len(nodes),'from',len(dag.nodes),'nodes')
 out={'format':'n11-s11-shared-residual-hypergraph-dag-v1','roots':root_entries,'nodes':nodes}
 path=Path(__file__).resolve().parent/'shared_s10_s11_dag.json'
 path.write_text(json.dumps(out,separators=(',',':'))+'\n')
 print('roots',len(roots),'nodes',len(nodes),'edges',sum(len(n['edges']) for n in nodes),'hits',dag.hits,'exact comparisons',dag.exact,'elapsed',time.time()-t,'bytes',path.stat().st_size)
 print('node WIN/LOSS',collections.Counter(n['win'] for n in nodes))
 print('node sizes',collections.Counter(n['n'] for n in nodes))
if __name__=='__main__':run()
