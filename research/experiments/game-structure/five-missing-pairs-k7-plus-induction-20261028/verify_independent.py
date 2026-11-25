"""Independent k=5 complete base and named-vertex spot checks for k=6/7."""
from functools import lru_cache
from itertools import combinations, permutations, product
from random import Random


def predict(k, pairs, leaves):
    z = [x & 1 for x in leaves]
    u = sum(leaves) & 1
    for (i, j), n in pairs.items():
        z[i] ^= n & 1
        z[j] ^= n & 1
        u ^= n & 1
    return (1 ^ u ^ z[0]) if len(set(z)) == 1 else 2 + u


def quotient(k, pairs, leaves):
    signatures = [(1 << i) | (1 << j) for i, j in pairs]
    signatures += [1 << i for i in range(k)]
    counts = list(pairs.values()) + leaves
    z = 0
    for s, n in zip(signatures, counts):
        if n & 1:
            z ^= s

    @lru_cache(None)
    def grundy(mask):
        if mask == 0:
            return 0
        parity = sum(n for s, n in zip(signatures, counts) if s & mask) & 1
        options = {parity ^ ((z >> i) & 1) for i in range(k) if mask & (1 << i)}
        for s, n in zip(signatures, counts):
            if n and s & mask:
                child = mask & ~s
                parity_child = sum(v for ss, v in zip(signatures, counts) if ss & child) & 1
                options.add(grundy(child) ^ parity ^ parity_child ^ 1)
        g = 0
        while g in options:
            g += 1
        return g

    return grundy((1 << k) - 1)


def direct(k, pairs, leaves):
    neighbors = [sum(1 << j for j in range(k) if j != i) for i in range(k)]
    for (i, j), count in pairs.items():
        for _ in range(count):
            idx = len(neighbors)
            neighbors.append((1 << i) | (1 << j))
            neighbors[i] |= 1 << idx
            neighbors[j] |= 1 << idx
    for i, count in enumerate(leaves):
        for _ in range(count):
            idx = len(neighbors)
            neighbors.append(1 << i)
            neighbors[i] |= 1 << idx

    @lru_cache(None)
    def grundy(mask):
        choices = set()
        todo = mask
        while todo:
            bit = todo & -todo
            todo -= bit
            i = bit.bit_length() - 1
            choices.add(grundy(mask & ~(bit | neighbors[i])))
        g = 0
        while g in choices:
            g += 1
        return g

    return grundy((1 << len(neighbors)) - 1)


def test_k5_all_positive():
    k = 5
    edges = list(combinations(range(k), 2))
    covered = set()
    reps = []
    for missing in combinations(range(len(edges)), 5):
        if missing in covered:
            continue
        reps.append(missing)
        for perm in permutations(range(k)):
            mapped = tuple(sorted(
                edges.index(tuple(sorted((perm[edges[i][0]], perm[edges[i][1]]))))
                for i in missing
            ))
            covered.add(mapped)
    assert len(reps) == 6 and len(covered) == 252
    total = 0
    for missing in reps:
        remaining = [edge for i, edge in enumerate(edges) if i not in missing]
        for parities in product((1, 2), repeat=5):
            pairs = dict(zip(remaining, parities))
            for leaves in product((1, 2), repeat=5):
                leaves = list(leaves)
                assert quotient(k, pairs, leaves) == predict(k, pairs, leaves)
                total += 1
    assert total == 6144
    print("PASS k=5: 6 orbits, 6144 positive-leaf representatives")


def test_named_graphs():
    k = 6
    missing = {(0, i) for i in range(1, k)}
    pairs = {edge: 1 for edge in combinations(range(k), 2) if edge not in missing}
    # A 17-vertex failure, and the repaired graph with a center leaf.
    assert direct(k, pairs, [0, 1, 0, 0, 0, 0]) == 2
    assert predict(k, pairs, [0, 1, 0, 0, 0, 0]) == 3
    assert direct(k, pairs, [1, 1, 0, 0, 0, 0]) == predict(k, pairs, [1, 1, 0, 0, 0, 0]) == 2
    rng = Random(20261028)
    for k in (6, 7):
        edges = list(combinations(range(k), 2))
        for _ in range(12):
            missing = set(rng.sample(edges, 5))
            pairs = {edge: 1 for edge in edges if edge not in missing}
            leaves = [0] * k
            assert direct(k, pairs, leaves) == quotient(k, pairs, leaves)
            if k == 7:
                assert direct(k, pairs, leaves) == predict(k, pairs, leaves)
    print("PASS named-vertex direct checks: 2 witnesses + 24 sampled graphs")


if __name__ == "__main__":
    test_k5_all_positive()
    test_named_graphs()
