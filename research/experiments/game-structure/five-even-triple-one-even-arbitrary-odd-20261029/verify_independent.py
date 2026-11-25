"""Independent named-vertex Node Kayles audit for one even support type."""
from functools import lru_cache
from random import Random

TARGET = 7
TYPES = [s for s in range(1, 32) if s.bit_count() >= 2 and s != TARGET]


def named_grundy(odd_types, even_type, add_target):
    supports = [1 << c for c in range(5)] + list(odd_types)
    supports += [even_type] * 2 + [TARGET] * add_target
    n = 5 + len(supports)
    adjacency = [0] * n
    for c in range(5):
        adjacency[c] = ((1 << 5) - 1) ^ (1 << c)
    for i, s in enumerate(supports, 5):
        adjacency[i] = s
        for c in range(5):
            if s & (1 << c):
                adjacency[c] |= 1 << i

    @lru_cache(None)
    def g(mask):
        iso = 0
        for i in range(n):
            if (mask >> i) & 1 and not (adjacency[i] & mask):
                iso |= 1 << i
        parity = iso.bit_count() & 1
        mask ^= iso
        if not mask:
            return parity
        values = set()
        remaining = mask
        while remaining:
            bit = remaining & -remaining
            remaining ^= bit
            i = bit.bit_length() - 1
            values.add(g(mask & ~(adjacency[i] | bit)))
        ans = 0
        while ans in values:
            ans += 1
        return ans ^ parity

    return g((1 << n) - 1)


def quotient(odd_types, even_type, add_target):
    counts = [0] * 32
    for c in range(5):
        counts[1 << c] = 1
    for s in odd_types:
        counts[s] = 1
    counts[even_type] = 2
    counts[TARGET] = add_target
    p = [
        sum(counts[s] for s in range(1, 32) if s & r) & 1
        for r in range(32)
    ]
    g = [0] * 32
    for r in range(1, 32):
        vals = set()
        for c in range(5):
            if r & (1 << c):
                vals.add(p[r] ^ p[1 << c])
        for s in range(1, 32):
            if counts[s] and r & s:
                child = r & ~s
                vals.add(g[child] ^ p[r] ^ p[child] ^ 1)
        while g[r] in vals:
            g[r] += 1
    return g[31]


def main():
    rng = Random(20261029)
    cases = 0
    for even in TYPES:
        for k in (0, 1, 2, 4, 7, 10, 13, 17, 20, 24):
            odd = rng.sample([s for s in TYPES if s != even], k)
            for target in (0, 2):
                a = named_grundy(odd, even, target)
                b = quotient(odd, even, target)
                assert a == b, (even, k, target, a, b, odd)
                cases += 1
    print(f"PASS named_vs_quotient={cases}, paired_comparisons={cases // 2}")


if __name__ == "__main__":
    main()
