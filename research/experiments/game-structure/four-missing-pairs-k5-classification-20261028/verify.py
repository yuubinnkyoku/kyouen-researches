"""Complete parity/positivity quotient for k=5, exactly four absent pair types.

Independent named-vertex Node Kayles recurrence checks all six minimal
representatives, including the 11-vertex star counterexample.
"""
from functools import cache
from itertools import combinations, permutations, product

K = 5
PAIRS = list(combinations(range(K), 2))
PATTERNS = [
    ((0, 1), (0, 2), (0, 3), (0, 4)),
    ((0, 1), (0, 2), (0, 3), (1, 2)),
    ((0, 1), (0, 2), (0, 3), (1, 4)),
    ((0, 1), (0, 2), (1, 2), (3, 4)),
    ((0, 1), (0, 2), (1, 3), (2, 3)),
    ((0, 1), (0, 2), (1, 3), (2, 4)),
]


def quotient(counts):
    """Exact clique-mask mex; counts maps neighbor signatures to multiplicity."""
    active = [0] * (1 << K)
    z = [0] * K
    types = [sig for sig, value in counts.items() if value]
    for sig, value in counts.items():
        if value % 2:
            for mask in range(1, 1 << K):
                if sig & mask:
                    active[mask] ^= 1
            for i in range(K):
                if sig & (1 << i):
                    z[i] ^= 1
    dp = [0] * (1 << K)
    for mask in range(1, 1 << K):
        a = active[mask]
        seen = set()
        for i in range(K):
            if mask & (1 << i):
                seen.add(a ^ z[i])
        for sig in types:
            if sig & mask:
                nxt = mask & ~sig
                seen.add(dp[nxt] ^ a ^ active[nxt] ^ 1)
        g = 0
        while g in seen:
            g += 1
        dp[mask] = g
    u = active[-1]
    expected = (1 ^ u ^ z[0]) if len(set(z)) == 1 else 2 + u
    return dp[-1], expected


def named(leaves, edges):
    """Independent literal graph deletion (does not use clique quotient)."""
    nbr = [(1 << K) - 1 ^ (1 << i) for i in range(K)]
    for i, count in enumerate(leaves):
        for _ in range(count):
            j = len(nbr)
            nbr.append(1 << i)
            nbr[i] |= 1 << j
    for (i, j), count in edges.items():
        for _ in range(count):
            p = len(nbr)
            nbr.append((1 << i) | (1 << j))
            nbr[i] |= 1 << p
            nbr[j] |= 1 << p

    @cache
    def sg(mask):
        if not mask:
            return 0
        seen = set()
        todo = mask
        while todo:
            bit = todo & -todo
            i = bit.bit_length() - 1
            todo ^= bit
            seen.add(sg(mask & ~(nbr[i] | bit)))
        g = 0
        while g in seen:
            g += 1
        return g

    full = (1 << len(nbr)) - 1
    return sg(full), [sg(full & ~(nbr[i] | (1 << i))) for i in range(len(nbr))]


def main():
    seen = set()
    weighted = 0
    for index, missing in enumerate(PATTERNS):
        orbit = {
            tuple(sorted(tuple(sorted((perm[a], perm[b]))) for a, b in missing))
            for perm in permutations(range(K))
        }
        assert not (seen & orbit)
        seen |= orbit
        pairs = [p for p in PAIRS if p not in missing]
        assert len(pairs) == 6
        bad = 0
        dist = [0] * 4
        for vals in product((1, 2), repeat=6):
            base = {(1 << i) | (1 << j): val for (i, j), val in zip(pairs, vals)}
            for leaves in product((0, 1, 2), repeat=K):
                counts = dict(base)
                counts.update({1 << i: leaves[i] for i in range(K)})
                got, expected = quotient(counts)
                assert 0 <= got < 4
                dist[got] += 1
                bad += (got != expected)
                weighted += 1
        assert bad == (4856 if index == 0 else 0), (index, bad)
        if index == 0:
            assert dist == [492, 492, 7284, 7284], dist
        else:
            assert sum(dist) == 15552
        edges = {p: 1 for p in pairs}
        direct, children = named((0,) * K, edges)
        via, expected = quotient({(1 << i) | (1 << j): 1 for i, j in pairs})
        assert direct == via
        if index == 0:
            assert (direct, expected) == (3, 2)
            assert children[:K] == [0, 1, 1, 1, 1]
            assert children[K:] == [2] * 6
        print(f'pattern={index+1} orbit={len(orbit)} cases=15552 mismatches={bad} '
              f'distribution={dist} unweighted={direct} expected={expected}')
    assert len(seen) == 210
    assert weighted == 93312
    print('PASS six isomorphism classes, 210 labelled missing sets, '
          '93312 parity/positivity representatives; direct named checks 6')


if __name__ == '__main__':
    main()
