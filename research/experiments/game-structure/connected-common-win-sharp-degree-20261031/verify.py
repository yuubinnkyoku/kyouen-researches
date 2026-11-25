"""Exact common normal/misere winning openings: sharp degree bound family.
Run: python3 verify.py
"""
from functools import lru_cache


def mex(values):
    t = 0
    while t in values:
        t += 1
    return t


def edge_list(n):
    return [(a, b) for a in range(n) for b in range(a + 1, n)]


def evaluate_mask(n, edges):
    closed = [1 << i for i in range(n)]
    for a, b in edges:
        closed[a] |= 1 << b
        closed[b] |= 1 << a

    @lru_cache(None)
    def value(mask):
        if mask == 0:
            return 0, 1
        children = [value(mask & ~closed[i]) for i in range(n) if mask & (1 << i)]
        return mex({x for x, _ in children}), mex({y for _, y in children})

    full = (1 << n) - 1
    return value(full), [value(full & ~closed[i]) for i in range(n)]


def evaluate_named(n, edges):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)

    @lru_cache(None)
    def value(remaining):
        if not remaining:
            return 0, 1
        children = [value(remaining - frozenset((v,)) - adj[v]) for v in remaining]
        return mex({x for x, _ in children}), mex({y for _, y in children})

    full = frozenset(range(n))
    return value(full), [value(full - frozenset((i,)) - adj[i]) for i in range(n)]


def family(n):
    assert n >= 8
    return [(i, (i + 1) % 6) for i in range(6)] + [(0, 6), (6, 7)] + [(7, i) for i in range(8, n)]


def audit_six():
    pairs = edge_list(6)
    both_zero = []
    for graph in range(1 << len(pairs)):
        edges = [e for i, e in enumerate(pairs) if graph >> i & 1]
        if evaluate_mask(6, edges)[0] == (0, 0):
            both_zero.append(edges)
    assert len(both_zero) == 150, len(both_zero)
    degree_types = {}
    for edges in both_zero:
        adj = [set() for _ in range(6)]
        for a, b in edges:
            adj[a].add(b)
            adj[b].add(a)
        degs = tuple(sorted(len(a) for a in adj))
        degree_types[degs] = degree_types.get(degs, 0) + 1
        if degs == (2,)*6:
            seen = {0}
            stack = [0]
            while stack:
                for v in adj[stack.pop()]:
                    if v not in seen:
                        seen.add(v)
                        stack.append(v)
            assert len(seen) == 6  # C6, not two C3
        else:
            assert degs == (1, 1, 1, 1, 2, 2)
            assert not any(adj[i] & adj[j] for i in range(6)
                           for j in adj[i] if len(adj[i]) == 2 and len(adj[j]) == 2)
    assert degree_types == {(2,)*6: 60, (1,1,1,1,2,2): 90}, degree_types
    print('all six-vertex graphs:', 1 << len(pairs), 'zero-zero:', degree_types)


def audit_family():
    expected = {8: ((1, 1), [7]), 9: ((5, 5), [1, 5, 7]), 10: ((2, 2), [0, 7])}
    for n in range(8, 21):
        edges = family(n)
        a = evaluate_mask(n, edges)
        b = evaluate_named(n, edges)
        assert a == b, (n, a, b)
        root, children = a
        common = [i for i, v in enumerate(children) if v == (0, 0)]
        if n in expected:
            assert (root, common) == expected[n], (n, root, common)
        elif n % 2:
            assert (root, common) == ((5, 5), [1, 5, 7]), (n, root, common)
        else:
            assert (root, common) == ((2, 2), [0, 7]), (n, root, common)
        assert children[7] == (0, 0)
        assert len([v for v in edges if 7 in v]) == n - 7
        print(n, 'root', root, 'common', common)


if __name__ == '__main__':
    audit_six()
    audit_family()
    print('PASS: independent recursions, exact six-vertex base, sharp degree family')
