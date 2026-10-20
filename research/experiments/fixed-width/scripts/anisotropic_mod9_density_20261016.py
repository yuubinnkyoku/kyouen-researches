#!/usr/bin/env python3
"""Complete mod-9 residue audit; independent polynomial/recurrence checks."""
from collections import Counter
from math import ceil
Q={x*x%9 for x in range(9)}
assert Q=={0,1,4,7}
patterns=[]
for a in range(9):
    for b in range(9):
        f,delta=a,b-a
        rec=[]
        for i in range(90):
            rec.append(f%9)
            f+=delta
            delta-=8
        pol=[(a+i*(b-a)-4*i*(i-1))%9 for i in range(90)]
        assert rec==pol
        assert all(rec[i]==rec[i%9] for i in range(90))
        patterns.append([int(x in Q) for x in rec[:9]])
hist=Counter(sum(p) for p in patterns)
assert hist=={0:18,3:9,5:27,6:27}
maxima=[]
for w in range(5,14):
    mx=max(sum(p[(s+i)%9] for i in range(w)) for p in patterns for s in range(9))
    maxima.append(mx)
    assert mx<=ceil(2*w/3)
assert maxima==[4,4,5,6,6,7,8,8,9]
print('PASS',dict(sorted(hist.items())),maxima)
