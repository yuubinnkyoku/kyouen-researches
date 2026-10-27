"""Independent Python quotient SG: all k=5 parity classes; k=6 deterministic samples.

The C++ exhaustive program uses the k=5 certified formula when evaluating k=6;
this Python implementation never shortcuts to the formula in its recursive solver.
"""
from functools import cache
from itertools import combinations, product
import random

PATTERNS = {
    'triangle': ((0,1),(0,2),(1,2)),
    'star': ((0,1),(0,2),(0,3)),
    'path4': ((0,1),(1,2),(2,3)),
    'path3_plus_edge': ((0,1),(1,2),(3,4)),
    'matching3': ((0,1),(2,3),(4,5)),
}

def norm(x):
    return 0 if x == 0 else (1 if x % 2 else 2)

@cache
def solve(leaves, edges):
    k = len(leaves)
    if not k:
        return 0
    # edges is a symmetric k-by-k matrix; zero diagonal.
    u = (sum(leaves) + sum(edges[i][j] for i in range(k) for j in range(i+1,k))) % 2
    options = set()
    for i in range(k):
        zi = (leaves[i] + sum(edges[i])) % 2
        options.add(u ^ zi)
        if leaves[i]:
            remain = [j for j in range(k) if j != i]
            new_leaves = tuple(norm(leaves[j] + edges[i][j]) for j in remain)
            new_edges = tuple(tuple(edges[a][b] for b in remain) for a in remain)
            options.add(solve(new_leaves, new_edges) ^ ((leaves[i]-1)%2))
    for i in range(k):
        for j in range(i+1,k):
            if not edges[i][j]:
                continue
            remain = [a for a in range(k) if a not in (i,j)]
            new_leaves = tuple(norm(leaves[a]+edges[i][a]+edges[j][a]) for a in remain)
            new_edges = tuple(tuple(edges[a][b] for b in remain) for a in remain)
            options.add(solve(new_leaves, new_edges) ^ ((leaves[i]+leaves[j]+edges[i][j]-1)%2))
    return next(i for i in range(16) if i not in options)

def predicted(leaves, edges):
    k = len(leaves)
    u = (sum(leaves) + sum(edges[i][j] for i in range(k) for j in range(i+1,k))) % 2
    z = [(leaves[i] + sum(edges[i])) % 2 for i in range(k)]
    return (1 ^ u ^ z[0]) if len(set(z)) == 1 else 2+u

def matrix(k, missing, pair_values):
    e = [[0]*k for _ in range(k)]
    pairs = [p for p in combinations(range(k),2) if p not in missing]
    for (i,j),value in zip(pairs,pair_values):
        e[i][j]=e[j][i]=value
    return tuple(map(tuple,e))

def run():
    total = 0
    for name,missing in PATTERNS.items():
        if name=='matching3':continue
        k=5
        pairs=[p for p in combinations(range(k),2) if p not in missing]
        count=0
        for values in product((1,2),repeat=len(pairs)):
            edges=matrix(k,missing,values)
            for leaves in product((0,1,2),repeat=k):
                got=solve(leaves,edges)
                assert got==predicted(leaves,edges),(k,name,values,leaves,got)
                count+=1
        total+=count
        print(f'k=5 {name} exact={count}',flush=True)
    rng=random.Random(20261028)
    for name,missing in PATTERNS.items():
        k=6
        pairs=[p for p in combinations(range(k),2) if p not in missing]
        for _ in range(150):
            edges=matrix(k,missing,[rng.choice((1,2)) for p in pairs])
            leaves=tuple(rng.randrange(3) for _ in range(k))
            got=solve(leaves,edges)
            assert got==predicted(leaves,edges),(k,name,leaves,got)
        total+=150
        print(f'k=6 {name} independent_full_recursion=150',flush=True)
    print(f'PASS total={total} cached_states={solve.cache_info().currsize}')

# Separate, literal named-vertex Node Kayles recursion (no signature quotient).
def direct_named(leaves,edges):
    k=len(leaves)
    nbr=[0]*k
    for i in range(k):
        for j in range(k):
            if i!=j:nbr[i]|=1<<j
    for i in range(k):
        for _ in range(leaves[i]):
            a=len(nbr);nbr.append(1<<i);nbr[i]|=1<<a
    for i in range(k):
        for j in range(i+1,k):
            for _ in range(edges[i][j]):
                a=len(nbr);nbr.append((1<<i)|(1<<j));nbr[i]|=1<<a;nbr[j]|=1<<a
    @cache
    def rec(mask):
        if not mask:return 0
        opts=set(); m=mask
        while m:
            bit=m&-m;i=bit.bit_length()-1;m-=bit
            opts.add(rec(mask&~(nbr[i]|bit)))
        return next(g for g in range(16) if g not in opts)
    return rec((1<<len(nbr))-1)

def run_direct():
    rng=random.Random(130072)
    count=0
    for k in (5,6):
        for name,missing in PATTERNS.items():
            if k==5 and name=='matching3':continue
            pairs=[p for p in combinations(range(k),2) if p not in missing]
            for _ in range(24):
                edges=matrix(k,missing,[1]*len(pairs))
                leaves=tuple(rng.randrange(2) for _ in range(k))
                got=direct_named(leaves,edges)
                want=predicted(leaves,edges)
                assert got==want,(k,name,leaves,got,want)
                count+=1
    print(f'PASS named-vertex-direct={count}',flush=True)

if __name__=='__main__':
    run()
    run_direct()
