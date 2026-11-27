"""Cone + frame double counting for the AG(2,9) s=2 cap game.

F = {(0,0),(1,0),(0,1)} (a 3-cap).  The cone (all caps containing F) is small;
the global size-layer Grundy distribution follows from transitivity of AGL(2,9)
on triangles and Grundy invariance: N_m(g) = N_3 * T_m(g) / C(m,3).
"""
import math, json
from collections import Counter, defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]
lines=(HERE/'output'/'board_ag2q9.txt').read_text().splitlines()
n,b=map(int,lines[0].split())
blocks=[]
for l in lines[1:]:
    m=0
    for p in list(map(int,l.split()[1:])): m|=1<<p
    blocks.append(m)
pc=[[] for _ in range(n)]
for c,m in enumerate(blocks):
    for p in range(n):
        if (m>>p)&1: pc[p].append(c)
F=(1<<0)|(1<<9)|(1<<1)
used=[False]*n; counts=[0]*len(blocks)
for p in range(n):
    if (F>>p)&1: used[p]=True
for p in range(n):
    if used[p]:
        for c in pc[p]: counts[c]+=1
order=[]
def dfs(mask,start):
    order.append(mask)
    for p in range(start,n):
        if used[p]: continue
        if any(counts[c]>=2 for c in pc[p]): continue
        used[p]=True
        for c in pc[p]: counts[c]+=1
        dfs(mask|(1<<p),p+1)
        for c in pc[p]: counts[c]-=1
        used[p]=False
dfs(F,0)
g={}
for m in sorted(order,key=lambda x:-x.bit_count()):
    ch=set()
    for p in range(n):
        if (m>>p)&1: continue
        nm=m|(1<<p)
        if nm in g: ch.add(g[nm])
    v=0
    while v in ch: v+=1
    g[m]=v
N3=81*80*72//6
T=Counter(); Tg=defaultdict(Counter)
for m in order:
    T[m.bit_count()]+=1; Tg[m.bit_count()][g[m]]+=1
res={'cone_size':len(order),'G3':g[F],'N3':N3,'sizes':{}}
for m in sorted(T):
    C=math.comb(m,3)
    res['sizes'][str(m)]={'T':T[m],'T_g':dict(Tg[m]),'N':N3*T[m]//C,
                          'N_g':{str(k):N3*v//C for k,v in Tg[m].items()}}
# k=0,1,2 by mex chain
res['sizes']['2']={'N':math.comb(81,2),'N_g':{'0':math.comb(81,2)}}
res['sizes']['1']={'N':81,'N_g':{'1':81}}
res['sizes']['0']={'N':1,'N_g':{'0':1}}
(HERE/'output'/'ag2q9_spectrum.json').write_text(json.dumps(res,indent=1))
print(json.dumps(res,indent=1))
