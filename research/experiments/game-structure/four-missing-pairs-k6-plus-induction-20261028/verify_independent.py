"""Independent checks for the four-missing-pair k>=6 theorem.

(1) Enumerate all 10,368 normalized k=5 star configurations with a
    positive private leaf at the star centre (the only exceptional child
    needed in the k=7 induction).
(2) Compare literal named-vertex closed-neighbourhood deletion with a
    separate clique-mask recurrence for 27 k=6 configurations.
The full 13,436,928-case k=6 enumeration is in verify_k6.cpp.
"""
from functools import cache
from itertools import combinations, product

K6_MISSING = (
    (0, 1, 2, 3), (0, 1, 2, 5), (0, 1, 2, 7),
    (0, 1, 2, 14), (0, 1, 5, 12), (0, 1, 6, 9),
    (0, 1, 6, 10), (0, 1, 6, 14), (0, 1, 12, 13),
)


def quotient(k, pairs, leaves):
    counts = {1 << i: leaves[i] for i in range(k)}
    counts.update({(1 << i) | (1 << j): n for (i, j), n in pairs.items()})
    active = [0] * (1 << k)
    z = [0] * k
    for sig, n in counts.items():
        if n % 2:
            for mask in range(1, 1 << k):
                if sig & mask:
                    active[mask] ^= 1
            for i in range(k):
                if sig & (1 << i):
                    z[i] ^= 1
    dp = [0] * (1 << k)
    for mask in range(1, 1 << k):
        seen = set()
        for i in range(k):
            if mask & (1 << i):
                seen.add(active[mask] ^ z[i])
        for sig, n in counts.items():
            if n and (mask & sig):
                child = mask & ~sig
                seen.add(dp[child] ^ active[mask] ^ active[child] ^ 1)
        g = 0
        while g in seen:
            g += 1
        dp[mask] = g
    u = active[-1]
    predicted = (1 ^ u ^ z[0]) if len(set(z)) == 1 else 2 + u
    return dp[-1], predicted


def named(k, pairs, leaves):
    """Literal graph, without any clique-subset or parity reduction."""
    adjacency = [((1 << k) - 1) ^ (1 << i) for i in range(k)]
    for i, n in enumerate(leaves):
        for _ in range(n):
            v = len(adjacency)
            adjacency.append(1 << i)
            adjacency[i] |= 1 << v
    for (i, j), n in pairs.items():
        for _ in range(n):
            v = len(adjacency)
            adjacency.append((1 << i) | (1 << j))
            adjacency[i] |= 1 << v
            adjacency[j] |= 1 << v

    @cache
    def grundy(mask):
        options = set()
        todo = mask
        while todo:
            bit = todo & -todo
            todo ^= bit
            i = bit.bit_length() - 1
            options.add(grundy(mask & ~(adjacency[i] | bit)))
        result = 0
        while result in options:
            result += 1
        return result

    return grundy((1 << len(adjacency)) - 1)


def check_star_centre_positive():
    k = 5
    pairs = list(combinations(range(1, 5), 2))
    checked = 0
    for multiplicities in product((1, 2), repeat=6):
        edge_counts = dict(zip(pairs, multiplicities))
        for centre_leaf in (1, 2):
            for other_leaves in product((0, 1, 2), repeat=4):
                leaves = (centre_leaf,) + other_leaves
                actual, predicted = quotient(k, edge_counts, leaves)
                assert actual == predicted, (edge_counts, leaves, actual, predicted)
                checked += 1
    assert checked == 10368
    print(f"PASS k=5 four-star with positive centre leaf: {checked} complete representatives")


def check_named_k6():
    k = 6
    all_pairs = list(combinations(range(k), 2))
    checked = 0
    for missing in K6_MISSING:
        edge_counts = {edge: 1 for j, edge in enumerate(all_pairs) if j not in missing}
        for leaves in ((0,) * k, (0, 1, 0, 1, 0, 1), (1,) * k):
            actual = named(k, edge_counts, leaves)
            via, predicted = quotient(k, edge_counts, leaves)
            assert actual == via == predicted, (missing, leaves, actual, via, predicted)
            checked += 1
    assert checked == 27
    print(f"PASS k=6 literal named-vertex checks: {checked}")


if __name__ == "__main__":
    check_star_centre_positive()
    check_named_k6()
