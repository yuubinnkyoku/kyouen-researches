"""Top-layer orbit census for the 3x3xm coplanar board, from a mask dump.

orbits.py re-enumerates all levels in Python, which is infeasible for
m=8 (102M states). This variant reads the maximum-size layer dumped by
enum2_128.cpp (one "hi lo" uint64 pair per line, point order x,y,z --
the same labelling as orbits.py's P), and partitions it under the box
symmetry group D4 (square cross-section) x Z2 (length flip), order 16.
Validated by reproducing orbits_m7.json from an enum2_128 m=7 dump.
"""
import sys, json
from itertools import product
m=int(sys.argv[1]); path=sys.argv[2]
P=list(product(range(3),range(3),range(m))); n=len(P)
idx={q:i for i,q in enumerate(P)}
top=set()
for ln in open(path):
    hi,lo=ln.split(); top.add((int(hi)<<64)|int(lo))
sq=[lambda x,y:(x,y),lambda x,y:(x,2-y),lambda x,y:(2-x,y),lambda x,y:(2-x,2-y),
    lambda x,y:(y,x),lambda x,y:(y,2-x),lambda x,y:(2-y,x),lambda x,y:(2-y,2-x)]
trans=[]
for f in sq:
    for zf in (0,1):
        t=[]
        for (x,y,z) in P:
            nx,ny=f(x,y); nz=(m-1-z) if zf else z
            t.append(idx[(nx,ny,nz)])
        trans.append(t)
assert len(trans)==16
rem=set(top); orbits=[]; reps=[]
while rem:
    s=next(iter(rem))
    orb={sum(1<<t[i] for i in range(n) if s>>i&1) for t in trans}
    assert orb<=top; orbits.append(len(orb)); reps.append(min(orb)); rem-=orb
print(json.dumps({'m':m,'K':9,'top_layer':len(top),
    'orbit_sizes':sorted(orbits),'num_orbits':len(orbits),
    'orbit_reps':[format(r,'x') for r in sorted(reps)]},sort_keys=True))
