from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).parent/'n11-18root-global184-20261019'))
from verify_core import children,points,canonical
P=Path(__file__).parent
rows={int(a,16):(b,int(s),int(m),int(w)) for a,b,s,m,w in (l.split() for l in (P/'s10-probe19-results.tsv').read_text().splitlines())}
assert len(rows)==2290
for a,b,s,m,w in (l.split() for l in (P/'s8-new-all-s10-results.tsv').read_text().splitlines()):
 key=int(a,16);val=(b,int(s),int(m),int(w))
 if key in rows:assert rows[key]==val
 rows[key]=val
roots=[]; winleaves=set()
for h,*idx in (l.split() for l in (P/'gap6_indices.txt').read_text().splitlines()):
 root=int(h,16);cs=sorted(children(root));assert root.bit_count()==8
 options=[]
 for i in idx:
  s9=cs[int(i)];ls=children(s9);loss=[x for x in ls if rows[x][0]=='LOSS']
  if not loss:options.append((sum(rows[x][1] for x in ls),len(ls),s9,ls))
 if options:
  cost,n,s9,ls=min(options)
  roots.append({'root':h,'verdict':'WIN','s9_witness':f'{s9:032x}','s10_win_children':[f'{m:032x}' for m in sorted(ls)],'cost':cost})
  winleaves.update(ls)
 else:
  roots.append({'root':h,'verdict':'LOSS'})
assert sum(x['verdict']=='WIN' for x in roots)==18
assert sum(x['verdict']=='LOSS' for x in roots)==1
assert next(x['root'] for x in roots if x['verdict']=='LOSS')=='00000000041000003000401000100100'
print('18 WIN root witness individual states',sum(x['cost'] for x in roots if x['verdict']=='WIN'))
print('distinct S10 WIN leaves',len(winleaves),'states',sum(rows[x][1] for x in winleaves))
print('WIN witness S9 legal child counts', [len(x['s10_win_children']) for x in roots if x['verdict']=='WIN'])
# s8 loss dual LP certificate
import numpy as np
from scipy.optimize import linprog
lossroot=int('00000000041000003000401000100100',16)
s9=sorted(children(lossroot))
s9_children=[children(m) for m in s9]
all_boundary=set().union(*s9_children)
losses=sorted(p for p,r in rows.items() if r[0]=='LOSS' and p in all_boundary)
print('s8 loss candidate S10 LOSS',len(losses))
A=np.array([[int(leaf in c) for leaf in losses] for c in s9_children],dtype=float)
r=linprog(-np.ones(len(s9)),A_ub=A.T,b_ub=np.ones(len(losses)),bounds=(0,None),method='highs')
assert r.success and abs(r.fun+15)<1e-8
weights=[int(round(2*x)) for x in r.x]
assert all(abs(x-y/2)<1e-8 for x,y in zip(r.x,weights))
assert sum(weights)==30
chosen=[int(h,16) for h in (P/'s8-new-certificate-s10-leaves.txt').read_text().split()]
assert len(chosen)==15 and all(rows[p][0]=='LOSS' for p in chosen)
assert all(any(p in c for p in chosen) for c in s9_children)
assert all(sum(weights[i] for i,m in enumerate(s9) if p in s9_children[i])<=2 for p in losses)
cert={'format':'n11-s8-gap6-terminal-certificate-v1','perspective':'side-to-move WIN/LOSS (normal play)',
      's8_win_roots':[{k:v for k,v in x.items() if k not in ('verdict','cost')} for x in roots if x['verdict']=='WIN'],
      's8_loss_root':f'{lossroot:032x}',
      's8_loss_s9_obligations':[f'{m:032x}' for m in s9],
      's8_loss_s10_leaves':[f'{p:032x}' for p in sorted(chosen)],
      's8_loss_dual_weights_halves':weights,
      'new_s7_loss_parents':[f'{m:032x}' for m in sorted({canonical(lossroot^(1<<p)) for p in points(lossroot)})]}
(P/'gap6-terminal-cert.json').write_text(json.dumps(cert,indent=2)+'\n')
print('dual weights halves',weights)
