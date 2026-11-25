"""Connected 8-vertex Node Kayles: common normal/misere winning openings."""
from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations


def values(n, edges):
    closed = [1 << i for i in range(n)]
    for a, b in edges:
        closed[a] |= 1 << b
        closed[b] |= 1 << a

    @lru_cache(None)
    def f(mask):
        if not mask:
            return (0, 1)
        children = [f(mask & ~closed[i]) for i in range(n) if mask >> i & 1]

        def mex(a):
            v = 0
            while v in a:
                v += 1
            return v

        return mex({p[0] for p in children}), mex({p[1] for p in children})

    full = (1 << n) - 1
    return f(full), [f(full & ~closed[i]) for i in range(n)]


def edge_bits(n, edges):
    return sum(1 << (a * (2*n-a-1)//2 + b-a-1)
               for u, v in edges for a, b in [tuple(sorted((u, v)))])


def six_edges(bits):
    return [(a, b) for a in range(6) for b in range(a+1, 6)
            if bits >> (a*(11-a)//2+b-a-1) & 1]


# All 60 labelled cycles and all 90 labelled disjoint pairs of 3-vertex paths.
cycles = {edge_bits(6, [(p[i], p[(i+1)%6]) for i in range(6)])
          for p in permutations(range(6))}
paths = set()
for A in combinations(range(6), 3):
    B = tuple(i for i in range(6) if i not in A)
    for a in A:
        for b in B:
            paths.add(edge_bits(6, [(a, v) for v in A if v != a] +
                                       [(b, v) for v in B if v != b]))
assert (len(cycles), len(paths)) == (60, 90)

# Enumerate all labelled connected graphs with a marked common-winning leaf.
# Prove uniqueness mathematically, then independently test no duplicates.
seen = set()
counts = Counter()
representatives = set()
for x in range(8):
    for y in range(8):
        if x == y:
            continue
        rest = [v for v in range(8) if v not in (x, y)]
        for kind, graphs in [('C6', cycles), ('2P3', paths)]:
            for bits in graphs:
                pairs = six_edges(bits)
                base = [(x, y)] + [(rest[a], rest[b]) for a, b in pairs]
                components = []
                if kind == '2P3':
                    adj = [set() for _ in range(6)]
                    for a, b in pairs:
                        adj[a].add(b)
                        adj[b].add(a)
                    component = {0}
                    stack = [0]
                    while stack:
                        for v in adj[stack.pop()]:
                            if v not in component:
                                component.add(v)
                                stack.append(v)
                    components = [component, set(range(6)) - component]
                for mask in range(1, 64):
                    if components and any(not any(mask >> i & 1 for i in c)
                                          for c in components):
                        continue
                    edges = base + [(y, rest[i]) for i in range(6) if mask >> i & 1]
                    encoded = edge_bits(8, edges)
                    assert encoded not in seen, ('duplicate', x, y, kind)
                    seen.add(encoded)
                    counts[kind] += 1
                    if x == 0 and y == 1:
                        # Every fixed-root labelled construction is checked.
                        root, children = values(8, edges)
                        assert children[0] == (0, 0)
                        assert [i for i, p in enumerate(children) if p == (0, 0)] == [0]
                        representatives.add((kind, root))
assert counts == {'C6': 211680, '2P3': 246960}
assert len(seen) == 458640
print('labelled connected graphs:', len(seen), dict(counts))
print('root (normal, misere) pairs:', sorted(representatives))


# Count rooted isomorphism types independently via residual automorphisms.
def canonical_cycle(mask):
    return min(sum(1 << ((a + d*i) % 6) for i in range(6) if mask >> i & 1)
               for a in range(6) for d in (-1, 1))


def canonical_path(mask):
    return min(mask, (mask & 2) | ((mask & 1) << 2) | ((mask & 4) >> 2))


bracelets = {canonical_cycle(mask) for mask in range(1, 64)}
path_types = {canonical_path(mask) for mask in range(1, 8)}
assert (len(bracelets), len(path_types)) == (12, 5)
assert 12 + len(path_types) * (len(path_types)+1) // 2 == 27
print('unlabelled connected graphs:', 12, '+', 15, '=', 27)
