#!/usr/bin/env python3
"""Independent exact recurrences for a 13-vertex degree-two split witness."""
from functools import lru_cache

C = 5
NEIGHBOR_MASKS = (1, 3, 3, 5, 5, 9, 9, 16)
N = C + len(NEIGHBOR_MASKS)


def adjacency():
    adj = [((1 << C) - 1) for _ in range(C)]
    for i, mask in enumerate(NEIGHBOR_MASKS, start=C):
        adj.append((1 << i) | mask)
        for c in range(C):
            if mask & (1 << c):
                adj[c] |= 1 << i
    return tuple(adj)


def mex(values):
    value = 0
    while value in values:
        value += 1
    return value


def verify():
    adj = adjacency()
    assert len(adj) == 13
    assert all(mask.bit_count() <= 2 for mask in NEIGHBOR_MASKS)
    assert all(not (adj[i] & (1 << j)) for i in range(C, N) for j in range(i + 1, N))

    @lru_cache(None)
    def remaining(mask):
        return mex({remaining(mask & ~adj[v]) for v in range(N) if mask & (1 << v)})

    @lru_cache(None)
    def occupied(mask):
        blocked = 0
        for v in range(N):
            if mask & (1 << v):
                blocked |= adj[v]
        return mex({occupied(mask | (1 << v)) for v in range(N) if not (blocked & (1 << v))})

    all_vertices = (1 << N) - 1
    children_a = tuple(remaining(all_vertices & ~adj[v]) for v in range(N))
    children_b = tuple(occupied(1 << v) for v in range(N))
    expected = (1, 0, 0, 0, 1, 3, 3, 3, 3, 3, 3, 3, 2)
    assert children_a == children_b == expected, (children_a, children_b)
    assert remaining(all_vertices) == occupied(0) == 4
    for v in range(C, N):
        assert remaining(all_vertices & ~(1 << v)) <= 3
    print('vertices=13 clique=5 independent=8 independent_max_degree=2')
    print('child_values=', children_a)
    print('grundy=4')
    print('independent_recursions=2 all_checks_passed')
    print('memo_states=', remaining.cache_info().currsize, occupied.cache_info().currsize)


if __name__ == '__main__':
    verify()
