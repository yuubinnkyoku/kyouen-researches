"""Exhaustive affine-rank-2 four-point avoidance on {0,1}^4."""
from itertools import product, combinations
from collections import Counter
from functools import lru_cache

points = list(product(range(2), repeat=4))
def determinant(a):
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
            -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
            +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))
def coplanar(q):
    base=points[q[0]]
    vectors=[[points[i][j]-base[j] for j in range(4)] for i in q[1:]]
    return all(determin([[row[j] for j in cols] for row in vectors])==0
               for cols in combinations(range(4),3))
forbidden=[sum(1<<i for i in q) for q in combinations(range(16),4) if coplanar(q)]
safe=[False]*65536
safe[0]=True
for mask in range(1,65536):
    safe[mask]=safe[mask&(mask-1)] and all((mask&e)!=e for e in forbidden)
@lru_cache(None)
def grundy(mask):
    children={grundy(mask|(1<<i)) for i in range(16) if not mask>>i&1 and safe[mask|(1<<i)]}
    return next(k for k in range(17) if k not in children)
@lru_cache(None)
def misere_win(mask):
    children=[misere_win(mask|(1<<i)) for i in range(16) if not mask>>i&1 and safe[mask|(1<<i)]]
    return not children or not all(children)
layers=Counter()
maximal=Counter()
for mask in range(65536):
    if not safe[mask]:continue
    layers[mask.bit_count()]+=1
    if not any(safe[mask|(1<<i)] for i in range(16) if not mask>>i&1):
        maximal[mask.bit_count()]+=1
print("forbidden",len(forbidden),"safe",sum(safe))
print("layers",sorted(layers.items()))
print("maximal",sorted(maximal.items()))
print("root grundy",grundy(0),"root misere win",misere_win(0))
print("first children",Counter((grundy(1<<i),misere_win(1<<i)) for i in range(16)))
assert len(forbidden)==100 and sum(safe)==8193
assert dict(maximal)=={6:1008,7:240}
assert grundy(0)==0 and not misere_win(0)
