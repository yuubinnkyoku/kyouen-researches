"""Independent named-vertex and cycle-space audits for seven-center pair graphs."""
from functools import lru_cache
from itertools import combinations
from random import Random

K = 7
PAIRS = [(1 << a) | (1 << b) for a, b in combinations(range(K), 2)]
W4 = (3, 3, 5, 5, 9, 9, 17, 17, 65, 96)
W5 = (3, 3, 5, 5, 9, 9, 33, 48, 80)

def mex(values):
    x = 0
    while x in values:
        x += 1
    return x

def by_signature(signatures):
    parity = [sum(bool(s & x) for s in signatures) % 2 for x in range(1 << K)]
    g = [0] * (1 << K)
    for x in range(1, 1 << K):
        options = {parity[x] ^ parity[1 << i] for i in range(K) if x & (1 << i)}
        for s in set(signatures):
            if s & x:
                y = x & ~s
                options.add(g[y] ^ parity[x] ^ parity[y] ^ 1)
        g[x] = mex(options)
    return g[-1]

def by_named_vertices(signatures):
    n = K + len(signatures)
    adj = [0] * n
    for i in range(K):
        adj[i] = ((1 << K) - 1) ^ (1 << i)
    for j, s in enumerate(signatures):
        v = K + j
        adj[v] = s
        for i in range(K):
            if s & (1 << i):
                adj[i] |= 1 << v

    @lru_cache(None)
    def solve(mask):
        options = set()
        bits = mask
        while bits:
            bit = bits & -bits
            bits ^= bit
            v = bit.bit_length() - 1
            options.add(solve(mask & ~(bit | adj[v])))
        return mex(options)

    full = (1 << n) - 1
    children = [solve(full & ~((1 << i) | adj[i])) for i in range(n)]
    return solve(full), children, solve.cache_info().currsize

def cycle_space_histogram():
    # Eulerian odd-edge supports form a 15-dimensional binary cycle space.
    index = {edge: i for i, edge in enumerate(combinations(range(K), 2))}
    basis = []
    for a, b in combinations(range(1, K), 2):
        basis.append((1 << index[0, a]) |
                     (1 << index[0, b]) |
                     (1 << index[a, b]))
    assert len(basis) == 15
    support = previous = 0
    counts = [0, 0]
    for code in range(1 << 15):
        gray = code ^ (code >> 1)
        if code:
            support ^= basis[(gray ^ previous).bit_length() - 1]
        previous = gray
        w = support.bit_count()
        # Absent/doubled choices for every edge outside the odd support.
        counts[1 ^ (w & 1)] += 1 << (21 - w)
    assert counts == [82385617, 82695704], counts
    print("Cycle-space independent g=0/1 histogram:", counts)

def main():
    for expected, signatures in ((4, W4), (5, W5)):
        direct, children, states = by_named_vertices(signatures)
        assert direct == by_signature(signatures) == expected
        assert set(children) == set(range(expected))
        print(f"g={expected}, independent={len(signatures)}, "
              f"states={states}, children={children}")
    rng = Random(20261030)
    for case in range(200):
        signatures = []
        for s in rng.sample(PAIRS, rng.randrange(0, 11)):
            signatures.extend([s] * rng.choice((1, 1, 2)))
        a = by_signature(signatures)
        b, _, _ = by_named_vertices(signatures)
        assert a == b, (case, signatures, a, b)
    print("200 fixed-seed named-vertex comparisons: no mismatch")
    cycle_space_histogram()
    print("All independent checks passed")

if __name__ == "__main__":
    main()
