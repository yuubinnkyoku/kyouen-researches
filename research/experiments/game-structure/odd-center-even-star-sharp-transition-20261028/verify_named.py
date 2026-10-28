"""Independent named-vertex Node Kayles check for the parity-star family.

No quotient, family recurrence, or symmetry reduction is used in the solver.
"""
from functools import lru_cache
from itertools import product


def direct(p, m, a, pair_counts, private_counts):
    k = 1 + p + m
    adj = [0] * k

    def edge(i, j):
        adj[i] |= 1 << j
        adj[j] |= 1 << i

    for i in range(k):
        for j in range(i):
            edge(i, j)

    def independent(neighbors):
        v = len(adj)
        adj.append(0)
        for w in neighbors:
            edge(v, w)

    for _ in range(a):
        independent((0,))
    for i, r in enumerate(pair_counts, 1):
        for _ in range(r):
            independent((0, i))
    for i, t in enumerate(private_counts, p + 1):
        for _ in range(t):
            independent((i,))

    closed = [neighbors | (1 << v) for v, neighbors in enumerate(adj)]

    @lru_cache(None)
    def sg(mask):
        if not mask:
            return 0
        values = set()
        remaining = mask
        while remaining:
            bit = remaining & -remaining
            v = bit.bit_length() - 1
            values.add(sg(mask & ~closed[v]))
            remaining ^= bit
        answer = 0
        while answer in values:
            answer += 1
        return answer

    return sg((1 << len(adj)) - 1), len(adj), sg.cache_info().currsize


def expected(p, m):
    if p + m == 0:
        return 1
    return 2 if p >= 3 else 3


def main():
    checked = 0
    maximum_states = 0
    for p in range(5):
        for m in range(3):
            for a in (1, 3):
                for rs in product((2, 4), repeat=p):
                    for ts in product((2, 4), repeat=m):
                        vertices = 1 + p + m + a + sum(rs) + sum(ts)
                        if vertices > 18:
                            continue
                        actual, count, states = direct(p, m, a, rs, ts)
                        assert count == vertices
                        assert actual == expected(p, m), (p, m, a, rs, ts, actual)
                        checked += 1
                        maximum_states = max(maximum_states, states)
    print(f"nonuniform exhaustive small cases: {checked}; max states: {maximum_states}")
    assert checked == 129

    extra = 0
    for p in range(5, 8):
        for m in range(3):
            vertices = 1 + p + m + 1 + 2 * p + 2 * m
            if vertices > 25:
                continue
            actual, count, states = direct(p, m, 1, (2,) * p, (2,) * m)
            assert count == vertices
            assert actual == expected(p, m), (p, m, actual)
            maximum_states = max(maximum_states, states)
            extra += 1
    assert extra == 6
    print(f"larger uniform cases: {extra}; total: {checked + extra}; max states: {maximum_states}")
    print("PASS")


if __name__ == "__main__":
    main()
