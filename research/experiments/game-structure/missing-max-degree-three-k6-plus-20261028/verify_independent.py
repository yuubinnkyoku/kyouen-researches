"""Independent small-instance checks for max-missing-degree-3, k=6.

Uses individual named vertices and direct closed-neighborhood deletion,
not the clique-subset quotient used by verify_k6.cpp.
"""
from functools import lru_cache

K = 6
EDGES = [(i, j) for i in range(K) for j in range(i + 1, K)]
# Canonical masks emitted by the standalone exhaustive verifier.
MASKS = [
    238, 246, 615, 619, 633, 685, 691, 693, 694, 700, 750,
    758, 760, 762, 921, 922, 954, 956, 1749, 1780, 1788,
    1880, 1881, 1884, 1916, 2012, 4060, 5872, 5905, 5907,
    5941, 5948, 7100,
]


def direct_grundy(missing, leaves, multiplicities):
    adj = [0] * K
    for i in range(K):
        for j in range(K):
            if i != j:
                adj[i] |= 1 << j
    for i, n in enumerate(leaves):
        for _ in range(n):
            v = len(adj)
            adj.append(1 << i)
            adj[i] |= 1 << v
    for e, (i, j) in enumerate(EDGES):
        if missing >> e & 1:
            assert multiplicities[e] == 0
            continue
        for _ in range(multiplicities[e]):
            v = len(adj)
            adj.append((1 << i) | (1 << j))
            adj[i] |= 1 << v
            adj[j] |= 1 << v

    @lru_cache(None)
    def g(state):
        if state == 0:
            return 0
        seen = set()
        bits = state
        while bits:
            b = bits & -bits
            bits -= b
            i = b.bit_length() - 1
            seen.add(g(state & ~((1 << i) | adj[i])))
        n = 0
        while n in seen:
            n += 1
        return n

    return g((1 << len(adj)) - 1)


def formula(leaves, multiplicities):
    u = sum(leaves) + sum(multiplicities)
    z = [
        leaves[i] + sum(
            multiplicities[e]
            for e, (a, b) in enumerate(EDGES)
            if i in (a, b)
        )
        for i in range(K)
    ]
    if all(v % 2 == z[0] % 2 for v in z):
        return 1 ^ (u % 2) ^ (z[0] % 2)
    return 2 + u % 2


def main():
    assert len(MASKS) == 33
    count = 0
    for D in MASKS:
        for seed in range(16):
            # Deterministic leaf multiplicities (0/1); all present pair types have one vertex.
            leaves = [
                ((seed * 17 + i * 23 + D * 7) >> (i % 5)) & 1
                for i in range(K)
            ]
            multiplicities = [0 if D >> e & 1 else 1 for e in range(15)]
            actual = direct_grundy(D, leaves, multiplicities)
            expected = formula(leaves, multiplicities)
            assert actual == expected, (D, seed, actual, expected)
            count += 1
    # Additional independent samples with positive even pair multiplicities.
    for D in MASKS:
        for seed in range(4):
            leaves = [(seed + i + D) % 2 for i in range(K)]
            multiplicities = [
                0 if D >> e & 1 else 1 + ((seed + e + D) % 2)
                for e in range(15)
            ]
            actual = direct_grundy(D, leaves, multiplicities)
            expected = formula(leaves, multiplicities)
            assert actual == expected, (D, seed, actual, expected)
            count += 1
    print(
        f"PASS: {count} independent named-vertex direct-recurrence "
        "instances across 33 missing graphs (including even pair multiplicities)"
    )


if __name__ == "__main__":
    main()
