#!/usr/bin/env python3
"""Independent literal-vertex Node Kayles checks for all-positive private leaves.

No parity quotient is used in the recursion. Exact checks: all k=3
representatives and 96 deterministic k=4 representatives, plus k=2 witnesses.
"""
from functools import lru_cache
from itertools import product


def literal_grundy(k, leaves, pairs):
    adjacency = [(1 << k) - 1 - (1 << i) for i in range(k)]
    n = k

    def add_vertex(neighbors):
        nonlocal n
        adjacency.append(sum(1 << i for i in neighbors))
        for i in neighbors:
            adjacency[i] |= 1 << n
        n += 1

    for i in range(k):
        for _ in range(leaves[i]):
            add_vertex((i,))
    for (i, j), count in zip(((i, j) for i in range(k) for j in range(i + 1, k)), pairs):
        for _ in range(count):
            add_vertex((i, j))

    @lru_cache(None)
    def grundy(mask):
        seen = set()
        pending = mask
        while pending:
            bit = pending & -pending
            pending -= bit
            i = bit.bit_length() - 1
            seen.add(grundy(mask & ~(adjacency[i] | bit)))
        value = 0
        while value in seen:
            value += 1
        return value

    return grundy((1 << n) - 1)


def predicted(k, leaves, pairs):
    u = (sum(leaves) + sum(pairs)) & 1
    z = [x & 1 for x in leaves]
    for (i, j), count in zip(((i, j) for i in range(k) for j in range(i + 1, k)), pairs):
        z[i] ^= count & 1
        z[j] ^= count & 1
    return (1 ^ u ^ z[0]) if len(set(z)) == 1 else 2 + u


def main():
    checks = 0
    for k in (3, 4):
        pair_count = k * (k - 1) // 2
        tested = 0
        for leaves in product((1, 2), repeat=k):
            for pairs in product((0, 1, 2), repeat=pair_count):
                if k == 4:
                    # 96 representatives, covering every private-leaf parity.
                    pnum = sum(v * (3 ** i) for i, v in enumerate(pairs))
                    lnum = sum((v - 1) << i for i, v in enumerate(leaves))
                    if pnum not in ((lnum * 17 + 13 * j) % (3 ** pair_count) for j in range(6)):
                        continue
                actual = literal_grundy(k, leaves, pairs)
                expected = predicted(k, leaves, pairs)
                assert actual == expected, (k, leaves, pairs, actual, expected)
                tested += 1
        print(f"PASS literal k={k}: {tested} cases")
        checks += tested
    for leaves, pairs, expected, forecast in [((1, 1), (1,), 3, 0), ((2, 2), (2,), 2, 1)]:
        assert literal_grundy(2, leaves, pairs) == expected
        assert predicted(2, leaves, pairs) == forecast
    print(f"PASS total literal cases: {checks}; two k=2 sharpness witnesses")


if __name__ == '__main__':
    main()
