"""Independent named-vertex Node Kayles verification.

Constructs every vertex separately and recursively deletes closed
neighborhoods. Does not use the clique-subset parity recurrence.
"""
from functools import lru_cache
from random import Random


def graph(k, leaves, pairs):
    adj = [0] * k
    for i in range(k):
        for j in range(i + 1, k):
            adj[i] |= 1 << j
            adj[j] |= 1 << i
    for i, n in enumerate(leaves):
        for _ in range(n):
            idx = len(adj)
            adj.append(1 << i)
            adj[i] |= 1 << idx
    for (i, j), n in sorted(pairs.items()):
        for _ in range(n):
            idx = len(adj)
            adj.append((1 << i) | (1 << j))
            adj[i] |= 1 << idx
            adj[j] |= 1 << idx
    return adj


def exact_named(adj):
    closed = [m | (1 << i) for i, m in enumerate(adj)]

    @lru_cache(maxsize=None)
    def sg(state):
        seen = set()
        v = state
        while v:
            b = v & -v
            i = b.bit_length() - 1
            seen.add(sg(state & ~closed[i]))
            v ^= b
        g = 0
        while g in seen:
            g += 1
        return g

    return sg((1 << len(adj)) - 1), sg.cache_info().currsize


def formula(k, leaves, pairs):
    u = sum(leaves) + sum(pairs.values())
    z = [leaves[i] for i in range(k)]
    for (i, j), v in pairs.items():
        z[i] += v
        z[j] += v
    u &= 1
    z = [v & 1 for v in z]
    return (1 ^ u ^ z[0]) if len(set(z)) == 1 else (2 + u)


def main():
    rng = Random(20261028)
    total_states = 0
    k = 7
    for rep in range(16):
        missing = {(i, j) for i in range(5) for j in range(i + 1, 5)}
        # Both H=2K1 and H=K2 are covered.
        if rng.randrange(2):
            missing.add((5, 6))
        leaves = [rng.randrange(2) for _ in range(k)]
        pairs = {
            (i, j): (2 if rng.randrange(12) == 0 else 1)
            for i in range(k) for j in range(i + 1, k)
            if (i, j) not in missing
        }
        got, states = exact_named(graph(k, leaves, pairs))
        want = formula(k, leaves, pairs)
        assert got == want, (rep, missing, leaves, pairs, got, want)
        total_states += states
    print(f"k=7: 16 named-vertex samples passed")
    print(f"total named-vertex memo states: {total_states}")


if __name__ == "__main__":
    main()
