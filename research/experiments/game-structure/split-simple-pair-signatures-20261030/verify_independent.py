"""Independent named-vertex audit of degree-two split-graph witnesses and samples."""
from functools import lru_cache
from itertools import combinations
from random import Random

W6 = (10, 33, 33, 34, 36, 36, 48, 48)
W7 = (5, 5, 12, 12, 20, 20, 34, 66, 68)


def mex(values):
    v = 0
    while v in values:
        v += 1
    return v


def by_signature(k, signatures):
    """Center-subset recursion; isolated residual vertices are handled by xor."""
    parity = [sum(bool(s & x) for s in signatures) & 1 for x in range(1 << k)]
    values = [0] * (1 << k)
    for x in range(1, 1 << k):
        choices = {parity[x] ^ parity[1 << i] for i in range(k) if x & (1 << i)}
        for s in set(signatures):
            if s & x:
                y = x & ~s
                choices.add(values[y] ^ parity[x] ^ parity[y] ^ 1)
        values[x] = mex(choices)
    x = (1 << k) - 1
    children = [parity[x] ^ parity[1 << i] for i in range(k)]
    children += [values[x & ~s] ^ parity[x] ^ parity[x & ~s] ^ 1 for s in signatures]
    return values[x], tuple(children)


def by_named_vertices(k, signatures):
    """Direct closed-neighborhood deletion, without signature parity reduction."""
    n = k + len(signatures)
    adj = [0] * n
    for i in range(k):
        adj[i] = ((1 << k) - 1) ^ (1 << i)
    for j, s in enumerate(signatures):
        v = k + j
        adj[v] = s
        for i in range(k):
            if s & (1 << i):
                adj[i] |= 1 << v

    @lru_cache(None)
    def exact(mask):
        options = set()
        bits = mask
        while bits:
            bit = bits & -bits
            bits ^= bit
            v = bit.bit_length() - 1
            options.add(exact(mask & ~(bit | adj[v])))
        return mex(options)

    full = (1 << n) - 1
    children = tuple(exact(full & ~((1 << v) | adj[v])) for v in range(n))
    return exact(full), children, exact.cache_info().currsize


def check_witness(k, signatures, expected):
    assert all(s.bit_count() == 2 and 0 < s < (1 << k) for s in signatures)
    sig = by_signature(k, signatures)
    named = by_named_vertices(k, signatures)
    assert sig[0] == named[0] == expected
    assert sig[1] == named[1]
    assert set(sig[1]) == set(range(expected))
    for mask in range((1 << len(signatures)) - 1):
        sub = tuple(s for i, s in enumerate(signatures) if mask & (1 << i))
        assert by_signature(k, sub)[0] != expected
    print(f"k={k} witness g={expected} vertices={k+len(signatures)} "
          f"named_states={named[2]} proper_independent_subsets={2**len(signatures)-1}")
    print("children=", sig[1])


def main():
    check_witness(6, W6, 4)
    check_witness(7, W7, 5)
    expected = {
        2: (0, 2, 0, 0),
        3: (1, 1, 6, 0),
        4: (8, 8, 18, 30),
        5: (32, 32, 490, 470),
        6: (1024, 1024, 15345, 15375),
    }
    for k, histogram in expected.items():
        pairs = tuple(sum(1 << v for v in p) for p in combinations(range(k), 2))
        counts = [0, 0, 0, 0]
        for mask in range(1 << len(pairs)):
            signatures = tuple(s for i, s in enumerate(pairs) if mask & (1 << i))
            g, _ = by_signature(k, signatures)
            assert g < 4
            counts[g] += 1
        assert tuple(counts) == histogram, (k, counts)
        print(f"k={k} independent exhaustive histogram={tuple(counts)}")

    # K0336 compresses arbitrary equal-neighborhood multiplicities to 0,1,2.
    pairs5 = tuple(sum(1 << v for v in p) for p in combinations(range(5), 2))
    hist5 = [0, 0, 0, 0]
    for code in range(3 ** len(pairs5)):
        q = code
        signatures = []
        for s in pairs5:
            q, count = divmod(q, 3)
            signatures.extend([s] * count)
        g, _ = by_signature(5, tuple(signatures))
        assert g < 4
        hist5[g] += 1
    assert tuple(hist5) == (1744, 2225, 27465, 27615)
    print("k=5 arbitrary multiplicities: 59049 parity representatives,", tuple(hist5))

    rng = Random(20261030)
    for i in range(150):
        k = rng.randrange(2, 8)
        pairs = [sum(1 << v for v in pair) for pair in combinations(range(k), 2)]
        rng.shuffle(pairs)
        signatures = tuple(sorted(pairs[:rng.randrange(min(len(pairs), 12) + 1)]))
        a = by_signature(k, signatures)
        b = by_named_vertices(k, signatures)
        assert a == b[:2], (i, k, signatures, a, b)
        if k == 7:
            assert a[0] <= 3
    print("150 fixed-seed simple-pair samples: root and every first child agree")
    print("all independent checks passed")


if __name__ == "__main__":
    main()
