import json,sys,time,collections,os
from pathlib import Path
from build_joint_dag import DAG,signature_any
P=Path(__file__).resolve().parent
Q=P/'n11-s11-quotient-optimality-20261019'
sys.path.insert(0,str(Q/'n11-s11-dual-branch-optimality-20261019'))
import compact_proof184_342 as v
from functools import lru_cache
v.circle=lru_cache(maxsize=500000)(v.circle)
D=json.loads((P/'baseline.json').read_text());s=DAG();t=time.time()
leaves=sorted(v.decode_positions(v.LEAVES_B85));r8=v.decode_positions(v.ROOTS_B85)
obs=set().union(*(v.children(p) for p in r8));boundary=set().union(*(v.children(p) for p in obs));packed=v.decode(v.WEIGHTS_B85)
weights={p:(packed[i//4]>>(2*(i%4)))&3 for i,p in enumerate(sorted(obs))}
obset={p:{v.canonical(p^(1<<i)) for i in v.points(p)}&obs for p in boundary}
high={p for p in boundary if sum(weights[q] for q in obset[p])>2}
print('high',len(high),'elapsed',round(time.time()-t,1),flush=True)
# inverse children: each S11 has 11 S10 predecessors
H={p:i for i,p in enumerate(sorted(high))}
quot=json.loads((Q/'s11_all_982_isomorphisms.json').read_text()); reps=quot['class_representatives'];members=quot['members'];class_cover=[set() for _ in reps]
for phex,cid,perm in members:
 p=int(phex,16)
 for i in v.points(p):
  par=v.canonical(p^(1<<i))
  if par in H:class_cover[cid].add(H[par])
assert len(set.union(*class_cover))==len(high)
print('class coverage',len(reps),'elapsed',round(time.time()-t,1),flush=True)

# solve 184 S10 leaf roots first; add all 606 S11 LOSS classes, sharing identical games
leafroots=[]
for p in leaves:
 n,bad=signature_any(p);g,id,perm=s.solve(n,tuple(sorted(bad)))
 assert not g
 leafroots.append([f'{p:032x}',id,perm])
print('S10 nodes',len(s.nodes),'elapsed',round(time.time()-t,1),flush=True)
classroots=[]
for k,phex in enumerate(reps):
 n,bad=signature_any(int(phex,16));g,id,perm=s.solve(n,tuple(sorted(bad)))
 assert not g,('unexpected WIN',k,phex)
 classroots.append([phex,id,perm])
 if k%100==0:print('class',k,'nodes',len(s.nodes),'elapsed',round(time.time()-t,1),flush=True)
print('ALL nodes',len(s.nodes),'elapsed',round(time.time()-t,1),flush=True)

# compute closures in DAG (pruned WIN edges to first LOSS witness)
closure=[None]*len(s.nodes)
def close(i):
 if closure[i] is not None:return closure[i]
 node=s.nodes[i]
 edges=([next(e for e in node['edges'] if not s.nodes[e[1]]['win'])] if node['win'] else node['edges'])
 z={i}
 for _,j,_ in edges:z|=close(j)
 closure[i]=z;return z
base=set()
for p,j,_ in leafroots:base|=close(j)
print('S10 proof base',len(base),'elapsed',round(time.time()-t,1),flush=True)

# Greedy set-cover with incremental closure cost
remaining=set(H.values());chosen=[];covered=set();used=set(base)
while remaining:
 best=None;bestscore=None
 for cid in range(len(reps)):
  new=class_cover[cid]&remaining
  if not new:continue
  extra=close(classroots[cid][1])-used
  cost=len(extra)
  score=(cost/len(new),-len(new),cost,cid)
  if bestscore is None or score<bestscore:bestscore=score;best=cid
 chosen.append(best);remaining-=class_cover[best];used|=close(classroots[best][1])
 if len(chosen)%25==0:print('selected',len(chosen),'remaining',len(remaining),'DAG nodes',len(used),'elapsed',round(time.time()-t,1),flush=True)
print('GREEDY selected',len(chosen),'DAG nodes',len(used),'elapsed',round(time.time()-t,1),flush=True)
# reverse delete any redundant classes, favor expensive removals
for cid in sorted(chosen,key=lambda i:len(close(classroots[i][1])-base),reverse=True):
 if all(any(j!=cid and k in class_cover[j] for j in chosen) for k in class_cover[cid]):
  chosen.remove(cid)
used=set(base)
for cid in chosen:used|=close(classroots[cid][1])
print('PRUNED',len(chosen),'DAG nodes',len(used),'elapsed',round(time.time()-t,1),flush=True)

# Save state for later optimization and independent check
out={'chosen_classes':chosen,'class_roots':classroots,'leaf_roots':leafroots,'class_cover':[sorted(x) for x in class_cover],'high_positions':[f'{p:032x}' for p in sorted(high)],'nodes':s.nodes,'selected_node_count':len(used)}
(P/'joint_class_search_state.json').write_text(json.dumps(out,separators=(',',':')))
print('WROTE state bytes',(P/'joint_class_search_state.json').stat().st_size)
