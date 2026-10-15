from collections import defaultdict, Counter
from itertools import combinations
from pathlib import Path
lines=(Path(__file__).resolve().parent.parent/'output/q48_circle_census_2000000_20261015.csv').read_text().splitlines()
patterns=[(1,3,3,1)]
for l in lines:
 p=tuple(map(int,l.split(',')))
 patterns.extend((p,p[::-1]))
patterns=sorted(set(patterns))
N=len(patterns)
P=[]
for p in patterns:
 D=max(p)
 P.append(frozenset(((D-d)//2,y) for y,d in enumerate(p))|frozenset(((D+d)//2,y) for y,d in enumerate(p)))
# overlap of A at 0, B at t. shifts only where overlap >=1
pair={}
for i in range(N):
 for j in range(N):
  shift=set(x-x2 for x,y in P[i] for x2,y2 in P[j] if y==y2)
  pair[i,j]=[(t,len(P[i]&{(x+t,y) for x,y in P[j]})) for t in shift if len(P[i]&{(x+t,y) for x,y in P[j]})>=1]
print('templates',N,'pair intersections',sum(len(x) for x in pair.values()),flush=True)
minunion=24
mincases=[]
union_counts=Counter()
triples20=0
for i in range(N):
 for j in range(N):
  for t,ij in pair[i,j]:
   if ij<1:continue
   PB=frozenset((x+t,y) for x,y in P[j])
   AB=P[i]|PB
   for k in range(N):
    for u,ik in pair[i,k]:
     if ik<1:continue
     PC=frozenset((x+u,y) for x,y in P[k])
     if len(PB&PC)==0:continue
     # distinct circles (templates plus shift unique)
     if (i,0)==(j,t) or (i,0)==(k,u) or (j,t)==(k,u):continue
     union=len(AB|PC)
     union_counts[union]+=1
     if union<minunion:
      minunion=union;mincases=[(i,j,k,t,u)]
     elif union==minunion and len(mincases)<15:
      mincases.append((i,j,k,t,u))
print('minimum',minunion,'mincases',mincases)
print('counts',sorted(union_counts.items()))
