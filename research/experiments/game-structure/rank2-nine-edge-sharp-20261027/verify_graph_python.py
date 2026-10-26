#!/usr/bin/env python3
"""Independent Python verifier for simple graphs with 1..9 edges.

No third-party packages. Exhaustive graph generation is by adjoining one edge,
followed by exact graph isomorphism testing. SG uses *occupied independent sets*,
not the available-vertex deletion recurrence of the C++ verifier.
"""
from collections import Counter, defaultdict
from functools import lru_cache

EXPECTED = {
    1: (1, (0, 1)),
    2: (2, (1, 0, 1)),
    3: (5, (1, 3, 0, 1)),
    4: (11, (5, 1, 3, 2)),
    5: (26, (5, 10, 4, 7)),
    6: (68, (22, 15, 18, 13)),
    7: (177, (43, 55, 33, 43, 3)),
    8: (497, (136, 121, 118, 105, 14, 3)),
    9: (1476, (366, 405, 309, 309, 56, 28, 3)),
}

def signature(adj):
    degrees = tuple(sorted(x.bit_count() for x in adj))
    remaining = set(range(len(adj)))
    components = []
    while remaining:
        root = next(iter(remaining))
        todo = [root]
        remaining.remove(root)
        vertices = []
        while todo:
            v = todo.pop()
            vertices.append(v)
            for u in list(remaining):
                if adj[v] & (1 << u):
                    remaining.remove(u)
                    todo.append(u)
        components.append((len(vertices), sum(adj[v].bit_count() for v in vertices) // 2))
    return (len(adj), degrees, tuple(sorted(components)))

def isomorphic(a, b):
    n = len(a)
    degrees_a = [x.bit_count() for x in a]
    degrees_b = [x.bit_count() for x in b]
    order = sorted(range(n), key=lambda i: (-degrees_a[i],
                   -sum(degrees_a[j] for j in range(n) if a[i] & (1 << j))))
    mapping = [-1] * n
    used = [False] * n

    def dfs(k):
        if k == n:
            return True
        u = order[k]
        for v in range(n):
            if used[v] or degrees_a[u] != degrees_b[v]:
                continue
            if any(bool(a[u] & (1 << order[j])) !=
                   bool(b[v] & (1 << mapping[order[j]])) for j in range(k)):
                continue
            mapping[u] = v
            used[v] = True
            if dfs(k + 1):
                return True
            used[v] = False
            mapping[u] = -1
        return False

    return dfs(0)

def grundy_occupied(adj):
    n = len(adj)

    @lru_cache(None)
    def recurse(chosen):
        reachable = set()
        for v in range(n):
            if chosen & (1 << v):
                continue
            if adj[v] & chosen:
                continue
            reachable.add(recurse(chosen | (1 << v)))
        g = 0
        while g in reachable:
            g += 1
        return g

    return recurse(0)

def generate(prev):
    buckets = defaultdict(list)
    for a in prev:
        n = len(a)
        candidates = [(i, j) for i in range(n) for j in range(i + 1, n)
                      if not a[i] & (1 << j)]
        candidates += [(i, n) for i in range(n)]
        candidates.append((n, n + 1))
        for u, v in candidates:
            b = list(a) + [0] * (max(u, v) + 1 - n)
            b[u] |= 1 << v
            b[v] |= 1 << u
            b = tuple(b)
            key = signature(b)
            if not any(isomorphic(b, old) for old in buckets[key]):
                buckets[key].append(b)
    return [g for group in buckets.values() for g in group]

def main():
    # Separate occupied-set recurrence for the sharp 9-edge / 11-vertex example.
    witness_edges = ((0, 1), (0, 2), (0, 3), (1, 4), (2, 4),
                     (3, 5), (4, 6), (7, 8), (7, 9))
    witness = [0] * 11
    for u, v in witness_edges:
        witness[u] |= 1 << v
        witness[v] |= 1 << u
    assert grundy_occupied(tuple(witness[:10])) == 6
    assert grundy_occupied(tuple(witness)) == 7
    graphs = [()]
    for e in range(1, 10):
        graphs = generate(graphs)
        counts = Counter(grundy_occupied(g) for g in graphs)
        actual = tuple(counts[i] for i in range(max(counts) + 1))
        assert (len(graphs), actual) == EXPECTED[e], (e, len(graphs), actual)
        print(f'edges={e} graphs={len(graphs)} grundy={actual}', flush=True)

if __name__ == '__main__':
    main()
