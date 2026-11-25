"""Independent checks for normal/misere Node Kayles and r-player lengths on complete multipartite graphs.
Run: python3 verify.py (stdlib only).
"""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import product
from math import factorial


def mex(vals):
    s = set(vals)
    k = 0
    while k in s:
        k += 1
    return k


def build_graph(sizes):
    parts = [tuple(range(sum(sizes[:i]), sum(sizes[:i+1]))) for i in range(len(sizes))]
    n = sum(sizes)
    adjacency = [0] * n
    for i, part in enumerate(parts):
        for v in part:
            adjacency[v] = sum(1 << w for j, p in enumerate(parts) if j != i for w in p)
    return adjacency, parts


def direct_bitmask(adj):
    n = len(adj)
    @lru_cache(None)
    def solve(mask):
        if not mask:
            return 0, 1, {0: Fraction(1)}
        children = []
        for v in range(n):
            if mask & (1 << v):
                child = mask & ~(adj[v] | (1 << v))
                children.append(solve(child))
        g = mex(x[0] for x in children)
        h = mex(x[1] for x in children)
        dist = Counter()
        for _, _, d in children:
            for length, prob in d.items():
                dist[length + 1] += prob / len(children)
        return g, h, dict(dist)
    return solve((1 << n) - 1)


def direct_named(adj):
    n = len(adj)
    edges = frozenset((a,b) for a in range(n) for b in range(a+1,n) if adj[a] >> b & 1)
    @lru_cache(None)
    def rec(vertices):
        if not vertices:
            return (0,1)
        vals=[]
        for x in vertices:
            remaining = tuple(v for v in vertices if v != x and
                              (min(v,x),max(v,x)) not in edges)
            vals.append(rec(remaining))
        return mex(v[0] for v in vals), mex(v[1] for v in vals)
    return rec(tuple(range(n)))


def formula(sizes):
    if not sizes:
        return 0, 1, {0: Fraction(1)}, 1
    odd = any(v % 2 for v in sizes)
    even = any(v % 2 == 0 for v in sizes)
    g = 2 if odd and even else (1 if odd else 0)
    h = 2 if odd and even else (0 if odd else 1)
    N = sum(sizes)
    d = Counter()
    for v in sizes:
        d[v] += Fraction(v,N)
    count = sum(factorial(v) for v in sizes)
    return g, h, dict(d), count


def direct_paths(adj):
    n = len(adj)
    @lru_cache(None)
    def paths(mask):
        if mask == 0:
            return {0: 1}
        d = Counter()
        for v in range(n):
            if mask >> v & 1:
                child = mask & ~(adj[v] | (1 << v))
                for length, count in paths(child).items():
                    d[length+1] += count
        return dict(d)
    return paths((1<<n)-1)


def main():
    checked = 0
    checked_paths = 0
    for k in range(0, 6):
        for sizes in product(range(1, 5), repeat=k):
            if sum(sizes) > 12:
                continue
            adj, parts = build_graph(sizes)
            g,h,d,cnt = formula(sizes)
            a,b,e = direct_bitmask(adj)
            assert (a,b,e) == (g,h,d), (sizes,(a,b,e),(g,h,d))
            assert direct_named(adj) == (g,h), sizes
            for i,part in enumerate(parts):
                for v in part:
                    child = tuple(w for w in range(len(adj)) if w != v and not (adj[v] >> w & 1))
                    adj_child = [sum((1 << j) for j,z in enumerate(child) if adj[w] >> z & 1) for w in child]
                    cg,ch,_ = direct_bitmask(adj_child)
                    assert (cg==0) == (sizes[i]%2==1)
                    assert (ch==0) == (sizes[i]%2==0)
            checked += 1
            if sum(sizes) <= 9:
                pathdist = direct_paths(adj)
                assert sum(pathdist.values()) == cnt, (sizes,pathdist,cnt)
                assert pathdist == ({t: sum(factorial(v) for v in sizes if v == t) for t in set(sizes)} if sizes else {0: 1}), (sizes,pathdist)
                assert set(pathdist) == set(d)
                for r in range(2, 8):
                    observed = {j: sum(c for t,c in pathdist.items() if (t-1) % r == j) for j in range(r)}
                    expected = {j: sum(factorial(t) for t in sizes if (t-1) % r == j) + (1 if not sizes and j == (r-1) else 0) for j in range(r)}
                    assert observed == expected
                checked_paths += 1
    print(f"PASS: {checked} labeled part-size sequences (k<=5, 1<=n_i<=4, total<=12)")
    print(f"PASS: {checked_paths} exact path-count enumerations (total<=9)")
    print("PASS: two independent mex implementations, uniform-play probabilities, winning openings, exact sequence count")
    print("Example K_(2,3,4): (g,h) =", formula((2,3,4))[:2], "; random lengths =", formula((2,3,4))[2])

if __name__ == '__main__':
    main()
