"""Maximal-layer orbit census for the 3x3xm coplanar board.

Re-enumerates safe sets with the same Leibniz determinant predicate as
verify.py (generation only, no mex), then partitions the top layer
(K stones) under the box symmetry group D4 (square cross-section) x Z2
(length flip), order 16. Third, independent use of the group action:
verify.py embeds the same action for m=4 only.
"""
import sys, json
from itertools import combinations, permutations, product
m=int(sys.argv[1]); assert m in (4,5,6,7)
P=list(product(range(3),range(3),range(m))); n=len(P)
perms=list(permutations(range(4)))
signs={p:(-1 if sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2 else 1) for p in perms}
def det(ids):
    a=[(*P[i],1) for i in ids]
    return sum(signs[p]*a[0][p[0]]*a[1][p[1]]*a[2][p[2]]*a[3][p[3]] for p in perms)
blocked={}
for q in combinations(range(n),4):
    if det(q): continue
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
    levels.append(nxt)
sq=[lambda x,y:(x,y),lambda x,y:(x,2-y),lambda x,y:(2-x,y),lambda x,y:(2-x,2-y),
    lambda x,y:(y,x),lambda x,y:(y,2-x),lambda x,y:(2-y,x),lambda x,y:(2-y,2-x)]
trans=[]
for f in sq:
    for zf in (0,1):
        t=[]
        for (x,y,z) in P:
            nx,ny=f(x,y); nz=(m-1-z) if zf else z
            t.append(P.index((nx,ny,nz)))
        trans.append(t)
assert len(trans)==16
rem=set(levels[-1]); orbits=[]; reps=[]
while rem:
    s=next(iter(rem))
    orb={sum(1<<t[i] for i in range(n) if s>>i&1) for t in trans}
    assert orb<=set(levels[-1]); orbits.append(len(orb)); reps.append(min(orb)); rem-=orb
print(json.dumps({'m':m,'K':len(levels)-1,'top_layer':len(levels[-1]),
    'orbit_sizes':sorted(orbits),'num_orbits':len(orbits),
    'orbit_reps':[format(r,'x') for r in sorted(reps)]},sort_keys=True))
