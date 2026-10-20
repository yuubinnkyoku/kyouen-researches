import sys,collections
from pathlib import Path
from itertools import combinations
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"n11-s11-dual-branch-optimality-20261019"))
import compact_proof184_342 as v

def sig(m):
 base=v.points(m); moves=v.legal(m); n=len(moves);bad=[]
 for i,j in combinations(range(n),2):
  if any(v.circle(a,b,moves[i],moves[j]) for a,b in combinations(base,2)):bad.append((1<<i)|(1<<j))
 for i,j,k in combinations(range(n),3):
  e=(1<<i)|(1<<j)|(1<<k)
  if any(e&b==b for b in bad):continue
  if any(v.circle(a,moves[i],moves[j],moves[k]) for a in base):bad.append(e)
 for ids in combinations(range(n),4):
  e=sum(1<<i for i in ids)
  if any(e&b==b for b in bad):continue
  if v.circle(*(moves[i] for i in ids)):bad.append(e)
 return n,tuple(sorted(bad))
