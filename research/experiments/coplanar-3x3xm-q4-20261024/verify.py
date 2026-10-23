"""Leibniz 4x4 determinant; increasing-order safe-set enumeration; reverse mex."""
import sys, json
from itertools import combinations, permutations, product
from collections import Counter
m=int(sys.argv[1]); assert 1<=m<=3
P=list(product(range(3),range(3),range(m))); n=len(P)
perms=list(permutations(range(4)))
signs={p:(-1 if sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2 else 1) for p in perms}
def det(ids):
    a=[(*P[i],1) for i in ids]
    return sum(signs[p]*a[0][p[0]]*a[1][p[1]]*a[2][p[2]]*a[3][p[3]] for p in perms)
blocked={}; forbidden=0
for q in combinations(range(n),4):
    if det(q): continue
    forbidden+=1
    for t in combinations(q,3):
        v=next(i for i in q if i not in t)
        blocked[t]=blocked.get(t,0)|(1<<v)
levels=[[0]]
while True:
    nxt=[]
    for s in levels[-1]:
        ids=[i for i in range(n) if s>>i&1]
        bad=0
        for t in combinations(ids,3):bad|=blocked.get(t,0)
        for v in range(ids[-1]+1 if ids else 0,n):
            if not bad>>v&1:nxt.append(s|(1<<v))
    if not nxt:break
    assert len(nxt)==len(set(nxt))
    levels.append(nxt)
sets=list(map(set,levels)); g={}; h={}; terminal=Counter()
for k in range(len(levels)-1,-1,-1):
    for s in levels[k]:
        nxt=sets[k+1] if k+1<len(levels) else set()
        children=[s|(1<<i) for i in range(n) if not s>>i&1 and (s|(1<<i)) in nxt]
        if not children:terminal[k]+=1
        vals={g[t] for t in children}; x=0
        while x in vals:x+=1
        g[s]=x
        vals={h[t] for t in children}; x=1 if not children else 0
        while x in vals:x+=1
        h[s]=x
orbits=[]
if m==3:
    rem=set(levels[-1]); trans=[]
    for ax in permutations(range(3)):
        for flip in product((0,1),repeat=3):
            trans.append([P.index(tuple(2-P[i][ax[j]] if flip[j] else P[i][ax[j]] for j in range(3))) for i in range(n)])
    while rem:
        s=next(iter(rem))
        orb={sum(1<<t[i] for i in range(n) if s>>i&1) for t in trans}
        assert orb<=set(levels[-1]);orbits.append(len(orb));rem-=orb
print(json.dumps({'m':m,'forbidden':forbidden,'safe':sum(map(len,levels)),
    'layers':list(map(len,levels)),'terminal':dict(terminal),
    'K':len(levels)-1,'s':min(terminal),'g_root':g[0],'h_root':h[0],
    'g_hist':dict(Counter(g.values())),'h_hist':dict(Counter(h.values())),
    'first_moves':{str(P[i]):[g[1<<i],h[1<<i]] for i in range(n)},
    'max_orbits':sorted(orbits)},sort_keys=True))
