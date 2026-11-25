#!/usr/bin/env python3
"""Independent finite audit for the proved two-token residual slice z=6,y=13."""
from __future__ import annotations
import hashlib,json,random
from functools import lru_cache
from pathlib import Path
def mex(values):
 s=set(values);g=0
 while g in s:g+=1
 return g
def odd(r,lo,hi=None):return r>=lo and (hi is None or r<=hi) and r%2==1
def even(r,lo,hi=None):return r>=lo and (hi is None or r<=hi) and r%2==0
def h5(x,y,r):
 if r==0:return 0
 s,d=x+y,x-y
 if d==0:t={1,3,5}
 elif d==1:t={1,3,5,2*y+3}
 elif d==2:t={1,3,5}
 elif d in (3,4):t={1,3,5}
 elif d==5:t={1,3,5,2*y+5}
 elif d==6:t={1,3,5,2*y+5,2*y+7,2*y+9,2*y+11}
 else:t={1,3,5,2*y+5}
 if r in t:return 2
 if d==0:p=even(r,6,s+2)
 elif d==1:p=even(r,6,s+3) or r>=s+4
 elif d==2:p=even(r,6,s)
 elif d==3:p=even(r,6,s+1) or r>=s+2
 elif d==4:p=even(r,6,s)
 elif d==5:p=even(r,6,s-1) or r>=s+1
 elif d==6:p=even(r,6,s-2)
 elif d>=7 and d%2:p=even(r,6,2*y+4) or odd(r,2*y+7,s+4) or r>=s+6
 else:p=even(r,6,2*y+4) or odd(r,2*y+7,s+5)
 return int(p)
def h6_y12(x,r):
 if r==0:return 0
 t={1,3,5}
 if x==12:t.add(27)
 elif x==16:t.add(29)
 elif x==19:t.update({31,33,35,37})
 elif x>=20:t.add(31)
 if r in t:return 2
 if x==12:p=odd(r,7,25)
 elif x==13:p=odd(r,7) or even(r,28)
 elif x==14:p=odd(r,7,27)
 elif x==15:p=odd(r,7) or even(r,30)
 elif x==16:p=odd(r,7,27)
 elif x==17:p=odd(r,7) or even(r,30)
 elif x==18:p=odd(r,7,29)
 elif x==19:p=odd(r,7,29) or even(r,32) or odd(r,39)
 elif x%2==0:p=odd(r,7,29) or even(r,32,x+18)
 else:p=odd(r,7,29) or even(r,32) or odd(r,x+20)
 return int(p)
def h6_y13(x,r):
 if r==0:return 0
 t={1,3,5}
 if x==13:t.add(29)
 elif x==17:t.add(31)
 elif x==20:t.update({33,35,37,39})
 elif x>=21:t.add(33)
 if r in t:return 2
 if x==13:p=odd(r,7,27)
 elif x==14:p=odd(r,7,27) or r>=29
 elif x==15:p=odd(r,7,29)
 elif x==16:p=odd(r,7,29) or r>=31
 elif x==17:p=odd(r,7,29)
 elif x==18:p=odd(r,7,29) or r>=31
 elif x==19:p=odd(r,7,31)
 elif x==20:p=odd(r,7,31) or even(r,34,38) or r>=40
 elif x%2==1:p=odd(r,7,31) or even(r,34,x+19)
 else:p=odd(r,7,31) or even(r,34,x+18) or r>=x+20
 return int(p)
SMALL={
13:{1:[(1,5,"01"),(7,27,"0"),(29,29,"01"),(31,31,"1")],0:[(2,6,"23"),(8,32,"1")]},
14:{1:[(1,5,"01"),(7,33,"0")],0:[(2,6,"23"),(8,28,"1"),(30,30,"023"),(32,32,"0")]},
15:{1:[(1,5,"01"),(7,29,"0"),(31,33,"1")],0:[(2,6,"23"),(8,34,"1")]},
16:{1:[(1,5,"01"),(7,35,"0")],0:[(2,6,"23"),(8,28,"1"),(30,30,"12"),(32,34,"0")]},
17:{1:[(1,5,"01"),(7,29,"0"),(31,31,"01"),(33,35,"1")],0:[(2,6,"23"),(8,36,"1")]},
18:{1:[(1,5,"01"),(7,37,"0")],0:[(2,6,"23"),(8,30,"1"),(32,32,"023"),(34,36,"0")]},
19:{1:[(1,5,"01"),(7,31,"0"),(33,37,"1")],0:[(2,6,"23"),(8,30,"1"),(32,38,"123")]},
20:{1:[(1,5,"01"),(7,31,"0"),(33,39,"01")],0:[(2,6,"23"),(8,30,"1"),(32,32,"123"),(34,38,"0")]},
21:{1:[(1,5,"01"),(7,31,"0"),(33,33,"01"),(35,39,"1")],0:[(2,6,"23"),(8,30,"1"),(32,32,"123"),(34,40,"02")]},
}
def expected_signature(x,r):
 if x in SMALL:rows=SMALL[x][r%2]
 else:
  assert x>=22
  if r%2:
   u=x+19 if x%2==0 else x+18
   rows=[(1,5,"01"),(7,31,"0"),(33,33,"01"),(35,u,"1")]
  else:
   v=x+18 if x%2==0 else x+19
   rows=[(2,6,"23"),(8,30,"1"),(32,32,"123"),(34,34,"02"),(36,v,"0")]
 for lo,hi,d in rows:
  if lo<=r<=hi and (r-lo)%2==0:return {int(c) for c in d}
 return set()
def actual_signature(x,r):
 if x==13:a=b=h6_y12(13,r-1)
 else:a=h6_y13(x-1,r-1);b=h6_y12(x,r-1)
 return {a,b,1^h5(x,13,r-1)}
def expected_t(x):
 t={1,3,5}
 if x==13:t.add(29)
 elif x==17:t.add(31)
 elif x==20:t.update({33,35,37,39})
 elif x>=21:t.add(33)
 return t
@lru_cache(None)
def ordered(r,tokens,z):
 if r==0:return 0
 opts=[]
 for i,t in enumerate(tokens):
  c=list(tokens)
  if t>=2:c[i]=t-1;zz=z
  else:c.pop(i);zz=z+1
  opts.append(ordered(r-1,tuple(c),zz))
 if z>=1:opts.append(1^ordered(r-1,tokens,z-1))
 return mex(opts)
@lru_cache(None)
def canonical(r,tokens,z):
 if r==0:return 0
 opts=[]
 for i,t in enumerate(tokens):
  c=list(tokens)
  if t>=2:c[i]=t-1;zz=z
  else:c.pop(i);zz=z+1
  opts.append(canonical(r-1,tuple(sorted(c,reverse=True)),zz))
 if z>=1:opts.append(1^canonical(r-1,tokens,z-1))
 return mex(opts)
def run_audit():
 fails=[];direct=0
 for x in range(13,41):
  for r in range(x+36):
   for z,t,f in ((6,(x,13),h6_y13(x,r)),(6,(x,12),h6_y12(x,r)),(5,(x,13),h5(x,13,r))):
    a=ordered(r,t,z);b=canonical(r,tuple(sorted(t,reverse=True)),z);direct+=1
    if a!=b or a!=f:fails.append({"kind":"direct","x":x,"r":r,"z":z,"tokens":t,"ordered":a,"canonical":b,"formula":f})
 sig=mexn=oddn=evenn=familyn=0
 for x in range(13,2001):
  obs=set()
  for r in range(1,x+20):
   a=actual_signature(x,r);e=expected_signature(x,r);sig+=1
   if a!=e:fails.append({"kind":"signature","x":x,"r":r,"actual":sorted(a),"expected":sorted(e)})
   v=mex(a);mexn+=1
   if v!=h6_y13(x,r):fails.append({"kind":"mex","x":x,"r":r,"actual":v,"formula":h6_y13(x,r)})
   if v==2:obs.add(r)
   if r%2:
    oddn+=1
    if not a<={0,1}:fails.append({"kind":"odd-bound","x":x,"r":r,"options":sorted(a)})
   else:
    evenn+=1
    if v>1:fails.append({"kind":"even-bound","x":x,"r":r,"value":v})
  familyn+=1
  if obs!=expected_t(x):fails.append({"kind":"family","x":x,"actual":sorted(obs),"expected":sorted(expected_t(x))})
 tailn=0
 for x in range(13,2001):
  for off in range(65):
   r=x+20+off;tailn+=1
   if h6_y13(x,r)!=(x+13)%2:fails.append({"kind":"tail","x":x,"r":r})
 rng=random.Random(20261117);randomn=0
 for _ in range(2000):
  x=rng.randint(13,100000);r=x+20+rng.randint(0,100000);randomn+=1
  if h6_y13(x,r)!=(x+13)%2:fails.append({"kind":"random-tail","x":x,"r":r})
 counts={"direct_ordered_canonical_formula_anchors":direct,"even_parent_bounds":evenn,"fixed_seed_random_tail":randomn,"mex":mexn,"odd_parent_bounds":oddn,"option_signatures":sig,"tail":tailn,"three_family_specialization":familyn}
 return {"schema":"two-token-z6-y13-audit-v1","claim":"H(R;(x,13);6) is given by the complete formula for all x>=13,R>=0","classification":"finite-independent-audit-not-proof","counts":counts,"total_checks":sum(counts.values()),"seed":20261117,"failures":fails,"pass":not fails}
def main():
 a=run_audit();encoded=json.dumps(a,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
 a["sha256_without_hash_field"]=hashlib.sha256(encoded.encode("utf-8")).hexdigest()
 out=Path(__file__).resolve().parent/"output"/"audit.json";out.parent.mkdir(parents=True,exist_ok=True)
 out.write_text(json.dumps(a,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"pass":a["pass"],"total_checks":a["total_checks"],"failures":len(a["failures"]),"sha256_without_hash_field":a["sha256_without_hash_field"]},sort_keys=True))
 if not a["pass"]:raise SystemExit(1)
if __name__=="__main__":main()
